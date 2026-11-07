"""make_proof_pack.py <code>: the files a proofreader reads, one set per page P (three digits, 1-based) in proof/<code>/:
  pP_src.png  the Chinese page          pP_out.png  the English page as last rendered (out_<code>/output.pdf)
  pP_old.png  the same page of the checked edition delivered earlier (deliveries/), when there is one
  pP.json     the page's paragraphs (id, role, source, protected, translation with ⟦n⟧ placeholders, shown, box,
              scale, note, lines), chinese_left_in_picture (OCR lines left untranslated), and, from leftover.json,
              chinese_visible_on_output and smaller_than_siblings
Page 2 (left out of the English book) and the last page (the afterword, typeset separately) have no set."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import final_page_of, out_dir, pdf_name, proof_dir, reading_order, source_pdf  # noqa: E402

DELIVERIES = Path(os.environ.get("BNU_DELIVERIES", "/tmp/piptest/deliveries"))
HAN = re.compile(r"[㐀-鿿]")
DPI = 75


def main() -> None:
    code = sys.argv[1]
    pdir = proof_dir(code)
    pdir.mkdir(parents=True, exist_ok=True)
    segs = json.load(open(out_dir(code) / "segments.json", encoding="utf-8"))["segments"]
    by_id = {s["id"]: s for s in segs}
    src = pymupdf.open(str(source_pdf(code)))
    out = pymupdf.open(str(out_dir(code) / "output.pdf"))
    old_path = DELIVERIES / pdf_name(code)
    old = pymupdf.open(str(old_path)) if old_path.exists() else None
    leftover = {}
    if (pdir / "leftover.json").exists():
        leftover = json.load(open(pdir / "leftover.json", encoding="utf-8")).get("pages", {})
    last = src.page_count - 1
    pages = []
    for i in range(src.page_count):
        if i in (1, last):
            continue
        n = i + 1
        tag = f"p{n:03d}"
        src[i].get_pixmap(dpi=DPI).save(str(pdir / f"{tag}_src.png"))
        out[i].get_pixmap(dpi=DPI).save(str(pdir / f"{tag}_out.png"))
        q = final_page_of(i)
        if old is not None and q is not None and q < old.page_count:
            old[q].get_pixmap(dpi=DPI).save(str(pdir / f"{tag}_old.png"))
        page_segs, left = [], []
        for s in segs:
            if s["page"] != i:
                continue
            b = [round(s["bbox"][k], 1) for k in ("x0", "y0", "x1", "y1")]
            if s["kind"] == "text":
                r = s.get("render") or {}
                lines = [m["source_text"] for m in reading_order(
                    [by_id[m] for m in s.get("members") or [] if m in by_id and by_id[m].get("image")
                     and not re.search(r"_e\d+$", m)],
                    lambda m: tuple(m["bbox"][k] for k in ("x0", "y0", "x1", "y1")))]  # the order a split uses
                page_segs.append({"id": s["id"], "role": s["style"].get("role"), "source": s.get("source_text"),
                                  "protected": s.get("protected_text"), "translation": s.get("translation_raw"),
                                  "shown": s.get("translated_text"), "box": b,
                                  "scale": round(r.get("scale", 0), 2) if r else None,
                                  "note": (r.get("notes") or "")[:120] if r else "",
                                  **({"lines": lines} if len(lines) > 1 else {})})
            elif s["kind"] == "image_text" and HAN.search(s.get("source_text") or "") \
                    and not (s.get("skip_reason") or "").startswith(("merged", "slanted", "watermark")):
                left.append({"id": s["id"], "text": s["source_text"], "why": (s.get("skip_reason") or "")[:60], "box": b})
        page_doc = {"page": n, "segments": page_segs, "chinese_left_in_picture": left,
                    "old_checked_edition": f"{tag}_old.png" if (pdir / f"{tag}_old.png").exists() else None}
        items = leftover.get(str(n)) or []
        vis = [it for it in items if not it.get("how", "").startswith("SMALLER")]
        small = [it for it in items if it.get("how", "").startswith("SMALLER")]
        if vis:
            page_doc["chinese_visible_on_output"] = vis
        if small:
            page_doc["smaller_than_siblings"] = small
        json.dump(page_doc, open(pdir / f"{tag}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        pages.append(n)
    json.dump({"code": code, "pages": pages}, open(pdir / "index.json", "w"))
    print(code, "proof pack:", len(pages), "pages")


if __name__ == "__main__":
    main()
