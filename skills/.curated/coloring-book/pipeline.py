#!/usr/bin/env python3
"""Staged pipeline for generating a printable, text-free coloring book PDF.

Stages (each writes reviewable files under output/ before the next runs):

  outline      spec.yaml -> output/outline.json   (story beats + locked character descriptions)
  characters   outline   -> output/characters/*.png  (one reference sheet per character)
  landmarks    outline   -> output/landmarks/*.png (real photo fetched from Wikipedia per
               page "landmark" field, redrawn as a line-art reference sheet)
  pages        outline + landmark sheets + character sheets -> output/pages/page_NN.png
  postprocess  pages -> output/print/page_NN.png  (pure black/white, print-ready)
  pdf          print pages -> output/book.pdf     (300 DPI, letter/A4, margins)
  all          run every stage in order

Usage:
  python3 pipeline.py outline
  python3 pipeline.py characters [--only NAME]
  python3 pipeline.py landmarks [--only NAME]
  python3 pipeline.py pages [--page N]
  python3 pipeline.py postprocess
  python3 pipeline.py pdf
  python3 pipeline.py all

Add --mock to any stage to run without the OpenAI API (placeholder art) so the
mechanics and PDF layout can be verified for free.

Files are read from and written to a *work directory* (spec.yaml, .env and the
output/ tree), which is separate from this script's own (possibly read-only)
install location. The work directory is, in order of precedence:
  1. --workdir PATH
  2. the COLORING_BOOK_DIR environment variable
  3. the current working directory (default)
The bundled spec.example.yaml lives next to this script; copy it into the work
directory as spec.yaml and edit it there.

The OpenAI key is read from the OPENAI_API_KEY environment variable, or from a
.env file in the work directory containing OPENAI_API_KEY=...  (never committed).
"""

import argparse
import base64
import io
import json
import math
import random
import sys
from pathlib import Path

import requests
import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Where this script and its bundled read-only template (spec.example.yaml) live.
ROOT = Path(__file__).resolve().parent
# Work directory: where spec.yaml, .env and output/ are read/written. Overridden
# in main() from --workdir / COLORING_BOOK_DIR; defaults to the current directory
# so the pipeline never writes into its (possibly read-only) install location.
WORK = Path.cwd()
OUT = WORK / "output"


def resolve_workdir(cli_workdir=None):
    """Pick the work directory: --workdir, then COLORING_BOOK_DIR, then cwd."""
    import os
    chosen = cli_workdir or os.environ.get("COLORING_BOOK_DIR")
    base = Path(chosen).expanduser() if chosen else Path.cwd()
    return base.resolve()

API = "https://api.openai.com/v1"
WIKI_API = "https://en.wikipedia.org/w/api.php"
# Wikimedia policy: identify the client and give a contact address, or get 429s.
WIKI_UA = {"User-Agent":
           "ColoringBookPipeline/1.0 (personal project; contact: sq42na@gmail.com)"}

# Hard constraints appended to every image prompt regardless of user style.
LINE_ART_RULES = (
    "Style requirements: children's coloring book page. Clean black outlines only, "
    "uniform medium-thick line weight, pure white background, no shading, no gray, "
    "no color fill, no cross-hatching, large simple regions that are easy to color. "
    "Absolutely no text, letters, numbers, captions or watermarks anywhere in the image."
)

PAGE_SIZES = {  # inches (width, height), portrait
    "letter": (8.5, 11.0),
    "a4": (8.27, 11.69),
}


def load_spec():
    path = WORK / "spec.yaml"
    if not path.exists():
        sys.exit(
            f"spec.yaml not found in {WORK}\n"
            f"  copy the template:  cp {ROOT / 'spec.example.yaml'} {path}\n"
            f"  then edit it (or point --workdir at a directory that has one)."
        )
    with open(path) as f:
        return yaml.safe_load(f)


def api_key():
    import os
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        env = WORK / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("No OPENAI_API_KEY in environment or .env file.")
    return key


def api_error(resp):
    try:
        msg = resp.json()["error"]["message"]
    except Exception:
        msg = resp.text[:500]
    sys.exit(f"OpenAI API error ({resp.status_code}): {msg}")


# ---------------------------------------------------------------- outline ---

