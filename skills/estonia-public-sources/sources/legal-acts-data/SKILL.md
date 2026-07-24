---
name: legal-acts-data
description: Search and retrieve official Estonian legislation through the Riigi Teataja legal-acts JSON API and linked act representations.
---

# Riigi Teataja Legal Acts

## Access

Public JSON search API and linked XML act texts. No authentication.

## Retrieve

Start with a bounded search:

```text
GET https://www.riigiteataja.ee/api/oigusakt_otsing/1/otsi?leht=1&limiit=25&pealkiri=riigieelarve
```

Useful query parameters include `leht` (page), `limiit` (page size), and `pealkiri` (title text). Add filters from the Riigi Teataja search UI only after confirming their exact URL names.

The response contains:

- `staatus` and `paring`;
- `metaandmed.kokku`, `metaandmed.leht`, and `metaandmed.limiit`;
- `aktid`, including `globaalID`, `terviktekstID`, `pealkiri`, `liik`, `valjaandja`, `kehtivus`, `staatus`, and relative `url`.

Resolve a returned `url`, such as `/akt/22451.xml`, against `https://www.riigiteataja.ee` to retrieve the official act representation.

## Return

Preserve legal IDs, title, type, issuer, validity start/end, publication status, text type, act URL, search parameters, page metadata, and retrieval time. Clearly distinguish current and historical versions.

## Limits

- A broad unfiltered search is valid but returns historical as well as current acts.
- Legal validity must be read from the returned version metadata, not inferred from search order.
- Do not rewrite relative act URLs incorrectly; resolve them against the Riigi Teataja origin.

## Verify

Require HTTP 200 JSON, `staatus: OK`, integer pagination metadata, and a parseable `aktid` array. At least one returned act must contain `globaalID`, `pealkiri`, `kehtivus`, and `url` before reporting success.

## Contract drift warning (verified 2026-07-24)

Resolving act representations like `/akt/{id}.xml` against `https://www.riigiteataja.ee` now returns the HTML application shell (SPA), NOT the act text — regardless of Accept header. Do not treat that HTML as act content, and do NOT recite paragraph (§) text from memory as if it were fetched.

Working text endpoints (verified 2026-07-24):

- `GET https://www.riigiteataja.ee/public-api/api/v1/akt/{globaalID}` — act metadata JSON.
- `GET https://www.riigiteataja.ee/public-api/api/v1/akt/{globaalID}/blob-html` — full consolidated act HTML. Responses can exceed 500 KB and the endpoint ignores Range headers, so a truncating `http_request` (20k) only returns the head; fetch and filter it inside the `run_code` sandbox instead.

If those endpoints are unavailable, ground answers in the search API's metadata only (title, validity, status, act URL), summarize at that level, and link the act for the user to read the text.

## Weak-model workflow: worked run_code script (added 2026-07-24, issue #8)

`pealkiri=` search matches substrings AND returns one `aktid` row per historical redaction, so a title search for e.g. "Töölepingu seadus" returns dozens of rows sharing the exact title, each a different consolidated-text version with its own `kehtivus.algus`/`lopp`. Do not just take the first search hit. To find the version actually in force:

1. Filter `aktid` to rows whose `pealkiri` equals the searched title exactly (not a substring match).
2. Among those, keep rows where `kehtivus.algus <= today` and (`kehtivus.lopp` is null or `>= today`).
3. Sort by `kehtivus.algus` descending and fetch `/public-api/api/v1/akt/{globaalID}` for each, starting with the highest `algus`, until one has top-level `aktiStaatus === "KEHTIV"` — that is the authoritative in-force signal. (A field named `kehtivId` exists on the metadata response but was observed always equal to the requested `globaalID` itself in testing 2026-07-24 — it did NOT point to a different, more-current globaalID. Do not rely on it; use `aktiStaatus` instead.)

Then fetch `blob-html` for that `globaalID`, `save()` it (it can exceed 500 KB), and locate sections by scanning for `§ <n>` or a keyword with `indexOf`, printing a window of characters around each hit — HTML tags included, so strip them for readability. A single keyword match is not guaranteed to be the right section (e.g. "maksimaalne" appears once in Perehüvitiste seadus but for an unrelated elatisabi clause) — print several hits and let the surrounding heading text (`§ NN. <title>`) disambiguate, or search a more specific phrase (benefit ceilings: search "ülempiir", not "maksimaalne").

