---
name: state-audit-reports
description: Retrieve National Audit Office audit records, topics, dates, findings, recommendations, responses, and linked report files.
---

# State Audit Reports

## Access

- English audit index: `https://www.riigikontroll.ee/en/audits`
- Estonian audit index: `https://www.riigikontroll.ee/auditid`
- Public server-rendered HTML and files; no login is required.

## Retrieve

Parse records only from the index's audit result list. Each card links to an audit detail page and includes report type, topic tags, title, teaser, and date. Use `?page=N` for later result pages and the visible facets for report type/topic selection.

On the detail page, extract title, teaser, report type, topic tags, publication information, body findings, recommendations, audited institutions' responses, and links under the report/sidebar fields. Resolve `/sites/default/files/...` links against the host and verify each file type before parsing.

## Return

- Preserve title, report type, topics, publication date, teaser, detail URL, report/summary file URLs, audited institutions, findings, recommendations, responses, page/query, and retrieval time.
- Keep the National Audit Office's finding, recommendation, and the audited body's response as separate attributed fields.

## Limits

- The index mixes audit reports, annual reports to Parliament, consolidated-account evaluations, and other report types. Retain the type.
- Some English pages provide only a summary file while the complete report is available in Estonian.
- Search result ordering and facet URLs can change; do not infer completeness from the first page.

## Verify

- Require the index to contain multiple `node--type-auditid` result cards with type, title, date, and detail links.
- Require a selected detail to expose its report type and at least one substantive body field or linked PDF; verify PDF signatures before extraction.
