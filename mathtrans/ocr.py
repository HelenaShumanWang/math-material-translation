"""OCR engines for text embedded in raster images.

Three engines implement the :class:`~mathtrans.interfaces.OcrEngine` protocol:

* :class:`RapidOcrEngine` - offline, wraps ``rapidocr_onnxruntime`` (models are
  bundled with the package, so it works without network access).
* :class:`ClaudeVisionOcrEngine` - sends the image to Claude and asks for a
  structured JSON list of text regions (useful for scripts the offline models
  do not cover well, e.g. Japanese / Korean / accented Latin text).
* :class:`NullOcrEngine` - recognises nothing (text inside images is kept as is).

All engines take an ``HxWx3`` RGB ``uint8`` array and return
:class:`~mathtrans.models.OcrResult` objects whose polygons are in image pixel
coordinates (top-left origin).
"""
from __future__ import annotations

import base64
import importlib.util
import io
import json
import logging
import threading
from typing import Any, Optional

import anthropic
import numpy as np

from .config import Settings, get_settings
from .interfaces import OcrEngine
from .languages import LANGUAGES
from .models import Lang, OcrResult

logger = logging.getLogger("mathtrans.ocr")

#: Images whose longest side is below this are upscaled 2x before OCR.
UPSCALE_MAX_SIDE = 600
#: Images whose longest side exceeds this are downscaled before RapidOCR runs (boxes are mapped back
#: to full-resolution pixels). Bounds the memory of huge rasters (high-DPI scans, decompression bombs);
#: PP-OCR text detection does not benefit from more pixels than this anyway.
DOWNSCALE_MAX_SIDE = 4000
#: Claude downsamples larger images anyway; sending more pixels only costs tokens.
CLAUDE_MAX_SIDE = 1568
#: Coordinates returned by the vision model are normalised to this range.
CLAUDE_COORD_RANGE = 1000.0
CLAUDE_MAX_TOKENS = 16000
#: Source languages whose script the bundled RapidOCR (zh/en PP-OCR) models read only partially:
#: kana and hangul are often misread as look-alike Han characters.
RAPID_LOW_TRUST_LANGS = frozenset({Lang.JA, Lang.KO})


class OcrError(RuntimeError):
    """An OCR backend could not produce a result for an image (callers skip that image)."""


class OcrUnavailableError(OcrError):
    """The OCR backend cannot serve *any* request: credentials, model or SDK problem.

    Raised instead of :class:`OcrError` so that callers stop after the first
    image instead of issuing one failing request per image and silently
    delivering a document whose in-image text was never translated.
    """


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #


def as_rgb_uint8(image: Any) -> np.ndarray:
    """Coerce ``image`` to a contiguous ``HxWx3`` uint8 RGB array.

    Accepts gray (``HxW``), RGB (``HxWx3``) and RGBA (``HxWx4``, alpha is
    dropped) arrays; anything else raises ``ValueError``.
    """
    arr = np.asarray(image)
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    elif arr.ndim == 3 and arr.shape[2] == 1:
        arr = np.concatenate([arr, arr, arr], axis=-1)
    elif arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[..., :3]
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise ValueError(f"expected an HxWx3 RGB image, got shape {arr.shape}")
    if arr.shape[0] == 0 or arr.shape[1] == 0:
        raise ValueError("empty image")
    return np.ascontiguousarray(arr)


def _lang_codes(hint_langs: Optional[list[Lang]]) -> Optional[list[str]]:
    """Language codes of ``hint_langs`` (accepts ``Lang`` members or code strings)."""
    if not hint_langs:
        return None
    return [Lang.parse(lang).value for lang in hint_langs]


def _clean_polygon(points: Any) -> Optional[list[list[float]]]:
    try:
        poly = [[float(p[0]), float(p[1])] for p in points]
    except (TypeError, ValueError, IndexError):
        return None
    if len(poly) != 4 or any(not np.isfinite(v) for pt in poly for v in pt):
        return None
    return poly


# --------------------------------------------------------------------------- #
# RapidOCR (offline)
# --------------------------------------------------------------------------- #


