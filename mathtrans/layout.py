"""Re-render translated text into the PDF while preserving the page layout.

For every text segment that has a translation the original glyphs are removed
with a redaction (images, vector graphics, rules and background fills are kept)
and the translation is inserted as real, extractable text with
``Page.insert_htmlbox`` using the original font size, colour, weight, italic,
alignment and line height. Text that does not fit is shrunk (down to
``min_font_scale``), set with a tighter line height, or given a slightly larger
box in free page space; what happened is recorded in ``TextSegment.render`` so
the QA layer can report overflow.

Empirical contract of ``Page.insert_htmlbox`` (PyMuPDF 1.28.2, verified by
``tests/test_layout.py::test_insert_htmlbox_contract``)::

    text fits                      -> (spare_height >= 0, scale)   scale_low <= scale <= 1
    does not fit, scale_low > 0    -> (-1, scale_low)              NOTHING is written to the page
    scale_low == 0 (unlimited)     -> (spare_height >= 0, scale)   always written, scale as small as needed
    empty text                     -> (rect height, 1.0)

So "does not fit" is signalled by a negative ``spare_height`` (``scale`` is
never 0), and a failed attempt leaves the page untouched, which makes it safe
to retry with other parameters.

Redaction removes a glyph as soon as the redaction rectangle covers roughly
10 % of the glyph's font box (measured: 1.5pt at 11px, 3pt at 22px). Font boxes
of adjacent lines overlap by ascender + descender (about 0.35 x font size), so
besides the 0.3pt shrink the redaction rectangle is cut back wherever it meets
a text line that does not belong to the segment (see :func:`_redaction_rect`).

``SegmentStyle.rotation`` is the ``rotate`` argument of ``insert_htmlbox`` /
``insert_text`` that reproduces the extracted writing direction (the convention
of ``mathtrans.extract``): ``(1, 0) -> 0``, ``(0, -1) -> 90`` (text runs upwards),
``(-1, 0) -> 180``, ``(0, 1) -> 270`` (text runs downwards). It is passed through
unchanged; see :func:`html_rotation`.

All geometry (``get_text``, ``get_image_info``, ``get_drawings``,
``add_redact_annot``, ``insert_htmlbox``) lives in the *unrotated* page space,
also for pages with a ``/Rotate`` entry, whereas ``page.rect`` describes the
displayed page; :func:`unrotated_page_rect` gives the matching rectangle.

Every ``insert_htmlbox`` call embeds a complete copy of the font it used, so
the document is saved with ``garbage=4`` which merges identical objects
(a 2-page sample otherwise grows from 0.7 MB to 23 MB). Fonts are deliberately
*not* subsetted: a fully embedded font lets PDF editors type any character
when the translation is corrected by hand.
"""
from __future__ import annotations

import html as _html
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, Sequence, Union

import pymupdf

from .fonts import find_font_file, html_font_setup
from .models import BBox, Lang, RenderInfo, SegmentKind, SegmentStyle, TextSegment, TranslatedDocument

log = logging.getLogger("mathtrans.layout")

PathLike = Union[str, "os.PathLike[str]"]

REDACT_SHRINK = 0.3
"""Points by which a segment box is shrunk before redaction (protects neighbours)."""
TIGHT_LINE_HEIGHT = 1.1
"""Line height tried when the text does not fit with the original one."""
MAX_HEIGHT_GROWTH = 0.5
"""A box may grow downward by at most this fraction of its height (=> 1.5 x)."""
MIN_WIDTH_GROWTH = 60.0
"""Horizontal growth allowance in points for tiny boxes (labels, page numbers)."""
MAX_WIDTH_GROWTH = 2.0
"""A box may grow horizontally by at most this fraction of its width."""
COLUMN_MIN_WIDTH_FRACTION = 0.15
"""Segments at least this wide (fraction of the page width) act as column walls:
a box never grows sideways past the near edge of such a segment, whatever its
vertical position, so that multi-column layouts keep their gutters."""
PAGE_MARGIN = 10.0
"""Boxes are never extended closer than this to the page edge."""
EDGE_MARGIN = 72.0
"""Boxes may grow into the outer inch of the page only where content already is."""
CONTENT_TOLERANCE = 4.0
"""Allowed overshoot beyond the page's content area when growing a box."""
OBSTACLE_GAP = 2.0
"""Minimum distance kept between an extended box and other content."""

