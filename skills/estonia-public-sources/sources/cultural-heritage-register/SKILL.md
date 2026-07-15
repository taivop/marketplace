---
name: cultural-heritage-register
description: Search Estonia's National Register of Cultural Monuments by registry number or text and extract public object details from its HTML records.
---

# Cultural Heritage Register

## Access

- Search and detail base: `https://register.muinas.ee/public.php?menuID=monument`
- The public server-rendered search works without authentication or browser automation.

## Search

POST form data to the base URL. Prefer the precise fields when known:

- `regnr`: cultural-monument registry number.
- `name`: monument name.
- `address`: address text.
- `county[]`, `parish[]`, `type[]`, and `cm_type[]`: multi-value identifiers taken from the live form options.

For a broad text search, POST `nameanddescription=<at least 3 characters>` and `quickseatch=true`; the misspelled field name is the site's actual contract.

The result is HTML. Parse the table headed `Reg. nr`, `Nimi`, `Tüüp`, `Liik`, `Omavalitsus`, and `Aadress`. Each row links to:

```text
public.php?menuID=monument&action=view&id={regnr}
```

## Detail

Fetch the absolute detail URL and parse labeled fields. Return the registry number, name, monument type and class, registration/protection dates, coordinates, condition, legal instruments, keywords, descriptions, address when present, and links to available detail, property, proceeding, grant, image, and document tabs.

## Limits

- Search and records are HTML, not JSON; decode HTML entities before extracting text.
- Multi-select filter values are internal IDs. Read them from the current search form instead of guessing from labels.
- A detail page can expose different tabs and fields by monument type.

## Verify

Require the requested registry number in both the result row and detail heading, plus the detail labels `Mälestise nimi` and `Mälestise registri number`.
