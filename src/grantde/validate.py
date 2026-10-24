"""Validate record structure, cross-record identity and saved evidence."""

import argparse
import re
import sys
from datetime import date, time
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker, SchemaError

from .catalogue import Catalogue, CatalogueError, load_catalogue


def _walk(value, path=""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            yield key, child, child_path
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}/{index}")


def _valid_url(value: str) -> bool:
    try:
        url = urlsplit(value)
        return bool(
            url.scheme in {"http", "https"}
            and url.hostname and not url.username and not url.password
            and not any(char.isspace() or ord(char) < 32 for char in value)
        )
    except ValueError:
        return False


def validate_catalogue(catalogue: Catalogue) -> list[str]:
    errors = []
    try:
        Draft202012Validator.check_schema(catalogue.schema)
    except SchemaError as error:
        return [f"schema: {error.message}"]
    validator = Draft202012Validator(catalogue.schema, format_checker=FormatChecker())
    properties = catalogue.schema.get("properties", {})
    try:
        scope = properties["study_scope"]["properties"]
        requirements = properties["applicant_requirements"]["properties"]
        expected_vocabularies = {
            "degree_levels": scope["degree_levels"]["properties"]["values"]["items"]["enum"],
            "subject_areas": scope["subject_areas"]["properties"]["values"]["items"]["enum"],
            "residence_situations": requirements["residence"]["properties"]["values"]["items"]["enum"],
            "funding_purposes": properties["funding"]["properties"]["covered_costs"]["items"]["enum"],
            "criterion_statuses": scope["degree_levels"]["properties"]["status"]["enum"],
        }
    except (KeyError, TypeError):
        return ["schema: required GrantDE criterion definitions are missing"]
    for name, expected in expected_vocabularies.items():
        if catalogue.vocabularies.get(name) != expected:
            errors.append(f"vocabularies/{name}: values must agree with the record schema")
    try:
        date.fromisoformat(catalogue.manifest["collected_on"])
    except (ValueError, TypeError):
        errors.append("catalogue/collected_on must be an ISO calendar date")
    for source_id, capture in catalogue.sources.items():
        for key, pointer, location in _walk(capture):
            if key == "derived_from_ref":
                prefix = "#/sources/"
                if not isinstance(pointer, str) or not pointer.startswith(prefix):
                    errors.append(f"sources/{source_id}{location}: expected a saved source pointer")
                    continue
                parent_id = pointer[len(prefix):].replace("~1", "/").replace("~0", "~")
                if parent_id not in catalogue.sources:
                    errors.append(f"sources/{source_id}{location}: missing parent source {parent_id!r}")
    if not catalogue.records:
        errors.append("scholarships: no records found; an empty catalogue may indicate the wrong data directory")

    ids, slugs = {}, {}
    for path, record in catalogue.records:
        label = path.relative_to(catalogue.root).as_posix()
        schema_errors = sorted(validator.iter_errors(record), key=lambda e: str(list(e.path)))
        for error in schema_errors:
            location = "/".join(str(part) for part in error.path)
            errors.append(f"{label}/{location}: {error.message}")
        if schema_errors:
            continue
        for key, seen in (("id", ids), ("slug", slugs)):
            value = record[key]
            if value in seen:
                errors.append(f"{label}/{key}: duplicate {value!r}; also in {seen[value]}")
            seen[value] = label
        if path.stem != record["id"]:
            errors.append(f"{label}/id: filename must be {record['id']}.json")

        declared = [source["id"] for source in record["provenance"]["sources"]]
        if len(declared) != len(set(declared)):
            errors.append(f"{label}/provenance/sources: duplicate source IDs")
        for key, value, location in _walk(record):
            if key == "source_ids":
                for source_id in value:
                    if source_id not in declared:
                        errors.append(f"{label}{location}: undeclared source ID {source_id!r}")
            if key in {"url", "official_programme_url", "application_url"} and value is not None:
                if not _valid_url(value):
                    errors.append(f"{label}{location}: expected an absolute HTTP(S) URL without credentials")

        for source in record["provenance"]["sources"]:
            prefix = f"{label}/provenance/sources/{source['id']}"
            capture = catalogue.sources.get(source["id"])
            if capture is None:
                errors.append(f"{prefix}: source capture not found in evidence_files")
            elif source["sha256"] != capture.get("original_capture_sha256"):
                errors.append(f"{prefix}/sha256: does not match the saved capture checksum")
            escaped_id = source["id"].replace("~", "~0").replace("/", "~1")
            if source["snapshot_ref"] != f"#/sources/{escaped_id}":
                errors.append(f"{prefix}/snapshot_ref: must point to its own saved source ID")

        nationality = record["applicant_requirements"]["nationality"]
        fields = ("allowed_country_codes", "excluded_country_codes", "country_groups")
        if nationality["status"] == "unrestricted" and any(nationality[key] is not None for key in fields):
            errors.append(f"{label}/applicant_requirements/nationality: unrestricted criteria must use null restrictions")
        overlap = set(nationality["allowed_country_codes"] or []) & set(nationality["excluded_country_codes"] or [])
        if overlap:
            errors.append(
                f"{label}/applicant_requirements/nationality: countries both allowed and excluded: {sorted(overlap)}"
            )

        funding = record["funding"]
        if (
            funding["amount_min"] is not None and funding["amount_max"] is not None
            and funding["amount_min"] > funding["amount_max"]
        ):
            errors.append(f"{label}/funding: amount_min exceeds amount_max")

        rounds = set()
        for round_ in record["application_rounds"]:
            prefix = f"{label}/application_rounds/{round_['id']}"
            if round_["id"] in rounds:
                errors.append(f"{prefix}: duplicate application round ID within this scholarship")
            rounds.add(round_["id"])
            if round_["opens_on"] and round_["deadline"] and round_["opens_on"] > round_["deadline"]:
                errors.append(f"{prefix}: opening date is later than the deadline")
            if round_["deadline_time"]:
                try:
                    time.fromisoformat(round_["deadline_time"])
                except ValueError:
                    errors.append(f"{prefix}/deadline_time: invalid time of day")
                if not round_["deadline"] or not round_["timezone"]:
                    errors.append(f"{prefix}: a deadline time requires a date and timezone")
            if round_["timezone"] and not re.fullmatch(r"[A-Za-z_]+(?:/[A-Za-z0-9_+.-]+)+|UTC", round_["timezone"]):
                errors.append(f"{prefix}/timezone: expected an IANA timezone name")

        if record["publication"]["status"] == "published":
            if not record["provenance"]["last_reviewed"]:
                errors.append(f"{label}/provenance/last_reviewed: required before publication")
            if record["provenance"]["review_method"] == "extracted_draft":
                errors.append(
                    f"{label}/provenance/review_method: extracted drafts require source review before publication"
                )
            if record["publication"]["review_notes"]:
                errors.append(f"{label}/publication/review_notes: resolve outstanding review notes before publication")
    return errors


def require_valid(catalogue: Catalogue) -> None:
    errors = validate_catalogue(catalogue)
    if errors:
        raise CatalogueError("\n".join(errors))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    args = parser.parse_args(argv)
    try:
        catalogue = load_catalogue(args.data_dir)
        require_valid(catalogue)
    except (CatalogueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    published = sum(r["publication"]["status"] == "published" for _, r in catalogue.records)
    print(f"Valid: {len(catalogue.records)} scholarships, {len(catalogue.sources)} saved sources, {published} published.")
    print("Offline structure and evidence checks only; provider links and editorial accuracy need separate review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
