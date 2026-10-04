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
from .images import _clear_box, encode_image, load_image, replace_image, resolve_placement
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
MERGED = "merged into paragraph"
"""Prefix of the ``skip_reason`` of OCR lines that became part of a paragraph."""


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
            return False  # a short label next to / under a long line is a diagram label or a table cell
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


def _join_row_pieces(candidates: list[TextSegment], blank_check: Optional[BlankCheck] = None
                     ) -> tuple[list[TextSegment], dict[str, list[TextSegment]]]:
    """Join same-row sentence pieces into one virtual line each (blank marked ``___``).
    Returns the lines for grouping and, per virtual line id, the OCR lines it stands for."""
    by_x = sorted(candidates, key=lambda l: (l.bbox.x0, l.bbox.y0))
    used: set[str] = set()
    units: dict[str, list[TextSegment]] = {}
    out: list[TextSegment] = []
    for line in sorted(candidates, key=lambda l: (round(l.bbox.y0, 1), l.bbox.x0)):
        if line.id in used:
            continue
        chain = [line]
        while True:
            last = chain[-1]
            nxt = next((c for c in by_x if c.id not in used and c is not last and c not in chain
                        and c.bbox.x0 >= last.bbox.x1 - 0.2 * last.bbox.height
                        and _row_joinable(last, c, blank_check)), None)
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
    if len(lines) == 1 and page_median_height > 0 and h >= 1.4 * page_median_height:
        role = "heading"
    elif len(lines) == 1 and letters <= 8:
        role = "label"
    else:
        role = "body"
    first = lines[0]
    translate = not is_fully_protected(protected) and any(l.translate for l in lines)
    return TextSegment(
        id=f"p{page_index}_s{index}",
        page=page_index,
        kind=SegmentKind.TEXT,
        bbox=para.bbox,
        source_text=text,
        protected_text=protected,
        protected=fragments,
        style=SegmentStyle(size=size, color=first.style.color, align=align, line_height=line_height, role=role),
        translate=translate,
        skip_reason="" if translate else "no translatable text (numbers / formula only)",
        origin="ocr",
        members=members if members is not None else [l.id for l in lines],
        reading_order=index,
    )


def group_ocr_lines(lines: list[TextSegment], page_index: int, source_lang: Lang,
                    blank_check: Optional[BlankCheck] = None) -> list[TextSegment]:
    """Merge the OCR line segments of one scanned page into paragraph segments.

    The merged lines are marked ``translate=False`` with ``skip_reason``
    ``"merged into paragraph <id>"`` (they are erased from the image later);
    lines that cannot be merged (labels, slanted text, foreign script) are left
    untouched. Returns the new paragraph segments in reading order.
    """
    candidates = [l for l in lines if l.page == page_index and _mergeable(l)]
    if not candidates:
        return []
    candidates, units = _join_row_pieces(candidates, blank_check)
    candidates.sort(key=lambda l: (round(l.bbox.y0, 1), l.bbox.x0))
    page_median_height = statistics.median(l.bbox.height for l in candidates)
    paragraphs: list[_Para] = []
    for line in candidates:
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
    paragraphs.sort(key=lambda p: (round(p.bbox.y0 / 20), p.bbox.x0))
    out: list[TextSegment] = []
    for i, para in enumerate(paragraphs):
        originals = [u for l in para.lines for u in units.get(l.id, [l])]
        seg = _paragraph_segment(para, i, page_index, source_lang, page_median_height,
                                 members=[u.id for u in originals])
        if not seg.translate:
            continue  # formulas and numbers are not translated: they stay in the picture untouched
        for u in originals:
            u.translate = False
            u.skip_reason = f"{MERGED} {seg.id}"
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
    try:
        for page_index in sorted(scanned):
            lines = [s for s in doc.segments if s.page == page_index and s.kind == SegmentKind.IMAGE_TEXT]
            out.extend(group_ocr_lines(lines, page_index, doc.source_lang, check))
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
        for seg in segs:
            assert seg.image is not None
            x0, y0, x1, y1 = (int(v) for v in seg.image.pixel_box)
            x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
            x1, y1 = min(current.width, x1 + pad), min(current.height, y1 + pad)
            if x1 <= x0 or y1 <= y0:
                continue
            canvas[y0:y1, x0:x1] = original.rgb[y0:y1, x0:x1]
            if alpha is not None and original.alpha is not None:
                alpha[y0:y1, x0:x1] = original.alpha[y0:y1, x0:x1]
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


