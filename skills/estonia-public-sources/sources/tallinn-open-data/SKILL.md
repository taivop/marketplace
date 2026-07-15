---
name: tallinn-open-data
description: Query Tallinn's universal municipal open-data API when a dataset page supplies its backing table name.
---

# Tallinn Open Data API

## Access

Public FastAPI GET service. No authentication. Dataset pages in the national portal document table names.

## Endpoints

- Instructions: https://avaandmed.tallinn.ee/
- OpenAPI: https://avaandmed.tallinn.ee/openapi.json
- Query: https://avaandmed.tallinn.ee/data/
- Known table example: https://avaandmed.tallinn.ee/data/?table=andurid_data&page=1&per_page=2

## Retrieve

1. Find the Tallinn dataset in `andmed.eesti.ee`; read its description for the `table` name. The API does not list tables.
2. Query `/data/` with required `table` and optional `columns`, `filters`, `order_by`, `page`, and `per_page`.
3. Use `page >= 1` and `1 <= per_page <= 1000`; paginate until a page is shorter than `per_page`.
4. Treat `filters` as the service's documented SQL-WHERE-style expression and URL-encode it.

The `andurid_data` example returns Old Town gate sensor records with `id`, `andurid_id`, `name`, `ts`, `pir`, `in`, `out`, `humidity`, and `temp`.

## Return

Preserve the national catalog page, table name, columns/filter/order, page size, original fields, source endpoint, and retrieval time.

## Limits

- A made-up or stale table name returns a JSON 500 with `Table not found`; the OpenAPI schema alone cannot discover valid tables.
- Maximum documented concurrency is five requests and query timeout is 20 seconds.
- Different tables have unrelated schemas.

## Verify

Require HTTP 200 JSON and a list of records. For `andurid_data`, require `andurid_id`, `name`, `ts`, and numeric count fields. A 422 missing-table response or 500 table-not-found response is not successful access.
