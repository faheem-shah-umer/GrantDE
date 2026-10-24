"""Export the working catalogue and registered source metadata."""

import argparse
import sys
from pathlib import Path

from .catalogue import Catalogue, CatalogueError, load_catalogue, write_json
from .validate import require_valid


def export_bundle(catalogue: Catalogue) -> dict:
    statuses = {record["publication"]["status"] for _, record in catalogue.records}
    return {
        "metadata": {
            "format": "GrantDE scholarship database",
            "schema_version": catalogue.manifest["schema_version"],
            "collected_on": catalogue.manifest["collected_on"],
            "scholarship_count": len(catalogue.records),
            "source_document_count": len(catalogue.sources),
            "exhaustive": False,
            "publication_status": next(iter(statuses)) if len(statuses) == 1 else "mixed",
        },
        "scholarships": [record for _, record in catalogue.records],
        "sources": catalogue.sources,
        "field_definitions": {
            "scholarship_schema": catalogue.schema,
            "vocabularies": catalogue.vocabularies,
        },
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("build/editorial-catalogue.json"))
    args = parser.parse_args(argv)
    try:
        catalogue = load_catalogue(args.data_dir)
        require_valid(catalogue)
        if args.output.resolve().is_relative_to(catalogue.root) or args.output.suffix != ".json":
            raise CatalogueError("export must use a .json path outside data/ to protect working records and evidence")
        write_json(args.output, export_bundle(catalogue))
    except (CatalogueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Exported {len(catalogue.records)} records to {args.output} (editorial backup; not public website data).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
