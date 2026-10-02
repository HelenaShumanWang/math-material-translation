"""Text extraction: turn PDF pages into :class:`~mathtrans.models.TextSegment` objects.

Responsibilities
----------------
* one segment per text block of ``page.get_text("dict")``; the block's lines are
  joined according to the source script (CJK: no separator, Latin: spaces plus
  de-hyphenation) and list markers are kept verbatim,
* placeholder protection of formulas, numbers and math-font spans through
  :func:`mathtrans.protect.protect_text`,
* the dominant style of each block (font, size, colour, weight, alignment, line
  height, rotation) and a role heuristic (heading / caption / list / label / body),
* a column-aware reading order,
* per-page :class:`~mathtrans.models.PageInfo` (size, rotation, image placements)
  and document-level source-language detection.

Coordinates
-----------
All boxes are PyMuPDF points with a top-left origin in the *unrotated* page space.
That is the space in which ``get_text``, ``get_image_info``, ``add_redact_annot``
and ``insert_htmlbox`` operate (verified empirically for pages with ``/Rotate``),
so ``PageInfo.width``/``height`` describe that space as well; the displayed size of
a page rotated by 90/270 degrees has width and height swapped.

``SegmentStyle.rotation`` is the ``rotate`` argument that ``page.insert_text`` /
``page.insert_htmlbox`` need in order to reproduce the extracted writing
direction: ``(1, 0) -> 0``, ``(0, -1) -> 90`` (text runs upwards), ``(-1, 0) -> 180``,
``(0, 1) -> 270`` (text runs downwards).
"""
from __future__ import annotations

import bisect
import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence, Union

import pymupdf

from .languages import detect_language, is_cjk, letters_of_script, script_profile
from .models import (
    Align,
    BBox,
    Lang,
    PageInfo,
    SegmentKind,
    SegmentStyle,
    TextSegment,
    TextSpan,
    TranslatedDocument,
)
from .protect import OPERATORS, is_fully_protected, protect_text

log = logging.getLogger("mathtrans.extract")

PdfSource = Union[str, Path, pymupdf.Document]

#: Flags for ``page.get_text("dict")``: the standard dict flags without image payloads
#: (image placements come from ``get_image_info``) and with ligatures expanded, so that
#: "ﬁ" is extracted as "fi" and QA / glossary comparisons see plain letters.
TEXT_FLAGS: int = (pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES) & ~pymupdf.TEXT_PRESERVE_LIGATURES

# --------------------------------------------------------------------------- #
# Heuristic tables
# --------------------------------------------------------------------------- #

_MATH_FONT_RE = re.compile(
    r"cmmi|cmsy|cmex|cmbsy|msam|msbm|symbol|math|mtextra|euclid|mt-|asana|xits|stix|rsfs|wasy|esint|txsy|pxsy",
    re.IGNORECASE,
)
_BOLD_NAME_RE = re.compile(r"bold|black|heavy", re.IGNORECASE)
_ITALIC_NAME_RE = re.compile(r"italic|oblique", re.IGNORECASE)
_SERIF_NAME_RE = re.compile(
    r"serif|times|song|simsun|ming|mincho|batang|roman|georgia|garamond|cambria|palatino|minion"
    r"|bookman|century|baskerville|didot|bodoni|charis",
    re.IGNORECASE,
)
_SANS_NAME_RE = re.compile(
    r"sans|gothic|hei\b|heiti|arial|helvetica|verdana|tahoma|calibri|segoe|roboto|lato|futura|gill|droid",
    re.IGNORECASE,
)

# List markers: "1." "1)" "(1)" "（1）" "①" "⑴" "•" "a." "(a)" "一、" "iv." ...
# Numeric markers may be glued to CJK text ("3.判断") but not to digits/dots ("1.1", "12.5 cm");
# letter, roman and bullet markers need a following space ("e.g.", "-x" are not markers).
_LIST_MARKER_RE = re.compile(
    r"^(?:"
    r"(?:\(?[0-9０-９]{1,3}[.)、．]|[（(][0-9０-９]{1,3}[)）]|[一二三四五六七八九十]{1,3}[、.．])(?=\s|[^0-9０-９.])"
    r"|[①-⑳㉑-㉟⑴-⒇⒈-⒛㊀-㊉]"
    r"|(?:\(?[A-Za-z][.)]|[（(][A-Za-z][)）]|[ivxIVX]{1,5}[.)]|[•·▪◦‣○●■□◆◇★☆※▶►➢✓\-–—])\s"
    r")"
)
_CAPTION_RE = re.compile(
    r"^(?:(?:图|表|図|그림|표)\s*[0-9０-９]"
    r"|(?:figure|fig\.?|figura|tabela|tabla|table)\s*[0-9])",
    re.IGNORECASE,
)
_SENTENCE_END = ".!?。！？；;:：…\"”’』」）)"
_SINGLE_LABEL_RE = re.compile(r"^[A-Za-z](?:[0-9]{0,2}|['’′]{0,2})$")

