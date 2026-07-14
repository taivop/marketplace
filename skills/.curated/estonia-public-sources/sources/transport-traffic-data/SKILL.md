---
name: transport-traffic-data
description: Query Estonia's Peatus GraphQL service for public transport stops and routes, plus official public transport notices and road-traffic publications.
---

# Transport and Public Transit

## Access

Public GraphQL POST endpoint and JSON notifications. No authentication.

## Endpoints

- GraphQL: https://api.peatus.ee/routing/v1/routers/estonia/index/graphql
- Notifications: https://web.peatus.ee/admin/api/public/notifications
- Road traffic publications: https://www.transpordiamet.ee/liiklussagedus

## Retrieve

POST JSON with `Content-Type: application/json`:

```json
{"query":"{stops(name:\"Tallinn\"){name gtfsId lat lon}}"}
```

Use `{"query":"{__typename}"}` as a schema sanity check. Scope stop/route queries to avoid very large responses. Fetch the notifications endpoint directly for current operational notices. Use Transport Administration files only when the question concerns road traffic rather than scheduled transit.

## Return

Preserve the GraphQL query, `gtfsId`, name, coordinates, mode/route fields requested, errors, endpoint, and retrieval time. For notices preserve publication time, affected service/location, text, and source URL.

## Limits

- GET on the GraphQL endpoint can return a server error; use POST.
- The schema can evolve; retain the exact query with the result.
- Name searches can return multiple stops with the same display name.

## Verify

Require HTTP 200 JSON with no top-level GraphQL `errors`. The sanity query must return `data.__typename: QueryType`; the Tallinn sample must return at least one stop with `name`, `gtfsId`, numeric `lat`, and numeric `lon`.
