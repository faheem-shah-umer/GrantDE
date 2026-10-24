"""Describe the current catalogue coverage without implying publication readiness."""

import argparse
import sys
from collections import Counter
from pathlib import Path

from .catalogue import Catalogue, CatalogueError, load_catalogue
from .validate import require_valid


def catalogue_report(catalogue: Catalogue) -> str:
    records = [record for _, record in catalogue.records]
    rounds = [round_ for record in records for round_ in record["application_rounds"]]
    lines = [
        "# Catalogue report", "",
        "Generated from the working records with `grantde-report`. Counts are descriptive;",
        "validation does not establish eligibility, current availability or editorial accuracy.", "",
        f"- Initial collection date: {catalogue.manifest['collected_on']}.",
        f"- Scholarship records: {len(records)}.",
        f"- Saved source documents: {len(catalogue.sources)}.",
        f"- Application rounds, including past and unconfirmed rounds: {len(rounds)}.",
        "- Coverage is not exhaustive.", "",
    ]

    def table(title, counts):
        lines.extend([f"## {title}", "", "| Value | Count |", "| --- | ---: |"])
        lines.extend(f"| {key} | {count} |" for key, count in sorted(counts.items()))
        lines.append("")

    table("Publication status", Counter(r["publication"]["status"] for r in records))
    table("Recorded review method", Counter(r["provenance"]["review_method"] for r in records))
    lines.extend([
        "`assistant_source_review` records an earlier assistant review of captured material.",
        "It does not mean a maintainer has approved publication. `extracted_draft` needs source review.", "",
    ])
    table("Application availability recorded on each round", Counter(r["availability"] for r in rounds))
    lines.extend([
        "These are historical observations as of each round's `as_of` date, not a live open/closed check.",
        "Multiple rounds can belong to one scholarship. Earlier rounds are retained.", "",
    ])
    unknowns = {
        "Degree levels": sum(r["study_scope"]["degree_levels"]["status"] == "unknown" for r in records),
        "Subject areas": sum(r["study_scope"]["subject_areas"]["status"] == "unknown" for r in records),
        "Nationality": sum(r["applicant_requirements"]["nationality"]["status"] == "unknown" for r in records),
        "Residence": sum(r["applicant_requirements"]["residence"]["status"] == "unknown" for r in records),
        "Required documents": sum(r["application_process"]["required_documents_status"] == "unknown" for r in records),
    }
    table("Unknown information by scholarship", unknowns)
    titles = Counter((r["title"].strip().casefold(), r["provider"]["name"].strip().casefold()) for r in records)
    duplicates = sum(count > 1 for count in titles.values())
    lines.extend([
        "## Review workload", "",
        f"- Records with outstanding editorial notes: {sum(bool(r['publication']['review_notes']) for r in records)}.",
        f"- Repeated title/provider pairs needing manual duplicate review: {duplicates}.",
        "- Check free-text country groups, exceptions and additional requirements before implementing matching.",
        "- Review source summaries, funding, application links and time-sensitive dates before publication.",
        "- Structural checks are offline; no live provider links were rechecked when generating this report.", "",
    ])
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true", help="fail if --output is missing or out of date")
    args = parser.parse_args(argv)
    if args.check and args.output is None:
        parser.error("--check requires --output")
    try:
        catalogue = load_catalogue(args.data_dir)
        require_valid(catalogue)
        report = catalogue_report(catalogue)
        if args.check:
            if not args.output.is_file() or args.output.read_bytes() != report.encode("utf-8"):
                raise CatalogueError(f"{args.output}: report is out of date; regenerate it with grantde-report --output")
            print(f"Report is current: {args.output}")
        elif args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8", newline="\n")
            print(f"Wrote {args.output}")
        else:
            print(report, end="")
    except (CatalogueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
