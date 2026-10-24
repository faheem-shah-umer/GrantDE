# Catalogue audit and first source-review batch

Date: 24 October 2026. This is an editorial audit, not publication approval.

The complete working catalogue passed offline structural and evidence-reference validation. Twelve scholarship records were then compared with official provider/university pages and linked documents. Twenty-one successful source captures were saved for editorial review. Their public metadata is in `data/evidence/2026-10-24-source-review.json`; original payloads are retained in ignored local storage. All scholarship records remain drafts; no programme was merged, deleted or published.

The report separates the offline review queue from live source checks. An unknown field is not automatically an error. Variable or route-dependent awards may correctly lack a single numeric amount. Old application rounds are retained as history.

## Catalogue-wide findings

| Measure | Before this batch | After this batch |
| --- | ---: | ---: |
| Extracted records still awaiting source review | 143 | 138 |
| Records with unconfirmed current dates | 138 | 137 |
| Required-document details unknown | 111 | 111 |
| No single numeric award summarised | 109 | 106 |
| Degree scope unknown | 38 | 39 |
| Subject scope unknown | 126 | 125 |
| Institution scope unknown | 112 | 109 |

No exact normalised title/provider duplicates were found. This does not rule out aliases or overlapping programmes. Six source-URL groups contain several records. Böll, Rosa Luxemburg, Bonn, Dresden, Jena and Stuttgart use shared programme pages; a shared URL alone does not establish a duplicate. The JSON audit lists every group for identity review.

## Priority correction queue

P1 means a recorded deadline within 30 days or a missing official destination, not a proven data error. The following P1 entries were not live-reviewed in this batch. Their dates are recorded catalogue values and still need a source check.