_FACE_VARIANTS: dict[str, tuple[str, ...]] = {
    "bold": ("-Bold", "Bold", "-bold", "bd", "-B"),
    "italic": ("-Italic", "-Oblique", "Italic", "Oblique", "-italic", "i"),
    "bolditalic": ("-BoldItalic", "-BoldOblique", "BoldItalic", "BoldOblique", "bi", "-BI"),
}
_FACE_DESCRIPTORS: dict[str, str] = {
    "bold": "font-weight: bold;",
    "italic": "font-style: italic;",
    "bolditalic": "font-weight: bold; font-style: italic;",
}


# --------------------------------------------------------------------------- #
# HTML / CSS generation
# --------------------------------------------------------------------------- #


def page_css(target_lang: Lang | str, fonts_dir: Optional[PathLike] = None) -> tuple[str, Optional[pymupdf.Archive]]:
    """CSS and ``Archive`` for ``insert_htmlbox`` when rendering ``target_lang``.

    Uses :func:`mathtrans.fonts.html_font_setup`; when it provides a dedicated
    font file, matching bold / italic faces found next to it are declared too
    (otherwise the Story engine would synthesise nothing and headings would lose
    their weight). The CSS always ends with ``* {font-family: <family>;} p {margin:0}``.
    """
    lang = Lang.parse(target_lang)
    css, archive, family = html_font_setup(lang, fonts_dir)
    if css and archive is not None:
        regular = find_font_file(lang, extra_dir=fonts_dir)
        if regular is not None:
            css += _extra_face_rules(regular, family)
    css += f"* {{font-family: {family};}} p {{margin:0}}"
    return css, archive


def _extra_face_rules(regular: Path, family: str) -> str:
    """``@font-face`` rules for bold / italic files that live beside ``regular``."""
    stem = regular.stem
    base = stem[: -len("-Regular")] if stem.endswith("-Regular") else stem
    rules = []
    for variant, suffixes in _FACE_VARIANTS.items():
        for suffix in suffixes:
            candidate = regular.with_name(base + suffix + regular.suffix)
            if candidate.is_file():
                rules.append(f"@font-face {{font-family: {family}; src: url({candidate.name}); "
                             f"{_FACE_DESCRIPTORS[variant]}}}\n")
                break
    return "".join(rules)


def segment_html(seg: TextSegment, text: str, line_height: Optional[float] = None) -> str:
    """HTML paragraph for ``insert_htmlbox`` reproducing the segment's style.

    The text is HTML-escaped, line breaks become ``<br>`` and the font size
    (px = pt inside the Story engine), colour, weight, italic, alignment and
    line height come from ``seg.style``. ``line_height`` overrides the style's
    line height (used for the tighter-fit attempt).
    """
    st = seg.style
    size = st.size if st.size > 0 else 10.0
    lh = line_height if line_height is not None else st.line_height
    if lh <= 0:
        lh = 1.25
    style = (
        f"font-size:{size:.2f}px;"
        f"color:#{st.color & 0xFFFFFF:06x};"
        f"font-weight:{'bold' if st.bold else 'normal'};"
        f"font-style:{'italic' if st.italic else 'normal'};"
        f"text-align:{st.align};"
        f"line-height:{lh:.2f}"
    )
    body = text.replace("\r\n", "\n").replace("\r", "\n").replace("\t", " ")
    body = _html.escape(body, quote=False).replace("\n", "<br>")
    return f'<p style="{style}">{body}</p>'


def html_rotation(style: SegmentStyle) -> int:
    """``insert_htmlbox(rotate=...)`` value for ``style``.

    ``SegmentStyle.rotation`` already *is* that value (0 / 90 / 180 / 270, the
    convention of ``mathtrans.extract``: 90 = text running up the page, 270 =
    running down); it is only normalised here. Vertical CJK segments without
    an explicit rotation are laid out running down the page (270), the closest
    the HTML engine offers to upright vertical writing.
    """
    rotation = int(round(style.rotation / 90.0)) * 90 % 360
    if rotation == 0 and style.is_vertical:
        rotation = 270
    return rotation