# Characters that have a Unicode superscript form (used for spans flagged as superscript).
_SUPERSCRIPT_MAP = str.maketrans({
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "+": "⁺", "-": "⁻", "−": "⁻", "=": "⁼", "(": "⁽", ")": "⁾", "n": "ⁿ", "i": "ⁱ",
})
_SUPERSCRIPTABLE = set("0123456789+-−=()ni")

_WS_RE = re.compile(r"[ \t ]+")
_STRIP_CHARS = " \t 　\r\n"
_LATIN_JOIN_CHARS = "=+−-×÷"  # CJK lines ending with these are followed by a space before ASCII text
_CJK = r"぀-ヿ㐀-䶿一-鿿豈-﫿가-힯々-〇"
_CJK_CHAR_RE = re.compile(f"[{_CJK}]")
_CJK_LATIN_SPACED_RE = re.compile(f"[{_CJK}] [A-Za-z0-9]|[A-Za-z0-9] [{_CJK}]")
_CJK_LATIN_GLUED_RE = re.compile(f"[{_CJK}][A-Za-z0-9]|[A-Za-z0-9][{_CJK}]")

# Reading-order parameters (points / fractions).
_COLUMN_MIN_GAP = 8.0  # minimum horizontal gap between two real columns
_WIDE_FRACTION = 0.55  # blocks at least this wide (relative to the text area) never define a column
_COLUMN_MIN_WEIGHT = 0.15  # share of the (narrow) text height a column needs to count
_VALLEY_FRACTION = 0.25  # x-coverage below this share of the neighbouring peaks is a gutter
_FURNITURE_ZONE = 0.1  # top / bottom share of the page where single-line blocks are headers/footers
_ROW_OVERLAP_FRACTION = 0.5  # vertical overlap (relative to the smaller box) to share a row


# --------------------------------------------------------------------------- #
# Public helpers
# --------------------------------------------------------------------------- #


def is_math_font(font_name: str) -> bool:
    """Whether ``font_name`` denotes a math / symbol font (CMMI, CMSY, Symbol, STIX ...)."""
    return bool(font_name) and _MATH_FONT_RE.search(font_name) is not None


def rotation_from_dir(direction: Sequence[float]) -> int:
    """Map a PyMuPDF line direction ``(dx, dy)`` to the ``rotate`` value (0/90/180/270)
    that ``insert_text`` / ``insert_htmlbox`` need to reproduce it."""
    dx, dy = float(direction[0]), float(direction[1])
    if abs(dx) >= abs(dy):
        return 0 if dx >= 0 else 180
    return 90 if dy < 0 else 270


def is_list_item(text: str) -> bool:
    """Whether ``text`` starts with a list marker such as ``1.``, ``(1)``, ``①`` or ``•``."""
    return _LIST_MARKER_RE.match(text.lstrip(_STRIP_CHARS)) is not None


def is_caption(text: str) -> bool:
    """Whether ``text`` starts like a figure / table caption (图 1, Figure 2, 表 3 ...)."""
    return _CAPTION_RE.match(text.lstrip(_STRIP_CHARS)) is not None


# --------------------------------------------------------------------------- #
# Document level
# --------------------------------------------------------------------------- #


def _check_document(doc: pymupdf.Document, label: str) -> None:
    """Raise ``ValueError`` unless ``doc`` is a readable PDF with at least one page."""
    if not doc.is_pdf:  # PyMuPDF also opens images, XPS, EPUB and plain text as documents
        raise ValueError(f"{label} is not a PDF document")
    if doc.needs_pass:
        raise ValueError(f"{label} is password protected; decrypt it before translating")
    if doc.page_count == 0:
        raise ValueError(f"{label} contains no pages")


def _open_document(source: PdfSource) -> tuple[pymupdf.Document, bool]:
    """Return ``(document, owned)``; ``owned`` tells the caller to close it."""
    if isinstance(source, pymupdf.Document):
        if source.is_closed:
            raise ValueError("The PyMuPDF document is already closed")
        _check_document(source, source.name or "The PyMuPDF document")
        return source, False
    path = Path(source)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    try:
        # filetype="pdf": the content decides, not the file extension
        doc = pymupdf.open(str(path), filetype="pdf")
    except Exception as exc:  # pymupdf raises various error types
        raise ValueError(f"Cannot open {path} as a PDF: {exc}") from exc
    try:
        _check_document(doc, str(path))
    except ValueError:
        doc.close()
        raise
    return doc, True


def _normalise_pages(pages: Optional[Iterable[int]], page_count: int) -> Optional[set[int]]:
    if pages is None:
        return None
    out: set[int] = set()
    for p in pages:
        if isinstance(p, bool) or not isinstance(p, int):
            raise ValueError(f"Page indices must be integers, got {p!r}")
        if p < 0 or p >= page_count:
            raise ValueError(f"Page index {p} out of range for a {page_count}-page document (0-based)")
        out.add(p)
    return out


