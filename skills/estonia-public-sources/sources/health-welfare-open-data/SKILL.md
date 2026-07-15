---
name: health-welfare-open-data
description: Query TEHIK's public PostgREST API for current seasonal COVID-19 hospitalization and risk-group vaccination aggregates.
---

# TEHIK Seasonal COVID-19 Open Data

## Access

- OpenAPI document and API root: `https://rest-avaandmed.tehik.ee/covid19/`
- Swagger UI: `https://rest-avaandmed.tehik.ee/covid19/swagger/`
- No authentication is required.

## Datasets

- `opendata_covid19_hospitalization`: weekly hospitalization counts by age group and bed profile.
- `opendata_covid19_riskgroup_vaccination_season_location_agegroup`: seasonal risk-group population and vaccination counts by date, county, and age group.
- `metadata_odata`: field/table descriptions, including historical schema metadata.

## Query

Use PostgREST URL parameters such as `select`, `order`, `limit`, `offset`, and column filters (`eq.`, `gte.`, `lte.`, `in.(...)`). Example:

```text
GET https://rest-avaandmed.tehik.ee/covid19/opendata_covid19_hospitalization?Valid=eq.true&order=StatisticsWeek.desc&limit=100
```

Request JSON by default or `text/csv` with the `Accept` header.

## Return

Preserve source endpoint, query, retrieval time, statistics date/week, season, geography/EHAK code, age group or bed profile, population/count fields, `Valid`, and `ModifiedAt`.

## Limits

- These are seasonal COVID-19 aggregates, not a general health/welfare catalog and not individual records.
- Filter to `Valid=eq.true` unless invalidated revisions are explicitly needed.
- A row with null dimensions may be a total; do not combine it with detailed rows without checking aggregation level.

## Verify

Use the root OpenAPI document as the current schema, require the documented field set, and check `Valid` plus `ModifiedAt` before analysis.
