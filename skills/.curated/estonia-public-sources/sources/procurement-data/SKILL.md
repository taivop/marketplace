---
name: procurement-data
description: Download Estonian public procurement and award notices as monthly XML from the official procurement register open-data API.
---

# Procurement Open Data

Use this source for tender notices, contract awards, and notice amendments. Use `public-finance-data` for budget totals without procurement detail.

## Endpoints

- Register UI: `https://riigihanked.riik.ee/rhr-web/`
- Procurement and modification notices: `https://riigihanked.riik.ee/rhr/api/public/v1/opendata/notice/{year}/month/{month}/xml`
- Contract, award, and modification notices: `https://riigihanked.riik.ee/rhr/api/public/v1/opendata/notice_award/{year}/month/{month}/xml`

`year` is four digits and `month` is `1` through `12`. The response is XML rooted at `OPEN-DATA`, although the server labels it `application/vnd.ms-excel`. Files can be tens of megabytes, so stream them to disk instead of loading them into memory.

## Workflow

1. Download both notice types for every required month.
2. Parse XML with a namespace-aware parser. Notice schemas and namespaces vary by notice type and year.
3. Keep the original notice identifier and type, publication and procedure dates, buyer and supplier identifiers/names, CPV codes, and estimated or awarded values when present.
4. Distinguish procurement notices, awards, and amendments before aggregation. Do not treat estimated values as contract values.
5. Record the canonical monthly URL and retrieval time with every extract.

## Verification

- A valid response starts with an XML declaration followed by `OPEN-DATA` and `TED_ESENDERS`.
- The server supplies filenames such as `HT_2019_1.xml` for `notice` and `HLST_2019_1.xml` for `notice_award`.
