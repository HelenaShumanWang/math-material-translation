"""Text inside raster images: locate it (OCR) and replace it with the translation.

:func:`extract_image_segments` walks the images placed on the pages of a PDF,
runs an :class:`~mathtrans.interfaces.OcrEngine` on each unique image XObject
and turns every recognised line into an ``IMAGE_TEXT``
:class:`~mathtrans.models.TextSegment` whose ``bbox`` is in page points and
whose ``image`` field records the pixel region.

:func:`render_image_segments` paints the translations back into the pixels
(background fill or inpainting, then text in a font for the target language,
sized to fit the original box) and swaps the image stream with
``page.replace_image`` so every placement of the image is updated while the
page layout, image placement and pixel dimensions stay unchanged.
"""
from __future__ import annotations

import io
import logging
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

import cv2
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont

from .fonts import pil_font
from .interfaces import OcrEngine
from .languages import is_cjk, letters_of_script, script_profile
from .models import (BBox, ImageRef, Lang, OcrResult, RenderInfo, SegmentKind, SegmentStyle, TextSegment,
                     TranslatedDocument)
from .ocr import OcrError
from .protect import is_fully_protected, protect_text

logger = logging.getLogger("mathtrans.images")

#: Smallest font (pixels) used when redrawing text; below this the result is unreadable.
MIN_FONT_PX = 8
#: Initial font size relative to the OCR box height.
FONT_HEIGHT_RATIO = 0.85
#: Width of the ring around a text box used to estimate the background colour.
RING_PX = 2
#: Per-channel standard deviation of the ring below which the background is "uniform".
UNIFORM_STD = 12.0
#: A box wider than this multiple of its height may be re-flowed into two lines.
TWO_LINE_ASPECT = 2.0
LINE_PITCH = 1.1
INPAINT_RADIUS = 3
#: Tolerance (page points) when matching an image placement by its rectangle.
PLACEMENT_TOL = 1.0
#: Max per-channel difference from the background for a pixel to count as free space.
FREE_TOL = 24
#: Free columns kept clear between redrawn text and the nearest obstacle.
FREE_MARGIN = 2
#: Text may grow into free background by at most this multiple of the box width on each side.
MAX_GROWTH = 1.25
#: A two-line split is only used when the shorter line is at least this fraction of the longer one.
MIN_LINE_BALANCE = 0.3

_LATIN_GREEK_RE = re.compile(r"[A-Za-zÀ-ɏΑ-ω]")

PdfSource = Union[str, Path, pymupdf.Document]


# --------------------------------------------------------------------------- #
# image loading
# --------------------------------------------------------------------------- #


@dataclass
class LoadedImage:
    """Decoded pixels of one image XObject."""

    xref: int
    rgb: np.ndarray  # HxWx3 uint8
    alpha: Optional[np.ndarray] = None  # HxW uint8, None when opaque
    ext: str = "png"
    smask_xref: int = 0
    is_mask: bool = False  # stencil mask (``/ImageMask true``): alpha = painted pixels

    @property
    def width(self) -> int:
        return int(self.rgb.shape[1])

    @property
    def height(self) -> int:
        return int(self.rgb.shape[0])

    def flattened(self) -> np.ndarray:
        """RGB composited over white - what a viewer shows for transparent pixels.

        The colour stored under fully transparent pixels is arbitrary (often
        black), so OCR must run on the flattened image, not on ``rgb``.
        """
        if self.alpha is None:
            return self.rgb
        a = self.alpha.astype(np.float32)[..., None] / 255.0
        return np.clip(self.rgb.astype(np.float32) * a + 255.0 * (1.0 - a) + 0.5, 0, 255).astype(np.uint8)


#: PIL modes that ``Image.convert("RGB")`` handles without losing information.
_PIL_SAFE_MODES = {"1", "L", "LA", "P", "PA", "RGB", "RGBA", "RGBX", "YCbCr"}


def _pixmap_rgb(pdf_doc: pymupdf.Document, xref: int) -> np.ndarray:
    """Decode an image XObject through MuPDF (handles CMYK/ICC/JPX/stencil masks)."""
    pix = pymupdf.Pixmap(pdf_doc, xref)
    if pix.alpha:
        pix = pymupdf.Pixmap(pix, 0)
    if pix.n != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return np.ascontiguousarray(arr[..., :3])


def _smask_alpha(pdf_doc: pymupdf.Document, smask_xref: int, width: int, height: int) -> Optional[np.ndarray]:
    try:
        spix = pymupdf.Pixmap(pdf_doc, smask_xref)
        if spix.alpha:
            spix = pymupdf.Pixmap(spix, 0)
        if spix.n != 1:
            spix = pymupdf.Pixmap(pymupdf.csGRAY, spix)
        alpha = np.frombuffer(spix.samples, dtype=np.uint8).reshape(spix.height, spix.width).copy()
    except Exception as exc:
        logger.warning("cannot decode soft mask xref %d: %s (treating the image as opaque)", smask_xref, exc)
        return None
    if alpha.shape != (height, width):
        alpha = cv2.resize(alpha, (width, height), interpolation=cv2.INTER_LINEAR)
    return alpha


def _is_stencil_mask(pdf_doc: pymupdf.Document, xref: int) -> bool:
    try:
        return pdf_doc.xref_get_key(xref, "ImageMask") == ("bool", "true")
    except Exception:  # bad xref / not a dictionary
        return False


