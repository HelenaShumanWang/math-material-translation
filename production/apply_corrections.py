"""apply_corrections.py <code> [--save-only]: apply every correction of a volume to its pristine stage-1 segments and
re-render it.

The pristine segments are out_<code>/segments_base.json (a copy of the pipeline's segments.json, made on the first
run). Each run starts from them and applies proof/<code>/corr_*.json in file-time order (the latest file wins), so a
run is reproducible and a rejection is a real one. Writes out_<code>/segments.json (corrected), and unless
--save-only, out_<code>/output.pdf and the QA report; proof/<code>/applied.json lists what was applied or rejected.

Correction kinds (boxes in PDF points; "page" = the 0-based page index of segment ids, pN_...):
  {"segment_id": id, "translation": "..."}      English for a paragraph ("DROP": the Chinese stays in the picture;
                                                 "BLANK": erased, nothing set); may carry "box" (lay it out there),
                                                 "erase" ([[x0, y0, x1, y1], ...] small areas next to it to erase too)
                                                 "clip" (only the part of its lines inside the box is erased)
                                                 and "vertical" (true: set rotated along a narrow upright strip)
  {"merge": [id, id, ...], "translation": "..."} one sentence the OCR split; the first id keeps the paragraph
  {"split": id, "translations": [...]}           one paragraph per OCR line; with "at": [x, ...] one line cut into cells
  {"line": id, "translation": "...", "force": true}  an OCR line left in the picture, set in its place (paragraph id_t)
  {"line": id, "pieces": [[x0, x1, "text"(, y0, y1)], ...]}  only these ranges of a line erased and re-set
  {"add": "pN_aK", "page": N, "box": [...], "translation": "...", "source": "...", "size": s, "align": a, "color": c}
                                                 text the OCR never read: exactly the box is erased and the English set
  {"restore": [...], "page": N} / {"paint": [...], "page": N, "colour": "border" | [r, g, b]}  pixel fixes
Paths can be redirected with MT_OUT_DIR / MT_PROOF_DIR (try_fix.py works on scratch copies)."""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import image_fixes  # noqa: E402
from common import out_dir as _out_dir, proof_dir as _proof_dir, reading_order, source_pdf  # noqa: E402

from mathtrans.glossary import default_glossary  # noqa: E402
from mathtrans.layout import render_document  # noqa: E402
from mathtrans.models import (BBox, Lang, PipelineOptions, QAReport, RenderInfo, SegmentKind,  # noqa: E402
                              SegmentStyle, TextSegment, TranslatedDocument)
from mathtrans.protect import restore_placeholders  # noqa: E402
from mathtrans.qa.checks import image_text, layout_fit, output_checks, rule_checks  # noqa: E402
from mathtrans.qa.report import report_markdown, summarize  # noqa: E402
from mathtrans.scanned import MERGED, erase_merged_lines, paragraphs_to_restore, restore_lines  # noqa: E402
from mathtrans.translate.postprocess import (ANSWER_BRACKET, _EMPTY_BRACKET_RE, british_spelling,  # noqa: E402
                                             space_units)

PLACEHOLDER = re.compile(r"⟦(\d+)⟧")
MAX_BOX_GROWTH = 6.0  # a new layout box is at most this many times the old one's area
DELIBERATE = re.compile(r"_(p\d+|a\d+_p0|k\d+|t)$")  # segments a correction made
# the recurring section labels read the same in every volume
SECTION_LABELS = {"你知道吗": "Did You Know?", "试一试": "Try It", "数学好玩": "Maths Is Fun", "说一说": "Talk About It",
                  "做一做": "Do It", "练一练": "Practice", "议一议": "Discuss", "想一想": "Think"}
RULE_CHECKS = {"completeness", "glossary", "numbers", "placeholders", "formatting", "layout_fit"}

code = sys.argv[1]
save_only = "--save-only" in sys.argv
t0 = time.time()
OUT = Path(os.environ.get("MT_OUT_DIR") or _out_dir(code))
PROOF = Path(os.environ.get("MT_PROOF_DIR") or _proof_dir(code))
SRC = str(source_pdf(code))
PROOF.mkdir(parents=True, exist_ok=True)
base = OUT / "segments_base.json"
if not base.exists():
    shutil.copy(OUT / "segments.json", base)
