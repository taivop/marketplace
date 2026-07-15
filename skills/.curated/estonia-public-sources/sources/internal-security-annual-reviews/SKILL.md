---
name: internal-security-annual-reviews
description: Retrieve Estonian Internal Security Service (KAPO) annual-review PDFs from its public year-by-year index.
---

# KAPO Annual Reviews

Use this source for KAPO's annual internal-security reviews from 1998 onward.

## Endpoints

- Public index: `https://kapo.ee/et/aastaraamatud/`
- Current direct-file example: `https://kapo.ee/sites/default/files/content_page_attachments/aastaraamat-2025-2026.pdf`

## Workflow

1. Open the index with a browser or web-page reader. Plain HTTP clients can receive `403` on the index even though the public page renders normally.
2. Select the required year and copy the linked PDF URL. Do not construct filenames from years: suffixes and year formats vary.
3. Download the direct PDF with an ordinary HTTP client and extract only the requested sections.
4. Keep the displayed review year, direct PDF URL, language, retrieval time, and page references.

The files are narrative reports, not row-level incident data. Do not infer complete operational statistics from omitted or selectively reported figures.

## Verification

- The public index lists annual reviews from 1998 through the current edition.
- A valid direct file returns `application/pdf` and starts with `%PDF-`.
