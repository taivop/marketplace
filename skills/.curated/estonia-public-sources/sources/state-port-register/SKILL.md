---
name: state-port-register
description: Query Estonia's public State Port Register API for active ports, addresses, services, water bodies, contacts, and detailed port records.
---

# State Port Register

## Access

- Frontend: `https://www.sadamaregister.ee/`
- Settings: `GET https://www.sadamaregister.ee/settings`
- Current public API base from settings: `https://sadamaregister.ee/api`
- Public JSON; no login is required for the endpoints below.

## Retrieve

1. Fetch `/settings` rather than hard-coding the API host indefinitely.
2. Fetch `<ApiBaseUrl>/ports/public-active` for all active public ports.
3. Select by `publicId`, name, address, water-body code, function, foreign-vessel support, or additional service.
4. Fetch `<ApiBaseUrl>/ports/<publicId>/public-details` for the full public record.

Supporting endpoints include `/ports/reservoirs` and `/ports/additional-service-types`. Public file links use `/ports/<publicId>/public-files/<fileId>` as exposed by a detail record.

## Return

- List records include `publicId`, `name`, `address`, phone numbers, email, water-body type/name, port function, foreign-vessel flag, and additional services.
- Detail records can add manager, harbour master, technical dimensions, quays, served vessels, services/providers, water and land areas, navigation aids, documents, pricing, and map location.
- Preserve classifier codes alongside translated labels, plus source URL and retrieval time.

## Limits

- Authentication is needed to amend register data, not to read these public endpoints.
- File endpoints may return temporary links; cite the port detail and record file metadata as well.
- Classifier names depend on the selected register language.

## Verify

- Require `/settings` JSON with `ApiBaseUrl`.
- Require `/ports/public-active` to return a non-empty JSON list whose rows contain `publicId`, `name`, `address`, and service/water-body fields.