def _stencil_mask_pixels(pdf_doc: pymupdf.Document, xref: int, info: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    """``(rgb, alpha)`` of a stencil mask: black ink where the mask paints, transparent elsewhere.

    MuPDF hands a stencil mask out as a gray PNG with ``/Decode`` applied and
    255 where the mask paints. The paint colour comes from the graphics state
    of each placement and is not part of the image, so black (by far the most
    common for scanned text) is assumed.
    """
    try:
        painted = np.array(Image.open(io.BytesIO(info["image"])).convert("L")) >= 128
    except Exception as exc:
        logger.debug("PIL cannot decode stencil mask xref %d (%s); using MuPDF", xref, exc)
        pix = pymupdf.Pixmap(pdf_doc, xref)
        samples = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        painted = samples[..., -1] >= 128
    alpha = np.where(painted, 255, 0).astype(np.uint8)
    rgb = np.where(painted[..., None], 0, 255).astype(np.uint8).repeat(3, axis=2)
    return np.ascontiguousarray(rgb), np.ascontiguousarray(alpha)


def load_image(pdf_doc: pymupdf.Document, xref: int) -> LoadedImage:
    """Decode image ``xref`` to RGB (+ alpha from its soft mask when present).

    Grayscale, palette, RGBA and CMYK sources are all normalised to RGB; CMYK,
    16-bit and formats PIL cannot open are decoded by MuPDF with proper colour
    management. Stencil masks (``/ImageMask true``, typical for scanned black
    and white pages) become black ink on a transparent background.
    Raises ``ValueError`` when ``xref`` is not an image.
    """
    try:
        info = pdf_doc.extract_image(xref)
    except (ValueError, RuntimeError) as exc:
        raise ValueError(f"xref {xref} is not an image: {exc}") from exc
    if not info or not info.get("image"):
        raise ValueError(f"xref {xref} is not an image")
    ext = str(info.get("ext", "png")).lower()
    smask = int(info.get("smask", 0) or 0)
    if _is_stencil_mask(pdf_doc, xref):
        rgb, alpha = _stencil_mask_pixels(pdf_doc, xref, info)
        return LoadedImage(xref=xref, rgb=rgb, alpha=alpha, ext="png", smask_xref=smask, is_mask=True)
    alpha: Optional[np.ndarray] = None
    rgb: Optional[np.ndarray] = None
    try:
        pil = Image.open(io.BytesIO(info["image"]))
        pil.load()
        if pil.mode == "CMYK" or int(info.get("colorspace", 3)) == 4 or pil.mode not in _PIL_SAFE_MODES:
            rgb = _pixmap_rgb(pdf_doc, xref)
        else:
            if pil.mode in ("RGBA", "LA", "PA") or (pil.mode == "P" and "transparency" in pil.info):
                rgba = np.array(pil.convert("RGBA"))
                alpha = np.ascontiguousarray(rgba[..., 3])
                rgb = np.ascontiguousarray(rgba[..., :3])
            else:
                rgb = np.array(pil.convert("RGB"))
    except Exception as exc:
        logger.debug("PIL cannot decode image xref %d (%s); using MuPDF", xref, exc)
        rgb = _pixmap_rgb(pdf_doc, xref)
    if rgb.ndim != 3 or rgb.shape[0] == 0 or rgb.shape[1] == 0:
        raise ValueError(f"image xref {xref} decoded to an empty array")
    if smask:
        mask_alpha = _smask_alpha(pdf_doc, smask, rgb.shape[1], rgb.shape[0])
        if mask_alpha is not None:
            alpha = mask_alpha
    return LoadedImage(xref=xref, rgb=np.ascontiguousarray(rgb), alpha=alpha, ext=ext, smask_xref=smask)


def encode_image(rgb: np.ndarray, alpha: Optional[np.ndarray], ext: str) -> bytes:
    """PNG bytes (RGBA when ``alpha`` is given); JPEG sources without alpha stay JPEG."""
    buf = io.BytesIO()
    if alpha is not None:
        rgba = np.dstack([rgb, alpha])
        Image.fromarray(rgba, "RGBA").save(buf, format="PNG")
    elif ext in ("jpeg", "jpg"):
        # quality 90 with 4:2:0 chroma keeps scanned pages close to their original size
        Image.fromarray(rgb, "RGB").save(buf, format="JPEG", quality=90, optimize=True)
    else:
        Image.fromarray(rgb, "RGB").save(buf, format="PNG")
    return buf.getvalue()


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #


def pixel_polygon_to_page(polygon: list[list[float]], width: int, height: int, transform: Any) -> BBox:
    """Page-space bounding box of an image-pixel polygon.

    ``transform`` is the ``transform`` entry of ``page.get_image_info`` - the
    matrix mapping the unit square (top-left origin) to the page. The result is
    exact for axis-aligned placements and the axis-aligned bounding box of the
    rotated region otherwise.
    """
    mat = pymupdf.Matrix(*transform)
    pts = [pymupdf.Point(x / width, y / height) * mat for x, y in polygon]
    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    return BBox(x0=min(xs), y0=min(ys), x1=max(xs), y1=max(ys))


def vertical_points_per_pixel(transform: Any, height: int) -> float:
    """Page points covered by one image pixel along the image's vertical axis.

    This is the length of the transform's second column divided by the pixel
    height, so it is right for rotated placements too (where the pixel rows run
    along the page's x axis).
    """
    _a, _b, c, d, _e, _f = (float(v) for v in transform)
    return math.hypot(c, d) / max(int(height), 1)


def pixel_box_to_page(box: tuple[int, int, int, int], ref: ImageRef, transform: Any = None) -> BBox:
    """Map an image-pixel box to page points.

    With the placement ``transform`` (from ``page.get_image_info``) the mapping
    is exact for rotated / flipped placements too; without it the box is scaled
    through the placement rectangle of ``ref`` (exact for unrotated images).
    """
    x0, y0, x1, y1 = box
    if transform is not None:
        return pixel_polygon_to_page([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], ref.width, ref.height, transform)
    sx = ref.bbox.width / max(ref.width, 1)
    sy = ref.bbox.height / max(ref.height, 1)
    return BBox(x0=ref.bbox.x0 + x0 * sx, y0=ref.bbox.y0 + y0 * sy, x1=ref.bbox.x0 + x1 * sx, y1=ref.bbox.y0 + y1 * sy)


def _clamp_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x0 = min(max(int(box[0]), 0), width)
    y0 = min(max(int(box[1]), 0), height)
    x1 = min(max(int(box[2]), 0), width)
    y1 = min(max(int(box[3]), 0), height)
    return (x0, y0, max(x0, x1), max(y0, y1))


# --------------------------------------------------------------------------- #
# colour estimation
# --------------------------------------------------------------------------- #


def ring_pixels(rgb: np.ndarray, box: tuple[int, int, int, int], ring: int = RING_PX) -> np.ndarray:
    """Pixels in a ``ring``-px frame around ``box`` (clipped to the image), ``Nx3``."""
    h, w = rgb.shape[:2]
    x0, y0, x1, y1 = box
    ox0, oy0, ox1, oy1 = max(x0 - ring, 0), max(y0 - ring, 0), min(x1 + ring, w), min(y1 + ring, h)
    outer = rgb[oy0:oy1, ox0:ox1]
    mask = np.ones(outer.shape[:2], dtype=bool)
    mask[y0 - oy0:y1 - oy0, x0 - ox0:x1 - ox0] = False
    px = outer[mask]
    if px.size == 0:  # box covers the whole image: use its border
        px = rgb[y0:y1, x0:x1].reshape(-1, rgb.shape[2])
    return px.reshape(-1, rgb.shape[2])


def estimate_background(rgb: np.ndarray, box: tuple[int, int, int, int],
                        alpha: Optional[np.ndarray] = None) -> tuple[np.ndarray, bool]:
    """(median ring colour, uniform?) for the surroundings of ``box``.

    With an ``alpha`` channel only visible ring pixels (alpha > 0) are used,
    because the colour stored under fully transparent pixels is arbitrary.
    """
    px = ring_pixels(rgb, box)
    if alpha is not None:
        visible = ring_pixels(alpha[..., None], box)[:, 0] > 0
        if visible.any():
            px = px[visible]
    if px.size == 0:
        return np.array([255, 255, 255], dtype=np.uint8), True
    median = np.median(px, axis=0)
    uniform = bool(px.std(axis=0).max() <= UNIFORM_STD)
    return np.clip(np.round(median), 0, 255).astype(np.uint8), uniform


def estimate_text_color(rgb: np.ndarray, box: tuple[int, int, int, int], background: Optional[np.ndarray] = None,
                        alpha: Optional[np.ndarray] = None) -> tuple[int, int, int]:
    """Colour of the glyphs inside ``box``: the pixels farthest from the background.

    The median of the pixels within 80 % of the maximum distance is used so a
    single stray pixel (anti-aliasing, a crossing line) does not win. With an
    ``alpha`` channel only opaque pixels (alpha > 128) are candidates.
    """
    x0, y0, x1, y1 = box
    region = rgb[y0:y1, x0:x1].reshape(-1, 3).astype(np.float32)
    if alpha is not None:
        opaque = alpha[y0:y1, x0:x1].reshape(-1) > 128
        if opaque.any():
            region = region[opaque]
    if region.size == 0:
        return (0, 0, 0)
    bg = (estimate_background(rgb, box, alpha)[0] if background is None else background).astype(np.float32)
    dist = np.linalg.norm(region - bg, axis=1)
    far = dist.max()
    if far < 20:  # nothing distinguishable from the background: default to dark text
        return (0, 0, 0)
    chosen = region[dist >= 0.8 * far]
    col = np.median(chosen, axis=0)
    return tuple(int(min(max(round(float(c)), 0), 255)) for c in col)


def rgb_to_int(color: tuple[int, int, int]) -> int:
    r, g, b = color
    return (r << 16) | (g << 8) | b


# --------------------------------------------------------------------------- #
# OCR result -> segment
# --------------------------------------------------------------------------- #


def _is_latin_or_greek(ch: str) -> bool:
    return bool(_LATIN_GREEK_RE.fullmatch(ch))


def classify_ocr_text(text: str, source_lang: Lang) -> tuple[str, list[str], bool, str]:
    """``(protected_text, fragments, translate, skip_reason)`` for an OCR line.

    Pure numbers / formulas (``is_fully_protected``), single Latin or Greek
    letters (diagram labels such as ``A``, ``B``, ``x``, ``α``) and text with
    neither source-script nor Latin letters (the same rule the text extractor
    applies) are kept as is. A single CJK character (``图``, ``解``) is a word
    and is translated.
    """
    stripped = text.strip()
    if not stripped:
        return "", [], False, "empty"
    protected, fragments = protect_text(stripped, source_lang)
    letters = [ch for ch in stripped if ch.isalpha()]
    if len(letters) == 1 and len(stripped.replace(" ", "")) <= 2 and _is_latin_or_greek(letters[0]):
        return protected, fragments, False, "single letter"
    if not letters or is_fully_protected(protected):
        return protected, fragments, False, "pure number / formula"
    if letters_of_script(stripped, source_lang) == 0 and script_profile(stripped)["latin"] == 0:
        return protected, fragments, False, "no source-script letters"
    return protected, fragments, True, ""


MAX_TEXT_SLANT_DEGREES = 12.0
"""OCR polygons slanted more than this (and less than 90 - this) are decorative:
watermarks, diagonal captions, text along curves. They are kept as they are."""


def polygon_slant_degrees(polygon: list[list[float]]) -> float:
    """Angle in degrees (0..90) between the polygon's top edge and the horizontal."""
    if len(polygon) < 2:
        return 0.0
    (x0, y0), (x1, y1) = polygon[0][:2], polygon[1][:2]
    dx, dy = float(x1) - float(x0), float(y1) - float(y0)
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return 0.0
    angle = abs(math.degrees(math.atan2(dy, dx)))
    return min(angle, 180.0 - angle)


def build_image_segment(result: OcrResult, *, page_index: int, xref: int, index: int, loaded: LoadedImage,
                        image_bbox: BBox, transform: Any, source_lang: Lang) -> Optional[TextSegment]:
    """Turn one OCR result on image ``xref`` into an ``IMAGE_TEXT`` segment.

    Returns ``None`` when the result's box has no area inside the image.
    """
    box = _clamp_box(result.box, loaded.width, loaded.height)
    if box[2] - box[0] <= 0 or box[3] - box[1] <= 0:
        logger.debug("page %d image %d: dropping %r (box %s outside the %dx%d image)", page_index, xref,
                     result.text, result.box, loaded.width, loaded.height)
        return None
    page_bbox = pixel_polygon_to_page([[box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]],
                                      loaded.width, loaded.height, transform)
    box_h_px = box[3] - box[1]
    size_pt = round(box_h_px * vertical_points_per_pixel(transform, loaded.height) * FONT_HEIGHT_RATIO, 1)
    bg, _uniform = estimate_background(loaded.rgb, box, loaded.alpha)
    color = estimate_text_color(loaded.rgb, box, bg, loaded.alpha)
    protected, fragments, translate, reason = classify_ocr_text(result.text, source_lang)
    slant = polygon_slant_degrees(result.polygon)
    if translate and MAX_TEXT_SLANT_DEGREES < slant < 90.0 - MAX_TEXT_SLANT_DEGREES:
        translate, reason = False, f"slanted text ({slant:.0f}°): watermark or decoration, kept as is"
    return TextSegment(
        id=f"p{page_index}_i{xref}_{index}",
        page=page_index,
        kind=SegmentKind.IMAGE_TEXT,
        bbox=page_bbox,
        source_text=result.text.strip(),
        protected_text=protected,
        protected=fragments,
        style=SegmentStyle(size=max(size_pt, 1.0), color=rgb_to_int(color), role="label", align="left"),
        image=ImageRef(xref=xref, page=page_index, bbox=image_bbox, width=loaded.width, height=loaded.height,
                       pixel_box=box, polygon=[[float(x), float(y)] for x, y in result.polygon],
                       confidence=float(result.confidence)),
        translate=translate,
        skip_reason=reason,
    )


def _open_pdf(source: PdfSource) -> tuple[pymupdf.Document, bool]:
    if isinstance(source, pymupdf.Document):
        return source, False
    return pymupdf.open(str(source)), True


def extract_image_segments(pdf_path: PdfSource, doc: TranslatedDocument, engine: OcrEngine, *,
                           min_confidence: float = 0.6, min_image_px: int = 40,
                           pages: Optional[list[int]] = None) -> list[TextSegment]:
    """Run OCR on the images of ``pdf_path`` and return ``IMAGE_TEXT`` segments.

    Each image XObject is processed once (on the first page that places it) so
    that a shared image gets one translation; tiny images (below
    ``min_image_px`` in either dimension), soft masks and OCR results under
    ``min_confidence`` are ignored. Results that need no translation are still
    returned with ``translate=False`` and a ``skip_reason`` so the pipeline can
    report them. Nothing is appended to ``doc`` - the caller extends
    ``doc.segments``.
    """
    pdf_doc, owned = _open_pdf(pdf_path)
    wanted = set(pages) if pages is not None else None
    seen: set[int] = set()
    smasks: set[int] = set()
    segments: list[TextSegment] = []
    try:
        for page in pdf_doc:
            if wanted is not None and page.number not in wanted:
                continue
            for info in page.get_image_info(xrefs=True):
                xref = int(info.get("xref", 0) or 0)
                if xref <= 0 or xref in seen or xref in smasks:
                    continue
                seen.add(xref)
                w, h = int(info.get("width", 0)), int(info.get("height", 0))
                if w < min_image_px or h < min_image_px:
                    logger.debug("page %d: skipping tiny image xref %d (%dx%d px)", page.number, xref, w, h)
                    continue
                try:
                    loaded = load_image(pdf_doc, xref)
                except Exception as exc:
                    logger.warning("page %d: cannot decode image xref %d: %s", page.number, xref, exc)
                    continue
                if loaded.smask_xref:
                    smasks.add(loaded.smask_xref)
                try:
                    results = engine.recognize(loaded.flattened(), hint_langs=[doc.source_lang])
                except OcrError as exc:
                    logger.warning("page %d: OCR failed on image xref %d: %s", page.number, xref, exc)
                    continue
                image_bbox = BBox.from_rect(info["bbox"])
                transform = info.get("transform") or (image_bbox.width, 0.0, 0.0, image_bbox.height,
                                                       image_bbox.x0, image_bbox.y0)
                kept = translatable = 0
                for n, result in enumerate(results):
                    if result.confidence < min_confidence:
                        logger.debug("page %d image %d: dropping %r (confidence %.2f < %.2f)", page.number, xref,
                                     result.text, result.confidence, min_confidence)
                        continue
                    seg = build_image_segment(result, page_index=page.number, xref=xref, index=n, loaded=loaded,
                                              image_bbox=image_bbox, transform=transform,
                                              source_lang=doc.source_lang)
                    if seg is None:
                        continue
                    segments.append(seg)
                    kept += 1
                    translatable += int(seg.translate)
                logger.info("page %d: image xref %d (%dx%d px): %d text regions, %d translatable", page.number,
                            xref, loaded.width, loaded.height, kept, translatable)
    finally:
        if owned:
            pdf_doc.close()
    for order, seg in enumerate(segments):
        seg.reading_order = order
    return segments


# --------------------------------------------------------------------------- #
# text fitting
# --------------------------------------------------------------------------- #


@dataclass
class TextFit:
    """Result of fitting a translation into a pixel box."""

    font: ImageFont.FreeTypeFont
    size_px: int
    lines: list[str]
    start_px: float
    overflow: bool = False
    ink_height: float = 0.0
    line_widths: list[float] = field(default_factory=list)

    @property
    def scale(self) -> float:
        """Final size relative to the start size (1.0 = no shrink; rounding up never counts as growth)."""
        return min(1.0, self.size_px / self.start_px) if self.start_px > 0 else 1.0


class _FontCache:
    def __init__(self, lang: Lang, bold: bool, fonts_dir: Optional[Union[str, Path]]):
        self.lang, self.bold, self.fonts_dir = lang, bold, fonts_dir
        self._fonts: dict[int, ImageFont.FreeTypeFont] = {}

    def get(self, size_px: float) -> ImageFont.FreeTypeFont:
        key = max(MIN_FONT_PX, int(round(size_px)))
        font = self._fonts.get(key)
        if font is None:
            font = pil_font(self.lang, key, bold=self.bold, extra_dir=self.fonts_dir)
            self._fonts[key] = font
        return font


def _ink(font: ImageFont.FreeTypeFont, text: str) -> tuple[float, float, float, float]:
    """Ink bbox of ``text`` relative to a left/baseline anchor: (left, top, right, bottom)."""
    return tuple(float(v) for v in font.getbbox(text, anchor="ls"))


def split_two_lines(text: str, lang: Lang, font: ImageFont.FreeTypeFont) -> Optional[list[str]]:
    """Split ``text`` into two lines of similar width (word boundary, or any character for CJK).

    Returns ``None`` when no split is balanced enough (``MIN_LINE_BALANCE``):
    "hypotenuse" / "c" is not a useful second line.
    """
    units = list(text) if is_cjk(lang) else text.split(" ")
    if len(units) < 2:
        return None
    joiner = "" if is_cjk(lang) else " "
    best: Optional[tuple[float, list[str]]] = None
    for i in range(1, len(units)):
        first, second = joiner.join(units[:i]).strip(), joiner.join(units[i:]).strip()
        if not first or not second:
            continue
        w1, w2 = font.getlength(first), font.getlength(second)
        if min(w1, w2) < MIN_LINE_BALANCE * max(w1, w2):
            continue
        widest = max(w1, w2)
        if best is None or widest < best[0]:
            best = (widest, [first, second])
    return best[1] if best else None


def fit_text(text: str, lang: Lang, box_w: int, box_h: int, fonts: _FontCache) -> TextFit:
    """Largest font at which ``text`` fits ``box_w`` x ``box_h`` pixels.

    Starts at ``FONT_HEIGHT_RATIO`` x box height, shrinks until the ink fits
    the box height and width; a wide box (aspect > ``TWO_LINE_ASPECT``) may be
    re-flowed into two lines when that allows a larger font. Explicit line
    breaks in ``text`` are honoured as given. Never goes below ``MIN_FONT_PX``;
    ``overflow`` reports when even that does not fit.
    """
    given = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not given:
        raise ValueError("cannot fit empty text")
    n_given = len(given)
    start = max(float(MIN_FONT_PX), box_h * FONT_HEIGHT_RATIO / (1.0 if n_given == 1 else n_given * LINE_PITCH))

    def shrink(lines: list[str], max_h: float, size: float) -> tuple[int, bool, float, list[float]]:
        while True:
            font = fonts.get(size)
            inks = [_ink(font, ln) for ln in lines]
            widths = [right - left for left, _top, right, _bottom in inks]
            height = max(bottom - top for _left, top, _right, bottom in inks)
            fits = max(widths) <= box_w + 0.5 and height <= max_h + 0.5
            if fits or int(round(size)) <= MIN_FONT_PX:
                return max(MIN_FONT_PX, int(round(size))), not fits, height, widths
            size = max(float(MIN_FONT_PX), size - max(1.0, size * 0.08))

    max_h = box_h * 1.05 if n_given == 1 else box_h / n_given
    single_size, single_over, single_h, single_w = shrink(given, max_h, start)
    best = TextFit(font=fonts.get(single_size), size_px=single_size, lines=given, start_px=start,
                   overflow=single_over, ink_height=single_h, line_widths=single_w)
    if n_given == 1 and box_w > TWO_LINE_ASPECT * box_h and (single_over or single_size < 0.75 * start):
        two_start = max(float(MIN_FONT_PX), box_h * FONT_HEIGHT_RATIO / (2 * LINE_PITCH))
        lines = split_two_lines(given[0], lang, fonts.get(two_start))
        if lines:
            size2, over2, h2, w2 = shrink(lines, box_h / 2.0, two_start)
            if (not over2 and (single_over or size2 > single_size)) or (over2 and single_over and size2 > single_size):
                best = TextFit(font=fonts.get(size2), size_px=size2, lines=lines, start_px=start,
                               overflow=over2, ink_height=h2, line_widths=w2)
    return best


# --------------------------------------------------------------------------- #
# drawing
# --------------------------------------------------------------------------- #


def _clear_box(canvas: np.ndarray, alpha: Optional[np.ndarray], original: np.ndarray,
               original_alpha: Optional[np.ndarray], box: tuple[int, int, int, int]) -> tuple[np.ndarray, str]:
    """Erase the original glyphs: flat fill when the ring is uniform, inpainting otherwise."""
    x0, y0, x1, y1 = box
    bg, uniform = estimate_background(original, box, original_alpha)
    if uniform:
        canvas[y0:y1, x0:x1] = bg
        if alpha is not None and original_alpha is not None:
            ring_alpha = ring_pixels(original_alpha[..., None], box)
            alpha[y0:y1, x0:x1] = int(np.median(ring_alpha)) if ring_alpha.size else 255
        return bg, "filled"
    h, w = canvas.shape[:2]
    pad = max(16, 4 * RING_PX)
    cx0, cy0, cx1, cy1 = max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + pad, w), min(y1 + pad, h)
    mask = np.zeros((cy1 - cy0, cx1 - cx0), dtype=np.uint8)
    mx0, my0 = max(x0 - RING_PX, cx0) - cx0, max(y0 - RING_PX, cy0) - cy0
    mx1, my1 = min(x1 + RING_PX, cx1) - cx0, min(y1 + RING_PX, cy1) - cy0
    mask[my0:my1, mx0:mx1] = 255
    crop = np.ascontiguousarray(canvas[cy0:cy1, cx0:cx1])
    canvas[cy0:cy1, cx0:cx1] = cv2.inpaint(crop, mask, INPAINT_RADIUS, cv2.INPAINT_TELEA)
    if alpha is not None:
        acrop = np.ascontiguousarray(alpha[cy0:cy1, cx0:cx1])
        alpha[cy0:cy1, cx0:cx1] = cv2.inpaint(acrop, mask, INPAINT_RADIUS, cv2.INPAINT_TELEA)
    return bg, "inpainted"


