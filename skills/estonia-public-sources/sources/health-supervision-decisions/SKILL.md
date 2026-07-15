---
name: health-supervision-decisions
description: Retrieve published Health Board precepts and annual supervision result files for regulated entities, health services, environmental health, and product safety.
---

# Health Supervision Decisions

## Access

- Precepts: `https://www.terviseamet.ee/ettekirjutused`
- Supervision results: `https://www.terviseamet.ee/jarelevalve`
- Public server-rendered HTML linking PDF decisions, PDF reports, and some XLS/XLSX result tables.

## Retrieve

Use the precepts page for entity-level enforcement documents. Extract links grouped by year; current filenames usually contain `Ettekirjutus`, the subject, and decision date.

Use the supervision page for aggregate annual results. Select the subject heading first because that page combines health and social services, food, beauty/accommodation services, product safety, drinking water, bathing water, pools, and physical hazards.

Resolve relative `/sites/default/files/documents/...` paths against `https://www.terviseamet.ee`, then download the original file. Parse PDF decisions as documents and XLS/XLSX files as spreadsheets.

## Return

- For a precept, preserve subject, decision date, legal basis, operative requirements, deadlines, reference identifiers, source file, and page numbers.
- For aggregate supervision results, preserve reporting year, inspected population, sample/inspection counts, noncompliance measures, units, and topic.
- Keep filename-derived metadata provisional until confirmed inside the document.

## Limits

- The pages do not provide a structured cross-year API or complete entity index.
- Older precepts are linked through Estonia's web archive and may need separate retrieval.
- `jarelevalve` is a mixed publication library, not a list of individual enforcement decisions.

## Verify

- Require the precepts page to contain multiple year headings and multiple PDF links whose paths or labels include `Ettekirjutus`.
- Require the supervision page to expose multiple topic headings and downloadable PDF/XLS/XLSX files. Require downloaded PDFs to begin `%PDF-`.
