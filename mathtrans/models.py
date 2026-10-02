"""Shared data models for the translation pipeline.

Every module in the package exchanges data through the types defined here, so
they are deliberately plain pydantic models that serialise to JSON (projects
persist them on disk and the web API returns them).

Coordinate conventions
----------------------
* Page coordinates are PDF points with the origin at the top-left corner, i.e.
  exactly what PyMuPDF (``page.get_text("dict")``, ``page.rect``) uses.
* Image pixel coordinates have the origin at the top-left corner of the image.
* ``page`` indices are 0-based everywhere.
"""
from __future__ import annotations

import re
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

# --------------------------------------------------------------------------- #
# Languages
# --------------------------------------------------------------------------- #


class Lang(str, Enum):
    ZH = "zh"
    EN = "en"
    PT = "pt"
    ES = "es"
    JA = "ja"
    KO = "ko"

    @classmethod
    def parse(cls, value: "str | Lang") -> "Lang":
        if isinstance(value, Lang):
            return value
        v = str(value).strip().lower().replace("_", "-")
        aliases = {
            "zh": "zh", "zh-cn": "zh", "zh-hans": "zh", "chinese": "zh", "中文": "zh", "cn": "zh",
            "en": "en", "en-us": "en", "english": "en", "英语": "en", "英文": "en",
            "pt": "pt", "pt-br": "pt", "portuguese": "pt", "português": "pt", "葡萄牙语": "pt",
            "es": "es", "spanish": "es", "español": "es", "西班牙语": "es",
            "ja": "ja", "jp": "ja", "japanese": "ja", "日本語": "ja", "日语": "ja",
            "ko": "ko", "kr": "ko", "korean": "ko", "한국어": "ko", "韩语": "ko",
        }
        if v not in aliases:
            raise ValueError(f"Unsupported language: {value!r}")
        return cls(aliases[v])


SUPPORTED_LANGS: tuple[Lang, ...] = (Lang.ZH, Lang.EN, Lang.PT, Lang.ES, Lang.JA, Lang.KO)


# --------------------------------------------------------------------------- #
# Geometry
# --------------------------------------------------------------------------- #


class BBox(BaseModel):
    """Axis-aligned rectangle in page points (top-left origin)."""

    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def width(self) -> float:
        return max(0.0, self.x1 - self.x0)

    @property
    def height(self) -> float:
        return max(0.0, self.y1 - self.y0)

    @property
    def area(self) -> float:
        return self.width * self.height

    @classmethod
    def from_rect(cls, rect: Any) -> "BBox":
        """Build from a PyMuPDF Rect / IRect / 4-sequence."""
        if hasattr(rect, "x0"):
            return cls(x0=float(rect.x0), y0=float(rect.y0), x1=float(rect.x1), y1=float(rect.y1))
        x0, y0, x1, y1 = rect
        return cls(x0=float(x0), y0=float(y0), x1=float(x1), y1=float(y1))

    def to_rect(self):
        import pymupdf  # local import keeps models importable without PyMuPDF

        return pymupdf.Rect(self.x0, self.y0, self.x1, self.y1)

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.x0, self.y0, self.x1, self.y1)

    def union(self, other: "BBox") -> "BBox":
        return BBox(
            x0=min(self.x0, other.x0),
            y0=min(self.y0, other.y0),
            x1=max(self.x1, other.x1),
            y1=max(self.y1, other.y1),
        )

    def intersection_area(self, other: "BBox") -> float:
        w = min(self.x1, other.x1) - max(self.x0, other.x0)
        h = min(self.y1, other.y1) - max(self.y0, other.y0)
        return w * h if w > 0 and h > 0 else 0.0

    def contains(self, other: "BBox", tol: float = 0.5) -> bool:
        return (
            other.x0 >= self.x0 - tol
            and other.y0 >= self.y0 - tol
            and other.x1 <= self.x1 + tol
            and other.y1 <= self.y1 + tol
        )

    def expanded(self, dx: float, dy: Optional[float] = None) -> "BBox":
        dy = dx if dy is None else dy
        return BBox(x0=self.x0 - dx, y0=self.y0 - dy, x1=self.x1 + dx, y1=self.y1 + dy)


# --------------------------------------------------------------------------- #
# Text structure
# --------------------------------------------------------------------------- #


class TextSpan(BaseModel):
    """A run of text with uniform style, as extracted from the PDF."""

    text: str
    font: str = ""
    size: float = 10.0
    bold: bool = False
    italic: bool = False
    color: int = 0  # sRGB packed as 0xRRGGBB
    bbox: BBox
    is_math: bool = False  # span judged to be a formula / variable (kept verbatim)