def unrotated_page_rect(page: pymupdf.Page) -> pymupdf.Rect:
    """The page rectangle in the unrotated space that text, image and drawing
    coordinates use (``page.rect`` is the displayed, possibly rotated, page)."""
    rect = pymupdf.Rect(page.rect)
    if page.rotation:
        rect = (rect * page.derotation_matrix).normalize()
    return rect


# --------------------------------------------------------------------------- #
# Free-space bookkeeping for box extension
# --------------------------------------------------------------------------- #


def _clip(box: BBox, page: BBox) -> Optional[BBox]:
    c = BBox(x0=max(box.x0, page.x0), y0=max(box.y0, page.y0), x1=min(box.x1, page.x1), y1=min(box.y1, page.y1))
    if c.x1 - c.x0 <= 0 or c.y1 - c.y0 <= 0:
        return None
    return c


class _PageSpace:
    """Occupied areas of one page, used to extend text boxes into free space.

    Obstacles are the other segments of the page (their *used* box once they
    are rendered), the page images, text blocks that no segment covers (they
    stay on the page) and vector drawings that do not touch the box. Drawings
    that enclose a box (frames, boxed examples) act as containers: the box may
    grow inside them but never across their border. Growth also stops at the
    page's content area (union of text and images, plus a small tolerance) so
    that no translation ends up in the page margins.
    """

    def __init__(self, page: pymupdf.Page, page_index: int, doc: TranslatedDocument):
        self.page_rect = BBox.from_rect(unrotated_page_rect(page))
        self._page = page
        self.occupied: dict[str, BBox] = {s.id: s.bbox for s in doc.segments if s.page == page_index}
        self.fixed: list[BBox] = []
        self._drawings: Optional[list[BBox]] = None
        try:
            image_boxes = [BBox.from_rect(info["bbox"]) for info in page.get_image_info()]
        except Exception as exc:  # corrupt image dictionaries: fall back to the extractor's placements
            log.warning("page %d: cannot read image placements (%s); using the extracted ones", page_index, exc)
            image_boxes = []
        for pi in doc.pages:
            if pi.index == page_index:
                image_boxes.extend(pi.image_bboxes)
        for box in image_boxes:
            clipped = _clip(box, self.page_rect)
            if clipped is not None:
                self.fixed.append(clipped)
        page_segments = list(self.occupied.values())
        content: Optional[BBox] = None
        self.lines: list[BBox] = []
        for raw in page.get_text("dict", flags=pymupdf.TEXTFLAGS_DICT)["blocks"]:
            if raw["type"] != 0:
                continue
            block = BBox.from_rect(raw["bbox"])
            if block.area <= 0:
                continue
            self.lines.extend(BBox.from_rect(line["bbox"]) for line in raw["lines"])
            content = block if content is None else content.union(block)
            covered = any(s.intersection_area(block) >= 0.5 * block.area for s in page_segments)
            if not covered:
                self.fixed.append(block)
        for box in page_segments + self.fixed:
            content = box if content is None else content.union(box)
        if content is None:
            content = self.page_rect
        pr = self.page_rect
        self.limit_left = max(min(content.x0 - CONTENT_TOLERANCE, pr.x0 + EDGE_MARGIN), pr.x0 + PAGE_MARGIN)
        self.limit_right = min(max(content.x1 + CONTENT_TOLERANCE, pr.x1 - EDGE_MARGIN), pr.x1 - PAGE_MARGIN)
        self.limit_bottom = min(max(content.y1 + CONTENT_TOLERANCE, pr.y1 - EDGE_MARGIN), pr.y1 - PAGE_MARGIN)

    def drawings(self) -> list[BBox]:
        if self._drawings is None:
            boxes: list[BBox] = []
            try:
                for d in self._page.get_drawings():
                    r = d.get("rect")
                    if r is None or r.is_empty or r.is_infinite:
                        continue
                    boxes.append(BBox.from_rect(r))
            except Exception as exc:  # pragma: no cover - defensive: exotic content streams
                log.warning("get_drawings failed on page %d: %s", self._page.number, exc)
            self._drawings = boxes
        return self._drawings

    def update(self, seg_id: str, used: BBox) -> None:
        self.occupied[seg_id] = used

    def extend(self, seg: TextSegment, *, down: bool, horizontal: bool) -> BBox:
        """Grow ``seg.bbox`` into free space (downward and/or sideways)."""
        box = seg.bbox
        obstacles = [b for sid, b in self.occupied.items() if sid != seg.id] + list(self.fixed)
        containers: list[BBox] = []
        for d in self.drawings():
            if d.contains(box, tol=1.0):
                containers.append(d)
            elif d.intersection_area(box) <= 0:
                obstacles.append(d)
        x0, y0, x1, y1 = box.x0, box.y0, box.x1, box.y1
        if down:
            y1 = self._extend_down(box, obstacles, containers)
        if horizontal:
            x0, x1 = self._extend_horizontal(BBox(x0=x0, y0=y0, x1=x1, y1=y1), seg.style.align, obstacles, containers)
        return BBox(x0=x0, y0=y0, x1=x1, y1=y1)

    def _extend_down(self, box: BBox, obstacles: list[BBox], containers: list[BBox]) -> float:
        limit = box.y1 + MAX_HEIGHT_GROWTH * box.height
        limit = min(limit, max(self.limit_bottom, box.y1))
        for c in containers:
            limit = min(limit, max(c.y1 - OBSTACLE_GAP, box.y1))
        for o in obstacles:
            if o.y1 <= box.y1 or min(o.x1, box.x1) - max(o.x0, box.x0) <= 0:
                continue
            limit = min(limit, max(o.y0 - OBSTACLE_GAP, box.y1))
        return limit

    def _extend_horizontal(self, box: BBox, align: str, obstacles: list[BBox],
                           containers: list[BBox]) -> tuple[float, float]:
        growth = max(MAX_WIDTH_GROWTH * box.width, MIN_WIDTH_GROWTH)
        right = min(box.x1 + growth, max(self.limit_right, box.x1))
        left = max(box.x0 - growth, min(self.limit_left, box.x0))
        # Column walls: wide text blocks entirely to one side of the box mark another
        # column; never grow across the gutter, even where that column has white space.
        min_wall_width = COLUMN_MIN_WIDTH_FRACTION * self.page_rect.width
        for o in obstacles:
            if o.width < min_wall_width:
                continue
            if o.x0 >= box.x1 - 1.0:
                right = min(right, max(o.x0 - OBSTACLE_GAP, box.x1))
            elif o.x1 <= box.x0 + 1.0:
                left = max(left, min(o.x1 + OBSTACLE_GAP, box.x0))
        for c in containers:
            right = min(right, max(c.x1 - OBSTACLE_GAP, box.x1))
            left = max(left, min(c.x0 + OBSTACLE_GAP, box.x0))
        for o in obstacles:
            if min(o.y1, box.y1) - max(o.y0, box.y0) <= 0:
                continue
            # An obstacle that already reaches into the box blocks that side entirely.
            if o.x1 > box.x1:
                right = min(right, max(o.x0 - OBSTACLE_GAP, box.x1))
            if o.x0 < box.x0:
                left = max(left, min(o.x1 + OBSTACLE_GAP, box.x0))
        if align == "right":
            return left, box.x1
        if align == "center":
            side = min(box.x0 - left, right - box.x1)
            return box.x0 - side, box.x1 + side
        return box.x0, right


