---
name: estonian-newspaper-archive
description: Search and retrieve material from Estonia's digitized newspaper archive DEA/DIGAR (dea.digar.ee), including full-text results, OCR text, document clipping images, and full-issue PDFs. Use when researching historical Estonian newspapers, locating archived articles, or verifying information against digitized newspaper sources.
metadata:
  distribution:
    tier: curated
    publish_anthropic: true
    plugin_name: estonian-newspaper-archive
    plugin_version: 0.1.0
    plugin_author: Taivo Marketplace
---

# Estonian newspaper archive (DEA / DIGAR)

Base: `https://dea.digar.ee/` (Veridian). Be polite: ~1 s between requests, honest User-Agent.

## Endpoints

```bash
# 1. Search (25 hits/page; r=26 for page 2; quoted phrases work; year range optional)
curl "https://dea.digar.ee/?a=q&hs=1&r=1&results=1&txq=<url_encoded_query>&txf=txIN&ssnip=txt&dafyq=<start_year>&datyq=<end_year>"
# hit doc_ids are in: href="/?a=d&d=<doc_id>&srpos=..."

# 2. OCR text of one document (strip tags to read)
curl "https://dea.digar.ee/?a=d&d=<doc_id>&f=XML"

# 3. Clipping image of the document (~100 KB JPEG; best for reading/verifying)
curl "https://dea.digar.ee/?a=is&oid=<doc_id>&type=blockimage&area=1&width=1400"

# 4. Whole issue PDF (10–30 MB); issue_id = doc_id prefix before the first dot
curl -L "https://dea.digar.ee/?a=is&oid=<issue_id>&type=staticpdf"
```

Human-readable page for citing: `https://dea.digar.ee/?a=d&d=<doc_id>`

## doc_id carries metadata — use it before fetching

`virumaateataja20150526.2.6.1` = title + date (YYYYMMDD) + node path. So the
search hit list alone gives you dated, sourced results. Nodes `.2.N…` are
articles; **`.1.N` are whole-page nodes** — their block images are useless
header fragments, use the DEA page or issue PDF for those.

## Traps

- **Restricted documents**: XML containing `piiratud` is searchable, but its
  text and images may be unavailable outside authorized networks. Detect and
  report the restriction; do not claim to have retrieved blocked content.
- **OCR structure**: flattened XML may include navigation document IDs. Remove
  tokens matching `[a-z]+\d{8}[\d.]*` before parsing extracted data. OCR can
  scramble page structure, so verify important quotations, names, dates, and
  numbers against the clipping image or issue PDF.
- **Block areas**: area 1 is often just the headline; try areas 1–3 (non-image
  or tiny response = no more areas).