Align = Literal["left", "center", "right", "justify"]


class SegmentStyle(BaseModel):
    """Dominant style of a segment, used to re-render the translation."""

    font: str = ""
    size: float = 10.0
    color: int = 0
    bold: bool = False
    italic: bool = False
    serif: bool = False
    align: Align = "left"
    line_height: float = 1.25  # multiple of font size
    rotation: int = 0  # PyMuPDF rotate value: 0 upright, 90 = text runs upward, 270 = downward, 180 upside down
    is_vertical: bool = False
    role: Literal["body", "heading", "caption", "label", "list", "table", "other"] = "body"


class ImageRef(BaseModel):
    """Where a piece of in-image text lives, in both page and pixel space."""

    xref: int
    page: int
    bbox: BBox  # placement rectangle of the whole image on the page
    width: int  # image pixel size
    height: int
    pixel_box: tuple[int, int, int, int]  # x0, y0, x1, y1 of the text region in image pixels
    polygon: list[list[float]] = Field(default_factory=list)  # 4 points, pixel coords
    confidence: float = 1.0


class RenderInfo(BaseModel):
    """What the layout engine did when placing the translated text."""

    font_size: float = 0.0
    scale: float = 1.0  # final scale factor applied to fit the box (1.0 = no shrink)
    spare_height: float = 0.0  # unused vertical space in the box (negative = overflow)
    overflow: bool = False
    bbox: Optional[BBox] = None  # rectangle actually used for the text
    notes: str = ""


class SegmentKind(str, Enum):
    TEXT = "text"  # native PDF text
    IMAGE_TEXT = "image_text"  # text recognised inside a raster image


class TextSegment(BaseModel):
    """The unit of translation: usually one paragraph / block, or one OCR line.

    ``source_text`` is the plain original text. ``protected_text`` is what is
    sent to the translator: formulas, numbers and other fragments that must be
    kept verbatim are replaced by placeholders ``⟦n⟧`` whose originals are in
    ``protected``. ``translation_raw`` is the translator output (still with
    placeholders) and ``translated_text`` the final text with placeholders
    restored.
    """

    id: str
    page: int
    kind: SegmentKind = SegmentKind.TEXT
    bbox: BBox
    source_text: str
    protected_text: str = ""
    protected: list[str] = Field(default_factory=list)
    spans: list[TextSpan] = Field(default_factory=list)
    style: SegmentStyle = Field(default_factory=SegmentStyle)
    image: Optional[ImageRef] = None
    translate: bool = True  # False => copied through untouched (pure math, numbers, empty)
    skip_reason: str = ""
    translation_raw: Optional[str] = None
    translated_text: Optional[str] = None
    attempts: int = 0
    feedback: list[str] = Field(default_factory=list)  # QA feedback for re-translation
    render: Optional[RenderInfo] = None
    reading_order: int = 0
    origin: Literal["pdf", "ocr"] = "pdf"  # "ocr": paragraph assembled from OCR lines of a scanned page
    members: list[str] = Field(default_factory=list)  # ids of the OCR line segments merged into this one

    @property
    def effective_text(self) -> str:
        """Text that ends up on the page (translation, or source if not translated)."""
        if self.translated_text is not None:
            return self.translated_text
        return self.source_text


# --------------------------------------------------------------------------- #
# Placeholders for protected fragments
# --------------------------------------------------------------------------- #

PLACEHOLDER_OPEN = "⟦"
PLACEHOLDER_CLOSE = "⟧"
PLACEHOLDER_RE = re.compile(r"⟦(\d+)⟧")


def make_placeholder(index: int) -> str:
    return f"{PLACEHOLDER_OPEN}{index}{PLACEHOLDER_CLOSE}"


def placeholder_indices(text: str) -> list[int]:
    return [int(m.group(1)) for m in PLACEHOLDER_RE.finditer(text)]


def restore_placeholders(text: str, protected: list[str]) -> str:
    """Replace ``⟦n⟧`` by ``protected[n]``; unknown indices are left untouched."""

    def _sub(m: re.Match) -> str:
        i = int(m.group(1))
        return protected[i] if 0 <= i < len(protected) else m.group(0)

    return PLACEHOLDER_RE.sub(_sub, text)


# --------------------------------------------------------------------------- #
# Glossary
# --------------------------------------------------------------------------- #


