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
from typing import Any, Callable, Optional, Sequence, Union

import cv2
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont

from .fonts import pil_font
from .interfaces import OcrEngine
from .languages import is_cjk, letters_of_script, script_profile
from .models import (ANCHOR_RE, anchor_marker, make_placeholder, BBox, ImageRef, Lang, OcrResult, RenderInfo, SegmentKind, SegmentStyle, TextSegment,
                     TranslatedDocument)
from .ocr import OcrError, OcrUnavailableError
from .protect import is_fully_protected, protect_text

logger = logging.getLogger("mathtrans.images")

#: Images with more pixels than this are not decoded or OCR'd (a 600 dpi A4 scan is ~35 MP; a
#: 12000x12000 flate "decompression bomb" is 144 MP and ~2 GB of RSS at full resolution).
MAX_IMAGE_PX = 50_000_000
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
    jpeg_qtables: Optional[dict] = None  # quantisation tables of a JPEG source (reused on re-encoding)
    jpeg_subsampling: int = -1  # chroma subsampling of a JPEG source (-1 = unknown)

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
    qtables: Optional[dict] = None
    subsampling = -1
    try:
        pil = Image.open(io.BytesIO(info["image"]))
        pil.load()
        if ext in ("jpeg", "jpg") and getattr(pil, "quantization", None):
            # Remember how the source was compressed so the replaced image stays the same size.
            qtables = {int(k): list(v) for k, v in pil.quantization.items()}
            try:
                from PIL import JpegImagePlugin

                subsampling = int(JpegImagePlugin.get_sampling(pil))
            except Exception:  # pragma: no cover - defensive
                subsampling = -1
        if pil.mode == "CMYK" or int(info.get("colorspace", 3)) == 4 or pil.mode not in _PIL_SAFE_MODES:
            rgb = _pixmap_rgb(pdf_doc, xref)
            qtables, subsampling = None, -1  # tables of a CMYK source do not transfer to RGB
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
    return LoadedImage(xref=xref, rgb=np.ascontiguousarray(rgb), alpha=alpha, ext=ext, smask_xref=smask,
                       jpeg_qtables=qtables, jpeg_subsampling=subsampling)


def encode_image(rgb: np.ndarray, alpha: Optional[np.ndarray], ext: str, *,
                 qtables: Optional[dict] = None, subsampling: int = -1) -> bytes:
    """PNG bytes (RGBA when ``alpha`` is given); JPEG sources without alpha stay JPEG,
    re-encoded with the source's own quantisation tables and chroma subsampling when
    known (so a scanned page keeps its size and quality), else at quality 90."""
    buf = io.BytesIO()
    if alpha is not None:
        rgba = np.dstack([rgb, alpha])
        Image.fromarray(rgba, "RGBA").save(buf, format="PNG")
    elif ext in ("jpeg", "jpg"):
        img = Image.fromarray(rgb, "RGB")
        if qtables:
            try:
                kwargs = {"qtables": qtables}
                if subsampling in (0, 1, 2):
                    kwargs["subsampling"] = subsampling
                img.save(buf, format="JPEG", optimize=True, **kwargs)
                return buf.getvalue()
            except Exception as exc:  # odd tables (e.g. 16-bit) - fall back to a fixed quality
                logger.debug("cannot reuse JPEG quantisation tables (%s); using quality 90", exc)
                buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90, optimize=True)
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


_CJK_PLUS_RE = re.compile(r"[\d\s.=×÷+\-()（）]*\d\s*[十一]\s*\d[\d\s.=×÷+\-()（）]*")
MEASURE_WORDS = "个只支本朵根米张把块颗条棵头辆元件匹双座间辆杯盒瓶袋箱筐束串片粒枝面层台架艘"
"""Chinese measure words (classifiers) that appear as unit labels after an answer box: □（只）."""
_UNIT_LABEL_RE = re.compile(rf"[（(]\s*[{MEASURE_WORDS}?]\s*[)）]")
_COUNT_LABEL_RE = re.compile(rf"\d+\s*[{MEASURE_WORDS}]")
"""``6个``, ``96个``, ``85本``: a count label, reliable even when read with low confidence."""
_TRAILING_UNIT_RE = re.compile(rf"\s*[（(]\s*[{MEASURE_WORDS}]?\s*[)）]?\s*$")
_BOX_GLYPHS = set("□○OoD0Q口〇◯●◇△▲☐")
_TEMPLATE_DROP = set(" +-−—–×÷=()（）[]［］_")
_EMPTY_QUOTES_RE = re.compile(r"[“‘「]\s*[”’」\"']|(?<=画)[\"']\s*[\"”’']")
_PICTOGRAM_GAP_RE = re.compile(
    r"用\s*表示|^表示(?=[，,。；;、）)]|$)|^比(?![一赛较例如方\d０-９])|(?<![一相])比(?=[，,。？?！!]|$)"
    r"|有个有个|在的面|的面(?=[，,。]|$)")
"""Missing-operand patterns left when OCR drops inline pictograms: 用○表示人 -> 用表示人,
△比●少□个 -> 比少个, 🍄比🍄多几个 -> 比多几个."""
_GAP_BEFORE_RE = re.compile(r"^(?:比(?![一赛较例如方\d０-９])|表示)")
"""The line starts with 比 / 表示: the picture it compares or stands for sits left of the OCR box."""
_GAP_AFTER_RE = re.compile(r"(?<![一相])(?:比|用|表示)[，,。？?！!]?$")
"""The line ends with 比 / 用 / 表示: the picture sits right of the OCR box."""


def has_pictogram_gap(text: str) -> bool:
    """True when ``text`` reads like a sentence whose inline pictures the OCR dropped
    (:data:`_PICTOGRAM_GAP_RE`); pictures already anchored in it count as present."""
    return bool(_PICTOGRAM_GAP_RE.search(ANCHOR_RE.sub("图", text).replace(" ", "")))


_DIGIT_CONFUSION_1_RE = re.compile(r"(?<![A-Za-z0-9])[hI|](?=\d+(?![A-Za-z0-9]))")
_DIGIT_CONFUSION_0_RE = re.compile(r"(?<=\d)[Oo](?![A-Za-z])")


def is_fill_in_template(text: str) -> bool:
    """``□-□=□``, ``□○□=□（只）`` (OCR: ``O-O=O (只)``, ``□OO=0``): answer boxes, not text."""
    core = _TRAILING_UNIT_RE.sub("", text.strip())
    kept = [c for c in core if c not in _TEMPLATE_DROP]
    if len(kept) < 2:
        return False
    boxes = sum(c in _BOX_GLYPHS for c in kept)
    others = len(kept) - boxes
    digits_other = sum(c.isdigit() and c not in _BOX_GLYPHS for c in kept)
    if others > 1 or (others == 1 and digits_other != 1):
        return False
    has_shape = any(c in "□○口〇◯●◇△▲☐" for c in kept)
    operator = any(op in core for op in "+-−×÷")  # "□○□=□" read as "0OO-O": = taken for -
    return boxes >= 2 and ("=" in core or has_shape or (boxes >= 3 and operator))


def normalize_ocr_digits(text: str) -> str:
    """Fix digit look-alikes that start or end a number token (``h5`` -> ``15``,
    ``5O`` -> ``50``); a letter inside a word or a variable name (``l1``) is left alone."""
    t = _DIGIT_CONFUSION_1_RE.sub("1", text)
    return _DIGIT_CONFUSION_0_RE.sub("0", t)


_PLACE_VALUE_RE = re.compile(r"^([十个百千万]位)\s*(\d{1,3})$|^(\d{1,3})\s*([十个百千万]位)$")
"""``十位5`` / ``7个位``: a place-value header fused with a digit of the vertical form next to it."""


def split_place_value(text: str, box: tuple[int, int, int, int]) -> Optional[tuple[str, tuple[int, int, int, int]]]:
    """``(label, label_box)`` for a place-value header fused with a digit, so only the label
    is translated and erased while the digit stays in the picture; None otherwise."""
    m = _PLACE_VALUE_RE.match(text.strip())
    if not m:
        return None
    x0, y0, x1, y1 = box
    if m.group(1):
        label, digits, label_first = m.group(1), m.group(2), True
    else:
        label, digits, label_first = m.group(4), m.group(3), False
    if y1 - y0 >= 1.8 * (x1 - x0):
        # stacked down a column (十 / 位 / 3): every glyph is about one em tall
        share = len(label) / (len(label) + len(digits))
        cut = y0 + share * (y1 - y0)
        margin = 0.08 * (x1 - x0)
        if label_first:
            return label, (x0, y0, x1, max(y0 + 1, int(cut - margin)))
        return label, (x0, min(y1 - 1, int(y0 + (1 - share) * (y1 - y0) + margin)), x1, y1)
    # a CJK glyph is about one em wide, a digit about 0.55 em; keep a margin towards the digit
    share = len(label) / (len(label) + 0.55 * len(digits))
    cut = x0 + share * (x1 - x0)
    margin = 0.08 * (y1 - y0)
    if label_first:
        new = (x0, y0, max(x0 + 1, int(cut - margin)), y1)
    else:
        new = (min(x1 - 1, int(x0 + (1 - share) * (x1 - x0) + margin)), y0, x1, y1)
    return label, new