# --------------------------------------------------------------------------- #
# Placing one segment
# --------------------------------------------------------------------------- #


def _insert(page: pymupdf.Page, rect: BBox, html: str, *, css: str, archive: Optional[pymupdf.Archive],
            scale_low: float, rotate: int) -> tuple[float, float]:
    spare, scale = page.insert_htmlbox(rect.to_rect(), html, css=css, scale_low=scale_low,
                                       archive=archive, rotate=rotate)
    return float(spare), float(scale)


def _place_segment(page: pymupdf.Page, seg: TextSegment, text: str, space: _PageSpace, *, css: str,
                   archive: Optional[pymupdf.Archive], min_scale: float) -> RenderInfo:
    """Insert ``text`` for ``seg`` and report what was done.

    Attempts, in order (a failed ``insert_htmlbox`` writes nothing, so retrying
    is safe):

    1. the original box at the original size (nothing changes);
    2. the box grown into free space (down by <= 50 % of its height, sideways
       on the side its alignment anchors away from), still at full size -
       growing into white space is far less visible than a different font size;
    3. the grown box shrunk down to ``min_scale``;
    4. the grown box with the tighter line height (1.1) shrunk to ``min_scale``;
    5. otherwise the grown box with unlimited shrinking: the translation stays on
       the page as editable text and ``overflow=True`` makes QA report it.

    Rotated / vertical segments skip the growth (their flow direction is not the
    page's) and go through the same ladder with their original box.
    """
    rotate = html_rotation(seg.style)
    base = seg.bbox
    grown = space.extend(seg, down=True, horizontal=True) if rotate == 0 else base
    grown_note = "" if grown == base else "box extended into free space"
    tight = TIGHT_LINE_HEIGHT if seg.style.line_height > TIGHT_LINE_HEIGHT + 1e-6 else None
    attempts: list[tuple[BBox, Optional[float], float, str]] = [(base, None, 1.0, "")]
    if grown != base:
        attempts.append((grown, None, 1.0, grown_note))
    attempts.append((grown, None, min_scale, grown_note))
    if tight is not None:
        attempts.append((grown, tight, min_scale, "tight line height"))
    size = seg.style.size if seg.style.size > 0 else 10.0
    for rect, lh, scale_low, note in attempts:
        spare, scale = _insert(page, rect, segment_html(seg, text, lh), css=css, archive=archive,
                               scale_low=scale_low, rotate=rotate)
        if spare >= 0:
            notes = [n for n in (grown_note if rect == grown else "", note) if n]
            if scale < 1:
                notes.append(f"shrunk to {scale:.2f}")
            return RenderInfo(font_size=round(size * scale, 3), scale=scale, spare_height=spare,
                              overflow=False, bbox=rect, notes="; ".join(dict.fromkeys(notes)))
    # Nothing fits at min_scale: render anyway in the largest box tried, shrinking as
    # much as needed so the text stays on the page (editable), and flag the overflow.
    rect, lh, _, _ = attempts[-1]
    _, scale = _insert(page, rect, segment_html(seg, text, lh), css=css, archive=archive,
                       scale_low=0, rotate=rotate)
    # The text just fits the box at ``scale``; set at ``min_scale`` it would need about
    # (min_scale / scale)^2 times the area, i.e. that much more height at the same width.
    missing = rect.height * ((min_scale / scale) ** 2 - 1) if scale > 0 else rect.height
    log.warning("segment %s overflows its box: rendered at scale %.2f (< %.2f)", seg.id, scale, min_scale)
    return RenderInfo(font_size=round(size * scale, 3), scale=scale, spare_height=-round(missing, 2),
                      overflow=True, bbox=rect,
                      notes=f"text does not fit at scale {min_scale:.2f}; shrunk to {scale:.2f}")


