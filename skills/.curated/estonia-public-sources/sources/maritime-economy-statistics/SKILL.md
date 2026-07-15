---
name: maritime-economy-statistics
description: Download sector-level Estonian maritime economy company, revenue, maritime-share, and employment indicators from the official embedded Tableau workbook.
---

# Maritime Economy Statistics

## Access

- Official page: `https://www.transpordiamet.ee/en/maritime-and-waterways/bringing-ships-under-estonian-flag/maritime-economy-statistics`
- Direct CSV: `https://public.tableau.com/views/Surveyofmaritimeeconomy/THEIMPACTOFTHEMARITIMESECTORONTHEESTONIANECONOMY.csv?:showVizHome=no`
- Public Tableau export; no login is required.

## Retrieve

Fetch the CSV URL directly. The workbook and sheet names come from the official page's Tableau embed, so re-read that embed if Tableau returns a view error after a publisher update.

Important columns include:

- `sektor` and `sektor detailne`
- total company count and percent of all companies
- total sales revenue
- maritime sales revenue and maritime share
- total employees

Preserve the original Estonian headers. Normalize non-breaking spaces in formatted numbers and decimal commas only in additional analysis columns.

## Return

- Return one row per detailed maritime sector with the original values, workbook URL, official-page URL, and retrieval time.
- State the period shown by the workbook/dashboard; do not infer it from retrieval time.
- Keep sector totals separate from detailed subsectors if both are exported.

## Limits

- Tableau's default CSV exports the active sheet, not every dashboard tab.
- For another tab, inspect the official embed or Tableau view and export that sheet explicitly.
- The dashboard is a survey/study output rather than a continuously updated administrative register.

## Verify

- Require HTTP 200 `text/csv`, multiple data rows, `sektor`, and company, revenue, and employee columns.
- Reject Tableau HTML or an error page returned with HTTP 200.