doc = TranslatedDocument.model_validate(json.load(open(base, encoding="utf-8")))
by_id: dict[str, TextSegment] = {s.id: s for s in doc.segments}
blanked: set[str] = set()
pixel_fixes: dict = {}
applied: list[dict] = []
rejected: list[dict] = []
page_rects = [pymupdf.Rect(0, 0, p.width, p.height) for p in doc.pages]


# --------------------------------------------------------------------------- helpers
def _remove(seg: TextSegment) -> None:
    doc.segments.remove(seg)
    by_id.pop(seg.id, None)


def _add_seg(seg: TextSegment) -> None:
    old = by_id.get(seg.id)
    if old is not None:
        doc.segments.remove(old)
    doc.segments.append(seg)
    by_id[seg.id] = seg


def _set_text(seg: TextSegment, tr: str) -> tuple[bool, str]:
    """English for a paragraph; DROP keeps the Chinese in the picture, BLANK erases it and sets nothing."""
    tr = str(tr).strip()
    if not tr:
        return False, "empty translation"
    if tr == "DROP":
        seg.translated_text, seg.translation_raw = None, None
        blanked.discard(seg.id)
        return True, "dropped: the picture keeps it"
    if tr == "BLANK":
        seg.translated_text, seg.translation_raw = "", ""
        blanked.add(seg.id)
        return True, "blanked"
    blanked.discard(seg.id)
    used = {int(i) for i in PLACEHOLDER.findall(tr)}
    unknown = sorted(i for i in used if i >= len(seg.protected))
    if unknown:
        return False, "placeholders: unknown placeholders: " + ", ".join(f"⟦{i}⟧" for i in unknown)
    seg.translation_raw = tr
    seg.translated_text = restore_placeholders(tr, seg.protected) if used else tr
    seg.translate = True
    missing = [i for i in range(len(seg.protected)) if f"⟦{i}⟧" in (seg.protected_text or "") and i not in used]
    return True, ("dropped placeholders " + ", ".join(f"⟦{i}⟧" for i in missing)) if missing and used else "set"


def _members(seg: TextSegment) -> list[TextSegment]:
    return [by_id[m] for m in seg.members or [] if m in by_id]


def _px(img, x0, y0, x1, y1) -> tuple[int, int, int, int]:
    sx, sy = img.width / img.bbox.width, img.height / img.bbox.height
    return (max(0, int((x0 - img.bbox.x0) * sx)), max(0, int((y0 - img.bbox.y0) * sy)),
            min(img.width, int((x1 - img.bbox.x0) * sx + 0.999)), min(img.height, int((y1 - img.bbox.y0) * sy + 0.999)))


def _exact_member(line: TextSegment, mid: str, owner: str, x0, y0, x1, y1) -> TextSegment:
    """A copy of ``line`` covering exactly the box (ids ending _p<k>m are erased exactly, never sideways)."""
    m = line.model_copy(deep=True)
    m.id, m.bbox, m.anchors, m.translate = mid, BBox(x0=x0, y0=y0, x1=x1, y1=y1), {}, False
    m.skip_reason = f"{MERGED} {owner}"
    if m.image is not None:
        px = _px(m.image, x0, y0, x1, y1)
        m.image = m.image.model_copy(update={"pixel_box": px, "polygon": [[px[0], px[1]], [px[2], px[1]],
                                                                           [px[2], px[3]], [px[0], px[3]]]})
    return m


def _new_para(pid: str, page: int, box: BBox, source: str, style: SegmentStyle, members: list[str]) -> TextSegment:
    return TextSegment(id=pid, page=page, kind=SegmentKind.TEXT, bbox=box, source_text=source, protected_text=source,
                       style=style, origin="ocr", members=members, translate=True)


def _owner_of(line_id: str) -> TextSegment | None:
    return next((s for s in doc.segments if s.kind == SegmentKind.TEXT and line_id in (s.members or [])), None)


def _box(c) -> tuple[float, float, float, float] | None:
    try:
        x0, y0, x1, y1 = (float(v) for v in c)
    except Exception:  # noqa: BLE001
        return None
    return (x0, y0, x1, y1) if x1 > x0 and y1 > y0 else None


