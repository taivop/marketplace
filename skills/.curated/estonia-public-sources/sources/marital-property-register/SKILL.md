---
name: marital-property-register
description: Query public aggregate statistics from Estonia's Marital Property Register by period, card status, property regime, and source document.
---

# Marital Property Register Statistics

## Access

- Form: `https://abieluvararegister.rik.ee/Statistika`
- Results endpoint: `GET https://abieluvararegister.rik.ee/Statistika/Otsi`
- Public aggregate HTML; no authentication is required. Individual register searches are a separate authenticated service and are outside this recipe.

## Retrieve

Send `dd.mm.yyyy` dates as `SearchFilter.AlgusKp` and `SearchFilter.LoppKp`. Include one or more boolean category parameters:

- card status: `SearchFilter.Kehtivad`, `SearchFilter.Suletud`
- regimes: `SearchFilter.VarasuhteLiik.VaralahutusStat`, `VarayhisusStat`, `VaraJuurdekasvuStat`, `ValisriigiOiguseStat`
- documents: `SearchFilter.Dokumendid.AbiellumisAvaldus`, `Abieluvaraleping`, `Kohtulahend`, `Kooseluleping`, `MuuDokument`

Prefix the last two groups with `SearchFilter.VarasuhteLiik.` or `SearchFilter.Dokumendid.` exactly as shown. Use `true` for selected values. A normal user agent plus `X-Requested-With: XMLHttpRequest` and a statistics-page referer reproduces the browser request.

Example period: `01.01.2025` through `31.01.2025`, both card statuses, and all regime/document categories.

## Return

- Parse the result tables by their original row and column labels.
- Preserve the period, regime/document category, total valid cards, total closed cards, cards opened in the period, and cards closed in the period.
- Include the exact parameters, source URL, and retrieval time.

## Limits

- Results are aggregates, not person-level records.
- The UI can export the displayed table through a temporary server-side file flow; parsing the HTML result avoids that stateful extra step.
- Category labels are Estonian.

## Verify

- Require HTTP 200 `text/html` containing the requested period and the columns `Kehtivaid kaarte kokku` and `Suletud kaarte kokku`.
- Require rows for multiple property regimes; reject the form page itself as a result.