def detect_document_language(pdf_path_or_doc: PdfSource) -> Lang:
    """Detect the dominant language of a PDF from the text of all its pages.

    Falls back to :attr:`Lang.ZH` (with a warning) when the document contains no
    letters at all, e.g. a scanned document without a text layer.
    """
    doc, owned = _open_document(pdf_path_or_doc)
    try:
        chunks = [page.get_text("text", flags=TEXT_FLAGS) for page in doc]
    finally:
        if owned:
            doc.close()
    text = "\n".join(chunks)
    lang = detect_language(text)
    if lang is None:
        log.warning("No letters found in the document text layer; assuming source language zh")
        return Lang.ZH
    log.debug("Detected document language %s from %d characters", lang.value, len(text))
    return lang


def extract_document(
    pdf_path: PdfSource,
    *,
    target_lang: Lang | str,
    source_lang: Lang | str | None = None,
    pages: Optional[list[int]] = None,
) -> TranslatedDocument:
    """Extract every text block of ``pdf_path`` into a :class:`TranslatedDocument`.

    ``pdf_path`` is a file path or an open :class:`pymupdf.Document` (which is
    left open). ``pages`` (0-based) restricts which pages get segments; a
    :class:`PageInfo` is still created for every page so that layout and QA know
    the whole document. When ``source_lang`` is ``None`` it is auto-detected over
    all text.

    Raises ``FileNotFoundError`` for a missing file and ``ValueError`` for a
    file that is not a PDF, a password-protected or empty document, or an
    invalid page index.
    """
    target = Lang.parse(target_lang)
    doc, owned = _open_document(pdf_path)
    try:
        source = Lang.parse(source_lang) if source_lang is not None else detect_document_language(doc)
        if source == target:
            log.warning("Source and target language are both %s", source.value)
        page_set = _normalise_pages(pages, doc.page_count)
        page_infos: list[PageInfo] = []
        segments: list[TextSegment] = []
        for pno in range(doc.page_count):
            page = doc[pno]
            page_infos.append(build_page_info(page, pno))
            if page_set is None or pno in page_set:
                page_segments = build_page_segments(page, pno, source)
                segments.extend(page_segments)
                log.debug("page %d: %d segments (%d translatable)", pno, len(page_segments),
                          sum(1 for s in page_segments if s.translate))
        title = _document_title(doc, segments)
        # an in-memory Document has no name (None)
        source_path = (pdf_path.name or "") if isinstance(pdf_path, pymupdf.Document) else str(pdf_path)
    finally:
        if owned:
            doc.close()
    log.info(
        "Extracted %d segments (%d translatable) from %d pages of %s [%s -> %s]",
        len(segments), sum(1 for s in segments if s.translate), len(page_infos), source_path,
        source.value, target.value,
    )
    return TranslatedDocument(
        source_path=source_path,
        source_lang=source,
        target_lang=target,
        pages=page_infos,
        segments=segments,
        title=title,
    )


def _document_title(doc: pymupdf.Document, segments: list[TextSegment]) -> str:
    meta_title = (doc.metadata or {}).get("title") or ""
    meta_title = meta_title.strip()
    if meta_title:
        return meta_title[:200]
    for seg in segments:
        if seg.style.role == "heading" and seg.source_text.strip():
            return seg.source_text.strip().splitlines()[0][:200]
    return ""


# --------------------------------------------------------------------------- #
# Page info
# --------------------------------------------------------------------------- #


def _page_space_rect(page: pymupdf.Page) -> pymupdf.Rect:
    """The page rectangle in the unrotated coordinate space used by text extraction."""
    rect = pymupdf.Rect(page.rect)
    if page.rotation:
        rect = (rect * page.derotation_matrix).normalize()
    return rect


def build_page_info(page: pymupdf.Page, index: int) -> PageInfo:
    """Size, rotation and de-duplicated image placements (clipped to the page) of ``page``."""
    rect = _page_space_rect(page)
    boxes: list[BBox] = []
    seen: set[tuple[float, float, float, float]] = set()
    try:
        infos = page.get_image_info(xrefs=True)
    except Exception as exc:  # corrupt image dictionaries must not abort extraction
        log.warning("page %d: cannot read image placements (%s)", index, exc)
        infos = []
    for info in infos:
        placed = pymupdf.Rect(info["bbox"]) & rect
        if placed.is_empty or placed.width < 1 or placed.height < 1:
            continue
        key = (round(placed.x0, 1), round(placed.y0, 1), round(placed.x1, 1), round(placed.y1, 1))
        if key in seen:
            continue
        seen.add(key)
        boxes.append(BBox.from_rect(placed))
    return PageInfo(index=index, width=float(rect.width), height=float(rect.height),
                    rotation=int(page.rotation), image_bboxes=boxes)


# --------------------------------------------------------------------------- #
# Page level: blocks -> segments
# --------------------------------------------------------------------------- #


@dataclass
class _Line:
    text: str
    bbox: BBox
    direction: tuple[float, float]
    wmode: int
    baseline: float  # origin y (horizontal lines) or origin x (vertical lines)
    chars: int


