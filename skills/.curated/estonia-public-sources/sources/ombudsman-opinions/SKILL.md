---
name: ombudsman-opinions
description: Retrieve Chancellor of Justice annual-review sites and historical annual-report PDFs from the official year index.
---

# Chancellor of Justice Annual Reports

## Access

- English index: `https://www.oiguskantsler.ee/en/opinions-and-initiatives/annual-reports`
- Recent report sites: `https://www.oiguskantsler.ee/annual-report-{year}/`
- Public HTML and PDFs; no login is required.

## Retrieve

Parse the annual-report cards from the index. Recent years link to standalone report sites; older years link directly to PDFs. On a recent report site, follow topic/chapter navigation for HTML or fetch `overview.pdf` for the complete report snapshot.

Use the site's `?q=` search only within the selected annual report. For individual current opinions and initiatives, use the site's separate search rather than treating annual-report chapters as case-level opinion records.

## Return

- Preserve reporting period, title, chapter/topic, section URL, PDF URL when available, source index, and retrieval time.
- Attribute findings and recommendations to the Chancellor and preserve links to cited decisions or legal acts.

## Limits

- This recipe covers annual reporting. It does not provide a structured API for every opinion or initiative.
- Recent reports are separate static sites; paths and chapter structure differ by year.
- Annual reports summarize work during a period and may not contain the latest position on a topic.

## Verify

- Require the index to link several `/annual-report-{year}/` sites and historical PDF files.
- Require the newest report site to identify its reporting period and return a valid `overview.pdf` beginning with `%PDF-`.
