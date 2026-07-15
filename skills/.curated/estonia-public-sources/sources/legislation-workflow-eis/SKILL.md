---
name: legislation-workflow-eis
description: Read draft legislation, coordination, submission, and public-consultation listings from Estonia's EIS application.
---

# Draft Legislation And Consultations (EIS)

## Access

- Current listings: `https://eelnoud.valitsus.ee/main/mount/share/home`
- Legacy OSALE URLs redirect to this EIS application.
- Public HTML; no login is required to read the current listing.

## Retrieve

Fetch the current-listings URL with a normal browser user agent and parse the tables headed:

- `Avalikuks konsulteerimiseks esitatud eelnoud` (public consultations)
- `Kooskolastamiseks esitatud eelnoud` (coordination)
- `Vabariigi Valitsusele esitatud eelnoud` (government submissions)

The visible rows contain title, EIS number, initiator reference, start date, deadline when applicable, status, and type. Keep each row associated with its table heading.

For records outside the current listing, use the page's `Tapne otsing` (exact search). EIS uses a stateful JavaScript form rather than stable query-string URLs, so use a browser for historical searches and preserve the final share URL or EIS number.

## Return

- Preserve the Estonian title, EIS number, initiator reference, dates, status, type, listing category, source URL, and retrieval time.
- Label whether a record is a consultation, coordination item, or government submission.
- Use Riigi Teataja for final enacted text; EIS describes the draft workflow.

## Limits

- Row links are JavaScript form events, not ordinary document URLs.
- The formerly advertised `/main/mount/rss/home/publicConsult.rss` endpoint no longer returns RSS reliably; do not use it.
- The homepage is a current/recent view, not a complete historical export.

## Verify

- Require HTTP 200 HTML with the EIS title, all three listing headings, and at least one row containing an EIS-style identifier such as `SOM/26-0813`.
- Reject a Cloudflare challenge, login page, or empty shell as data.