# --------------------------------------------------------------------------- correction kinds
def set_box(seg: TextSegment, box) -> tuple[bool, str]:
    b = _box(box)
    if b is None:
        return False, f"bad box {box}"
    new = BBox(x0=b[0], y0=b[1], x1=b[2], y1=b[3])
    r = page_rects[seg.page]
    if new.x0 < -1 or new.y0 < -1 or new.x1 > r.width + 1 or new.y1 > r.height + 1:
        return False, "box off the page"
    if new.intersection_area(seg.bbox) <= 0:
        return False, "the new box must overlap the old one"
    if new.width * new.height > MAX_BOX_GROWTH * max(1.0, seg.bbox.width * seg.bbox.height):
        return False, "box more than six times the old one"
    seg.bbox = new
    return True, "box set"


def add_erase(seg: TextSegment, boxes) -> tuple[bool, str]:
    lines = [m for m in _members(seg) if m.image is not None]
    if not lines:
        return False, "the paragraph has no picture line to erase with"
    ref = lines[0]
    img = ref.image
    line_h = max(m.bbox.height for m in lines)
    n = 0
    for k, box in enumerate(boxes or []):
        b = _box(box)
        if b is None:
            return False, f"bad box {box}"
        x0, y0, x1, y1 = b
        if (y1 - y0) > 4 * line_h + 6 or (x1 - x0) > 0.6 * img.bbox.width:
            return False, f"box {box} is not a small area next to the line"
        if x0 < img.bbox.x0 or y0 < img.bbox.y0 or x1 > img.bbox.x1 or y1 > img.bbox.y1:
            return False, f"box {box} is off the picture"
        eid = f"{seg.id}_e{k}"
        e = ref.model_copy(deep=True)
        e.id, e.bbox, e.source_text, e.protected_text, e.translate = eid, BBox(x0=x0, y0=y0, x1=x1, y1=y1), "", "", False
        e.anchors = {}
        e.skip_reason = f"{MERGED} {seg.id}"
        px = _px(img, x0, y0, x1, y1)
        e.image = img.model_copy(update={"pixel_box": px, "polygon": [[px[0], px[1]], [px[2], px[1]], [px[2], px[3]],
                                                                       [px[0], px[3]]]})
        _add_seg(e)
        if eid not in seg.members:
            seg.members = list(seg.members) + [eid]
        n += 1
    return True, f"{n} erase box(es)"


def clip_lines(seg: TextSegment, box) -> tuple[bool, str]:
    b = _box(box)
    if b is None:
        return False, f"bad clip {box}"
    n = 0
    for m in _members(seg):
        if m.image is None:
            continue
        x0, y0 = max(m.bbox.x0, b[0]), max(m.bbox.y0, b[1])
        x1, y1 = min(m.bbox.x1, b[2]), min(m.bbox.y1, b[3])
        if x1 <= x0 or y1 <= y0:
            continue
        clipped = _exact_member(m, f"{m.id}_c{n}_p0m", seg.id, x0, y0, x1, y1)
        _add_seg(clipped)
        m.skip_reason = f"kept in the picture: clipped by {seg.id}"
        seg.members = [x for x in seg.members if x != m.id] + [clipped.id]
        n += 1
    return (True, f"{n} line(s) clipped") if n else (False, "the clip box holds none of its lines")


def segment_text(c) -> tuple[bool, str]:
    sid = c.get("segment_id")
    seg = by_id.get(sid)
    if seg is None or seg.kind != SegmentKind.TEXT:
        return False, "unknown or not a translated paragraph"
    notes = []
    if c.get("vertical") is not None:  # set along a narrow upright strip (a name tag on a tile), rotated
        seg.style.is_vertical = bool(c["vertical"])
        notes.append("vertical" if seg.style.is_vertical else "horizontal")
    if c.get("box") is not None:
        ok, why = set_box(seg, c["box"])
        if not ok:
            return False, why
        notes.append(why)
    if c.get("erase"):
        ok, why = add_erase(seg, c["erase"])
        if not ok:
            return False, why
        notes.append(why)
    if c.get("clip"):
        ok, why = clip_lines(seg, c["clip"])
        if not ok:
            return False, why
        notes.append(why)
    if c.get("translation") is not None:
        ok, why = _set_text(seg, c["translation"])
        if not ok:
            return False, why
        notes.append(why)
    return (True, "; ".join(notes)) if notes else (False, "nothing to do")


