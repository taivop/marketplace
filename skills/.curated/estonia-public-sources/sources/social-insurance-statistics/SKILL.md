---
name: social-insurance-statistics
description: Download Social Insurance Board pension, state social-insurance, A1 certificate, and service statistics workbooks from the official index.
---

# Social Insurance Statistics

## Access

- Index: `https://www.sotsiaalkindlustusamet.ee/asutus-uudised-ja-kontakt/praktiline-teave/statistika`
- The page contains direct XLS/XLSX links grouped by topic and period; no authentication is required.

## Retrieve

Fetch the index and parse spreadsheet anchors with their nearest section heading. Select by title and period:

- `aasta aruande tabel lisadega`: annual pensioner tables.
- `Riiklik sotsiaalkindlustus YYYY - ...`: quarterly/cumulative state social-insurance workbook.
- `Tõendi A1 väljastamise statistika`: A1 certificate statistics.
- Other section-specific service workbooks as labeled on the page.

The state social-insurance workbook is a formatted report, not a flat table. Identify numbered sections and their local header rows; for example pension rows distinguish recipient count, average assigned pension, and amount in thousands of euros.

## Return

Return index/file URLs, anchor title, topic, reporting period, sheet/section, original row label and code, value, unit, and retrieval time.

## Limits

- Some historical files are binary `.xls`; use a reader that supports the legacy format.
- Quarterly files can be cumulative (`3 kuud`, `6 kuud`, `9 kuud`, `12 kuud`), not independent quarter flows.
- Do not flatten differently structured report sections into one metric without retaining their headers and units.

## Verify

Require spreadsheet signatures and match the requested period in the link label and workbook heading before extracting records.
