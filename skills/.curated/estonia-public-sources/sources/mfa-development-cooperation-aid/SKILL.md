---
name: mfa-development-cooperation-aid
description: Search and export project-level records from Estonia's public development cooperation database (AKTA).
---

# Development Cooperation Projects (AKTA)

## Access

- Search form: `https://akta.mfa.ee/andmed_otsing.php?language=eng`
- Result list: `https://akta.mfa.ee/andmed.php`
- CSV export: `https://akta.mfa.ee/andmed_csv.php`
- Public, no authentication. Search state and export are tied to a PHP session.

## Search And Export

1. GET the search form with a cookie jar and extract hidden `_csrf_token`.
2. POST the form back to `andmed_otsing.php`, preserving cookies. Useful fields include:
   - `aasta_a`, `aasta_k`: project-year range
   - `makse_aasta_a`, `makse_aasta_k`: payment-year range
   - `summa_alates`, `summa_kuni`
   - `makstud_summa_alates`, `makstud_summa_kuni`
   - `tekst`: free text
   - `projekti_andmed`: project number
   - `tegevuse_staadium`: `1` planned, `2` ongoing, `3` completed
   - `koostoovorm`: `1` bilateral, `2` multilateral
3. Include the form defaults `aastased_projektid=0`, `kaasfinantseerija=0`, `mitu_riiki=1`, `mitu_arenguabi_liiki=1`, and submit field `otsi=Otsi` unless replacing them with selected values.
4. Follow the redirect to `andmed.php`. Parse project links `andmed_vaata.php?id=<id>` for HTML records, or GET `andmed_csv.php` in the same session for the complete filtered export.
5. Decode the CSV as Windows-1257 and parse it as semicolon-delimited data. Cells use Excel-safe values such as `="2025"`; remove that wrapper without evaluating formulas.

## Return

Preserve the CSV columns, including year, contributor, implementer, status, recipient country, amount, ODA-counted amount, project name and description, cooperation form, dates, project number, and per-year payments. Include filters and retrieval time.

## Limits

- A CSV request without the search session may return a different/default result set.
- The English language parameter does not consistently translate labels or records.
- Payment-year columns vary with the selected records.

## Verify

Require the redirected result page to contain project-detail links. Require the CSV header to contain `Aasta`, `Projekti nimi`, and `Arvesseminev summa EUR`, followed by at least one record matching the requested year or other filter.