OUTLINE_SYSTEM = """You are helping plan a wordless coloring book that tells a story
through pictures only. Given a story idea, characters and a page count, return JSON:

{
  "title": "...",
  "characters": [
    {"name": "...",
     "description": "very specific, repeatable visual description: species/age/build,
      face, hair, clothing, accessories, distinguishing features. This exact text is
      reused in every image prompt, so it must fully pin down the character's look."}
  ],
  "pages": [
    {"page": 1,
     "scene": "one self-contained visual moment advancing the story. Name which
      characters appear, their pose/action/emotion, setting and 1-3 background
      elements. Composition must read clearly without any text.",
     "landmark": "optional: if the scene features a real-world place or structure,
      the exact English Wikipedia article title for it (used to fetch a reference
      photo). Omit for interiors or generic settings."}
  ]
}

Rules: the story must be understandable purely visually; each page one clear moment;
keep scenes simple enough for a coloring page (no crowds, no tiny detail); reuse the
characters' names verbatim in the scenes."""


def stage_outline(spec, mock=False):
    OUT.mkdir(exist_ok=True)
    if mock:
        outline = _mock_outline(spec)
    else:
        user_msg = json.dumps({
            "story_idea": spec["story"],
            "characters": spec.get("characters", "invent suitable characters"),
            "page_count": spec.get("pages", 8),
            "audience": spec.get("audience", "children age 4-8"),
        })
        r = requests.post(f"{API}/chat/completions",
            headers={"Authorization": f"Bearer {api_key()}"},
            json={
                "model": spec.get("text_model", "gpt-4o-mini"),
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": OUTLINE_SYSTEM},
                    {"role": "user", "content": user_msg},
                ],
            }, timeout=120)
        if r.status_code != 200:
            api_error(r)
        outline = json.loads(r.json()["choices"][0]["message"]["content"])

    path = OUT / "outline.json"
    path.write_text(json.dumps(outline, indent=2))
    print(f"Wrote {path}")
    print(f"  title: {outline['title']}")
    print(f"  characters: {', '.join(c['name'] for c in outline['characters'])}")
    print(f"  pages: {len(outline['pages'])}")
    print("Review/edit output/outline.json before running the next stage.")


def _mock_outline(spec):
    n = spec.get("pages", 8)
    return {
        "title": "Mock Story (placeholder)",
        "characters": [
            {"name": "Pip", "description": "a small round fox kit with a fluffy "
             "tail, oversized ears, a tiny triangular nose and a striped scarf"},
        ],
        "pages": [{"page": i + 1, "scene": f"Pip in mock scene {i + 1}"} for i in range(n)],
    }


def load_outline():
    path = OUT / "outline.json"
    if not path.exists():
        sys.exit("output/outline.json not found - run the outline stage first.")
    return json.loads(path.read_text())


# ------------------------------------------------------------- characters ---

def stage_characters(spec, mock=False, only=None):
    outline = load_outline()
    cdir = OUT / "characters"
    cdir.mkdir(parents=True, exist_ok=True)
    for ch in outline["characters"]:
        if only and ch["name"].lower() != only.lower():
            continue
        dest = cdir / f"{ch['name'].lower().replace(' ', '_')}.png"
        prompt = (
            f"Character model sheet of {ch['name']}: {ch['description']}. "
            "Show the same character three times on one page: front view, side view, "
            "and a walking pose. Same proportions and features in all three. "
            f"{LINE_ART_RULES} "
            f"Overall style: {spec.get('style', 'simple, friendly cartoon')}."
        )
        if mock:
            _mock_line_art(dest, seed=ch["name"], label_shapes=3)
        else:
            _generate_image(spec, prompt, dest)
        print(f"Wrote {dest}")
    print("Inspect the character sheet(s). Regenerate with --only NAME, or tweak the "
          "description in output/outline.json and rerun, until you like them.")


# -------------------------------------------------------------- landmarks ---

def _slug(name):
    return "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")


def _get_with_retry(url, **kw):
    """GET with backoff for Wikimedia rate limiting (429) and transient errors."""
    import time
    for attempt in range(5):
        r = requests.get(url, headers=WIKI_UA, timeout=120, **kw)
        if r.status_code not in (429, 500, 502, 503):
            r.raise_for_status()
            return r
        time.sleep(5 * 2 ** attempt)
    r.raise_for_status()
    return r