def _cut_away(rect: pymupdf.Rect, other: BBox, gap: float) -> pymupdf.Rect:
    """Shrink ``rect`` so that it no longer intersects ``other`` (plus ``gap``),
    cutting on the side that loses the least area; unchanged when impossible."""
    options: list[tuple[float, pymupdf.Rect]] = []
    if other.y0 - gap > rect.y0:
        options.append(((rect.y1 - other.y0 + gap) * rect.width, pymupdf.Rect(rect.x0, rect.y0, rect.x1, other.y0 - gap)))
    if other.y1 + gap < rect.y1:
        options.append(((other.y1 + gap - rect.y0) * rect.width, pymupdf.Rect(rect.x0, other.y1 + gap, rect.x1, rect.y1)))
    if other.x0 - gap > rect.x0:
        options.append(((rect.x1 - other.x0 + gap) * rect.height, pymupdf.Rect(rect.x0, rect.y0, other.x0 - gap, rect.y1)))
    if other.x1 + gap < rect.x1:
        options.append(((other.x1 + gap - rect.x0) * rect.height, pymupdf.Rect(other.x1 + gap, rect.y0, rect.x1, rect.y1)))
    if not options:
        return rect
    return min(options, key=lambda o: o[0])[1]


def _redaction_rect(seg: TextSegment, page_rect: pymupdf.Rect, lines: Sequence[BBox]) -> Optional[pymupdf.Rect]:
    """Rectangle whose redaction removes the segment's glyphs and nothing else.

    The segment box is shrunk by ``REDACT_SHRINK`` and then cut back wherever it
    still intersects a text line that is not part of the segment (less than half
    of the line inside the segment box), because adjacent lines' font boxes
    overlap and MuPDF drops a glyph at ~10 % coverage. Returns None for a
    degenerate box or one outside the page (``page_rect`` is the unrotated
    page rectangle).
    """
    rect = seg.bbox.to_rect() & page_rect
    if rect.is_empty:
        return None
    if rect.width > 2 * REDACT_SHRINK + 0.1 and rect.height > 2 * REDACT_SHRINK + 0.1:
        rect = pymupdf.Rect(rect.x0 + REDACT_SHRINK, rect.y0 + REDACT_SHRINK,
                            rect.x1 - REDACT_SHRINK, rect.y1 - REDACT_SHRINK)
    for line in lines:
        if line.area <= 0 or line.intersection_area(seg.bbox) >= 0.5 * line.area:
            continue  # the segment's own line
        if BBox.from_rect(rect).intersection_area(line) <= 0:
            continue
        rect = _cut_away(rect, line, REDACT_SHRINK)
    return rect