class RapidOcrEngine:
    """Offline OCR through ``rapidocr_onnxruntime`` (PP-OCR models).

    The underlying ``RapidOCR`` object is created lazily and shared by all
    instances (model loading takes a few hundred milliseconds). When the
    package cannot be imported, :meth:`recognize` returns an empty list and the
    problem is logged once.

    The bundled models are the Chinese + English PP-OCRv4 set; they read
    Chinese, Latin letters and digits reliably, Japanese kana / Korean hangul
    only partially (see :data:`RAPID_LOW_TRUST_LANGS`; a warning is logged once
    per process when such a source is OCR'd). Use :class:`ClaudeVisionOcrEngine`
    for those sources.

    Images are upscaled 2x below ``upscale_max_side`` and downscaled above
    ``downscale_max_side`` (longest side) before recognition; the returned
    polygons are always in the original pixel space.
    """

    name = "rapid"

    _lock = threading.Lock()
    _shared: Any = None
    _import_error: Optional[BaseException] = None
    _import_error_logged = False
    _low_trust_warned = False

    def __init__(self, upscale_max_side: int = UPSCALE_MAX_SIDE, downscale_max_side: int = DOWNSCALE_MAX_SIDE):
        self.upscale_max_side = int(upscale_max_side)
        self.downscale_max_side = int(downscale_max_side)

    @staticmethod
    def available() -> bool:
        """True when ``rapidocr_onnxruntime`` is importable."""
        try:
            return importlib.util.find_spec("rapidocr_onnxruntime") is not None
        except (ImportError, ValueError):
            return False

    @classmethod
    def _engine(cls) -> Any:
        """The shared ``RapidOCR`` instance, or ``None`` when unavailable."""
        with cls._lock:
            if cls._shared is not None:
                return cls._shared
            if cls._import_error is not None:
                return None
            try:
                from rapidocr_onnxruntime import RapidOCR

                cls._shared = RapidOCR()
            except Exception as exc:  # ImportError, missing models, onnxruntime failures
                cls._import_error = exc
                if not cls._import_error_logged:
                    cls._import_error_logged = True
                    logger.warning("RapidOCR is unavailable (%s: %s); text inside images will not be "
                                   "recognised by the 'rapid' engine", type(exc).__name__, exc)
                return None
            return cls._shared

    @classmethod
    def reset(cls) -> None:
        """Forget the shared instance and any recorded import failure (tests)."""
        with cls._lock:
            cls._shared = None
            cls._import_error = None
            cls._import_error_logged = False
            cls._low_trust_warned = False

    @classmethod
    def _warn_low_trust(cls, hint_langs: Optional[list[Lang]]) -> None:
        """Warn once per process when a ja/ko source is read by the zh/en models."""
        if cls._low_trust_warned:
            return
        try:
            hints = {Lang.parse(lang) for lang in hint_langs or []}
        except (ValueError, KeyError):
            return
        low = sorted(lang.value for lang in hints & RAPID_LOW_TRUST_LANGS)
        if low:
            cls._low_trust_warned = True
            logger.warning("RapidOCR's bundled Chinese/English models read %s text inside images only partially "
                           "(kana / hangul are often misread as Han characters): check the figures in the preview "
                           "or use the Claude vision OCR (MATHTRANS_OCR_ENGINE=claude / --ocr-engine claude)",
                           ", ".join(LANGUAGES[Lang(c)].name_en for c in low))

    def recognize(self, image_rgb: np.ndarray, hint_langs: Optional[list[Lang]] = None) -> list[OcrResult]:
        engine = self._engine()
        if engine is None:
            return []
        import cv2

        self._warn_low_trust(hint_langs)
        rgb = as_rgb_uint8(image_rgb)
        h, w = rgb.shape[:2]
        scale = 1.0
        if max(h, w) < self.upscale_max_side:
            scale = 2.0
            rgb = cv2.resize(rgb, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
        elif self.downscale_max_side > 0 and max(h, w) > self.downscale_max_side:
            # Huge rasters are recognised at a bounded size: this caps the colour-conversion copies and
            # the detection model's memory; the polygons are mapped back to full resolution below.
            scale = self.downscale_max_side / float(max(h, w))
            rgb = cv2.resize(rgb, (max(1, round(w * scale)), max(1, round(h * scale))), interpolation=cv2.INTER_AREA)
            logger.debug("rapid OCR: %dx%d image downscaled by %.3f before recognition", w, h, scale)
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)  # RapidOCR treats 3-channel arrays as BGR
        try:
            result, _elapse = engine(bgr)
        except Exception as exc:
            raise OcrError(f"RapidOCR failed on a {w}x{h} image: {exc}") from exc
        out: list[OcrResult] = []
        for item in result or []:
            try:
                box, text, conf = item[0], item[1], item[2]
            except (TypeError, IndexError):
                logger.debug("ignoring malformed RapidOCR item %r", item)
                continue
            poly = _clean_polygon(box)
            text = str(text).strip()
            if poly is None or not text:
                continue
            if scale != 1.0:
                poly = [[x / scale, y / scale] for x, y in poly]
            poly = [[min(max(x, 0.0), float(w)), min(max(y, 0.0), float(h))] for x, y in poly]
            out.append(OcrResult(text=text, polygon=poly, confidence=float(conf)))
        logger.debug("rapid OCR: %d regions in %dx%d image (hint %s)", len(out), w, h, _lang_codes(hint_langs))
        return out


