---
name: coloring-book
description: Generate a printable, text-free story coloring book PDF from a story idea, with consistent characters and real-landmark backgrounds. Use when the user asks to create a coloring book, coloring pages, or a wordless picture-story PDF. Requires an OpenAI API key.
metadata:
  distribution:
    tier: curated
    publish_anthropic: true
    plugin_name: coloring-book
    plugin_version: 0.1.0
    plugin_author: Taivo Marketplace
---

# Coloring Book Generator

`pipeline.py` and `spec.example.yaml` live in this skill's directory (treat it as
read-only — it may be an installed plugin). Everything the pipeline writes —
`spec.yaml`, `.env` and the `output/` tree — goes in a separate **work
directory**. Create one for the book (e.g. `~/coloring-book/<title>/`), `cd` into
it, and run the script by its full path from there; the work directory defaults
to the current directory (override with `--workdir PATH` or `$COLORING_BOOK_DIR`).

Drive `pipeline.py` stage by stage. The rule that matters: **inspect each stage's
images with Read before running the next stage** — a bad character sheet poisons
every page built from it. Fix at the earliest stage.

## Setup

- Make a work directory and `cd` into it. Copy the template:
  `cp <skill-dir>/spec.example.yaml spec.yaml`, then edit `spec.yaml`.
- `.env` (in the work directory) with `OPENAI_API_KEY=sk-...` (gitignored; ask if
  missing), or export `OPENAI_API_KEY`. Test the key with one cheap generation
  first — `billing_hard_limit_reached` or `insufficient_quota` mean the user must
  add credits, so stop and say so.
- `pip install -r <skill-dir>/requirements.txt`.

## Workflow

Gather story, characters (or invent), style, audience and page count into
`spec.yaml` (copied from `spec.example.yaml`). Run stages in order from the work
directory (`python3 <skill-dir>/pipeline.py <stage>`), reviewing each before the
next. Paths below (`output/...`) are relative to the work directory:

| Stage | Command | Review before continuing |
|-------|---------|--------------------------|
| 1. Outline | `python3 pipeline.py outline` | Read `output/outline.json`. Story beats visual-only? Character descriptions specific enough to repeat verbatim? Every wanted landmark present (the model drops some — re-add in the JSON)? Add per-page `landmark` fields = exact English Wikipedia article titles. |
| 2. Characters | `python3 pipeline.py characters` | Read each `output/characters/*.png`. Same features across poses? Species right? Fix by tightening the description in outline.json, then `--only NAME`. |
| 3. Landmarks | `python3 pipeline.py landmarks` | Read each `output/landmarks/*.png`. Structure recognizable, proportions right? Aerial/map-style photos anchor badly — drop that page's `landmark` instead. |
| 4. Pages | `python3 pipeline.py pages` (slow — run in background) | Read every page: no text anywhere; correct character count; each character's signature features present; landmark faithful. Redo one page with `--page N`. |
| 5. PDF | `python3 pipeline.py postprocess && python3 pipeline.py pdf` | Deliver `output/book.pdf` with SendUserFile. |

## Fixing pages

Each page uses one landmark sheet + one composite character sheet — don't add
more references, or accessories start migrating between characters. When review
finds a problem, edit that page's `scene` in `output/outline.json` and rerun
`pages --page N`:

- **Place/brand names appear as signage text** despite the no-text rule. Drop
  the proper noun, or add "no name, sign lettering or writing; sign boards
  blank". Ships/vehicles: "plain sides, no lettering, no flags".
- **A character is duplicated or missing** in a group scene. State the exact
  cast: "exactly three dinosaurs, no others".
- **A signature feature vanishes** (e.g. stegosaurus plates). Append
  "IMPORTANT: <name> must clearly show <feature>".
- **Wikipedia gave a bad anchor photo** (trains not the station; aerial not
  façade). Try another article title, drop your own photo into
  `output/landmarks/photos/<slug>.png`, or remove the page's `landmark`.
- **Wikimedia 429s**: wait and rerun; finished sheets are skipped.

## Cost

~$0.07/image at medium quality; a 10-page, 3-character book ≈ $1.50–2 with redos
(~25% of pages need one). Set `image_quality: high` in spec.yaml for print-gift
quality (~2× cost).
