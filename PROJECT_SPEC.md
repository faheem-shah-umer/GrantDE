# GrantDE — Project Specification

Status: local static website and draft catalogue preview implemented; public release preparation remains.

This document defines the first version of GrantDE. It records the agreed product scope, technical architecture, content standards and interface expectations. Performance numbers below are implementation targets, not measured results.

## 1. Product vision

GrantDE is a free scholarship discovery website for international students who want to study, or are already studying, in Germany.

Visitors provide a few study-related details, explore relevant scholarships, understand the requirements and follow a direct link to the official provider. The experience should feel premium, modern and effortless while remaining lightweight.

**Product promise:** Find relevant scholarships in Germany, understand their requirements and reach the official application page quickly.

The catalogue should grow towards broad coverage. Do not claim to list every scholarship, guarantee eligibility or imply that an application will succeed. Publish the actual coverage and limitations.

## 2. First-version scope

### Included

- Public browsing without an account.
- Search by scholarship name, provider and subject.
- Filters for degree level, subject area and relevant scholarship requirements. Nationality conditions are shown in scholarship descriptions rather than used as a filter.
- Scholarship summaries, individual detail pages and official application links.
- Clear funding information, deadlines, additional requirements and source references.
- A responsive interface for phones, tablets and desktops.
- A manually maintained, validated JSON catalogue.
- Local, browser-based filtering.
- Cloudflare Pages deployment through GitHub.

### Deferred

- Candidate accounts, authentication and personal profiles.
- Application tracking, synchronised bookmarks and personalised notifications.
- CV uploads, document storage and application submission.
- AI recommendations, chatbots and automatic eligibility guarantees.
- A database, a public editing interface and a running application server.
- Automated scraping and unattended publication of collected information.

These features are future possibilities, not requirements for the initial release.

## 3. Intended visitor journey

1. Open the website and immediately understand its purpose.
2. Browse all published scholarships or choose a few filters.
3. See relevant results immediately, with clear reasons and remaining requirements.
4. Open a scholarship detail page.
5. Read the funding, conditions, dates and application instructions.
6. Follow the clearly labelled link to the official programme or application page.
7. Return to the directory without losing the previous filters, result page or scroll position.

Do not place registration, a questionnaire or an introductory animation in front of browsing.

## 4. Pages and navigation

Use three primary page templates and a small set of supporting pages.

| Page | Suggested route | Required content |
| --- | --- | --- |
| Home | `/` | Concise introduction, primary search or discovery action, coverage explanation and a small selection of useful opportunities. |
| Directory | `/scholarships/` | Search, filters, matching result count when filtering or searching, sorting, scholarship cards, pagination and an informative empty state. |
| Scholarship detail | `/scholarships/<slug>/` | Full programme details, requirements, application round, official links, sources and last review date. |
| About and coverage | `/about/` | Purpose, source selection, review process, catalogue boundaries and matching limitations. |
| Contact and corrections | `/contact/` | A simple way to report an incorrect listing or suggest a scholarship; initially an email link or repository issue link. |
| Privacy and legal information | `/privacy/`, `/legal/` | Information appropriate to the actual operator and deployment. Operator details must be supplied before launch. |
| Not found | `/404.html` | A useful explanation with links to the directory and home page. |

Keep the main navigation short: Scholarships, About, Contact. The brand links to Home. Supporting links belong in the footer.

Keep catalogue totals off the homepage, About page and unfiltered directory. Show the number of matching scholarships when at least one filter or a non-empty search is applied, updating it as selections change. Sorting alone does not reveal a total. Use page numbers for navigation.

## 5. Visual direction

### Overall character

Use bold sans-serif typography with italic serif emphasis, neutral black and off-white surfaces, blue/violet accents, rounded cards and a pill-shaped header. The directory should feel approachable and precise, with generous spacing and clear alignment. See `docs/DESIGN.md` for the implemented design tokens.

The expensive feeling should come from consistency and craftsmanship. Avoid visual clutter, oversized decorative sections and animations that delay useful content.

### Colour and surfaces

- Provide polished light and dark themes, with a moon/sun toggle available throughout the website. Remember the appearance preference locally and apply it before the page is painted.
- Use off-white and white surfaces with near-black text in light mode; use neutral charcoal surfaces with off-white text in dark mode.
- Use monochrome primary actions, blue/violet links and focus states, and soft lilac feature panels. Small aqua accents may distinguish study paths and application status.
- Use fine neutral borders, subtle surface differences and very restrained shadows.
- Use rounded cards around 24 px, larger feature panels around 32 px, 12 px form controls and pill-shaped actions.
- Keep status colours secondary and always pair them with text.
- Treat these as initial directions; verify contrast before finalising colour tokens.

