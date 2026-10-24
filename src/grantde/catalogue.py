"""Read the working records and the collection evidence they reference."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class CatalogueError(ValueError):
    pass


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise CatalogueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise CatalogueError(f"non-finite JSON number: {value}")


def read_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8-sig"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, ValueError) as error:
        raise CatalogueError(f"{path}: {error}") from error


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_text(value), encoding="utf-8", newline="\n")


def data_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name:
        raise CatalogueError("catalogue paths must be nonempty relative paths")
    candidate = (root / name).resolve()
    if Path(name).is_absolute() or not candidate.is_relative_to(root.resolve()):
        raise CatalogueError(f"catalogue path escapes the data directory: {name}")
    return candidate


@dataclass
class Catalogue:
    root: Path
    manifest: dict
    schema: dict
    vocabularies: dict
    records: list[tuple[Path, dict]]
    sources: dict[str, dict]


def load_catalogue(root: Path) -> Catalogue:
    root = root.resolve()
    manifest = read_json(root / "catalogue.json")
    required = {"schema_version", "collected_on", "records", "schema", "vocabularies", "evidence_files"}
    if not isinstance(manifest, dict) or not required.issubset(manifest):
        raise CatalogueError(f"{root / 'catalogue.json'}: incomplete catalogue manifest")
    if manifest["schema_version"] != "2.0.0":
        raise CatalogueError("unsupported catalogue schema_version; expected 2.0.0")
    evidence_files = manifest["evidence_files"]
    if not isinstance(evidence_files, list) or not evidence_files or not all(isinstance(p, str) for p in evidence_files):
        raise CatalogueError("evidence_files must be a nonempty list of relative JSON paths")
    if len(evidence_files) != len(set(evidence_files)):
        raise CatalogueError("evidence_files contains duplicate paths")

    schema = read_json(data_path(root, manifest["schema"]))
    vocabularies = read_json(data_path(root, manifest["vocabularies"]))
    if not isinstance(vocabularies, dict):
        raise CatalogueError("vocabularies must be an object of controlled-value lists")
    records_directory = data_path(root, manifest["records"])
    if not records_directory.is_dir():
        raise CatalogueError(f"record directory not found: {records_directory}")
    records = [(p, read_json(p)) for p in sorted(records_directory.glob("*.json"))]

    sources = {}
    for name in evidence_files:
        bundle = read_json(data_path(root, name))
        if not isinstance(bundle, dict) or not isinstance(bundle.get("sources"), dict):
            raise CatalogueError(f"{name}: evidence bundle must contain a sources object")
        for source_id, capture in bundle["sources"].items():
            if not isinstance(capture, dict):
                raise CatalogueError(f"{name}: source {source_id!r} must be an object")
            if source_id in sources and sources[source_id] != capture:
                raise CatalogueError(f"{name}: conflicting capture for source ID {source_id!r}")
            sources[source_id] = capture
    return Catalogue(root, manifest, schema, vocabularies, records, sources)


def working_json_paths(catalogue: Catalogue) -> list[Path]:
    return [
        catalogue.root / "catalogue.json",
        data_path(catalogue.root, catalogue.manifest["schema"]),
        data_path(catalogue.root, catalogue.manifest["vocabularies"]),
        *(path for path, _ in catalogue.records),
    ]
