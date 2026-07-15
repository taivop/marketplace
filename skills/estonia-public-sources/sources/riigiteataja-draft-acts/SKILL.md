---
name: riigiteataja-draft-acts
description: Query Riigi Teataja's public JSON API for draft-act proceedings, stages, issuers, statuses, and links back to EIS documents.
---

# Riigi Teataja Draft Proceedings

## Access

- Search UI: `https://www.riigiteataja.ee/et/otsing/eelnoud`
- Search API: `POST https://www.riigiteataja.ee/public-api/api/v1/otsing/eelnoud`
- Detail API: `POST https://www.riigiteataja.ee/public-api/api/v1/avalik/eelnou`
- Public JSON; no login is required.

## Retrieve

Use this minimal search payload:

```json
{
  "general": {
    "searchInText": false,
    "searchInTitle": false,
    "searchText": "",
    "searchText2": "",
    "logicalOperator": "AND",
    "morphSearch": false,
    "sort": "esimeseEtapiAeg",
    "sortAscending": false
  },
  "precise": {}
}
```

Precise fields are `aktiAndja`, `eelnouLiik`, `menetluseAlgus`, `menetluseLopp`, `menetluseEtapp`, and `menetluseNr`. The response contains `kokku` and up to 30 `tulemused`; each result includes `id`, `pealkiri`, `eelnouLiik`, `aktiAndja`, `menetluseAlgus`, `menetlusKaik`, and stage records in `etapid`.

To resolve one proceeding, POST `{"menetluseId":"REM/26-0818"}` to `/avalik/eelnou`. Follow each stage's `menetlusTeave` URL to EIS for draft files and coordination material.

## Return

- Preserve the Riigi Teataja ID, title, type and issuer codes, proceeding number, start date, every stage's name/time/authority/status/EIS URL, query, and retrieval time.
- Keep draft proceedings separate from enacted acts. Use `legal-acts-data` to resolve final law text.

## Limits

- The search returns 30 rows and exposes no documented bulk pagination contract. Use date, issuer, type, or proceeding-number filters.
- Issuer and type values are classifier codes; read current choices from the search UI rather than guessing labels.
- Riigi Teataja indexes the lifecycle, while EIS holds the underlying draft documents.

## Verify

- Require HTTP 200 JSON with positive `kokku` and nonempty `tulemused` for the minimal search payload.
- Require result rows to contain `id`, `pealkiri`, `menetlusKaik`, and nonempty `etapid`; require stage records to contain `etapp`, `aeg`, `staatus`, and `menetlusTeave`.
