"""leftover_items.py <code> <han_left output>: what the leftover pass decides on, page by page: the Chinese still
visible on the rendered volume (OCR findings, watermark misreadings left out), the paragraphs a proofreader dropped
or that have no translation, and the numbered instructions set smaller than the other numbered instructions of their
page (same kind of text, same size). Writes proof/<code>/leftover.json and prints a count."""
import glob
import json
import os
import re
import statistics
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import out_dir, proof_dir, source_pdf  # noqa: E402

from mathtrans.models import Lang  # noqa: E402
from mathtrans.scanned import _text_width  # noqa: E402

code, ocr_path = sys.argv[1], sys.argv[2]
segs = json.load(open(out_dir(code) / "segments.json"))["segments"]
LAST = pymupdf.open(str(source_pdf(code))).page_count
HAN = re.compile(r"[㐀-鿿]")
WM = set("北京师范大学出版社帅泡版")
ITEM = re.compile(r"^\s*(\d{1,2}\.\s|\(\d{1,2}\)\s|[①-⑩])")
drops = {}
for f in sorted(glob.glob(f"{proof_dir(code)}/corr_*.json"), key=os.path.getmtime):
    try:
        for c in json.load(open(f)).get("corrections", []):
            if c.get("segment_id") and c.get("translation") in ("DROP", "BLANK"):
                drops[c["segment_id"]] = (c["translation"], (c.get("reason") or "")[:90])
            elif c.get("segment_id") and c.get("translation"):
                drops.pop(c["segment_id"], None)
    except Exception:  # noqa: BLE001
        pass


def overlapping(page, box):
    out = []
    for s in segs:
        if s["page"] != page:
            continue
        b = s["bbox"]
        if b["x1"] > box[0] and b["x0"] < box[2] and b["y1"] > box[1] and b["y0"] < box[3]:
            if s["kind"] == "text" or ((s.get("skip_reason") or "") and not (s.get("skip_reason") or "").startswith("merged")):
                out.append(s["id"])
    return out


items: dict[int, list] = {}
for line in open(ocr_path):
    m = re.match(r"page (\d+) \[(\d+), (\d+), (\d+), (\d+)\] '(.*)' ([\d.]+)$", line.strip())
    if not m:
        continue
    P = int(m.group(1))
    if P == 2 or P == LAST:
        continue  # the QR page is left out of the book; the afterword page is typeset separately
    box = [int(m.group(k)) for k in range(2, 6)]
    text, conf = m.group(6), float(m.group(7))
    han = HAN.findall(text)
    if not han or (len(han) <= 4 and sum(c in WM for c in han) >= 0.5 * len(han)):
        continue
    items.setdefault(P, []).append({"text": text, "box": box, "how": f"visible on the output (OCR {conf:.2f})",
                                    "ids": overlapping(P - 1, box)})
for s in segs:
    if s["kind"] != "text" or (s.get("translated_text") or "").strip() or not HAN.search(s.get("source_text") or ""):
        continue
    kind, why = drops.get(s["id"], ("", ""))
    if kind == "BLANK":
        continue
    P = s["page"] + 1
    if P in (2, LAST):
        continue
    b = s["bbox"]
    box = [round(b["x0"]), round(b["y0"]), round(b["x1"]), round(b["y1"])]
    already = [it for it in items.get(P, []) if s["id"] in it["ids"]]
    note = f"paragraph dropped by a proofreader: {why}" if kind == "DROP" else "paragraph with no translation"
    if already:
        already[0]["how"] += f"; {note}"
    else:
        items.setdefault(P, []).append({"text": s.get("source_text"), "box": box, "how": note, "ids": [s["id"]]})
by_page: dict[int, list] = {}
for s in segs:
    r = s.get("render") or {}
    if s["kind"] == "text" and r.get("font_size") and ITEM.match(s.get("translated_text") or ""):
        by_page.setdefault(s["page"], []).append(s)
smaller = 0
for pg, ss in by_page.items():
    if len(ss) < 2 or pg + 1 in (2, LAST):
        continue
    top = statistics.median(x["render"]["font_size"] for x in ss)
    for s in ss:
        f = s["render"]["font_size"]
        if f >= 0.9 * top:
            continue
        rb = s["render"].get("bbox") or s["bbox"]
        tr = s.get("translated_text") or ""
        width = max(_text_width(line, top, Lang.EN) for line in tr.split("\n"))
        items.setdefault(pg + 1, []).append({
            "text": tr, "box": [round(rb["x0"]), round(rb["y0"]), round(rb["x1"]), round(rb["y1"])],
            "how": (f"SMALLER: set at {f:.1f} pt while the other numbered instructions on this page are {top:.1f} pt; "
                    f"at {top:.1f} pt this English is {width:.0f} pt wide on one line (its box was "
                    f"{rb['x1'] - rb['x0']:.0f} x {rb['y1'] - rb['y0']:.0f} pt)"), "ids": [s["id"]]})
        smaller += 1
out = {"code": code, "pages": {str(p): items[p] for p in sorted(items)}}
json.dump(out, open(proof_dir(code) / "leftover.json", "w"), ensure_ascii=False, indent=1)
print(code, sum(len(v) for v in items.values()), "items on", len(items), "pages;", smaller, "smaller instructions")
