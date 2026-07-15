---
name: geospatial-open-data
description: Retrieve Estonian Land and Spatial Board maps, cadastral/address layers, and topographic vectors through public OGC services.
---

# Geospatial Open Data

## Access

Public WMS/WFS/WMTS services and file downloads. No authentication.

## Endpoints

- Service index: https://geoportaal.maaamet.ee/eng/services/public-wms-wfs-p346.html
- Base-map WMS capabilities: https://kaart.maaamet.ee/wms/alus?SERVICE=WMS&REQUEST=GetCapabilities
- Address/cadastral WMS: https://kaart.maaamet.ee/wms/aadressid?
- Orthophoto WMS: https://kaart.maaamet.ee/wms/fotokaart?
- ETAK WFS capabilities: https://gsavalik.envir.ee/geoserver/etak/ows?service=WFS&request=GetCapabilities
- Downloads: https://geoportaal.maaamet.ee/eng/spatial-data-p58.html

## Retrieve

1. Fetch `GetCapabilities` for the selected service.
2. Read advertised layer/type names, supported CRS, operations, and output formats.
3. Use WMS `GetMap` for rendered imagery or WFS `GetFeature` for vectors; bound requests with BBOX, feature count, or filters.
4. Preserve the service URL, layer/type name, CRS, axis order, BBOX/filter, and output format.

## Return

Keep authoritative layer identifiers, CRS, geometry type, source service, query parameters, feature attributes/geometries or map file, and retrieval time.

## Limits

- Do not guess layer names from portal labels; use the current capabilities document.
- WMS is rendered imagery, not feature data.
- CRS axis order differs by WMS/WFS version; verify coordinates before spatial joins.

## Verify

Require parseable OGC capabilities XML. WMS must expose a capabilities root and named layers; WFS must expose `WFS_Capabilities`, `FeatureTypeList`, and at least one feature type before issuing data requests.
