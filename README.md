# GrantDE

A lightweight scholarship directory for international students in Germany.
Browse funding opportunities, understand requirements and follow the official
provider's application link.

GrantDE combines a manually maintained JSON catalogue with a Python static-site
builder. Search and filtering run in the browser. Visitors need no account,
profile or application upload.

> **Development status:** the website works locally; the catalogue remains in
> draft review. This repository is not a published or fully verified directory.
> Public builds are blocked until reviewed records and deployment details exist.

## Features

- Search, study-related filters, sorting and paginated scholarship cards.
- Detailed funding, requirements, application rounds and official source links.
- Responsive layouts, keyboard controls and a saved light/dark theme.
- Matching counts when searching or filtering, without promotional catalogue totals.
- Static HTML browsing before JavaScript enhancement.
- Schema validation, provenance checks and guarded preview/public builds.
- Local assets, with no analytics or third-party browser scripts.

## Run locally

Requires Python 3.11 or newer. No npm install or database server is needed.

```sh
git clone https://github.com/faheem-shah-umer/GrantDE.git
cd GrantDE
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Install the pinned dependencies and start the preview:

```sh
python -m pip install --upgrade -r requirements-dev.txt
python -m pip install --no-build-isolation --no-deps -e .
python -m grantde.preview
```

Open [localhost:8000](http://127.0.0.1:8000/). Use `--port 8001` if needed.
The preview includes clearly labelled drafts, binds to loopback and writes only
to ignored `build/preview/`. Stop it with Ctrl+C.

## Work with the catalogue

```sh
python -m grantde.validate
python -m grantde.normalise check
python -m grantde.report --output docs/CATALOGUE_REPORT.md --check
python -m grantde.build --preview
```

Edit records in `data/scholarships/`. Validation checks structure, controlled
values, identities, dates, URL syntax and source references. It does not verify
that a provider's offer is still current. Review official sources before
approving a record. Tests and temporary verification artifacts are intentionally
excluded from this repository; CI validates the catalogue, JavaScript syntax,
dependency consistency and preview build.

## Repository layout

```text
data/          Scholarship records, schema and provenance metadata
docs/          Product, design, build and editorial review guides
scripts/       Reusable catalogue audit command
src/grantde/   Validation, maintenance and static-site commands
static/        CSS, JavaScript and icons
templates/     Autoescaped Jinja templates
.github/       Validation workflow and dependency updates
```

Raw third-party captures stay in ignored local editorial storage. The public
registry retains source IDs and original checksums without redistributing full
pages. Neither those registries nor internal review notes enter website output.

## Deployment

The intended target is Cloudflare Pages, using GitHub as the source repository.
Hosting and a custom domain are not configured by this repository setup.

Copy `site.example.json` to ignored `site.json` when preparing deployment. Fill
in the base URL, corrections URL and actual operator details outside Git, then
complete the publication review and hosting-specific privacy information.

```sh
python -m grantde.build
```

A successful public build produces `dist/`. The build refuses to publish drafts
or replace an unrelated directory. Do not deploy `build/preview/` as the live
website. See [the build guide](docs/BUILD.md) for configuration and safeguards.

## Documentation

- [Project specification](PROJECT_SPEC.md)
- [Visual design](docs/DESIGN.md)
- [Data maintenance](docs/DATA_MAINTENANCE.md)
- [Editorial review and open questions](docs/audits/2026-10-24/REVIEW.md)
- [Roadmap](docs/ROADMAP.md)
- [Contributing](CONTRIBUTING.md) and [security](SECURITY.md)

## Licence

GrantDE's original code and documentation use the [MIT licence](LICENSE).
Provider material and dependencies retain their own rights; see
[third-party notices](THIRD_PARTY_NOTICES.md).