class GlossaryEntry(BaseModel):
    """One concept with its preferred term in each language (keys are language codes)."""

    terms: dict[str, str]
    note: str = ""

    def get(self, lang: "Lang | str") -> Optional[str]:
        code = Lang.parse(lang).value
        term = self.terms.get(code)
        return term.strip() if term and term.strip() else None


class Glossary(BaseModel):
    id: str = "default"
    name: str = "Default math glossary"
    entries: list[GlossaryEntry] = Field(default_factory=list)

    def pairs(self, src: "Lang | str", tgt: "Lang | str") -> list[tuple[str, str]]:
        """(source term, target term) pairs, longest source term first."""
        out: list[tuple[str, str]] = []
        for e in self.entries:
            s, t = e.get(src), e.get(tgt)
            if s and t and s != t:
                out.append((s, t))
        out.sort(key=lambda p: (-len(p[0]), p[0]))
        return out

    def merged_with(self, other: Optional["Glossary"]) -> "Glossary":
        """Entries of ``other`` take precedence: an entry of this glossary is dropped
        when any of its terms (same language) is also a term of a custom entry, so a
        custom ``斜边 => hypotenuse side`` really replaces the built-in pair instead
        of coexisting with it."""
        if other is None:
            return self

        def norm(term: str) -> str:
            import unicodedata

            return unicodedata.normalize("NFKC", term).casefold().strip()

        taken = {(lang, norm(term)) for e in other.entries for lang, term in e.terms.items()
                 if term and term.strip()}
        kept = [e for e in self.entries
                if not any((lang, norm(term)) in taken for lang, term in e.terms.items() if term and term.strip())]
        return Glossary(id=other.id, name=other.name, entries=list(other.entries) + kept)


# --------------------------------------------------------------------------- #
# Translation / review / OCR exchange types
# --------------------------------------------------------------------------- #


class TranslationItem(BaseModel):
    id: str
    text: str  # protected text (with placeholders)
    kind: SegmentKind = SegmentKind.TEXT
    context: str = ""  # e.g. "heading", "figure caption", "label inside a diagram"
    max_chars: Optional[int] = None  # soft hint for space-constrained labels
    feedback: list[str] = Field(default_factory=list)  # QA feedback from a previous round
    previous: Optional[str] = None  # previous (rejected) translation


class TranslationResult(BaseModel):
    id: str
    text: str
    notes: str = ""


class ReviewItem(BaseModel):
    id: str
    source: str
    translation: str
    context: str = ""


class ReviewFinding(BaseModel):
    id: str
    severity: Literal["error", "warning"]
    category: str  # meaning | omission | number | terminology | grammar | format | untranslated
    message: str
    suggested_fix: Optional[str] = None


class OcrResult(BaseModel):
    text: str
    polygon: list[list[float]]  # 4 points [[x, y], ...] in image pixels, clockwise from top-left
    confidence: float = 1.0

    @property
    def box(self) -> tuple[int, int, int, int]:
        xs = [p[0] for p in self.polygon]
        ys = [p[1] for p in self.polygon]
        return (int(min(xs)), int(min(ys)), int(max(xs) + 0.999), int(max(ys) + 0.999))


# --------------------------------------------------------------------------- #
# QA
# --------------------------------------------------------------------------- #

Severity = Literal["error", "warning"]


class QAIssue(BaseModel):
    check: str
    severity: Severity
    message: str
    segment_id: Optional[str] = None
    page: Optional[int] = None
    details: dict[str, Any] = Field(default_factory=dict)
    fixable: bool = True  # True => re-translating the segment may fix it


class QARound(BaseModel):
    round: int
    issues: list[QAIssue] = Field(default_factory=list)
    retranslated: list[str] = Field(default_factory=list)
    passed: bool = False
    duration_s: float = 0.0


class QAReport(BaseModel):
    passed: bool = False
    rounds: list[QARound] = Field(default_factory=list)
    checks_run: list[str] = Field(default_factory=list)
    final_issues: list[QAIssue] = Field(default_factory=list)
    errors: int = 0
    warnings: int = 0
    duration_s: float = 0.0
    summary: str = ""


# --------------------------------------------------------------------------- #
# Document / pipeline
# --------------------------------------------------------------------------- #


class PageInfo(BaseModel):
    index: int
    width: float
    height: float
    rotation: int = 0
    image_bboxes: list[BBox] = Field(default_factory=list)  # for layout-preservation checks


