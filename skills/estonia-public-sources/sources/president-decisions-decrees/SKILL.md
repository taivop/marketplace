---
name: president-decisions-decrees
description: Retrieve Estonian presidential decisions from the Office of the President's public JSON endpoint, including dates, titles, full text, and record paths.
---

# President Decisions and Decrees

## Use when
- You need presidential decisions on appointments, promulgation, decorations, or other constitutional duties.
- You need chronologically traceable official decision text.

## Avoid when
- You need draft laws or parliamentary proceedings; use `riigikogu-open-data`.

## Endpoints
- Complete Estonian JSON list: `https://p.president.ee/et/entity/block/decisions_list?_format=json`
- Public listing: https://president.ee/et/ametitegevus/otsused/

## Workflow
1. Fetch the JSON list once and filter `field_date` locally for the requested date range.
2. Match keywords against `title` and the HTML in `body`.
3. Strip HTML only for analysis; retain the original body when exact text matters.
4. Build the public record URL from the listing origin and `view_node`, inserting `/ametitegevus/otsused` after the language prefix when needed.

## Access reality
- Public unauthenticated JSON, verified 2026-07-14.
- The complete Estonian response was under 1 MB and returned hundreds of records. It is an array, not a paginated object.
- Use the `p.president.ee` data host exactly. `www.president.ee` redirects obsolete paths to the homepage; the canonical public site omits `www`.

## Output schema expectations
- Preserve `nid`, `title`, `field_date`, `body`, `field_head_of_state`, and `view_node`, plus the retrieval timestamp and constructed public URL.

## Limits and caveats
- `body` contains HTML and may be empty for some records.
- The English endpoint has less complete coverage; use Estonian for exhaustive retrieval and translate only the requested output.
- Decision type is not a separate field. Infer it only when the title or text makes the category explicit.

## Verification hooks
- Require `application/json`, a non-empty array, and `nid`, `title`, `field_date`, and `view_node` on selected records.
- Confirm dates are ISO `YYYY-MM-DD` before applying range filters.
