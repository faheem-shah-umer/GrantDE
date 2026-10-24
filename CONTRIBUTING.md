# Contributing

Read [the project specification](PROJECT_SPEC.md) and
[data maintenance guide](docs/DATA_MAINTENANCE.md) before changing records.
Use official sources, concise original summaries and explicit unknown values.
Preserve stable IDs and historical rounds. Keep records as drafts until their
publication review is complete.

After following the README setup, run:

```sh
python -m grantde.validate
python -m grantde.normalise check
python -m grantde.report --output docs/CATALOGUE_REPORT.md --check
python -m pip check
python -m grantde.build --preview
```

Use Node.js 22 or newer to check changed JavaScript with `node --check`.
Describe changed facts and their official sources. Add new captures only to
ignored local editorial storage; public registry entries contain metadata and
checksums. Do not redistribute scraped pages or documents without a rights review.

Before committing, inspect `git diff --cached`. Keep credentials, operator details,
local environments, tests, temporary scripts, generated output and raw captures
out of Git. Maintained local regression suites are intentionally not distributed.
See [SECURITY.md](SECURITY.md) for sensitive reports and secret handling.
