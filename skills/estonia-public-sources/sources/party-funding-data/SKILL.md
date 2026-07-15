---
name: party-funding-data
description: Query the ERJK JSON API for Estonian political-party quarterly and election funding reports, receipts, expenses, donors, and suppliers.
---

# Party Funding Data (ERJK)

## Use when
- You need party revenue, expenditure, donor, or supplier data.
- You need quarterly or election-report comparisons across parties.

## Avoid when
- You need party membership records; use `political-party-membership`.

## Endpoints
- OpenAPI YAML: https://www.erjk.ee/avaandmed/erjkapi.yaml
- Parties: `https://erjk.ee/api/quarterly-reports/parties`
- Party reports: `https://erjk.ee/api/quarterly-reports/quarters/{party_id}`
- One report: `https://erjk.ee/api/quarterly-reports/{report_id}?report_type=receipts`
- Receipt query: `https://erjk.ee/api/quarterly-reports/queries/receipts?party_id=159&category_id=all&period=2025&quarter=quarter`
- Expense query: `https://erjk.ee/api/quarterly-reports/queries/expenses?party_id=159&category_id=all_by_group&period=2025&quarter=quarter`
- Election events: `https://erjk.ee/api/events`
- Classifiers: `https://erjk.ee/api/categories/receipts`, `https://erjk.ee/api/categories/expenses`

## Workflow
1. Resolve `party_id`, category IDs, or election `event_id` from their list endpoints.
2. Use aggregate query endpoints for comparisons; use report endpoints for record-level receipts or expenses.
3. Preserve the exact query URL and return numeric amounts without silently rounding.

## Access reality
- Public unauthenticated JSON API, verified 2026-07-14.
- The 2025 receipt example returns party/category/quarter rows with `amount`, `period`, `party_id`, `party_name`, `category_id`, `category_name`, and `quarter`.
- Requests may redirect from `/api/...` to `/et/api/...`; allow redirects.

## Request contract
- `report_type` is required on individual quarterly and election report endpoints and accepts `receipts` or `expenses`.
- `party_id` accepts a numeric ID, `all`, or `all_sum` where documented.
- `category_id` supports endpoint-specific aggregate values such as `all`, `all_by_group`, and `all_sum`.
- `quarter=quarter` groups a selected year by quarter; `q1` through `q4` select quarter bounds.
- The OpenAPI `period` enum is stale and stops at 2022; discover newer years from party report lists rather than rejecting them locally.

## Output schema expectations
- Preserve IDs, names, period, quarter, category, amount, report type, and the exact request URL.
- Keep receipts and expenses separate.

## Limits and caveats
- Party and category lists include inactive or historical values; do not treat every returned party as currently registered.
- Amounts are JSON strings. Parse them as decimal values, not binary floats, when totals must reconcile.

## Verification hooks
- Require `application/json` and the expected ID/name fields on list endpoints.
- For aggregate queries, require at least one row and preserve its period and party/category identifiers.
