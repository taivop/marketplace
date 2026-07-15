---
name: communicable-disease-bulletins
description: Retrieve Estonia's monthly communicable-disease surveillance bulletins and their disease, outbreak, age, and regional indicators from Health Board PDFs.
---

# Communicable Disease Bulletins

## Access

- Index: `https://www.terviseamet.ee/en/communicable-diseases/statistics/communicable-disease-bulletins`
- Public server-rendered HTML linking monthly PDF bulletins; no login or JavaScript is required.

## Retrieve

1. Fetch the index and extract links under the required year.
2. Resolve relative `/sites/default/files/documents/...pdf` paths against `https://www.terviseamet.ee`.
3. Download the PDFs whose visible labels match the requested months. Current English filenames use `EEpiR <month> <year>.pdf`.
4. Extract tables with a PDF-aware tool; use OCR only for pages that have no text layer.

The page also links the TAI PxWeb morbidity database for longer time series. Use `health-statistics` when that structured database answers the question without bulletin-specific commentary.

## Return

- Preserve bulletin month, publication URL, disease name, geography, age group, count/rate, unit, footnotes, and retrieval time.
- Keep provisional values and case-definition notes attached to their table.
- Cite the exact PDF page for extracted values.

## Limits

- The index is a publication archive, not an API; file paths change each month.
- Bulletin tables and narrative may mix Estonian and English disease labels.
- Do not combine counts across tables until their periods, geographies, and definitions match.

## Verify

- Require HTTP 200 `text/html` with multiple year sections and multiple `.pdf` bulletin links.
- Require each selected file to return a PDF (`%PDF-` signature). Reject the index page itself as disease data.
