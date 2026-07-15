---
name: state-assets-register
description: Download nightly XML extracts and the XSD for Estonia's State Real Estate Register (RKVR).
---

# State Real Estate Register Open Data

Use this source for state real estate, land, buildings, structures, proceedings, contracts, and real-estate complexes. Use `state-ownership-data` for state-owned companies and foundations.

## Endpoints

Base: `https://riigivara.fin.ee/rkvr/api/avaandmed`

| Extract | URL suffix | XML root |
|---|---|---|
| Real estate | `/KINNISVARAD` | `kinnisvarad` |
| Land | `/MAAD` | `maad` |
| Buildings | `/HOONED` | `hooned` |
| Structures | `/RAJATISED` | `rajatised` |
| Proceedings | `/MENETLUSED` | `menetlused` |
| Contracts | `/LEPINGUD` | `lepingud` |
| Real-estate complexes | `/KINNISVARAYKSUSED` | `kinnisvarayksused` |

- Schema: `https://riigivara.fin.ee/rkvr/api/avaandmed-xsd`
- Human index: `https://riigivara.fin.ee/rkvr-frontend/#/aruanded/avaandmed`

## Workflow

1. Download the XSD and only the extracts needed for the question. The files are regenerated nightly.
2. Parse XML using the XSD element names; preserve register identifiers and relationship keys so records can be joined across extracts.
3. Keep the canonical endpoint, retrieval time, and extract type. Treat the response as XML even though extract endpoints report `text/plain`.

## Verification

- Each extract returns an attachment named after its lowercase root, such as `kinnisvarad.xml`.
- The XSD returns `application/xsd+xml` and defines the extract structures.