Do not introduce glass effects, animated gradients, heavy blur, decorative particles, background video or large stock-photo banners.

### Typography and layout

- Use a high-quality system font stack initially; a single self-hosted font can be considered within the performance budget.
- Use a restrained type scale, comfortable line height and a readable body size of approximately 16 px.
- Make scholarship names, funding and deadlines easy to scan.
- Limit long-form reading width to roughly 65–75 characters per line.
- Use a consistent spacing scale based on 4 or 8 px increments.
- Keep the content container around 1120–1200 px on large screens.
- Make components feel related through shared alignment, spacing and states.

### Responsive behaviour

- Desktop: filters beside results, with clear visual separation.
- Tablet: reduce columns before text becomes cramped.
- Mobile: a single result column and a labelled Filters control opening an accessible panel.
- Keep draft filter choices when closing the mobile panel; Apply updates results and Cancel restores the applied choices.
- Keep essential funding, deadline and action information visible without hover.
- Support 320 px-wide screens without horizontal page overflow.
- Avoid permanent overlays that obscure scholarship information.

## 6. Interaction and motion

**Smooth as butter means immediate feedback, stable content and uninterrupted interaction.** Motion supports that experience; it must not slow it down.

| Interaction | Desired behaviour |
| --- | --- |
| Hover and focus | Subtle colour or border change, typically 100–160 ms. |
| Button press | Immediate feedback; optional very small transform without shifting surrounding content. |
| Filter selection | Control state updates immediately; results update promptly without a full-page reload. |
| Search typing | Short debounce, around 100–150 ms, when needed to avoid repeated work. |
| Mobile filter panel | A short opacity/transform transition, approximately 180–240 ms. |
| Page navigation | Normal, fast navigation. Never wait for an exit animation. |
| Results update | Preserve the results container and focus; avoid repeatedly animating every card. |
| Back navigation | Restore the relevant directory state and scroll position. |

- Animate opacity and transforms where practical; avoid animating dimensions or large shadows.
- Do not apply `transition: all` globally.
- Avoid artificial loading delays, fake progress indicators and unnecessary skeleton screens.
- Respect `prefers-reduced-motion`: remove nonessential movement and use immediate state changes.
- Keep native scrolling and normal browser behaviour. Do not implement scroll hijacking.
- Prevent layout jumps by reserving space for predictable elements.
- Keep controls usable while results are updating.
- Do not automatically move keyboard focus when filters change.
- Avoid a large animation library for these interactions.

## 7. Search, filters and matching

### Initial filters

- Nationality is not a directory filter. Keep nationality requirements and country-specific application conditions in the scholarship description; retain standard country codes in the source records.
- Degree level: Bachelor's, Master's, doctorate and other explicitly supported categories.
- Subject area or domain, using a controlled vocabulary.
- Current situation: outside Germany, already in Germany or not specified.
- University or location restrictions where the data supports them.
- Funding purpose: living costs, tuition, research, travel or study completion.
- Application availability: open, upcoming, closed, rolling or dates unconfirmed.

Keep degree level and subject area separate. Specific course names may be searchable, but do not require an exhaustive list of every course in Germany.

Filters should compose predictably: different filter categories narrow results together; multiple selected values within one category match any of those values. Clearly show active filters and provide one Reset action.

### Matching rules

Use transparent, deterministic rules implemented in a small JavaScript module. Do not introduce a numerical match score.

- **Potential match:** the provided details match the known criteria, with additional conditions still shown.
- **Needs checking:** the record or the visitor's answers do not establish an important requirement.
- **Does not meet a listed requirement:** a known mandatory condition fails; show the specific reason when relevant.

Missing data means unknown, not unrestricted and not ineligible. An unrestricted field must be recorded explicitly. Mandatory requirements, preferences and exceptions must remain distinct.

Keep application availability separate from eligibility. A person may fit a programme whose current application round is closed.

Do not describe all filtered results as guaranteed opportunities the visitor can apply for. Use wording such as “Scholarships matching your selected criteria,” with outstanding requirements on the detail page.

### Results behaviour

