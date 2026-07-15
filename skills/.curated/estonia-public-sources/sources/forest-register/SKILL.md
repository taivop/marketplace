---
name: forest-register
description: Query the public Forest Register JSON API for properties, cadastral units, forest stands, inventory attributes, geometry, and proposed work.
---

# Forest Register

## Access

- Application: `https://register.metsad.ee/`
- API base: `https://register.metsad.ee/portaal/api/rest/`
- No authentication is required for the public calls below.

## Search

Send `GET eraldis/puu` with one or more URL parameters:

- `katastriNr`: cadastral identifier.
- `kinnistuNr`: property number.
- `yksuseNimi`: property name.
- `kvartaliNr`: forest quarter number.
- `maakondKood` and `valdKood`: optional location narrowing.

At least one of `katastriNr`, `kinnistuNr`, `yksuseNimi`, or `kvartaliNr` is required; county or municipality alone is not a search. Example:

```text
GET https://register.metsad.ee/portaal/api/rest/eraldis/puu?kinnistuNr=12345
```

The response is a property tree: top-level units contain `alamYksused`, and cadastral sub-units contain `eraldised`. Each stand has an `id`, `katastriNr`, `eraldiseNr`, `pindala`, status, ownership label, and EPSG:3301 GeoJSON string.

## Detail

Use the stand `id`, not its displayed stand number:

```text
GET https://register.metsad.ee/portaal/api/rest/eraldis/detail/{id}
```

Return identifiers, property and cadastral data, inventory date, county/municipality, area, site and main-species codes, dimensions, age/composition elements, volume/increment, damage, special features, proposed work, ownership fields, and `alaGeoJson` as available.

## Limits

- Code fields such as `kasvukohaKood`, `peapuuliik`, and `tooKood` are register classifications; do not guess labels when a code list has not been retrieved.
- Dates are Unix epoch milliseconds in several fields.
- `alaGeoJson` is a JSON-encoded string in EPSG:3301, not an already parsed WGS84 geometry.

## Verify

Require a non-empty `eraldised` list, then require the detail response `id` to match the requested stand and preserve `katastriNr` plus `eraldiseNr`.
