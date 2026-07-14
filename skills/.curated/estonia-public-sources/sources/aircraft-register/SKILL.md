---
name: aircraft-register
description: Fetch Estonia's current public aircraft register table, including registration marks, aircraft types, owners, and operators.
---

# Aircraft Register

## Access

- Data page: `https://www.transpordiamet.ee/ohusoidukite-register`
- Method: `GET`
- Response: server-rendered HTML; no public JSON endpoint is documented.

## Retrieve

1. Fetch the data page and locate the table containing `Registration mark` and `Type of the Aircraft`.
2. Read the update date and total from the table's first row.
3. For each aircraft row, use physical cells 2, 5, 6, 7, and 8 (one-based). The other cells are empty layout columns.
4. Normalize whitespace, including non-breaking spaces, but preserve identifiers and names.

Return:

- `registration_mark`
- `aircraft_type`
- `serial_number`
- `owner`
- `operator`
- `register_update_date`
- `source_url`

## Limits

- This is a complete published table, not an identifier search API.
- Owners and operators may be `eraisik` (private person); do not infer a hidden identity.
- The update date is written as `DD.MM.YYYY/updated`, without a `Register seisuga` label.

## Verify

Require the five bilingual column labels, a date matching `DD.MM.YYYY/updated`, and multiple registration marks beginning `ES -` after whitespace normalization.
