---
name: planning-decisions
description: Query Estonia's national planning-register JSON API for plans, lifecycle status, authorities, geometry links, related plans, and public documents.
---

# Estonia Planning Decisions

## Access

- Application: `https://www.planeeringud.ee/plank-web/`
- API base: `https://www.planeeringud.ee/plank-web/api/`
- Public JSON requests require no authentication.

## Search

POST JSON to `planeering/otsing`; control the result page in the URL:

```http
POST /plank-web/api/planeering/otsing?page=0&size=25&sort=kehtestkp,desc
Content-Type: application/json

{"otsistring":"Vanalinna"}
```

`otsistring` is the verified free-text filter. The response is a Spring page with `content`, `totalElements`, `totalPages`, and page metadata. Search records include `sysid`, `planid`, `plannim`, abbreviated plan type, authority, lifecycle status, relevant dates, purpose, and map link.

## Detail

Fetch `GET planeering/{sysid}` using `sysid` from search results. Do not substitute `planid`; it is a different identifier and is not accepted by this route.

Return at least `sysid`, `planid`, name, type, status, organizing authority, purpose, lifecycle dates, `planviide`, `bbox`, related plans, and every public `planDokuments` item with its type, original filename, size, and `filePublicUrl`.

## Limits

- Status is lifecycle data. Keep the original `planseisNimi` or `klPlanseisByPlanseis`, and do not collapse draft, established, repealed, or paused plans.
- Search/export request bodies support more UI filters, but use only fields verified from the live application; use `otsistring` unless another exact filter contract has been checked (probed 2026-07: an `orgId` body filter is silently ignored).
- Document links may be PDF, ASiC-E, or another original file type.
- The national register cannot answer Tallinn public-display questions. `planeering/otsing` has no working organizing-authority filter (`{"orgId":784}` returns the same unfiltered `totalElements` as an empty body — silently ignored), and `planseis`/`planseisNimi` only ever takes coarse post-establishment values (`broneeritud`, `kehtiv`, `osaliselt kehtiv`, `osaliselt peatunud`, `kehtetu`) — there is no in-process "avalik väljapanek" value and the detail response exposes only milestone dates, no display-window start/end. For live Tallinn public displays and freshly initiated plans, use the Tallinn register below instead.

## Tallinn: Tallinna planeeringute register (tpr.tallinn.ee)

Tallinn's own register gets new detail plans first, and — unlike the national register — it exposes the in-process public-display window that is the citizen's objection window. The SPA lives at `https://tpr.tallinn.ee/`; its backend under `https://tpr.tallinn.ee/api/*` answers **anonymously today** on the read endpoints below (only the edit/menetlus routes are Bearer-gated). Verified live 2026-07-24.

Caveat: these endpoints are `withCredentials`-flagged in the SPA but currently respond without any token or cookie. If they start returning HTTP 401 `WWW-Authenticate: Bearer`, the anonymous access has been closed — re-verify and fall back to citing `https://tpr.tallinn.ee/` as a pointer rather than inventing data.

Anonymous read endpoints:

- `GET https://tpr.tallinn.ee/api/avalikustamine/avaleht` — JSON array of current & upcoming public displays / discussions (front-page "avalikustamised"). This is the direct answer to "what is on public display in Tallinn right now." Each row:
  - `avLiikNimetus` — `Avalik väljapanek` / `Eskiislahenduse avalik väljapanek` / `Avalik arutelu`.
  - `staatus` — `TOIMUB` (ongoing) or `TULEMAS` (upcoming).
  - `alustamiseAeg` / `lopetamiseAeg` — display window = the citizen objection window (`lopetamiseAeg` is null for `Avalik arutelu` rows, which are single meetings).
  - `toimumiskoht`, `linnaosa`, `planLiikNimetus`, `planKood`, `planNimetus`.
