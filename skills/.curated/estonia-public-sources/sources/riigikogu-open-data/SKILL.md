---
name: riigikogu-open-data
description: Query the Riigikogu open data API for draft laws, votes, members, agendas, stenograms, and legislative activity.
---

# Riigikogu Open Data API

## Use when
- You need draft laws, parliamentary votes, members, plenary agendas, or stenograms.
- You need machine-readable legislative activity from the Riigikogu API.

## Avoid when
- You need election outcomes (use election archive skill).

## Primary endpoints
- OpenAPI contract: https://api.riigikogu.ee/v3/api-docs
- Draft search: `https://api.riigikogu.ee/api/volumes/drafts?initiatedStartDate=2026-01-01&initiatedEndDate=2026-01-31&lang=EN&page=0&size=20`
- Draft detail: `https://api.riigikogu.ee/api/volumes/drafts/{uuid}?lang=EN&querySteno=false`
- Votes: `https://api.riigikogu.ee/api/votings?startDate=2025-01-01&endDate=2025-01-31&lang=EN`
- Plenary agendas: `https://api.riigikogu.ee/api/agenda/plenary?startDate=2025-01-01&endDate=2025-01-31&lang=EN`
- Stenograms: `https://api.riigikogu.ee/api/steno/verbatims?startDate=2025-01-01&endDate=2025-01-31`
- Public calendar fallback: https://www.riigikogu.ee/tegevus/kalender/
- Public stenogram fallback: https://www.riigikogu.ee/tegevus/stenogrammid/

## Workflow
1. Choose the endpoint family from the OpenAPI contract.
2. Query a bounded date range using ISO dates. For a known draft, use `reference`, `mark`, or `title` instead.
3. Preserve UUIDs, draft marks, stages, timestamps, sitting metadata, speaker names, and vote values as returned.
4. Follow UUID detail, document, or file endpoints only when the requested record needs them.
5. Return the exact endpoint and query parameters with the extracted records.

## Access reality
- Public access type: API or structured endpoint access.
- Verified 2026-07-14 against OpenAPI version `2.21.8`.
- The January 2025 plenary-agenda example returns `weekStartDate`, `weekEndDate`, `title`, and a non-empty `sittings` array.
- The January 2026 draft example returns a HAL page under `_embedded.content`; each result has a UUID, title, draft mark, type, stage, status, and initiation date.
- The service may return HTTP 429 for rapid consecutive requests; query serially and back off before retrying.

## Request contract
- `startDate` and `endDate` use `yyyy-MM-dd`.
- Both dates are required for `/api/votings` and `/api/steno/verbatims`; they are optional for `/api/agenda/plenary`.
- Draft search accepts `title`, `reference`, `mark`, `membership`, `draftTypeCode`, `proceedingStatus`, `activeDraftStage`, initiator or committee UUIDs, initiation/amendment date bounds, `page`, `size`, and `sort`.
- `draftTypeCode` accepts `UA`, `DE`, `PE`, `AE`, `TK`, `SE`, or `OE`. Use the OpenAPI classifiers rather than translating these values.
- `lang` accepts `ET`, `RU`, or `EN` and defaults to `ET` where supported.
- Stenogram `type` accepts `IS` (sitting), `IT` (question time), or `IK` (committee sitting).
- Responses are JSON. No authentication is documented for these endpoints.

## Output schema expectations
- Keep the record UUID, draft mark/type/stage/status, date/time, sitting or agenda identifiers, titles/topics, member or speaker identifiers, and vote/speech fields present in the selected response.
- Preserve original field names and classifier values.

## Limits and caveats
- Use the public calendar or stenogram pages only when the API omits content needed by the user.
- Do not infer that a scheduled agenda item was completed; join to votes, stenograms, or documents when outcomes matter.

## Verification hooks
- Confirm `Content-Type: application/json` and parse the response before reporting success.
- For the agenda example, require each sitting to contain `uuid`, `sittingDateTime`, and `agendaItems`.
- Confirm returned dates overlap the requested window.
- Treat HTTP 429 as rate limiting, not evidence that the endpoint is unavailable.
