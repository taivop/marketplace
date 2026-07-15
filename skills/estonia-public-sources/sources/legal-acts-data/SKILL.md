---
name: legal-acts-data
description: Search and retrieve official Estonian legislation through the Riigi Teataja legal-acts JSON API and linked act representations.
---

# Riigi Teataja Legal Acts

## Access

Public JSON search API and linked XML act texts. No authentication.

## Retrieve

Start with a bounded search:

```text
GET https://www.riigiteataja.ee/api/oigusakt_otsing/1/otsi?leht=1&limiit=25&pealkiri=riigieelarve
```

Useful query parameters include `leht` (page), `limiit` (page size), and `pealkiri` (title text). Add filters from the Riigi Teataja search UI only after confirming their exact URL names.

The response contains:

- `staatus` and `paring`;
- `metaandmed.kokku`, `metaandmed.leht`, and `metaandmed.limiit`;
- `aktid`, including `globaalID`, `terviktekstID`, `pealkiri`, `liik`, `valjaandja`, `kehtivus`, `staatus`, and relative `url`.

Resolve a returned `url`, such as `/akt/22451.xml`, against `https://www.riigiteataja.ee` to retrieve the official act representation.

## Return

Preserve legal IDs, title, type, issuer, validity start/end, publication status, text type, act URL, search parameters, page metadata, and retrieval time. Clearly distinguish current and historical versions.

## Limits

- A broad unfiltered search is valid but returns historical as well as current acts.
- Legal validity must be read from the returned version metadata, not inferred from search order.
- Do not rewrite relative act URLs incorrectly; resolve them against the Riigi Teataja origin.

## Verify

Require HTTP 200 JSON, `staatus: OK`, integer pagination metadata, and a parseable `aktid` array. At least one returned act must contain `globaalID`, `pealkiri`, `kehtivus`, and `url` before reporting success.
