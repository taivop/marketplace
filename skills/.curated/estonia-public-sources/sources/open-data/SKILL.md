---
name: open-data
description: Discover Estonian public datasets through the national data portal RSS catalog when no source-specific recipe is known.
---

# National Open Data Discovery

## Access

Public RSS catalog at `https://andmed.eesti.ee/api/rss/feed`. The interactive portal may require a browser or normal user agent, but the RSS feed is directly machine-readable.

## Retrieve

1. Download and parse the RSS feed.
2. Search item `title` and `description` using both Estonian and English terms.
3. Use `link`/`guid` to open the matching dataset page, then capture publisher, update date, license, formats, and direct distributions.
4. Prefer an existing source-specific recipe when the dataset points to a known API or registry.

RSS items contain `title`, `description`, `link`, `guid`, and `pubDate`. The feed contained 2,831 items in the 2026-07-14 verification run.

## Return

Return a short ranked list with dataset title, owner, dataset-page URL, update date, description, license, format/access method, direct data URL, and recommended next recipe. Do not return the whole catalog.

## Limits

- RSS describes dataset updates; it does not expose every portal facet or all distribution metadata.
- A dataset page can describe a source without providing a working distribution. Verify the final API/file separately.
- Use this only as fallback discovery, not as a substitute for a known acquisition recipe.

## Verify

Require HTTP 200 `application/rss+xml`, root `rss`, a `channel`, and non-empty `item` elements containing title, link, and publication date. Verify the selected dataset's final distribution before claiming data access.