def merge_fragments(c) -> tuple[bool, str]:
    ids = [str(i) for i in c.get("merge") or []]
    segs = [by_id.get(i) for i in ids]
    if len(ids) < 2 or segs[0] is None:
        return False, f"unknown first id {ids[0] if ids else ''}"
    if any(s is None or s.kind != SegmentKind.TEXT for s in segs):
        return False, "unknown paragraph " + ", ".join(i for i, s in zip(ids, segs) if s is None)
    first = segs[0]
    own_protected = list(first.protected)
    if any(s.page != first.page for s in segs):
        return False, "the fragments are on different pages"
    for s in segs[1:]:
        first.members = list(first.members) + [m for m in s.members if m not in first.members]
        first.bbox = BBox(x0=min(first.bbox.x0, s.bbox.x0), y0=min(first.bbox.y0, s.bbox.y0),
                          x1=max(first.bbox.x1, s.bbox.x1), y1=max(first.bbox.y1, s.bbox.y1))
        first.source_text = (first.source_text or "") + (s.source_text or "")
        for m in s.members:
            if m in by_id:
                by_id[m].skip_reason = f"{MERGED} {first.id}"
        blanked.discard(s.id)
        _remove(s)
    first.protected_text, first.protected = first.source_text, []
    # a merged sentence is written out in full; a placeholder left in it means the first fragment's
    tr = restore_placeholders(str(c.get("translation") or ""), own_protected)
    ok, why = _set_text(first, tr)
    return ok, f"{len(segs)} fragments merged into {first.id}; {why}"


def _reading_lines(para: TextSegment) -> list[TextSegment]:
    lines = [m for m in _members(para) if m.image is not None and not re.search(r"_e\d+$", m.id)]
    return reading_order(lines, lambda m: (m.bbox.x0, m.bbox.y0, m.bbox.x1, m.bbox.y1))


def split_paragraph(c) -> tuple[bool, str]:
    pid = str(c.get("split"))
    trs = [str(t).strip() for t in c.get("translations") or []]
    para = by_id.get(pid)
    if para is None:  # split before (another file): update its parts
        parts = sorted((s for s in doc.segments if re.fullmatch(rf"{re.escape(pid)}_k\d+", s.id)),
                       key=lambda s: int(s.id.rsplit("_k", 1)[1]))
        if not parts or len(parts) != len(trs):
            return False, "unknown paragraph"
        for part, tr in zip(parts, trs):
            _set_text(part, tr)
        return True, f"{len(parts)} parts of {pid} updated"
    if para.kind != SegmentKind.TEXT:
        return False, "not a paragraph"
    lines = _reading_lines(para)
    cuts = c.get("at")
    if cuts:
        if len(lines) != 1:
            return False, "'at' cuts one line; this paragraph has several"
        line = lines[0]
        xs = sorted(float(x) for x in cuts)
        edges = [line.bbox.x0] + [x for x in xs if line.bbox.x0 < x < line.bbox.x1] + [line.bbox.x1]
        if len(edges) - 1 != len(trs):
            return False, f"{len(edges) - 1} cells but {len(trs)} translations"
        line.skip_reason = f"kept in the picture: cut into the parts of {pid}"
        for k in range(len(trs)):
            part_id = f"{pid}_k{k}"
            m = _exact_member(line, f"{part_id}_p0m", part_id, edges[k], line.bbox.y0, edges[k + 1], line.bbox.y1)
            _add_seg(m)
            part = _new_para(part_id, para.page, m.bbox, line.source_text, para.style.model_copy(), [m.id])
            _add_seg(part)
            _set_text(part, trs[k])
        _remove(para)
        return True, f"{pid} cut into {len(trs)} cells"
    if len(lines) != len(trs):
        return False, f"{len(lines)} lines but {len(trs)} translations"
    for k, (line, tr) in enumerate(zip(lines, trs)):
        part_id = f"{pid}_k{k}"
        style = para.style.model_copy()
        part = _new_para(part_id, para.page, line.bbox, line.source_text, style, [line.id])
        _add_seg(part)
        line.skip_reason = f"{MERGED} {part_id}"
        _set_text(part, tr)
    for extra in [m for m in _members(para) if re.search(r"_e\d+$", m.id)]:
        _remove(extra)
    _remove(para)
    return True, f"{pid} split into {len(trs)} parts"