# --------------------------------------------------------------------------- #
# Claude vision
# --------------------------------------------------------------------------- #

_OCR_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "box": {"type": "array", "items": {"type": "number"}},
                },
                "required": ["text", "box"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}

_UNAVAILABLE = "Text inside images cannot be recognised with the Claude vision OCR: "

_OCR_INSTRUCTIONS = (
    "You are an OCR engine for figures from math textbooks. List every piece of text printed in this "
    "image: labels, captions, titles, axis labels, numbers and formulas. Return one item per text line "
    "(do not merge separate lines, do not split a line into words). Transcribe the text exactly as "
    "written, in its original language, keeping spaces, punctuation, superscripts (²) and symbols. "
    "For each item give its bounding box as [x0, y0, x1, y1] with coordinates normalised to a "
    "0-1000 grid where (0, 0) is the top-left corner of the image and (1000, 1000) the bottom-right "
    "corner; the box must tightly enclose the glyphs. Return an empty list when the image contains "
    "no text."
)


def parse_vision_ocr_json(data: Any, width: int, height: int) -> list[OcrResult]:
    """Convert the model's ``{"items": [{"text", "box"}]}`` answer to pixel-space results.

    Boxes are ``[x0, y0, x1, y1]`` on a 0-1000 grid. A bare list is accepted
    too. Malformed items are skipped (logged at DEBUG level).
    """
    items = data
    if isinstance(data, dict):
        items = data.get("items")
        if items is None:
            for key in ("results", "texts", "regions", "lines"):
                if isinstance(data.get(key), list):
                    items = data[key]
                    break
    if not isinstance(items, list):
        raise OcrError(f"vision OCR answer is not a list of items: {type(data).__name__}")
    out: list[OcrResult] = []
    sx = width / CLAUDE_COORD_RANGE
    sy = height / CLAUDE_COORD_RANGE
    for item in items:
        if not isinstance(item, dict):
            logger.debug("ignoring non-object OCR item %r", item)
            continue
        raw_text = item.get("text")
        text = raw_text.strip() if isinstance(raw_text, str) else ""
        box = item.get("box")
        try:
            x0, y0, x1, y1 = (float(v) for v in box)
        except (TypeError, ValueError):
            logger.debug("ignoring OCR item with malformed box %r", item)
            continue
        if not text:
            continue
        x0, x1 = sorted((min(max(x0, 0.0), CLAUDE_COORD_RANGE), min(max(x1, 0.0), CLAUDE_COORD_RANGE)))
        y0, y1 = sorted((min(max(y0, 0.0), CLAUDE_COORD_RANGE), min(max(y1, 0.0), CLAUDE_COORD_RANGE)))
        if x1 - x0 < 1e-6 or y1 - y0 < 1e-6:
            logger.debug("ignoring OCR item with empty box %r", item)
            continue
        px0, px1, py0, py1 = x0 * sx, x1 * sx, y0 * sy, y1 * sy
        conf = item.get("confidence", 1.0)
        try:
            conf = min(max(float(conf), 0.0), 1.0)
        except (TypeError, ValueError):
            conf = 1.0
        out.append(OcrResult(text=text, polygon=[[px0, py0], [px1, py0], [px1, py1], [px0, py1]],
                             confidence=conf))
    return out