PixelBox = tuple[int, int, int, int]


def free_extension(original: LoadedImage, box: PixelBox, bg: np.ndarray, blocked: list[PixelBox],
                   max_each: int) -> tuple[int, int]:
    """Free background columns to the left and right of ``box`` (over the box's rows).

    A column is free when every pixel in it is opaque and matches the
    background colour within ``FREE_TOL`` and it lies in none of the
    ``blocked`` boxes. Transparent pixels are never free: whatever the page
    shows through them is unknown here. The scan stops at the first obstacle,
    the image border or ``max_each`` and keeps ``FREE_MARGIN`` columns clear
    of the obstacle.
    """
    h, w = original.rgb.shape[:2]
    x0, y0, x1, y1 = box
    if max_each <= 0 or y1 <= y0:
        return 0, 0
    lo, hi = max(0, x0 - max_each), min(w, x1 + max_each)
    strip = original.rgb[y0:y1, lo:hi].astype(np.int16)
    free = np.abs(strip - bg.astype(np.int16)).max(axis=2) <= FREE_TOL
    if original.alpha is not None:
        free &= original.alpha[y0:y1, lo:hi] >= 255 - FREE_TOL
    col_free = free.all(axis=0)
    for bx0, by0, bx1, by1 in blocked:
        if by1 > y0 and by0 < y1:
            cs, ce = max(bx0 - lo, 0), min(bx1 - lo, hi - lo)
            if ce > cs:
                col_free[cs:ce] = False
    left = 0
    for c in range(x0 - lo - 1, -1, -1):
        if not col_free[c]:
            break
        left += 1
    right = 0
    for c in range(x1 - lo, hi - lo):
        if not col_free[c]:
            break
        right += 1
    return max(0, left - FREE_MARGIN), max(0, right - FREE_MARGIN)