def _classify_mark(mask: np.ndarray) -> Optional[str]:
    """``✓`` / ``○`` / ``△`` / ``□`` for the ink of one mark, None when unsure."""
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if not contours or hierarchy is None:
        return None
    outer = max(contours, key=cv2.contourArea)
    if cv2.contourArea(outer) <= 0:
        return None
    _x, _y, bw, bh = cv2.boundingRect(outer)
    holes = [c for c, info in zip(contours, hierarchy[0]) if info[3] >= 0 and cv2.contourArea(c) > 0.15 * bw * bh]
    if holes:
        corners = len(cv2.approxPolyDP(outer, 0.04 * cv2.arcLength(outer, True), True))
        return {3: "△", 4: "□"}.get(corners, "○")
    ys, xs = np.nonzero(mask)
    if xs.size == 0:
        return None
    width = xs.max() - xs.min() + 1
    bottom = ys.max()
    bottom_x = float(np.median(xs[ys >= bottom - 1]) - xs.min()) / max(width, 1)
    # a tick has its lowest point left of centre and a long arm up to the right; < and > do not
    return "✓" if 0.15 <= bottom_x <= 0.6 else None


def detect_quoted_marks(rgb: np.ndarray, box: tuple[int, int, int, int]) -> list[Optional[str]]:
    """The marks drawn between the quote pairs of an OCR line, left to right (画“✓”,
    画“○”), whether or not the OCR read them; None for a pair whose mark is unclear."""
    x0, y0, x1, y1 = box
    crop = rgb[y0:y1, x0:x1]
    h = y1 - y0
    if crop.size == 0 or h < 10:
        return []
    flat = crop.reshape(-1, 3).astype(np.int32)
    q = flat // 16
    keys = (q[:, 0] << 8 | q[:, 1]) << 8 | q[:, 2]
    vals, counts = np.unique(keys, return_counts=True)
    bg = np.median(flat[keys == vals[counts.argmax()]], axis=0)
    ink = (np.abs(crop.astype(np.int32) - bg).max(axis=2) > 50).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    quotes, others = [], []
    for i in range(1, n):
        bx, by, bw, bh, area = (int(v) for v in stats[i])
        if area < 3:
            continue
        if bh <= 0.4 * h and bw <= 0.22 * h and by + bh / 2 <= 0.5 * h:
            quotes.append((bx, bx + bw))
        elif bh >= 0.35 * h:
            others.append((i, bx, bx + bw))
    quotes.sort()
    groups: list[list[int]] = []  # [x0, x1, blob count]
    for a, b in quotes:
        if groups and a - groups[-1][1] <= 0.2 * h:
            groups[-1][1] = max(groups[-1][1], b)
            groups[-1][2] += 1
        else:
            groups.append([a, b, 1])
    # a quote mark is two small strokes side by side (“ ” or straight ""): the top of a ？ or a
    # lone dot is not
    clusters = [g[:2] for g in groups if g[2] == 2 and g[1] - g[0] <= 0.5 * h]
    marks: list[Optional[str]] = []
    k = 0
    while k + 1 < len(clusters):
        left, right = clusters[k], clusters[k + 1]
        gap = right[0] - left[1]
        inside = [o for o in others if o[1] >= left[1] - 2 and o[2] <= right[0] + 2]
        if 0.3 * h <= gap <= 2.5 * h and inside:
            marks.append(_classify_mark(np.isin(labels, [o[0] for o in inside]).astype(np.uint8)))
            k += 2  # a pair: opening and closing quote
        else:
            k += 1
    return marks


def detect_quoted_mark(rgb: np.ndarray, box: tuple[int, int, int, int]) -> Optional[str]:
    """The mark of the first quote pair (see :func:`detect_quoted_marks`)."""
    marks = detect_quoted_marks(rgb, box)
    return marks[0] if marks else None


_QUOTE_PAIR_RE = re.compile(r"[“‘「\"'][^“”‘’「」\"']{0,3}[”’」\"']")


def fill_empty_quotes(text: str, marks: list[Optional[str]]) -> str:
    """Fill the empty quote pairs of ``text`` with the detected ``marks`` (one per quote pair,
    filled or not, in order); unchanged when the counts do not match."""
    pairs = list(_QUOTE_PAIR_RE.finditer(text))
    if len(pairs) != len(marks):
        return text
    out, pos = [], 0
    for m, mark in zip(pairs, marks):
        inner = m.group(0)[1:-1]
        out.append(text[pos:m.start()])
        if not inner.strip() and mark:
            out.append(m.group(0)[0] + mark + m.group(0)[-1])
        else:
            out.append(m.group(0))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


ANCHOR_MIN_HEIGHT = 0.45
"""An inline picture or answer box is at least this share of the line height tall ..."""
ANCHOR_MIN_WIDTH = 0.3
"""... and at least this share of it wide (underlines and dots are not pictures)."""
ANCHOR_COLOUR_DISTANCE = 110.0
"""... and its colour differs from the text colour by at least this RGB distance."""
MAX_ANCHORS = 6
ANCHOR_MIN_SATURATION = 60
"""Textbook pictures and answer boxes are coloured; grey strokes are the watermark."""
ANCHOR_MIN_CONTRAST = 90
"""Picture pixels differ from the background by more than this (the semi-transparent
watermark printed over the text does not)."""
TextCheck = Callable[[np.ndarray], bool]
"""``text_check(crop)`` -> True when the OCR recogniser reads the crop as text."""


def _char_width(ch: str) -> float:
    if is_cjk_char(ch) or ch in "，。！？；：、（）“”‘’《》【】":
        return 1.0
    if ch.isspace():
        return 0.3
    if ch.isalnum():
        return 0.55
    return 0.45


def _dominant(pixels: np.ndarray) -> tuple[np.ndarray, float]:
    flat = pixels.reshape(-1, 3).astype(np.int32)
    q = flat // 16
    keys = (q[:, 0] << 8 | q[:, 1]) << 8 | q[:, 2]
    vals, counts = np.unique(keys, return_counts=True)
    colour = np.median(flat[keys == vals[counts.argmax()]], axis=0)
    near = np.abs(flat - colour).max(axis=1) <= 30
    return colour, float(near.mean())


_HEADING_ONLY_RE = re.compile(r"([\u4e00-\u9fff])一\1[。.！!]?")
"""A short heading line (练一练, 试一试, 我学到了什么) - no inline pictures expected."""


def _formula_core(text: str) -> bool:
    """A worked equation: mostly digits and operators around an equals sign."""
    t = text.strip()
    return "=" in t and sum(c.isdigit() or c in "+-−×÷=()（） ." for c in t) >= 0.6 * len(t)


