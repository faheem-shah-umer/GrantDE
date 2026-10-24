# Maintaining the catalogue

## Edit the working records

Use `data/scholarships/<id>.json`. Keep existing IDs and slugs stable; renaming them
would break references and future detail-page URLs. Add new application rounds
instead of overwriting historical rounds. Do not infer a future deadline from an
earlier year's schedule.

Keep `PROJECT_SPEC.md` as the product specification. The repository currently
implements data maintenance and a local static website; public release preparation
is tracked in `ROADMAP.md`.

## Preserve uncertainty

- `restricted` means the source establishes a restriction. Read structured values,
  notes, mandatory requirements and exceptions together.
- `unrestricted` means the source explicitly establishes no restriction. It must
  never be inferred from missing information.
- `unknown` means the evidence does not establish a complete rule. A nationality
  record may retain partial country information while still being unknown.
- `null` means unconfirmed or not applicable, interpreted with the associated status.
  Do not replace it with an empty list to imply unrestricted eligibility.

The supplied schema enforces the distinction for degree, subject, institution and
residence criteria. Nationality can use explicit country codes, exclusions and
free-text country groups. These groups include incomplete or contextual rules;
they must not be treated as a complete machine-readable country allowlist.
Additional requirements, preferences and exceptions are separate fields.

## Keep evidence traceable

Each rule's `source_ids` must refer to a source declared in that scholarship's
`provenance.sources`. Each declared source must exist in a bundle registered under
`evidence_files` in `data/catalogue.json`.

The public source registry is in `data/sources.json` and `data/evidence/`.
Keep full raw captures in ignored `.local/evidence/`. To register new evidence,
save metadata in a new file such as `data/evidence/provider-2026-11-01.json`:

```json
{
  "sources": {
    "provider-2026-11-01": {
      "original_capture_sha256": "SHA256_OF_THE_ORIGINAL_CAPTURE_BYTES",
      "registry_format": "metadata-only",
      "data": {"content_omitted": true}
    }
  }
}
```

This is a structural example, not a real record. Compute the checksum from the
private original capture and use a new source ID for a changed capture. Preserve
any `derived_from_ref` in the metadata. Register the bundle's relative path in `evidence_files`, then
add the source's URL, title, check date, checksum and `snapshot_ref` to the record.
Keep older evidence when updating a record.

The validator checks that each record's source checksum agrees with
`original_capture_sha256` and that derived captures have their saved parent source. The original
standalone retrieval files are not present, so those individual historical hashes
cannot be recomputed from the parsed embedded JSON. A checksum agreement is not
proof that a source claim is correct.

The 24 October 2026 review captures declare a canonical JSON checksum encoding.
Those checksums can be recomputed from the private payload using the declared
UTF-8/indent/newline convention. They identify the retrieval payload, not the
provider's original HTTP bytes. The public projection deliberately omits those
payloads; exporting it does not restore the original captures.

## Review before publication

1. Read the official source and confirm the programme identity and study scope.
2. Check nationality, residence, language, academic and additional requirements.
3. Confirm funding, application documents, official links and each current round.
4. Update the checked/reviewed dates honestly and resolve editorial review notes.
5. Run validation and formatting checks; regenerate the coverage report.
6. Review the diff, then change `publication.status` to `published` when approved.

At initial import, all 185 records were drafts: 42 recorded `assistant_source_review`
and 143 recorded `extracted_draft`. Current counts are generated in
`CATALOGUE_REPORT.md`; later review batches are documented under `audits/`.
Review-method labels do not constitute publication approval. The validator prevents publishing an extracted draft, a
record without a review date, or a record with unresolved review notes. It cannot
determine whether a maintainer's editorial review was sufficient.

Availability is recorded **as of** the date on each round. Validation does not
refresh it automatically, fetch provider pages, convert unknown dates or guarantee
eligibility. The website derives date-sensitive presentation from confirmed dates
and displays unconfirmed dates honestly.

## Editorial audit queue

```powershell
.\.venv\Scripts\python.exe scripts\audit_catalogue.py --as-of 2026-10-24 --output docs\audits\2026-10-24\catalogue-audit.json
```

This offline triage lists unknown fields, review notes, near deadlines and shared
source URLs for every record. P1 indicates time sensitivity or a missing programme
destination; it does not establish an incorrect record. Variable awards may
correctly lack a single numeric amount. A shared source URL does not establish a
duplicate, and historical rounds must remain intact.

The first live batch, its supported changes and unresolved provider conflicts are
documented in `audits/2026-10-24/REVIEW.md`. Review the report and record diffs before
selecting entries for publication.

## Import and export

The active catalogue has already been organised. If a combined export is needed,
generate one explicitly and import it into a **new** folder:

```powershell
.\.venv\Scripts\python.exe -m grantde.export
.\.venv\Scripts\python.exe -m grantde.normalise import build/editorial-catalogue.json --data-dir build/reimported-data
```

Import refuses to overwrite an existing destination and validates a staged copy
before installing the new catalogue. Formatting operates on working records,
the manifest, schema and vocabularies only; it never rewrites captured evidence.

`grantde-export` produces `build/editorial-catalogue.json`, combining current records,
registered sources, schema and vocabularies. Counts and publication status are
computed from the active catalogue. Exports are optional, generated files; they
are not another active database. Import creates individual records and a source
registry without retaining a duplicate combined file.

Exports contain the registered source metadata, not omitted raw captures. Raw
captures are retained in ignored `.local/evidence/` storage on the editorial
machine. They are not required to build a preview from a fresh clone. Never
commit them or treat a public metadata-only export as a full evidence backup.