def translate_line(c) -> tuple[bool, str]:
    lid = str(c.get("line"))
    line = by_id.get(lid)
    if line is None or line.kind != SegmentKind.IMAGE_TEXT:
        return False, "unknown line"
    if line.skip_reason.startswith(MERGED):
        return False, "the line already belongs to a paragraph"
    why = (line.skip_reason or "").lower()
    if not c.get("force") and any(k in why for k in ("slanted", "watermark", "pictogram")):
        return False, f"refused ({line.skip_reason[:40]}); use force when the box holds only text"
    pid = f"{lid}_t"
    style = line.style.model_copy()
    if style.size <= 0:
        style.size = max(6.0, 0.8 * line.bbox.height)
    para = _new_para(pid, line.page, line.bbox, line.source_text, style, [lid])
    _add_seg(para)
    line.skip_reason = f"{MERGED} {pid}"
    ok, w = _set_text(para, c.get("translation") or "")
    return ok, f"{pid} set; {w}"


def line_pieces(c) -> tuple[bool, str]:
    lid = str(c.get("line"))
    line = by_id.get(lid)
    if line is None or line.kind != SegmentKind.IMAGE_TEXT or line.image is None:
        return False, "unknown line"
    owner = _owner_of(lid)
    if owner is not None:
        owner.members = [m for m in owner.members if m != lid]
        if not [m for m in owner.members if not re.search(r"_e\d+$", m)]:
            _remove(owner)
    for s in [s for s in doc.segments if re.fullmatch(rf"{re.escape(lid)}_p\d+m?", s.id)]:
        _remove(s)  # pieces of an earlier correction of this line
    line.skip_reason = "kept in the picture: words set as pieces"
    n = 0
    for k, piece in enumerate(c.get("pieces") or []):
        try:
            x0, x1, text = float(piece[0]), float(piece[1]), str(piece[2])
            y0, y1 = (float(piece[3]), float(piece[4])) if len(piece) >= 5 else (line.bbox.y0, line.bbox.y1)
        except Exception:  # noqa: BLE001
            return False, f"bad piece {piece}"
        if x1 <= x0 or y1 <= y0:
            return False, f"bad piece {piece}"
        x0, x1 = max(x0, line.image.bbox.x0), min(x1, line.image.bbox.x1)
        pid = f"{lid}_p{k}"
        m = _exact_member(line, f"{pid}m", pid, x0, y0, x1, y1)
        _add_seg(m)
        style = line.style.model_copy()
        if style.size <= 0:
            style.size = max(6.0, 0.8 * (y1 - y0))
        style.align = "center"  # each piece stands in the gap it was measured for
        part = _new_para(pid, line.page, m.bbox, "", style, [m.id])
        _add_seg(part)
        _set_text(part, text)
        n += 1
    return True, f"{lid} set in {n} pieces"


def add_text(c) -> tuple[bool, str]:
    aid = str(c.get("add") or "").strip()
    tr = str(c.get("translation") or "").strip()
    try:
        page = int(c.get("page"))
        x0, y0, x1, y1 = (float(v) for v in c.get("box"))
    except Exception:  # noqa: BLE001
        return False, "an add needs page and box"
    if not aid or not tr or x1 <= x0 or y1 <= y0:
        return False, "an add needs an id, a box and a translation"
    pid, mid = f"{aid}_p0", f"{aid}_p0m"
    box = BBox(x0=x0, y0=y0, x1=x1, y1=y1)
    refs = [s for s in doc.segments if s.page == page and s.kind == SegmentKind.IMAGE_TEXT and s.image is not None
            and s.image.bbox.x0 <= x0 + 0.5 and s.image.bbox.y0 <= y0 + 0.5 and s.image.bbox.x1 >= x1 - 0.5
            and s.image.bbox.y1 >= y1 - 0.5 and not DELIBERATE.search(s.id)]
    if not refs:
        return False, "no picture of the page holds that box"
    ref = max(refs, key=lambda s: s.image.bbox.width * s.image.bbox.height)
    m = _exact_member(ref, mid, pid, x0, y0, x1, y1)
    m.source_text = m.protected_text = str(c.get("source") or "")
    _add_seg(m)
    size = float(c.get("size") or 0) or max(6.0, 0.75 * min(box.height, 3 * box.width))
    align = c.get("align") if c.get("align") in ("left", "center", "right") else "center"
    color = int(c["color"]) if isinstance(c.get("color"), (int, float)) else ref.style.color
    style = SegmentStyle(size=size, color=color, role="body" if align == "left" else "label", align=align,
                         line_height=1.2)
    para = _new_para(pid, page, box, m.source_text, style, [mid])
    _add_seg(para)
    ok, why = _set_text(para, tr)
    return ok, f"{pid} added; {why}"


