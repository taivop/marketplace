---
name: medicines-agency-statistics
description: Download State Agency of Medicines statistical yearbook PDFs for medicines use, market, pharmacy, and regulatory activity indicators.
---

# Medicines Agency Statistical Yearbooks

## Use when
- You need annual medicines, pharmacy, clinical-trial, or agency activity statistics.
- You need tables and definitions from a specific yearbook edition.

## Avoid when
- You need individual medicinal-product records; use `medicines-register`.

## Endpoint
- Yearbook index: https://www.ravimiamet.ee/en/statistics/statistics/statistical-yearbooks

## Workflow
1. Parse PDF anchors from the yearbook index and extract the four-digit edition year from each label.
2. Select the requested edition, resolve its relative URL against the index, and download the PDF.
3. Extract tables with their section heading, units, footnotes, and edition year.
4. Compare editions only after checking whether labels or definitions changed.

## Access reality
- Public HTML index and direct PDFs, verified 2026-07-14.
- The index listed ten PDF publications, including annual editions from 2017 through 2025 and other statistical books.

## Output schema expectations
- Keep edition year, table/section title, original row and column labels, unit, value, footnotes, PDF URL, and retrieval timestamp.

## Limits and caveats
- The annual sequence has gaps on the English index.
- PDFs mix narrative and tables; do not treat every number as a comparable indicator.

## Verification hooks
- Require a `.pdf` link with a yearbook label and four-digit year.
- Require `application/pdf` and `%PDF-` before extraction.
