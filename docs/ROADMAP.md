# Implementation roadmap

The full requirements and acceptance criteria are in `PROJECT_SPEC.md`.

## Completed: repository foundation

- Maintain one active scholarship catalogue and a separate source-evidence registry.
- Split the existing 185 draft scholarships into stable, individual JSON files.
- Extract and enforce the supplied schema and controlled vocabularies.
- Check identities, dates, URL syntax, source references and derived-source dependencies.
- Provide repeatable import, formatting, coverage and editorial export commands.
- Document setup and the data-review workflow, with local verification and CI.

## Completed: first local website

- Generate the home page, 16 directory pages, 185 detail pages, supporting pages and 404.
- Use the black/off-white/violet direction, light and dark themes,
  system fonts and responsive layouts.
- Search, filter, sort and paginate in the browser, with transparent uncertainty labels.
- Preserve selections, sort, page and scroll context when returning from a detail page.
- Keep unapplied mobile filter choices; support Apply, Cancel, Escape and focus restoration.
- Generate a compact index without editorial notes or captured source documents.
- Keep a usable, fully paginated HTML directory before JavaScript enhancement.
- Provide an explicit local draft preview and a separate, guarded public build.

## Completed: first editorial audit

- Audit the entire working catalogue and generate a prioritised per-record queue.
- Source-review twelve records against official pages and linked documents; save
  twenty-one new evidence captures with reproducible payload checksums.
- Enrich funding, scope, documents and current-round details while retaining old
  evidence, stable IDs and historical rounds.
- Record unresolved Böll, FES, portal and programme-scope conflicts explicitly.
- Keep every record in draft status pending publication approval.

See [the audit and source-review report](audits/2026-10-24/REVIEW.md).

## Next: public release preparation

1. Resolve the first batch's documented open items, review the remaining urgent
   cases and select a verified launch subset for publication. All records remain drafts.
2. Supply real operator and correction details in ignored local `site.json`, and finalise the
   deployment-specific privacy/legal content. Supporting preview pages currently
   identify missing configuration honestly.
3. Complete accessibility checks with assistive technology, text zoom, reduced
   motion, keyboard-only use and browser/device coverage. Initial 320 px and desktop
   browser checks are recorded in `docs/BUILD.md`.
4. Measure loading, layout stability, filtering plus rendering and real-device
   performance under documented conditions. Compressed asset checks alone do not
   establish the user-facing performance targets.
5. Configure GitHub and Cloudflare Pages; verify the
   applicable build environment and free-plan limits then. Inspect a preview before
   publishing reviewed records.

Python runs during the build and local development. The visitor-facing site remains
static, with no database service, account system or AI matching.
