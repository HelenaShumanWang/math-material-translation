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
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pymupdf

from .images import _clear_box, encode_image, load_image, resolve_placement
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
HEIGHT_RATIO = (0.6, 1.7)
"""Line heights within a paragraph must stay within this ratio range."""
FONT_HEIGHT_RATIO = 0.82
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
        if narrower <= 0:
            return False
        left_aligned = abs(line.bbox.x0 - self.bbox.x0) <= 1.5 * h
        return overlap >= MIN_X_OVERLAP * narrower or (left_aligned and overlap > 0)

    def add(self, line: TextSegment) -> None:
        self.lines.append(line)
        self.bbox = self.bbox.union(line.bbox)
        self.heights.append(line.bbox.height)


def _join_lines(texts: list[str], lang: Lang) -> str:
    if is_cjk(lang):
        out = ""
        for t in texts:
            t = t.strip()
            if out and out[-1].isascii() and out[-1].isalnum() and t[:1].isascii() and t[:1].isalnum():
                out += " "
            out += t
        return out
    return " ".join(t.strip() for t in texts)


def _paragraph_segment(para: _Para, index: int, page_index: int, source_lang: Lang,
                       page_median_height: float) -> TextSegment:
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
        members=[l.id for l in lines],
        reading_order=index,
    )


def group_ocr_lines(lines: list[TextSegment], page_index: int, source_lang: Lang) -> list[TextSegment]:
    """Merge the OCR line segments of one scanned page into paragraph segments.

    The merged lines are marked ``translate=False`` with ``skip_reason``
    ``"merged into paragraph <id>"`` (they are erased from the image later);
    lines that cannot be merged (labels, slanted text, foreign script) are left
    untouched. Returns the new paragraph segments in reading order.
    """
    candidates = sorted((l for l in lines if l.page == page_index and _mergeable(l)),
                        key=lambda l: (round(l.bbox.y0, 1), l.bbox.x0))
    if not candidates:
        return []
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
        seg = _paragraph_segment(para, i, page_index, source_lang, page_median_height)
        if not seg.translate:
            continue  # formulas and numbers are not translated: they stay in the picture untouched
        for l in para.lines:
            l.translate = False
            l.skip_reason = f"{MERGED} {seg.id}"
        out.append(seg)
    return out


def build_overlay_segments(doc: TranslatedDocument, scanned: set[int]) -> list[TextSegment]:
    """Paragraph segments for every scanned page of ``doc`` (lines are marked merged)."""
    out: list[TextSegment] = []
    for page_index in sorted(scanned):
        lines = [s for s in doc.segments if s.page == page_index and s.kind == SegmentKind.IMAGE_TEXT]
        out.extend(group_ocr_lines(lines, page_index, doc.source_lang))
    return out


# --------------------------------------------------------------------------- #
# erasing merged lines from the page images
# --------------------------------------------------------------------------- #


def erase_merged_lines(pdf_doc: pymupdf.Document, doc: TranslatedDocument) -> int:
    """Erase the glyphs of every merged OCR line from its image (flat fill or
    inpainting, as the repaint mode does) and replace the image in ``pdf_doc``.
    Returns the number of images modified."""
    by_image: dict[tuple[int, int], list[TextSegment]] = defaultdict(list)
    for seg in doc.segments:
        if seg.kind == SegmentKind.IMAGE_TEXT and seg.image is not None and seg.skip_reason.startswith(MERGED):
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
            _bg, how = _clear_box(canvas, alpha, original, original_alpha, (x0, y0, x1, y1))
            seg.render = RenderInfo(font_size=0.0, scale=1.0, notes=f"{how}; translation placed as page text")
        stream = encode_image(canvas, alpha, loaded.ext, qtables=loaded.jpeg_qtables,
                              subsampling=loaded.jpeg_subsampling)
        try:
            page.replace_image(placement.xref, stream=stream)
            modified += 1
        except Exception as exc:  # noqa: BLE001 - keep the run going; QA reports the leftovers
            log.error("page %d: replace_image(xref=%d) failed: %s", page_index, placement.xref, exc)
    return modified


__all__ = ["is_scanned_page", "scanned_pages", "group_ocr_lines", "build_overlay_segments",
           "erase_merged_lines", "MERGED"]