def _renderable(seg: TextSegment) -> bool:
    """Text segments with a translation that differs from the source."""
    if seg.kind != SegmentKind.TEXT or seg.translated_text is None:
        return False
    if not seg.translated_text.strip():
        log.debug("segment %s: empty translation, keeping the original text", seg.id)
        return False
    if seg.translated_text == seg.source_text:
        log.debug("segment %s: translation identical to the source, keeping the original glyphs", seg.id)
        return False
    return True


def render_page_segments(page: pymupdf.Page, page_index: int, segments: Sequence[TextSegment],
                         doc: TranslatedDocument, *, css: str, archive: Optional[pymupdf.Archive],
                         min_font_scale: float) -> list[RenderInfo]:
    """Redact and re-insert ``segments`` (all on ``page``); fills ``seg.render``."""
    page_rect = unrotated_page_rect(page)
    ordered = sorted(segments, key=lambda s: (s.reading_order, s.bbox.y0, s.bbox.x0))
    space = _PageSpace(page, page_index, doc)  # must inspect the text blocks before redaction
    todo: list[TextSegment] = []
    for seg in ordered:
        rect = _redaction_rect(seg, page_rect, space.lines)
        if rect is None:
            log.warning("segment %s: box %s is empty or lies outside page %d, skipped",
                        seg.id, seg.bbox.as_tuple(), page_index)
            seg.render = RenderInfo(font_size=seg.style.size, scale=1.0, overflow=False, bbox=seg.bbox,
                                    notes="box empty or outside the page; not rendered")
            continue
        page.add_redact_annot(rect, fill=False)
        todo.append(seg)
    if todo:
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    infos: list[RenderInfo] = []
    for seg in todo:
        info = _place_segment(page, seg, seg.translated_text or "", space, css=css, archive=archive,
                              min_scale=min_font_scale)
        seg.render = info
        if info.bbox is not None:
            space.update(seg.id, info.bbox)
        infos.append(info)
    return infos


# --------------------------------------------------------------------------- #
# Public entry points
# --------------------------------------------------------------------------- #


