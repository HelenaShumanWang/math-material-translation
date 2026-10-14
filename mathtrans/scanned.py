"""Scanned pages: editable text instead of repainted pixels ("overlay" mode).

A scanned page is one full-page raster image without a text layer. In
``repaint`` mode the translation is drawn into the image (see
:mod:`mathtrans.images`). In ``overlay`` mode the OCR lines of such a page are
grouped into paragraph segments (``kind=TEXT``, ``origin="ocr"``), the
recognised glyphs are erased from the image, and the paragraphs are translated
and laid out by the normal text pipeline - the result is real, editable PDF
text and sentences are translated with their paragraph context.
"""
from __future__ import annotations

import logging
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Callable, Optional, Union

import numpy as np
import pymupdf

from .extract import is_list_item
from .images import (INLINE_PICTOGRAMS, _clear_box, encode_image, has_pictogram_gap, load_image, replace_image,
                     resolve_placement)
from .languages import is_cjk
from .models import (BBox, Lang, RenderInfo, SegmentKind, SegmentStyle, TextSegment,
                     TranslatedDocument)
from .protect import is_fully_protected, protect_text

log = logging.getLogger("mathtrans.scanned")

MIN_PAGE_COVER = 0.85
"""An image covering at least this share of the page makes a text-less page "scanned"."""
MAX_LINE_GAP = 0.75
"""Lines closer than this many line heights belong to the same paragraph."""
MIN_X_OVERLAP = 0.4
"""Horizontal overlap (share of the narrower line) required to stack lines."""
HEIGHT_RATIO = (0.7, 1.4)
"""Line heights within a paragraph must stay within this ratio range."""
MIN_WIDTH_SHARE = 0.3
"""A line narrower than this share of the paragraph width joins it only when left-aligned."""
MAX_X0_JUMP = 2.5
FIRST_LINE_INDENT = 2.6
"""A paragraph's first line may be indented by up to this many line heights (two characters
plus slack): its second line then starts that far to the left of it."""
"""A line whose left edge is more than this many line heights away from a left-aligned
paragraph's (and that is not centred under it) is in another column: a speech bubble,
a label next to the instruction."""
_ANSWER_START_RE = re.compile(r"^\s*[答解][:：]")
"""答：/ 解：: an answer line is a paragraph of its own."""
_STARTS_NEW_RE = re.compile(r"^\s*(?:([\u4e00-\u9fff])一\1|[●•·▪◆■]|[答解][:：])")
"""Lines that always start a new paragraph: reduplicated instruction verbs (做一做, 说一说,
比一比, 算一算 ...), bullet glyphs and answer lines."""
_SENTENCE_END = "。！？!?"


def _closes_paragraph(text: str) -> bool:
    """``答：`` / ``解：`` / ``Answer:`` on their own line are followed by a blank to fill."""
    t = text.strip()
    return len(t) <= 8 and t[-1:] in "：:" if t else False
FONT_HEIGHT_RATIO = 0.82
MAX_COLOR_DISTANCE = 120.0
"""Lines whose estimated text colours differ by more than this (RGB distance) are
not merged: a white heading on a coloured badge must not drag the black body
text below it into a white paragraph."""


def _color_distance(a: int, b: int) -> float:
    ra, ga, ba = (a >> 16) & 255, (a >> 8) & 255, a & 255
    rb, gb, bb = (b >> 16) & 255, (b >> 8) & 255, b & 255
    return ((ra - rb) ** 2 + (ga - gb) ** 2 + (ba - bb) ** 2) ** 0.5
"""Font size relative to the OCR line height (box height includes ascender/descender room)."""
REPEATED_LABEL_LETTERS = 6
"""A short line (at most this many letters) that repeats the line above it word for word is a
label of a list (有几个？ under each picture), set on its own; it never continues a paragraph."""
MERGED = "merged into paragraph"
UNIT_DROPPED = "unit label after an answer box (dropped)"
"""Prefix of the ``skip_reason`` of OCR lines that became part of a paragraph."""


# --------------------------------------------------------------------------- #
# pages assembled from a page image plus patch images drawn over it
# --------------------------------------------------------------------------- #

PATCH_DUPLICATE = "duplicate read on a patch image of"
"""``skip_reason`` (after :data:`MERGED`) of an OCR line read on a patch image - a smaller
image placed over the page image that repeats the same part of the scan - when the line
underneath carries the text: the copy is erased from the patch and set once, from the line
underneath. Followed by the id of that line."""
PATCH_OVERLAP = 0.6
"""A patch line and a line underneath are the same text when their intersection covers at
least this share of the smaller of the two boxes (page space)."""


def _patch_pairs(lines: list[TextSegment]) -> list[tuple[int, int]]:
    """``(patch_xref, base_xref)`` for every image whose placement lies inside another, larger
    image of the same page (a crop of the scan drawn on top of the page image)."""
    boxes: dict[int, BBox] = {}
    for seg in lines:
        if seg.image is not None and seg.image.xref not in boxes:
            boxes[seg.image.xref] = seg.image.bbox
    pairs: list[tuple[int, int]] = []
    for patch, pb in boxes.items():
        best: Optional[tuple[float, int]] = None
        for base, bb in boxes.items():
            if base == patch:
                continue
            inside = (pb.x0 >= bb.x0 - 1 and pb.y0 >= bb.y0 - 1 and pb.x1 <= bb.x1 + 1 and pb.y1 <= bb.y1 + 1)
            if inside and bb.width * bb.height > pb.width * pb.height * 1.05:
                area = bb.width * bb.height
                if best is None or area < best[0]:  # the nearest enclosing image is the one underneath
                    best = (area, base)
        if best is not None:
            pairs.append((patch, best[1]))
    return pairs


def _overlap_share(a: BBox, b: BBox) -> float:
    ix = max(0.0, min(a.x1, b.x1) - max(a.x0, b.x0))
    iy = max(0.0, min(a.y1, b.y1) - max(a.y0, b.y0))
    smaller = min(a.width * a.height, b.width * b.height)
    return ix * iy / smaller if smaller > 0 else 0.0


def suppress_patch_duplicates(lines: list[TextSegment], page_index: int) -> int:
    """Scanned pages are sometimes assembled from a full-page image plus smaller patch images
    (crops of the same scan) drawn over it; the OCR then reads the text under a patch twice.
    The copies read on the patch that repeat a line of the image underneath are marked
    erase-only (``translate=False``, ``skip_reason`` :data:`MERGED` + :data:`PATCH_DUPLICATE`
    + the id of the line underneath): the text is set once, from the line underneath, and the
    glyphs are wiped on the patch, which is the one that shows. Patch lines with nothing
    underneath stay as they are. Call before :func:`group_ocr_lines`; returns the number marked."""
    page_lines = [l for l in lines if l.page == page_index and l.kind == SegmentKind.IMAGE_TEXT and l.image is not None]
    marked = 0
    for patch, base in _patch_pairs(page_lines):
        under = [l for l in page_lines if l.image is not None and l.image.xref == base]
        for line in page_lines:
            if line.image is None or line.image.xref != patch or line.skip_reason.startswith(MERGED):
                continue
            best = max(under, key=lambda u: _overlap_share(u.bbox, line.bbox), default=None)
            if best is None or _overlap_share(best.bbox, line.bbox) < PATCH_OVERLAP:
                continue
            line.translate = False
            line.skip_reason = f"{MERGED} {PATCH_DUPLICATE} {best.id}"
            marked += 1
    if marked:
        log.info("page %d: %d line(s) read again on a patch image are erased there and set once", page_index, marked)
    return marked


def relink_patch_duplicates(lines: list[TextSegment], page_index: int) -> None:
    """After grouping: a patch copy follows the line underneath - erased and restored with the
    paragraph that line was merged into, or left in the picture when that line is."""
    by_id = {l.id: l for l in lines if l.page == page_index}
    prefix = f"{MERGED} {PATCH_DUPLICATE} "
    for line in lines:
        if line.page != page_index or not line.skip_reason.startswith(prefix):
            continue
        under = by_id.get(line.skip_reason[len(prefix):].strip())
        if under is None:
            continue
        if under.skip_reason.startswith(MERGED) or not under.translate:
            line.skip_reason = under.skip_reason


def is_scanned_page(page: pymupdf.Page, min_cover: float = MIN_PAGE_COVER) -> bool:
    """True for a page without text whose one image covers (almost) the whole page."""
    if page.get_text("words"):
        return False
    area = page.rect.width * page.rect.height
    if area <= 0:
        return False
    for info in page.get_image_info():
        rect = pymupdf.Rect(info["bbox"]) & page.rect
        if not rect.is_empty and rect.get_area() >= min_cover * area:
            return True
    return False


def scanned_pages(pdf: Union[str, Path, pymupdf.Document], pages: Optional[list[int]] = None) -> set[int]:
    doc = pdf if isinstance(pdf, pymupdf.Document) else pymupdf.open(str(pdf))
    try:
        indices = pages if pages is not None else range(doc.page_count)
        return {i for i in indices if 0 <= i < doc.page_count and is_scanned_page(doc[i])}
    finally:
        if not isinstance(pdf, pymupdf.Document):
            doc.close()


# --------------------------------------------------------------------------- #
# grouping OCR lines into paragraphs
# --------------------------------------------------------------------------- #


def _mergeable(seg: TextSegment) -> bool:
    """Lines that may become part of a paragraph: translatable text, and numbers /
    formulas (they are protected inside the paragraph). Labels, slanted text and
    foreign-script lines stay as they are."""
    if seg.kind != SegmentKind.IMAGE_TEXT or seg.image is None:
        return False
    if seg.translate:
        return True
    return seg.skip_reason == "pure number / formula" and not seg.source_text.strip().isdigit()


def _x_overlap(a: BBox, b: BBox) -> float:
    return max(0.0, min(a.x1, b.x1) - max(a.x0, b.x0))


