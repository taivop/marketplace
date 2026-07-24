---
name: riigikogu-open-data
description: Query the Riigikogu open data API for draft laws, votes, members, agendas, stenograms, and legislative activity.
---

# Riigikogu Open Data API

## Use when
- You need draft laws, parliamentary votes, members, plenary agendas, or stenograms.
- You need machine-readable legislative activity from the Riigikogu API.

## Avoid when
- You need election outcomes (use election archive skill).

## Primary endpoints
- OpenAPI contract: https://api.riigikogu.ee/v3/api-docs
- Draft search: `https://api.riigikogu.ee/api/volumes/drafts?initiatedStartDate=2026-01-01&initiatedEndDate=2026-01-31&lang=EN&page=0&size=20`
- Draft detail: `https://api.riigikogu.ee/api/volumes/drafts/{uuid}?lang=EN&querySteno=false`
- Votes: `https://api.riigikogu.ee/api/votings?startDate=2025-01-01&endDate=2025-01-31&lang=EN`
- One member's votes (with each decision inline): `https://api.riigikogu.ee/api/votings/plenary-member/{memberUuid}?startDate=2026-05-01&endDate=2026-06-30&lang=ET&size=100&page=0`
- Plenary agendas: `https://api.riigikogu.ee/api/agenda/plenary?startDate=2025-01-01&endDate=2025-01-31&lang=EN`
- Stenograms: `https://api.riigikogu.ee/api/steno/verbatims?startDate=2025-01-01&endDate=2025-01-31`
- Public calendar fallback: https://www.riigikogu.ee/tegevus/kalender/
- Public stenogram fallback: https://www.riigikogu.ee/tegevus/stenogrammid/

## Workflow
1. Choose the endpoint family from the OpenAPI contract.
2. Query a bounded date range using ISO dates. For a known draft, use `reference`, `mark`, or `title` instead.
3. Preserve UUIDs, draft marks, stages, timestamps, sitting metadata, speaker names, and vote values as returned.
4. Follow UUID detail, document, or file endpoints only when the requested record needs them.
5. Return the exact endpoint and query parameters with the extracted records.

## Access reality
- Public access type: API or structured endpoint access.
- Verified 2026-07-14 against OpenAPI version `2.21.8`.
- The January 2025 plenary-agenda example returns `weekStartDate`, `weekEndDate`, `title`, and a non-empty `sittings` array.
- The January 2026 draft example returns a HAL page under `_embedded.content`; each result has a UUID, title, draft mark, type, stage, status, and initiation date.
- The service may return HTTP 429 for rapid consecutive requests; query serially and back off before retrying.

## Request contract
- `startDate` and `endDate` use `yyyy-MM-dd`.
- Both dates are required for `/api/votings` and `/api/steno/verbatims`; they are optional for `/api/agenda/plenary`.
- Draft search accepts `title`, `reference`, `mark`, `membership`, `draftTypeCode`, `proceedingStatus`, `activeDraftStage`, initiator or committee UUIDs, initiation/amendment date bounds, `page`, `size`, and `sort`.
- `draftTypeCode` accepts `UA`, `DE`, `PE`, `AE`, `TK`, `SE`, or `OE`. Use the OpenAPI classifiers rather than translating these values.
- `lang` accepts `ET`, `RU`, or `EN` and defaults to `ET` where supported.
- Stenogram `type` accepts `IS` (sitting), `IT` (question time), or `IK` (committee sitting).
- Responses are JSON. No authentication is documented for these endpoints.

## Output schema expectations
- Keep the record UUID, draft mark/type/stage/status, date/time, sitting or agenda identifiers, titles/topics, member or speaker identifiers, and vote/speech fields present in the selected response.
- Preserve original field names and classifier values.

## Limits and caveats
- Use the public calendar or stenogram pages only when the API omits content needed by the user.
- Do not infer that a scheduled agenda item was completed; join to votes, stenograms, or documents when outcomes matter.

## Verification hooks
- Confirm `Content-Type: application/json` and parse the response before reporting success.
- For the agenda example, require each sitting to contain `uuid`, `sittingDateTime`, and `agendaItems`.
- Confirm returned dates overlap the requested window.
- Treat HTTP 429 as rate limiting, not evidence that the endpoint is unavailable.

## Weak-model workflow notes (added 2026-07-24, issue #8; member-votings rewrite issue #15)