def detect_anchors(rgb: np.ndarray, box: tuple[int, int, int, int], text: str, key_prefix: str,
                   text_check: Optional[TextCheck]) -> tuple[str, dict[str, list[int]]]:
    """Find pictures and answer boxes inside an OCR text line (第□节, 第几只是🦆？, 用○表示人)
    and put an anchor marker into ``text`` at each one's position, so the translation keeps
    it and the layout draws it inline. Returns ``(text, {key: [x0, y0, x1, y1]})``.

    Candidates are ink components clearly unlike the text colour and at least half a line
    tall; neighbouring components merge into one picture. A candidate the OCR recogniser
    reads as text (a red word, a coloured label cell) is not a picture. The characters of
    ``text`` are distributed over the text columns left and right of the pictures by their
    estimated widths."""
    if text_check is None or not any(is_cjk_char(c) for c in text):
        return text, {}
    if is_fill_in_template(text) or _CJK_PLUS_RE.fullmatch(text.strip()) or _formula_core(text):
        return text, {}  # answer-box templates and formulas stay in the picture as they are
    if _HEADING_ONLY_RE.fullmatch(text.strip()):
        return text, {}  # exercise headings (练一练) sit on decorative brush strokes
    x0, y0, x1, y1 = box
    crop = rgb[y0:y1, x0:x1]
    h, w = crop.shape[:2]
    if h < 12 or w < 2 * h:
        return text, {}
    bg, share = _dominant(crop)
    if share < 0.4:
        return text, {}  # busy background: the components are not reliable
    if float(bg.max() - bg.min()) >= ANCHOR_MIN_SATURATION or float(bg.max()) < 150:
        return text, {}  # text on a coloured badge or a dark panel: its shapes are decoration
    ink = np.abs(crop.astype(np.int32) - bg).max(axis=2) > 50
    text_colour = np.array(estimate_text_color(rgb, box, bg.astype(np.uint8)), dtype=np.int32)
    dist = np.sqrt(((crop.astype(np.int32) - text_colour) ** 2).sum(axis=2))
    strong = np.abs(crop.astype(np.int32) - bg).max(axis=2) > ANCHOR_MIN_CONTRAST  # not the faint watermark
    unlike = ink & strong & (dist >= ANCHOR_COLOUR_DISTANCE)
    if not unlike.any():
        return text, {}
    # the colour right around the glyphs: a panel or badge behind the text has it, a picture not
    near_text = cv2.dilate((ink & (dist < ANCHOR_COLOUR_DISTANCE)).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    surround_px = crop[near_text & ~(dist < ANCHOR_COLOUR_DISTANCE)]
    surround = np.median(surround_px.reshape(-1, 3), axis=0) if surround_px.size else bg
    k = max(2, h // 6)
    grown = cv2.dilate(unlike.astype(np.uint8), np.ones((k, k), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(grown, connectivity=8)
    groups: list[tuple[int, int, int, int]] = []
    for i in range(1, n):
        gx, gy, gw, gh, _area = (int(v) for v in stats[i])
        if gh < ANCHOR_MIN_HEIGHT * h or gw < ANCHOR_MIN_WIDTH * h:
            continue
        gx0, gy0 = max(0, gx - 2), max(0, gy - 2)
        gx1, gy1 = min(w, gx + gw + 2), min(h, gy + gh + 2)
        if gx1 - gx0 >= 0.8 * w:
            continue  # a panel or banner behind the whole line
        px = crop[gy0:gy1, gx0:gx1][unlike[gy0:gy1, gx0:gx1]].astype(np.int32)
        if px.size == 0 or float(np.median(px.max(axis=1) - px.min(axis=1))) < ANCHOR_MIN_SATURATION:
            continue  # grey: the watermark or a shadow, not a coloured picture or answer box
        if np.abs(np.median(px, axis=0) - surround).max() <= 60:
            continue  # the panel behind the text (a heading badge), not a picture
        if text_check(np.ascontiguousarray(crop[gy0:gy1, gx0:gx1])):
            continue  # coloured text, not a picture
        groups.append((gx0, gy0, gx1, gy1))
    if not groups or len(groups) > MAX_ANCHORS:
        return text, {}
    groups.sort()
    text_ink = ink & (dist < ANCHOR_COLOUR_DISTANCE)
    for gx0, _gy0, gx1, _gy1 in groups:
        text_ink[:, gx0:gx1] = False
    cols = text_ink.any(axis=0)
    runs: list[list[int]] = []
    for xi in np.flatnonzero(cols):
        if runs and xi - runs[-1][1] <= max(2, h // 4):
            runs[-1][1] = int(xi) + 1
        else:
            runs.append([int(xi), int(xi) + 1])
    runs = [r for r in runs if r[1] - r[0] >= 0.15 * h]
    if not runs:
        return text, {}
    # distribute the characters over the text runs by their estimated widths
    widths = [_char_width(c) for c in text]
    total = sum(widths) or 1.0
    run_total = float(sum(b - a for a, b in runs))
    bounds, acc = [], 0.0
    for a, b in runs:
        acc += (b - a) / run_total
        bounds.append(acc)
    assigned: list[list[str]] = [[] for _ in runs]
    pos = 0.0
    for ch, cw in zip(text, widths):
        mid = (pos + cw / 2) / total
        pos += cw
        idx = next((j for j, bound in enumerate(bounds) if mid <= bound + 1e-9), len(runs) - 1)
        assigned[idx].append(ch)
    items: list[tuple[int, str, int]] = [(a, "run", j) for j, (a, _b) in enumerate(runs)]
    items += [(g[0], "pic", j) for j, g in enumerate(groups)]
    items.sort()
    out, anchors = [], {}
    for _x, kind, j in items:
        if kind == "run":
            out.append("".join(assigned[j]))
        else:
            key = f"{key_prefix}.{j}"
            gx0, gy0, gx1, gy1 = groups[j]
            anchors[key] = [x0 + gx0, y0 + gy0, x0 + gx1, y0 + gy1]
            out.append(anchor_marker(key))
    return "".join(out), anchors


def find_adjacent_picture(rgb: np.ndarray, box: tuple[int, int, int, int], side: str,
                          text_check: Optional[TextCheck]) -> Optional[tuple[int, int, int, int]]:
    """The coloured picture right next to an OCR line, on ``side`` ("left" / "right"):
    🍎比🍐多几个 is read as 比多几个 with the box starting at 比. Returns its pixel box, or
    None when there is no single clear picture within two line heights (text, a busy
    background or nothing at all)."""
    if text_check is None:
        return None
    x0, y0, x1, y1 = (int(v) for v in box)
    h = y1 - y0
    H, W = rgb.shape[:2]
    if h < 12:
        return None
    bg, share = _dominant(rgb[y0:y1, x0:x1])
    if share < 0.4 or float(bg.max() - bg.min()) >= ANCHOR_MIN_SATURATION or float(bg.max()) < 150:
        return None
    ry0, ry1 = max(0, y0 - h), min(H, y1 + h)
    rx0, rx1 = (max(0, x0 - int(2.6 * h)), x0) if side == "left" else (x1, min(W, x1 + int(2.6 * h)))
    if rx1 - rx0 < h // 2:
        return None
    region = rgb[ry0:ry1, rx0:rx1].astype(np.int32)
    diff = np.abs(region - bg).max(axis=2)
    ink = diff > 50
    text_colour = np.array(estimate_text_color(rgb, box, bg.astype(np.uint8)), dtype=np.int32)
    dist = np.sqrt(((region - text_colour) ** 2).sum(axis=2))
    unlike = ink & (diff > ANCHOR_MIN_CONTRAST) & (dist >= ANCHOR_COLOUR_DISTANCE)
    if not unlike.any():
        return None
    k = max(2, h // 10)  # (a tight merge: a dashed frame line next to the picture stays apart)
    grown = cv2.dilate(unlike.astype(np.uint8), np.ones((k, k), np.uint8))
    n, _labels, stats, _ = cv2.connectedComponentsWithStats(grown, connectivity=8)
    best = None
    for i in range(1, n):
        gx, gy, gw, gh, _area = (int(v) for v in stats[i])
        if not (0.35 * h <= gh <= 2.6 * h) or gw < ANCHOR_MIN_WIDTH * h or gw > 2.6 * h:
            continue  # (the OCR box may hold an answer box: its height overstates the text's)
        if gy + gh < h // 2 or gy > (ry1 - ry0) - h // 2:
            continue  # above or below the line, not beside it
        if gy == 0 or gy + gh >= ry1 - ry0:
            continue  # cut by the search band: part of a larger drawing
        near = (rx1 - rx0) - (gx + gw) if side == "left" else gx
        if near > 0.9 * h:
            continue
        px = region[gy:gy + gh, gx:gx + gw][unlike[gy:gy + gh, gx:gx + gw]]
        if px.size == 0 or float(np.median(px.max(axis=1) - px.min(axis=1))) < ANCHOR_MIN_SATURATION:
            continue
        if best is None or near < best[0]:
            best = (near, gx, gy, gw, gh)
    if best is None:
        return None
    _near, gx, gy, gw, gh = best
    between = (slice(None), slice(gx + gw, None)) if side == "left" else (slice(None), slice(0, gx))
    if (ink & (dist < ANCHOR_COLOUR_DISTANCE))[between].sum() > 0.02 * h * h:
        return None  # a word between the picture and the line: not its operand
    pic = (rx0 + max(0, gx - 2), ry0 + max(0, gy - 2), rx0 + min(rx1 - rx0, gx + gw + 2),
           ry0 + min(ry1 - ry0, gy + gh + 2))
    crop = np.ascontiguousarray(rgb[pic[1]:pic[3], pic[0]:pic[2]])
    if not _multicoloured(crop, bg) and text_check(crop):
        return None  # coloured text, not a picture
    return pic


def _multicoloured(crop: np.ndarray, bg: np.ndarray) -> bool:
    """Two or more distinct hues among the coloured pixels (a flower with its leaves):
    a drawing, never a coloured word - the recogniser readily "reads" such drawings."""
    px = crop.reshape(-1, 3)
    px = px[(np.abs(px.astype(np.int32) - bg).max(axis=1) > 50)
            & ((px.max(axis=1).astype(np.int32) - px.min(axis=1)) >= ANCHOR_MIN_SATURATION)]
    if len(px) < 30:
        return False
    hue = cv2.cvtColor(px.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_RGB2HSV)[:, 0, 0]
    counts = np.bincount(hue.astype(np.int32) // 15, minlength=12)
    return int((counts >= 0.15 * len(px)).sum()) >= 2


def is_cjk_char(ch: str) -> bool:
    return "\u3400" <= ch <= "\u9fff"
_TALLY_RE = re.compile(r"[正\s]+")
_BARE_LABEL_RE = re.compile(r"[A-Z]{2,4}['’]*(?:\s*[A-Z]{1,4}['’]*)?")


def classify_ocr_text(text: str, source_lang: Lang) -> tuple[str, list[str], bool, str]:
    """``(protected_text, fragments, translate, skip_reason)`` for an OCR line.

    Pure numbers / formulas (``is_fully_protected``), single Latin or Greek
    letters (diagram labels such as ``A``, ``B``, ``x``, ``α``) and text with
    neither source-script nor Latin letters (the same rule the text extractor
    applies) are kept as is. A single CJK character (``图``, ``解``) is a word
    and is translated.

    Korean sanity gate: a line of a Korean source that contains Han characters
    but no hangul at all (``臣C`` for ``빗변 c``, ``二 1-1`` for ``그림 1-1``) is
    almost always a misread by the zh/en OCR models rather than a hanja-only
    label; it is kept as is (``unreliable OCR``) so that garbage is never
    painted over a correct label. Latin-only labels (``Area = c²``) are still
    translated. No such gate exists for Japanese, where kanji-only labels
    (``小正方形``) are legitimate.
    """
    stripped = text.strip()
    if not stripped:
        return "", [], False, "empty"
    if is_fill_in_template(stripped):
        # answer boxes / circles read as letters ("O-O=O"): repainting them would destroy the exercise
        return make_placeholder(0), [stripped], False, FILL_IN_TEMPLATE
    if _EMPTY_QUOTES_RE.search(stripped) and any(is_cjk_char(c) for c in stripped):
        # (画“✓”) with the mark unread: a translation would say 'Draw ""'
        return protect_text(stripped, source_lang) + (False, UNREADABLE_SYMBOL)
    if any(is_cjk_char(c) for c in stripped) and has_pictogram_gap(stripped):
        # the sentence is built around pictures the OCR could not read (用○表示人 -> 用表示人)
        return protect_text(stripped, source_lang) + (False, INLINE_PICTOGRAMS)
    if _CJK_PLUS_RE.fullmatch(stripped):
        # "118十104" / "7一3": the OCR read a + or - sign as the look-alike character 十 / 一
        return make_placeholder(0), [stripped], False, "pure number / formula"
    if _TALLY_RE.fullmatch(stripped):
        # 正 used as counting strokes (tally marks) is a symbol, not a word
        return make_placeholder(0), [stripped], False, "tally marks"
    if _BARE_LABEL_RE.fullmatch(stripped):
        # a lone upper-case token in a diagram ("AB", "ABC", "PQR'") names a segment / polygon
        return make_placeholder(0), [stripped], False, "pure number / formula"
    protected, fragments = protect_text(stripped, source_lang)
    letters = [ch for ch in stripped if ch.isalpha()]
    if len(letters) == 1 and len(stripped.replace(" ", "")) <= 2 and _is_latin_or_greek(letters[0]):
        return protected, fragments, False, "single letter"
    if not letters or is_fully_protected(protected):
        return protected, fragments, False, "pure number / formula"
    profile = script_profile(stripped)
    if letters_of_script(stripped, source_lang) == 0 and profile["latin"] == 0:
        return protected, fragments, False, "no source-script letters"
    if Lang.parse(source_lang) is Lang.KO and profile["hangul"] == 0 and profile["han"] > 0:
        return protected, fragments, False, UNRELIABLE_OCR_KO
    return protected, fragments, True, ""


UNRELIABLE_OCR_KO = "unreliable OCR (Han characters but no hangul in a Korean source)"
FILL_IN_TEMPLATE = "fill-in template (answer boxes)"
UNREADABLE_SYMBOL = "unreadable symbol in quotes (left in the picture)"
INLINE_PICTOGRAMS = "inline pictograms the OCR cannot read (left in the picture)"
"""``skip_reason`` values for OCR lines that stay untouched in the picture."""
"""``skip_reason`` of Korean OCR lines rejected by the sanity gate of :func:`classify_ocr_text`."""


MAX_TEXT_SLANT_DEGREES = 12.0
_WRITING_GRID_RE = re.compile(r"[田口\s]{1,8}")


def answer_box_left_of(rgb: np.ndarray, box: tuple[int, int, int, int]) -> bool:
    """True when a coloured answer box (a saturated frame about one line high) stands right
    before ``box`` (within two line heights)."""
    x0, y0, x1, y1 = (int(v) for v in box)
    h = y1 - y0
    if h < 8:
        return False
    rx0 = max(0, x0 - 2 * h)
    if x0 - rx0 < h // 2:
        return False
    region = rgb[max(0, y0 - h // 4):y1 + h // 4, rx0:x0].astype(np.int32)
    if region.size == 0:
        return False
    sat = region.max(axis=2) - region.min(axis=2)
    coloured = (sat >= ANCHOR_MIN_SATURATION) & (np.abs(region - np.median(region.reshape(-1, 3), axis=0)).max(axis=2) > 50)
    cols = coloured.any(axis=0)
    rows = coloured.any(axis=1)
    return bool(cols.sum() >= 0.5 * h and rows.sum() >= 0.6 * h)


LOW_CONFIDENCE_SINGLE_CHAR = 0.9
"""A single non-Latin character below this OCR confidence is left in the picture."""
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


# --------------------------------------------------------------------------- #
# superscripts flattened by OCR
# --------------------------------------------------------------------------- #

PixelBox = tuple[int, int, int, int]

#: OCR text ending in one or two digits right after a letter, digit or closing bracket (``c2``, ``x10``,
#: ``(a+b)2``): the digits may be a superscript the OCR engine read as plain digits.
_TRAILING_DIGITS_RE = re.compile(r"[A-Za-z0-9)\]]\s?([0-9]{1,2})$")
_SUPERSCRIPT_DIGITS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
#: A trailing glyph counts as raised when its bottom sits at least this fraction of the box height
#: above the baseline of the other glyphs (a descender of ``g`` / ``y`` stays well below this)...
SUPERSCRIPT_MIN_RAISE = 0.2
#: ... and as clearly raised above this fraction.
SUPERSCRIPT_STRONG_RAISE = 0.3
#: A raised glyph must also be smaller than the tallest other glyph: at most this fraction of its height
#: when merely raised, a little more when clearly raised (a superscript after an x-height letter).
SUPERSCRIPT_MAX_HEIGHT = 0.8
SUPERSCRIPT_MAX_HEIGHT_STRONG = 0.9
#: Boxes lower than this (pixels) are too coarse for the geometry to be trusted.
SUPERSCRIPT_MIN_BOX_PX = 12


def glyph_clusters(ink: np.ndarray) -> list[tuple[int, int]]:
    """``[(x0, x1), ...]`` runs of columns containing ink, separated by at least one empty column."""
    cols = ink.any(axis=0)
    out: list[tuple[int, int]] = []
    start: Optional[int] = None
    for i, filled in enumerate(cols):
        if filled and start is None:
            start = i
        elif not filled and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(cols)))
    return out


def restore_superscripts(loaded: LoadedImage, box: PixelBox, text: str, bg: np.ndarray) -> str:
    """Put back a trailing superscript that OCR flattened to plain digits (``c2`` -> ``c²``).

    The OCR engines cannot tell ``c²`` from ``c2``, and the whole line is later
    repainted from the recognised text, so a flattened exponent would silently
    change the formula in the figure. The glyph geometry inside ``box`` still
    knows: the trailing digit glyphs are taken from the column profile of the
    ink (pixels farther than ``FREE_TOL`` from the background ``bg``), and when
    they sit clearly above the baseline of the other glyphs *and* are smaller
    than the tallest of them, the digits are replaced by their Unicode
    superscript forms. Flat digits, subscripts and descenders (``g2``) are
    left as they are; so is anything the heuristic cannot read safely (tiny,
    noisy or transparent boxes, touching glyphs).
    """
    stripped = text.strip()
    match = _TRAILING_DIGITS_RE.search(stripped)
    if not match:
        return text
    base = stripped[:match.start(1)].rstrip()
    if base[-1:].isdigit():
        return text  # "26", "50", "42颗": exponents on plain numbers do not occur in school books
    digits = match.group(1)
    n = len(digits)
    x0, y0, x1, y1 = box
    box_h = y1 - y0
    if box_h < SUPERSCRIPT_MIN_BOX_PX or x1 - x0 <= 0:
        return text
    region = loaded.rgb[y0:y1, x0:x1].astype(np.int16)
    ink = np.abs(region - bg.astype(np.int16)).max(axis=2) > FREE_TOL
    if loaded.alpha is not None:
        ink &= loaded.alpha[y0:y1, x0:x1] >= 128
    if not ink.any() or ink.mean() > 0.5:  # empty, or a busy background rather than glyphs
        return text
    clusters = glyph_clusters(ink)
    if len(clusters) < n + 1 or len(clusters) > 3 * len(stripped) + 2:
        return text

    def rows(cluster: tuple[int, int]) -> tuple[int, int]:
        r = np.flatnonzero(ink[:, cluster[0]:cluster[1]].any(axis=1))
        return int(r.min()), int(r.max()) + 1

    candidates = [rows(c) for c in clusters[-n:]]
    others = [rows(c) for c in clusters[:-n]]
    cand_top, cand_bottom = min(t for t, _ in candidates), max(b for _, b in candidates)
    cand_height = cand_bottom - cand_top
    baseline = float(np.median([b for _, b in others]))
    tallest = max(b - t for t, b in others)
    raise_ratio = (baseline - cand_bottom) / box_h
    if clusters[-n][0] - clusters[-n - 1][1] > box_h:  # too far from the base glyph to be its exponent
        return text
    if raise_ratio >= SUPERSCRIPT_STRONG_RAISE:
        max_height = SUPERSCRIPT_MAX_HEIGHT_STRONG
    elif raise_ratio >= SUPERSCRIPT_MIN_RAISE:
        max_height = SUPERSCRIPT_MAX_HEIGHT
    else:
        return text
    if cand_height >= max_height * tallest:
        return text
    return stripped[:match.start(1)] + digits.translate(_SUPERSCRIPT_DIGITS) + stripped[match.end(1):]


def build_image_segment(result: OcrResult, *, page_index: int, xref: int, index: int, loaded: LoadedImage,
                        image_bbox: BBox, transform: Any, source_lang: Lang,
                        text_check: Optional[TextCheck] = None) -> Optional[TextSegment]:
    """Turn one OCR result on image ``xref`` into an ``IMAGE_TEXT`` segment.

    A trailing superscript that the OCR engine flattened to plain digits is
    restored from the glyph geometry first (:func:`restore_superscripts`), so
    ``source_text`` carries ``c²`` rather than ``c2``.
    Returns ``None`` when the result's box has no area inside the image.
    """
    box = _clamp_box(result.box, loaded.width, loaded.height)
    raw_text = result.text
    place_value = split_place_value(raw_text, box)
    if place_value is not None:
        raw_text, box = place_value
        result = result.model_copy(update={"text": raw_text, "polygon": [[box[0], box[1]], [box[2], box[1]],
                                                                          [box[2], box[3]], [box[0], box[3]]]})
    han = sum(is_cjk_char(c) for c in raw_text)
    bw, bh = box[2] - box[0], box[3] - box[1]
    if han >= 2 and han == len(raw_text.strip()) and bh >= 1.8 * bw and bh / han > 1.25 * bw:
        # stacked characters (十位 written down a column): the detector's box often covers only part
        # of each character's width; widen it to the characters' size so they can be erased whole
        cx, half = (box[0] + box[2]) / 2, min(bh / han, 2.5 * bw) / 2
        box = _clamp_box((int(cx - half), box[1], int(cx + half + 0.999), box[3]), loaded.width, loaded.height)
        result = result.model_copy(update={"polygon": _rect(*box)})
    unit_core = _LEADING_BOXES_RE.sub("", raw_text.strip())
    bare = _BARE_UNIT_RE.fullmatch(raw_text.strip())
    if bare:
        # "）个": the measure word after an answer bracket; the bracket itself stays
        widths = [_char_width(c) for c in raw_text.strip()]
        cut = box[0] + int(sum(widths[:-1]) / max(sum(widths), 1e-6) * (box[2] - box[0]))
        box = (cut, box[1], box[2], box[3])
        raw_text = unit_core = "（" + bare.group(1) + "）"
        result = result.model_copy(update={"text": bare.group(1), "polygon": _rect(*box)})
    elif _UNIT_LABEL_RE.fullmatch(unit_core):
        # "（支）" whose box also holds the answer box before it ("□（支）", or the box unread):
        # keep only the label's pixels, so that dropping (erasing) it leaves the answer box alone
        cut = locate_trailing_label(loaded.rgb, box)
        if cut is not None and box[0] < cut < box[2]:
            box = (cut, box[1], box[2], box[3])
            raw_text = unit_core
            result = result.model_copy(update={"text": unit_core, "polygon": _rect(*box)})
        elif unit_core != raw_text.strip():
            unit_core = ""  # the label could not be separated from the box: leave both as they are
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
    text = restore_superscripts(loaded, box, space_after_enumerator(normalize_ocr_digits(result.text)), bg)
    if _EMPTY_QUOTES_RE.search(text):
        filled = fill_empty_quotes(text, detect_quoted_marks(loaded.rgb, box))
        if filled != text:
            logger.info("page %d image %d: marks read between the quotes: %r -> %r", page_index, xref, text, filled)
            text = filled
    anchors: dict[str, list[int]] = {}
    if text_check is not None and not _UNIT_LABEL_RE.fullmatch(unit_core):
        text, pixel_anchors = detect_anchors(loaded.rgb, box, text, f"{xref}.{index}", text_check)
        probe = ANCHOR_RE.sub("图", text.strip())
        for side, gap_re in (("left", _GAP_BEFORE_RE), ("right", _GAP_AFTER_RE)):
            if not gap_re.search(probe):
                continue
            pic = find_adjacent_picture(loaded.rgb, box, side, text_check)
            if pic is None:
                continue
            key = f"{xref}.{index}.{side[0]}"
            pixel_anchors[key] = list(pic)
            if side == "left":
                text = anchor_marker(key) + text.lstrip()
            else:
                body = text.rstrip()
                tail = body[-1] if body[-1:] in "，,。？?！!" else ""
                text = body[:len(body) - len(tail)] + anchor_marker(key) + tail
        anchors = {k: [xref, *v] for k, v in pixel_anchors.items()}
        if anchors:
            logger.info("page %d image %d: %d inline picture(s) anchored in %r", page_index, xref, len(anchors), text)
    if text != result.text:
        logger.info("page %d image %d: superscript restored from the glyph geometry: %r -> %r", page_index, xref,
                    result.text, text)
    protected, fragments, translate, reason = classify_ocr_text(text, source_lang)
    letters = [c for c in text if c.isalpha()]
    unit_label = bool(_UNIT_LABEL_RE.fullmatch(text.strip())) or bool(bare)
    if unit_label:
        # "(个)" after an answer box: English books write "13 - 9 = □" and let the picture show what is
        # counted; the label is erased (scanned pages) instead of being set as an unreadable "(apples)"
        translate, reason = False, "unit label after an answer box (dropped)"
    count_label = bool(_COUNT_LABEL_RE.fullmatch(text.strip()))
    lone = len(text.strip().strip("。，、：；！？.,:;!? ")) == 1
    if translate and _WRITING_GRID_RE.fullmatch(text.strip()):
        translate, reason = False, "writing grid"  # 田 cells for practising characters, not a word
    elif (translate and lone and len(letters) == 1 and not letters[0].isascii() and not count_label
            and result.confidence < LOW_CONFIDENCE_SINGLE_CHAR):
        # a lone CJK character read with low confidence is usually noise (an arrow, a stroke, a watermark piece)
        translate, reason = False, f"single character with low OCR confidence ({result.confidence:.2f})"
    elif (translate and lone and text.strip() in MEASURE_WORDS
            and answer_box_left_of(loaded.rgb, box)):
        # a lone measure word right after an answer box (□ 个): dropped like （个）
        translate, reason = False, "unit label after an answer box (dropped)"
    slant = polygon_slant_degrees(result.polygon)
    if translate and MAX_TEXT_SLANT_DEGREES < slant < 90.0 - MAX_TEXT_SLANT_DEGREES:
        translate, reason = False, f"slanted text ({slant:.0f}°): watermark or decoration, kept as is"
    return TextSegment(
        id=f"p{page_index}_i{xref}_{index}",
        page=page_index,
        kind=SegmentKind.IMAGE_TEXT,
        bbox=page_bbox,
        source_text=text.strip(),
        protected_text=protected,
        protected=fragments,
        style=SegmentStyle(size=max(size_pt, 1.0), color=rgb_to_int(color), role="label", align="left"),
        image=ImageRef(xref=xref, page=page_index, bbox=image_bbox, width=loaded.width, height=loaded.height,
                       pixel_box=box, polygon=[[float(x), float(y)] for x, y in result.polygon],
                       confidence=float(result.confidence)),
        translate=translate,
        skip_reason=reason,
        anchors=anchors,
    )


UNREAD_UNIT = "（?）"
"""Text given to a unit label found in the pixels but misread by the OCR (``(v)``, ``(*)``)."""
_TRAILING_BOX_RE = re.compile(r"(?<![0-9])[□○OoD0Q口〇◯●◇△▲☐]\s*$")
"""``=□`` / ``=0`` (a box read as a digit) at the end of a template; ``=230`` is a result."""
_BARE_UNIT_RE = re.compile(rf"[)）]\s*([{MEASURE_WORDS}])")
"""``）个``: a measure word right after the closing bracket of an answer blank."""
_MISREAD_UNIT_RE = re.compile(r"^\s*[（(]\s*[^\s()（）]?\s*[)）]|[（(]\s*[^\s()（）]?\s*[)）]\s*$")
_LEADING_BOXES_RE = re.compile(r"^[□○OoD0Q口〇◯●◇△▲☐)）\s]+")


def locate_trailing_label(rgb: np.ndarray, box: tuple[int, int, int, int]) -> Optional[int]:
    """Pixel x where a dark label (``（个）``) right of a coloured answer box starts inside
    ``box``, or None. The ink columns are read from the right: dark runs belong to the label,
    the first coloured run is the answer box. A label must have ink in its middle (an empty
    ``（ ）`` is an answer bracket, not a unit) and be about one to three line heights wide."""
    x0, y0, x1, y1 = (int(v) for v in box)
    crop = rgb[max(0, y0):y1, max(0, x0):x1]
    h, w = crop.shape[:2]
    if h < 8 or w < 2 * h:
        return None
    bg, _share = _dominant(crop)
    px = crop.astype(np.int32)
    ink = np.abs(px - bg).max(axis=2) > 60
    sat = px.max(axis=2) - px.min(axis=2)
    runs: list[list[int]] = []
    for xi in np.flatnonzero(ink.any(axis=0)):
        if runs and xi - runs[-1][1] <= max(2, h // 8):
            runs[-1][1] = int(xi) + 1
        else:
            runs.append([int(xi), int(xi) + 1])
    start, i = None, len(runs) - 1
    while i >= 0:
        a, b = runs[i]
        cell = ink[:, a:b]
        if float(np.median(sat[:, a:b][cell])) >= ANCHOR_MIN_SATURATION:
            break  # the coloured answer box
        start, i = a, i - 1
    if start is None or i < 0:
        return None
    end = runs[-1][1]
    if not (0.8 * h <= end - start <= 3.6 * h):
        return None
    mid = ink[:, start + (end - start) * 3 // 10:start + (end - start) * 7 // 10]
    if mid.size == 0 or not mid.any():
        return None  # "（ ）": an empty answer bracket
    gap = start - runs[i][1]
    return max(0, x0) + start - max(1, min(gap // 2, h // 4))


WIDE_GAP = 1.6
"""An empty stretch wider than this many line heights inside one OCR line separates two
labels (price tags, captions, table cells) the detector merged."""
WIDE_GAP_SPACED = 1.0
"""... or this many when the recogniser itself put a space into the text."""
_PRICE_TOKENS_RE = re.compile(r"(?:¥?\d+(?:\.\d+)?\s*[元角分](?:\d+\s*[角分])?\s*){2,}")


NUMERAL_STROKES = {1: "一", 2: "二", 3: "三"}


def numeral_strokes_left_of(rgb: np.ndarray, box: tuple[int, int, int, int],
                            others: Sequence[tuple[int, int, int, int]] = ()) -> Optional[tuple[str, int]]:
    """The unit numeral 一 / 二 / 三 the detector skipped before a heading (``一  生活中的数``,
    its strokes look like rules): one to three flat dark strokes stacked within the line's
    height, left of ``box`` within three line heights, nothing else there, no other OCR box
    in the way. Returns ``(numeral, x0, x1)`` of the strokes or None."""
    H, W = rgb.shape[:2]
    x0, y0, x1, y1 = (int(v) for v in box)
    x0, x1, y0, y1 = max(0, min(x0, W)), max(0, min(x1, W)), max(0, min(y0, H)), max(0, min(y1, H))
    h = y1 - y0
    if h < 10 or x1 <= x0:
        return None
    rx0, rx1 = max(0, x0 - 3 * h), max(0, x0 - max(2, h // 8))
    if rx1 - rx0 < h:
        return None
    for ox0, oy0, ox1, oy1 in others:
        if ox1 > rx0 and ox0 < rx1 and oy1 > y0 and oy0 < y1:
            rx0 = max(rx0, ox1 + 1)  # another line stands left of this one: search only after it
    if rx1 - rx0 < h:
        return None
    region = rgb[y0:y1, rx0:rx1]
    if region.size == 0:
        return None
    bg, share = _dominant(region)
    if share < 0.6 or float(bg.max()) < 150:
        return None
    ink = (np.abs(region.astype(np.int32) - bg).max(axis=2) > 80).astype(np.uint8)
    if not ink.any():
        return None
    n, labels, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    strokes, others_ink = [], []
    for i in range(1, n):
        bx, by, bw, bh, area = (int(v) for v in stats[i])
        if area < 6:
            continue  # dust
        if (0.45 * h <= bw <= 1.3 * h and 0.07 * h <= bh <= 0.28 * h and bw >= 2.5 * bh
                and area >= 0.6 * bw * bh):
            strokes.append((bx, by, bw, bh))  # a thick printed stroke, not the hairline of a diagram
        else:
            others_ink.append((bx, by, bw, bh))
    if not 1 <= len(strokes) <= 3:
        return None
    strokes.sort(key=lambda t: t[1])
    xs0, xs1 = min(t[0] for t in strokes), max(t[0] + t[2] for t in strokes)
    if xs1 - xs0 > 1.4 * h:
        return None  # not stacked
    centre = (min(t[1] for t in strokes) + max(t[1] + t[3] for t in strokes)) / 2
    if not 0.3 * h <= centre <= 0.7 * h:
        return None  # a rule along the top or bottom of the line, not a numeral beside it
    if any(bx + bw > xs0 - h // 4 for bx, _by, bw, _bh in others_ink):
        return None  # a picture, a letter or a frame between the strokes and the line (or among them)
    gap_to_line = (rx1 - rx0 - xs1) + (x0 - rx1)
    if gap_to_line > 2.2 * h:
        return None
    return NUMERAL_STROKES[len(strokes)], rx0 + xs0, rx0 + xs1


def attach_numeral_strokes(results: list[OcrResult], rgb: np.ndarray) -> list[OcrResult]:
    """Prefix a CJK line with the unit numeral whose strokes the detector skipped before it
    (see :func:`numeral_strokes_left_of`); the result's box then covers the strokes."""
    boxes = [r.box for r in results]
    out: list[OcrResult] = []
    for i, r in enumerate(results):
        text = r.text.strip()
        if not text or not is_cjk_char(text[0]) or _UNIT_NUMERAL_START_RE.match(text):
            out.append(r)
            continue
        bh = r.box[3] - r.box[1]
        # only text lines of about this size stand in the way; the huge box of a slanted watermark
        # line or of a picture caption spanning the page does not
        found = numeral_strokes_left_of(rgb, r.box, [b for j, b in enumerate(boxes)
                                                     if j != i and 0.5 * bh <= b[3] - b[1] <= 2.0 * bh
                                                     and b[2] - b[0] <= 12 * bh])
        if found is None:
            out.append(r)
            continue
        numeral, sx0, sx1 = found
        bx0, by0, bx1, by1 = r.box
        sep = " " if bx0 - sx1 > 0.3 * (by1 - by0) else ""  # 一  生活中的数 (a unit heading) / 一共有
        out.append(OcrResult(text=numeral + sep + text, polygon=_rect(sx0, by0, bx1, by1), confidence=r.confidence))
    return out


_UNIT_NUMERAL_START_RE = re.compile(r"^[一二三四五六七八九十]")


def split_price_tokens(results: list[OcrResult]) -> list[OcrResult]:
    """``20元1元5角`` (three price tags side by side read as one line) -> one result per
    amount, cut by the amounts' estimated widths."""
    out: list[OcrResult] = []
    for r in results:
        text = r.text.strip()
        if not _PRICE_TOKENS_RE.fullmatch(text):
            out.append(r)
            continue
        tokens = re.findall(r"¥?\d+(?:\.\d+)?\s*[元角分](?:\d+\s*[角分])?", text)
        if len(tokens) < 2:
            out.append(r)
            continue
        xs = [p[0] for p in r.polygon]; ys = [p[1] for p in r.polygon]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        widths = [sum(_char_width(c) for c in t) for t in tokens]
        total = sum(widths) or 1.0
        pos = x0
        for t, w in zip(tokens, widths):
            end = pos + w / total * (x1 - x0)
            out.append(OcrResult(text=t.strip(), polygon=_rect(pos, y0, end, y1), confidence=r.confidence))
            pos = end
    return out
_ENUM_DIGIT_RE = re.compile(r"^(\s*(?:[（(]\d{1,2}[)）]|[①-⑳]))(\d)")


def _ink_runs(rgb: np.ndarray, box: tuple[int, int, int, int]) -> Optional[tuple[list[tuple[int, int]], int]]:
    """Horizontal ink runs ``[(x0, x1), ...]`` (crop coordinates) of a line box and the line
    height, or None when the background is not plain."""
    x0, y0, x1, y1 = (int(v) for v in box)
    crop = rgb[max(0, y0):y1, max(0, x0):x1]
    h, w = crop.shape[:2]
    if h < 8 or w < 2 * h or crop.size == 0:
        return None
    bg, share = _dominant(crop)
    if share < 0.4:
        return None
    ink = np.abs(crop.astype(np.int32) - bg).max(axis=2) > 50
    runs: list[list[int]] = []
    for xi in np.flatnonzero(ink.any(axis=0)):
        if runs and xi - runs[-1][1] <= max(2, h // 8):
            runs[-1][1] = int(xi) + 1
        else:
            runs.append([int(xi), int(xi) + 1])
    return [(a, b) for a, b in runs], h


def split_wide_gaps(results: list[OcrResult], rgb: np.ndarray) -> list[OcrResult]:
    """Split OCR lines whose ink shows an empty stretch of at least :data:`WIDE_GAP` line
    heights (``¥32    ¥23``, ``小华   小明``, the cells of a table row) into one result per
    piece; the characters go to the pieces by their estimated widths, at a space of the OCR
    text when there is one nearby. Templates and formulas are left alone."""
    out: list[OcrResult] = []
    for r in results:
        text = r.text.strip()
        if len(text) < 2 or is_fill_in_template(text) or _formula_core(text) or ANCHOR_RE.search(text):
            out.append(r)
            continue
        xs = [p[0] for p in r.polygon]; ys = [p[1] for p in r.polygon]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        found = _ink_runs(rgb, (int(x0), int(y0), int(x1 + 0.999), int(y1 + 0.999)))
        if found is None:
            out.append(r)
            continue
        runs, h = found
        spaced = " " in text  # the recogniser marked a gap itself: a narrower one will do
        cuts: list[tuple[int, int]] = []  # (end of the ink before the gap, start of the ink after it)
        for (_a, b), (c, _d) in zip(runs, runs[1:]):
            if c - b >= (WIDE_GAP_SPACED if spaced else WIDE_GAP) * h:
                cuts.append((b, c))
        if not cuts:
            out.append(r)
            continue
        # character positions along the line by their estimated widths over the ink extent
        widths = [_char_width(ch) for ch in text]
        total = sum(widths) or 1.0
        ink_x0, ink_x1 = runs[0][0], runs[-1][1]
        ink_w = float(ink_x1 - ink_x0)
        if ink_w <= 0:
            out.append(r)
            continue
        pieces: list[tuple[int, int]] = []  # (char_from, char_to)
        start = 0
        acc = 0.0
        centres = []
        for cw in widths:
            centres.append(ink_x0 + (acc + cw / 2) / total * ink_w)
            acc += cw
        ok = True
        for b, c in cuts:
            cut = (b + c) // 2
            k = next((i for i, cx in enumerate(centres) if cx > cut), len(text))
            # prefer a space of the OCR text within one character of the geometric split
            for cand in (k, k - 1, k + 1):
                if 0 < cand < len(text) and text[cand - 1] == " ":
                    k = cand
                    break
                if 0 < cand < len(text) and text[cand] == " ":
                    k = cand + 1
                    break
            if k <= start or k >= len(text) or not text[start:k].strip():
                ok = False
                break
            pieces.append((start, k))
            start = k
        if not ok or not text[start:].strip():
            out.append(r)
            continue
        pieces.append((start, len(text)))
        margin = max(1, h // 10)
        starts = [int(x0)] + [int(x0) + c - margin for _b, c in cuts]
        ends = [int(x0) + b + margin for b, _c in cuts] + [int(x1 + 0.999)]
        for (a, b), px0, px1 in zip(pieces, starts, ends):
            piece = text[a:b].strip()
            if not piece:
                continue
            out.append(OcrResult(text=piece, polygon=_rect(px0, y0, px1, y1), confidence=r.confidence))
    return out


def split_stacked_repeats(results: list[OcrResult]) -> list[OcrResult]:
    """``有有`` / ``个个个个`` read down a column (one character per row of a fill-in grid)
    become one result per character, each with its own row's box."""
    out: list[OcrResult] = []
    for r in results:
        text = r.text.strip()
        n = len(text)
        if n < 2 or len(set(text)) != 1 or not is_cjk_char(text[0]):
            out.append(r)
            continue
        xs = [p[0] for p in r.polygon]; ys = [p[1] for p in r.polygon]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if (y1 - y0) < max(1.5, 0.7 * n) * (x1 - x0):
            out.append(r)  # side by side (一一 / 口口), not a column
            continue
        step = (y1 - y0) / n
        for i in range(n):
            out.append(OcrResult(text=text[0], polygon=_rect(x0, y0 + i * step, x1, y0 + (i + 1) * step),
                                 confidence=r.confidence))
    return out


def space_after_enumerator(text: str) -> str:
    """``(2)36`` / ``①3`` -> ``(2) 36`` / ``① 3``: the enumerator and the number that follows
    it are two tokens (``2.40`` is left to the page-level check: it may be a decimal)."""
    return _ENUM_DIGIT_RE.sub(lambda m: m.group(1) + " " + m.group(2), text, count=1)


def _rect(x0: float, y0: float, x1: float, y1: float) -> list[list[float]]:
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def _split_template_units(results: list[OcrResult], rgb: Optional[np.ndarray] = None) -> list[OcrResult]:
    """Split a trailing unit label off an answer-box template line (``□-□=□（个）``) so the
    template stays untouched in the picture while the label is handled (dropped) on its own.
    With the image's pixels (``rgb``) the cut is placed where the label starts, and labels the
    OCR misread (``O=O-O (v)``, ``(v) O=O-O``, ``□（只）``) are found too."""
    out: list[OcrResult] = []
    for r in results:
        text = r.text.strip()
        xs = [p[0] for p in r.polygon]; ys = [p[1] for p in r.polygon]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        m = re.search(rf"[（(]\s*[{MEASURE_WORDS}]\s*[)）]\s*$", text)
        if m and m.start() > 0:
            head, unit = text[:m.start()], text[m.start():]
        else:
            m = _MISREAD_UNIT_RE.search(text) if rgb is not None else None
            if not m:
                out.append(r)
                continue
            head, unit = (text[:m.start()] + text[m.end():]).strip(), m.group(0).strip()
            if not _UNIT_LABEL_RE.fullmatch(unit):
                unit = UNREAD_UNIT
        boxes_only = bool(head.strip()) and not _LEADING_BOXES_RE.sub("", head.strip())
        if not (is_fill_in_template(text) or is_fill_in_template(head) or boxes_only
                or ("=" in head and _TRAILING_BOX_RE.search(head))):
            out.append(r)  # a worked result keeps its unit: 10÷5=2（元）, 260-30=230（元）
            continue
        cut = locate_trailing_label(rgb, (int(x0), int(y0), int(x1 + 0.999), int(y1 + 0.999))) \
            if rgb is not None else None
        if cut is None:
            if not m or m.start() == 0 or unit == UNREAD_UNIT:
                out.append(r)  # where the label sits is unknown
                continue
            widths = [_char_width(c) for c in text]
            cut = x0 + sum(widths[:m.start()]) / max(sum(widths), 1e-6) * (x1 - x0)
        out.append(OcrResult(text=head, polygon=_rect(x0, y0, cut, y1), confidence=r.confidence))
        out.append(OcrResult(text=unit, polygon=_rect(cut + 1, y0, x1, y1), confidence=r.confidence))
    return out


def _text_check_for(engine: Any) -> Optional[TextCheck]:
    """A :data:`TextCheck` backed by the engine's recogniser (RapidOCR), or None."""
    recognize_crop = getattr(engine, "recognize_crop", None)
    if recognize_crop is None:
        return None

    def check(crop: np.ndarray) -> bool:
        try:
            found, conf = recognize_crop(crop)
        except Exception:  # noqa: BLE001 - no verdict, no anchor
            return True
        letters = [c for c in found if c.isalnum() and c not in _BOX_GLYPHS]  # a square "reads" as 口 / 0
        return bool(letters) and conf >= 0.5
    return check


def _open_pdf(source: PdfSource) -> tuple[pymupdf.Document, bool]:
    if isinstance(source, pymupdf.Document):
        return source, False
    return pymupdf.open(str(source)), True


def extract_image_segments(pdf_path: PdfSource, doc: TranslatedDocument, engine: OcrEngine, *,
                           min_confidence: float = 0.6, min_image_px: int = 40,
                           pages: Optional[list[int]] = None, max_image_px: int = MAX_IMAGE_PX,
                           failures: Optional[list[str]] = None) -> list[TextSegment]:
    """Run OCR on the images of ``pdf_path`` and return ``IMAGE_TEXT`` segments.

    Each image XObject is processed once (on the first page that places it) so
    that a shared image gets one translation; tiny images (below
    ``min_image_px`` in either dimension), oversized images (more than
    ``max_image_px`` pixels - they are never decoded, see :data:`MAX_IMAGE_PX`),
    soft masks and OCR results under ``min_confidence`` are ignored. Results
    that need no translation are still returned with ``translate=False`` and a
    ``skip_reason`` so the pipeline can report them. Nothing is appended to
    ``doc`` - the caller extends ``doc.segments``.

    An :class:`~mathtrans.ocr.OcrError` on one image is logged, recorded in
    ``failures`` (when given) and the image is skipped; an
    :class:`~mathtrans.ocr.OcrUnavailableError` (credentials, model, SDK) is
    re-raised at once instead of being retried on every remaining image.
    """
    pdf_doc, owned = _open_pdf(pdf_path)
    wanted = set(pages) if pages is not None else None
    text_check = _text_check_for(engine)
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
                if max_image_px and w * h > max_image_px:
                    logger.warning("page %d: skipping oversized image xref %d (%dx%d px > %d pixel budget, "
                                   "MATHTRANS_MAX_IMAGE_MEGAPIXELS); its text is kept as is",
                                   page.number, xref, w, h, max_image_px)
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
                except OcrUnavailableError:
                    raise
                except OcrError as exc:
                    logger.warning("page %d: OCR failed on image xref %d: %s", page.number, xref, exc)
                    if failures is not None:
                        failures.append(f"page {page.number + 1} image xref {xref}: {exc}")
                    continue
                image_bbox = BBox.from_rect(info["bbox"])
                transform = info.get("transform") or (image_bbox.width, 0.0, 0.0, image_bbox.height,
                                                       image_bbox.x0, image_bbox.y0)
                kept = translatable = 0
                prepared = split_stacked_repeats(split_price_tokens(
                    split_wide_gaps(_split_template_units(results, loaded.rgb), loaded.rgb)))
                prepared = attach_numeral_strokes(prepared, loaded.rgb)
                for n, result in enumerate(prepared):
                    if result.confidence < min_confidence:
                        logger.debug("page %d image %d: dropping %r (confidence %.2f < %.2f)", page.number, xref,
                                     result.text, result.confidence, min_confidence)
                        continue
                    seg = build_image_segment(result, page_index=page.number, xref=xref, index=n, loaded=loaded,
                                              image_bbox=image_bbox, transform=transform,
                                              source_lang=doc.source_lang, text_check=text_check)
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


def _xobject_owner(pdf_doc: pymupdf.Document, page: pymupdf.Page) -> Optional[tuple[int, str]]:
    """``(xref, path)`` of the object that holds the page's ``/XObject`` resource dictionary directly.

    ``Document.xref_set_key`` only edits the object it is given: a path through
    an indirect ``/Resources`` object is not followed, so the owner (the page,
    its indirect resources, the indirect ``/XObject`` dictionary, or an
    ancestor ``/Pages`` node when the resources are inherited) is resolved
    first. ``path`` is the key path inside that object (empty when the owner
    *is* the ``/XObject`` dictionary). ``None`` when there is no such dictionary.
    """
    owner = page.xref
    kind, value = pdf_doc.xref_get_key(owner, "Resources")
    while kind == "null":  # inherited resources
        pkind, parent = pdf_doc.xref_get_key(owner, "Parent")
        if pkind != "xref":
            return None
        owner = int(parent.split()[0])
        kind, value = pdf_doc.xref_get_key(owner, "Resources")
    if kind == "xref":
        owner, path = int(value.split()[0]), "XObject"
    elif kind == "dict":
        path = "Resources/XObject"
    else:
        return None
    kind, value = pdf_doc.xref_get_key(owner, path)
    if kind == "xref":
        return int(value.split()[0]), ""
    if kind == "dict":
        return owner, path
    return None


def replace_image(page: pymupdf.Page, xref: int, stream: bytes) -> None:
    """``page.replace_image(xref, stream=...)`` without leaving a second copy of the image behind.

    PyMuPDF implements ``replace_image`` as ``insert_image`` (a new image
    object under a new ``/XObject`` resource name plus an extra ``/Contents``
    stream, which is then blanked) followed by ``xref_copy(new -> old)``. The
    drawn ``xref`` ends up with the new pixels, but the never-drawn duplicate
    stays referenced from the page resources, so no garbage collection level
    drops it and every replaced image is stored twice. The resource entry the
    call added (identified by name, which is unambiguous where xrefs and
    digests of two identical images are not) is set to ``null`` here - the PDF
    equivalent of an absent entry - so a save with ``garbage >= 1`` discards
    the duplicate. When the resource dictionary cannot be located the
    duplicate is left in place (the output is still correct, just larger).
    """
    doc = page.parent
    before = {im[7] for im in page.get_images(full=True) if im[9] == 0}
    page.replace_image(xref, stream=stream)
    stale = [im[7] for im in page.get_images(full=True) if im[9] == 0 and im[7] not in before]
    if not stale:
        return
    owner = _xobject_owner(doc, page)
    if owner is None:
        logger.debug("page %d: cannot locate the /XObject resources; the duplicate of image %d stays", page.number, xref)
        return
    owner_xref, path = owner
    for name in stale:
        try:
            doc.xref_set_key(owner_xref, f"{path}/{name}" if path else name, "null")
        except Exception as exc:  # pragma: no cover - defensive: odd resource dictionaries
            logger.debug("page %d: cannot drop duplicate image resource %s: %s", page.number, name, exc)
    page._image_info = None


def render_image_segments(pdf_doc: pymupdf.Document, doc: TranslatedDocument, *,
                          fonts_dir: Optional[Union[str, Path]] = None) -> int:
    """Paint translated ``IMAGE_TEXT`` segments into their images and replace them in ``pdf_doc``.

    Segments are grouped by image xref; each image is decoded once, every
    translation is drawn (original glyphs erased first), and the image stream
    is replaced on the page that references it - :func:`replace_image` swaps
    the stream behind the xref (without the duplicate object that
    ``page.replace_image`` leaves behind), so all placements are updated while
    the placement rectangles and pixel dimensions stay unchanged. The image is
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
        stream = encode_image(canvas, alpha, loaded.ext, qtables=loaded.jpeg_qtables,
                              subsampling=loaded.jpeg_subsampling)
        try:
            replace_image(page, placement.xref, stream)
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