class _Para:
    def __init__(self, line: TextSegment) -> None:
        self.lines = [line]
        self.bbox = line.bbox
        self.heights = [line.bbox.height]

    @property
    def last(self) -> TextSegment:
        return self.lines[-1]

    @property
    def median_height(self) -> float:
        return statistics.median(self.heights)

    def accepts(self, line: TextSegment) -> bool:
        if line.translate != self.lines[0].translate:
            return False  # formula / number lines never join a prose paragraph (they stay in the picture)
        if _color_distance(line.style.color, self.lines[0].style.color) > MAX_COLOR_DISTANCE:
            return False  # different text colour: a badge / heading vs the body text next to it
        if is_list_item(line.source_text):
            return False  # "2. ..." / "(1) ..." starts a new paragraph (a question, an exercise)
        if _letter_count(line.source_text) <= 1 or _letter_count(self.lines[0].source_text) <= 1:
            return False  # single-character lines are table cells / diagram labels, never paragraph lines
        if (line.source_text.strip() == self.last.source_text.strip()
                and _letter_count(line.source_text) <= REPEATED_LABEL_LETTERS):
            return False  # the same short label line after line (有几个？ × 4): one label each, not a paragraph
        if _closes_paragraph(self.last.source_text):
            return False  # "答：" / "解：" followed by a blank: nothing may be appended to it
        if _ANSWER_START_RE.match(self.lines[0].source_text) or _STARTS_NEW_RE.match(line.source_text):
            return False  # answer lines stand alone; 做一做 / ● / 答： open the next exercise
        h = self.median_height
        lh = line.bbox.height
        if h <= 0 or lh <= 0:
            return False
        if not (HEIGHT_RATIO[0] <= lh / h <= HEIGHT_RATIO[1]):
            return False
        gap = line.bbox.y0 - self.last.bbox.y1
        if gap > MAX_LINE_GAP * max(h, lh) or line.bbox.y0 < self.last.bbox.y0:
            return False
        overlap = _x_overlap(line.bbox, self.bbox)
        narrower = min(line.bbox.width, self.bbox.width)
        wider = max(line.bbox.width, self.bbox.width)
        if narrower <= 0:
            return False
        left_aligned = abs(line.bbox.x0 - self.bbox.x0) <= 1.5 * h
        if narrower < MIN_WIDTH_SHARE * wider:
            # a short label next to / under a long line is a diagram label or a table cell - unless it
            # is the left-aligned tail of an unfinished sentence (…与同伴说一说你的 / 设计意图。)
            # the first line of a paragraph is often indented by two characters: its tail then
            # starts to the LEFT of it (小朋友，数学就在我们身边，你和数学一定会成为 / 好朋友。)
            indented_first = (len(self.lines) == 1 and 0 < self.last.bbox.x0 - line.bbox.x0 <= FIRST_LINE_INDENT * h)
            # a numbered item wraps with a hanging indent: its tail starts to the RIGHT of the
            # marker ((1)说一说，图中有哪些数学 / 信息？)
            hanging = (len(self.lines) == 1 and is_list_item(self.lines[0].source_text)
                       and 0 < line.bbox.x0 - self.last.bbox.x0 <= FIRST_LINE_INDENT * h)
            tail = ((abs(line.bbox.x0 - self.last.bbox.x0) <= 0.6 * h or indented_first or hanging)
                    and line.bbox.width < self.last.bbox.width
                    and self.last.source_text.rstrip()[-1:] not in _SENTENCE_END + "：:"
                    and _letter_count(self.last.source_text) >= 8 and gap <= MAX_LINE_GAP * h)
            if not tail:
                return False
            if indented_first or hanging:
                return True  # the indent is the paragraph's shape, not a new column
        centre_shift = abs((line.bbox.x0 + line.bbox.x1) / 2 - (self.bbox.x0 + self.bbox.x1) / 2)
        if self._left_aligned(h) and abs(line.bbox.x0 - self.bbox.x0) > MAX_X0_JUMP * h and centre_shift > h:
            return False  # another column: a speech bubble or label beside / below the instruction
        if self.last.source_text.rstrip()[-1:] in _SENTENCE_END and (
                abs(line.bbox.x0 - self.bbox.x0) > 0.6 * h or gap > 0.5 * h):
            return False  # the sentence ended; an indented or separated line starts something new
        return overlap >= MIN_X_OVERLAP * narrower or (left_aligned and overlap > 0)

    def _left_aligned(self, h: float) -> bool:
        x0s = [l.bbox.x0 for l in self.lines]
        return max(x0s) - min(x0s) <= 0.5 * h

    def add(self, line: TextSegment) -> None:
        self.lines.append(line)
        self.bbox = self.bbox.union(line.bbox)
        self.heights.append(line.bbox.height)


def _letter_count(text: str) -> int:
    return sum(c.isalpha() for c in text)


_FORMULA_CHARS = set("0123456789=+-−×÷().,（）:：/%")


def _formula_like(text: str) -> bool:
    """A line that is mostly digits and operators (a worked equation with a unit)."""
    t = text.strip()
    if not t or "=" not in t:
        return False
    return sum(c in _FORMULA_CHARS or c.isspace() for c in t) >= 0.6 * len(t)


def _join_lines(texts: list[str], lang: Lang) -> str:
    """Join OCR lines into paragraph text. Consecutive equation lines keep their line
    breaks (each worked step stays on its own line); prose lines are joined the way
    the language writes it (no space for CJK, a space for Latin scripts)."""
    out = ""
    prev = ""
    for raw in texts:
        t = raw.strip()
        if not t:
            continue
        if out:
            if _formula_like(prev) and _formula_like(t):
                out += "\n"
            elif is_cjk(lang):
                if out[-1].isascii() and out[-1].isalnum() and t[:1].isascii() and t[:1].isalnum():
                    out += " "
            else:
                out += " "
        out += t
        prev = t
    return out


MAX_ROW_GAP = 5.0
"""Pieces of one sentence split by an answer blank or a picture (same row, same colour)
are joined when the gap is at most this many line heights."""
BLANK = "___"


def _same_row(a: TextSegment, b: TextSegment) -> bool:
    ha, hb = a.bbox.height, b.bbox.height
    if ha <= 0 or hb <= 0 or not (0.75 <= ha / hb <= 1.33):
        return False
    overlap = min(a.bbox.y1, b.bbox.y1) - max(a.bbox.y0, b.bbox.y0)
    return overlap >= 0.7 * min(ha, hb)


BlankCheck = Callable[[TextSegment, TextSegment], bool]


def _row_joinable(left: TextSegment, right: TextSegment, blank_check: Optional[BlankCheck] = None) -> bool:
    """``right`` continues the sentence of ``left`` on the same row after an answer blank:
    ``七巧板由 ___ 种图形组成。``, ``答：还剩下 ___ 个果子。``. Without ``blank_check`` (or
    when it finds no underline in the gap: a picture, a box, a bubble border) nothing joins."""
    if blank_check is None:
        return False
    if not (left.translate and right.translate) or not _same_row(left, right):
        return False
    if _color_distance(left.style.color, right.style.color) > MAX_COLOR_DISTANCE:
        return False
    h = max(left.bbox.height, right.bbox.height)
    gap = right.bbox.x0 - left.bbox.x1
    if gap < -0.2 * h or gap > MAX_ROW_GAP * h:
        return False
    lt, rt = left.source_text.strip(), right.source_text.strip()
    if not lt or not rt or lt[-1] in _SENTENCE_END or _STARTS_NEW_RE.match(rt) or is_list_item(rt):
        return False
    # table cells and labels side by side are short nouns; a sentence piece ends the sentence
    # or is long enough to be one
    if not (_letter_count(lt) >= 2 and (rt[-1] in _SENTENCE_END + "，," or _letter_count(rt) >= 5)):
        return False
    return blank_check(left, right)


