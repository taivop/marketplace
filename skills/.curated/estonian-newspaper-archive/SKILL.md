---
name: estonian-newspaper-archive
description: Search and extract from Estonia's digitized newspaper archive DEA (dea.digar.ee) — full-text search across ~170 years of papers, OCR text, article clipping images, full-issue PDFs. USE WHEN user asks about old Estonian newspapers or ads, historical mentions/prices of something in print, DIGAR/DEA, or verifying a claim from an old paper.
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
curl "https://dea.digar.ee/?a=q&hs=1&r=1&results=1&txq=%22kirju+koer%22&txf=txIN&ssnip=txt&dafyq=1990&datyq=1999"
# hit doc_ids are in: href="/?a=d&d=<doc_id>&srpos=..."

# 2. OCR text of one document (strip tags to read)
curl "https://dea.digar.ee/?a=d&d=<doc_id>&f=XML"

# 3. Clipping image of the article/ad itself (~100 KB JPEG; best for reading/verifying)
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

- **Restricted documents**: XML contains `piiratud` → searchable but image/
  text blocked outside the library network (typically big commercial titles:
  Õhtuleht, Postimees, Eesti Ekspress, Maaleht; varies by title and period).
  Detect per document and skip — open regional papers carry the same national
  content (incl. the same chain ads).
- **Extracting numbers from OCR text**: the flattened XML embeds navigation
  doc_ids — strip tokens matching `[a-z]+\d{8}[\d.]*` first, or you will
  "extract" numbers from document ids. OCR also scrambles ad-grid layout, so
  a number near a product name often belongs to the neighboring item:
  **always verify against the clipping image (endpoint 3) before asserting.**
- **Block areas**: area 1 is often just the headline; try areas 1–3 (non-image
  or tiny response = no more areas).

## Search strategy notes

- Retail ads print both the promo price and the crossed-out regular price.
- Soviet-era papers (open access) have almost no retail ads — prices appear
  in currency-reform articles, price surveys, and factory advertorials; search
  product + `kop`/`rbl`/`maksab` rather than expecting ad layouts.
