---
name: bank-of-statistics
description: Retrieve Bank of Estonia macro-financial statistics and exchange-rate series from its public statistics portal JSON endpoints.
---

# Bank of Estonia Statistics

## Access

Public JSON endpoints behind the portal at `https://statistika.eestipank.ee/`. No login, but send a browser user agent plus `Referer: https://statistika.eestipank.ee/`; Cloudflare may reject generic clients.

## Retrieve

Use these headers for `/spring/*` requests:

```text
Accept: application/json, text/plain, */*
X-Requested-With: XMLHttpRequest
Referer: https://statistika.eestipank.ee/
User-Agent: Mozilla/5.0
```

Currency discovery:

```text
GET https://statistika.eestipank.ee/spring/getValuutad?lang=et
```

Known-valid history example:

```text
GET https://statistika.eestipank.ee/spring/getValuutaKurssAjaloos?valuuta1=USD&valuuta2=GBP&aegAlg=1.1.2010&aegLopp=7.1.2010&lang=et&step=DAY
```

`step` accepts `DAY`, `WEEK`, `MONTH`, `QUARTER`, `SEMIANNUAL`, or `YEAR`. Dates use `d.m.yyyy`. Other indicator families are selected in the portal; preserve the `/spring/*` request and parameters observed there.

## Return

Keep the indicator/currency codes, date or period, value, unit/currency, frequency, filters, endpoint, parameters, and retrieval time. The exchange-rate history fields are `aeg`, `kurss`, and `teade`; decimal commas are locale-formatted numbers.

## Limits

- The frontend endpoints are public but not a versioned API; contracts can change with the portal.
- Incomplete or incompatible parameters can return an empty array with HTTP 200.
- Cloudflare cookies or a normal user agent may be required even when the endpoint is public.

## Verify

Require `application/json` and a non-empty array. The known-valid history example returns four records dated 4-7 January 2010; `getValuutad` returns objects containing `code`, `name`, and `teade`.
