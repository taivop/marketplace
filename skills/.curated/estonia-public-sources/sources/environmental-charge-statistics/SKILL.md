---
name: environmental-charge-statistics
description: Download Environmental Board charge declarations by county, fee category, and year from the official XLSX workbook.
---

# Environmental Charge Statistics

## Access

- Index: `https://www.keskkonnaamet.ee/en/supervision-environmental-charge/environmental-charge/statistics`
- Fetch the index and resolve its `.xlsx` link against the index URL; do not hard-code the dated file path.
- Send a browser-like `User-Agent` and the index URL as `Referer` when downloading the workbook. The file host otherwise may return HTTP 403.

## Retrieve

1. Parse the index for the environmental-charge statistics `.xlsx` link.
2. Download it with `Referer` set to the index URL.
3. Read both workbook sheets:
   - `Maakondade kaupa`: `Deklaratsiooni valdkond`, `Maakond`, `Aasta`, and declared-charge amount columns.
   - `Liikide kaupa`: the same category/year/amount fields plus whichever of `Saasteaine`, `Maavara liik`, `Veekasutusala`, `Jäätmegrupp`, or `Tuulepargi liik` identifies the fee subtype.

## Return

Preserve the Estonian headers, workbook URL, sheet name, retrieval time, category, geography or subtype, year, and both original and rounded declared amounts.

## Limits

- This is declared environmental-charge data, not payment or collection data.
- Coverage follows the current workbook; inspect its year values rather than assuming the page text is current.
- Empty subtype columns are intentional because one table combines several declaration domains.

## Verify

Require an XLSX ZIP signature (`PK`) and the two expected sheet/header sets before using values.
