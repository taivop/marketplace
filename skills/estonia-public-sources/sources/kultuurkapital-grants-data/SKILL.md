---
name: kultuurkapital-grants-data
description: Extract award-level Estonian Cultural Endowment allocations from official round-page HTML tables.
---

# Kultuurkapital Grant Allocations

## Access

- Round index: `https://www.kulka.ee/avalik-teave/eraldused-voorude-kaupa`
- Public HTML, no authentication or API.

## Retrieve

1. GET the index and collect unique links under `/avalik-teave/eraldused-voorude-kaupa/`.
2. Select the requested year and round from the link slug; do not invent slugs because historical naming varies.
3. GET the round page and parse each grant table. The first row is the header rather than a `thead` in many tables.
4. Normalize the header variants:
   - recipient: `Eralduse saaja`
   - purpose: `Kasutamise eesmärk` or `Eralduse eesmärk`
   - amount: `Summa` or `Eraldatud summa`
5. Associate each table with the nearest preceding heading, such as a council, endowment, programme, or county expert group.
6. Remove normal and non-breaking spaces from amount text, then parse it as euros while preserving the original value.

## Return

Return round slug, source URL, section heading, recipient, purpose, original amount, and numeric amount.

## Limits

- Round pages contain many independently formatted tables and occasional empty tables.
- Section headings are outside the tables; a flat table parser loses this context.
- Published recipients include individuals. Return only fields present in the public allocation table.

## Verify

Require at least one round link and one non-empty three-column table whose normalized headers identify recipient, purpose, and amount.