def _left_aligned_neighbour(seg: TextSegment, siblings: list[TextSegment]) -> bool:
    """True when another box in the same image shares this box's left edge (a text column)."""
    if seg.image is None:
        return False
    x0 = seg.image.pixel_box[0]
    tol = max(3, int(0.15 * (seg.image.pixel_box[3] - seg.image.pixel_box[1])))
    return any(o is not seg and o.image is not None and abs(o.image.pixel_box[0] - x0) <= tol for o in siblings)


def _scaled_box(box: PixelBox, ref: ImageRef, width: int, height: int) -> PixelBox:
    """``box`` (recorded for ``ref``'s pixel size) in the pixel space of a ``width`` x ``height`` image."""
    box = _clamp_box(box, ref.width, ref.height)
    if ref.width == width and ref.height == height:
        return box
    fx, fy = width / max(ref.width, 1), height / max(ref.height, 1)
    return _clamp_box((round(box[0] * fx), round(box[1] * fy), round(box[2] * fx), round(box[3] * fy)), width, height)


def draw_translation(canvas: np.ndarray, alpha: Optional[np.ndarray], original: LoadedImage, seg: TextSegment,
                     text: str, target_lang: Lang, fonts: _FontCache, siblings: list[TextSegment],
                     transform: Any = None, occupied: Optional[list[PixelBox]] = None) -> RenderInfo:
    """Paint ``text`` over the original glyphs of ``seg`` on ``canvas``/``alpha`` and return what was done.

    ``original`` holds the untouched pixels used to estimate background and
    text colours (earlier segments may already have been drawn on ``canvas``).
    ``siblings`` are all text boxes of the same image (translated or not) and
    ``occupied`` the pixel boxes already redrawn on this canvas; both are kept
    clear when the text grows into free background, and the box drawn here is
    appended to ``occupied``. ``transform`` is the current placement matrix of
    the image (used to report the page-space rectangle of the drawn text
    exactly); without it the rectangle is derived from ``seg.image.bbox``.
    """
    ref = seg.image
    if ref is None:
        raise ValueError(f"segment {seg.id} has no image reference")
    if not text.strip():
        raise ValueError(f"segment {seg.id} has an empty translation")
    h, w = canvas.shape[:2]
    box = _scaled_box(ref.pixel_box, ref, w, h)  # pixel size may differ from extraction time
    x0, y0, x1, y1 = box
    box_w, box_h = x1 - x0, y1 - y0
    if box_w <= 0 or box_h <= 0:
        return RenderInfo(font_size=0.0, scale=0.0, overflow=True, bbox=seg.bbox, notes="empty pixel box")
    color = estimate_text_color(original.rgb, box, None, original.alpha)
    bg, how = _clear_box(canvas, alpha, original.rgb, original.alpha, box)
    centred = not _left_aligned_neighbour(seg, siblings)
    # A longer translation may spread into free background next to the label (never over other
    # labels, already redrawn text or graphics); a text column only grows to the right.
    blocked = [_scaled_box(o.image.pixel_box, o.image, w, h) for o in siblings if o is not seg and o.image is not None]
    blocked += list(occupied or [])
    left, right = free_extension(original, box, bg, blocked, int(MAX_GROWTH * box_w))
    if not centred:
        left = 0
    avail_x0, avail_x1 = x0 - left, x1 + right
    fit = fit_text(text, target_lang, avail_x1 - avail_x0, box_h, fonts)

    pil = Image.fromarray(canvas, "RGB")
    draw = ImageDraw.Draw(pil)
    alpha_pil = Image.fromarray(alpha, "L") if alpha is not None else None
    alpha_draw = ImageDraw.Draw(alpha_pil) if alpha_pil is not None else None
    pitch = fit.size_px * LINE_PITCH
    inks = [_ink(fit.font, ln) for ln in fit.lines]
    baseline = y1 - max(0.0, inks[-1][3])  # last line sits on the original box bottom
    drawn_x0, drawn_x1, drawn_y0 = float(x1), float(x0), float(y1)
    for i, (line, ink) in enumerate(zip(fit.lines, inks)):
        by = baseline - (len(fit.lines) - 1 - i) * pitch
        width = ink[2] - ink[0]
        if centred:
            ink_x = (x0 + x1) / 2.0 - width / 2.0  # centred on the original label ...
            ink_x = max(float(avail_x0), min(ink_x, avail_x1 - width))  # ... but inside the free span
        else:
            ink_x = float(x0)
        bx = ink_x - ink[0]
        draw.text((bx, by), line, fill=color, font=fit.font, anchor="ls")
        if alpha_draw is not None:
            alpha_draw.text((bx, by), line, fill=255, font=fit.font, anchor="ls")
        drawn_x0, drawn_x1 = min(drawn_x0, bx + ink[0]), max(drawn_x1, bx + ink[2])
        drawn_y0 = min(drawn_y0, by + ink[1])
    canvas[:] = np.array(pil)
    if alpha is not None and alpha_pil is not None:
        alpha[:] = np.array(alpha_pil)

    if transform is not None:
        pts_per_px = vertical_points_per_pixel(transform, h)
    else:
        pts_per_px = ref.bbox.height / max(ref.height, 1)
    drawn = _clamp_box((int(drawn_x0), int(drawn_y0), int(np.ceil(drawn_x1)), int(np.ceil(y1))), w, h)
    if occupied is not None:
        occupied.append(drawn)
    if (w, h) != (ref.width, ref.height):  # report in the pixel space ``ref`` was built in
        fx, fy = ref.width / w, ref.height / h
        drawn = (int(drawn[0] * fx), int(drawn[1] * fy), int(np.ceil(drawn[2] * fx)), int(np.ceil(drawn[3] * fy)))
    font_name = Path(getattr(fit.font, "path", "") or "").name or "PIL default"
    used_l, used_r = max(0, x0 - drawn_x0), max(0, drawn_x1 - x1)
    grown = f", grown {used_l:.0f}px left / {used_r:.0f}px right" if used_l >= 1 or used_r >= 1 else ""
    notes = (f"{how}; {len(fit.lines)} line(s) at {fit.size_px}px, "
             f"{'centred' if centred else 'left-aligned'}{grown}, colour #{rgb_to_int(color):06x}, font {font_name}")
    return RenderInfo(
        font_size=round(fit.size_px * pts_per_px, 2),
        scale=round(fit.scale, 3),
        spare_height=round((box_h - fit.ink_height * len(fit.lines)) * pts_per_px, 2),
        overflow=fit.overflow,
        bbox=pixel_box_to_page(drawn, ref, transform),
        notes=notes,
    )


