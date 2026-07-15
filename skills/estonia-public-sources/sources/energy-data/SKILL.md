---
name: energy-data
description: Query Elering public dashboard APIs for Estonian electricity prices, production, consumption, forecasts, balances, and cross-border flows.
---

# Elering Energy Data

## Access

Public JSON GET endpoints at `https://dashboard.elering.ee/api/`. No authentication.

## Retrieve

Use ISO-8601 UTC timestamps. Known-valid examples:

```text
GET https://dashboard.elering.ee/api/nps/price?start=2026-07-01T00%3A00%3A00.000Z&end=2026-07-02T00%3A00%3A00.000Z
GET https://dashboard.elering.ee/api/system/with-plan?start=2026-07-01T00%3A00%3A00.000Z&end=2026-07-02T00%3A00%3A00.000Z
```

For cross-border analysis also use `/api/transmission/cross-border` with the same `start` and `end` contract.

Parse `data` by series. Price data has regional arrays (`ee`, `fi`, `lv`, `lt`) with `timestamp` and `price`. System data has `real` and `plan` arrays with fields such as `production`, `consumption`, `frequency`, `system_balance`, `ac_balance`, and renewable/solar values.

## Return

Keep the endpoint, exact UTC window, series/region, Unix timestamp, original measurements, inferred interval, retrieval time, and missing-value flags. Convert timestamps only after preserving the originals.

## Limits

- Literal `...` placeholders are invalid and return 400.
- Values and intervals can change at daylight-saving or market-resolution boundaries; infer cadence from returned timestamps.
- Do not combine `real` and `plan` values without labeling them.

## Verify

Require HTTP 200 JSON, `success: true`, and non-empty arrays under the expected `data` keys. Check timestamps fall inside the requested window and required measurement fields are numeric or explicitly null.
