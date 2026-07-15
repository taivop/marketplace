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

## Output and limits

- Keep the queried identifier, endpoint, retrieval time, and exact returned fields or message.
- Minimize personal-data queries: use a personal identifier only when the task requires it and the user is entitled to perform the public lookup.
- A no-arrears response is a point-in-time result, not proof that arrears never existed.

## Verification

Registry code `70000349` returns the public EMTA entity name in both forms and reference number `01000012` in the reference-number result.
