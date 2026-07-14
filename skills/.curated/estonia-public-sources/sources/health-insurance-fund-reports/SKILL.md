---
name: health-insurance-fund-reports
description: Download Estonian Health Insurance Fund annual reports by year for official financing, service-volume, and system-performance evidence.
---

# Health Insurance Fund Annual Reports

## Access

- English index: `https://www.tervisekassa.ee/en/organisation/annual-reports`
- Each year label links directly to a PDF; no authentication is required.

## Retrieve

1. Fetch the index and parse year-labeled `.pdf` anchors.
2. Select the requested year from the anchor text, then resolve its URL against the index.
3. Download and extract the PDF while retaining page numbers and table headings.

## Return

Return reporting year, report URL, retrieval time, page/table reference, indicator label, value, unit, accounting basis, and any budget/actual distinction.

## Limits

- The English archive currently trails the current calendar year; report availability is determined by index links.
- Older files may use the former `haigekassa.ee` host but remain official archive links.
- Annual-report definitions and organizational names can change across years.

## Verify

Require a year-labeled index entry and `%PDF-` signature. Cite the exact report page for every extracted value.
