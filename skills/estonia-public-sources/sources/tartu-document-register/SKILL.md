---
name: tartu-document-register
description: Search Tartu's public document register for legal acts, agendas, minutes, contracts, correspondence, orders, stenograms, and construction records.
---

# Tartu Document Register

## Access

- Register chooser: `https://info.raad.tartu.ee/dhs.nsf/dokreg?readform`
- Public HTML backed by Lotus Notes views; no login is required.
- The old `webaktid.nsf` route redirects to the same document-register splash page and is not a separate source.

## Retrieve

Fetch the chooser and select the view matching the record type. Direct view prefixes are:

- `koik` - all records
- `oigusaktid` - legal acts
- `haldusaktid` - permits, precepts, and other decisions
- `paevakorrad` - agendas
- `protokollid` - minutes
- `lepingud` - contracts
- `skirjad` / `vkirjad` - incoming / outgoing correspondence
- `kaskkirjad` - administrative orders
- `Stenogrammid` - meeting transcripts
- `epd` - construction-related documents

Each search view starts with this query string:

```text
?SearchView&Count=100&Start=1&SearchOrder=4&SearchMax=1000
```

Open the chosen view in a browser, fill its record-specific fields, and submit. Preserve the resulting URL and filter values. Search results are newest first, return at most 1,000 matches, and show 100 rows per page.

## Return

- Preserve the document type, registry number, title/summary, issuer or correspondent, registration/adoption date, access status, detail URL, attached full-text links, search filters, and retrieval time.
- Keep restricted records in the result only when their public metadata is relevant; do not claim access to restricted full text.

## Limits

- Physical-person names in correspondence may be reduced to initials.
- Search fields differ by document type, so choose the view before forming the query.
- Lotus Notes search URLs are stateful and awkward to construct manually; use browser interaction when a direct GET does not reproduce the result.

## Verify

- Require HTTP 200 HTML whose title is `Dokumendiregister`.
- Require chooser links for `oigusaktid`, `paevakorrad`, `protokollid`, and `lepingud`; the bare `dhs.nsf` splash page is not a successful data response.
