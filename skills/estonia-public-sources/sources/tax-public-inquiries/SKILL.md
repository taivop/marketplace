---
name: tax-public-inquiries
description: Query the Estonian Tax and Customs Board public reference-number and tax-arrears forms with their exact session and CSRF contract.
---

# Tax Public Inquiries

Use this source for a person's or entity's public EMTA reference number or current tax-arrears result. It does not expose confidential tax filings or bulk tax records.

## Endpoints

| Inquiry | Form GET | Form POST |
|---|---|---|
| Reference number | `https://apps.emta.ee/saqu/public/reference?lang=en` | `https://apps.emta.ee/saqu/public/reference/query` |
| Tax arrears | `https://apps.emta.ee/saqu/public/taxdebt?lang=en` | `https://apps.emta.ee/saqu/public/taxdebt/query` |

## Request contract

1. Create a cookie-preserving HTTP session and GET the selected form.
2. Extract the hidden `CSRFToken` value.
3. POST `application/x-www-form-urlencoded` data to the matching query URL using the same session:
   - `personCode`: Estonian personal identification code or registry code
   - `p_submit`: `Search`
   - `CSRFToken`: token from the form
4. Parse the returned HTML table or result paragraph. The tax-arrears response includes its effective timestamp.

No CAPTCHA was present in the verified public flow. If the service later introduces one, stop automation instead of bypassing it.

## Worked run_code script (tax arrears, verified 2026-07-24)

The `get` helper does not expose response headers, so it cannot carry the session
cookie the CSRF check needs — the POST returns `403 Bad or missing CSRF value`
without the `SAQUSESSION` cookie from the GET. Use raw `fetch` and pass the cookie
back explicitly. For a company you do not yet have a registry code for, resolve it
first via `business-register-open-data` (its autocomplete JSON) — never guess it.

```js
import { show } from "./kratt.mjs";

const personCode = "12417834"; // registry code (or personal ID) — obtained from a source, not memory

// 1. GET the form: capture the SAQUSESSION cookie and the hidden CSRFToken.
const formRes = await fetch("https://apps.emta.ee/saqu/public/taxdebt?lang=en");
const cookie = (formRes.headers.getSetCookie()[0] || "").split(";")[0];
const token = /name="CSRFToken"\s+value="([^"]+)"/.exec(await formRes.text())?.[1];

// 2. POST the query with the SAME cookie + token.
const res = await fetch("https://apps.emta.ee/saqu/public/taxdebt/query", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded", Cookie: cookie },
  body: new URLSearchParams({ personCode, p_submit: "Search", CSRFToken: token }).toString(),
});
const text = (await res.text()).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
show("HTTP " + res.status + ": " + text.slice(0, 400));
```

Verified live 2026-07-24: for `personCode=12417834` this prints "Person Bolt
Technology OÜ (12417834) has no arrears as of <timestamp>". State the arrears status
and the identifier ONLY from the line the script printed, quoting its timestamp; if
the POST is not HTTP 200 or the result text is missing, report that the arrears check
failed rather than asserting a status.

## Output and limits

- Keep the queried identifier, endpoint, retrieval time, and exact returned fields or message.
- Minimize personal-data queries: use a personal identifier only when the task requires it and the user is entitled to perform the public lookup.
- A no-arrears response is a point-in-time result, not proof that arrears never existed.

## Verification

Registry code `70000349` returns the public EMTA entity name in both forms and reference number `01000012` in the reference-number result.
