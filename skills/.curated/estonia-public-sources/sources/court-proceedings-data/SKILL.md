---
name: court-proceedings-data
description: Query Riigi Teataja's public JSON endpoints for Estonian court decisions and court hearings.
---

# Court Decisions and Hearings

## Access

- Search UI: `https://www.riigiteataja.ee/et/otsing/kohtulahendid`
- API base: `https://www.riigiteataja.ee/public-api/api/v1`
- Public JSON POST endpoints; no login is required.

## Retrieve

Post JSON to `/kohtuteave/otsing/kohtulahendid` for decisions. A minimal request is:

```json
{
  "general": {
    "searchInText": false,
    "searchInTitle": false,
    "searchText": "",
    "searchText2": "",
    "logicalOperator": "AND",
    "morphSearch": false,
    "sort": "toiminguNr",
    "sortAscending": false
  },
  "precise": {"kohus": [], "seaduseSatted": {}}
}
```

Post the same `general` object to `/kohtuteave/otsing/kohtuistungid` with `precise: {"kohus": []}` for hearings. Useful precise decision fields include `lahendiKpAlgus`, `lahendiKpLopp`, `kohtunik`, `ecliNr`, `menetluseTyyp`, `menetlusliigid`, `kohtumenetluseLiik`, and `kohus`. Hearing fields include `istungiAegAlgus`, `istungiAegLopp`, `istungiLiik`, `istungiSaal`, `kohtunik`, `menetluseLiik`, and `kohus`.

Both responses contain `kokku` and up to 30 `tulemused`. Narrow the query with dates or court filters; do not treat the first response as a bulk export. A decision's public file is `GET /kohtuteave/kohtulahendid/{avalikustatudFailiId}/file`.

## Return

- Decisions: preserve `objektId`, case number, ECLI when present, court, decision date, proceeding type, status, public-file ID/name, annotations, and source URL.
- Hearings: preserve case number, court, judge, hearing time/type/room, status, title, query, and retrieval time.
- Do not infer an outcome from a hearing listing or an annotation.

## Limits

- Publicity restrictions and redactions apply; this is not access to complete case files.
- The result API returns 30 rows at a time and exposes no documented bulk pagination contract. Use focused searches.
- Historical URLs ending in `koik_menetlused.html` and `kohtuistungid_otsing.html` now load the same JavaScript application; they are not data endpoints.

## Verify

- Require HTTP 200 JSON with integer `kokku` and nonempty `tulemused` from both POST endpoints.
- Require decision rows to contain `kohtuasjaNumber`, `objektId`, and `lahendiKuulutamiseAeg`; require hearing rows to contain `kohtuasjaNr`, `kohus`, and `istungiAeg`.