WATERMARK_CONFUSIONS = set("乐东字五品反童厶")
"""Characters the OCR reads for pieces of a semi-transparent watermark (京 -> 乐 / 东,
出 -> 五, 版 -> 反): inside the watermark band they count as watermark letters."""
BAND_MIN_HALF_WIDTH = 0.025
"""Minimum half-width of the watermark band (share of the page height)."""
BAND_MAX_LETTERS = 4


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
    return float(slope), float(intercept), half, float(xs.min()) - 0.05, float(xs.max()) + 0.05


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
        inside = band is not None and _in_band(seg, band, sizes.get(seg.page, (0.0, 0.0)))
        if inside and len(letters) <= BAND_MAX_LETTERS and (
                all(c in band_letters for c in letters)
                or (any(c in band_letters for c in letters) and confidence < LOW_CONFIDENCE)):
            # an upright or misread piece of the watermark (学, 五, 反社) lying on the watermark's diagonal
            seg.translate = False
            seg.skip_reason = WATERMARK
            changed += 1
            continue
        in_alphabet = sum(c in alphabet for c in letters)
        if len(letters) <= MAX_FRAGMENT_LETTERS and (
                in_alphabet == len(letters)
                or (len(letters) <= 4 and in_alphabet * 2 >= len(letters) and confidence < LOW_CONFIDENCE)):
            # all letters from the watermark, or a short low-confidence piece half made of them
            # (a semi-transparent watermark is misread: "出版社" -> "五社")
            seg.translate = False
            seg.skip_reason = WATERMARK
            changed += 1
            continue
        trimmed = _trim_watermark_runs(text, band_letters if inside else alphabet)
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
ICON_MIN_FILL = 0.45
"""A solid ink component (fill ratio of its bounding box at least this, at least about a
glyph in size) in a colour unlike the text is a pictogram and is kept."""
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
    """``box`` extended to the right over a small ink blob (trailing punctuation)."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    ex1 = min(original.shape[1], x1 + h)
    if ex1 - x1 < 3 or h < 6:
        return box
    for bx0, by0, bx1, by1 in blocked:
        if bx0 < ex1 and bx1 > x1 and by0 < y1 and by1 > y0:
            return box  # another line starts right there
    strip = original[y0:y1, x1:ex1]
    bg, share = _dominant_colour(strip)
    if share < STRIPE_FLAT_SHARE:
        return box
    ink = np.abs(strip.astype(np.int32) - bg.astype(np.int32)).max(axis=2) > GLYPH_DIFF
    if not ink.any() or ink.mean() > PUNCT_MAX_SHARE:
        return box
    cols = np.flatnonzero(ink.any(axis=0))
    if cols.max() >= strip.shape[1] - 2:
        return box  # ink runs on beyond the strip: a neighbouring object, not punctuation
    return x0, y0, x1 + int(cols.max()) + 2, y1


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
    """
    import cv2

    from .images import estimate_text_color

    box = _extend_for_punctuation(original, box, blocked or [])
    x0, y0, x1, y1 = box
    crop = original[y0:y1, x0:x1].astype(np.int32)
    if crop.size == 0:
        return "empty"
    h, w = crop.shape[:2]
    box_bg, _share = _dominant_colour(original[y0:y1, x0:x1])
    ink_colour = np.array(estimate_text_color(original, box, box_bg, original_alpha), dtype=np.int32)
    dist_ink = np.sqrt(((crop - ink_colour) ** 2).sum(axis=2))
    mask = np.zeros((h, w), np.uint8)
    fill = np.zeros((h, w, 3), np.uint8)
    flat = np.zeros((h, w), bool)
    step = max(4, int(round(0.6 * h)))
    strips: list[tuple[int, int, np.ndarray, float]] = []
    prev_bg, prev_share = box_bg, _share
    for sx in range(0, w, step):
        ex = min(w, sx + step)
        bg, share = _dominant_colour(crop[:, sx:ex].astype(np.uint8))
        if np.abs(bg.astype(np.int32) - ink_colour).max() < GLYPH_DIFF and \
                np.abs(prev_bg.astype(np.int32) - ink_colour).max() >= GLYPH_DIFF:
            bg, share = prev_bg, prev_share  # a heavy glyph dominates the strip: keep the neighbour's background
        prev_bg, prev_share = bg, share
        strips.append((sx, ex, bg, share))
    for k, (sx, ex, bg, share) in enumerate(strips):
        stripe = crop[:, sx:ex]
        diff = np.abs(stripe - bg.astype(np.int32)).max(axis=2)
        if share >= STRIPE_MIN_SHARE:
            m = diff > GLYPH_DIFF
        else:  # picture content: only what looks like the text colour
            m = (diff > GLYPH_DIFF) & (dist_ink[:, sx:ex] < INK_TOLERANCE)
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
        flat[:, sx:ex] = share >= STRIPE_FLAT_SHARE
    if not mask.any():
        return "nothing to erase"
    # keep pictograms, bars and rulings: large solid components unlike the text colour
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    for i in range(1, count):
        bx, by, bw, bh, area = stats[i]
        if area >= 0.5 * h * h and area >= ICON_MIN_FILL * bw * bh:
            comp = labels == i
            if float(np.median(dist_ink[comp])) >= INK_TOLERANCE:
                mask[comp] = 0
    if float(mask.mean()) > 0.85:
        _bg, how = _clear_box(canvas, alpha, original, original_alpha, box)
        return how
    kernel = np.ones((2 * GLYPH_DILATE_PX + 1, 2 * GLYPH_DILATE_PX + 1), np.uint8)
    grown = cv2.dilate(mask, kernel) > 0
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
           "erase_merged_lines", "suppress_watermark_fragments", "watermark_alphabet", "MERGED", "WATERMARK"]
