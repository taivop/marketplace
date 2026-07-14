---
name: etis-research-information-system
description: Search public ETIS projects, publications, researchers, and institutions through its browser-rendered portal and stable record URLs.
---

# ETIS Research Information System

## Use when
- You need public Estonian research projects, publications, researchers, or institutions.
- You need stable ETIS detail URLs and visible project funding, dates, people, or institution fields.

## Avoid when
- You need restricted internal ETIS data.
- You have no browser-capable tool; stateless HTTP calls do not return the rendered records.

## Browser routes
- Projects: https://www.etis.ee/Portal/Projects/Index
- Publications: https://www.etis.ee/Portal/Publications/Index
- Researchers: https://www.etis.ee/Portal/Persons/Index
- Institutions: https://www.etis.ee/Portal/Institutions/Index
- Detail pattern: `https://www.etis.ee/Portal/{Entity}/Display/{uuid}`

## Workflow
1. Open the exact entity route in a full browser and wait for the result count and list to render.
2. Enter a search word or use the visible side filters, then activate `Search` or `Filter`.
3. Capture each selected record's `/Portal/{Entity}/Display/{uuid}` link and visible fields.
4. Use the portal's export controls when bulk output is required; retain the selected filters with the downloaded file.

## Access reality
- Public browser-rendered records, verified 2026-07-14 without login.
- The project route rendered more than 26,000 results with titles, UUID detail links, dates, funding, principal investigator, project number, funder, and institution.
- The JavaScript bundle names `/Portal/.../Search` and `/GetFilters`, but direct stateless requests return the SPA HTML shell. Do not present those paths as a public API.

## Output schema expectations
- Keep entity type, UUID, detail URL, title/name, dates, institution, people, funding/status fields shown, selected filters, and retrieval timestamp.

## Limits and caveats
- Browser execution is required; raw HTML clients see only the app shell.
- Field schemas differ by entity type, and some older records are incomplete.
- Search results may include future-dated projects; do not infer current activity from list order alone.

## Verification hooks
- Require a rendered result count and at least one stable `/Display/{uuid}` link before reporting success.
- For projects, require the visible title plus at least one of dates, project number, funding, principal investigator, funder, or institution.