class ClaudeVisionOcrEngine:
    """OCR through Claude's vision capability with structured JSON output.

    ``client`` may be any object exposing ``messages.create(**kwargs)`` with the
    official SDK's response shape (used by the tests with a fake client). When
    omitted, an ``anthropic.Anthropic`` client is created on first use from
    ``settings.anthropic_api_key`` (or the SDK's own environment lookup).
    """

    name = "claude"

    def __init__(self, client: Any = None, model: Optional[str] = None, settings: Optional[Settings] = None):
        self._settings = settings or get_settings()
        self._client = client
        self.model = model or self._settings.claude_model

    def _get_client(self) -> Any:
        if self._client is None:
            try:
                key = self._settings.anthropic_api_key
                self._client = anthropic.Anthropic(api_key=key) if key else anthropic.Anthropic()
            except Exception as exc:
                raise OcrUnavailableError(
                    f"{_UNAVAILABLE}cannot create the Anthropic client ({exc}); set ANTHROPIC_API_KEY / "
                    f"ANTHROPIC_AUTH_TOKEN or set MATHTRANS_OCR_ENGINE=rapid|none") from exc
        return self._client

    @staticmethod
    def _encode_png(rgb: np.ndarray) -> str:
        from PIL import Image

        pil = Image.fromarray(rgb, "RGB")
        longest = max(pil.size)
        if longest > CLAUDE_MAX_SIDE:
            f = CLAUDE_MAX_SIDE / longest
            pil = pil.resize((max(1, round(pil.width * f)), max(1, round(pil.height * f))), Image.LANCZOS)
        buf = io.BytesIO()
        pil.save(buf, format="PNG", optimize=True)
        return base64.standard_b64encode(buf.getvalue()).decode("ascii")

    def build_request(self, image_rgb: np.ndarray, hint_langs: Optional[list[Lang]] = None) -> dict[str, Any]:
        """The keyword arguments passed to ``client.messages.create``."""
        rgb = as_rgb_uint8(image_rgb)
        prompt = _OCR_INSTRUCTIONS
        codes = _lang_codes(hint_langs)
        if codes:
            names = ", ".join(LANGUAGES[Lang(c)].name_en for c in codes)
            prompt += f" The text is most likely in: {names}."
        return {
            "model": self.model,
            "max_tokens": CLAUDE_MAX_TOKENS,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                 "data": self._encode_png(rgb)}},
                    {"type": "text", "text": prompt},
                ],
            }],
            "output_config": {"format": {"type": "json_schema", "schema": _OCR_SCHEMA}},
        }

    def recognize(self, image_rgb: np.ndarray, hint_langs: Optional[list[Lang]] = None) -> list[OcrResult]:
        rgb = as_rgb_uint8(image_rgb)
        h, w = rgb.shape[:2]
        request = self.build_request(rgb, hint_langs)
        client = self._get_client()
        # Most-specific first. Credential / model / SDK problems affect every image and abort the OCR
        # stage (OcrUnavailableError); everything else is reported for this image only (OcrError).
        try:
            response = client.messages.create(**request)
        except anthropic.AuthenticationError as exc:
            raise OcrUnavailableError(
                f"{_UNAVAILABLE}Anthropic authentication failed (401): check ANTHROPIC_API_KEY / "
                f"ANTHROPIC_AUTH_TOKEN, or set MATHTRANS_OCR_ENGINE=rapid|none (--ocr-engine). {exc}") from exc
        except anthropic.PermissionDeniedError as exc:
            raise OcrUnavailableError(
                f"{_UNAVAILABLE}the Anthropic API key is not allowed to use model {self.model!r} (403): choose "
                f"another MATHTRANS_CLAUDE_MODEL / --model, or set MATHTRANS_OCR_ENGINE=rapid|none. {exc}") from exc
        except anthropic.NotFoundError as exc:
            raise OcrUnavailableError(
                f"{_UNAVAILABLE}model {self.model!r} was not found (404): check MATHTRANS_CLAUDE_MODEL / --model, "
                f"or set MATHTRANS_OCR_ENGINE=rapid|none. {exc}") from exc
        except anthropic.RateLimitError as exc:
            raise OcrError(
                "Claude vision OCR hit the Anthropic rate limit (429) even after the SDK's automatic retries; "
                f"retry later or lower MATHTRANS_MAX_WORKERS. {exc}") from exc
        except anthropic.APIStatusError as exc:
            hint = "retry later" if exc.status_code >= 500 else "check the request / image"
            raise OcrError(
                f"Claude vision OCR request failed with Anthropic API error {exc.status_code} ({hint}): {exc}") from exc
        except anthropic.APIConnectionError as exc:
            raise OcrError(f"Claude vision OCR could not reach the Anthropic API (network/proxy/timeout): {exc}") from exc
        except anthropic.APIError as exc:
            raise OcrError(f"Claude vision OCR request failed: {exc}") from exc
        except TypeError as exc:
            # The SDK raises a bare TypeError when no credential can be resolved at request time, and
            # when an older SDK does not know a request parameter: nothing image-specific about it.
            raise OcrUnavailableError(
                f"{_UNAVAILABLE}the Anthropic SDK rejected the request; set ANTHROPIC_API_KEY / "
                f"ANTHROPIC_AUTH_TOKEN and make sure anthropic >= 1.0 is installed, or set "
                f"MATHTRANS_OCR_ENGINE=rapid|none: {exc}") from exc
        except Exception as exc:
            raise OcrError(f"Claude vision OCR request failed ({type(exc).__name__}): {exc}") from exc
        stop_reason = getattr(response, "stop_reason", None)
        if stop_reason == "refusal":
            logger.warning("Claude declined to read a %dx%d image (stop_reason=refusal); skipping it", w, h)
            return []
        if stop_reason == "max_tokens":
            raise OcrError("Claude vision OCR output was truncated (stop_reason=max_tokens)")
        text = ""
        for block in getattr(response, "content", None) or []:
            if getattr(block, "type", None) == "text":
                text = getattr(block, "text", "") or ""
                break
        if not text.strip():
            raise OcrError("Claude vision OCR returned no text block")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise OcrError(f"Claude vision OCR returned invalid JSON: {exc}") from exc
        results = parse_vision_ocr_json(data, w, h)
        logger.debug("claude OCR: %d regions in %dx%d image", len(results), w, h)
        return results


