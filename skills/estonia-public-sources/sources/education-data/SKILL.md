---
name: education-data
description: Download public EHIS education-register extracts for institutions, curricula, and institutions with unconfirmed data.
---

# Education Data (EHIS)

## Use when
- You need public education-institution contacts or curriculum-register records.
- You need the EHIS list of institutions whose registry data is unconfirmed.

## Avoid when
- You need student-level personal data; it is not public.
- You need general education indicators rather than EHIS registry extracts; use Statistics Estonia or the separate HaridusSilm website.

## Endpoints
- EHIS file index: https://www.ehis.ee/
- Institution contacts: `https://gituja.eenet.ee/ehis/ehis1/failihoidla/-/raw/main/koolide_kontaktid.xls?ref_type=heads&inline=false`
- Curricula: `https://gituja.eenet.ee/ehis/ehis1/failihoidla/-/raw/main/oppekavad.xlsx?ref_type=heads&inline=false`
- Unconfirmed institution data: `https://gituja.eenet.ee/ehis/ehis1/failihoidla/-/raw/main/kinnitamised_EHIS_esileht.xls?ref_type=heads&inline=false`
- Public registry UI fallback: https://enda.ehis.ee/avalik/

## Workflow
1. Use the direct file matching the requested record type.
2. Parse `.xls` with an OLE-compatible spreadsheet reader and `.xlsx` with an OOXML reader.
3. Preserve original sheet names and columns; add normalized field names only in a separate output layer.
4. Use the public registry UI only when the published snapshots omit a required field.

## Access reality
- Public direct files with no authentication, verified 2026-07-14.
- EHIS links to the three files from its homepage. The institution and unconfirmed-data files are legacy OLE `.xls`; curricula is OOXML `.xlsx`.
- The server labels downloads `application/octet-stream`, so validate the file signature rather than relying on MIME type.

## Output schema expectations
- Keep the source URL, retrieval timestamp, workbook/sheet name, and original EHIS columns.
- Keep institution and curriculum identifiers exactly as stored.

## Limits and caveats
- These are current published snapshots, not a historical time series.
- Registry snapshots may update without a versioned URL; record retrieval time and file hash when reproducibility matters.

## Verification hooks
- Require OLE signature `D0 CF 11 E0 A1 B1 1A E1` for `.xls` and ZIP signature `PK 03 04` for `.xlsx`.
- Reject HTML responses even when the URL ends in a spreadsheet extension.
