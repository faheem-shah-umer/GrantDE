"""Import an initial collection or check the formatting of working JSON files."""

import argparse
import sys
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from jsonschema import Draft202012Validator, FormatChecker, SchemaError

from .catalogue import (
    CatalogueError, json_text, load_catalogue, read_json, working_json_paths, write_json,
)
from .validate import require_valid


def import_collection(source: Path, destination: Path) -> None:
    if destination.exists():
        raise CatalogueError(f"{destination}: import requires a new directory; existing work will not be overwritten")
    bundle = read_json(source)
    try:
        metadata = bundle["metadata"]
        schema = bundle["field_definitions"]["scholarship_schema"]
        vocabularies = bundle["field_definitions"]["vocabularies"]
        records = bundle["scholarships"]
        sources = bundle["sources"]
        collected_on = metadata["collected_on"]
        date.fromisoformat(collected_on)
    except (KeyError, TypeError, ValueError) as error:
        raise CatalogueError(f"{source}: not a supported GrantDE collection: {error}") from error
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise CatalogueError(f"{source}: invalid record schema: {error.message}") from error
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for index, record in enumerate(records):
        error = next(validator.iter_errors(record), None)
        if error:
            raise CatalogueError(f"{source}/scholarships/{index}: {error.message}")
    if metadata["scholarship_count"] != len(records) or metadata["source_document_count"] != len(sources):
        raise CatalogueError(f"{source}: metadata counts do not match the collection")
    for key in ("id", "slug"):
        values = [record[key] for record in records]
        if len(values) != len(set(values)):
            raise CatalogueError(f"{source}: duplicate scholarship {key}s")

    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".grantde-import-", dir=destination.parent) as temporary:
        staging = Path(temporary) / "catalogue"
        write_json(staging / "catalogue.json", {
            "format": "GrantDE working catalogue",
            "schema_version": "2.0.0",
            "collected_on": collected_on,
            "records": "scholarships",
            "schema": "schema/scholarship.schema.json",
            "vocabularies": "schema/vocabularies.json",
            "evidence_files": ["sources.json"],
        })
        write_json(staging / "sources.json", {"sources": sources})
        write_json(staging / "schema/scholarship.schema.json", schema)
        write_json(staging / "schema/vocabularies.json", vocabularies)
        for record in records:
            write_json(staging / "scholarships" / f"{record['id']}.json", record)
        require_valid(load_catalogue(staging))
        staging.rename(destination)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    importing = commands.add_parser("import", help="split a collection into a new data directory")
    importing.add_argument("source", type=Path)
    importing.add_argument("--data-dir", type=Path, default=Path("data"))
    for name in ("check", "format"):
        command = commands.add_parser(name, help=f"{name} UTF-8, indentation and newlines")
        command.add_argument("--data-dir", type=Path, default=Path("data"))
    args = parser.parse_args(argv)
    try:
        if args.command == "import":
            import_collection(args.source, args.data_dir)
            print(f"Imported records and source evidence into {args.data_dir}.")
            return 0
        catalogue = load_catalogue(args.data_dir)
        require_valid(catalogue)
        changed = []
        for path in working_json_paths(catalogue):
            expected = json_text(read_json(path)).encode("utf-8")
            if path.read_bytes() != expected:
                changed.append(path)
                if args.command == "format":
                    path.write_bytes(expected)
        if changed and args.command == "check":
            for path in changed:
                print(f"{path}: run grantde-normalise format", file=sys.stderr)
            return 1
        state = "updated" if changed else "clean"
        print(f"Formatting {state}: {len(changed)} changed files; source evidence left intact.")
        return 0
    except (CatalogueError, OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
