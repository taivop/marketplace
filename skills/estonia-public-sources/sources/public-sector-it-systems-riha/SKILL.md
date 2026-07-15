---
name: public-sector-it-systems-riha
description: Query RIHA's public JSON API for Estonian information systems, owners, purposes, lifecycle and X-Road status, security metadata, documents, and data files.
---

# Public-Sector IT Systems (RIHA)

## Access

- Frontend: `https://www.riha.ee/`
- Systems API: `GET https://www.riha.ee/api/v1/systems`
- Classifiers: `GET https://www.riha.ee/api/v1/environment/classifiers`
- Public JSON; no login is required for these endpoints.

## Retrieve

Use `page` (zero-based) and `size` on `/api/v1/systems`, for example:

`https://www.riha.ee/api/v1/systems?page=0&size=100`

The response contains `totalElements`, `content`, `size`, `page`, and `totalPages`. Page until `page + 1 == totalPages` when a full snapshot is required.

Each row has a numeric `id`, request/approval metadata, and `details`. Important `details` fields include:

- `name`, `uuid`, `short_name`, `purpose`, and `homepage`
- `owner.code` and `owner.name`
- `meta.system_status`, `meta.x_road_status`, creation/update timestamps, and development status
- `topics`, `security`, `documents`, `data_files`, `stored_data`, and `legislations`

Fetch `/api/v1/environment/classifiers` to map lifecycle, X-Road, security, document, relation, and legislation codes to Estonian labels.

## Return

- Preserve RIHA `id`, UUID, short name, owner code/name, statuses with timestamps, purpose, topics, security metadata, and source URL.
- Keep documents, data files, stored data, and legislation as arrays.
- Include page parameters, `totalElements`, and retrieval time.

## Limits

- RIHA includes finished, establishing, private-owner, and legacy systems; filter deliberately rather than assuming every row is an active state system.
- Registry metadata may be stale; preserve `meta.update_timestamp`.
- `file://<uuid>` document links are RIHA-managed identifiers, not local filesystem paths.

## Verify

- Require HTTP 200 JSON with nonempty `content`, integer paging metadata, and nested `details.name`, `details.owner`, and `details.meta` fields.
- Reject the Angular HTML shell or the legacy `riha.eesti.ee/riha/main/infSystem/search` redirect as data.
