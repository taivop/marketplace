---
name: tallinn-council-documents
description: Query Tallinn's TEELE JSON API for adopted council legal acts, council drafts, and document details.
---

# Tallinn TEELE Documents

Use this source for Tallinn City Council regulations, resolutions, drafts, and proceeding metadata. TEELE supersedes the broken `oigusaktid.tallinn.ee` wrapper for these records.

## API

Base: `https://teele.tallinn.ee/api`

- System settings: `GET /systemSettings`
- Search: `GET /documents`
- Detail: `GET /documents/{id}?lang=EE`
- Browser detail: `https://teele.tallinn.ee/documents/{id}/view`

Read `COUNCILUNIT` from `/systemSettings` rather than hard-coding the current unit ID. Encode arrays as repeated query keys.

## Search contracts

Common pagination: `page=1&pageSize=10&lang=EE`.

Adopted council acts:

- `documentTypes=RESOLUTION&documentTypes=REGULATION`
- `publisherUnitId={COUNCILUNIT}`
- `status=ACCEPTED`
- `sortColumn=publishedAt&sortDirection=desc`

Council drafts in active council proceedings:

- same document types and publisher unit
- `statuses=INCOUNCILPROCEEDING&statuses=WAITINGFORCOUNCILMEETING`
- `sortColumn=documentSubmission.acceptedAt&sortDirection=asc`

## Output and limits

Keep `id`, `title`, document type/status, `number`, `draftNumber`, `publishedAt`, `documentSubmission.acceptedAt`, submitters, publisher, and access-restriction flags. Fetch detail for enforcement/publication metadata and use the browser detail only for full rendered content or attachments.

Respect `pageCount`; do not treat restricted documents as accessible merely because they appear in search results.

## Verification

A valid search response contains `page`, `pageCount`, `rowCount`, and `results`; each result has an integer `id`, title, document type, and status.
