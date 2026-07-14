# Estonia Public Sources Simplification Plan

## Goal

Give Codex and Claude the shortest reliable path from an Estonian public-data question to an official record. Ship acquisition recipes, not an inventory of government topics.

## Product contract

A source belongs in the skill only when a fresh agent can retrieve a real public record without repeating source discovery. Each shipped source must provide:

1. A working API request, direct download, or reproducible public browser/export path.
2. The required query parameters or UI inputs.
3. The expected response type and identifying fields.
4. Source-specific limits such as authentication, pagination, language, or coverage.
5. A semantic verification that distinguishes useful data from an HTML error page.

Descriptive pages, authenticated services without public records, duplicate topic wrappers, and broken endpoints do not qualify.

## Distribution constraints

- Keep the package-level `SKILL.md` as the Codex entry point.
- Keep `skills/query/SKILL.md` as the Claude slash-command entry point.
- Keep distribution metadata in the package `SKILL.md` and regenerate Claude manifests after metadata changes.
- Both entry points must use the same routing catalog and source recipes.

## Target structure

```text
estonia-public-sources/
├── SKILL.md                 # shared runtime policy and routing
├── SOURCE_MAP.md            # canonical topic-to-recipe catalog
├── skills/query/SKILL.md    # thin Claude command wrapper
└── sources/<interface>/SKILL.md
```

The root skill, command wrapper, and README must not maintain separate source inventories or hard-code a source count.

## Execution plan

### Phase 1: Remove structural duplication

- [x] Make `SOURCE_MAP.md` the canonical routing catalog.
- [x] Reduce the root skill to shared routing, retrieval, and output rules.
- [x] Keep the Claude command as a thin wrapper around the root skill.
- [x] Remove the hand-maintained README source index and numeric source claims.
- [x] Add validation for catalog references and nested source frontmatter.

### Phase 2: Prune and merge

- [x] Remove the clearest narrative, registration, and access-controlled non-sources.
- [x] Merge Riigikogu agenda and stenogram routing into the Riigikogu API recipe.
- [ ] Group remaining entries by underlying technical interface.
- [ ] Merge duplicate wrappers that use the same API, dataset, or public application.
- [ ] Delete entries that cannot retrieve public records in a clean agent session.

### Phase 3: Verify every surviving recipe

- [ ] Run every working request or browser path.
- [ ] Replace homepage-only endpoints and placeholder requests.
- [ ] Replace generic generated sections with exact request and response contracts.
- [ ] Add one content-level smoke check per source.
- [ ] Remove any source that cannot pass the practical-access test.

Audited and smoke-covered in the first endpoint wave: Statistics Estonia, Bank of Estonia, Riigi Teataja, Riigikogu, Business Register, public finance, tax/customs, weather, Elering, Peatus, geospatial services, Tallinn open data, election results, the national open-data RSS catalog, and MuIS.

Second interface wave: merged food and feed operator lookups into the tested JVIS contract; merged OSALE consultation routing into EIS; removed duplicate OSALE RSS, PTA guidance, animal-keeper registration, and animal-disease guidance entries that do not independently retrieve records.

Live primary-URL audit: removed dead Competition Authority, Data Protection Inspectorate, and police-statistics routes; closed VOLIS; three Labour Inspectorate routes that redirect to its homepage; and policy/authenticated-service wrappers for migration, archives, prosecution statistics, e-ship, and succession records.

Municipal interface audit: removed the obsolete Tartu WebAktid duplicate and replaced the Tartu document-register splash-page recipe with its actual searchable Lotus Notes view chooser and record-type contracts. Removed the Tartu open-data wrapper because the city page only forwards to the already tested national catalog.

Ministry of Finance interface audit: removed procurement review and supervision procedure pages plus the incorrectly routed local-government benchmark wrapper. Rebuilt state ownership as a tested HTML-table contract for companies and foundations.

RIK interface audit: removed the access-approved e-File statistics environment and authenticated/paid Land Register wrapper. Rebuilt the public marital-property aggregate statistics endpoint and ADR document-register form contracts with live checks.

Transport Administration interface audit: removed fairway-dues and ship-registration guidance wrappers. Rebuilt maritime economy around the Tableau CSV export and State Port Register around its public settings, list, and detail APIs.

Health Board interface audit: retained four distinct public datasets but replaced their generic wrappers with exact bulletin/precept file discovery, MEDRE JSON/XML API, and vaccination Tableau export contracts.

RIA and Government Office interface audit: removed the duplicate/misdirected Government Office document-register wrapper. Replaced obsolete UI routes with RIHA and X-Road JSON contracts, and made RIA cyber/study publications and quarterly lobbying workbooks directly discoverable and testable.

Government Office data audit: retained five distinct working sources. Replaced generic journal and cabinet-agenda wrappers with Lotus Notes XML and search-service JSON contracts, removed stale generated table IDs from strategy recipes, and added checks for the Power BI/file discovery paths.

### Phase 4: Keep the catalog healthy

- [x] Run offline structure checks on every change.
- [x] Run network smoke checks for audited sources on a schedule rather than on every pull request.
- [ ] Test representative Codex and Claude queries for routing and retrieval success.
- [ ] Remove failed recipes promptly instead of retaining deprecated placeholders.

## Acceptance criteria

- Every catalog route resolves to an existing source recipe.
- Every source recipe is reachable from the catalog.
- Both Codex and Claude load the same shared workflow.
- Every shipped source retrieves public data or records as documented.
- No runtime file exists only to signal catalog breadth or thoroughness.
- Examples, generated analyses, virtual environments, and application dependencies are not distributed with the skill.