LIGATURE_TEXT = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl", "\ufb05": "st", "\ufb06": "st"}
LIGATURES = re.compile("[\ufb00-\ufb06]")
TRAILING_DOTS = re.compile(r"\s?(?:\.{3,}|…+|·{2,}|⋯+)(?=[\s\"'”’)）]*$)", re.M)

# --------------------------------------------------------------------------- apply, file by file
files = sorted(glob.glob(f"{PROOF}/corr_*.json"), key=lambda f: (os.path.getmtime(f), f))
for path in files:
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        rejected.append({"file": os.path.basename(path), "why": f"unreadable: {exc}"})
        continue
    for c in data.get("corrections", []) if isinstance(data, dict) else []:
        if not isinstance(c, dict):
            continue
        # English recovered from a delivered PDF carries its typographic ligatures (ﬁ ﬂ ﬀ): plain letters
        for k in ("translation", "translations", "pieces"):
            if c.get(k) is not None:
                c[k] = json.loads(LIGATURES.sub(lambda m: LIGATURE_TEXT[m.group()], json.dumps(c[k], ensure_ascii=False)))
        try:
            if c.get("restore") is not None or c.get("paint") is not None:
                why = image_fixes.check(c, len(doc.pages), page_rects)
                if why is None:
                    key = (int(c["page"]), tuple(round(float(v), 1) for v in (c.get("restore") or c.get("paint"))))
                    pixel_fixes[key] = c
                ok = why is None
                why = why or "pixel fix"
            elif c.get("add"):
                ok, why = add_text(c)
            elif c.get("line") and c.get("pieces") is not None:
                ok, why = line_pieces(c)
            elif c.get("line"):
                ok, why = translate_line(c)
            elif c.get("merge"):
                ok, why = merge_fragments(c)
            elif c.get("split"):
                ok, why = split_paragraph(c)
            elif c.get("segment_id"):
                ok, why = segment_text(c)
            else:
                ok, why = False, "unknown correction"
        except Exception as exc:  # noqa: BLE001 - one bad entry never stops the volume
            ok, why = False, f"error: {type(exc).__name__}: {exc}"
        entry = {k: c[k] for k in ("segment_id", "merge", "split", "line", "add") if k in c}
        entry.update(file=os.path.basename(path), why=why)
        (applied if ok else rejected).append(entry)

# --------------------------------------------------------------------------- one style throughout
for seg in doc.segments:
    if seg.translated_text:
        t = seg.translated_text
        if "(" in t:
            t = _EMPTY_BRACKET_RE.sub(ANSWER_BRACKET, t)
        t = british_spelling(space_units(t))
        # one ellipsis: "...", "……" and "······" ending a sentence or a bubble are "…" (a run of dots in the
        # middle of a line can be a blank to fill in, and a text of dots only is a printed line: left)
        if re.search(r"[^\s.·…]", t):
            t = TRAILING_DOTS.sub("…", t)
        key = re.sub(r"[？?。.!！\s]", "", seg.source_text or "")
        if (seg.kind == SegmentKind.TEXT and key in SECTION_LABELS and seg.style.role in ("heading", "label")
                and not DELIBERATE.search(seg.id)):
            t = SECTION_LABELS[key]
        seg.translated_text = t