def _fetch_wikipedia_photo(title, dest):
    """Fetch the lead image of a Wikipedia article and save it as PNG."""
    r = _get_with_retry(WIKI_API, params={
        "action": "query", "titles": title, "prop": "pageimages",
        "format": "json", "pithumbsize": 1200, "redirects": 1})
    pages = r.json()["query"]["pages"]
    url = next(iter(pages.values())).get("thumbnail", {}).get("source")
    if not url:
        return False
    img = _get_with_retry(url)
    Image.open(io.BytesIO(img.content)).convert("RGB").save(dest)
    return True


def stage_landmarks(spec, mock=False, only=None):
    """One line-art reference sheet per unique page 'landmark' (a Wikipedia title)."""
    outline = load_outline()
    ldir = OUT / "landmarks"
    photos = ldir / "photos"
    photos.mkdir(parents=True, exist_ok=True)
    names = sorted({pg["landmark"] for pg in outline["pages"] if pg.get("landmark")})
    if not names:
        print("No 'landmark' fields in output/outline.json - nothing to do.")
        return
    for name in names:
        if only and only.lower() not in name.lower():
            continue
        slug = _slug(name)
        sheet = ldir / f"{slug}.png"
        photo = photos / f"{slug}.png"
        if sheet.exists() and not only:
            print(f"Skipping '{name}' (sheet exists; use --only to regenerate)")
            continue
        if mock:
            _mock_line_art(sheet, seed=name, label_shapes=2)
            print(f"Wrote {sheet} (mock)")
            continue
        if not photo.exists():
            import time
            time.sleep(3)  # politeness delay between Wikimedia fetches
            try:
                found = _fetch_wikipedia_photo(name, photo)
            except Exception as e:
                print(f"WARNING: photo fetch failed for '{name}' ({e}); skipping.")
                continue
            if found:
                print(f"Fetched photo for '{name}' -> {photo}")
            else:
                print(f"WARNING: no Wikipedia image found for '{name}'; "
                      f"pages will rely on the text description alone.")
                continue
        prompt = (
            f"The attached image is a photograph of {name}. Redraw it as a coloring "
            "book line-art reference of the structure: keep the real proportions and "
            "the distinctive architectural features accurate while simplifying small "
            "details. Show the structure only - no people, no animals, no vehicles "
            f"unless they are part of the structure itself. {LINE_ART_RULES}"
        )
        _generate_image(spec, prompt, sheet, refs=[photo])
        print(f"Wrote {sheet}")
    print("Inspect the landmark sheets; regenerate one with --only NAME, or drop in "
          "your own photo at output/landmarks/photos/<slug>.png and rerun.")


def _composite_character_sheet():
    """Combine all character sheets into one reference image (fewer refs = less
    identity bleed when a landmark sheet is also attached)."""
    sheets = sorted(p for p in (OUT / "characters").glob("*.png")
                    if not p.name.startswith("_"))
    if not sheets:
        return None
    dest = OUT / "characters" / "_all.png"
    newest = max(p.stat().st_mtime for p in sheets)
    if dest.exists() and dest.stat().st_mtime >= newest:
        return dest
    imgs = [Image.open(p).convert("L") for p in sheets]
    h = min(i.height for i in imgs)
    imgs = [i.resize((int(i.width * h / i.height), h), Image.LANCZOS) for i in imgs]
    combo = Image.new("L", (sum(i.width for i in imgs), h), 255)
    x = 0
    for i in imgs:
        combo.paste(i, (x, 0))
        x += i.width
    combo.save(dest)
    return dest


# ------------------------------------------------------------------ pages ---

