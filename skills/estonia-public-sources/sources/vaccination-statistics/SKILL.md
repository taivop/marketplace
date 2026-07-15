---
name: vaccination-statistics
description: Access the Health Board's official COVID-19 and influenza vaccination Tableau dashboards and export published immunization coverage data.
---

# Vaccination Statistics

## Access

- Official page: `https://www.terviseamet.ee/en/nakkushaigused/statistika/vaktsineerimine`
- COVID-19 workbook: `https://tableauapp.tehik.ee/t/Terviseamet/views/Covid-19vaccination/Vaccinationmap`
- Influenza workbook: `https://tableauapp.tehik.ee/t/Terviseamet/views/Influenzavaccination/Mapview`
- Public Tableau views; no login is required.

## Retrieve

Use the official page to discover the current workbook/view names. Append `.csv?:showVizHome=no` to a Tableau view for its active-sheet export. For example:

`https://tableauapp.tehik.ee/t/Terviseamet/views/Influenzavaccination/Mapview.csv?:showVizHome=no`

The influenza default export includes vaccination season and coverage measures. The COVID default `Vaccinationmap` CSV may expose only the active age-group sheet; use Tableau's view/worksheet export controls when other dashboard measures are required.

## Return

- Preserve vaccination type, season/date, age group, geography, dose/status definition, numerator, denominator, coverage, original field names, workbook/view URL, and retrieval time.
- Treat decimal coverage values as proportions unless the field label or dashboard explicitly formats them as percentages.
- State the dashboard's data period, not just the retrieval date.

## Limits

- A Tableau CSV exports the active worksheet, not necessarily every measure visible on a dashboard.
- Sheet names and default filters can change when the publisher updates a workbook.
- Do not combine COVID-19 and influenza coverage without retaining their different seasons and eligibility definitions.

## Verify

- Require the official page to embed both named Tableau workbooks.
- Require the selected export to return HTTP 200 `text/csv`, a header row, and data rows. Reject Tableau HTML or a one-column selector export when the requested measure is absent.
