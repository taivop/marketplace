---
name: health-statistics
description: Query the National Institute for Health Development PxWeb API for official Estonian health indicators and machine-readable multidimensional tables.
---

# Estonia Health Statistics

## Access

- API root: `https://statistika.tai.ee/api/v1/et/`
- Database root: `https://statistika.tai.ee/api/v1/et/Andmebaas`
- The path is case-sensitive. The public API requires no authentication.

## Discover

GET the database root, then append each list item's `id` while `type` is `l`. A table item has `type: "t"`, an `.px` `id`, title, and update timestamp. GET the complete table path to retrieve its dimension metadata.

## Query

POST the standard PxWeb body to the same `.px` URL:

```json
{
  "query": [
    {"code": "Aasta", "selection": {"filter": "item", "values": ["2025"]}},
    {"code": "Elulisus", "selection": {"filter": "item", "values": ["1"]}}
  ],
  "response": {"format": "json-stat2"}
}
```

The example table is `Andmebaas/01Rahvastik/02Synnid/SR001.px`. Always GET metadata first and use its exact dimension codes and values.

## Return

Preserve table path/title, source, update timestamp, notes/methodology links, dimension codes and labels, units, selected categories, values, and retrieval time.

## Limits

- Public aggregates only; no patient-level records.
- Table notes can define denominator changes, breaks, and mandatory caveats.
- Keep missing/suppressed values distinct from zero.

## Verify

Require JSON-stat2 `class: "dataset"`, matching `id`/`size` dimensions, a value count equal to the product of `size`, and the table's source and notes.
