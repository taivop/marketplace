---
name: political-party-membership
description: Retrieve current Estonian political-party and member lists from the e-Business Register, including direct CSV exports by registry code.
---

# Political Party Membership

## Use when
- You need the official list of registered political parties.
- You need a party's public current-member list or membership start dates.

## Avoid when
- You need campaign finance; use `party-funding-data`.

## Endpoints
- Party chooser: https://ariregister.rik.ee/eng/political_party
- Member list: `https://ariregister.rik.ee/eng/political_party/members/{registry_code}`
- Direct CSV: `https://ariregister.rik.ee/eng/political_party/members/{registry_code}?download=CSV`
- Historical Power BI statistics: https://ariregister.rik.ee/eng/statistics/political_parties

## Workflow
1. Parse the chooser's party table and take the eight-digit registry code from each `/members/{registry_code}` link.
2. Fetch the CSV directly for each requested party. Decode it as UTF-8 with BOM and parse it with semicolon delimiters.
3. Preserve the party name and registry code from the chooser with every exported row.
4. Use the Power BI page only for historical aggregates not present in the current lists.

## Access reality
- Public HTML and CSV, verified 2026-07-14.
- The chooser exposes party/member links without JavaScript. The tested CSV response is `text/csv` and starts with the five-column member header.

## Request contract
- No authentication or session cookie is required for the chooser or CSV export.
- The CSV columns are `First name`, `Last name`, `Date of birth`, `Date of starting membership`, and `Suspension of membership in political party`.
- HTML member pages paginate with `?page=N`, but the CSV export returns the full list; prefer CSV for data work.

## Output schema expectations
- Keep the registry code, party name, source URL, retrieval time, and original CSV fields.
- For aggregate answers, report the retrieval date because the export is a current snapshot.

## Limits and caveats
- These are personal data published under the Political Parties Act. Retrieve and expose only fields necessary for the request; avoid republishing bulk member data when an aggregate suffices.
- The current CSV is not a historical trend series. Do not infer join/leave history beyond the exported dates.

## Verification hooks
- Require `text/csv`, the expected semicolon-delimited header, and at least one data row.
- Confirm that the registry code used in the export came from the current chooser.
