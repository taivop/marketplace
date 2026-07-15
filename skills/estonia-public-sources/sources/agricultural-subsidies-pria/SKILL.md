---
name: agricultural-subsidies-pria
description: Download recipient-level agricultural and rural support payments from PRIA's public CSV export.
---

# PRIA Support Recipients

## Access

- Filter page: `https://www.pria.ee/toetused/toetusesaajad`
- Public, no authentication; labels and CSV headers are Estonian.
- Coverage is the two latest completed financial years, not the current financial year.

## Retrieve

1. GET the filter page with any of these query parameters:
   - `year`: a listed year or `all`
   - `name`: recipient name
   - `county`, `township`: values from the page's select controls
   - `type=payed`
   - `mp[<code>]=<code>`: one or more measure codes read from the current form
2. Preserve the response cookies.
3. Parse the CSV link whose path starts `/download/file/PRIA_export_`. The URL includes the selected filters plus transient `form_build_id` and `form_id=filter_receivers_form` values.
4. GET that absolute URL with the same cookies. Do not construct or reuse an old export URL.
5. Decode UTF-8 with BOM and parse as semicolon-delimited CSV after removing the first `sep=;` line.

## Return

Preserve the original columns. Key fields include `Toetusesaaja nimi`, `Maakond`, `Omavalitsus`, `Meede/sekkumisviis/sektor`, measure code, the EAGF/EAFRD and co-financing amount columns, and `Finantsaasta`. Also return the filter-page URL, resolved export URL, filters, and retrieval time.

## Limits

- Rows ending in ` KOKKU` are recipient totals; do not mix them with measure rows.
- Decimal commas and empty amount cells require locale-aware parsing.
- Measure codes and available years change with each publication.

## Verify

Require `sep=;`, a header containing `Toetusesaaja nimi` and `Finantsaasta`, and at least one data row. For a single-year request, verify non-total rows carry that year.