- Offer simple sorting: relevance, deadline and name.
- Label deadline sorting as nearest known deadline; keep undated and rolling opportunities clearly identified.
- Use paginated rendering to keep the DOM small, even when filtering a larger local catalogue.
- Preserve selections when switching result pages.
- Explain zero results and allow users to remove individual filters.
- Announce result updates and empty states accessibly without announcing every keystroke. Include the matching count when a filter or search is active.
- Provide an unfiltered, paginated directory and working detail links when JavaScript is unavailable.

## 8. Scholarship information model

Store one JSON record per scholarship with a stable ID and URL slug. Use a schema to define required fields, types, controlled values and unknown-value handling.

| Group | Information |
| --- | --- |
| Identity | ID, slug, title, provider and concise original summary. |
| Study scope | Supported degree levels, subject areas and any university/location restrictions. |
| Applicant requirements | Nationality conditions, residence rules, language, grades, experience and other mandatory conditions. |
| Exceptions and preferences | Conditional exceptions, preferred characteristics and explanatory notes. |
| Funding | Amount or range, currency, payment frequency, duration and covered costs. |
| Application rounds | Round identifier, opening date, deadline, timezone where relevant, and confirmed availability information. |
| Application process | Required documents, short steps, official programme URL and application URL when available. |
| Provenance | Source URLs, notes supporting important rules, last checked date and last reviewed date. |
| Publication | Draft/published/archived status and any information requiring further review. |

Define a consistent distinction between explicitly unrestricted criteria and unknown criteria. Do not use an empty list to mean both. Preserve structured conditions alongside readable source-grounded explanations.

A scholarship and its yearly application rounds are different things. Retain earlier rounds rather than overwriting their dates. Never copy an earlier deadline into a new round unless the provider confirms it.

Dates must have explicit meaning. A review date is not an application deadline, and an automated link check is not an editorial review.

## 9. Technical architecture

| Part | Agreed technology | Responsibility |
| --- | --- | --- |
| Data processing | Python | Read, validate, normalise and maintain scholarship records. |
| Page generation | Python + Jinja2 | Generate the home page, directory pages and scholarship detail pages. |
| Data storage | JSON | Hold the version-controlled catalogue. |
| Appearance | HTML + CSS | Provide semantic structure, responsive layout and the visual system. |
| Interactivity | Small amount of JavaScript | Filter, sort, paginate and manage interface state in the browser. |
| Version control | GitHub | Track changes to data, templates, styles and scripts. |
| Hosting | Cloudflare Pages | Serve the generated static output. |

Python runs during development and the build. It does not run as a visitor-facing backend. The public deployment contains generated HTML, CSS, JavaScript and public catalogue data.

### Build flow

```text
Scholarship JSON + templates + static assets
                    |
          Python validation and generation
                    |
     HTML pages + compact filter index + assets
                    |
                  dist/
                    |
             Cloudflare Pages
```

### Proposed project structure

```text
GrantDE/
  PROJECT_SPEC.md
  README.md
  pyproject.toml
  data/
    scholarships/
    schema/
  src/
    grantde/
      build.py
      validate.py
      normalise.py
  templates/
    base.html
    home.html
    directory.html
    scholarship.html
    partials/
  static/
    css/
    js/
    icons/
  dist/                 # Generated; not hand-edited.
```

Use Jinja2 as the template engine and one schema-validation approach, such as JSON Schema validation in Python. Keep dependencies small and pin a reproducible dependency set when implementation begins.

Enable template autoescaping and validate public links. Do not render externally collected content as trusted HTML.

Generate a compact public index for filtering, containing only the fields needed by search and result cards. Keep longer descriptions on the generated detail pages. Never publish internal editorial notes or credentials in that index.

Begin with a simple CSS file and small JavaScript modules. A bundler, frontend framework, database and API are not initial requirements.

## 10. Content maintenance and trust

1. Identify an official provider, foundation or university source.
2. Create or update a scholarship record with source references.
3. Check requirements, funding, application dates and official links.
4. Validate the record automatically.
5. Review the proposed change in GitHub.
6. Build and publish the updated website.

- Prefer official sources; distinguish uncertain information clearly.
- Write concise summaries rather than copying entire provider pages.
- Detect duplicate records before publishing.
- Check time-sensitive records more frequently around application deadlines.
- Preserve the original source when an application URL redirects elsewhere.
- Show “Deadline not announced” or “Details need checking” instead of inventing values.
- Provide a visible correction route on scholarship pages.
- Use clearly labelled fictional records during development; exclude them from the public launch catalogue.

The initial launch should prioritise a manageable, reviewed catalogue over an unsupported claim of complete coverage.

