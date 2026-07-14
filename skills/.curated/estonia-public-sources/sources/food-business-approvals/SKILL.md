---
name: food-business-approvals
description: Query the Agriculture and Food Board JVIS public register for registered and approved food or feed business operators.
---

# Food And Feed Business Operators (JVIS)

## Access

- Public application: `https://jvis.agri.ee/jvis/avalik.html`
- Food operator API: `POST https://jvis.agri.ee/jvis/api/avalik/toidukaitleja/otsing`
- Feed operator API: `POST https://jvis.agri.ee/jvis/api/avalik/soodakaitleja/otsing`
- No login is required, but API calls require cookies from the public application and the `XSRF-TOKEN` cookie echoed in the `X-XSRF-TOKEN` header.

## Retrieve

Use a cookie-aware client. First `GET` the public application, then send JSON to one of the search endpoints with the same cookies and XSRF header:

```json
{
  "filter": {"kaitlejaNimi": "Selver"},
  "sort": [
    {"field": "kaitlejaNimi", "direction": "ascending"},
    {"field": "tegevuskohaNimi", "direction": "ascending"}
  ],
  "page": {"number": 1, "size": 20}
}
```

Useful food filters are `kaitlejaNimi`, `kaitlejaKood`, `tegevuskohaNimi`, `tegevuskohaAadress`, `tunnusnumber`, `maakonnaEhak`, `onlyTunnustatud`, `pohiKaitlemisvaldkonnad`, and `kaitlemisvaldkonnad`. Start with one narrow text filter; an unfiltered query is large.

## Return

- The response is JSON with `total` and `data`.
- Preserve `kaitlejaNimi`, `kaitlejaIsikukoodRegkood`, `kaitlejaAadress`, `tegevuskohaNimi`, `tegevuskohaAadress`, `tunnusnumber`, and the activity/approval fields present in each record.
- Report the endpoint, filter, page number, page size, retrieval time, and `total`.

## Limits

- Search values and classifier codes are primarily Estonian.
- `onlyTunnustatud: true` limits results to approved establishments; false or omitted also includes notified operators.
- Treat personal identifiers and addresses as public-register data and return only fields relevant to the request.
- A direct API POST without the cookie/XSRF bootstrap returns an error and is not a valid availability check.

## Verify

- Require HTTP 200 and `application/json` from the POST.
- Require integer `total`, list `data`, and operator and location fields in returned rows.
