# Build and local preview

Run commands from the repository root, after installing the pinned dependencies
from `requirements-dev.txt` as described in the main README.

## One-command local website

```powershell
.\.venv\Scripts\python.exe -m grantde.preview
```

The command validates the catalogue, generates the draft preview and serves
`build/preview/` at `http://127.0.0.1:8000/`. It binds to the loopback interface only.
Use `--port 8001` to select another port; Ctrl+C stops the server. The installed
shortcut is `grantde-preview` after reinstalling the editable local package.

For a build without a server:

```powershell
.\.venv\Scripts\python.exe -m grantde.build --preview
```

An explicit `--as-of 2026-10-23` makes date-dependent generation reproducible.
Otherwise the build uses the machine's current calendar date. Interactive directory
availability is recalculated in the browser using the date in Europe/Berlin.
Availability is currently evaluated at calendar-date granularity; review exact
deadline-time handling before adding timed calls to a launch catalogue.

## What is generated

- Home, directory, scholarship detail, About/coverage, corrections, privacy,
  operator-information and 404 pages.
- Twelve static scholarship cards per directory page; with the initial data this
  produces 16 directory pages and 207 HTML pages overall.
- Local CSS, small JavaScript modules and a content-named JSON filter index.
- A robots file and Cloudflare-compatible `_headers`. Public builds also include
  a sitemap and canonical links from the configured base URL.

HTML pagination and detail links work before JavaScript enhancement. If the index
fails to load, the static directory remains available with an explanatory message.
The filter module is independent of the interface and can be checked separately.

The header's moon/sun button switches every page between light and dark themes.
A small script applies the saved theme before CSS loads; without a saved choice,
the system colour preference is used. Only the appearance preference is stored
across browser visits. The theme can still be toggled if storage is unavailable.

Nationality is descriptive information on scholarship pages. It is not a filter,
and a nationality value saved by an earlier version is discarded when restoring
directory controls. Other supported selections can still be restored.

The build validates every internal HTML link and source anchor before replacing
the previous generated output. Existing output must carry GrantDE's build marker;
arbitrary user folders are refused. Only resolved paths inside `build/` (or `dist/`
for public output) can be replaced. Source data, templates and research evidence
are never part of that cleanup.

The Jinja environment uses explicit autoescaping and `StrictUndefined`, following
the [official Jinja API](https://jinja.palletsprojects.com/en/stable/api/). Collected
text remains text. Browser-created cards use DOM text nodes rather than treating
source strings as HTML.

## Draft preview and public build

Preview is explicit: `--preview` includes drafts, labels the pages and discourages
indexing. Archived records are excluded. Preview output is restricted to `build/`;
the command cannot place draft pages in `dist/`.

```powershell
.\.venv\Scripts\python.exe -m grantde.build
```

The public command fails with an actionable message while there are no published
records. It also requires actual `base_url`, `corrections_url`, `operator_name`,
`operator_address` and `operator_email` values in `site.json`. The null values in
`site.example.json` support local development and block public generation. Copy
it to ignored `site.json` before supplying deployment configuration. Do not commit
operator details or credentials. The builder uses the example when no local file exists.
Approving a record still requires the manual review process in `DATA_MAINTENANCE.md`.

Public pages and the public index are constructed from selected records. Internal
review notes, raw source captures, retrieval metadata and the source registry are
not copied to the generated site. The catalogue JSON files keep their original
publication status; building the website never edits records.

## Verification for this milestone

On Windows with Python 3.11 and the pinned dependency set:

```powershell
.\.venv\Scripts\python.exe -m grantde.build --preview --as-of 2026-10-23
```

Local regression suites, excluded from the public repository, covered data integrity, generated links, complete static
pagination, escaped text, publication selection, safe output replacement and
unknown/conditional matching. Browser inspection covers search, multi-value degree
filtering, sorting, pagination, detail navigation, returning selections, mobile
filter drafts/Apply/Cancel, empty-state recovery and reset. Desktop and 320 px
layouts were inspected in the in-app browser. Browser console checks showed no
warnings or errors during those interactions.

The generated `.grantde-build.json` records compressed CSS, JavaScript and index
sizes for each build. These are gzip measurements of local output, without network
or device simulation. They do not establish LCP, INP, CLS or mobile filter/render
latency. Native HTML pagination is checked from the generated output; a separate
browser session with JavaScript disabled remains part of broader release testing.

Provider links were validated syntactically during website implementation. A
separate source-review batch on 24 October 2026 checked twelve records against
official pages and linked documents; see `audits/2026-10-24/REVIEW.md` for its scope
and unresolved questions. That does not establish live accuracy for the full
catalogue. All records remain drafts, and public deployment is pending.