State numeric values, multipliers, and deadlines ONLY if their exact wording appears in a window you printed — if the printed window cuts off before the operative words, print a wider window instead of completing the sentence from memory (observed failure: § 40 located, but the model answered "kolmekordne" from memory while the fetched text says "kahekordne").

```js
import { get, show, save, sleep } from "./kratt.mjs";

async function getRetry(url) {
  try {
    return await get(url);
  } catch (e) {
    if (!String(e).includes("429")) throw e;
    await sleep(2000);
    return await get(url); // one retry, then let it throw
  }
}

async function fetchCurrentAct(title) {
  const q = encodeURIComponent(title);
  const search = await getRetry(`https://www.riigiteataja.ee/api/oigusakt_otsing/1/otsi?leht=1&limiit=200&pealkiri=${q}`);
  const today = new Date().toISOString().slice(0, 10);
  const exact = (search.aktid ?? []).filter(a => a.pealkiri === title);
  if (exact.length === 0) throw new Error(`No exact title match for "${title}"`);
  const candidates = exact
    .filter(a => (a.kehtivus.algus ?? "") <= today && (a.kehtivus.lopp === null || a.kehtivus.lopp >= today))
    .sort((a, b) => b.kehtivus.algus.localeCompare(a.kehtivus.algus));
  for (const c of candidates) {
    const meta = await getRetry(`https://www.riigiteataja.ee/public-api/api/v1/akt/${c.globaalID}`);
    if (meta.aktiStaatus === "KEHTIV") return { globaalID: c.globaalID, meta };
  }
  if (candidates.length === 0) throw new Error(`No currently-dated redaction for "${title}"`);
  const fallback = candidates[0]; // best guess if none confirmed KEHTIV
  return { globaalID: fallback.globaalID, meta: await getRetry(`https://www.riigiteataja.ee/public-api/api/v1/akt/${fallback.globaalID}`) };
}

function findAround(html, term, max = 3) {
  const hits = [];
  let idx = -1;
  while (hits.length < max && (idx = html.indexOf(term, idx + 1)) !== -1) {
    hits.push(html.slice(Math.max(0, idx - 400), idx + 400).replace(/<[^>]+>/g, " ").replace(/\s+/g, " "));
  }
  return hits;
}

const { globaalID, meta } = await fetchCurrentAct("Töölepingu seadus"); // example verified 2026-07-24: globaalID 103072026034
show({ globaalID, aktiStaatus: meta.aktiStaatus, algus: meta.aktiParameetrid.kehtivuseAlgus, lopp: meta.aktiParameetrid.kehtivuseLopp });

const html = await getRetry(`https://www.riigiteataja.ee/public-api/api/v1/akt/${globaalID}/blob-html`);
await save(`akt_${globaalID}.html`, html); // reuse in later run_code calls with load() instead of refetching
show(`saved ${html.length} chars as akt_${globaalID}.html`);

for (const hit of findAround(html, "§ 97")) show(hit, 500);
for (const hit of findAround(html, "etteteatamise")) show(hit, 500);
```

Later run_code calls in the same question should `load("akt_{globaalID}.html")` to re-slice for a different section instead of refetching the ~550 KB blob.

Verified live 2026-07-24 (plain `node -e` fetch chain, no sandbox):
- "Töölepingu seadus" → currently valid `globaalID: 103072026034` (`aktiStaatus: "KEHTIV"`, in force 2026-07-13..2026-09-30). `blob-html` (550,960 chars) contains `§ 97. Tööandja ülesütlemise etteteatamise tähtajad` and the string "etteteatamise" (multiple hits).
- "Perehüvitiste seadus" → currently valid `globaalID: 121052026010` (`aktiStaatus: "KEHTIV"`, in force 2026-05-22..2026-08-31). `blob-html` (335,756 chars) contains `§ 40. Vanemahüvitise ülempiir`, found by searching "ülempiir" (15 hits) or "vanemahüvitis" (202 hits, so prefer the narrower term); searching "maksimaalne" alone finds only an unrelated elatisabi clause (§ 50(4)), not the parental-benefit cap — a reminder to check the heading around a hit, not just the raw string match.
