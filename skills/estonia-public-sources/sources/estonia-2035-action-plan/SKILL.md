---
name: estonia-2035-action-plan
description: Retrieve Estonia 2035 action-plan versions from Government Office document tables, including multilingual files and publication timestamps.
---

# Estonia 2035 Action Plan

## Use when
- You need official Estonia 2035 action-plan versions and update chronology.
- You need multilingual files and implementation-overview attachments.

## Avoid when
- You need the full cross-sector registry of all strategic plans (use strategic registry skill).

## Inputs
- Target year/version.
- Language preference.

## Outputs
- Versioned action-plan dataset with file URLs and publication dates.

## Access reality statement
- Access type: `download files`.
- Verified on 2026-02-24.
- Document list is available as embedded datatable JSON on the page.

## Primary endpoints
- Estonia 2035 action plan page: https://www.valitsus.ee/strateegia-eesti-2035-arengukavad-ja-planeering/eesti-2035-tegevuskava

## Retrieval workflow (reproducible)
1. Open action-plan page and locate datatable script block (`id="datatable-..."`).
2. Parse rows into title, publication date, file format, and link.
3. Convert relative file paths (`/sites/default/files/...`) to absolute URLs.
4. Label record language using title text and/or page language marker.
5. Return a chronological version table.

## Request/query contract
- No auth required.
- Embedded table records are in `script type="application/json" id="datatable-..."`.
- Date values are provided via `time datetime` in table payload rows.

## Output schema expectations
- `source_page_url`
- `record_title`
- `record_date`
- `file_url`
- `file_format`
- `language`
- `record_type` (`action_plan`, `implementation_overview`, etc.)

## Limits and caveats
- Files are published as point-in-time snapshots; do not assume one canonical latest file without date comparison.
- Older versions may include translated titles with inconsistent naming.

## Verification hooks
- Page exposes a `script type="application/json" id="datatable-..."` block with multiple dated action-plan files.
- At least one direct file must return a PDF. Do not hard-code the generated datatable ID because it changes when the table is republished.
