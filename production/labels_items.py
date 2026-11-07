"""labels_items.py <code>: every heading and label of a volume as the headings-and-labels review reads them
(workflows/labels_review.js), written to proof/<code>/labels.json: one item per short translated text (a title, a
section label, a sign, a tag, a table cell, a picture label) with
  id, page (1-based), role, zh (the Chinese), en (the English as printed), w (box width in points), size (the Chinese
  type size), set (the size the English was set at), lesson (the page's title) and near (the nearest longer paragraph).
Page 2 (left out of the English book) and the last page (the afterword) are skipped."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import out_dir, proof_dir  # noqa: E402

HAN = re.compile(r"[㐀-鿿]")
MAX_WORDS = 8


def short(s: dict) -> bool:
    en = (s.get("translated_text") or "").strip()
    return bool(en) and "\n" not in en and len(en.split()) <= MAX_WORDS and len(en) <= 60


def main() -> None:
    code = sys.argv[1]
    segs = [s for s in json.load(open(out_dir(code) / "segments.json", encoding="utf-8"))["segments"]
            if s["kind"] == "text" and HAN.search(s.get("source_text") or "")]
    last = max(s["page"] for s in segs)
    by_page: dict[int, list] = {}
    for s in segs:
        by_page.setdefault(s["page"], []).append(s)
    items = []
    for p, ss in sorted(by_page.items()):
        if p in (1, last):
            continue
        heads = [s for s in ss if s["style"].get("role") == "heading" and (s.get("translated_text") or "").strip()]
        lesson = min(heads, key=lambda s: s["bbox"]["y0"])["translated_text"].strip() if heads else ""
        body = [s for s in ss if not short(s) and (s.get("translated_text") or "").strip()]
        for s in ss:
            if not short(s) or (s.get("translated_text") or "").strip() in ("DROP", "BLANK"):
                continue
            b, r = s["bbox"], s.get("render") or {}
            cy = (b["y0"] + b["y1"]) / 2
            near = min(body, key=lambda o: abs((o["bbox"]["y0"] + o["bbox"]["y1"]) / 2 - cy), default=None)
            items.append({"id": s["id"], "page": p + 1, "role": s["style"].get("role"),
                          "zh": (s.get("source_text") or "").strip(), "en": s["translated_text"].strip(),
                          "w": round(b["x1"] - b["x0"]), "size": round(s["style"].get("size") or 0, 1),
                          "set": round(r.get("font_size") or 0, 1), "lesson": lesson,
                          "near": (near["translated_text"].strip()[:80] if near else "")})
    json.dump(items, open(proof_dir(code) / "labels.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(code, len(items), "headings and labels")


if __name__ == "__main__":
    main()
