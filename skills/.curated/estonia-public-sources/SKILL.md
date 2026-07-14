---
name: estonia-government-public-sources
description: "Route Estonian public-data questions to documented official APIs, downloads, and reproducible public web interfaces. Use for Estonian statistics, legislation, parliament, registries, public finance, procurement, environment, health, transport, municipal records, and other official data retrieval."
metadata:
  distribution:
    tier: curated
    publish_anthropic: true
    plugin_name: estonia-public-sources
    plugin_version: 1.3.0
    plugin_author: Taivo Marketplace
---

# Estonia Government Public Sources

## Workflow

1. Search `SOURCE_MAP.md` using the user's topic, institution, dataset, or Estonian term.
2. Select the narrowest matching source and open its `sources/<name>/SKILL.md` recipe.
3. Use the recipe's exact API, download, or browser workflow. Do not repeat general web discovery unless the catalog has no match.
4. Verify that the response contains the documented records, not merely an HTTP success page.
5. If the recipe is broken or the useful records require authentication, say so explicitly and do not claim that the source was queried.

Use `sources/open-data` only as the fallback for vague topics or topics absent from `SOURCE_MAP.md`.

## Retrieval rules

- Prefer `curl`/`wget` on direct URLs over browser navigation.
- If the source has an API, use it directly.
- Only fall back to browser/UI when the data is truly UI-only.
- Treat login, CAPTCHA, and role-restricted systems as unavailable unless the recipe documents a separate public-data path.
- Keep exact request URLs, parameters, table IDs, filters, and retrieval times in the result.

## Output requirements

- Cite exact source URL where data was retrieved.
- Include retrieval timestamp.
- Preserve original field names, units, and identifiers from the source.
- Separate facts from interpretation.
