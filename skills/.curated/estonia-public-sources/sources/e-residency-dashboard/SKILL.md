---
name: e-residency-dashboard
description: Extract current official e-Residency headline and country metrics from the dashboard's embedded Next.js data.
---

# e-Residency Dashboard

Use this source for programme totals, recent applications, e-resident companies, and country rankings. Use `business-register-open-data` for legal-entity records.

## Endpoint

`https://www.e-resident.gov.ee/dashboard/`

The page has no documented data API. Its server HTML contains React Flight calls of the form `self.__next_f.push([1,"..."])` with the dashboard data inside the string payload.

## Extraction

1. GET the HTML.
2. Regex each `self.__next_f.push((\[.*?\]))</script>` call with DOTALL and decode the captured array using a JSON parser.
3. Keep element `1` when it is a string. In the decoded strings, locate a quoted metric key followed by `:` and use a JSON decoder's `raw_decode` at the next character to parse its value.
4. Extract only the metric groups needed. Stable current groups include:
   - `top-figures`: objects with `names` and `values`
   - `top-countries-by-number-of-applications-in-the-last-12-months`: `citizenship`, `code`, `value`
   - `top-countries-by-number-of-e-residents`: `citizenship`, `code`, `value`
5. Keep the exact metric key, labels, values, dimensions, source URL, and retrieval time.

Do not scrape chart pixels or assume these cumulative figures equal Business Register counts. The frontend payload can change, so fail clearly if a requested key is absent.

## Verification

The current page yields five `top-figures` rows and nonempty country arrays with two-letter country codes and numeric values.
