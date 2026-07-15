---
name: consumer-technical-regulator-decisions
description: Query TTJA's public JSON register of Consumer Disputes Committee decisions and download the decision PDFs.
---

# Consumer Disputes Committee Decisions

## Access

- Register UI and JSON endpoint: `https://jvis.ttja.ee/modules/tarbijavaidluskomisjoni-otsused/avalik`
- Public access; no login is required.

## Retrieve

Send a GET request to the register with `_wbbdl=1`, `X-Requested-With: XMLHttpRequest`, and `Accept: application/json`. Optional query fields are:

- `search[company]`
- `search[published_date][from]` and `search[published_date][to]`
- `search[document_nr]`
- `search[decision]`: `for_customer` or `for_seller`
- `search[full_search]`
- `search[group_search]`

The JSON response contains `result`, `total`, and `items`. Each item includes `id`, `company`, `publishing_date`, `document_nr`, `decision`, `committee`, `summary`, and `public_pdf_id`. Download the decision from `/modules/media/media/download/{public_pdf_id}`.

## Return

- Preserve trader, publication date, decision number/outcome, committee, summary, PDF URL, query, total, and retrieval time.
- Treat the summary as an index description; use the PDF for the full reasoning.

## Limits

- The endpoint returns 10 items by default. Narrow searches are reliable; no documented bulk pagination contract is published.
- JSON rows and PDFs can contain names of consumers and committee members. Return personal data only when necessary for the request.
- This register covers Consumer Disputes Committee decisions, not all TTJA supervision or enforcement actions.

## Verify

- Require HTTP 200 JSON with `result=success`, positive `total`, and nonempty `items` for a focused company query.
- Require decision fields and confirm the first `public_pdf_id` URL returns a PDF beginning with `%PDF-`.
