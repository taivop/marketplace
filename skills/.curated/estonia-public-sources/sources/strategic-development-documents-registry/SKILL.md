---
name: strategic-development-documents-registry
description: Retrieve the Government Office registry of active strategic development documents, including file links and Riigi Teataja references.
---

# Strategic Development Documents Registry

## Use when
- You need the master list of active Estonian strategic development documents.
- You need links to programme PDFs and legal references in one registry workflow.

## Avoid when
- You only need one specific strategy family already covered by a dedicated source skill.

## Inputs
- Sector/topic keywords.
- Time range for publication dates.

## Outputs
- Registry extract with document titles, dates, and links.

## Access reality statement
- Access type: `download files` + `UI copy-only`.
- Verified on 2026-02-24.
- Registry table is embedded as datatable JSON in page HTML.

## Primary endpoints
- Active strategic documents page: https://www.valitsus.ee/strateegia-eesti-2035-arengukavad-ja-planeering/strateegilised-arengudokumendid/kehtivad

## Retrieval workflow (reproducible)
1. Open the `kehtivad` page and locate `datatable-...` JSON script.
2. Parse each row for title, date, and link type (file download vs external legal link).
3. Normalize file URLs to absolute `https://www.valitsus.ee/...`.
4. Keep Riigi Teataja links as explicit legal-reference records.
5. Return registry rows with source row type and link classification.

## Request/query contract
- No auth required.
- Registry records are serialized in `script type="application/json" id="datatable-..."`.
- Rows can contain mixed link types: local files and external legal URLs.

## Output schema expectations
- `source_page_url`
- `document_title`
- `publication_date`
- `document_url`
- `url_type` (`file`, `riigiteataja`, `external`)
- `file_format` (if file)
- `sector_tag` (derived)

## Limits and caveats
- Registry includes heterogeneous documents with different update cycles.
- Title language and formatting vary across ministries and years.
- Some entries point to legal text pages instead of downloadable files.

## Verification hooks
- Page exposes a `script type="application/json" id="datatable-..."` block with many dated records.
- Require both direct file links and `riigiteataja.ee` references. Do not hard-code the generated datatable ID because it changes when the table is republished.