@dataclass
class _SpanInfo:
    span: TextSpan
    serif: bool
    chars: int


@dataclass
class _BlockData:
    bbox: BBox
    lines: list[_Line] = field(default_factory=list)
    spans: list[_SpanInfo] = field(default_factory=list)


def build_page_segments(page: pymupdf.Page, page_index: int, source_lang: Lang | str) -> list[TextSegment]:
    """All text blocks of ``page`` as segments in reading order, ids ``p{page}_b{n}`` assigned."""
    lang = Lang.parse(source_lang)
    page_rect = _page_space_rect(page)
    raw = page.get_text("dict", flags=TEXT_FLAGS)
    blocks = [b for b in raw.get("blocks", []) if b.get("type") == 0 and b.get("lines")]
    median_size = _page_median_size(blocks)
    segments: list[TextSegment] = []
    for block in blocks:
        data = _collect_block(block, page_rect)
        if data is None:
            continue
        segments.append(_segment_from_block(data, page_index, lang, median_size, page_rect))
    ordered = sort_reading_order(segments, page_height=page_rect.height)
    for idx, seg in enumerate(ordered):
        seg.id = f"p{page_index}_b{idx}"
        seg.reading_order = idx
    return ordered


def _page_median_size(blocks: list[dict[str, Any]]) -> float:
    """Character-weighted median font size of a page (10 pt when the page has no text)."""
    weights: Counter[float] = Counter()
    for block in blocks:
        for line in block["lines"]:
            for span in line["spans"]:
                n = len(span["text"].strip())
                if n:
                    weights[round(float(span["size"]), 1)] += n
    total = sum(weights.values())
    if total == 0:
        return 10.0
    acc = 0
    for size in sorted(weights):
        acc += weights[size]
        if acc * 2 >= total:
            return size
    return max(weights)


def _collect_block(block: dict[str, Any], page_rect: pymupdf.Rect) -> Optional[_BlockData]:
    """Normalise one raw text block: span texts, line texts and geometry."""
    bbox_rect = pymupdf.Rect(block["bbox"])
    clipped = bbox_rect & page_rect
    bbox = BBox.from_rect(clipped if not clipped.is_empty else bbox_rect)
    data = _BlockData(bbox=bbox)
    for line in block["lines"]:
        spans = line.get("spans") or []
        if not spans:
            continue
        line_max_size = max(float(s["size"]) for s in spans)
        parts: list[str] = []
        for span in spans:
            text = _span_text(span, line_max_size)
            parts.append(text)
            stripped = text.strip(_STRIP_CHARS)
            if not stripped:
                continue
            font = str(span.get("font") or "")
            flags = int(span.get("flags") or 0)
            bold = bool(flags & 16) or _BOLD_NAME_RE.search(font) is not None
            italic = bool(flags & 2) or _ITALIC_NAME_RE.search(font) is not None
            serif = _SANS_NAME_RE.search(font) is None and (bool(flags & 4) or _SERIF_NAME_RE.search(font) is not None)
            is_math = is_math_font(font) or (italic and len(stripped) == 1 and stripped.isascii() and stripped.isalpha())
            data.spans.append(_SpanInfo(
                span=TextSpan(text=text, font=font, size=float(span["size"]), bold=bold, italic=italic,
                              color=int(span.get("color") or 0), bbox=BBox.from_rect(span["bbox"]),
                              is_math=is_math),
                serif=serif,
                chars=len(stripped),
            ))
        line_text = _WS_RE.sub(" ", "".join(parts)).strip(_STRIP_CHARS)
        direction = tuple(float(v) for v in line.get("dir", (1.0, 0.0)))
        origin = spans[0].get("origin") or (line["bbox"][0], line["bbox"][3])
        vertical = abs(direction[1]) > abs(direction[0])
        data.lines.append(_Line(
            text=line_text,
            bbox=BBox.from_rect(line["bbox"]),
            direction=(direction[0], direction[1]),
            wmode=int(line.get("wmode") or 0),
            baseline=float(origin[0] if vertical else origin[1]),
            chars=len(line_text),
        ))
    if not data.lines:
        return None
    return data


def _span_text(span: dict[str, Any], line_max_size: float) -> str:
    """Span text; raised small spans of digits/signs become Unicode superscripts (x2 -> x²)."""
    text = str(span.get("text") or "")
    flags = int(span.get("flags") or 0)
    stripped = text.strip()
    if (
        flags & 1
        and stripped
        and len(stripped) <= 3
        and float(span["size"]) < 0.9 * line_max_size
        and all(ch in _SUPERSCRIPTABLE for ch in stripped)
    ):
        return text.translate(_SUPERSCRIPT_MAP)
    return text


