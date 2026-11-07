"""preview_pages.py <code> <page,...> [--dpi N]: render only these pages (1-based, as printed) of a volume as its
corrected segments stand (out_<code>/segments.json, written by apply_corrections.py), side by side with the source,
into previews/<tag>_<code>_<page>.png. Nothing of the volume is touched. MT_OUT_DIR / MT_PROOF_DIR / MT_PREVIEW_TAG
redirect the inputs and name the outputs (try_fix.py)."""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

import pymupdf
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import image_fixes  # noqa: E402
from common import PREVIEWS, out_dir, proof_dir, source_pdf  # noqa: E402

from mathtrans.layout import render_document  # noqa: E402
from mathtrans.models import RenderInfo, SegmentKind, TranslatedDocument  # noqa: E402
from mathtrans.scanned import erase_merged_lines, paragraphs_to_restore, restore_lines  # noqa: E402

code = sys.argv[1]
pages = sorted({int(p) - 1 for p in sys.argv[2].split(",") if p.strip()})
dpi = int(sys.argv[sys.argv.index("--dpi") + 1]) if "--dpi" in sys.argv else 90
OUT = Path(os.environ.get("MT_OUT_DIR") or out_dir(code))
PROOF = Path(os.environ.get("MT_PROOF_DIR") or proof_dir(code))
TAG = os.environ.get("MT_PREVIEW_TAG", "preview")
PREVIEWS.mkdir(parents=True, exist_ok=True)
t0 = time.time()
src = str(source_pdf(code))
doc = TranslatedDocument.model_validate(json.load(open(OUT / "segments.json", encoding="utf-8")))
doc.segments = [s for s in doc.segments if s.page in pages]
for seg in doc.segments:
    if seg.kind == SegmentKind.TEXT:
        seg.render = None
tmp = PREVIEWS / f".{TAG}_{code}_{os.getpid()}"  # one scratch folder per run: previews may run side by side
tmp.mkdir(parents=True, exist_ok=True)
index = {p: i for i, p in enumerate(pages)}
for seg in doc.segments:
    seg.page = index[seg.page]
    if seg.image is not None:
        seg.image.page = index.get(seg.image.page, seg.image.page)
doc.pages = [doc.pages[p].model_copy(update={"index": index[p]}) for p in pages]
sel = pymupdf.open(src)
sel.select(pages)  # page objects keep their image xrefs
sel.save(str(tmp / "src.pdf"))
sel.close()
work = pymupdf.open(src)
work.select(pages)
erase_merged_lines(work, doc)
fixes = []
for fpath in {PROOF / "pixel_fixes.json", proof_dir(code) / "pixel_fixes.json"}:
    if fpath.exists():
        fixes += [dict(c, page=index[int(c["page"])]) for c in json.load(open(fpath)) if int(c["page"]) in index]
if fixes:
    image_fixes.apply(work, str(tmp / "src.pdf"), fixes)
work.save(str(tmp / "erased.pdf"), garbage=1)
work.close()
render_document(str(tmp / "erased.pdf"), doc, str(tmp / "out.pdf"), min_font_scale=0.55, anchor_source=str(tmp / "src.pdf"))
blank_ids: set[str] = set()
for bpath in {PROOF / "blanked.json", proof_dir(code) / "blanked.json"}:
    if bpath.exists():
        blank_ids |= set(json.load(open(bpath)))
for seg in doc.segments:  # BLANKed paragraphs are erased and set nothing, as in the full render
    if seg.id in blank_ids and seg.kind == SegmentKind.TEXT:
        seg.render = RenderInfo(font_size=0.0, scale=1.0, notes="blanked by the proofreader")
o = pymupdf.open(str(tmp / "out.pdf"))
restore = paragraphs_to_restore(doc)
if restore:
    s2 = pymupdf.open(str(tmp / "src.pdf"))
    restore_lines(o, s2, doc, restore)
    s2.close()
srcd = pymupdf.open(str(tmp / "src.pdf"))
for p in pages:
    i = index[p]
    a, b = srcd[i].get_pixmap(dpi=dpi), o[i].get_pixmap(dpi=dpi)
    im = Image.new("RGB", (a.width + b.width + 10, max(a.height, b.height)), "white")
    im.paste(Image.frombytes("RGB", (a.width, a.height), a.samples), (0, 0))
    im.paste(Image.frombytes("RGB", (b.width, b.height), b.samples), (a.width + 10, 0))
    path = PREVIEWS / f"{TAG}_{code}_{p + 1}.png"
    im.save(path)
    small = [(s.id, round(s.render.scale, 2), (s.translated_text or "")[:40]) for s in doc.segments
             if s.page == i and s.kind == SegmentKind.TEXT and s.render and 0 < s.render.scale < 0.8]
    left = [(s.id, (s.translated_text or "")[:40]) for s in doc.segments if s.page == i and s.kind == SegmentKind.TEXT
            and s.render and "left in source" in (s.render.notes or "")]
    print(f"page {p + 1}: {path}; shrunk<0.8: {small}; left in source: {left}")
shutil.rmtree(tmp, ignore_errors=True)
print(f"{time.time() - t0:.1f}s")
