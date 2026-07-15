---
name: healthcare-professionals-register
description: Query MEDRE's public JSON API for registered healthcare professionals and download its occupation, speciality, and pharmacist open-data files.
---

# Healthcare Professionals Register (MEDRE)

## Access

- Frontend: `https://medre.tehik.ee/home`
- API base: `https://medre.tehik.ee/api-common`
- Public JSON search and XML downloads; no login is required for the endpoints below.

## Retrieve

POST JSON to `/public/persons/filter`. Paging fields are `page` (zero-based), `size`, and optional `sort`. For an unfiltered page:

```json
{"page": 0, "size": 10}
```

The response has `content`, `page`, `size`, `totalElements`, and `totalPages`. Each person includes `id`, `firstName`, `lastName`, `occupationCodes`, `specialities`, and `specialistCodes`. Read occupation and speciality IDs from:

- `GET /public/persons/occupations`
- `GET /public/persons/specialities`

Bulk/classifier downloads:

- `/public/persons/pharmacists/open-data` -> `od_apteekrid.xml`
- `/public/persons/occupations/open-data` -> `od_kutsed.xml`
- `/public/persons/specialities/open-data` -> `od_erialad.xml`

The frontend's public search form is authoritative for additional filter names; preserve the exact POST payload used.

## Return

- Preserve the public person ID, name, registration code, occupation and speciality codes/names, registration dates, source URL, query, and retrieval time.
- Keep multiple occupations and specialities as arrays rather than flattening them into a single label.
- Report `totalElements` and all paging parameters.

## Limits

- The API exposes professional registration, not employment history or private personnel records.
- Unfiltered search is paginated; do not mistake one page for the complete register.
- The dedicated bulk person file currently covers pharmacists; other professionals are available through paged JSON search.

## Verify

- Require `/public/persons/filter` to return JSON with nonempty `content` for `{"page":0,"size":2}` and the documented person fields.
- Require classifier endpoints to return nonempty JSON or XML. Reject the single-page frontend shell as register data.