def _segment_from_block(
    data: _BlockData, page_index: int, lang: Lang, median_size: float, page_rect: pymupdf.Rect
) -> TextSegment:
    style = _block_style(data, lang, median_size, page_rect)
    text = _join_lines(data.lines, _joins_without_space(data.lines, lang, style.size), style.size,
                       korean=lang is Lang.KO)
    math_fragments = [
        _WS_RE.sub(" ", info.span.text).strip(_STRIP_CHARS)
        for info in data.spans
        if info.span.is_math and not all(ch in OPERATORS or ch.isspace() for ch in info.span.text)
    ]
    protected_text, protected = protect_text(text, lang, extra_fragments=math_fragments)
    translate, reason = _skip_reason(text, protected_text, lang)
    style.role = _role(text, data, style, median_size, page_rect, is_fully_protected(protected_text))
    return TextSegment(
        id="",
        page=page_index,
        kind=SegmentKind.TEXT,
        bbox=data.bbox,
        source_text=text,
        protected_text=protected_text,
        protected=protected,
        spans=[info.span for info in data.spans],
        style=style,
        translate=translate,
        skip_reason=reason,
    )


def _skip_reason(text: str, protected_text: str, lang: Lang) -> tuple[bool, str]:
    """``(translate, skip_reason)`` for a block's text."""
    stripped = text.strip(_STRIP_CHARS)
    if not stripped:
        return False, "empty"
    if is_fully_protected(protected_text):
        return False, "no translatable text (numbers / formula only)"
    if _SINGLE_LABEL_RE.match(stripped):
        return False, "single-letter label"
    if letters_of_script(stripped, lang) == 0 and script_profile(stripped)["latin"] == 0:
        return False, f"no letters of the source script ({lang.value}) and no Latin letters"
    return True, ""


# --------------------------------------------------------------------------- #
# Line joining
# --------------------------------------------------------------------------- #


def _joins_without_space(lines: list[_Line], lang: Lang, size: float) -> bool:
    """Whether the line breaks of a block stand for nothing (CJK wrapping) or for a space.

    Chinese and Japanese are always wrapped between characters; Latin scripts at
    spaces. Korean is written with spaces but may be wrapped either way, so a
    block counts as word-wrapped (break = space) as soon as one of its breaks is
    "loose": the first character of the following line would still have fitted on
    the line that was ended.
    """
    if not is_cjk(lang):
        return False
    if lang is not Lang.KO:
        return True
    texts = [ln for ln in lines if ln.text and abs(ln.direction[0]) >= abs(ln.direction[1])]
    if len(texts) < 2:
        return True
    right_edge = max(ln.bbox.x1 for ln in texts)
    for prev, cur in zip(texts, texts[1:]):
        first = cur.text[0]
        glyph = size if _CJK_CHAR_RE.match(first) else 0.55 * size
        if right_edge - prev.bbox.x1 >= glyph + 0.25 * size:
            return False
    return True


def _join_lines(lines: list[_Line], cjk: bool, size: float, korean: bool = False) -> str:
    """Join the lines of a block into one paragraph text.

    * ``cjk`` (breaks between characters): no separator; a space is kept between
      ASCII words / numbers split by the line break (``BC =`` + ``8`` -> ``BC = 8``)
      and between CJK and ASCII when the block itself spaces them (``a 和 b``);
      ``korean`` blocks space Hangul -> Latin/digit but attach particles (``c라``).
    * otherwise (breaks at spaces): lines are joined with a space and
      ``word-`` + ``word`` is de-hyphenated.
    * An explicit ``"\\n"`` is kept where a line ends with sentence punctuation and the
      next line starts a list item, is indented, or the ended line is clearly short.
    """
    texts = [ln for ln in lines if ln.text]
    if not texts:
        return ""
    block_x0 = min(ln.bbox.x0 for ln in texts)
    block_x1 = max(ln.bbox.x1 for ln in texts)
    block_w = max(block_x1 - block_x0, 1.0)
    out = texts[0].text
    spaced_convention = cjk and _cjk_latin_spaced(ln.text for ln in texts)
    for prev, cur in zip(texts, texts[1:]):
        if _paragraph_break(prev, cur, block_x0, block_w, size, cjk):
            out += "\n" + cur.text
            continue
        last, first = out[-1], cur.text[0]
        if cjk:
            out += _cjk_joiner(last, first, spaced_convention, korean) + cur.text
            continue
        if last == "­":  # soft hyphen: always a hyphenation point
            out = out[:-1] + cur.text
        elif last in "-‐" and len(out) >= 2 and out[-2].isalpha() and first.isalpha():
            out = (out[:-1] if first.islower() else out) + cur.text
        else:
            out += " " + cur.text
    return out


def _paragraph_break(prev: _Line, cur: _Line, block_x0: float, block_w: float, size: float, cjk: bool) -> bool:
    if prev.text[-1] not in _SENTENCE_END:
        return False
    horizontal = abs(prev.direction[0]) >= abs(prev.direction[1])
    if not horizontal:
        return is_list_item(cur.text)
    if is_list_item(cur.text):
        return True
    indent = cur.bbox.x0 - prev.bbox.x0
    if indent >= 0.8 * size and prev.bbox.x0 - block_x0 < 0.5 * size:
        return True
    prev_fill = (prev.bbox.x1 - block_x0) / block_w
    return prev_fill < (0.7 if cjk else 0.55)