# --------------------------------------------------------------------------- #
# Null engine + factory
# --------------------------------------------------------------------------- #


class NullOcrEngine:
    """Recognises nothing; text inside images is left untouched."""

    name = "none"

    def recognize(self, image_rgb: np.ndarray, hint_langs: Optional[list[Lang]] = None) -> list[OcrResult]:
        return []


def _is_low_trust_lang(source_lang: Optional[Lang | str]) -> bool:
    if source_lang is None:
        return False
    try:
        return Lang.parse(source_lang) in RAPID_LOW_TRUST_LANGS
    except (ValueError, KeyError):
        return False


def ocr_low_trust(engine: Any, source_lang: Optional[Lang | str]) -> bool:
    """True when ``engine`` is the offline RapidOCR engine and ``source_lang`` is one
    whose script its bundled zh/en models read only partially (Japanese, Korean):
    the recognised text, and therefore what gets painted into the images, may be
    wrong. The pipeline records this on the document so QA can warn about it."""
    return getattr(engine, "name", None) == RapidOcrEngine.name and _is_low_trust_lang(source_lang)


def get_ocr_engine(name: str, settings: Optional[Settings] = None,
                   source_lang: Optional[Lang | str] = None) -> OcrEngine:
    """Build the OCR engine called ``name`` (``auto`` | ``rapid`` | ``claude`` | ``none``).

    ``auto`` prefers the offline RapidOCR engine, then Claude vision when an API
    key is configured, otherwise the null engine - except for a Japanese or
    Korean ``source_lang`` (:data:`RAPID_LOW_TRUST_LANGS`): the bundled RapidOCR
    models read kana / hangul only partially, so Claude vision is preferred
    whenever an API key is available (RapidOCR stays the fallback without one).
    An explicit ``claude`` without credentials degrades the same way (with a
    warning) instead of failing the whole translation job.
    """
    settings = settings or get_settings()
    key = (name or "auto").strip().lower()
    if key == "none":
        return NullOcrEngine()
    if key == "rapid":
        return RapidOcrEngine()
    if key == "claude":
        if settings.has_api_key:
            return ClaudeVisionOcrEngine(settings=settings)
        logger.warning("OCR engine 'claude' requested but no ANTHROPIC_API_KEY is configured; "
                       "falling back to automatic selection")
        key = "auto"
    if key == "auto":
        if _is_low_trust_lang(source_lang) and settings.has_api_key:
            logger.info("OCR engine 'auto': using Claude vision for a %s source (the offline RapidOCR models "
                        "read its script only partially)", Lang.parse(source_lang).value)  # type: ignore[arg-type]
            return ClaudeVisionOcrEngine(settings=settings)
        if RapidOcrEngine.available():
            return RapidOcrEngine()
        if settings.has_api_key:
            return ClaudeVisionOcrEngine(settings=settings)
        logger.warning("no OCR engine available (rapidocr_onnxruntime not installed, no API key); "
                       "text inside images will be kept as is")
        return NullOcrEngine()
    raise ValueError(f"unknown OCR engine {name!r}; expected one of auto, rapid, claude, none")