| Scholarship | Recorded deadline | Action |
| --- | --- | --- |
| [Bürkert emergency fund](https://www.uni-stuttgart.de/en/study/new-in-stuttgart/finances/international/#id-994379e8-2) | 2026-10-31 | Verify the current call, restrictions and funds availability. |
| [DAAD STIBET Commitment](https://www.uni-stuttgart.de/en/study/new-in-stuttgart/finances/international/#id-994379e8-0) | 2026-10-31 | Verify the current call, restrictions and funds availability. |
| [DAAD STIBET More equal opportunities](https://www.uni-stuttgart.de/en/study/new-in-stuttgart/finances/international/#id-994379e8-0) | 2026-10-31 | Verify the current call, restrictions and funds availability. |
| [DAAD STIBET Final Stage](https://www.uni-stuttgart.de/en/study/new-in-stuttgart/finances/international/#id-994379e8-0) | 2026-10-31 | Verify the current call, restrictions and funds availability. |
| [Future Network Weimar Triangle: Science for Europe - Doctoral candidates (to Germany)](https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/?detail=57871506) | 2026-11-02 | Verify the current call, restrictions and funds availability. |

For the complete prioritised list, use [catalogue-audit.json](catalogue-audit.json). It includes flags, last-check/review dates, publication status, editorial notes and source URLs for every record.

## Source-reviewed batch

### DAAD Master's: daad-50026200

The [official DAAD page](https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/?detail=50026200) confirms EUR 992/month, the 2027 funding start, study duration and residence rule already recorded. The fresh capture now supports funding. The origin-unspecified page does not establish a universal current deadline or complete country eligibility list; those remain unresolved.

### H-BRS completion: bonn-rhein-sieg-stibet-completion

The [university overview](https://www.h-brs.de/en/io/scholarships-international-students) confirms EUR 650/month for up to three months. Added the thesis-registration-dependent deadline and usual February/July announcement pattern as descriptive notes. The applicable call and full document list must be obtained from the International Office; no year-specific date was invented.

### Böll doctoral: daad-10000113

The [October 2026 funding overview](https://www.boell.de/sites/default/files/2026-10/uebersicht_finanzielle-forderung_engl_10_2026.pdf) lists a EUR 1,500 base for the AA non-EU route and EUR 1,750 for the BMFTR route, plus a EUR 100 allowance. The record now explains the conditional routes, adds a funding range and expands German-language proof and application documents using the [linked doctoral checklist](https://www.boell.de/sites/default/files/2026-04/3-a2-1b-info_checklist_application_prom_may_2025.pdf). That older checklist has different monetary figures, so the dated October overview supplies current amounts. Country eligibility still needs route-specific confirmation.

### Böll study: daad-10000124

The [September 2026 checklist](https://www.boell.de/sites/default/files/2026-09/1_a1-1a-infoblatt_checkliste_bewerbung-stud_september_2026-2.pdf) adds the international Diplom/State Examination main-study routes alongside Master's, a detailed document list and the latest stage for German-language proof. Funding is described by route, with no universal numeric award. The [English page](https://www.boell.de/en/applying-scholarship) still has a first-cycle-only notice for March 2027, while its Master's section, the [German page](https://www.boell.de/de/stipendium-studium) and recent checklist describe international Master's applicants. This conflict remains a publication blocker; the country selection is also not treated as a complete whitelist.

### FES study: daad-10000153

The [programme page](https://www.fes.de/studienfoerderung/stipendium/grundfoerderung-fuer-auslaender-innen) confirms the recorded funding and study stages. The [linked FAQ](https://www.fes.de/studienfoerderung/faq/foerderung-von-auslaendischen-studierenden) adds regional scope and a residence rule with exceptions. The main page permits formal applications from abroad, but the FAQ says applicants must already be in Germany and gives varying EU-country definitions. Residence is now explicitly unknown with this conflict explained. The recurring Master's dates are not applied to all degree routes. A full document checklist still needs review.

### Deutschlandstipendium: daad-10000207

The [official federal FAQ](https://www.deutschlandstipendium.de/deutschlandstipendium/de/studierende/haeufig-gestellte-fragen/haeufig-gestellte-fragen_node.html) confirms EUR 300/month, all nationalities and subject areas, and no repayment. Added explicit doctoral and institutional exclusions and the general concurrent-award restriction. Local university calls, selection and documents remain institution-specific. The original English URL returned no usable content from the retrieval tool; it is not labelled a dead link without further evidence.

### FAU graduation: fau-international-student-graduation-scholarship

The [current FAU call](https://www.fau.eu/studying/organizing-your-studies-and-where-to-go-for-advice/funding-your-studies/scholarships-for-international-students-about-to-graduate/) confirms the recorded one-off EUR 1,000 award and Master's/State Examination scope. The nationality restriction is now explicitly classified, and unsupported all-subject wording was removed. The 28 October 2026 noon deadline is preserved; timezone and opening date remain unconfirmed.

### Amirana: heidelberg-amirana-amirana-scholarship

The [German call linked by Heidelberg](https://backend.uni-heidelberg.de/de/dokumente/alumniamiranaausschreibungpdf/download) states a maximum EUR 300/month for up to two semesters, with a progress check. Added this cap and the ten requested document categories, plus the German-submission/consent conditions. The annual 15 November deadline remains descriptive because the document is not year-stamped. Replaced the unsupported other degree classification with unknown; the medical/dental degree mapping needs maintainer review.

### Heidelberg completion: heidelberg-completion-graduation-completion-grant-for-international-students

The [university page](https://www.uni-heidelberg.de/en/study/management-of-studies/funding-of-studies/graduation-completion-grant-for-international-students) confirms EUR 500/month for up to six months and the existing document list. Added the excluded applicant groups, tuition-fee/stay-abroad limitations and explicit international scope. The phrase postgraduate Master's needs programme-specific interpretation. February/August windows lack an explicit year, so no current year was inferred.

### a.r.t.e.s.: uni-cologne-artes-a-r-t-e-s-doctoral-scholarships

The [current call](https://artes.phil-fak.uni-koeln.de/en/doctorate/funding-programmes/artes-doctoral-scholarships/application) confirms the funding, three-year duration and 29 October 2026 application deadline for April 2027. A portal-selection instruction still names April 2026. This mismatch is now an explicit review note; the correct portal call must be confirmed.

### Stuttgart Beihilfe: uni-stuttgart-beihilfe

The [university page](https://www.uni-stuttgart.de/en/study/new-in-stuttgart/finances/international/#id-994379e8-1) confirms case-by-case aid and the conditional 31 October 2026 joint deadline. The international restriction is now explicit, and unsupported all-subject wording was removed. The introduction mentions doctoral students, but the specific bullets describe Bachelor's/Master's semesters; doctoral coverage remains unresolved. Applicants must consult the International Office for the form and current funds availability.

### Elsa Neumann: berlin-elsa-neumann-doctoral-scholarship

The [central DRS conditions](https://www.fu-berlin.de/sites/drs/funding/nafoeg/about-nafoeg.html) correct the recorded two-year full award to up to 36 months and establish a EUR 1,350 base plus EUR 100 research allowance. The [central call](https://www.fu-berlin.de/sites/drs/funding/nafoeg/index.html) and [TU Berlin information](https://www.tu.berlin/go5168/) support a new 16 September–11 November 2026 round, with earliest funding start April 2027. Added the institutional/public-funding conditions and central programme link. The old unconfirmed round remains as history. The full application brochure and explicit noon-deadline timezone still need review.

## Launch preparation

1. Resolve the explicit provider conflicts and record the chosen university/country routes. Complete the remaining high-priority source checks.
2. Review the resulting record diffs and select records for publication. Source review alone does not change draft status.
3. Supply the public base URL, correction route and operator/contact details in `site.json`; finalise deployment-specific supporting text.
4. Complete assistive-technology, text-zoom, reduced-motion, device and measured loading/rendering checks. Local compressed sizes are not real-device performance results.
5. Configure and inspect a deployment preview before a public release. No deployment was performed in this pass.

## Reproduce the offline queue

```powershell
.\.venv\Scripts\python.exe scripts\audit_catalogue.py --as-of 2026-10-24 --output docs\audits\2026-10-24\catalogue-audit.json
.\.venv\Scripts\python.exe -m grantde.validate
.\.venv\Scripts\python.exe -m grantde.report --output docs\CATALOGUE_REPORT.md
```

See [source-review-batch.json](source-review-batch.json) for reviewed IDs, source URLs, changed sections, before/after fingerprints and outstanding notes. New capture checksums cover canonical UTF-8 JSON with a trailing newline; they identify the saved retrieval payload, not the provider's original HTTP bytes. Previous captures and all stable scholarship IDs/slugs remain intact.
