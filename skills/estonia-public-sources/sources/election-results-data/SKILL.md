---
name: election-results-data
description: Download official Estonian election-result XML archives and retrieve National Electoral Committee decisions.
---

# Election Results and Decisions

## Access

Public ZIP/XML election snapshots and public decision pages. No authentication. Use a normal user agent if Cloudflare blocks a generic client.

## Endpoints

- Election files: https://www.valimised.ee/en/archive/open-data-estonian-elections
- Archive navigation: https://www.valimised.ee/et/toimunud-valimiste-arhiiv
- VVK decisions: https://www.valimised.ee/et/korraldajad/vabariigi-valimiskomisjon/otsused
- Riigi Teataja VVK search: https://www.riigiteataja.ee/algteksti_tulemused.html?doli=otsus&valj1=Vabariigi+Valimiskomisjon&kuvaKoik=true&sorteeri=kuupaev&kasvav=false

## Retrieve

1. Select election type/year from the open-data page and resolve the relative ZIP link against `https://www.valimised.ee`.
2. Download and inspect the archive before parsing its XML files.
3. Record election type, year, geography level/code, file name, and result declaration context.
4. For VVK decisions, parse title/date/link from the official list and cross-reference the Riigi Teataja result when legal publication matters.

Known archive: `https://www.valimised.ee/sites/default/files/uploads/misc/RK2019_election_result_data.zip`.

The ZIP pattern does not exist for 2023+ elections (`RK2023_election_result_data.zip` returns 404). For elections from 2021 on, use the year-specific result site's JSON API (verified 2026-07-24): `https://<code><year>.valimised.ee/resources/<page-type>/data.json`, e.g. `https://rk2023.valimised.ee/resources/election-result/data.json` for party-level results. `GET /resources/metadata.json` on the same host identifies the election (`electionCode`, `electionType`, `electionYear`) — confirmed for `rk2023`, `ep2024`, and `kov2025`.

## Return

Keep dataset type (`results` or `vvk_decisions`), election type/year, geography and candidate/list identifiers, vote/result fields, decision title/date, direct record URL, legal reference, archive member name, and retrieval time.

## Limits

- Result archives are published after declaration and are not real-time feeds.
- XML schemas and territorial units differ between election years.
- Keep decisions separate from numerical election results.

## Verify

Require a valid ZIP and XML members matching the selected election. The RK2019 archive contains `RK2019_ELECTION_RESULT_*.xml` plus county and parish result files. Reject HTML error pages even if the requested filename ends in `.zip`. For the JSON API, require valid JSON whose `metadata.json` election code matches the requested election before reporting results.
