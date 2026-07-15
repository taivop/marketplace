---
name: muis-open-data
description: Retrieve MuIS museum objects and related collection entities as public CIDOC-CRM RDF/XML.
---

# MuIS RDF

## Access

Public RDF over HTTP at `https://opendata.muis.ee/`. No authentication. Request `Accept: application/rdf+xml`.

## Retrieve

Known-valid object:

```text
GET https://opendata.muis.ee/object/1522095
Accept: application/rdf+xml
```

Documented path families include:

- `/object/{museum-object-id}`
- `/media-list/{museum-object-id}`
- `/person-group/{subject-id}`
- `/thesaurus/{thesaurus-id}` and `/thesaurus/{thesaurus-id}/{term-id}`
- `/event/{event-id}`
- `/place/{place-id}`
- collection, museum, and bulk object paths listed on the documentation page

Parse the RDF graph and follow linked resources only as needed. Use `Accept-Encoding: gzip` for documented bulk responses.

## Return

Keep endpoint URL, entity type/ID, RDF predicates and object values needed by the question, labels/titles, museum/collection links, dates/periods, linked media/resources, and retrieval time. Preserve source IDs and URIs.

## Limits

- Not every numeric ID exists; `/object/1` currently returns 404.
- Linked entities require additional requests for full context.
- RDF schema is available at `https://opendata.muis.ee/rdf-schema/muis.rdfs` and may be served as `application/octet-stream` despite containing RDF/XML.

## Verify

Require HTTP 200, parseable XML, and RDF root `{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF`. For the known object, require at least one RDF description/resource; a 404 or HTML body is not successful retrieval.
