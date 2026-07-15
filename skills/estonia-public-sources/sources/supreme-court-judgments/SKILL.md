---
name: supreme-court-judgments
description: Query the Supreme Court's public server-rendered judgment search by case number, date, proceeding type, annotation, or text.
---

# Supreme Court Judgments

## Access

- Supreme Court page: `https://www.riigikohus.ee/et/lahendid`
- Search endpoint embedded by that page: `GET https://rikos.rik.ee/`
- Public HTML; no login or browser automation is required.

## Retrieve

Send search fields as query parameters. The short parameter names accepted by the public form include:

- `asjaNr`: case number
- `asjaLiigidIds`: case type classifier, repeat for multiple values
- `syyteoLiigidIds`: offence type classifier
- `otsuseKpalgus`, `otsuseKpLopp`: decision date range
- `annotatsioon`: annotation text
- `tekst`: full-text term
- `pageSize`: 1-100
- `sortVaartus`: `LahendiKuulutamiseAeg` or `Menetlus.MenetluseNR`
- `sortAsc`: `true` or `false`

For example, `?tekst=pohiseadus&pageSize=25` returns matching rows. Follow `/LahendiOtsingEriVaade?asjaNr=...` for the decision view. Add `genereeriPdf=True` to the same search query for the site's result-list PDF.

## Return

- Preserve case number, decision date/type, title or annotation, detail URL, search parameters, result count, and retrieval time.
- Link the decision text or file itself when available; do not summarize a holding from the result-list snippet alone.

## Limits

- This search is Supreme Court-specific. Use `court-proceedings-data` for all court levels and public hearing listings.
- Search results are HTML, not JSON. Parse the result table and resolve relative links against `https://rikos.rik.ee/`.
- Some judgments are redacted or not publicly available.

## Verify

- Require a focused text query to return a positive `Tulemused` count and rows with `/LahendiOtsingEriVaade?asjaNr=` links.
- Confirm that the Supreme Court page still embeds `https://rikos.rik.ee/`; reject unrelated files linked elsewhere on the page as judgment results.
