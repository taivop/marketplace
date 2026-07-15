---
name: eu-funded-projects
description: Download RTK project-level EU and related funding workbooks from its public Nextcloud WebDAV share.
---

# EU-Funded Projects

## Access

- Official index: `https://www.rtk.ee/toetuste-ulevaated-oigusaktid/ulevaade-toetatud-projektidest/toetatud-projektid`
- Public file share: `https://pilv.rtk.ee/s/Mig46PpedQosEam`
- WebDAV root: `https://pilv.rtk.ee/public.php/webdav/`
- Public, no password. Use HTTP Basic username `Mig46PpedQosEam` with an empty password.

## Retrieve

1. Send `PROPFIND` to the WebDAV root with header `Depth: 2` and the public-share credentials.
2. Parse the DAV XML responses. Select an XLSX by filename and `getlastmodified`; do not hard-code the dated filename.
3. Current folders distinguish the latest Kohesio export, domestic programmes, and supported-project tables for historical and current funding periods.
4. GET the selected percent-encoded `d:href` from `https://pilv.rtk.ee` with the same credentials.
5. Read the workbook's title and multi-row headers before normalizing it. In the current combined workbook, the project table starts after title/blank rows and uses two header rows.

Example listing:

```bash
curl -u 'Mig46PpedQosEam:' -X PROPFIND -H 'Depth: 2' \
  https://pilv.rtk.ee/public.php/webdav/
```

## Return

Keep the source filename, modification date, funding period, fund, measure, project number and name, recipient and registry code, region, dates, status, budget components, and paid amounts. Preserve approved budget and paid amounts as separate fields.

## Limits

- Filenames contain dates and are replaced as RTK updates the export.
- Older funding periods are separate workbooks; choose by filename rather than assuming the newest file covers all periods.
- Excel dates and merged/multi-row headings require workbook-aware parsing.

## Verify

Require HTTP `207 Multi-Status`, DAV `200` entries, XLSX content type, a non-zero content length, and a workbook containing project, recipient, and funding fields. Reject the RTK narrative page or Power BI/Tableau embed as a data response.
