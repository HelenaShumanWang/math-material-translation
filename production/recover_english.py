"""recover_english.py <code> [<delivered.pdf>]: carry the checked English of an earlier delivered edition over to the
fresh stage-1 segments of a volume.

Every text line of a delivered page is given to the paragraph it was set for: the one whose box (grown the way the
layout grows boxes, right and down) holds most of the line, the nearest when two do. The lines of a paragraph, in
reading order, are its recovered English. It is kept only when it is plausible for that paragraph: no number the
source does not have, a length near the new translation's, and no inline picture in the paragraph (those are
images in the delivered page, so their place in the sentence cannot be read back). Kept texts are written as
proof/<code>/corr_000_recovered.json, dated first so that every later correction overrides them.
The default delivered edition is deliveries/<Mathematics Grade N Volume M.pdf> (page 2 left out of it)."""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import final_page_of, out_dir, pdf_name, proof_dir  # noqa: E402

from mathtrans.models import ANCHOR_RE, SegmentKind, TranslatedDocument  # noqa: E402

DELIVERIES = Path(os.environ.get("BNU_DELIVERIES", "/tmp/piptest/deliveries"))
NUM = re.compile(r"\d+(?:\.\d+)?")
CN_NUM = re.compile(r"[一二三四五六七八九十百千万零两]")


def grown(b, page_w: float) -> tuple[float, float, float, float]:
    w, h = b.x1 - b.x0, b.y1 - b.y0
    return (b.x0 - 6, b.y0 - max(6.0, 0.6 * h), min(page_w, b.x1 + max(40.0, 0.6 * w)), b.y1 + max(14.0, 0.9 * h))


def overlap(a, b) -> float:
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    return max(0.0, x1 - x0) * max(0.0, y1 - y0)


def main() -> None:
    code = sys.argv[1]
    delivered = Path(sys.argv[2]) if len(sys.argv) > 2 else DELIVERIES / pdf_name(code)
    base = out_dir(code) / "segments_base.json"
    if not base.exists():
        base = out_dir(code) / "segments.json"
    doc = TranslatedDocument.model_validate(json.load(open(base, encoding="utf-8")))
    old = pymupdf.open(str(delivered))
    last_source = len(doc.pages) - 1  # the afterword is typeset separately
    paras: dict[int, list] = {}
    for s in doc.segments:
        if s.kind == SegmentKind.TEXT and s.page not in (1, last_source):
            paras.setdefault(s.page, []).append(s)
    out, why = [], Counter()
    for page, segs in paras.items():
        q = final_page_of(page)
        if q is None or q >= old.page_count:
            continue
        pw = doc.pages[page].width
        lines = []
        for b in old[q].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for ln in b["lines"]:
                t = "".join(sp["text"] for sp in ln["spans"]).strip()
                if t:
                    lines.append((ln["bbox"], t))
        boxes = {s.id: grown(s.bbox, pw) for s in segs}
        got: dict[str, list] = {}
        for lb, t in lines:
            area = max(1.0, (lb[2] - lb[0]) * (lb[3] - lb[1]))
            scored = [(overlap(lb, boxes[s.id]) / area, s) for s in segs]
            scored = [(sc, s) for sc, s in scored if sc >= 0.5]
            if not scored:
                continue
            cy, cx = (lb[1] + lb[3]) / 2, (lb[0] + lb[2]) / 2

            def dist(s):
                bx = s.bbox
                return max(bx.x0 - cx, 0, cx - bx.x1) + max(bx.y0 - cy, 0, cy - bx.y1)
            best = min(scored, key=lambda x: (dist(x[1]), -x[0]))[1]
            got.setdefault(best.id, []).append((lb, t))
        for s in segs:
            new = (s.translated_text or "").strip()
            if s.id not in got:
                why["no English found"] += 1
                continue
            if ANCHOR_RE.search(new) or s.anchors:
                why["inline picture"] += 1
                continue
            ls = sorted(got[s.id], key=lambda x: (round(x[0][1] / 6), x[0][0]))
            text = re.sub(r"\s+", " ", " ".join(t for _, t in ls)).replace("- ", "-").strip()
            if not text or text == new:
                why["same as new"] += 1
                continue
            src_nums = set(NUM.findall(s.source_text or "")) | set(NUM.findall(new))
            bad = [n for n in NUM.findall(text) if n not in src_nums]
            if bad and not CN_NUM.search(s.source_text or ""):
                why["number not in source"] += 1
                continue
            if new and not 0.35 <= len(text) / max(1, len(new)) <= 2.8:
                why["length unlike the new translation"] += 1
                continue
            out.append({"segment_id": s.id, "translation": text,
                        "reason": "recovered from the checked edition delivered earlier"})
            why["recovered"] += 1
    pdir = proof_dir(code)
    pdir.mkdir(parents=True, exist_ok=True)
    path = pdir / "corr_000_recovered.json"
    json.dump({"corrections": out}, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.utime(path, (1, 1))  # first in file-time order: every later correction overrides it
    print(code, dict(why))


if __name__ == "__main__":
    main()
