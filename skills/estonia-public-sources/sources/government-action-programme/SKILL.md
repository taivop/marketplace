---
name: government-action-programme
description: Retrieve Government Office action-programme records and monitoring dashboard outputs, including responsibilities, deadlines, and status views.
---

# Government Action Programme

## Use when
- You need official government action-programme commitments, responsibilities, and deadline tracking.
- You need the monitoring dashboard view used for programme execution transparency.

## Avoid when
- You need only long-term strategy plans (use Estonia 2035 / strategic docs skills).

## Inputs
- Programme period or government term.
- Policy chapter/topic.

## Outputs
- Task-level programme extract and dashboard status snapshot with source links.

## Access reality statement
- Access type: `UI copy-only` + `download files` (linked previous programme files).
- Verified on 2026-02-24.
- Page embeds PowerBI dashboards and linked historical programme documents.

## Primary endpoints
- Action programme page: https://www.valitsus.ee/valitsuse-eesmargid-ja-tegevused/valitsemise-alused/tegevusprogramm-0
- Embedded dashboard (page 1): https://app.powerbi.com/view?r=eyJrIjoiYzUxMTg3MWUtN2M4My00N2E5LWExMzItZWFhMzEzYmQzMmJhIiwidCI6IjhmZTA5OGQyLTQyOGQtNGJkNC05ODAzLTcxOTVmZTk2ZjBlMiIsImMiOjl9&pageName=06bb907844ed3bab3769&iframe=1&langcode=et
- Embedded dashboard (page 2): https://app.powerbi.com/view?r=eyJrIjoiYzUxMTg3MWUtN2M4My00N2E5LWExMzItZWFhMzEzYmQzMmJhIiwidCI6IjhmZTA5OGQyLTQyOGQtNGJkNC05ODAzLTcxOTVmZTk2ZjBlMiIsImMiOjl9&pageName=80b7f5658c06fa5ad0c1&iframe=1&langcode=et

## Retrieval workflow (reproducible)
1. Open action programme page and capture lead text (scope, monitoring description, confirmation date).
2. Extract task metadata visible on the page/dashboard (responsible body, deadline, completion state).
3. Record embedded dashboard URLs from iframe sources.
4. Collect linked historical programme files (including machine-readable links when present).
5. Return normalized task records and dashboard snapshots with page-level provenance.

## Request/query contract
- No public standalone API documentation for programme tasks on this page.
- Data is exposed via page content and PowerBI embeds.
- Treat dashboard extraction as UI-derived unless a stable export API is explicitly available during run.

## Output schema expectations
- `source_page_url`
- `programme_period`
- `task_title`
- `responsible_entity`
- `deadline`
- `status`
- `coalition_chapter`
- `dashboard_url`
- `notes`

## Limits and caveats
- Dashboard schema can change without URL changes.
- Some historical links may point to cloud storage and may expire/move.
- Content is primarily Estonian.

## Verification hooks
- Action programme page includes two embedded PowerBI iframes (`pageName=06bb...` and `pageName=80b...`).
- Page text states government confirmed updates and describes monthly monitoring.
- Page contains links to previous programme files, including a "töödeldaval kujul" link.
