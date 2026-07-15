---
name: construction-register
description: Query Estonia's Construction Register (EHR) public JSON endpoints for building search results and detailed building records.
---

# Construction Register (EHR)

## Access

- Search API: `POST https://livekluster.ehr.ee/api/building/v2/buildingSearchPageable`
- Detail API: `GET https://livekluster.ehr.ee/api/building/v3/buildingData`
- Public search UI: `https://livekluster.ehr.ee/ui/ehr/v1/detailsearch/BUILDINGS_SEARCH`
- Response: JSON; no login is required for these two API calls.

## Search

Send JSON with at least one useful filter plus one-based pagination:

```json
{
  "buildingName": "raekoda",
  "page": 1,
  "pageSize": 10
}
```

Supported public UI filters map directly to these payload fields:

- `buildingLocation`: address, EHR code, or cadastral identifier
- `buildingName`
- `buildingType`: array containing `H` (building) or `R` (structure)
- `buildingStates`: array of classifier codes
- `purposeOfUse` and `ocurringPurposeOfUse`: arrays of purpose IDs
- `lastRegisteredDocumentType`, `ownershipType`, `heritage`
- `firstUseDate`: object with optional `from` and `to` year strings
- `firstUseMissing`: boolean
- `page`, `pageSize`, optional `sortField`, `sortDir`

The response contains `page`, `pageSize`, `total`, and `data`. Keep each result's `ehrCode`, `buildingId`, addresses, name, type, state, purpose, first-use year, dimensions, ownership type, latest document metadata, and geometry.

## Detail

After selecting an `ehrCode`, request:

```text
GET https://livekluster.ehr.ee/api/building/v3/buildingData?ehr_code=<EHR_CODE>&json=true
```

The detail response is nested under `ehitis` and includes basic data, addresses, cadastral units, geometry, uses, dimensions, technical systems, and energy labels when present.

## Limits

- Owner search uses an authenticated endpoint and is not part of this public contract.
- Public access to some attached documents is temporarily restricted; do not promise document-file access from the building APIs.
- Geometry coordinates are in the register's source coordinate system; do not label them WGS84 without conversion.

## Verify

Require a numeric `total`, a non-empty `data` array, and `ehrCode`, `buildingId`, `buildingAddress`, and `buildingState` in a search result. For detail calls, require `ehitis.ehitiseAndmed.ehrKood` to equal the requested code.