## 11. Performance and accessibility targets

These are proposed budgets to verify during implementation, not guarantees on every device or network.

| Measure | Initial target |
| --- | --- |
| Initial compressed CSS | At most 25 KiB. |
| Initial compressed JavaScript | At most 35 KiB. |
| Initial page transfer | At most 200 KiB, excluding the separately measured catalogue index. |
| Catalogue transfer | Keep compact; measure separately and split or redesign retrieval if it becomes a noticeable download. |
| Filter computation and rendering | Target under 100 ms for a 1,000-record synthetic benchmark on an agreed mid-range mobile test device, excluding intentional typing debounce. |
| Largest Contentful Paint | Target at most 2.5 s under documented mobile test conditions. |
| Interaction to Next Paint | Target at most 200 ms once enough real usage exists to measure it. |
| Cumulative Layout Shift | Target at most 0.1. |

- Measure performance using repeatable conditions and record the device/network assumptions.
- Treat Lighthouse as a diagnostic tool, not proof of smoothness for every visitor.
- Serve local assets; avoid unnecessary third-party scripts and font requests.
- Use semantic HTML, visible focus indicators, explicit form labels and sufficient contrast.
- Support keyboard-only operation and reduced-motion preferences.
- Make mobile controls comfortably tappable, aiming for approximately 44 px targets.
- If a mobile filter panel behaves as a modal, manage focus, Escape and focus restoration correctly.
- Test text zoom, long scholarship names, long provider names and missing information.

## 12. Privacy and hosting

The first version requests no name, email, address, CV or account information. Study filters are optional inputs used locally. The light/dark appearance preference may be saved in local browser storage across visits.

- Keep filter answers in memory by default.
- If needed for returning from detail pages, use a minimal tab-scoped session state for filters, pagination and scroll position; store no application documents or candidate profile.
- Do not put filter answers into URLs by default.
- Do not transmit answers to an analytics service or matching API.
- Avoid analytics, advertising and tracking scripts in the initial release.
- Describe hosting-level request processing accurately; do not claim that no infrastructure logs exist.

Use Cloudflare Pages for static deployment, initially with its provided subdomain. Connect the GitHub repository and configure the Python build to publish `dist/`.

Aim for zero recurring hosting cost within the free plan's current limits. Confirm the applicable build environment and platform limits at implementation time. A purchased domain, external data services and future dynamic features have separate cost considerations.

## 13. Implementation sequence

1. Define the record schema and create a small reviewed sample catalogue.
2. Implement validation and the Python/Jinja2 build.
3. Establish colour, typography, spacing and component tokens.
4. Build the responsive directory and scholarship detail templates.
5. Implement filtering, sorting, pagination and state restoration.
6. Polish interaction states, motion, accessibility and empty/error states.
7. Add supporting content, metadata, sitemap, robots file and a useful 404 page.
8. Run data, functional, accessibility and performance checks.
9. Configure deployment and inspect a Cloudflare preview before public release.

## 14. Acceptance criteria for the first release

- The project builds reproducibly from a clean checkout using documented commands.
- Invalid records, duplicate IDs/slugs and invalid known dates fail the build with actionable messages.
- Data checks distinguish unknown, unrestricted and explicitly restricted criteria.
- Important matching behaviour is tested, including exceptions and missing information.
- All published scholarship links resolve to generated detail pages.
- Official application links are correctly labelled and checked; missing links have an honest fallback.
- Expired rounds and unconfirmed future dates are presented accurately.
- Visitors can browse, filter, sort, reset and navigate results without a login.
- Returning from a detail page restores the previous browsing context.
- The directory remains useful if JavaScript fails or is disabled.
- Mobile controls, keyboard navigation, reduced motion and 320 px layouts work correctly.
- Loading, filtering and navigation have no avoidable layout jumps or artificial delays.
- Published performance results state the conditions used and identify any missed budgets.
- Sources, review dates, catalogue coverage and correction options are visible.
- No fictional scholarships, placeholder operator information or candidate-data collection appear in the launch version.

## 15. Future growth

Potential later features include local bookmarks, an editorial interface, provider submissions, more languages, automated source-change detection, accounts and application tracking.

Preserve stable scholarship IDs, separate data from templates and keep matching rules independent of presentation. These boundaries allow later additions without requiring a running backend now.

Revisit server-side search or a database when measured catalogue size, editing needs or personalised features justify it. Do not add infrastructure solely for hypothetical growth.
