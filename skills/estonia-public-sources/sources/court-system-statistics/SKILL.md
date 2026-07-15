---
name: court-system-statistics
description: Locate Estonia's official court caseload and procedural statistics in the public court-system Fabric reports.
---

# Court System Statistics

## Access

- Index: `https://www.kohus.ee/eesti-kohtud/kohtute-menetlusstatistika`
- Main proceedings report: `https://app.fabric.microsoft.com/view?r=eyJrIjoiOWVjNWMxY2ItMDgwMS00NzhiLWIzOTctMDM5NTFlNjczNGE4IiwidCI6ImY2MzQyZDcwLWRhYzEtNDYxNC04ZTFhLTQ3YjkxYzE2YjhkZiIsImMiOjl9`
- Payment-order report: `https://app.fabric.microsoft.com/view?r=eyJrIjoiOGQ5MmY3YWItZjM0Zi00OWNlLThjZWYtZDIzN2IyY2YwNmYwIiwidCI6ImY2MzQyZDcwLWRhYzEtNDYxNC04ZTFhLTQ3YjkxYzE2YjhkZiIsImMiOjl9`

## Retrieve

Use the index to discover the current public report IDs. In Fabric, set the year, court, court level, and proceeding type before copying or exporting a visual. Record every active filter with the extracted values.

Use `https://www.riigikohus.ee/et/riigikohus/statistika` for Supreme Court-specific totals and the index's historical link for 1997-2014 series. Court yearbooks are narrative context, not a substitute for the statistical report.

## Return

- Preserve metric name, value, unit, period, court, court level, proceeding type, report URL, active filters, and retrieval time.
- Keep incoming cases, resolved cases, pending cases, duration, and clearance indicators distinct.
- Label values copied from a visual as dashboard extracts, not API records.

## Limits

- No documented public REST contract is exposed for these reports.
- Fabric report IDs and visual schemas can change. Rediscover them from the index rather than relying only on a saved ID.
- Historical and current series may use different court structures or definitions.

## Verify

- Require the index to link both public Fabric reports and the Supreme Court statistics page.
- Reject a blank Fabric shell as evidence that data was retrieved; require visible values or a successful export with recorded filters.