@dataclass
class _Placement:
    """Where an :class:`ImageRef` currently lives in a document."""

    xref: int
    transform: Optional[tuple[float, ...]]  # None when the image is not drawn on its page any more


def _same_rect(a: BBox, b: Any, tol: float = PLACEMENT_TOL) -> bool:
    bb = BBox.from_rect(b)
    return all(abs(x - y) <= tol for x, y in zip(a.as_tuple(), bb.as_tuple()))


def _xref_image_size(pdf_doc: pymupdf.Document, xref: int) -> Optional[tuple[int, int]]:
    """``(width, height)`` of image ``xref``, or ``None`` when it is not an image."""
    try:
        if xref <= 0 or not pdf_doc.xref_is_image(xref):
            return None
        return int(pdf_doc.xref_get_key(xref, "Width")[1]), int(pdf_doc.xref_get_key(xref, "Height")[1])
    except (ValueError, RuntimeError, TypeError):
        return None


def resolve_placement(pdf_doc: pymupdf.Document, page: pymupdf.Page, ref: ImageRef) -> Optional[_Placement]:
    """Find the image ``ref`` describes in ``pdf_doc`` (xref + current placement matrix).

    The xref recorded at extraction time is only trusted when it still is an
    image with the recorded pixel size: a save with ``garbage >= 2`` (as the
    layout stage does) renumbers objects, so the placement rectangle and pixel
    size on the recorded page are the reliable identity. Returns ``None`` when
    nothing matches.
    """
    infos = [i for i in page.get_image_info(xrefs=True) if int(i.get("xref", 0) or 0) > 0]

    def placement(info: dict[str, Any]) -> _Placement:
        return _Placement(xref=int(info["xref"]), transform=tuple(info["transform"]) if info.get("transform") else None)

    for info in infos:  # exact: same xref drawn at the same place
        if int(info["xref"]) == ref.xref and _same_rect(ref.bbox, info["bbox"]):
            return placement(info)
    for tol in (PLACEMENT_TOL, 3 * PLACEMENT_TOL):  # renumbered: same rectangle and pixel size
        for info in infos:
            if _same_rect(ref.bbox, info["bbox"], tol) and \
                    (int(info.get("width", 0)), int(info.get("height", 0))) == (ref.width, ref.height):
                if int(info["xref"]) != ref.xref:
                    logger.info("page %d: image xref %d was renumbered to %d", page.number, ref.xref, info["xref"])
                return placement(info)
    if _xref_image_size(pdf_doc, ref.xref) == (ref.width, ref.height) and not infos:
        # the page draws no image any more (e.g. a stripped preview copy) but the object itself is intact
        logger.warning("page %d: image xref %d is no longer drawn there; replacing the object anyway", page.number,
                       ref.xref)
        return _Placement(xref=ref.xref, transform=None)
    return None