def underline_blank_check(loaded_for: Callable[[int], Optional[object]]) -> BlankCheck:
    """A :data:`BlankCheck` that looks at the page image between two OCR pieces: the gap is
    an answer blank when its lower part holds a horizontal rule across most of it and the
    rest of the gap is empty. ``loaded_for(xref)`` returns the decoded image (cached)."""
    def check(left: TextSegment, right: TextSegment) -> bool:
        if left.image is None or right.image is None or left.image.xref != right.image.xref:
            return False
        loaded = loaded_for(left.image.xref)
        if loaded is None:
            return False
        rgb = loaded.rgb  # type: ignore[attr-defined]
        lx0, ly0, lx1, ly1 = (int(v) for v in left.image.pixel_box)
        rx0, ry0, rx1, ry1 = (int(v) for v in right.image.pixel_box)
        x0, x1 = lx1 + 1, rx0 - 1
        y0, y1 = min(ly0, ry0), max(ly1, ry1)
        h = y1 - y0
        if x1 - x0 < max(4, int(0.5 * h)) or h < 6:
            return False
        y1 = min(rgb.shape[0], y1 + max(2, h // 5))  # underlines may sit just below the glyph boxes
        region = rgb[y0:y1, x0:x1]
        bg, _share = _dominant_colour(region)
        ink = np.abs(region.astype(np.int32) - bg.astype(np.int32)).max(axis=2) > 60
        rows = ink.mean(axis=1)
        split = int(0.55 * len(rows))
        rule = rows[split:].max() if len(rows) > split else 0.0
        upper = float(ink[:split].mean()) if split > 0 else 1.0
        if rule >= 0.7 and upper <= 0.08:
            return True  # an answer-blank underline
        # a narrow empty gap: OCR split one sentence at a space or a quoted mark
        return bool(x1 - x0 <= 1.5 * h and float(ink.mean()) <= 0.03)
    return check


PLACE_VALUE_ABBREVIATIONS = {"个位": "O", "十位": "T", "百位": "H", "千位": "Th", "万位": "TTh", "十万位": "HTh",
                             "百万位": "M", "千万位": "TM", "亿位": "HM"}
"""Column headers over a vertical form or place-value chart, as English books abbreviate them."""
_UNIT_NUMERAL_RE = re.compile(r"[一二三四五六七八九十]")
LONE_CHAR_REASON = "single character with low OCR confidence"


def _single_cjk(seg: TextSegment) -> bool:
    t = seg.source_text.strip()
    return len(t) == 1 and "\u3400" <= t <= "\u9fff"


def _glyph_joinable(left: TextSegment, right: TextSegment) -> bool:
    """A lone character the detector cut off its word (目|录, 数|学, 一|共有), or a bare unit
    numeral set before its heading (一  加与减): the pieces are one line."""
    if not (_single_cjk(left) or _single_cjk(right)):
        return False
    h = max(left.bbox.height, right.bbox.height)
    gap = right.bbox.x0 - left.bbox.x1
    if gap < -0.2 * h:
        return False
    if _single_cjk(left) and _UNIT_NUMERAL_RE.fullmatch(left.source_text.strip()) \
            and _letter_count(right.source_text) >= 2 and not _single_cjk(right):
        # a bare numeral is shorter than the full-height characters of its heading (二 has no
        # vertical stroke): it only has to sit within the heading's height
        inside = left.bbox.y0 >= right.bbox.y0 - 0.3 * h and left.bbox.y1 <= right.bbox.y1 + 0.3 * h
        # the numeral is often set apart in colour (white on a badge, red): colour does not decide
        return inside and gap <= 2.5 * h
    if not _same_row(left, right):
        return False
    if _single_cjk(left) and _single_cjk(right):
        # the two characters of a title set wide apart (目  录, 数  学): same size, any colour
        # (a decorated glyph's colour estimate is unreliable)
        return gap <= 1.2 * h and abs(left.bbox.height - right.bbox.height) <= 0.3 * h
    if _color_distance(left.style.color, right.style.color) > MAX_COLOR_DISTANCE:
        return False
    return gap <= 0.6 * h


def _glyph_join_text(left: TextSegment, right: TextSegment) -> str:
    h = max(left.bbox.height, right.bbox.height)
    numeral = _single_cjk(left) and _UNIT_NUMERAL_RE.fullmatch(left.source_text.strip())
    sep = " " if numeral and right.bbox.x0 - left.bbox.x1 > 0.6 * h else ""
    return left.source_text.strip() + sep + right.source_text.strip()


LineCheck = Callable[[TextSegment], bool]


def bullet_check(loaded_for: Callable[[int], Optional[object]]) -> LineCheck:
    """A check for a bullet glyph (●, a coloured dot or square) printed just before an OCR
    line: such a line starts a new paragraph (a list of rules), however close it is to the
    line above. ``loaded_for(xref)`` returns the decoded image (cached)."""
    import cv2

    def check(line: TextSegment) -> bool:
        if line.image is None:
            return False
        loaded = loaded_for(line.image.xref)
        if loaded is None:
            return False
        rgb = loaded.rgb  # type: ignore[attr-defined]
        x0, y0, x1, y1 = (int(v) for v in line.image.pixel_box)
        h = y1 - y0
        rx0, rx1 = max(0, x0 - int(1.6 * h)), max(0, x0 - max(2, h // 8))
        ry0, ry1 = max(0, y0 - h // 6), min(rgb.shape[0], y1 + h // 6)
        if h < 8 or rx1 - rx0 < h // 2:
            return False
        region = rgb[ry0:ry1, rx0:rx1]
        bg, share = _dominant_colour(region)
        if share < STRIPE_MIN_SHARE:
            return False
        ink = (np.abs(region.astype(np.int32) - bg.astype(np.int32)).max(axis=2) > GLYPH_DIFF).astype(np.uint8)
        n, _labels, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
        if n != 2:
            return False  # nothing, or more than one blob (text)
        bx, by, bw, bh, area = (int(v) for v in stats[1])
        if not (0.2 * h <= bw <= 0.8 * h and 0.2 * h <= bh <= 0.8 * h) or area < 0.5 * bw * bh:
            return False  # not a compact dot or square
        cy = by + bh / 2
        return (ry1 - ry0) * 0.25 <= cy <= (ry1 - ry0) * 0.75
    return check


def _join_row_pieces(candidates: list[TextSegment], blank_check: Optional[BlankCheck] = None
                     ) -> tuple[list[TextSegment], dict[str, list[TextSegment]]]:
    """Join same-row sentence pieces into one virtual line each (blank marked ``___``).
    Returns the lines for grouping and, per virtual line id, the OCR lines it stands for."""
    by_x = sorted(candidates, key=lambda l: (l.bbox.x0, l.bbox.y0))
    used: set[str] = set()
    units: dict[str, list[TextSegment]] = {}
    out: list[TextSegment] = []
    for line in by_x:  # left to right: a chain starts at the leftmost piece of its row
        if line.id in used:
            continue
        chain = [line]
        while True:
            last = chain[-1]
            nxt = next((c for c in by_x if c.id not in used and c is not last and c not in chain
                        and c.bbox.x0 >= last.bbox.x1 - 0.2 * last.bbox.height
                        and (_glyph_joinable(last, c) or _row_joinable(last, c, blank_check))), None)
            if nxt is None:
                break
            chain.append(nxt)
        used.update(c.id for c in chain)
        if len(chain) == 1:
            out.append(line)
            continue
        text = chain[0].source_text.strip()
        bbox = chain[0].bbox
        for prev, cur in zip(chain, chain[1:]):
            if _glyph_joinable(prev, cur):
                text = _glyph_join_text(prev.model_copy(update={"source_text": text}), cur)
            else:
                gap = cur.bbox.x0 - prev.bbox.x1
                wide = gap > 1.6 * max(prev.bbox.height, cur.bbox.height)  # an underline blank, not a space
                text += (BLANK if wide else "") + cur.source_text.strip()
            bbox = bbox.union(cur.bbox)
        virtual = chain[0].model_copy(update={"bbox": bbox, "source_text": text, "protected_text": text})
        units[virtual.id] = chain
        out.append(virtual)
    return out, units


def _paragraph_segment(para: _Para, index: int, page_index: int, source_lang: Lang,
                       page_median_height: float, members: Optional[list[str]] = None) -> TextSegment:
    lines = para.lines
    text = _join_lines([l.source_text for l in lines], source_lang)
    protected, fragments = protect_text(text, source_lang)
    h = para.median_height
    size = max(4.0, round(h * FONT_HEIGHT_RATIO, 1))
    if len(lines) > 1:
        pitches = [b.bbox.y0 - a.bbox.y0 for a, b in zip(lines, lines[1:]) if b.bbox.y0 > a.bbox.y0]
        line_height = statistics.median(pitches) / h if pitches else 1.25
        line_height = min(1.8, max(1.05, line_height))
    else:
        line_height = 1.2
    centred = all(abs((l.bbox.x0 + l.bbox.x1) / 2 - (para.bbox.x0 + para.bbox.x1) / 2) <= 0.08 * para.bbox.width
                  for l in lines) and len(lines) > 1
    align = "center" if centred else "left"
    letters = sum(ch.isalpha() for ch in text)
    han = sum("\u3400" <= ch <= "\u9fff" for ch in text)
    box = para.bbox
    vertical = (len(lines) == 1 and han >= 2 and box.width > 0 and box.height >= 1.5 * box.width
                and box.height / box.width >= 0.6 * han)
    column_header = PLACE_VALUE_ABBREVIATIONS.get(text.strip()) if vertical else None
    if column_header is not None:
        # 十位 / 个位 stacked over the columns of a vertical form: English books head the columns
        # with the abbreviations T / O (H, Th ...), set upright at the column's width
        vertical = False
        size = max(4.0, round(box.width * FONT_HEIGHT_RATIO, 1))
        role = "label"
    elif vertical:
        # other stacked labels (被减数, 结束): the English is set running down the column
        size = max(4.0, round(min(box.width, box.height / han) * FONT_HEIGHT_RATIO, 1))
        role = "label"
    elif len(lines) == 1 and page_median_height > 0 and h >= 1.4 * page_median_height:
        role = "heading"
    elif len(lines) == 1 and letters <= 8:
        role = "label"
    else:
        role = "body"
    first = lines[0]
    translate = not is_fully_protected(protected) and any(l.translate for l in lines)
    if column_header is not None:
        return TextSegment(
            id=f"p{page_index}_s{index}", page=page_index, kind=SegmentKind.TEXT, bbox=para.bbox,
            source_text=text, protected_text=protected, protected=fragments,
            style=SegmentStyle(size=size, color=first.style.color, align="center", line_height=1.1, role="label"),
            translate=False, skip_reason=f"place-value column header, set as {column_header}",
            translated_text=column_header, translation_raw=column_header, origin="ocr",
            members=members if members is not None else [l.id for l in lines], reading_order=index)
    return TextSegment(
        id=f"p{page_index}_s{index}",
        page=page_index,
        kind=SegmentKind.TEXT,
        bbox=para.bbox,
        source_text=text,
        protected_text=protected,
        protected=fragments,
        style=SegmentStyle(size=size, color=first.style.color, align=align, line_height=line_height, role=role,
                           is_vertical=vertical),
        translate=translate,
        skip_reason="" if translate else "no translatable text (numbers / formula only)",
        origin="ocr",
        members=members if members is not None else [l.id for l in lines],
        reading_order=index,
    )


_ENUM_LINE_RE = re.compile(r"^\s*(\d{1,2})[.．、]")
_ENUM_FUSED_RE = re.compile(r"^(\s*)(\d{1,2})[.．](\d{1,4})(?![.．\d])(?=.*\S)")


def space_fused_enumerators(lines: list[TextSegment]) -> int:
    """``4.10个小朋友在做游戏`` -> ``4. 10个...``: the exercise number and the number that
    starts its text were read as one decimal. Only a number that continues the page's
    exercise numbering (1, or the one after the last enumerator seen) is taken for an
    enumerator; ``2.5米`` elsewhere stays a decimal. ``lines`` must be in reading order."""
    seen: set[int] = set()
    changed = 0
    for line in lines:
        text = line.source_text
        m = _ENUM_FUSED_RE.match(text)
        if m:
            n = int(m.group(2))
            if 1 <= n <= 20 and n not in seen and (n == 1 or n - 1 in seen) and m.group(3)[0] != "0":
                line.source_text = f"{m.group(1)}{n}. {m.group(3)}{text[m.end():]}"
                seen.add(n)
                changed += 1
                continue
        m = _ENUM_LINE_RE.match(text)
        if m:
            seen.add(int(m.group(1)))
    return changed


def group_ocr_lines(lines: list[TextSegment], page_index: int, source_lang: Lang,
                    blank_check: Optional[BlankCheck] = None,
                    bullet: Optional[LineCheck] = None) -> list[TextSegment]:
    """Merge the OCR line segments of one scanned page into paragraph segments.

    The merged lines are marked ``translate=False`` with ``skip_reason``
    ``"merged into paragraph <id>"`` (they are erased from the image later);
    lines that cannot be merged (labels, slanted text, foreign script) are left
    untouched. Returns the new paragraph segments in reading order.
    """
    for line in lines:
        if line.page == page_index and line.skip_reason == UNIT_DROPPED:
            line.skip_reason = f"{MERGED} {UNIT_DROPPED}"  # erased with the merged lines, nothing set instead
    # a line set aside for a dropped picture may just be the first or last line of a sentence that
    # wraps (我的花生比 / 你的多): it joins a paragraph when the joined text has no gap left
    pending = {l.id for l in lines if l.page == page_index and l.kind == SegmentKind.IMAGE_TEXT
               and l.image is not None and l.skip_reason == INLINE_PICTOGRAMS}
    # a lone character read with low confidence may be the piece of a word the detector cut off
    # (目|录) or the numeral of a unit heading (一 加与减): it joins its row neighbour, else it stays
    lone = {l.id for l in lines if l.page == page_index and l.kind == SegmentKind.IMAGE_TEXT
            and l.image is not None and l.skip_reason.startswith(LONE_CHAR_REASON)}
    for line in lines:
        if line.id in pending or line.id in lone:
            line.translate = True
    candidates = [l for l in lines if l.page == page_index and _mergeable(l)]
    if not candidates:
        for line in lines:
            if line.id in lone:
                line.translate = False
        return []
    candidates, units = _join_row_pieces([c for c in candidates if c.id not in pending], blank_check)
    joined = {u.id for chain in units.values() for u in chain}
    for line in lines:
        if line.id in lone and line.id not in joined:
            line.translate = False
    candidates = [c for c in candidates if c.id not in lone or c.id in joined]
    candidates += [l for l in lines if l.id in pending]
    candidates.sort(key=lambda l: (round(l.bbox.y0, 1), l.bbox.x0))
    if not candidates:
        return []
    space_fused_enumerators(candidates)
    bullets = {l.id for l in candidates if bullet is not None and l.id not in units and bullet(l)}
    page_median_height = statistics.median(l.bbox.height for l in candidates)
    paragraphs: list[_Para] = []
    for line in candidates:
        if line.id in bullets:
            paragraphs.append(_Para(line))  # a bulleted rule or question: always its own paragraph
            continue
        best: Optional[_Para] = None
        best_overlap = -1.0
        for para in paragraphs:
            if para.accepts(line):
                overlap = _x_overlap(line.bbox, para.bbox)
                if overlap > best_overlap:
                    best, best_overlap = para, overlap
        if best is None:
            paragraphs.append(_Para(line))
        else:
            best.add(line)
    for para in paragraphs:
        if any(l.id in pending for l in para.lines) and has_pictogram_gap(
                _join_lines([l.source_text for l in para.lines], source_lang)):
            para.lines = [l for l in para.lines if l.id not in pending]
            if para.lines:
                para.bbox = para.lines[0].bbox
                for l in para.lines[1:]:
                    para.bbox = para.bbox.union(l.bbox)
                para.heights = [l.bbox.height for l in para.lines]
    for line in lines:
        if line.id in pending:
            line.translate = False  # merged lines are re-marked below; the others stay in the picture
    paragraphs = [p for p in paragraphs if p.lines]
    paragraphs.sort(key=lambda p: (round(p.bbox.y0 / 20), p.bbox.x0))
    out: list[TextSegment] = []
    for i, para in enumerate(paragraphs):
        originals = [u for l in para.lines for u in units.get(l.id, [l])]
        seg = _paragraph_segment(para, i, page_index, source_lang, page_median_height,
                                 members=[u.id for u in originals])
        if not seg.translate and not seg.translated_text:
            continue  # formulas and numbers are not translated: they stay in the picture untouched
        for u in originals:
            u.translate = False
            u.skip_reason = f"{MERGED} {seg.id}"
            seg.anchors.update(u.anchors)
        out.append(seg)
    return out


def build_overlay_segments(doc: TranslatedDocument, scanned: set[int],
                           pdf: Optional[Union[str, Path, pymupdf.Document]] = None) -> list[TextSegment]:
    """Paragraph segments for every scanned page of ``doc`` (lines are marked merged). With
    ``pdf`` the page images are consulted to join sentence pieces split by answer blanks."""
    out: list[TextSegment] = []
    pdf_doc = None
    if pdf is not None:
        pdf_doc = pdf if isinstance(pdf, pymupdf.Document) else pymupdf.open(str(pdf))
    cache: dict[int, object] = {}

    def loaded_for(xref: int) -> Optional[object]:
        if pdf_doc is None:
            return None
        if xref not in cache:
            try:
                cache.clear()  # one page image at a time keeps memory flat
                cache[xref] = load_image(pdf_doc, xref)
            except Exception as exc:  # noqa: BLE001 - no pixels, no joining
                log.debug("cannot load image %d for blank detection: %s", xref, exc)
                cache[xref] = None
        return cache[xref]

    check = underline_blank_check(loaded_for) if pdf_doc is not None else None
    bullets = bullet_check(loaded_for) if pdf_doc is not None else None
    try:
        for page_index in sorted(scanned):
            lines = [s for s in doc.segments if s.page == page_index and s.kind == SegmentKind.IMAGE_TEXT]
            suppress_patch_duplicates(lines, page_index)
            out.extend(group_ocr_lines(lines, page_index, doc.source_lang, check, bullets))
            relink_patch_duplicates(lines, page_index)
    finally:
        if pdf_doc is not None and not isinstance(pdf, pymupdf.Document):
            pdf_doc.close()
    return out


# --------------------------------------------------------------------------- #
# erasing merged lines from the page images
# --------------------------------------------------------------------------- #


def erase_merged_lines(pdf_doc: pymupdf.Document, doc: TranslatedDocument) -> int:
    """Erase the glyphs of every merged OCR line from its image (flat fill or
    inpainting, as the repaint mode does) and replace the image in ``pdf_doc``.
    Returns the number of images modified."""
    by_image: dict[tuple[int, int], list[TextSegment]] = defaultdict(list)
    image_lines: dict[tuple[int, int], list[TextSegment]] = defaultdict(list)
    for seg in doc.segments:
        if seg.kind == SegmentKind.IMAGE_TEXT and seg.image is not None:
            image_lines[(seg.page, seg.image.xref)].append(seg)
            if seg.skip_reason.startswith(MERGED):
                by_image[(seg.page, seg.image.xref)].append(seg)
    modified = 0
    for (page_index, _xref), segs in by_image.items():
        if page_index >= pdf_doc.page_count:
            continue
        page = pdf_doc[page_index]
        ref = segs[0].image
        assert ref is not None
        placement = resolve_placement(pdf_doc, page, ref)
        if placement is None:
            log.warning("page %d: image for %d merged lines not found; text left in the picture", page_index, len(segs))
            continue
        try:
            loaded = load_image(pdf_doc, placement.xref)
        except ValueError as exc:
            log.warning("page %d: cannot decode image xref %d: %s", page_index, placement.xref, exc)
            continue
        original = np.array(loaded.rgb, copy=True)
        original_alpha = np.array(loaded.alpha, copy=True) if loaded.alpha is not None else None
        canvas = np.array(loaded.rgb, copy=True)  # MuPDF-decoded buffers are read-only
        alpha = np.array(loaded.alpha, copy=True) if loaded.alpha is not None else None
        for seg in segs:
            assert seg.image is not None
            x0, y0, x1, y1 = seg.image.pixel_box
            x0, y0 = max(0, int(x0)), max(0, int(y0))
            x1, y1 = min(loaded.width, int(x1)), min(loaded.height, int(y1))
            if x1 <= x0 or y1 <= y0:
                continue
            others = [tuple(int(v) for v in o.image.pixel_box) for o in image_lines[(page_index, _xref)]
                      if o is not seg and o.image is not None]
            how = _erase_glyphs(canvas, alpha, original, original_alpha, (x0, y0, x1, y1), others)
            for _key, (_ax, ax0, ay0, ax1, ay1) in seg.anchors.items():
                # the picture is drawn inline in the translation: remove it from its old place
                _clear_box(canvas, alpha, original, original_alpha,
                           (max(0, ax0 - 2), max(0, ay0 - 2), min(loaded.width, ax1 + 2), min(loaded.height, ay1 + 2)))
            seg.render = RenderInfo(font_size=0.0, scale=1.0, notes=f"{how}; translation placed as page text")
        stream = encode_image(canvas, alpha, loaded.ext, qtables=loaded.jpeg_qtables,
                              subsampling=loaded.jpeg_subsampling)
        try:
            replace_image(page, placement.xref, stream)
            modified += 1
        except Exception as exc:  # noqa: BLE001 - keep the run going; QA reports the leftovers
            log.error("page %d: replace_image(xref=%d) failed: %s", page_index, placement.xref, exc)
    return modified


def paragraphs_to_restore(doc: TranslatedDocument) -> list[TextSegment]:
    """OCR paragraphs whose merged lines were erased but that carry no rendered text:
    left in the source language by the layout (too long to set legibly) or not set at
    all (no usable translation)."""
    out: list[TextSegment] = []
    for seg in doc.segments:
        if seg.origin != "ocr" or seg.kind != SegmentKind.TEXT:
            continue
        r = seg.render
        if r is None or (r.font_size <= 0 and r.notes.startswith("left in source language")):
            out.append(seg)
    return out


def restore_lines(pdf_doc: pymupdf.Document, source_doc: pymupdf.Document, doc: TranslatedDocument,
                  paragraphs: list[TextSegment]) -> int:
    """Copy the original pixels of the merged lines of ``paragraphs`` from ``source_doc``
    back into the (erased) images of ``pdf_doc``. Returns the number of images modified."""
    wanted = {p.id for p in paragraphs}
    by_image: dict[tuple[int, int], list[TextSegment]] = defaultdict(list)
    for seg in doc.segments:
        if seg.kind != SegmentKind.IMAGE_TEXT or seg.image is None or not seg.skip_reason.startswith(MERGED):
            continue
        if seg.skip_reason[len(MERGED):].strip() in wanted:
            by_image[(seg.page, seg.image.xref)].append(seg)
    modified = 0
    for (page_index, _xref), segs in by_image.items():
        if page_index >= pdf_doc.page_count or page_index >= source_doc.page_count:
            continue
        ref = segs[0].image
        assert ref is not None
        dst_place = resolve_placement(pdf_doc, pdf_doc[page_index], ref)
        src_place = resolve_placement(source_doc, source_doc[page_index], ref)
        if dst_place is None or src_place is None:
            log.warning("page %d: cannot restore %d line(s): image not found", page_index, len(segs))
            continue
        try:
            current = load_image(pdf_doc, dst_place.xref)
            original = load_image(source_doc, src_place.xref)
        except ValueError as exc:
            log.warning("page %d: cannot decode image for restoring: %s", page_index, exc)
            continue
        if (current.width, current.height) != (original.width, original.height):
            continue
        canvas = np.array(current.rgb, copy=True)
        alpha = np.array(current.alpha, copy=True) if current.alpha is not None else None
        pad = GLYPH_DILATE_PX + 3
        # the lines that stay erased (their paragraphs are set in English) and the inline pictures drawn
        # in the text keep their erased pixels: a large box restored around them (a watermark misread
        # as text) must not bring their Chinese back
        keep = np.zeros((current.height, current.width), bool)
        by_para = {p.id: p for p in doc.segments if p.kind == SegmentKind.TEXT}
        for other in doc.segments:
            if other.kind != SegmentKind.IMAGE_TEXT or other.image is None or other.page != page_index \
                    or other.image.xref != _xref or not other.skip_reason.startswith(MERGED):
                continue
            parent = other.skip_reason[len(MERGED):].strip()
            if parent in wanted:
                continue
            ox0, oy0, ox1, oy1 = (int(v) for v in other.image.pixel_box)
            keep[max(0, oy0 - pad):max(0, oy1 + pad), max(0, ox0 - pad):max(0, ox1 + pad)] = True
            para = by_para.get(parent)
            for _key, (_ax, ax0, ay0, ax1, ay1) in (para.anchors.items() if para is not None else []):
                keep[max(0, ay0 - 2):max(0, ay1 + 2), max(0, ax0 - 2):max(0, ax1 + 2)] = True
        for seg in segs:
            assert seg.image is not None
            x0, y0, x1, y1 = (int(v) for v in seg.image.pixel_box)
            x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
            x1, y1 = min(current.width, x1 + pad), min(current.height, y1 + pad)
            if x1 <= x0 or y1 <= y0:
                continue
            take = ~keep[y0:y1, x0:x1]
            canvas[y0:y1, x0:x1][take] = original.rgb[y0:y1, x0:x1][take]
            if alpha is not None and original.alpha is not None:
                alpha[y0:y1, x0:x1][take] = original.alpha[y0:y1, x0:x1][take]
            seg.render = RenderInfo(font_size=0.0, scale=1.0, notes="original text restored (translation not set)")
        stream = encode_image(canvas, alpha, current.ext, qtables=current.jpeg_qtables,
                              subsampling=current.jpeg_subsampling)
        try:
            replace_image(pdf_doc[page_index], dst_place.xref, stream)
            modified += 1
        except Exception as exc:  # noqa: BLE001
            log.error("page %d: restoring image xref %d failed: %s", page_index, dst_place.xref, exc)
    return modified


# --------------------------------------------------------------------------- #
# watermarks
# --------------------------------------------------------------------------- #

WATERMARK = "watermark fragment"
"""``skip_reason`` of OCR lines recognised as pieces of a repeated page watermark."""
MIN_SLANTED_LINES = 3
"""Slanted lines needed before their characters are treated as a watermark alphabet."""
MIN_CHAR_SHARE = 0.1
"""A character must occur in at least this share of the slanted lines (and in >= 2 of
them) to belong to the watermark alphabet."""
MIN_SLANTED_SHARE = 0.5
"""... and at least this share of all its occurrences must be in slanted lines."""
MAX_FRAGMENT_LETTERS = 12
LOW_CONFIDENCE = 0.8
"""OCR confidence below which a short, half-watermark line counts as a misread fragment."""


def watermark_alphabet(doc: TranslatedDocument) -> set[str]:
    """Letters that make up the document's diagonal watermark, learnt from the OCR
    lines skipped as slanted text (a publisher's name printed across every page)."""
    from collections import Counter

    lines = [s for s in doc.segments if s.kind == SegmentKind.IMAGE_TEXT]
    slanted = [s for s in lines if s.skip_reason.startswith("slanted text")]
    if len(slanted) < MIN_SLANTED_LINES:
        return set()
    counts: Counter[str] = Counter()
    for seg in slanted:
        for ch in set(c for c in seg.source_text if c.isalpha()):
            counts[ch] += 1
    others: Counter[str] = Counter()
    for seg in lines:
        if seg not in slanted:
            for ch in set(c for c in seg.source_text if c.isalpha()):
                others[ch] += 1
    import math

    needed = max(2, math.ceil(MIN_CHAR_SHARE * len(slanted)))
    # A watermark letter occurs mostly in slanted lines; a letter that is common in the
    # upright text as well (米 of distance labels along slanted roads) is ordinary text.
    alphabet = {ch for ch, n in counts.items()
                if n >= needed and n >= MIN_SLANTED_SHARE * (n + others.get(ch, 0))}
    return alphabet if len(alphabet) >= 3 else set()


WATERMARK_CONFUSIONS = set("乐东字五品反童厶尔中")
"""Characters the OCR reads for pieces of a semi-transparent watermark (京 -> 乐 / 东,
出 -> 五, 版 -> 反): inside the watermark band they count as watermark letters."""
BAND_MIN_HALF_WIDTH = 0.025
"""Minimum half-width of the watermark band (share of the page height)."""
BAND_MAX_LETTERS = 4
BAND_END_MARGIN = 0.12
"""How far (share of the page width) the band reaches beyond the outermost slanted piece."""
BAND_CONFIDENCE = 0.9
"""Inside the band, a short line half made of watermark letters read below this confidence
is a misread piece of the watermark."""


def _touches_band(seg: TextSegment, band: tuple[float, float, float, float, float], size: tuple[float, float]) -> bool:
    """True when the watermark's diagonal crosses the segment's box (for trimming watermark
    letters glued to a long genuine line whose centre is off the band)."""
    slope, intercept, half, x_min, x_max = band
    w, h = size
    if w <= 0 or h <= 0:
        return False
    for x in (seg.bbox.x0 / w, (seg.bbox.x0 + seg.bbox.x1) / 2 / w, seg.bbox.x1 / w):
        if x_min <= x <= x_max and seg.bbox.y0 / h - half <= slope * x + intercept <= seg.bbox.y1 / h + half:
            return True
    return False


def watermark_band(doc: TranslatedDocument, alphabet: set[str]) -> Optional[tuple[float, float, float, float, float]]:
    """``(slope, intercept, half_width, x_min, x_max)`` of the diagonal band the watermark
    occupies, in page-relative coordinates (x / width, y / height), fitted through the
    centres of the slanted watermark lines of the whole document (it is printed at the
    same place on every page); None when there are too few of them or they do not line up."""
    sizes = {pi.index: (pi.width, pi.height) for pi in doc.pages}
    pts: list[tuple[float, float]] = []
    for seg in doc.segments:
        if seg.kind != SegmentKind.IMAGE_TEXT or not seg.skip_reason.startswith("slanted text"):
            continue
        letters = [c for c in seg.source_text if c.isalpha()]
        if not letters or sum(c in alphabet for c in letters) * 2 < len(letters):
            continue
        w, h = sizes.get(seg.page, (0.0, 0.0))
        if w <= 0 or h <= 0:
            continue
        pts.append(((seg.bbox.x0 + seg.bbox.x1) / 2 / w, (seg.bbox.y0 + seg.bbox.y1) / 2 / h))
    if len(pts) < MIN_SLANTED_LINES:
        return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    if float(xs.max() - xs.min()) < 0.1:
        return None
    for _ in range(2):  # least squares, then once more without the outliers
        slope, intercept = np.polyfit(xs, ys, 1)
        res = np.abs(ys - (slope * xs + intercept))
        keep = res <= max(3 * float(np.median(res)), 0.01)
        if keep.sum() < MIN_SLANTED_LINES or keep.all():
            break
        xs, ys = xs[keep], ys[keep]
    res = np.abs(ys - (slope * xs + intercept))
    if float(np.median(res)) > 0.02:
        return None  # no consistent diagonal: several watermarks or none
    half = max(BAND_MIN_HALF_WIDTH, 3 * float(np.median(res)))
    # the first and last letters (北, 社) lie beyond the centres of the recognised pieces
    return float(slope), float(intercept), half, float(xs.min()) - BAND_END_MARGIN, float(xs.max()) + BAND_END_MARGIN


def _in_band(seg: TextSegment, band: tuple[float, float, float, float, float], size: tuple[float, float]) -> bool:
    slope, intercept, half, x_min, x_max = band
    w, h = size
    if w <= 0 or h <= 0:
        return False
    x = (seg.bbox.x0 + seg.bbox.x1) / 2 / w
    y = (seg.bbox.y0 + seg.bbox.y1) / 2 / h
    return x_min <= x <= x_max and abs(y - (slope * x + intercept)) <= half


def suppress_watermark_fragments(doc: TranslatedDocument) -> int:
    """Skip OCR lines that consist only of watermark letters (the un-slanted or
    partially recognised pieces of the watermark) and trim watermark runs glued to
    the start or end of a genuine line ("观察物体！版社" -> "观察物体！").
    Returns the number of lines changed."""
    alphabet = watermark_alphabet(doc)
    if not alphabet:
        return 0
    band = watermark_band(doc, alphabet)
    band_letters = alphabet | WATERMARK_CONFUSIONS | set("北京师范大学出版社")
    sizes = {pi.index: (pi.width, pi.height) for pi in doc.pages}
    changed = 0
    for seg in doc.segments:
        if seg.kind != SegmentKind.IMAGE_TEXT or not seg.translate:
            continue
        text = seg.source_text
        letters = [c for c in text if c.isalpha()]
        if not letters:
            continue
        confidence = seg.image.confidence if seg.image is not None else 1.0
        size = sizes.get(seg.page, (0.0, 0.0))
        inside = band is not None and _in_band(seg, band, size)
        touching = inside or (band is not None and _touches_band(seg, band, size))
        if inside and len(letters) <= BAND_MAX_LETTERS and (
                all(c in band_letters for c in letters)
                or (sum(c in band_letters for c in letters) * 2 >= len(letters) and confidence < BAND_CONFIDENCE)):
            # an upright or misread piece of the watermark (学, 五, 反社, 中版社) lying on the watermark's diagonal
            seg.translate = False
            seg.skip_reason = WATERMARK
            changed += 1
            continue
        in_alphabet = sum(c in alphabet for c in letters)
        bare = text.strip() == "".join(letters)  # only letters: no digits or punctuation around them
        if len(letters) <= MAX_FRAGMENT_LETTERS and (
                (in_alphabet == len(letters) and (len(letters) >= 2 or bare))
                or (len(letters) <= 4 and in_alphabet * 2 >= len(letters) and confidence < LOW_CONFIDENCE)):
            # all letters from the watermark, or a short low-confidence piece half made of them
            # (a semi-transparent watermark is misread: "出版社" -> "五社")
            seg.translate = False
            seg.skip_reason = WATERMARK
            changed += 1
            continue
        trimmed = _trim_watermark_runs(text, band_letters if touching else alphabet)
        if trimmed != text:
            rest_letters = sum(c.isalpha() for c in trimmed)
            if rest_letters >= 2:
                seg.source_text = trimmed
                seg.protected_text, seg.protected = protect_text(trimmed, doc.source_lang)
                seg.translate = not is_fully_protected(seg.protected_text)
                if not seg.translate:
                    seg.skip_reason = "no translatable text (numbers / formula only)"
                changed += 1
    if changed:
        log.info("watermark alphabet %s: %d OCR lines suppressed or trimmed", "".join(sorted(alphabet)), changed)
    return changed


GLYPH_DIFF = 40
"""Per-channel difference from the background colour above which a pixel is ink."""
GLYPH_DILATE_PX = 2
GLYPH_FRINGE_DIFF = 18
"""Fainter pixels (above this difference) connected to glyph ink are erased with it."""
INK_TOLERANCE = 110.0
"""RGB distance to the estimated text colour within which a pixel counts as ink."""
MAX_GLYPH_SHARE = 0.7
"""When more than this share of a box is ink the box is light text on a dark panel: fill it whole."""


BACKGROUND_TOLERANCE = 30
"""Pixels within this per-channel difference of the dominant colour count as background."""
STRIPE_MIN_SHARE = 0.45
"""A glyph-wide strip of a line box whose most common colour covers at least this share
of its pixels has a plain local background (text on paper or on a label cell); below it
the strip holds picture content and only pixels of the text colour are erased."""
STRIPE_FLAT_SHARE = 0.55
"""... and with at least this share the erased pixels are filled flat (else inpainted)."""
DECORATION_REACH = 0.12
"""The outline or drop shadow of a decorated title (slate around yellow strokes) lies within
this share of the line height of the stroke pixels ..."""
DECORATION_SHARE = 0.85
"""... a connected patch of pixels in neither the background nor the text colour lying there
by at least this share of its area is part of the glyphs, not of a picture."""
DECORATION_MIN = 0.03
"""Below this share of the box, odd-coloured pixels are JPEG halo, not worth the test."""
GLYPH_COMPONENT_SHARE = 0.5
"""A solid component made of at least this share of glyph pixels (strokes with their outline)
is a decorated glyph, not a pictogram to keep."""
ICON_MIN_FILL = 0.45
"""A solid ink component (fill ratio of its bounding box at least this, at least about a
glyph in size) in a colour unlike the text is a pictogram and is kept."""
MISSED_GLYPH_REACH = 0.6
"""A glyph the detector left out at the end (or the start) of a line stands within this share
of the line height of the box, or of the glyph taken before it ..."""
MISSED_GLYPHS_MAX = 6
"""... and at most this many line heights of them are taken: a tight polygon loses the last
word or two, not a whole sentence."""
MISSED_GLYPH_HEIGHT = 1.25
"""A blob taller than this share of the line height is a bubble outline or a picture, not a
glyph of the line: the run ends there."""
PUNCT_MAX_SHARE = 0.12
"""Ink right of the OCR box covering at most this share of a one-glyph strip is trailing
punctuation (。，！？) the detector left out; it is erased with the line."""


def _dominant_colour(pixels: np.ndarray) -> tuple[np.ndarray, float]:
    """Most common colour (16-level quantised, refined by the median) and its pixel share."""
    flat = pixels.reshape(-1, 3)
    if flat.size == 0:
        return np.array([255, 255, 255], dtype=np.uint8), 0.0
    q = (flat // 16).astype(np.int32)
    keys = (q[:, 0] << 8 | q[:, 1]) << 8 | q[:, 2]
    values, counts = np.unique(keys, return_counts=True)
    best = values[counts.argmax()]
    colour = np.median(flat[keys == best], axis=0)
    # share of pixels close to that colour: tolerant of gradients and JPEG noise
    near = np.abs(flat.astype(np.int32) - colour.astype(np.int32)).max(axis=1) <= BACKGROUND_TOLERANCE
    colour = np.median(flat[near], axis=0) if near.any() else colour
    return colour.astype(np.uint8), float(near.mean())


def _extend_for_punctuation(original: np.ndarray, box: tuple[int, int, int, int],
                            blocked: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    """``box`` extended to the right over trailing punctuation the detector left out (。，！？):
    small separate ink blobs starting within 0.7 line heights of the box; whatever lies
    further right (a bubble outline, the next word) is not taken."""
    import cv2

    x0, y0, x1, y1 = box
    h = y1 - y0
    ex1 = min(original.shape[1], x1 + h)
    if ex1 - x1 < 3 or h < 6:
        return box
    for bx0, by0, bx1, by1 in blocked:
        if bx0 < x1 + 0.7 * h and bx1 > x1 and by0 < y1 and by1 > y0:
            return box  # another line starts right there
    strip = original[y0:y1, x1:ex1]
    bg, share = _dominant_colour(strip)
    if share < STRIPE_MIN_SHARE:
        # the strip reaches a bubble outline or the page beyond it: take the line's own background
        bg, share = _dominant_colour(original[y0:y1, x0:x1])
        if share < STRIPE_MIN_SHARE:
            return box
    # the text's own darkness separates a full stop from the faint watermark strokes around it
    line_diff = np.abs(original[y0:y1, x0:x1].astype(np.int32) - bg.astype(np.int32)).max(axis=2)
    threshold = max(GLYPH_DIFF, 0.5 * float(np.percentile(line_diff, 99))) if line_diff.size else GLYPH_DIFF
    ink = (np.abs(strip.astype(np.int32) - bg.astype(np.int32)).max(axis=2) > threshold).astype(np.uint8)
    if not ink.any():
        return box
    n, _labels, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    faint = (np.abs(strip.astype(np.int32) - bg.astype(np.int32)).max(axis=2) > GLYPH_DIFF).astype(np.uint8)
    _nf, faint_labels, faint_stats, _ = cv2.connectedComponentsWithStats(faint, connectivity=8)
    right = 0
    for i in range(1, n):
        bx, by, bw, bh, area = (int(v) for v in stats[i])
        if bx > 0.7 * h or bw > 0.55 * h or bh > 0.55 * h or area > 0.12 * h * h:
            continue  # too far, too big: not a punctuation mark
        if bx + bw >= ink.shape[1] - 1:
            continue
        right = max(right, bx + bw)
        for f in set(faint_labels[by:by + bh, bx:bx + bw][ink[by:by + bh, bx:bx + bw] > 0].tolist()) - {0}:
            fx, _fy, fw, _fh, _fa = (int(v) for v in faint_stats[f])
            if fw <= 0.6 * h and fx + fw < ink.shape[1] - 1:
                right = max(right, fx + fw)  # the mark's anti-aliased rim
    if right == 0:
        return box
    return x0, y0, min(ex1, x1 + right + max(2, h // 10)), y1




def _missed_glyph_run(region: np.ndarray, h: int, bg: np.ndarray, ink_colour: np.ndarray,
                      threshold: float) -> tuple[int, list[tuple[int, int, int, int]]]:
    """The run of glyphs in the line's colour at the left edge of ``region`` (the pixels right
    of a line box, or left of it mirrored): ink blobs (darker than ``threshold`` against the
    background, which leaves a faint watermark out) no taller than a glyph, one after another
    a short gap apart, in the text colour. Returns the run's width and the boxes of the glyph
    blobs in it (region coordinates). The run ends at a gap, at a blob too tall or too wide (a
    bubble outline, a picture, a rule) or in another colour (a pictogram), and is 0 when such
    a blob comes first."""
    import cv2

    diff = np.abs(region.astype(np.int32) - bg.astype(np.int32)).max(axis=2)
    any_ink = (diff > threshold).astype(np.uint8)
    if not any_ink.any():
        return 0, []
    dist = np.sqrt(((region.astype(np.int32) - ink_colour) ** 2).sum(axis=2))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(any_ink, connectivity=8)
    reach = max(3, int(round(MISSED_GLYPH_REACH * h)))
    order = sorted(range(1, n), key=lambda i: int(stats[i][0]))
    taken = 0
    blobs: list[tuple[int, int, int, int]] = []
    for i in order:
        bx, by, bw, bh, area = (int(v) for v in stats[i])
        if bx > taken + reach:
            break  # a gap wider than between two glyphs: the line ended
        if area >= 0.03 * h * h or bh >= 0.5 * h or bw >= 0.5 * h:
            # specks (the anti-aliased rim of a glyph the box cut) are taken as they come; a long thin
            # line is no speck
            if bh > MISSED_GLYPH_HEIGHT * h or bw > 1.5 * h or (bh >= 0.9 * h and bw <= 0.2 * h):
                break  # a bubble outline, a picture, a rule (a cell border): not a glyph of the line
            comp = labels == i
            if float((dist[comp] < INK_TOLERANCE).mean()) < 0.5:
                break  # another colour: a pictogram
            blobs.append((bx, by, bx + bw, by + bh))
        if bx + bw >= region.shape[1] - 1:
            break  # runs to the edge of what we may take: not a word's end
        taken = max(taken, bx + bw)
    return taken, blobs


def _extend_over_missed_glyphs(original: np.ndarray, box: tuple[int, int, int, int],
                               blocked: list[tuple[int, int, int, int]]
                               ) -> tuple[tuple[int, int, int, int], list[tuple[int, int, int, int]]]:
    """``box`` extended sideways over whole glyphs the detector left out at either end of the
    line (掂一掂。 after a polygon that stops at 称一称，; the 一 before 枚), so they are erased
    with the line instead of staying beside its translation, and the boxes of those glyphs
    (image coordinates): they are erased even where they touch a bubble outline that the
    eraser keeps. Only glyph-sized blobs in the line's colour a short gap apart are taken,
    never past another OCR line, and only over the line's own plain background."""
    from .images import estimate_text_color

    x0, y0, x1, y1 = box
    h = y1 - y0
    if h < 6:
        return box, []
    bg, share = _dominant_colour(original[y0:y1, x0:x1])
    if share < STRIPE_MIN_SHARE:
        return box, []  # a line over a picture: too risky to guess where it ends
    ink_colour = np.array(estimate_text_color(original, box, bg), dtype=np.int32)
    # the text's own darkness separates its glyphs from the faint watermark strokes around them
    line_diff = np.abs(original[y0:y1, x0:x1].astype(np.int32) - bg.astype(np.int32)).max(axis=2)
    threshold = max(GLYPH_DIFF, 0.5 * float(np.percentile(line_diff, 99))) if line_diff.size else GLYPH_DIFF
    pad = int(round(0.15 * h))
    by0, by1 = max(0, y0 - pad), min(original.shape[0], y1 + pad)
    limit = int(round(MISSED_GLYPHS_MAX * h))

    def barrier(side: str) -> int:
        edge = original.shape[1] if side == "right" else 0
        for bx0, bby0, bx1, bby1 in blocked:
            if bby0 >= by1 or bby1 <= by0:
                continue
            if side == "right" and bx0 >= x1 - 1:
                edge = min(edge, bx0)
            elif side == "left" and bx1 <= x0 + 1:
                edge = max(edge, bx1)
        return edge

    nx0, nx1 = x0, x1
    glyphs: list[tuple[int, int, int, int]] = []
    right_lim = min(barrier("right"), x1 + limit)
    if right_lim - x1 >= 3:
        run, blobs = _missed_glyph_run(original[by0:by1, x1:right_lim], h, bg, ink_colour, threshold)
        if run:
            nx1 = min(right_lim, x1 + run + max(2, h // 10))
            glyphs += [(x1 + bx0, by0 + bby0, x1 + bx1, by0 + bby1) for bx0, bby0, bx1, bby1 in blobs]
    left_lim = max(barrier("left"), x0 - limit)
    if x0 - left_lim >= 3:
        run, blobs = _missed_glyph_run(np.ascontiguousarray(original[by0:by1, left_lim:x0][:, ::-1]), h, bg,
                                       ink_colour, threshold)
        if run:
            nx0 = max(left_lim, x0 - run - max(2, h // 10))
            glyphs += [(x0 - bx1, by0 + bby0, x0 - bx0, by0 + bby1) for bx0, bby0, bx1, bby1 in blobs]
    if (nx0, nx1) == (x0, x1):
        return box, []
    _bg2, share2 = _dominant_colour(original[y0:y1, nx0:nx1])
    if share2 < STRIPE_MIN_SHARE or np.abs(_bg2.astype(np.int32) - bg.astype(np.int32)).max() > BACKGROUND_TOLERANCE:
        return box, []  # the extension reaches onto another surface
    return (nx0, y0, nx1, y1), glyphs


GRADIENT_ROWS = 4
"""Rows sampled at the top and at the bottom of a strip to tell a gradient background (a title
band fading into colour) from a plain one."""
GRADIENT_DIFF = 10
"""Top and bottom rows of a strip whose backgrounds differ by more than this (per channel) lie on
a gradient; even a faint one shows as a block or a ghost when refilled with one flat colour."""
PLAIN_MARGIN = 0.08
"""Share of the line height added around a box on plain surroundings before erasing, so the
edges of glyphs that a tight OCR polygon cut off go with the rest."""






PLAIN_RING_SHARE = 0.7
"""Share of the pixels in a wide ring around a box that must match the ring's median colour for
the surroundings to count as plain (the ring may cut through glyph edges a tight box left out)."""


def _plain_surroundings(original: np.ndarray, alpha: Optional[np.ndarray],
                        box: tuple[int, int, int, int]) -> tuple[np.ndarray, bool]:
    """(median colour, plain?) of a ring a third of the box height wide around ``box``."""
    from .images import RING_PX, ring_pixels

    x0, y0, x1, y1 = box
    ring = max(RING_PX, (y1 - y0) // 3)
    px = ring_pixels(original, box, ring)
    if alpha is not None:
        visible = ring_pixels(alpha[..., None], box, ring)[:, 0] > 0
        if visible.any():
            px = px[visible]
    if px.size == 0:
        return np.array([255, 255, 255], dtype=np.uint8), False
    median = np.clip(np.round(np.median(px, axis=0)), 0, 255).astype(np.uint8)
    near = np.abs(px.astype(np.int32) - median.astype(np.int32)).max(axis=1) <= BACKGROUND_TOLERANCE
    if not near.any():
        return median, False
    median = np.clip(np.round(np.median(px[near], axis=0)), 0, 255).astype(np.uint8)
    return median, bool(near.mean() >= PLAIN_RING_SHARE)


def _grow_on_plain_surroundings(original: np.ndarray, alpha: Optional[np.ndarray], box: tuple[int, int, int, int],
                                blocked: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    """A box on a plain background grows by a small margin on every side (a tight OCR polygon
    cuts the outermost pixels of the glyphs off), unless the margin would reach another box."""
    x0, y0, x1, y1 = box
    ih, iw = original.shape[:2]
    m = max(2, int(round(PLAIN_MARGIN * (y1 - y0))))

    def free(margin: tuple[int, int, int, int]) -> bool:
        mx0, my0, mx1, my1 = margin
        if mx1 <= mx0 or my1 <= my0:
            return False
        return not any(bx0 < mx1 and bx1 > mx0 and by0 < my1 and by1 > my0 for bx0, by0, bx1, by1 in blocked)

    ring_bg, _plain = _plain_surroundings(original, alpha, box)

    def lined(band: np.ndarray, along: int) -> bool:
        """A straight line of ink runs along this side (the border of the cell the label is in):
        growing over it would take the cell's border, and the paper beyond, into the box."""
        if band.size == 0:
            return False
        ink = np.abs(band.astype(np.int32) - ring_bg.astype(np.int32)).max(axis=2) > GLYPH_DIFF
        runs = ink if along == 1 else ink.T
        for line in runs:
            if not line.any():
                continue
            d = np.diff(np.concatenate(([0], line.astype(np.int8), [0])))
            if int((np.flatnonzero(d == -1) - np.flatnonzero(d == 1)).max()) >= RULING_SPAN * line.size:
                return True
        return False

    e = 3
    gx0 = max(0, x0 - m) if free((max(0, x0 - m), y0, x0, y1)) \
        and not lined(original[y0:y1, max(0, x0 - m):x0 + e], 0) else x0
    gx1 = min(iw, x1 + m) if free((x1, y0, min(iw, x1 + m), y1)) \
        and not lined(original[y0:y1, max(0, x1 - e):min(iw, x1 + m)], 0) else x1
    gy0 = max(0, y0 - m) if free((gx0, max(0, y0 - m), gx1, y0)) \
        and not lined(original[max(0, y0 - m):y0 + e, x0:x1], 1) else y0
    gy1 = min(ih, y1 + m) if free((gx0, y1, gx1, min(ih, y1 + m))) \
        and not lined(original[max(0, y1 - e):min(ih, y1 + m), x0:x1], 1) else y1
    grown = (gx0, gy0, gx1, gy1)
    if grown == box:
        return box
    _bg, plain = _plain_surroundings(original, alpha, box)
    if not plain:
        return box
    _bg2, plain2 = _plain_surroundings(original, alpha, grown)
    return grown if plain2 else box


def _gradient_strip(stripe: np.ndarray) -> bool:
    """True when the background of a strip changes from its top rows to its bottom rows (a title
    band fading into colour): such glyphs are inpainted from their surroundings, because one
    flat fill colour would leave a block or a ghost."""
    if stripe.shape[0] < 3 * GRADIENT_ROWS:
        return False
    top, _t = _dominant_colour(stripe[:GRADIENT_ROWS].astype(np.uint8))
    bottom, _b = _dominant_colour(stripe[-GRADIENT_ROWS:].astype(np.uint8))
    return bool(np.abs(top.astype(np.int32) - bottom.astype(np.int32)).max() > GRADIENT_DIFF)



def _glyph_decoration(crop: np.ndarray, near_ink: np.ndarray, bg: np.ndarray, h: int) -> np.ndarray:
    """Pixels of a decorated title that belong to its glyphs without being in the text colour:
    the outline or drop shadow hugging the strokes (slate around yellow 目录). A picture behind
    the text, or a pictogram beside it, reaches far from the strokes and is left alone."""
    import cv2

    none = np.zeros(near_ink.shape, bool)
    other = ~near_ink & (np.abs(crop - bg.astype(np.int32)).max(axis=2) > GLYPH_DIFF)
    if other.mean() < DECORATION_MIN or near_ink.mean() < DECORATION_MIN:
        return none
    reach = max(2, int(round(DECORATION_REACH * h)))
    halo = cv2.dilate(near_ink.astype(np.uint8), np.ones((2 * reach + 1, 2 * reach + 1), np.uint8)) > 0
    count, labels = cv2.connectedComponents(other.astype(np.uint8), connectivity=8)
    sizes = np.bincount(labels.ravel(), minlength=count)
    inside = np.bincount(labels.ravel(), weights=halo.ravel(), minlength=count)
    hugging = inside >= DECORATION_SHARE * sizes
    hugging[0] = False
    return hugging[labels]


RULING_SPAN = 0.8
"""A straight line of ink covering at least this share of a line box's height (or width) ..."""
RULING_BEYOND = 3
"""... that goes on for this many pixels past the box (the border of a table the label stands in) ..."""
RULING_THICK = 0.15
"""A ruling is at most this share of the line height thick."""
RULING_MIN_LENGTH = 2.5
"""... or, for a horizontal line, that crosses a box at least this many line heights wide (a cell
border; a glyph like 口 is not that wide), with the vertical lines meeting its ends, is a ruling,
not a stroke of the glyphs: it is kept."""


def _crossing_rulings(original: np.ndarray, box: tuple[int, int, int, int], mask: np.ndarray,
                      bg: np.ndarray) -> np.ndarray:
    """Pixels of ``mask`` (box coordinates) on table or cell rulings crossing the line box: rows
    (columns) of ink spanning the box that continue past it in the original image, horizontal
    lines across a box several glyphs wide, and the vertical lines meeting their ends (the
    corners of the cell). Glyph strokes stay inside the box read around them."""
    x0, y0, x1, y1 = box
    h, w = mask.shape
    keep = np.zeros((h, w), bool)
    m = mask > 0
    H, W = original.shape[:2]
    bgi = bg.astype(np.int32)

    def ink(patch: np.ndarray) -> np.ndarray:
        return np.abs(patch.astype(np.int32) - bgi).max(axis=2) > GLYPH_DIFF

    def beyond_rows(gx: int) -> bool:  # the column's line goes on above or below the box
        xs = slice(max(0, gx - 1), min(W, gx + 2))
        above = original[max(0, y0 - RULING_BEYOND):y0, xs]
        below = original[y1:min(H, y1 + RULING_BEYOND), xs]
        return any(p.shape[0] == RULING_BEYOND and bool(ink(p).any(axis=1).all()) for p in (above, below))

    def beyond_cols(gy: int) -> bool:  # the row's line goes on left or right of the box
        ys = slice(max(0, gy - 1), min(H, gy + 2))
        left = original[ys, max(0, x0 - RULING_BEYOND):x0]
        right = original[ys, x1:min(W, x1 + RULING_BEYOND)]
        return any(p.shape[1] == RULING_BEYOND and bool(ink(p).any(axis=0).all()) for p in (left, right))

    def longest_run(v: np.ndarray) -> int:
        if not v.any():
            return 0
        d = np.diff(np.concatenate(([0], v.astype(np.int8), [0])))
        return int((np.flatnonzero(d == -1) - np.flatnonzero(d == 1)).max())

    def thin(lines: list[int], limit: float) -> list[int]:
        """Lines in bands at most ``limit`` thick (a ruling), not a block of them (a bold glyph)."""
        out, band = [], []
        for v in lines + [None]:  # type: ignore[list-item]
            if band and (v is None or v != band[-1] + 1):
                if len(band) <= limit:
                    out += band
                band = []
            if v is not None:
                band.append(v)
        return out

    rows = thin([int(r) for r in range(h) if longest_run(m[r, :]) >= RULING_SPAN * w
                 and (w >= RULING_MIN_LENGTH * h or beyond_cols(y0 + r))], max(2.0, RULING_THICK * h))
    for r in rows:
        keep[r, :] = m[r, :]
    cols = thin([int(c) for c in range(w) if longest_run(m[:, c]) >= RULING_SPAN * h], max(2.0, RULING_THICK * h))
    for c in cols:
        ys = np.flatnonzero(m[:, c])
        corner = any(abs(r - int(ys[0])) <= 3 or abs(r - int(ys[-1])) <= 3 for r in rows)
        if corner or beyond_rows(x0 + c):
            keep[:, c] = m[:, c]
    return keep


def _erase_glyphs(canvas: np.ndarray, alpha: Optional[np.ndarray], original: np.ndarray,
                  original_alpha: Optional[np.ndarray], box: tuple[int, int, int, int],
                  blocked: Optional[list[tuple[int, int, int, int]]] = None) -> str:
    """Erase the glyphs of one OCR line.

    The line box is cut into glyph-wide strips. Where a strip has a plain local
    background (its most common colour dominates), every pixel that differs from that
    colour is ink - whatever its colour (red words inside black text, white text on a
    badge, two-colour label cells) - except solid components in a colour unlike the
    text (pictograms), and is filled with the strip's background. Strips holding
    picture content fall back to erasing only pixels of the text colour by inpainting.
    The background of a strip is the most common colour among its pixels that are not
    glyph (text colour, or the solid outline and shadow of a decorated title): the
    glyphs of a bold or decorated line may outnumber the paper behind them.
    """
    import cv2

    from .images import estimate_text_color

    from .images import estimate_background

    box = _extend_for_punctuation(original, box, blocked or [])
    box, missed = _extend_over_missed_glyphs(original, box, blocked or [])
    box = _grow_on_plain_surroundings(original, original_alpha, box, blocked or [])
    x0, y0, x1, y1 = box
    crop = original[y0:y1, x0:x1].astype(np.int32)
    if crop.size == 0:
        return "empty"
    h, w = crop.shape[:2]
    box_bg, _share = _dominant_colour(original[y0:y1, x0:x1])
    ring_bg, ring_uniform = _plain_surroundings(original, original_alpha, box)
    if ring_uniform and np.abs(ring_bg.astype(np.int32) - box_bg.astype(np.int32)).max() > BACKGROUND_TOLERANCE \
            and float(np.sqrt(((np.array(estimate_text_color(original, box, ring_bg, original_alpha), dtype=np.int32)
                                - box_bg.astype(np.int32)) ** 2).sum())) < INK_TOLERANCE:
        # bold or wide glyphs (SHUXUE in a tight box) outnumber the background pixels inside the box:
        # the plain surroundings say what the background is, not the most common colour inside. A box
        # whose most common colour is not the text's (a label in a yellow cell on white paper) keeps it.
        box_bg = ring_bg
        _share = float((np.abs(crop - ring_bg.astype(np.int32)).max(axis=2) <= BACKGROUND_TOLERANCE).mean())
    ink_colour = np.array(estimate_text_color(original, box, box_bg, original_alpha), dtype=np.int32)
    dist_ink = np.sqrt(((crop - ink_colour) ** 2).sum(axis=2))
    near_ink = dist_ink < INK_TOLERANCE
    glyph = near_ink | _glyph_decoration(crop, near_ink, box_bg, h)
    mask = np.zeros((h, w), np.uint8)
    fill = np.zeros((h, w, 3), np.uint8)
    flat = np.zeros((h, w), bool)
    step = max(4, int(round(0.6 * h)))
    strips: list[tuple[int, int, np.ndarray, float]] = []
    prev_bg, prev_share = box_bg, _share
    for sx in range(0, w, step):
        ex = min(w, sx + step)
        rest = crop[:, sx:ex][~glyph[:, sx:ex]].astype(np.uint8)
        total = (ex - sx) * h
        if rest.shape[0] >= 0.1 * total:
            bg, share = _dominant_colour(rest)
            share *= rest.shape[0] / total
        else:  # a heavy glyph fills the strip: the surface is the neighbour's
            bg, share = prev_bg, 0.0
        if share < STRIPE_MIN_SHARE and prev_share >= STRIPE_MIN_SHARE \
                and np.abs(bg.astype(np.int32) - prev_bg.astype(np.int32)).max() <= BACKGROUND_TOLERANCE:
            share = prev_share  # a heavy glyph on the same surface as the plain strip before it
        if ring_uniform and np.abs(bg.astype(np.int32) - ring_bg.astype(np.int32)).max() <= BACKGROUND_TOLERANCE:
            share = max(share, STRIPE_FLAT_SHARE)  # plain surroundings: fill flat, do not inpaint
        elif ring_uniform and float(np.sqrt(((bg.astype(np.int32) - ink_colour) ** 2).sum())) < INK_TOLERANCE:
            # the strip is all glyph (bold letters): its background is the plain one around the box;
            # a strip in another solid colour is a pictogram and keeps its own surface
            bg = ring_bg
            share = float((np.abs(crop[:, sx:ex] - ring_bg.astype(np.int32)).max(axis=2)
                           <= BACKGROUND_TOLERANCE).mean())
            share = max(share, STRIPE_FLAT_SHARE)
        prev_bg, prev_share = bg, share
        strips.append((sx, ex, bg, share))
    for k, (sx, ex, bg, share) in enumerate(strips):
        stripe = crop[:, sx:ex]
        diff = np.abs(stripe - bg.astype(np.int32)).max(axis=2)
        if share >= STRIPE_MIN_SHARE:
            m = diff > GLYPH_DIFF
        else:  # picture content: only what looks like the text (strokes and their decoration)
            m = (diff > GLYPH_DIFF) & glyph[:, sx:ex]
        # pixels of a neighbouring strip's surface (the next label cell, a pictogram that
        # dominates the next strip) are not ink of this one
        for j in (k - 1, k + 1):
            if 0 <= j < len(strips) and strips[j][3] >= STRIPE_MIN_SHARE:
                nbg = strips[j][2].astype(np.int32)
                if np.abs(nbg - bg.astype(np.int32)).max() > BACKGROUND_TOLERANCE and \
                        float(np.sqrt(((nbg - ink_colour) ** 2).sum())) >= INK_TOLERANCE:
                    m &= np.abs(stripe - nbg).max(axis=2) > BACKGROUND_TOLERANCE
        mask[:, sx:ex] = m
        fill[:, sx:ex] = bg
        flat[:, sx:ex] = share >= STRIPE_FLAT_SHARE and not _gradient_strip(stripe)
    if not mask.any():
        return "nothing to erase"
    # keep pictograms, bars and rulings: large solid components unlike the text colour
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    for i in range(1, count):
        bx, by, bw, bh, area = stats[i]
        if area >= 0.5 * h * h and area >= ICON_MIN_FILL * bw * bh:
            comp = labels == i
            if float(np.median(dist_ink[comp])) >= INK_TOLERANCE and float(glyph[comp].mean()) < GLYPH_COMPONENT_SHARE:
                mask[comp] = 0  # not a decorated glyph (strokes inside their outline): a pictogram
    for mx0, my0, mx1, my1 in missed:
        # a glyph the detector left out goes even where it touches a kept outline (一 against its bubble)
        sl = (slice(max(0, my0 - y0), max(0, min(h, my1 - y0))), slice(max(0, mx0 - x0), max(0, min(w, mx1 - x0))))
        mask[sl][near_ink[sl]] = 1
    rulings = _crossing_rulings(original, box, mask, box_bg)
    if rulings.any():
        import cv2 as _cv2
        rulings = _cv2.dilate(rulings.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        mask[rulings] = 0  # the border of the cell the label stands in stays
    if float(mask.mean()) > 0.85:
        _bg, how = _clear_box(canvas, alpha, original, original_alpha, box)
        return how
    # hysteresis: faint fringe pixels (JPEG halo, anti-aliasing) connected to a glyph go too
    weak = np.zeros((h, w), bool)
    for sx, ex, bg, share in strips:
        if share >= STRIPE_MIN_SHARE:
            weak[:, sx:ex] = np.abs(crop[:, sx:ex] - bg.astype(np.int32)).max(axis=2) > GLYPH_FRINGE_DIFF
    if weak.any():
        n_weak, weak_labels = cv2.connectedComponents((weak | (mask > 0)).astype(np.uint8), connectivity=8)
        touched = np.unique(weak_labels[mask > 0])
        fringe = np.isin(weak_labels, touched[touched > 0]) & weak
        mask = (mask > 0) | fringe
        mask = mask.astype(np.uint8)
    kernel = np.ones((2 * GLYPH_DILATE_PX + 1, 2 * GLYPH_DILATE_PX + 1), np.uint8)
    grown = cv2.dilate(mask, kernel) > 0
    if rulings.any():
        grown &= ~rulings
    region = canvas[y0:y1, x0:x1]
    flat_px = grown & flat
    region[flat_px] = fill[flat_px]
    rest = (grown & ~flat).astype(np.uint8)
    if rest.any():
        pad = 6
        cy0, cy1 = max(0, y0 - pad), min(canvas.shape[0], y1 + pad)
        cx0, cx1 = max(0, x0 - pad), min(canvas.shape[1], x1 + pad)
        full_mask = np.zeros((cy1 - cy0, cx1 - cx0), np.uint8)
        full_mask[y0 - cy0:y1 - cy0, x0 - cx0:x1 - cx0] = rest * 255
        canvas[cy0:cy1, cx0:cx1] = cv2.inpaint(np.ascontiguousarray(canvas[cy0:cy1, cx0:cx1]), full_mask, 3,
                                               cv2.INPAINT_TELEA)
        return "glyphs filled and inpainted" if flat_px.any() else "glyphs inpainted"
    return "glyphs filled"


def _trim_watermark_runs(text: str, alphabet: set[str]) -> str:
    """Remove a run of >= 2 watermark letters at either end of ``text`` (plus the
    whitespace / punctuation between the run and the rest)."""
    t = text.strip()
    connectors = " \t,，、:："
    for _ in range(2):
        # trailing run
        i = len(t)
        while i > 0 and (t[i - 1] in alphabet or (t[i - 1] in connectors and i < len(t))):
            i -= 1
        tail = t[i:]
        if sum(c in alphabet for c in tail) >= 2 and not any(c.isalpha() and c not in alphabet for c in tail):
            t = t[:i].rstrip(" \t,，、:：")
        # leading run
        j = 0
        while j < len(t) and (t[j] in alphabet or (t[j] in connectors and j > 0)):
            j += 1
        head = t[:j]
        if sum(c in alphabet for c in head) >= 2 and not any(c.isalpha() and c not in alphabet for c in head):
            t = t[j:].lstrip(" \t,，、:：")
    return t


__all__ = ["is_scanned_page", "scanned_pages", "group_ocr_lines", "build_overlay_segments",
           "erase_merged_lines", "suppress_watermark_fragments", "suppress_patch_duplicates",
           "relink_patch_duplicates", "watermark_alphabet", "MERGED", "PATCH_DUPLICATE", "WATERMARK"]
