---
name: environmental-permit-decisions
description: Query KOTKAS public server-side forms for environmental permits, applications, proceedings, documents, and permit details.
---

# Environmental Permits (KOTKAS)

## Access

- Permits: `https://kotkas.envir.ee/permits/public_index`
- Applications: `https://kotkas.envir.ee/permits/public_application_index`
- Documents: `https://kotkas.envir.ee/permits/public_document_index`
- Public HTML forms; no login is required.

## Retrieve

POST form-encoded data with `search=1` to the relevant endpoint. Permit filters include `permit_nr`, `owner_name`, `object_name`, `permit_type`, `permit_status`, issue/validity date ranges, `well_number`, and location/activity fields. Application filters include `applicant`, `application_type`, `permit_nr`, `proceeding_nr`, `proceeding_public_status`, and registration dates. Document filters include `document_number`, `external_number`, `document_type`, `title`, `keyword`, sender/recipient, publication level, and registration dates.

Permit results are server-rendered rows with links to `/permits/public_view?...&permit_id={id}`. Page with `qs` in increments of 20 while preserving the filters. The result footer states the current page and total record count. On a permit, use the registration/detail, documents, and assignments tabs rather than treating the list row as complete.

## Return

- Preserve permit/application/proceeding/document identifiers, holder or applicant, object and location, type, status, relevant dates, detail/document URLs, query, total, and retrieval time.
- Keep application, proceeding, permit, and document records as separate record types.

## Limits

- This is HTML extraction, not a public JSON API. Estonian labels and form fields may change.
- A permit number can appear in several lifecycle/version rows; do not deduplicate without retaining internal `permit_id` and status dates.
- Some files or fields may be restricted even when the public register row is visible.

## Verify

- Require a focused POST search to return a positive `Kokku ... kirjet` count and `/permits/public_view?...permit_id=` links.
- Require a selected detail page to expose status plus registration, documents, and assignments tabs.