- The API rate-limits aggressively: on HTTP 429 or an HTML error page, back off and retry the SAME request before changing approach.
- **Voting history for one member: use `/api/votings/plenary-member/{memberUuid}`.** It returns that member's votings paged, each row already carrying the member's `decision` (poolt/vastu/erapooletu/ei hääletanud/puudub) plus the `relatedDraft` title and mark. This means **no per-voting `/api/votings/{uuid}` detail fetch** — the old N+1 fan-out was what spiralled into 429s. The whole answer is 2–3 requests total: one `/api/plenary-members` list to resolve the UUID by name, then one page (100 votings) — a second page only if the window has 100+ votings.
- Notes on this endpoint: it ignores `sort`, returning votings oldest→newest; page with a hard cap and, when truncating, keep the LAST pages (most recent votings). `_embedded.content` holds the rows; `page.totalPages`/`page.totalElements` drive paging. `type.value === "Kohaloleku kontroll"` rows are presence checks, not substantive votes.
- Keep a single 429-retry budget for the whole run so a rate-limited run degrades to a partial answer (with an explicit "(osaline — API piiras päringute arvu)" note) instead of retrying to the step cap. `save()` intermediate pages so a later run_code call can `load()` instead of refetching.

```js
import { get, show, save, load, sleep } from "./kratt.mjs";

// One shared 429-retry budget for the whole run. When it's spent, stop retrying
// and answer from what we already have — never spiral to the step cap (issue #15).
let retryBudget = 5;
async function getBudgeted(url) {
  let delay = 1500;
  for (;;) {
    try {
      return await get(url);
    } catch (e) {
      if (!String(e).includes("429") || retryBudget <= 0) throw e;
      retryBudget--;
      await sleep(delay);
      delay = Math.min(delay * 2, 12000); // adaptive backoff
    }
  }
}

const NAME = "Ees Nimi";
const startDate = "2026-05-24", endDate = "2026-07-24";

// 1) Resolve the member UUID by name — one request. The list is ~400 KB but a
//    single fetch; filter in code, never print it whole.
const members = await getBudgeted("https://api.riigikogu.ee/api/plenary-members?lang=ET");
const member = members.find((m) => m.fullName === NAME);
if (!member) throw new Error("member not found: " + NAME);

// 2) Fetch the member's OWN voting history directly — decisions are inline, so
//    there is NO per-voting detail fetch. Page with a hard cap; the API returns
//    votings oldest→newest and ignores `sort`, so when the cap truncates we keep
//    the LAST pages (most recent votings).
const base = "https://api.riigikogu.ee/api/votings/plenary-member/" + member.uuid;
const pageUrl = (p) => `${base}?startDate=${startDate}&endDate=${endDate}&lang=ET&size=100&page=${p}`;
const MAX_PAGES = 3; // hard cap: up to 300 votings, ample for "last couple months"

const first = await getBudgeted(pageUrl(0));
const totalPages = first?.page?.totalPages ?? 1;
let wanted = Array.from({ length: totalPages }, (_, i) => i);
let truncated = false;
if (wanted.length > MAX_PAGES) { wanted = wanted.slice(-MAX_PAGES); truncated = true; }

const byPage = { 0: first };
for (const p of wanted) {
  if (byPage[p]) continue;
  try { byPage[p] = await getBudgeted(pageUrl(p)); }
  catch { truncated = true; break; } // rate-limited out — keep what we have
}

const rows = [];
for (const p of wanted) {
  for (const v of byPage[p]?._embedded?.content ?? []) {
    rows.push({
      date: v.startDateTime?.slice(0, 10),
      type: v.type?.value,
      decision: v.decision?.value,
      title: v.description,
      draft: v.relatedDraft ? `${v.relatedDraft.title} (${v.relatedDraft.mark})` : null,
    });
  }
}
rows.reverse(); // newest first for display

await save("member_votings.json", { member: member.fullName, startDate, endDate, truncated, rows });

// Presence checks ("Kohaloleku kontroll") are noise; substantive votes are the answer.
const substantive = rows.filter((r) => r.type !== "Kohaloleku kontroll");
show({ member: member.fullName, window: [startDate, endDate], total: rows.length, substantive: substantive.length, truncated }, 400);
show(substantive.slice(0, 25));
// If truncated is true, tell the user the answer is partial (oldest votes omitted).
```
