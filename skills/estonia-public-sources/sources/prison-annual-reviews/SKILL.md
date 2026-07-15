---
name: prison-annual-reviews
description: Retrieve Vanglateenistus annual visual reviews and public Fabric dashboards for current prison and probation indicators.
---

# Prison Reviews and Operational Statistics

## Access

- Annual visual reviews: `https://vanglateenistus.ee/meist/uudised-ja-arvud/aasta-ulevaated`
- Current numeric overview: `https://vanglateenistus.ee/meist/uudised-ja-arvud/paevakohane-arvuline-ulevaade`
- Public dashboard: `https://app.fabric.microsoft.com/view?r=eyJrIjoiNTg0YmZmMjAtN2FhZC00MDI3LWE2NTUtMTZiM2IwYTVlNzUzIiwidCI6ImY2MzQyZDcwLWRhYzEtNDYxNC04ZTFhLTQ3YjkxYzE2YjhkZiIsImMiOjl9`

## Retrieve

The annual page contains accordion sections by year. Recent reviews are sequences of infographic images under `/sites/default/files/...`; older sections may contain HTML tables or links to year-specific Power BI reports. Treat image text extraction as OCR and retain the image URL for every value.

The current overview embeds at least two Fabric reports, including operational indicators and prison-service events. Set and record every active dashboard filter before copying or exporting values. Capture the page's `Viimati uuendatud` date with the extract.

## Return

- Preserve source type (`annual_image`, `annual_dashboard`, or `current_dashboard`), year/date, metric, value, unit, population/scope, active filters, image/report URL, page URL, and retrieval time.
- Keep prisoner, detainee, probation, staffing, incident, and activity measures distinct.

## Limits

- No documented public REST contract is exposed. Dashboard and image schemas can change.
- Recent annual reviews are images rather than machine-readable tables; OCR must be checked against the source image.
- Dashboard definitions may differ from annual-review definitions. Do not merge series without confirming comparability.
- `https://www.vangla.ee/et/statistika` is obsolete and redirects to the current site.

## Verify

- Require the annual page to contain multiple year accordions and `/sites/default/files/` review images or year-specific dashboard links.
- Require the current page to contain public Fabric iframe URLs and a `Viimati uuendatud` date. Reject a blank dashboard shell as retrieved data.
