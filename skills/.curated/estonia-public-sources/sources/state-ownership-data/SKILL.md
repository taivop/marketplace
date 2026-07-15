---
name: state-ownership-data
description: Extract current state-owned companies, ownership shares, purposes, sectors, and state-founded foundations from the Ministry of Finance tables.
---

# State Ownership Data

## Access

- `https://www.fin.ee/en/public-procurement-state-aid-and-assets/state-assets/state-stakeholdings`
- Public server-rendered HTML; no login or browser JavaScript is required.

## Retrieve

Fetch the page with a normal user agent and parse the tables under `State-owned companies` and `Foundations`.

For operating companies, preserve:

- administering ministry
- company name
- `Share of state` and its as-of date
- public-interest / income-earning purpose
- field of activity

For foundations, preserve:

- administering ministry
- foundation name
- number of founders
- foundation date
- stated goal

The narrative immediately above each table provides the reporting period and aggregate counts, assets, turnover, and employment. Associate those values with their stated as-of dates rather than treating the page retrieval date as the data date.

## Return

- Return one row per company or foundation with the original organization name and table labels.
- Include entity type, administering ministry, page update date, source URL, and retrieval time.
- Keep decimal commas and ownership percentages as published; add normalized numeric columns only in addition to the originals.

## Limits

- This is a current snapshot page, not a historical API.
- The English and Estonian versions may be updated at different times; identify the language used.
- Company-level financial statements are not supplied by these tables. Use the Business Register for company filings and baseline entity data.

## Verify

- Require HTTP 200 `text/html` containing `State-owned companies`, `Share of state`, `Foundations`, and multiple named entities.
- Require an explicit as-of period near the company table. Reject a navigation shell or policy-only page.