def _cjk_latin_spaced(line_texts: Iterable[str]) -> bool:
    """Whether a block separates CJK and Latin/digit runs with spaces (``为 a 和 b``)
    more often than it glues them (``为a和b``); decides what a line break stands for."""
    spaced = glued = 0
    for text in line_texts:
        spaced += len(_CJK_LATIN_SPACED_RE.findall(text))
        glued += len(_CJK_LATIN_GLUED_RE.findall(text))
    return spaced > glued


def _cjk_joiner(last: str, first: str, spaced_convention: bool, korean: bool = False) -> str:
    """Separator between two CJK-source lines: a space between ASCII tokens, and
    between a CJK character and an ASCII token when the block spaces them.
    Korean always spaces Hangul -> ASCII (``삼각형 4개``) and never ASCII -> Hangul,
    where a particle or counter attaches to the token (``c라``, ``4개``)."""
    last_ascii = (last.isascii() and last.isalnum()) or last in _LATIN_JOIN_CHARS
    first_ascii = (first.isascii() and first.isalnum()) or first in _LATIN_JOIN_CHARS or first == "("
    if last_ascii and first_ascii:
        return " "
    if korean:
        return " " if first_ascii and _CJK_CHAR_RE.match(last) else ""
    if spaced_convention and (
        (last_ascii and _CJK_CHAR_RE.match(first)) or (first_ascii and _CJK_CHAR_RE.match(last))
    ):
        return " "
    return ""


# --------------------------------------------------------------------------- #
# Style and role
# --------------------------------------------------------------------------- #


def _dominant(values: Iterable[tuple[Any, int]], default: Any) -> Any:
    """Value with the largest total weight (first seen wins ties)."""
    weights: dict[Any, int] = {}
    order: list[Any] = []
    for value, weight in values:
        if value not in weights:
            weights[value] = 0
            order.append(value)
        weights[value] += weight
    if not weights:
        return default
    return max(order, key=lambda v: (weights[v], -order.index(v)))


def _block_style(data: _BlockData, lang: Lang, median_size: float, page_rect: pymupdf.Rect) -> SegmentStyle:
    spans = [info for info in data.spans if info.chars]
    size = float(_dominant(((round(i.span.size, 1), i.chars) for i in spans), median_size))
    font = str(_dominant(((i.span.font, i.chars) for i in spans), ""))
    color = int(_dominant(((i.span.color, i.chars) for i in spans), 0))
    bold = bool(_dominant(((i.span.bold, i.chars) for i in spans), False))
    italic = bool(_dominant(((i.span.italic, i.chars) for i in spans), False))
    serif = bool(_dominant(((i.serif, i.chars) for i in spans), False))
    text_lines = [ln for ln in data.lines if ln.text]
    direction = _dominant(((ln.direction, ln.chars) for ln in text_lines), (1.0, 0.0))
    rotation = rotation_from_dir(direction)
    wmode = int(_dominant(((ln.wmode, ln.chars) for ln in text_lines), 0))
    joined = "".join(ln.text for ln in text_lines)
    cjk_letters = letters_of_script(joined, lang) if is_cjk(lang) else 0
    is_vertical = wmode == 1 or (rotation in (90, 270) and cjk_letters > 0
                                 and cjk_letters >= script_profile(joined)["latin"])
    return SegmentStyle(
        font=font,
        size=size,
        color=color,
        bold=bold,
        italic=italic,
        serif=serif,
        align=_alignment(text_lines, data.bbox, size, rotation, page_rect),
        line_height=_line_height(text_lines, size, rotation),
        rotation=rotation,
        is_vertical=is_vertical,
    )


def _alignment(lines: list[_Line], block: BBox, size: float, rotation: int, page_rect: pymupdf.Rect) -> Align:
    if rotation != 0 or not lines:
        return "left"
    tol = max(2.0, 0.15 * size)
    if len(lines) == 1:
        centre = (block.x0 + block.x1) / 2
        page_centre = (page_rect.x0 + page_rect.x1) / 2
        if abs(centre - page_centre) <= 2.0 and block.x0 - page_rect.x0 > 0.15 * page_rect.width:
            return "center"
        return "left"
    lefts = [ln.bbox.x0 - block.x0 for ln in lines]
    rights = [block.x1 - ln.bbox.x1 for ln in lines]
    if len(lines) >= 3 and all(r <= 2.0 for r in rights[:-1]) and all(l <= tol for l in lefts[1:]):
        return "justify"
    if all(abs(l - r) <= tol for l, r in zip(lefts, rights)) and any(l > tol for l in lefts):
        return "center"
    if all(r <= tol for r in rights) and any(l > tol for l in lefts):
        return "right"
    return "left"