- `POST https://tpr.tallinn.ee/api/detailplaneering/otsi?page=0&size=25` with a JSON body — Spring page of detail plans (`content`, `size`, `totalElements`, `totalPages`, `number`). Rows carry `planKood`, `planNimetus`, `seisund`, `seisundNimetus`, `seisundiKp`, `linnaosa`. Body contract fields: `isKiirotsing`, `searchText`, `locationText`, `personText`, `personId`, `archiveNumber`, `statusCode`, `startDate`, `endDate`, `tagAktiivesMenetluses`, `tagKehtivPlaneering`, `tagYldMuutev`, `tagTapsustavPt`, `tagKhsKoostamine`, `sortKey`, `sortDirection`. Empty `{}` returns everything (~4589 rows); `statusCode` filters to one process stage; `locationText` matches streets/districts; `sortKey: "seisundiKp"` + `sortDirection: "desc"` surfaces the most recent stage changes first.
- `GET https://tpr.tallinn.ee/api/classifiers/menseisund/dp/menetluses` — the `statusCode` vocabulary (detail plans in process): `3203` Algatamisel, `3208` Eskiis avalikustamisel, `3211` Koostamisel, `3221` Avalikustamisel, `3226` Kehtestamisel, `3231` Kehtetuks tunnistamisel.
- Supporting: `GET https://tpr.tallinn.ee/api/planeering/kiirotsing?searchText=X` (quick text search), `GET https://tpr.tallinn.ee/api/detailplaneering/linnaosad/valikud` (district picklist), `GET https://tpr.tallinn.ee/api/config`.

Grounding rule: state plan names, `planKood`s, addresses, and display-window dates ONLY when they appear in output you actually printed from these endpoints — never from memory or inference. If a fetch fails, say so and link the register; do not fabricate a plausible-looking listing.

### Weak-model workflow: worked run_code script (added 2026-07-24, issue #17)

Answers "Millised detailplaneeringud on Tallinnas praegu avalikul väljapanekul või hiljuti algatatud?" in two requests. The `get` helper takes a second `init` argument, so POST is `get(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })`.

```js
import { get, show, save, sleep } from "./kratt.mjs";

async function getRetry(url, init) {
  try {
    return await get(url, init);
  } catch (e) {
    if (!String(e).includes("429")) throw e;
    await sleep(2000);
    return await get(url, init); // one retry, then let it throw
  }
}

// 1) Current + upcoming public displays (the citizen objection windows).
const av = await getRetry("https://tpr.tallinn.ee/api/avalikustamine/avaleht");
const displays = av
  .filter(r => r.planLiikNimetus === "Detailplaneering")
  .map(r => ({
    plan: r.planNimetus,
    kood: r.planKood,
    liik: r.avLiikNimetus,
    staatus: r.staatus, // TOIMUB / TULEMAS
    algus: r.alustamiseAeg?.slice(0, 10),
    lopp: r.lopetamiseAeg?.slice(0, 10) ?? null, // null for Avalik arutelu
    linnaosa: r.linnaosa,
    koht: r.toimumiskoht,
  }));

// 2) Recently initiated plans (statusCode 3203 = Algatamisel), newest first.
const page = await getRetry(
  "https://tpr.tallinn.ee/api/detailplaneering/otsi?page=0&size=25",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      isKiirotsing: false,
      statusCode: 3203,
      sortKey: "seisundiKp",
      sortDirection: "desc",
    }),
  },
);
const initiated = (page.content ?? []).map(r => ({
  plan: r.planNimetus,
  kood: r.planKood,
  seisund: r.seisundNimetus, // "Algatamisel"
  kuupaev: r.seisundiKp,
  linnaosa: r.linnaosa,
}));

await save("tallinn_dp.json", { displays, initiated }); // later calls can load() instead of refetching
show({ avalikulValjapanekul: displays, hiljutiAlgatatud: initiated }, 3500);
```

## Verify

Require a paged JSON response, ensure detail `sysid` matches the selected search record, and accept documents only when `filePublicUrl` is present.
