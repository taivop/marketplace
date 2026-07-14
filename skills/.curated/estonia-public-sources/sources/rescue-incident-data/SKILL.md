---
name: rescue-incident-data
description: Download Rescue Board historical incident workbooks and current forest and landscape fire incident CSV records.
---

# Rescue Incident Data

Use this source for Rescue Board incident counts through 2020 and row-level forest or landscape fire incidents from 2014 onward. It is not a current row-level feed of every rescue incident type.

## Endpoints

- Historical incident workbooks: `https://www.rescue.ee/et/paeaestesuendmuste-statistika`
- Current-year forest/landscape fires: `https://opendata.smit.ee/paa/csv/metsa_ja_maastikutulekahjud_jooksev_aasta.csv`
- 2014-2025 forest/landscape fires: `https://opendata.smit.ee/paa/csv/metsa_ja_maastikutulekahjud_2014_kuni_2025.csv`
- Other Rescue Board open-data indexes: `https://www.rescue.ee/et/juhend/avaandmed`

## Workflow

1. For counts by incident type and county or month, discover the XLSX links on the historical page. It supplies 2010-2014 aggregates and annual files for 2015-2020.
2. For current row-level forest/landscape fires, download both CSV periods when the requested range crosses 2025/2026.
3. Parse the fire CSV as UTF-8, tab-delimited data despite its `application/octet-stream` content type.
4. Preserve `sundmuse_number`, incident date/type, county/municipality, coordinates, dispatch/arrival/localization timestamps, resource counts, and burned area where present.
5. Keep category definitions, source URL, covered period, and retrieval time. Do not mix incident counts with response times or burned area.

## Verification

- Historical downloads are valid XLSX files beginning `PK\x03\x04`.
- The current CSV header begins with `sundmuse_number` and `sundmuse_kuupaev_dt` and is followed by incident rows.