class TranslatedDocument(BaseModel):
    """Everything the pipeline knows about one document."""

    source_path: str
    source_lang: Lang
    target_lang: Lang
    pages: list[PageInfo] = Field(default_factory=list)
    segments: list[TextSegment] = Field(default_factory=list)
    glossary: Optional[Glossary] = None
    title: str = ""

    @property
    def page_count(self) -> int:
        return len(self.pages)

    def segment(self, seg_id: str) -> Optional[TextSegment]:
        for s in self.segments:
            if s.id == seg_id:
                return s
        return None

    def text_segments(self) -> list[TextSegment]:
        return [s for s in self.segments if s.kind == SegmentKind.TEXT]

    def image_segments(self) -> list[TextSegment]:
        return [s for s in self.segments if s.kind == SegmentKind.IMAGE_TEXT]

    def translatable(self) -> list[TextSegment]:
        return [s for s in self.segments if s.translate]


class PipelineOptions(BaseModel):
    target_lang: Lang
    source_lang: Optional[Lang] = None  # None => auto-detect
    glossary: Optional[Glossary] = None  # merged on top of the built-in default glossary
    use_default_glossary: bool = True
    translate_images: bool = True
    bilingual: bool = False
    export_docx: bool = False
    max_qa_rounds: int = 3
    require_qa_pass: bool = True
    llm_review: bool = True  # semantic review by Claude (skipped automatically with the mock translator)
    min_font_scale: float = 0.55
    translator: str = "auto"  # auto | claude | mock
    ocr_engine: str = "auto"  # auto | rapid | claude | none
    model: Optional[str] = None
    pages: Optional[list[int]] = None  # restrict processing to these 0-based pages (debug / preview)
    skip_pages: Optional[list[int]] = None  # 0-based pages copied through untouched (e.g. a page with a QR code)
    preview_dpi: int = 110
    subset_fonts: bool = False  # subset embedded fonts (much smaller file, but editors can only reuse embedded glyphs)
    # Scanned pages (one full-page image, no text layer): "repaint" draws the translation into
    # the page image; "overlay" erases the recognised text in the image and places the
    # translation as real, editable PDF text (OCR lines are grouped into paragraphs first).
    scanned_mode: Literal["repaint", "overlay"] = "repaint"


class PipelineStats(BaseModel):
    pages: int = 0
    pages_skipped: int = 0
    text_segments: int = 0
    image_segments: int = 0
    translated: int = 0
    skipped: int = 0
    images_processed: int = 0
    qa_rounds: int = 0
    duration_s: float = 0.0
    translator: str = ""
    ocr_engine: str = ""
    model: str = ""
    source_lang: str = ""
    target_lang: str = ""


class PipelineResult(BaseModel):
    status: Literal["completed", "qa_failed", "error"]
    output_pdf: Optional[str] = None
    bilingual_pdf: Optional[str] = None
    docx: Optional[str] = None
    segments_json: Optional[str] = None
    qa_report_json: Optional[str] = None
    qa_report: Optional[QAReport] = None
    stats: PipelineStats = Field(default_factory=PipelineStats)
    error: Optional[str] = None
    preview_pages: list[str] = Field(default_factory=list)  # PNG paths, one per page


def parse_page_spec(spec: Optional[str], page_count: Optional[int] = None) -> Optional[list[int]]:
    """Parse a user-facing page specification such as ``"2,5-7"`` (1-based, inclusive
    ranges, ``7-`` means "to the end") into sorted unique 0-based indices.

    Returns ``None`` for an empty specification. Raises ``ValueError`` for malformed
    input or, when ``page_count`` is given, for pages outside the document.
    """
    if spec is None:
        return None
    text = str(spec).strip().replace("，", ",").replace("－", "-").replace("—", "-")
    if not text:
        return None
    pages: set[int] = set()
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo_s, hi_s = part.split("-", 1)
            lo_s, hi_s = lo_s.strip(), hi_s.strip()
            if not lo_s.isdigit() or (hi_s and not hi_s.isdigit()):
                raise ValueError(f"invalid page range: {part!r}")
            lo = int(lo_s)
            if hi_s:
                hi = int(hi_s)
            elif page_count is not None:
                hi = page_count
            else:
                raise ValueError(f"open range {part!r} needs the page count")
        else:
            if not part.isdigit():
                raise ValueError(f"invalid page number: {part!r}")
            lo = hi = int(part)
        if lo < 1 or hi < lo:
            raise ValueError(f"invalid page range: {part!r}")
        if page_count is not None and hi > page_count:
            raise ValueError(f"page {hi} is beyond the last page ({page_count})")
        pages.update(range(lo - 1, hi))
    return sorted(pages) if pages else None
