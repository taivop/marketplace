---
name: government-session-agendas
description: Query Estonia's government-site search JSON for cabinet session agendas, agenda items, presenters, draft types, summaries, and publication dates.
---

# Government Session Agendas

## Access

- Search page: `https://valitsus.ee/otsing?filters%5Btype%5D=Uudis&filters%5Bkeyword%5D=Istungi%20p%C3%A4evakord&sort=created&page=1`
- Search API: `GET https://search.service.eu-live.vportal.ee/v1/search/valitsus`
- Public JSON; send `Origin: https://valitsus.ee` and a `https://valitsus.ee/` referer.

## Retrieve

Use API parameters:

- `query=Istungi päevakord`
- `filters[type]=Uudis`
- `sort_by=created`
- `page=1` (one-based), `limit=10`
- `langcode=et`
- `timezone=Europe/Tallinn`

Read `response.numFound`, `response.start`, and `response.docs`. Each result includes `title`, `uri`, `created`, `lead_text`, content fragments, content type, language, and highlighted matches. Resolve `uri` against `https://valitsus.ee` and fetch the article for the complete ordered agenda.

Agenda articles identify numbered items, presenter (`Esitaja`), type (`Tüüp`), and explanatory summary. Keep post-session `Istung läbi` announcements separate from pre-session `kommenteeritud päevakord` records.

## Return

- Return session date, publication timestamp, agenda status, item number/title, presenter, draft type, summary, article URL, and retrieval time.
- Preserve the article's warning when an agenda is unconfirmed and may change.
- Link adopted legal acts through `legal-acts-data` instead of treating the agenda summary as final law.

## Limits

- The search API is full-text search, so query results include related post-session communications.
- Search result content can be truncated; use the article page for complete agenda items.
- The keyword taxonomy count is not a count of distinct cabinet sessions.

## Verify

- Require HTTP 200 JSON with positive `numFound` and nonempty `docs` for the documented query.
- Require at least one result title containing `istungi` and `päevakord`, with `uri`, `created`, and content fields.
