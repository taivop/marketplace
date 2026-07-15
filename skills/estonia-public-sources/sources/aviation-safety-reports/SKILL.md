---
name: aviation-safety-reports
description: Fetch the Transport Administration's historical ANS and ATM safety oversight reports for 2009-2015.
---

# Aviation Safety Reports

## Access

- Index: `https://www.transpordiamet.ee/en/aviation-and-aviation-safety/aviation-safety/reports`
- Method: `GET`
- Files: public PDFs linked under `ANS and ATM Annual Safety Oversight Reports`.

## Retrieve

1. Fetch the index and collect PDF links inside the ANS/ATM report section.
2. Resolve relative links against the index URL and download the requested editions.
3. Extract claims with the report title, covered year, page, and PDF URL.

The index currently exposes reports for 2015, 2014, 2013, 2012, 2011, and 2009-2010. Discover links from the index instead of hard-coding file paths.

## Limits

- This is a historical oversight archive, not an aviation-occurrence dataset or current safety dashboard.
- Coverage stops at 2015 and is not annual after that date.
- Tables and charts may require PDF layout-aware extraction.

## Verify

Require the `ANS and ATM Annual Safety Oversight Reports` heading, at least six year-labelled PDF links, and `%PDF-` at the start of every downloaded file.
