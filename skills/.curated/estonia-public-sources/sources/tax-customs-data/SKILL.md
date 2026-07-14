---
name: tax-customs-data
description: Download Estonian Tax and Customs Board public tax-payment, turnover, employment, and related open-data files.
---

# Tax and Customs Open Data

## Access

Public large CSV downloads linked from the EMTA statistics page. No authentication.

## Endpoints

- Index: https://www.emta.ee/en/business-client/statistics-and-open-data
- Current file: https://ncfailid.emta.ee/s/e4DneiWeKFfje6d/download/tasutud_maksud_kaesolev_aasta_eng.csv
- Historical file: https://ncfailid.emta.ee/s/K8snLYNdZnqJCRn/download/tasutud_maksud_varasemad_aastad_eng.csv

## Retrieve

1. Use the current file for current-year quarterly updates and the historical file for earlier years.
2. Stream the CSV to disk or a parser; the current file can exceed 60 MB.
3. Parse as UTF-8 CSV with quoted English headers.
4. Filter by registry code, year, quarter, county, or activity after parsing.

## Return

Preserve `Data date`, `Registry code`, `Name`, `Type`, `County`, `Activity`, `Year`, quarterly state taxes, labour taxes/payments, turnover, employee counts, direct file URL, and retrieval time. Keep blank future-quarter cells as missing values.

## Limits

- This is published taxpayer-level aggregate information, not confidential tax-return data.
- A single entity can have multiple year rows; use both registry code and year as keys.
- Direct download tokens can change; if one fails, refresh it from the official index rather than guessing a replacement.

## Verify

Require HTTP 200 `text/csv`, a download filename, and a header containing `Data date`, `Registry code`, `Year`, and the quarterly tax fields. Verify at least one data row has a numeric registry code and parseable year.
