"""Font discovery and text measurement for both PDF (HTML box) and raster (PIL) rendering."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from .languages import LANGUAGES, is_cjk
from .models import Lang

_REPO_FONTS = Path(__file__).resolve().parent.parent / "fonts"
_CACHE_FONTS = Path.home() / ".cache" / "mathtrans" / "fonts"
_SYSTEM_DIRS = [
    Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts",
    Path.home() / ".local/share/fonts", Path("/Library/Fonts"), Path("/System/Library/Fonts"),
    Path("C:/Windows/Fonts"),
]
_EXTS = {".ttf", ".otf", ".ttc"}


def font_search_dirs(extra: Optional[str | Path] = None) -> list[Path]:
    dirs: list[Path] = []
    env = os.environ.get("MATHTRANS_FONTS_DIR")
    for d in [extra, env, _REPO_FONTS, _CACHE_FONTS, *_SYSTEM_DIRS]:
        if d:
            p = Path(d)
            if p.is_dir() and p not in dirs:
                dirs.append(p)
    return dirs


@lru_cache(maxsize=8)
def _font_index(dirs_key: tuple[str, ...]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for d in dirs_key:
        for root, _dirs, files in os.walk(d):
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in _EXTS:
                    index.setdefault(p.stem.lower(), p)
    return index


def find_font_file(lang: Lang | str, bold: bool = False, extra_dir: Optional[str | Path] = None) -> Optional[Path]:
    """Best available font file for ``lang`` (None => rely on PyMuPDF built-ins)."""
    lang = Lang.parse(lang)
    dirs = tuple(str(d) for d in font_search_dirs(extra_dir))
    index = _font_index(dirs)
    candidates = list(LANGUAGES[lang].font_candidates)
    if bold:
        candidates = [c.replace("-Regular", "-Bold") for c in candidates] + candidates
    # generic fallbacks
    if is_cjk(lang):
        candidates += ["NotoSansCJK-Regular", "NotoSansCJKsc-Regular", "wqy-zenhei", "wqy-microhei",
                       "DroidSansFallbackFull", "DroidSansFallback", "NotoSansSC-Regular"]
    else:
        candidates += ["DejaVuSans", "LiberationSans-Regular", "NotoSans-Regular", "Arial", "arial"]
    for c in candidates:
        p = index.get(c.lower())
        if p:
            return p
    return None


def pil_font(lang: Lang | str, size: float, bold: bool = False, extra_dir: Optional[str | Path] = None):
    """A PIL ImageFont able to draw ``lang``; falls back to PIL's default font."""
    from PIL import ImageFont

    size_i = max(6, int(round(size)))
    path = find_font_file(lang, bold=bold, extra_dir=extra_dir)
    if path is not None:
        try:
            return ImageFont.truetype(str(path), size_i)
        except Exception:
            pass
    try:
        return ImageFont.load_default(size=size_i)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


def html_font_setup(lang: Lang | str, extra_dir: Optional[str | Path] = None) -> tuple[str, Optional[object], str]:
    """CSS ``@font-face`` rule, PyMuPDF Archive and family name for ``insert_htmlbox``.

    Returns ``("", None, "sans-serif")`` when no dedicated font file is found, in
    which case PyMuPDF's built-in fonts (Droid Sans Fallback for CJK, Nimbus
    Sans for Latin) are used - they cover all six supported languages.
    """
    import pymupdf

    path = find_font_file(lang, extra_dir=extra_dir)
    if path is None or path.suffix.lower() == ".ttc":
        return "", None, "sans-serif"
    try:
        archive = pymupdf.Archive(str(path.parent))
    except Exception:
        return "", None, "sans-serif"
    family = "mtfont"
    css = f"@font-face {{font-family: {family}; src: url({path.name});}}\n"
    return css, archive, family


@lru_cache(maxsize=16)
def _measure_font(lang: Lang, extra_dir: Optional[str]):
    import pymupdf

    path = find_font_file(lang, extra_dir=extra_dir)
    if path is not None and path.suffix.lower() != ".ttc":
        try:
            return pymupdf.Font(fontfile=str(path))
        except Exception:
            pass
    try:
        return pymupdf.Font("cjk") if is_cjk(lang) else pymupdf.Font("helv")
    except Exception:
        return None


def text_width(text: str, lang: Lang | str, size: float, extra_dir: Optional[str | Path] = None) -> float:
    """Width in points of ``text`` set in the font chosen for ``lang``."""
    lang = Lang.parse(lang)
    font = _measure_font(lang, str(extra_dir) if extra_dir else None)
    if font is not None:
        try:
            return float(font.text_length(text, fontsize=size))
        except Exception:
            pass
    return len(text) * size / LANGUAGES[lang].chars_per_em


def wrap_lines(text: str, lang: Lang | str, size: float, max_width: float,
               extra_dir: Optional[str | Path] = None) -> list[str]:
    """Greedy word/character wrapping using real glyph widths."""
    lang = Lang.parse(lang)
    lines: list[str] = []
    for para in text.split("\n"):
        units = list(para) if is_cjk(lang) else para.split(" ")
        joiner = "" if is_cjk(lang) else " "
        cur = ""
        for u in units:
            cand = u if not cur else cur + joiner + u
            if text_width(cand, lang, size, extra_dir) <= max_width or not cur:
                cur = cand
            else:
                lines.append(cur)
                cur = u
        lines.append(cur)
    return lines


def fit_font_size(text: str, lang: Lang | str, box_w: float, box_h: float, start_size: float,
                  min_size: float = 4.0, line_height: float = 1.25, step: float = 0.5,
                  extra_dir: Optional[str | Path] = None) -> float:
    """Largest font size <= start_size at which ``text`` wraps into the box."""
    size = start_size
    while size >= min_size:
        lines = wrap_lines(text, lang, size, box_w, extra_dir)
        if all(text_width(l, lang, size, extra_dir) <= box_w + 0.01 for l in lines) and \
                len(lines) * size * line_height <= box_h + 0.01:
            return size
        size -= step
    return min_size
