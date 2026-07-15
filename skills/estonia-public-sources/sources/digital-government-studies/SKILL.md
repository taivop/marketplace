---
name: digital-government-studies
description: Retrieve RIA's categorized studies, analyses, cryptography reviews, cyber-security reports, and institutional overviews from its embedded publication tables.
---

# RIA Studies and Analyses

## Access

- Index: `https://www.ria.ee/en/authority-news-and-contact/news-media-contact/studies-analyses-overviews`
- Public server-rendered HTML with embedded JSON tables and direct file links.

## Retrieve

Fetch the page and parse each `<script type="application/json" id="datatable-...">` block. Each table row contains rendered HTML for:

1. document/reference name and URL
2. entry date
3. download/view URL

Parse those HTML fragments with an HTML parser, not a regular expression. Keep the table's surrounding heading as the category. Categories include studies/analyses, cryptographic algorithms, cyber-security annual reports, and RIA overviews/yearbooks.

If an embedded file URL uses the staging host `ria.prelive.vportal.ee`, replace only that host with `www.ria.ee` and keep the path unchanged. The published staging-host URLs return 403 while the corresponding production-host paths serve the files.

The `/en/download_all_files/<id>` links are category-level browser helpers. Prefer the direct file URL from each JSON row when fetching one publication.

## Return

- Return title, category, entry date, file/reference type, direct URL, file size when shown, language, and retrieval time.
- Preserve web-publication and PDF variants as separate records when both exist.
- Extract report contents only after selecting the relevant publication.

## Limits

- This is a publication catalog, not a metric API; data inside reports requires document extraction.
- Entry date can differ from the report's coverage year.
- Some categories overlap the dedicated cyber-situation recipe; use that recipe when the question is specifically about incident trends.

## Verify

- Require multiple datatable JSON blocks, parseable rows, dates, and direct RIA PDF/reference URLs after the documented staging-host normalization.
- Require selected PDF files to begin `%PDF-`; reject navigation and category download icons as publications.
