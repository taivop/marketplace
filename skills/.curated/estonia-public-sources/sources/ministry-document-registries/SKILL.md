---
name: ministry-document-registries
description: Search the RIK-hosted public document-register network for ministry, agency, court, prosecution, prison, and other administrative records.
---

# Public Document Registers (ADR)

## Access

- Agency index: `https://adr.rik.ee/`
- Each agency has a path prefix such as `jm`, `ram`, `som`, `riigikantselei`, `ria`, or `transpordiamet`.
- Public server-rendered HTML; no login or JavaScript is required.

## Retrieve

1. Fetch the agency index and choose the exact organization path.
2. For a keyword search, POST form data to `https://adr.rik.ee/<agency>/kiirotsing`:

```text
input=riigieelarve&pageNumber=1
```

3. For a fielded search, POST to `/<agency>/otsing`. Useful fields include `title`, `regDateBegin`, `regDateEnd`, repeated `documentTypes`, `party`, `senderRegNr`, `accessRestriction` (`Avalik` or `AK`), and `pageNumber`.

The form requires at least one search field. Dates use the format shown by the selected agency form. Document-type numeric values differ by agency, so read them from that agency's `/otsing` HTML rather than copying values across organizations.

## Return

- Result rows expose reference, registration date, title, document type, other parties, and a stable `/<agency>/dokument/<id>` detail link.
- Preserve the agency, query fields, page, access status, source URL, and retrieval time.
- Follow detail links for public attachments only when needed; restricted (`AK`) records may expose metadata without full text.

## Limits

- Quick search may cap output and ask for a narrower query; use fielded search for precision.
- Page URLs after a POST rely on the search state held by the server. Preserve the original POST fields when paging.
- The index includes historical organization names and aliases. Report the register label actually used.

## Verify

- Require the agency index to contain multiple `avalik dokumendiregister` links.
- Require search results to contain the expected five table headings and at least one `/<agency>/dokument/<id>` link. Reject an empty form or homepage as data.
