---
name: business-register-open-data
description: Look up an Estonian company's registry code, status, and address by name, or download bulk Business Register snapshots (entities, shareholders, beneficial owners).
---

# Business Register Open Data

## Single-company lookup by name (preferred for one registry code)

For a single company's registry code (`registrikood`), status, or address — do NOT
download a bulk snapshot. Use the public autocomplete JSON the search UI calls. No
authentication, returns JSON directly, works with any user agent.

```text
GET https://ariregister.rik.ee/est/api/autocomplete?q=Bolt+Technology&company=true
```

- `q` is a name substring (URL-encoded). `company=true` restricts to legal entities.
- Response: `{ "status": "OK", "data": [ { "reg_code", "name", "historical_names",
  "status", "legal_address", "zip_code", "legal_form", "url", "company_id" }, ... ] }`.
- `status` is a registry status code (`R` = registered/active).
- `historical_names` lets you match a company that was renamed (e.g. "Taxify OÜ" →
  "Bolt Technology OÜ").
- Match the exact name against `name` (or `historical_names`); if several rows
  come back, do not blindly take the first — pick the one whose name matches.

The `/est/api/autocomplete` path works and returns JSON. Do NOT use the bare
`/api/autocomplete` path — it returns a Cloudflare error page.

### Anti-fabrication grounding rule (issue #16)

A registry code is an identifier, not something to recall. State a registry code
ONLY if it appears verbatim in output your script actually printed from this
endpoint. If the lookup returns an empty `data` array, an error, or you cannot
match the requested company, say the code could not be retrieved — NEVER supply a
registry code from memory or guess an 8-digit number. (Observed failure: the agent
confidently answered fabricated codes like 14036220 / 14532842 for Bolt Technology
OÜ; the real code is 12417834, which this endpoint returns.)

### Worked run_code script (registry code + tax-arrears, verified 2026-07-24)

This resolves the registry code, then chains into the EMTA public tax-arrears query
(see `tax-public-inquiries`). The tax-arrears form needs a cookie + CSRF token, so
that half uses raw `fetch` (the `get` helper does not expose response headers);
`get` is fine for the autocomplete lookup.

```js
import { get, show, sleep } from "./kratt.mjs";

const name = "Bolt Technology"; // company name (substring is fine)

// 1. Registry code via the autocomplete JSON.
const ac = await get(
  "https://ariregister.rik.ee/est/api/autocomplete?q=" +
    encodeURIComponent(name) + "&company=true"
);
const rows = ac.data ?? [];
const hit =
  rows.find((c) => (c.name || "").toLowerCase().startsWith(name.toLowerCase())) ??
  rows[0];
if (!hit) {
  show("NO MATCH — registry code could not be retrieved for: " + name);
} else {
  const regCode = String(hit.reg_code);
  show({ regCode, status: hit.status, name: hit.name, address: hit.legal_address });

  // 2. Tax arrears: GET form (capture SAQUSESSION cookie + CSRFToken), then POST.
  const formRes = await fetch("https://apps.emta.ee/saqu/public/taxdebt?lang=en");
  const cookie = (formRes.headers.getSetCookie()[0] || "").split(";")[0];
  const formHtml = await formRes.text();
  const token = /name="CSRFToken"\s+value="([^"]+)"/.exec(formHtml)?.[1];

  const body = new URLSearchParams({
    personCode: regCode,
    p_submit: "Search",
    CSRFToken: token,
  });
  const debtRes = await fetch("https://apps.emta.ee/saqu/public/taxdebt/query", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded", Cookie: cookie },
    body: body.toString(),
  });
  const debtText = (await debtRes.text())
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  show("TAX ARREARS (HTTP " + debtRes.status + "): " + debtText.slice(0, 400));
}
```

Verified live 2026-07-24: autocomplete for "Bolt Technology" returns
`reg_code: 12417834`, `name: "Bolt Technology OÜ"`, `status: "R"`,
`historical_names: ["Taxify OÜ", "MTAKSO OÜ"]`; the EMTA query then prints
"Person Bolt Technology OÜ (12417834) has no arrears as of <timestamp>". Report the
arrears status only from that printed line, with its timestamp — a no-arrears result
is point-in-time, not proof arrears never existed.

## Bulk snapshots (many companies / fields not in autocomplete)

Public ZIP snapshots from `https://avaandmed.ariregister.rik.ee/en/downloading-open-data`.
No login. Send a normal user agent if Cloudflare returns 403. Use these only when you
need bulk data or fields the autocomplete does not carry (shareholders, beneficial
owners, registry-card detail) — not for a single company's registry code.

1. Fetch the download page and select the dataset family and format.
2. Resolve relative links against `https://avaandmed.ariregister.rik.ee`.
3. Download the archive, record its filename and retrieval time, and verify the ZIP before parsing.

Known direct snapshot:

```text
https://avaandmed.ariregister.rik.ee/sites/default/files/avaandmed/ettevotja_rekvisiidid__lihtandmed.csv.zip
```

Other published families include `yldandmed`, `registrikaardid`, `kaardile_kantud_isikud`, `osanikud`, `kasusaajad`, `kommertspandid`, and `maarused`, commonly as JSON or XML ZIPs.

## Return

Preserve registry code (`reg_code`/`ariregistri_kood`), legal form and status,
name and historical names, address, source, and retrieval time. For bulk snapshots
also keep the source filename and snapshot date. Keep beneficial-owner and person
records separate from core entity records.

## Limits

- Archives are large; inspect headers and stream/process them instead of loading several complete snapshots into memory.
- Static snapshots are open; WSDL/API services linked from the site can have different terms or fees.
- Schemas differ across dataset families and formats.

## Verify

- Autocomplete: require HTTP 200 JSON with `status: "OK"` and a `data` array; a
  usable result has a numeric `reg_code` and a `name` matching the requested company.
- Bulk: require HTTP 200, `application/zip`, ZIP magic bytes `PK`, and a valid archive
  member; for the simple CSV snapshot require a header containing the registry
  identifier before analysis.