def stage_pages(spec, mock=False, page=None):
    outline = load_outline()
    pdir = OUT / "pages"
    pdir.mkdir(parents=True, exist_ok=True)
    char_by_name = {c["name"]: c for c in outline["characters"]}
    for pg in outline["pages"]:
        if page is not None and pg["page"] != page:
            continue
        dest = pdir / f"page_{pg['page']:02d}.png"
        present = [c for c in char_by_name if c.lower() in pg["scene"].lower()]
        descs = "; ".join(
            f"{n} ({char_by_name[n]['description']})" for n in present) or "no named characters"

        refs, ref_notes = [], []
        landmark = pg.get("landmark")
        if landmark:
            sheet = OUT / "landmarks" / f"{_slug(landmark)}.png"
            if sheet.exists():
                refs.append(sheet)
                ref_notes.append(
                    f"Attached image {len(refs)} is a line-art reference of the real "
                    f"{landmark} - reproduce this structure in the scene faithfully, "
                    f"keeping its proportions and distinctive architectural features.")
        combo = _composite_character_sheet()
        if combo and present:
            refs.append(combo)
            ref_notes.append(
                f"Attached image {len(refs)} is the official character model sheet - "
                f"copy the characters' faces, proportions, clothing and accessories "
                f"from it exactly.")

        prompt = (
            f"Coloring book page, one scene from a wordless picture story. Scene: {pg['scene']}. "
            f"Characters must exactly match these locked designs: {descs}. "
            + " ".join(ref_notes) + " "
            + f"{LINE_ART_RULES} Overall style: {spec.get('style', 'simple, friendly cartoon')}."
        )
        if mock:
            _mock_line_art(dest, seed=f"page{pg['page']}", label_shapes=pg["page"])
        else:
            _generate_image(spec, prompt, dest, refs=refs)
        print(f"Wrote {dest}")
    print("Review the page(s); regenerate any single page with: pipeline.py pages --page N")


# --------------------------------------------------------- image back end ---

def _generate_image(spec, prompt, dest, refs=None):
    """Generations endpoint, or edits endpoint when reference images are given."""
    key = api_key()
    model = spec.get("image_model", "gpt-image-1")
    size = spec.get("image_size", "1024x1536")  # portrait
    quality = spec.get("image_quality", "medium")
    if refs:
        files = [("image[]", (p.name, open(p, "rb"), "image/png")) for p in refs]
        data = {"model": model, "prompt": prompt, "size": size, "quality": quality,
                "input_fidelity": "high"}
        r = requests.post(f"{API}/images/edits",
                          headers={"Authorization": f"Bearer {key}"},
                          data=data, files=files, timeout=300)
    else:
        r = requests.post(f"{API}/images/generations",
                          headers={"Authorization": f"Bearer {key}"},
                          json={"model": model, "prompt": prompt, "size": size,
                                "quality": quality, "n": 1}, timeout=300)
    if r.status_code != 200:
        api_error(r)
    b64 = r.json()["data"][0]["b64_json"]
    dest.write_bytes(base64.b64decode(b64))