def _line_height(lines: list[_Line], size: float, rotation: int) -> float:
    """Median baseline distance of consecutive lines as a multiple of the font size."""
    same_dir = [ln for ln in lines if rotation_from_dir(ln.direction) == rotation]
    if len(same_dir) < 2 or size <= 0:
        return 1.25
    gaps = [abs(b.baseline - a.baseline) for a, b in zip(same_dir, same_dir[1:])]
    gaps = [g for g in gaps if g > 0]
    if not gaps:
        return 1.25
    gaps.sort()
    median = gaps[len(gaps) // 2]
    return round(min(2.5, max(0.9, median / size)), 3)


def _word_count(text: str) -> int:
    """Approximate word count: whitespace tokens, or half the CJK letters if that is more."""
    prof = script_profile(text)
    cjk_letters = prof["han"] + prof["kana"] + prof["hangul"]
    return max(len(text.split()), (cjk_letters + 1) // 2)


def _role(text: str, data: _BlockData, style: SegmentStyle, median_size: float, page_rect: pymupdf.Rect,
          protected_only: bool) -> str:
    stripped = text.strip(_STRIP_CHARS)
    if not stripped:
        return "other"
    n_lines = sum(1 for ln in data.lines if ln.text)
    small_box = data.bbox.width <= 0.3 * page_rect.width and data.bbox.height <= 3.0 * style.size
    is_label = n_lines <= 2 and small_box and _word_count(stripped) <= 3
    if protected_only:  # formulas, page numbers: never a heading however large they are set
        return "label" if is_label else "other"
    if is_caption(stripped):
        return "caption"
    if style.size >= 1.25 * median_size:
        return "heading"
    if is_list_item(stripped):
        return "list"
    if style.bold and n_lines <= 2 and len(stripped) <= 120 and stripped[-1] not in ".!?。！？;；":
        return "heading"
    if is_label:
        return "label"
    return "body"


# --------------------------------------------------------------------------- #
# Reading order
# --------------------------------------------------------------------------- #


@dataclass
class _Column:
    x0: float
    x1: float
    members: list[int]

    @property
    def width(self) -> float:
        return self.x1 - self.x0


def sort_reading_order(segments: Sequence[TextSegment], page_height: Optional[float] = None) -> list[TextSegment]:
    """Return the segments of one page in reading order.

    Blocks are grouped into columns by their x-extent (gutters are gaps in the
    height-weighted x-projection of the narrow blocks; single-line blocks in the
    header / footer zones do not take part). When the page has at least two
    clearly separated, side-by-side columns, it is read column by column
    (top-to-bottom inside a column); blocks spanning several columns (titles,
    full-width paragraphs) and the header / footer blocks split the page into
    horizontal bands that are read one after the other, so a running head is
    read first and a page number last whatever margin it sits in. Otherwise
    blocks are read top-to-bottom, left-to-right (blocks on the same row go
    left to right).

    ``page_height`` locates the header / footer zones; without it the vertical
    extent of the blocks is used.
    """
    if len(segments) <= 1:
        return list(segments)
    boxes = [s.bbox for s in segments]
    content_w = max(b.x1 for b in boxes) - min(b.x0 for b in boxes)
    top, bottom = 0.0, page_height if page_height else max(b.y1 for b in boxes)
    if not page_height:
        top = min(b.y0 for b in boxes)
    zone = _FURNITURE_ZONE * (bottom - top)
    furniture = {
        i for i, s in enumerate(segments)
        if (s.bbox.y1 <= top + zone or s.bbox.y0 >= bottom - zone)
        and s.bbox.height <= 2.2 * max(s.style.size, 1.0)
        and s.bbox.width < 0.4 * content_w
    }
    columns = _detect_columns(boxes, furniture)
    if columns:
        order = _column_order(boxes, columns, furniture)
    else:
        order = _rows_order(list(range(len(boxes))), boxes)
    return [segments[i] for i in order]


def _coverage_cells(indices: list[int], boxes: list[BBox]) -> list[tuple[float, float, float]]:
    """Height-weighted x-projection: ``(x0, x1, covered_height)`` per elementary interval."""
    xs = sorted({v for i in indices for v in (boxes[i].x0, boxes[i].x1)})
    cells: list[tuple[float, float, float]] = []
    for a, b in zip(xs, xs[1:]):
        cover = sum(boxes[i].height for i in indices if boxes[i].x0 <= a and boxes[i].x1 >= b)
        cells.append((a, b, cover))
    return cells


def _gutters(cells: list[tuple[float, float, float]]) -> list[tuple[float, float]]:
    """x-intervals whose coverage is far below the peaks on both sides."""
    peak = max(c[2] for c in cells)
    out: list[tuple[float, float]] = []
    k = 0
    while k < len(cells):
        if cells[k][2] > _VALLEY_FRACTION * peak:
            k += 1
            continue
        j = k
        while j + 1 < len(cells) and cells[j + 1][2] <= _VALLEY_FRACTION * peak:
            j += 1
        left_peak = max((c[2] for c in cells[:k]), default=0.0)
        right_peak = max((c[2] for c in cells[j + 1:]), default=0.0)
        depth = max(c[2] for c in cells[k:j + 1])
        if (
            cells[j][1] - cells[k][0] >= _COLUMN_MIN_GAP
            and left_peak > 0 and right_peak > 0
            and depth <= _VALLEY_FRACTION * min(left_peak, right_peak)
        ):
            out.append((cells[k][0], cells[j][1]))
        k = j + 1
    return out


def _side_by_side(a: _Column, b: _Column, boxes: list[BBox]) -> bool:
    for i in a.members:
        for j in b.members:
            bi, bj = boxes[i], boxes[j]
            overlap = min(bi.y1, bj.y1) - max(bi.y0, bj.y0)
            if overlap > 0 and overlap >= 0.3 * min(bi.height, bj.height):
                return True
    return False


def _detect_columns(boxes: list[BBox], furniture: set[int]) -> list[_Column]:
    """Real columns of a page (empty list = single-column / free layout)."""
    content_w = max(b.x1 for b in boxes) - min(b.x0 for b in boxes)
    if content_w <= 0:
        return []
    narrow = [
        i for i, b in enumerate(boxes)
        if i not in furniture and 0 < b.width < _WIDE_FRACTION * content_w and b.height > 0
    ]
    total = sum(boxes[i].height for i in narrow)
    if len(narrow) < 2 or total <= 0:
        return []
    cells = _coverage_cells(narrow, boxes)
    gutters = _gutters(cells)
    if not gutters:
        return []
    edges = [cells[0][0], *(x for gutter in gutters for x in gutter), cells[-1][1]]
    columns: list[_Column] = []
    for x0, x1 in zip(edges[::2], edges[1::2]):
        members = [i for i in narrow if x0 <= (boxes[i].x0 + boxes[i].x1) / 2 <= x1]
        if members and sum(boxes[i].height for i in members) >= _COLUMN_MIN_WEIGHT * total:
            columns.append(_Column(x0=min(boxes[i].x0 for i in members),
                                   x1=max(boxes[i].x1 for i in members), members=members))
    if len(columns) < 2:
        return []
    paired = [
        col for k, col in enumerate(columns)
        if any(_side_by_side(col, other, boxes) for m, other in enumerate(columns) if m != k)
    ]
    return paired if len(paired) >= 2 else []


def _rows_order(indices: list[int], boxes: list[BBox]) -> list[int]:
    """Top-to-bottom, left-to-right: boxes sharing a row are read left to right."""
    rows: list[list[Any]] = []  # [y0, y1, members]
    for i in sorted(indices, key=lambda k: (boxes[k].y0, boxes[k].x0)):
        b = boxes[i]
        if rows:
            ry0, ry1, members = rows[-1]
            overlap = min(ry1, b.y1) - max(ry0, b.y0)
            if overlap > 0 and overlap >= _ROW_OVERLAP_FRACTION * min(b.height, ry1 - ry0):
                members.append(i)
                rows[-1][1] = max(ry1, b.y1)
                continue
        rows.append([b.y0, b.y1, [i]])
    out: list[int] = []
    for _, _, members in rows:
        out.extend(sorted(members, key=lambda k: (boxes[k].x0, boxes[k].y0)))
    return out


def _column_order(boxes: list[BBox], columns: list[_Column], furniture: set[int]) -> list[int]:
    """Column-by-column order; spanning blocks (and header / footer ``furniture``)
    cut the page into bands."""
    spanning: list[int] = []
    members: list[list[int]] = [[] for _ in columns]
    for i, b in enumerate(boxes):
        overlaps = [max(0.0, min(b.x1, c.x1) - max(b.x0, c.x0)) for c in columns]
        covering = sum(1 for o, c in zip(overlaps, columns) if c.width > 0 and o >= 0.25 * c.width)
        if covering >= 2 or i in furniture:
            spanning.append(i)
            continue
        centre = (b.x0 + b.x1) / 2
        col = next((k for k, c in enumerate(columns) if c.x0 - 1.0 <= centre <= c.x1 + 1.0), None)
        if col is None and b.width > 0:
            best = max(range(len(columns)), key=lambda k: overlaps[k])
            if overlaps[best] >= 0.5 * b.width:
                col = best
        if col is None:
            spanning.append(i)
        else:
            members[col].append(i)

    def centre_y(k: int) -> float:
        return (boxes[k].y0 + boxes[k].y1) / 2

    spanning.sort(key=lambda k: (centre_y(k), boxes[k].x0))
    cuts = [centre_y(k) for k in spanning]
    bands: list[list[list[int]]] = [[[] for _ in columns] for _ in range(len(spanning) + 1)]
    for k, col_members in enumerate(members):
        for i in col_members:
            bands[bisect.bisect_right(cuts, centre_y(i))][k].append(i)
    out: list[int] = []
    for band_idx, band in enumerate(bands):
        for col_members in band:
            out.extend(_rows_order(col_members, boxes))
        if band_idx < len(spanning):
            out.append(spanning[band_idx])
    return out
