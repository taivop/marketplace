---
name: business-register-open-data
description: Download Estonian Business Register snapshots for legal entities, registry cards, persons, shareholders, beneficial owners, and related company records.
---

# Business Register Open Data

## Access

Public ZIP snapshots from `https://avaandmed.ariregister.rik.ee/en/downloading-open-data`. No login. Send a normal user agent if Cloudflare returns 403.

## Retrieve

1. Fetch the download page and select the dataset family and format.
2. Resolve relative links against `https://avaandmed.ariregister.rik.ee`.
3. Download the archive, record its filename and retrieval time, and verify the ZIP before parsing.

Known direct snapshot:

```text
https://avaandmed.ariregister.rik.ee/sites/default/files/avaandmed/ettevotja_rekvisiidid__lihtandmed.csv.zip
```

Other published families include `yldandmed`, `registrikaardid`, `kaardile_kantud_isikud`, `osanikud`, `kasusaajad`, `kommertspandid`, and `maarused`, commonly as JSON or XML ZIPs.

## Return

Preserve source filename, snapshot/retrieval date, registry code (`ariregistri_kood` where present), legal form and status, registration dates, names, addresses, and source-specific relationship fields. Keep beneficial-owner and person records separate from core entity records.

## Limits

- Archives are large; inspect headers and stream/process them instead of loading several complete snapshots into memory.
- Static snapshots are open; WSDL/API services linked from the site can have different terms or fees.
- Schemas differ across dataset families and formats.

## Verify

Require HTTP 200, `application/zip`, ZIP magic bytes `PK`, and a valid archive member. For the simple CSV snapshot, require a header containing the registry identifier before analysis.