def render_image_segments(pdf_doc: pymupdf.Document, doc: TranslatedDocument, *,
                          fonts_dir: Optional[Union[str, Path]] = None) -> int:
    """Paint translated ``IMAGE_TEXT`` segments into their images and replace them in ``pdf_doc``.

    Segments are grouped by image xref; each image is decoded once, every
    translation is drawn (original glyphs erased first), and the image stream
    is replaced on the page that references it - ``page.replace_image`` swaps
    the stream behind the xref, so all placements are updated while the
    placement rectangles and pixel dimensions stay unchanged. The image is
    located by its placement rectangle and pixel size, so segments extracted
    from the source PDF still apply after the document was re-saved with
    renumbered xrefs. Translations identical to the source text leave the
    pixels untouched. ``seg.render`` is filled with the font size (page
    points), scale factor and the page-space rectangle of the drawn text.
    Returns the number of images modified.
    """
    groups: dict[int, list[TextSegment]] = {}
    siblings: dict[int, list[TextSegment]] = {}
    for seg in doc.segments:
        if seg.kind != SegmentKind.IMAGE_TEXT or seg.image is None:
            continue
        siblings.setdefault(seg.image.xref, []).append(seg)
        if not seg.translate or seg.translated_text is None or not seg.translated_text.strip():
            continue
        if seg.translated_text.strip() == seg.source_text.strip():
            seg.render = RenderInfo(font_size=seg.style.size, scale=1.0, bbox=seg.bbox,
                                    notes="unchanged: translation equals the source text")
            continue
        groups.setdefault(seg.image.xref, []).append(seg)
    modified = 0
    for xref, segs in groups.items():
        ref = segs[0].image
        assert ref is not None  # guaranteed by the grouping above
        page_index = ref.page
        if page_index < 0 or page_index >= pdf_doc.page_count:
            logger.warning("image xref %d refers to page %d which does not exist; skipped", xref, page_index)
            _mark_failed(segs, f"page {page_index} does not exist")
            continue
        page = pdf_doc[page_index]
        placement = resolve_placement(pdf_doc, page, ref)
        if placement is None:
            logger.error("page %d: cannot find image xref %d (%dx%d px at %s) in the document; skipped",
                         page_index, xref, ref.width, ref.height, ref.bbox.as_tuple())
            _mark_failed(segs, "image not found in the document")
            continue
        try:
            loaded = load_image(pdf_doc, placement.xref)
        except Exception as exc:
            logger.warning("page %d: cannot decode image xref %d for rendering: %s", page_index, placement.xref, exc)
            _mark_failed(segs, f"image decoding failed: {exc}")
            continue
        canvas = loaded.rgb.copy()
        alpha = loaded.alpha.copy() if loaded.alpha is not None else None
        bold = any(s.style.bold for s in segs)
        fonts = _FontCache(doc.target_lang, bold, fonts_dir)
        drawn = 0
        occupied: list[PixelBox] = []
        for seg in segs:
            text = seg.translated_text.strip()  # type: ignore[union-attr]
            try:
                seg.render = draw_translation(canvas, alpha, loaded, seg, text, doc.target_lang, fonts,
                                              siblings.get(xref, segs), placement.transform, occupied)
                drawn += 1
            except Exception as exc:
                logger.exception("page %d: drawing segment %s failed: %s", page_index, seg.id, exc)
                seg.render = RenderInfo(font_size=0.0, scale=0.0, overflow=True, bbox=seg.bbox,
                                        notes=f"drawing failed: {exc}")
        if drawn == 0:
            continue
        stream = encode_image(canvas, alpha, loaded.ext)
        try:
            page.replace_image(placement.xref, stream=stream)
        except Exception as exc:
            logger.error("page %d: replace_image(xref=%d) failed: %s", page_index, placement.xref, exc)
            _mark_failed(segs, f"image replacement failed: {exc}")
            continue
        modified += 1
        logger.info("page %d: replaced image xref %d (%dx%d px) with %d translated region(s)", page_index,
                    placement.xref, loaded.width, loaded.height, drawn)
    return modified


def _mark_failed(segs: list[TextSegment], reason: str) -> None:
    """Record a failed replacement on every segment so QA can report it."""
    for seg in segs:
        seg.render = RenderInfo(font_size=0.0, scale=0.0, overflow=True, bbox=seg.bbox, notes=f"not rendered: {reason}")
