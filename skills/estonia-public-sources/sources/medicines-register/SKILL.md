---
name: medicines-register
description: Download public Estonia Medicines Register CSV/XML datasets for products, packages, substances, dosage forms, administration routes, and ATC codes.
---

# Medicines Register Downloads

## Use when
- You need medicinal-product or package records, authorization status, substances, dosage forms, administration routes, or ATC codes.
- You need a complete bulk extract rather than manual search results.

## Avoid when
- You need annual market or pharmacy indicators; use `medicines-agency-statistics`.

## Endpoint
- Public downloads: https://www.ravimiregister.ee/publichomepage.aspx?pv=PublicDownloads

## Workflow
1. Start a cookie-preserving HTTP session and GET the downloads page.
2. Parse all hidden form fields, including `__VIEWSTATE`, `__VIEWSTATEGENERATOR`, and `__EVENTVALIDATION`.
3. POST them to the same URL with `__EVENTTARGET` set to the required control and an empty `__EVENTARGUMENT`.
4. Parse the returned CSV with UTF-8 BOM and semicolon delimiters, or parse XML against the downloadable schema.

## Export controls
- Packages CSV: `ctl10$packagesCsvDownload`
- Detailed packages CSV: `ctl10$packagesDetailedCsvDownload`
- Detailed packages CSV v2: `ctl10$packagesSpecialCsvDownload`
- Packages XML: `ctl10$packagesXmlDownload`
- Human medicines: `ctl10$humMedDownload`
- Veterinary medicines: `ctl10$vetMedDownload`
- Active substances CSV: `ctl10$downloadActiveSubstancesCsv`
- Dosage forms CSV: `ctl10$downloadMedFormsCsv`
- Administration routes CSV: `ctl10$downloadRoutesOfAdministrationCsv`
- Human/veterinary ATC CSV: `ctl10$humAtcDownload`, `ctl10$vetAtcDownload`

## Access reality
- Public ASP.NET WebForms exports with no login, verified 2026-07-14.
- The packages postback redirects to `https://www.ravimiregister.ee/Data/XML/pakendid.csv` and returns a UTF-8 semicolon CSV with product, package, authorization, pricing, and medicine-information fields.

## Output schema expectations
- Preserve package/product identifiers, names, ATC code, active substance, strength, form, prescription status, authorization holder/status dates, and source URL when present.
- Keep authorization-ended, unauthorized, human, and veterinary records distinguishable.

## Limits and caveats
- Do not hard-code `__VIEWSTATE` or other hidden values; fetch them for each session.
- The server uses `application/octet-stream` for CSV. Validate the BOM/header and parse content rather than relying on MIME type.
- This is medical-regulatory data, not prescribing advice.

## Verification hooks
- Require a successful downloads page containing the requested postback control.
- For packages CSV, require a UTF-8 BOM and a header beginning `Pakendi liik;Ravimi liik;Pakendi kood;Pakendi nimetus;ATC kood`.
