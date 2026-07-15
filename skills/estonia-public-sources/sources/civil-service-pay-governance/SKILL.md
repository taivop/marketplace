---
name: civil-service-pay-governance
description: Retrieve Ministry of Finance civil-service pay guidance, job-evaluation material, disclosure instructions, and the current salary-disclosure template.
---

# Civil Service Pay Governance

## Access

- Index: `https://www.fin.ee/riigihaldus-ja-avalik-teenistus-kinnisvara/avalik-teenistus/palgakorraldus`
- No authentication is required; documents are direct PDF/XLSX links.

## Retrieve

Fetch the index and parse anchors whose URLs end in `.pdf` or `.xlsx`. Keep the anchor text and nearby heading so guidance, higher-official salary calculations, disclosure instructions, and disclosure templates remain distinguishable.

For the annual template, choose the link labeled with the requested year and `põhipalgad vorm`. Its `Põhipalk` sheet contains the disclosure columns `Asutus`, `Struktuuriüksus`, `Ametikoht`, `Eesnimi`, `Perekonnanimi`, `Ametniku koormus ametikohal`, and `Põhipalk`.

## Return

Return the index URL, document title, direct URL, format, year/version from the label, document category, and retrieval time. Preserve the template's original Estonian headers.

## Limits

- The XLSX is a disclosure template, not the completed salary dataset. Use `public-sector-statistics-fin` for published salary records.
- Guidance and methodology documents have independent version dates; do not infer that every file is annual.

## Verify

Require direct PDF/XLSX signatures and, for the template, the `Põhipalk` sheet plus the expected disclosure columns.