json.dump({"applied": applied, "rejected": rejected}, open(PROOF / "applied.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(list(pixel_fixes.values()), open(PROOF / "pixel_fixes.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(sorted(blanked), open(PROOF / "blanked.json", "w", encoding="utf-8"))
print(f"{code}: {len(applied)} corrections applied, {len(rejected)} rejected", flush=True)
if save_only:
    with open(OUT / "segments.json", "w", encoding="utf-8") as fh:
        fh.write(doc.model_dump_json(indent=1))
    sys.exit(0)

# --------------------------------------------------------------------------- render
for seg in doc.segments:
    if seg.kind == SegmentKind.TEXT:
        seg.render = None
erased, tmp_out = str(OUT / ".erased.pdf"), str(OUT / ".output.pdf")
s_doc = pymupdf.open(SRC)
erase_merged_lines(s_doc, doc)
if pixel_fixes:
    print(f"{code}: {image_fixes.apply(s_doc, SRC, list(pixel_fixes.values()))} pixel fixes", flush=True)
s_doc.save(erased, garbage=1)
s_doc.close()
render_document(erased, doc, tmp_out, min_font_scale=0.55, checkpoint_pages=25, anchor_source=SRC)
for seg in doc.segments:
    if seg.id in blanked and seg.kind == SegmentKind.TEXT:
        seg.render = RenderInfo(font_size=0.0, scale=1.0, notes="blanked by the proofreader")
pdf_doc = pymupdf.open(tmp_out)
restore = paragraphs_to_restore(doc)
if restore:
    s2 = pymupdf.open(SRC)
    restore_lines(pdf_doc, s2, doc, restore)
    s2.close()
try:
    pdf_doc.subset_fonts()
except Exception as exc:  # noqa: BLE001
    print("subsetting failed:", exc)
final_tmp = tmp_out + ".final.pdf"
pdf_doc.save(final_tmp, garbage=4, deflate=True)
pdf_doc.close()

# --------------------------------------------------------------------------- QA report
report_path = OUT / "qa_report.json"
report = QAReport.model_validate(json.load(open(report_path, encoding="utf-8")))
if not (OUT / "qa_report_base.json").exists():
    shutil.copy(report_path, OUT / "qa_report_base.json")
base_report = QAReport.model_validate(json.load(open(OUT / "qa_report_base.json", encoding="utf-8")))
opts = PipelineOptions(target_lang=Lang.EN)
corrected = {a.get("segment_id") or (a.get("merge") or [None])[0] or a.get("split") or a.get("line") for a in applied}
reviewed = corrected | {s.id for s in doc.segments if DELIBERATE.search(s.id)}
kept_review = [i for i in base_report.final_issues if i.check == "llm_review" and i.segment_id not in reviewed]
for i in kept_review:  # the first automatic review, made before the proofreading passes that kept this text
    if i.severity == "error":
        i.severity, i.message = "warning", "Earlier automatic review, text kept by the proofreading: " + i.message
pairs = default_glossary().pairs(doc.source_lang, doc.target_lang)
fresh = rule_checks(doc, opts, pairs) + layout_fit(doc, opts, []) + image_text(doc, opts, []) + output_checks(final_tmp, SRC, doc)
for i in fresh:  # a rule check on English a proofreader set records a decision, not an open problem
    if i.check in RULE_CHECKS and i.segment_id in reviewed and i.severity == "error":
        i.severity, i.message = "warning", "Reviewed by the proofreader: " + i.message
report.final_issues = kept_review + [i for i in fresh if i.check != "llm_review"]
report.errors = sum(1 for i in report.final_issues if i.severity == "error")
report.warnings = sum(1 for i in report.final_issues if i.severity == "warning")
report.passed = report.errors == 0
out_errors = sum(1 for i in report.final_issues if i.check.startswith("output") and i.severity == "error")
report.summary = summarize(report) + f"; proofread: {len(applied)} corrections applied; output file checks: {out_errors} error(s)"
os.replace(final_tmp, OUT / "output.pdf")
with open(OUT / "segments.json", "w", encoding="utf-8") as fh:
    fh.write(doc.model_dump_json(indent=1))
with open(report_path, "w", encoding="utf-8") as fh:
    fh.write(report.model_dump_json(indent=1))
with open(OUT / "qa_report.md", "w", encoding="utf-8") as fh:
    fh.write(report_markdown(report, doc))
for f in (erased, tmp_out):
    if os.path.exists(f):
        os.unlink(f)
print(code, "re-rendered in", round(time.time() - t0), "s |", report.summary, flush=True)