def _mock_line_art(dest, seed, label_shapes=1):
    """Free placeholder line art so the pipeline and PDF can be tested offline."""
    rng = random.Random(str(seed))
    w, h = 1024, 1536
    img = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, w - 40, h - 40], outline=0, width=8)
    for i in range(3 + label_shapes % 4):
        cx, cy = rng.randint(200, w - 200), rng.randint(220, h - 220)
        r0 = rng.randint(70, 190)
        kind = rng.choice(["circle", "flower", "star"])
        if kind == "circle":
            d.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], outline=0, width=10)
            d.ellipse([cx - r0 // 3, cy - r0 // 3, cx, cy], outline=0, width=8)
        elif kind == "flower":
            for a in range(6):
                ang = a * math.pi / 3
                px, py = cx + int(r0 * math.cos(ang)), cy + int(r0 * math.sin(ang))
                d.ellipse([px - r0 // 2, py - r0 // 2, px + r0 // 2, py + r0 // 2],
                          outline=0, width=8)
            d.ellipse([cx - r0 // 3, cy - r0 // 3, cx + r0 // 3, cy + r0 // 3],
                      outline=0, width=8)
        else:
            pts = []
            for a in range(10):
                rr = r0 if a % 2 == 0 else r0 // 2
                ang = a * math.pi / 5 - math.pi / 2
                pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
            d.polygon(pts, outline=0, width=8)
    img.save(dest)


# ------------------------------------------------------------ postprocess ---

def stage_postprocess(spec):
    src = sorted((OUT / "pages").glob("page_*.png"))
    if not src:
        sys.exit("No pages in output/pages - run the pages stage first.")
    pdir = OUT / "print"
    pdir.mkdir(parents=True, exist_ok=True)
    thresh = int(spec.get("bw_threshold", 200))
    for p in src:
        img = Image.open(p).convert("L")
        img = ImageOps.autocontrast(img)
        img = img.point(lambda v: 255 if v >= thresh else 0, mode="L")
        img.save(pdir / p.name)
        print(f"Wrote {pdir / p.name}")


# -------------------------------------------------------------------- pdf ---

def _number_font(size):
    """A scalable font for page numbers; fall back gracefully across platforms."""
    for path in ("/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/Library/Fonts/Arial.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)  # Pillow >= 10.1 scalable default
    except TypeError:
        return ImageFont.load_default()


def _draw_page_number(sheet, number, pw, ph, margin, dpi):
    """Print a small page number centered in the bottom margin (never over art)."""
    draw = ImageDraw.Draw(sheet)
    font = _number_font(max(16, int(dpi * 0.14)))
    label = str(number)
    l, t, r, b = draw.textbbox((0, 0), label, font=font)
    x = (pw - (r - l)) // 2 - l
    y = ph - int(margin * dpi * 0.5) - (b - t) // 2 - t
    draw.text((x, y), label, fill=0, font=font)


def stage_pdf(spec):
    src = sorted((OUT / "print").glob("page_*.png"))
    if not src:
        sys.exit("No pages in output/print - run the postprocess stage first.")
    dpi = int(spec.get("dpi", 300))
    size_name = spec.get("page_size", "letter")
    if size_name not in PAGE_SIZES:
        sys.exit(f"page_size must be one of {list(PAGE_SIZES)}")
    win, hin = PAGE_SIZES[size_name]
    margin = float(spec.get("margin_inches", 0.5))
    pw, ph = int(win * dpi), int(hin * dpi)
    box_w, box_h = pw - int(2 * margin * dpi), ph - int(2 * margin * dpi)

    page_numbers = bool(spec.get("page_numbers", True))
    sheets = []
    for i, p in enumerate(src, start=1):
        art = Image.open(p).convert("L")
        scale = min(box_w / art.width, box_h / art.height)
        art = art.resize((int(art.width * scale), int(art.height * scale)), Image.LANCZOS)
        # re-threshold after resampling so lines stay pure black on white
        art = art.point(lambda v: 255 if v >= 128 else 0, mode="L")
        sheet = Image.new("L", (pw, ph), 255)
        sheet.paste(art, ((pw - art.width) // 2, (ph - art.height) // 2))
        if page_numbers:
            _draw_page_number(sheet, i, pw, ph, margin, dpi)
        sheets.append(sheet)

    dest = OUT / "book.pdf"
    sheets[0].save(dest, save_all=True, append_images=sheets[1:],
                   resolution=dpi, title=spec.get("title", "Coloring Book"))
    print(f"Wrote {dest} ({len(sheets)} pages, {size_name} @ {dpi} DPI, "
          f"{margin}\" margins)")


# ------------------------------------------------------------------- main ---

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["outline", "characters", "landmarks", "pages",
                                      "postprocess", "pdf", "all"])
    ap.add_argument("--mock", action="store_true",
                    help="run without the OpenAI API (placeholder art)")
    ap.add_argument("--page", type=int, help="pages stage: only (re)generate this page")
    ap.add_argument("--only", help="characters/landmarks stage: only (re)generate this one")
    ap.add_argument("--workdir", help="directory holding spec.yaml/.env/output "
                    "(default: $COLORING_BOOK_DIR or the current directory)")
    args = ap.parse_args()

    global WORK, OUT
    WORK = resolve_workdir(args.workdir)
    OUT = WORK / "output"

    spec = load_spec()
    if args.stage in ("outline", "all"):
        stage_outline(spec, mock=args.mock)
    if args.stage in ("characters", "all"):
        stage_characters(spec, mock=args.mock, only=args.only)
    if args.stage in ("landmarks", "all"):
        stage_landmarks(spec, mock=args.mock, only=args.only)
    if args.stage in ("pages", "all"):
        stage_pages(spec, mock=args.mock, page=args.page)
    if args.stage in ("postprocess", "all"):
        stage_postprocess(spec)
    if args.stage in ("pdf", "all"):
        stage_pdf(spec)


if __name__ == "__main__":
    main()
