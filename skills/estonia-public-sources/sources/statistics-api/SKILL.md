---
name: statistics-api
description: Query Statistics Estonia PXWeb tables and metadata for official indicators, time series, and table-level methodology.
---

# Statistics Estonia API

## Access

Public PXWeb JSON API. No authentication. Use `https://andmed.stat.ee/api/v1/en/stat` for English or replace `en` with `et` for Estonian.

## Retrieve

1. Discover folders and tables with `GET /api/v1/en/stat`; descend by appending returned folder IDs.
2. Fetch a table contract with `GET /api/v1/en/stat/{TABLE_ID}`. It returns `title` and `variables`; use each variable's `code` and allowed `values` in the query.
3. POST the query to the same table URL:

```json
{
  "query": [
    {"code": "Aasta", "selection": {"filter": "item", "values": ["2025"]}}
  ],
  "response": {"format": "json-stat2"}
}
```

4. Request with `Content-Type: application/json`. Use `csv`, `json-stat2`, or another format accepted by the table service.
5. When methodology matters, run `python get_metadata.py TABLE_ID --format text` from this directory.

Working sample: `GET https://andmed.stat.ee/api/v1/en/stat/IA001`, then POST the payload above. The response is JSON-stat 2 with table ID `IA001`, year `2025`, and a numeric `value`.

Known tables (verified 2026-07-24):

- Wages: `PA001` is discontinued (data ends 2022Q4). Annual wage statistics live in `PA101` under `majandus/palk-ja-toojeukulu/palk/aastastatistika` (updated 2026-03).
- Population totals: `RV021` under `rahvastik/rahvastikunaitajad-ja-koosseis/rahvaarv-ja-rahvastiku-koosseis/RV021.PX`.

## Return

Preserve the table ID, source and update metadata, dimension codes and labels, selected values, units/decimals, observations, exact POST payload, and retrieval time.

## Limits

- The API root itself returns 404; include the language and database path.
- Table IDs are not enough to construct a query: always read the current variable contract first.
- Confirm units, seasonal adjustment, reference period, and suppression markers before analysis.
- Variable codes may contain non-ASCII characters (e.g. `Vanuserühm` in RV021); send them exactly as returned by the table contract.
- Discontinued tables still return contracts and data; check the last period value before treating a table as current.

## Verify

Require HTTP 200 JSON, `variables` in the table contract, and matching `id`, `dimension`, `size`, and `value` fields in a JSON-stat response. A portal HTML page or API-base 404 is not successful retrieval.
