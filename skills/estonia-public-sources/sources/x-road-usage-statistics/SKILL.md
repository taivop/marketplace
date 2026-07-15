---
name: x-road-usage-statistics
description: Download current and historical X-Road environment counts for members, member classes, subsystems, and security servers from the official statistics JSON files.
---

# X-Road Usage Statistics

## Access

- Dashboard: `https://x-tee.ee/stats/`
- Current production snapshot: `https://x-tee.ee/stats/EE/environmentData.json`
- Production history: `https://x-tee.ee/stats/EE/history.json`
- Public static JSON; no login is required.

## Retrieve

Fetch `environmentData.json` for the current snapshot. It contains:

- `instanceIdentifier` and data `date`
- `members`, `subsystems`, and `securityServers`
- `memberClasses`, with `memberClass` and `memberCount`

Fetch `history.json` for periodic snapshots with the same totals and member-class breakdown. Development and test environments use sibling `ee-dev/` and `ee-test/` paths; use `EE/` for production.

## Return

- Return one row per snapshot date and environment with all three totals.
- Keep member-class counts as a child table or expand `COM`, `GOV`, `NGO`, and `NEE` into explicit columns.
- Include the JSON URL and retrieval time; use the payload's `date` as the observation date.

## Limits

- These datasets count infrastructure and participants, not X-Road requests or transaction volume.
- History frequency is determined by the publisher and may not be daily.
- The old `/facts-and-figures/` URL now redirects to the X-Road self-service homepage and is not a data source.

## Verify

- Require the current endpoint to return an `EE` JSON object with a parseable date and positive integer totals.
- Require history to be a nonempty chronological JSON array with the same metric keys.
