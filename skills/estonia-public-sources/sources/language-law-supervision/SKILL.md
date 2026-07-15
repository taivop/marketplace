---
name: language-law-supervision
description: Retrieve Keeleamet and historical Language Inspectorate annual activity reports from the page's embedded document-table JSON.
---

# Language-Law Supervision Reports

## Access

- Report index: `https://www.keeleamet.ee/keeleameti-tegevused-ja-eesmargid/keeleseaduse-ja-teiste-keeleoskust-ja-keelekasutust-3`
- Public HTML with embedded JSON and linked PDFs; no login is required.

## Retrieve

Find the `script type="application/json"` whose ID starts with `datatable-` and does not end in `-options`. Parse its row arrays. The first column contains report title, file size/type, and PDF link; the second contains an ISO timestamp and displayed insertion date; the third repeats the download link.

Resolve escaped relative links such as `\/sites\/default\/files\/documents\/...pdf` against `https://www.keeleamet.ee`. Derive the report year from the title, not the insertion date. Records before the agency rename use `Keeleinspektsioon` rather than `Keeleamet`.

## Return

- Preserve report title/year, insertion timestamp, institution name, PDF URL, file size when stated, page URL, and retrieval time.
- Extract supervision counts or findings only from the report itself and retain table/page references.

## Limits

- This source is an annual report archive, not case-level supervision data.
- The datatable ID is generated and changes when the page is rebuilt; discover it by prefix and content.
- Historical filenames contain spelling and encoding variations.

## Verify

- Require a non-options `datatable-` JSON script with multiple report rows and PDF paths.
- Require the newest linked report to return a PDF beginning with `%PDF-`; reject navigation links as report files.
