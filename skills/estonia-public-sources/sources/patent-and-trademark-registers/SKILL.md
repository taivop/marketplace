---
name: patent-and-trademark-registers
description: Query the Estonian Patent Office's current public invention, trademark, and industrial-design databases.
---

# Patent and Trademark Registers

## Trademarks and designs

Use the public JSON APIs behind `https://andmebaas.epa.ee/avalik/`:

```text
GET https://andmebaas.epa.ee/avalik/api/trademarks/search/findBySearchParameters
GET https://andmebaas.epa.ee/avalik/api/designApplications/search/findBySearchParameters
```

Both accept `page` (zero-based), `size`, and optional filters such as:

- `registrationNumber`
- `applicationNumber`
- `verbalElement`
- `applicantOwner`
- `types`
- `currentStatus`
- date-range fields shown in the public form

Trademark searches also support `exactMatch`, `markKind`, Nice classes/terms, and Vienna image classes. Design searches also support `author`, Locarno classes, and `numberOfVariants`.

Results use Spring HAL: records are under `_embedded.trademarks` or `_embedded.designApplications`. Keep `id`, dossier type, application and registration numbers/dates, current status, verbal element/title, owner sort value, and relevant classification fields.

For related data, request the public relation directly, for example:

```text
GET https://andmebaas.epa.ee/avalik/api/trademarks/<id>/persons
GET https://andmebaas.epa.ee/avalik/api/trademarks/<id>/goodsAndServicesSpecifications
GET https://andmebaas.epa.ee/avalik/api/designApplications/<id>/persons
GET https://andmebaas.epa.ee/avalik/api/designApplications/<id>/locarno
```

Ignore HAL links whose host is `127.0.0.1`; reconstruct the path on `https://andmebaas.epa.ee` as shown above.

## Inventions

- Public application: `https://leiutised.epa.ee/avalik/home?selectedTab=general`
- Use `General search` for registration/application number, dates, Estonian or English title, keyword, applicant/owner, author, representative, or status.
- Use `Invention search` for invention-specific fields.
- Run the browser search, then extract the result list and selected record. The application currently requires browser rendering and does not publish a supported API contract.

## Limits

- These databases are informative; official registers and gazette notices have legal effect.
- Trademark data is normally updated daily, design data weekly, and invention data continuously.
- The old `online.epa.ee` and `teenused.epa.ee` routes are filing services, not the current public search databases.

## Verify

For trademark/design API searches, require the expected `_embedded` collection and identifiers/status fields. For inventions, require the page title `Patendiameti avalik veebirakendus`, the two search tabs, and a result linked to the submitted identifier or term.
