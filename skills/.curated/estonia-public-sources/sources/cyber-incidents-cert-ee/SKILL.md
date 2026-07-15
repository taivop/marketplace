---
name: cyber-incidents-cert-ee
description: Retrieve RIA's monthly, quarterly, and annual public cyber-situation reports for Estonian incident counts, trends, attack types, and significant events.
---

# RIA Cyber-Situation Reports

## Access

- Publication index: `https://www.ria.ee/en/cyber-security/cyberspace-analysis-and-prevention/situation-cyberspace`
- Public server-rendered HTML linking report pages and PDFs; no login or JavaScript is required.

## Retrieve

The index groups publications into:

- monthly summaries from 2023 onward
- quarterly assessments through 2023
- annual `Cyber Security in Estonia` reports

Select the period first. Resolve relative monthly report and `/sites/default/files/documents/...pdf` links against `https://www.ria.ee`. Newer monthly entries may be HTML articles while older entries are PDFs.

Extract incident totals, handled/impactful incident distinctions, phishing/malware/DDoS and availability categories, significant events, comparison period, and any revised definitions. Use the annual reports for yearly totals and methodology; use monthly reports for timely operational context.

## Return

- Preserve report period, publication date, metric label, count/rate, comparison value, definition, source URL, page/section, and retrieval time.
- Keep observed incidents separate from reports received, incidents handled, vulnerabilities, and automated monitoring events.
- Quote category labels exactly before adding normalized categories.

## Limits

- Public reports are curated aggregates, not the confidential CERT-EE incident database.
- Publication format varies between HTML and PDF across years.
- The former incident-handling landing page describes CERT-EE procedures but does not itself provide incident records.

## Verify

- Require the index to expose multiple monthly years, monthly report links, quarterly assessments, and annual cyber-security reports.
- Require selected PDF files to begin `%PDF-`; for HTML reports, require the requested month/year and incident-related content.
