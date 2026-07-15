---
name: mfa-sanctions
description: Retrieve Estonia-specific sanctions regulations and official subject-list links from the Ministry of Foreign Affairs sanctions page.
---

# MFA Sanctions

## Use when
- You need Estonia-specific sanctions regulations or the MFA's official regime-specific subject-list routes.

## Avoid when
- You need only EU or UN consolidated sanctions lists without Estonia-specific implementation context.

## Endpoint
- MFA index: https://www.vm.ee/en/activity/international-sanctions/sanctions-government-republic-estonia

## Workflow
1. Parse anchors in the main content area.
2. Keep direct `riigiteataja.ee/akt/` regulation links and MFA links whose labels identify a subject list.
3. Resolve relative MFA links against the index URL and preserve the anchor label as the regime/list title.
4. Fetch Riigi Teataja records with the legal-acts recipe when full text or validity metadata is needed.

## Access reality
- Public server-rendered HTML, verified 2026-07-14.
- No working public data API is documented. The portal's configured backend returns `null` without undocumented context and is intentionally not part of this recipe.

## Output schema expectations
- Keep `source_type` (`regulation` or `subject_list`), `source_url`, `regime`, `record_title`, and `retrieved_at`.

## Limits and caveats
- Sanctions content changes frequently; always capture retrieval date.
- Linked subject-list pages are JavaScript-backed and may render no rows to a raw client. Do not claim a complete person/entity list unless rows were actually returned.
- The MFA page is an Estonia-specific index, not a substitute for the EU sanctions map or consolidated EU/UN lists.

## Verification hooks
- Require HTML plus at least one direct Riigi Teataja act link and one MFA subject-list link.
- Cite the regulation URL for legal claims and state explicitly when a linked subject list could not be enumerated.
