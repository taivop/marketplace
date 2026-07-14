---
name: official-notices
description: Retrieve public Ametlikud Teadaanded notices as HTML, XML, RDF, or text through its documented stable URI scheme.
---

# Official Notices

## Access

- URI contract and current type slugs: `https://www.ametlikudteadaanded.ee/avalik/uriotsing`
- Interactive search: `POST https://www.ametlikudteadaanded.ee/avalik/otsing`
- Public notice URIs: `https://www.ametlikudteadaanded.ee/ee/...`

## Retrieve

Build a URI in this order:

`/ee/{publisher}/{main-type}/{subtype}/{year}/{month}/{day}/{notice-number}/{format}`

Trailing components may be omitted. Use `-` for an unused publisher, main type, or subtype in the middle. The optional format is `xml`, `rdf`, or `txt`; without it the response is HTML. For example, `/ee/-/advokatuur/xml` returns a public XML collection for the `advokatuur` main type.

Read publisher and type slugs from the URI contract page. XML collections use root element `at:teadaanded`; each `at:teadaanne` includes the notice number, canonical URL, type, legal basis, purpose, publisher, publication data, and notice-specific fields.

For ad hoc name/keyword searches, POST `do_search=1`, `o__search_term`, and optional `o__teate_liigid`, `o__teate_alaliik_list`, `o__avaldamise_kuupaev_alates`, and `o__avaldamise_kuupaev_kuni` to `/avalik/otsing`.

## Return

- Preserve notice number, canonical URL, publication date, publisher, main/subtype, legal basis, status, matched party fields, query URI, and retrieval time.
- Keep notice publication distinct from the underlying court, insolvency, procurement, or administrative action.

## Limits

- URI searches return at most 1,000 results. Narrow by type and date when completeness matters.
- The open URI interface excludes archived notices and notices addressed to natural persons for service.
- Notice XML can contain personal data lawfully published in the source. Return only fields needed for the user's request.

## Verify

- Require the contract page to contain the documented URI pattern and current type slugs.
- Require a collection URI ending in `/xml` to return parseable XML with `at:teadaanded` and at least one `at:teadaanne` containing `teate_number` and `url`.
