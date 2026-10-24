# Catalogue data

- `scholarships/` is the active database: one JSON record per scholarship.
- `schema/` contains the JSON Schema and controlled vocabularies.
- `catalogue.json` identifies the working paths and registered source bundles.
- `sources.json` and `evidence/` contain metadata-only provenance registries.

Records retain official URLs, retrieval dates, source identifiers and original
capture checksums. Registry entries explicitly mark omitted content. Full raw
captures are preserved in ignored `.local/evidence/` on the editorial machine;
they are not redistributed through Git. Checksums identify those original
captures, rather than the metadata-only projection.

`snapshot_ref` pointers resolve through the registered source objects. Derived
source references remain intact. Validation checks registry membership, matching
stored checksums and source relationships; it does not recompute omitted payloads
or establish current provider accuracy.

The public website build selects published records and constructs a small public
index. It excludes raw captures, source registries and internal review notes.
See [third-party notices](../THIRD_PARTY_NOTICES.md) and the
[data maintenance guide](../docs/DATA_MAINTENANCE.md).
