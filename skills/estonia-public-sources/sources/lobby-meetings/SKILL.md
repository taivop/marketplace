---
name: lobby-meetings
description: Download quarterly XLSX disclosures of meetings between lobbyists and Estonia's prime minister or Government Office officials.
---

# Government Office Lobby Meetings

## Access

- Index: `https://www.riigikantselei.ee/asutus-uudised-ja-kontakt/lobitegevus/lobistidega-kohtumised`
- Public server-rendered HTML with quarterly XLSX files; no login is required.

## Retrieve

1. Fetch the index and select the required year/quarter accordion.
2. Extract the `.xlsx` link, resolving relative `/sites/default/files/documents/...` paths against the index URL.
3. Download and parse with a spreadsheet library.

Use the workbook's own headers. Typical fields identify the meeting date, official, lobbyist/person or organization, and subject. Preserve all sheets because revised files or explanatory tabs may accompany the records.

## Return

- Return one row per disclosed meeting with year, quarter, date, official, lobbyist/organization, subject, original workbook/sheet, source URL, and retrieval time.
- Preserve names and organization labels exactly as published.
- Deduplicate only exact repeated rows across revised quarter files, and retain the revision source.

## Limits

- The page covers the prime minister and Government Office; other public bodies publish their own disclosures.
- File naming dates do not always equal the covered quarter or revision date.
- Absence from a disclosure file is not evidence that no contact occurred.

## Verify

- Require the index to expose multiple year accordions and multiple `.xlsx` links.
- Require each workbook to begin with the ZIP signature `PK` and contain at least one nonempty worksheet with the expected meeting fields.