def render_document(src_pdf: PathLike, doc: TranslatedDocument, out_pdf: PathLike, *,
                    min_font_scale: float = 0.55, fonts_dir: Optional[PathLike] = None,
                    pages: Optional[list[int]] = None) -> list[RenderInfo]:
    """Write ``out_pdf`` = ``src_pdf`` with every translated text segment re-rendered.

    Only ``SegmentKind.TEXT`` segments whose ``translated_text`` is set (and
    differs from the source) are touched; image text is handled by
    ``images.render_image_segments``. Page count, page sizes, images and vector
    graphics are preserved. ``pages`` restricts the work to those 0-based pages.
    Returns the ``RenderInfo`` of every rendered segment (also stored in
    ``seg.render``).
    """
    if not 0 < min_font_scale <= 1:
        raise ValueError(f"min_font_scale must be in (0, 1], got {min_font_scale}")
    src_path, out_path = Path(src_pdf), Path(out_pdf)
    css, archive = page_css(doc.target_lang, fonts_dir)
    pdf = pymupdf.open(str(src_path))
    try:
        if pdf.needs_pass:
            raise ValueError(f"{src_path} is encrypted; decrypt it before translating")
        if pages is None:
            wanted = list(range(pdf.page_count))
        else:
            bad = [p for p in pages if not 0 <= p < pdf.page_count]
            if bad:
                raise ValueError(f"page indices out of range for a {pdf.page_count}-page document: {bad}")
            wanted = sorted(set(pages))
        by_page: dict[int, list[TextSegment]] = {}
        for seg in doc.segments:
            if not _renderable(seg):
                continue
            if not 0 <= seg.page < pdf.page_count:
                log.warning("segment %s refers to page %d but %s has %d page(s); skipped",
                            seg.id, seg.page, src_path, pdf.page_count)
                continue
            by_page.setdefault(seg.page, []).append(seg)
        infos: list[RenderInfo] = []
        for pno in wanted:
            segs = by_page.get(pno)
            if not segs:
                continue
            page_infos = render_page_segments(pdf[pno], pno, segs, doc, css=css, archive=archive,
                                              min_font_scale=min_font_scale)
            infos.extend(page_infos)
            log.info("page %d: rendered %d segments (%d overflow, %d shrunk)", pno, len(page_infos),
                     sum(1 for i in page_infos if i.overflow), sum(1 for i in page_infos if i.scale < 1))
        _save(pdf, src_path, out_path)
    finally:
        pdf.close()
    log.info("rendered %d segments into %s (%d overflow)", len(infos), out_path,
             sum(1 for i in infos if i.overflow))
    return infos


def _save(pdf: pymupdf.Document, src_path: Path, out_path: Path) -> None:
    """Save with duplicate-object merging (``garbage=4``): every ``insert_htmlbox``
    call embeds its own full copy of the font, which would otherwise multiply
    the file size by the number of segments."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    options = dict(garbage=4, deflate=True)
    if out_path.exists() and out_path.resolve() == src_path.resolve():
        fd, tmp = tempfile.mkstemp(prefix=out_path.stem + "-", suffix=".pdf", dir=str(out_path.parent))
        os.close(fd)
        try:
            pdf.save(tmp, **options)
            os.replace(tmp, out_path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        return
    pdf.save(str(out_path), **options)


def render_page_previews(pdf: Union[PathLike, pymupdf.Document], out_dir: PathLike, dpi: int = 110,
                         pages: Optional[list[int]] = None) -> list[str]:
    """Rasterise pages to ``out_dir/page-NNN.png`` (1-based numbers) and return the paths."""
    if dpi <= 0:
        raise ValueError(f"dpi must be positive, got {dpi}")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    owned = not isinstance(pdf, pymupdf.Document)
    document = pymupdf.open(str(pdf)) if owned else pdf
    try:
        if pages is None:
            wanted = list(range(document.page_count))
        else:
            bad = [p for p in pages if not 0 <= p < document.page_count]
            if bad:
                raise ValueError(f"page indices out of range for a {document.page_count}-page document: {bad}")
            wanted = sorted(set(pages))
        paths: list[str] = []
        for pno in wanted:
            target = out / f"page-{pno + 1:03d}.png"
            document[pno].get_pixmap(dpi=dpi).save(str(target))
            paths.append(str(target))
    finally:
        if owned:
            document.close()
    log.info("wrote %d preview(s) at %d dpi to %s", len(paths), dpi, out)
    return paths
