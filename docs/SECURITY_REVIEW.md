# Repository publication review

Reviewed on 24 October 2026. Scope: files selected for the first public commit,
Git author metadata, Python dependencies, browser scripts, templates and build
output. This is a focused publication review, not a penetration test or a
guarantee that no vulnerability exists.

## Resolved findings

| Finding | Evidence and impact | Resolution |
| --- | --- | --- |
| Build tools with known advisories | `requirements-dev.txt` and `pyproject.toml` pinned setuptools 80.9.0 and wheel 0.45.1. Malicious package/archive input could trigger documented path or file-permission issues. | Pin setuptools 84.2.1 and wheel 0.48.0; include packaging 26.3. |
| Outdated local installer | The local environment used pip 23.2.1, with multiple archive/path and package-source advisories. | Upgrade and pin pip 26.2.2 in development requirements. |
| Personal metadata | Product/design documentation referenced private filesystem locations; the original commit used a personal author name. | Remove the references and prepare a new public history with a generic contributor identity. |
| Private or unnecessary publication files | Local configuration, source-page payloads, tests, screenshots and generated build output do not belong in this public snapshot. | Ignore local configuration/tests, retain captures in ignored local storage, publish only provenance metadata and remove generated artifacts. |
| JS-CSP-001, defence in depth | `src/grantde/build.py`, in `build_site`, previously emitted `_headers` without a Content Security Policy. No exploitable injection was demonstrated. | Add a same-origin policy with scripts/styles restricted to local assets, plugins disabled and framing denied. Verify delivery on the deployed host. |

## Dependency verification

OSV's public API returned no known advisory matches for the final installed
versions: attrs 25.4.0, jsonschema 4.24.0, jsonschema-specifications 2025.4.1,
Jinja2 3.1.6, MarkupSafe 3.0.3, referencing 0.36.2, rpds-py 0.25.1,
typing_extensions 4.15.0, setuptools 84.2.1, wheel 0.48.0, packaging 26.3 and
pip 26.2.2. This is a point-in-time database result; Dependabot is configured
for ongoing dependency and GitHub Actions updates.

Relevant upstream advisories:

- [setuptools Windows path escape](https://github.com/pypa/setuptools/security/advisories/GHSA-xmj3-9gf7-h52w)
- [setuptools exclusion bypass](https://github.com/pypa/setuptools/security/advisories/GHSA-h35f-9h28-mq5c)
- [wheel path traversal](https://github.com/advisories/GHSA-8rrh-rw8j-w5fx)
- [pip package URL handling](https://github.com/advisories/GHSA-qwm4-qh6w-59xr)
- [OSV API](https://google.github.io/osv.dev/api/)

## Existing protections and limits

Jinja HTML/XML autoescaping and strict template variables remain enabled.
Browser result cards use DOM text nodes. Catalogue URLs and relative data paths
are validated; generated output replacement is confined to owned build folders.
The preview server binds to loopback. No credentials or applicant data are
required, and no third-party browser scripts are loaded.

The publication scan checks private-key markers, common token formats, credential
assignments, personal identifiers and private filesystem paths. The intended
GitHub repository URL is public project configuration. Official provider names,
public contacts and eligibility conditions remain part of the catalogue.

Local Python and JavaScript regression suites passed (43 and 9 tests), alongside
catalogue validation, formatting, report consistency, dependency consistency and
the preview build's internal-link check. Tests remain local and are excluded
from the public Git repository as requested.

The staged publication scan covered 239 files with no flagged secret or personal
data patterns. A checkout reconstructed solely from those staged files passed
validation, formatting, report consistency and preview generation without local
configuration, tests or raw captures.

Hosting headers, TLS, operator disclosures and the domain still require deployment
verification. All records remain drafts; no public website was deployed by this
cleanup.
