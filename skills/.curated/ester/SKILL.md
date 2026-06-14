---
name: ester
description: Searches the Estonian library catalog ESTER (ester.ee) to find books, check availability, and locate them in specific library branches. USE WHEN user asks to find a book in Estonian libraries, check if a book is available, find where to pick up a library book, search ESTER, or mentions Estonian library branches like Kalamaja, Keskraamatukogu, Tartu, etc.
metadata:
  distribution:
    tier: curated
    publish_anthropic: true
    plugin_name: ester
    plugin_version: 0.1.0
    plugin_author: Taivo Marketplace
---


# ESTER Library Catalog Search

Search the Estonian unified library catalog (ESTER) to find books and check their availability at specific branches. No public API — uses curl + HTML parsing.

**Parser scripts are in this skill directory** (relative to SKILL.md).

## Workflow

### 1. Search for books

```bash
curl -s "https://www.ester.ee/search~S1*est/X?searchtype=X&searcharg=QUERY&searchscope=SCOPE&SORT=DZ&extended=0&SUBMIT=OTSI" \
  | python3 SKILL_DIR/parse_search.py
```

Replace `QUERY` with URL-encoded search terms (ä=`%C3%A4`, ö=`%C3%B6`, ü=`%C3%BC`, õ=`%C3%B5`, spaces=`+`).

**Search types** (replace `X` in both URL path and `searchtype=`):

| Code | Field |
|------|-------|
| `X` | Keyword (all fields) — default |
| `i` | ISBN/ISSN |

Use keyword (`X`) for title and author queries too — it handles them well. Do **not** use `searchtype=t` (title) or `searchtype=a` (author): ESTER returns a browse-heading index page for those, not a results list, and the parser will report 0 results even when matches exist.

**searchscope values:**

| Scope | Library |
|-------|---------|
| 1 | All libraries (default) |
| 7 | Eesti Rahvusraamatukogu (National Library) |
| 8 | Tallinna Raamatukogud / TlnRK (all Tallinn public library branches) |
| 15 | TLÜ Akadeemiline Raamatukogu |
| 55 | Tartu Linnaraamatukogu |
| 58 | Tartu Ülikooli raamatukogud |

**Output:** JSON with `total` count and `results` array of `{id, title}`. If an ISBN search redirects directly to a record page, output includes `"direct_record": true`.

**Pagination:** 50 results per page. Add `&startnum=51` for page 2.

### 2. Get holdings for a book

**Step 1** — Fetch the record page and check for truncation:

```bash
curl -s "https://www.ester.ee/record=b{RECORD_ID}~S1*est" \
  | python3 SKILL_DIR/parse_record.py
```

**Step 2** — If output contains `"truncated": true`, fetch the full holdings using the `full_holdings_url` from the output:

```bash
curl -s "FULL_HOLDINGS_URL" \
  | python3 SKILL_DIR/parse_record.py
```

The record page only shows the first 10 holdings. **Always check for truncation** — popular books often have 30-50+ copies across branches.

**Output:** JSON with `title`, `author`, `published`, `isbn`, `holdings` array of `{location, call_number, status, notes}`, and optionally `truncated`/`full_holdings_url`.

**Status values:**
- `KOHAL` — available on shelf
- `TÄHTAEG DD.MM.YY` — checked out, due date
- `TÖÖTLUSES` — being processed, not yet available
- `KOHALKASUTUS` — in-library use only
- `ARHIIVEKSEMPLAR` — archive copy
- `EI LAENUTATA` — non-circulating
- `REMONDI AJAKS PAKITUD` — packed away during renovation
- `+N JÄRJEKORRAS` — N people in queue (appended to due date)

### 3. Present results

For each book, show:
- Title, author, year
- Holdings filtered to user's preferred branch(es), with status and call number
- ESTER link: `https://www.ester.ee/record=b{RECORD_ID}~S1*est`

For multiple books, show a summary table of availability per branch.

## Tallinn public library branches (TlnRK)

| User says | ESTER location contains |
|-----------|------------------------|
| Kalamaja | TlnRK Kalamaja |
| Keskraamatukogu / main | TlnRK Keskraamatukogu |
| Südalinn / city center | TlnRK Südalinna |
| Liivalaia | TlnRK Liivalaia |
| Pelgulinn / Pelguranna | TlnRK Pelguranna |
| Nõmme | TlnRK Nõmme |
| Mustamäe | TlnRK Mustamäe |
| Õismäe | TlnRK Väike-Õismäe |
| Pirita | TlnRK Pirita |
| Kadriorg | TlnRK Kadrioru |
| Pääsküla | TlnRK Pääsküla |

Children's sections are listed separately with "lastekirjandus" suffix. Children's books have call numbers starting with `L-`.

## Extra metadata (age group, description, price)

For info not in ESTER (age group, description, price, series), use `WebSearch` for the book title + author with `allowed_domains: ["rahvaraamat.ee", "apollo.ee"]`. Use title + author, not ISBN — ISBN search is unreliable on these stores.

## Tips

- Keyword search (`searchtype=X`) is forgiving with word order — use it for all freetext queries.
- Boolean operators work: AND, OR, NOT.
- For multiple books, batch all searches first, then fetch records for matches.
- `searchscope` filters search results but the record/holdings page always shows ALL libraries' copies. Filter the holdings JSON by location to show only relevant branches.
