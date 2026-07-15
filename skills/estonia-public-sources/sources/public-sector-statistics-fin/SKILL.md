---
name: public-sector-statistics-fin
description: Download Ministry of Finance public-sector institution, civil-service salary, survey, and annual-report files from the official statistics index.
---

# Public-Sector Statistics

## Access

- Index: `https://www.fin.ee/riigihaldus-ja-avalik-teenistus-kinnisvara/riigihaldus/avaliku-sektori-statistika`
- The page contains direct XLSX/PDF links and optional Power BI dashboards; no authentication is required.

## Retrieve

Fetch the index and select by anchor label, not a dated storage URL:

- `Avaliku sektori asutused ...`: institution list XLSX.
- `Ametnike põhipalgad ... ja kogupalgad ...`: completed salary disclosure XLSX.
- `palgauuring`: salary survey PDFs.
- `Avaliku teenistuse aasta...`: annual-report PDFs.

The salary workbook separates local-government and state records and separates snapshot base salary from prior-year total salary. Read sheet-specific notes before locating the header row.

## Return

Return the index and file URLs, anchor title, file type, stated years, sheet name, original headers, retrieval time, and extracted records. Keep `põhipalk` snapshot dates separate from `kogupalk` earning years.

## Limits

- The page mixes datasets, reports, surveys, and dashboards. Do not treat every link as row-level statistics.
- Salary sheets can begin with explanatory rows and corrections before the tabular header.
- Power BI links are presentation views unless a separate export contract is verified.

## Verify

Require file signatures and expected workbook labels such as `Asutus`, `Ametikoht`, and `Põhipalk`; preserve correction notes attached to the selected sheet.
