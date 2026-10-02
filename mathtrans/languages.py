"""Language table, script statistics and lightweight language detection."""
from __future__ import annotations

import re
import unicodedata
from typing import Literal, Optional

from pydantic import BaseModel

from .models import Lang

Script = Literal["han", "kana_han", "hangul", "latin"]


class LanguageInfo(BaseModel):
    code: Lang
    name_en: str
    name_native: str
    script: Script
    # Typical text-length ratio relative to Chinese for the same content (used by the
    # length-ratio QA check and for fitting hints). Rough, deliberately generous.
    length_vs_zh: float
    # Font family hints: CSS family used by the HTML layout engine and candidate TTF
    # file name stems for PIL drawing, in priority order.
    css_family: str
    font_candidates: list[str]
    # Characters per em (approx.) for width estimation when no font metrics are available.
    chars_per_em: float


LANGUAGES: dict[Lang, LanguageInfo] = {
    Lang.ZH: LanguageInfo(
        code=Lang.ZH, name_en="Chinese (Simplified)", name_native="中文", script="han",
        length_vs_zh=1.0, css_family="sans-serif",
        font_candidates=["NotoSansSC-Regular", "NotoSansCJKsc-Regular", "SourceHanSansSC-Regular",
                         "wqy-microhei", "wqy-zenhei", "DroidSansFallbackFull", "DroidSansFallback"],
        chars_per_em=1.0),
    Lang.EN: LanguageInfo(
        code=Lang.EN, name_en="English", name_native="English", script="latin",
        length_vs_zh=2.6, css_family="sans-serif",
        font_candidates=["NotoSans-Regular", "DejaVuSans", "LiberationSans-Regular", "Arial"],
        chars_per_em=2.0),
    Lang.PT: LanguageInfo(
        code=Lang.PT, name_en="Portuguese", name_native="Português", script="latin",
        length_vs_zh=2.9, css_family="sans-serif",
        font_candidates=["NotoSans-Regular", "DejaVuSans", "LiberationSans-Regular", "Arial"],
        chars_per_em=2.0),
    Lang.ES: LanguageInfo(
        code=Lang.ES, name_en="Spanish", name_native="Español", script="latin",
        length_vs_zh=2.9, css_family="sans-serif",
        font_candidates=["NotoSans-Regular", "DejaVuSans", "LiberationSans-Regular", "Arial"],
        chars_per_em=2.0),
    Lang.JA: LanguageInfo(
        code=Lang.JA, name_en="Japanese", name_native="日本語", script="kana_han",
        length_vs_zh=1.5, css_family="sans-serif",
        font_candidates=["NotoSansJP-Regular", "NotoSansCJKjp-Regular", "SourceHanSansJP-Regular",
                         "wqy-zenhei", "DroidSansFallbackFull", "DroidSansFallback"],
        chars_per_em=1.0),
    Lang.KO: LanguageInfo(
        code=Lang.KO, name_en="Korean", name_native="한국어", script="hangul",
        length_vs_zh=1.4, css_family="sans-serif",
        font_candidates=["NotoSansKR-Regular", "NotoSansCJKkr-Regular", "SourceHanSansKR-Regular",
                         "NanumGothic", "wqy-zenhei", "DroidSansFallbackFull", "DroidSansFallback"],
        chars_per_em=1.1),
}


def info(lang: Lang | str) -> LanguageInfo:
    return LANGUAGES[Lang.parse(lang)]


def is_cjk(lang: Lang | str) -> bool:
    return info(lang).script in ("han", "kana_han", "hangul")


def language_choices() -> list[dict[str, str]]:
    return [{"code": li.code.value, "name": li.name_en, "native": li.name_native} for li in LANGUAGES.values()]


# --------------------------------------------------------------------------- #
# Script statistics
# --------------------------------------------------------------------------- #

_HAN = re.compile(r"[一-鿿㐀-䶿豈-﫿]")
_KANA = re.compile(r"[ぁ-ゟ゠-ヿｦ-ﾟ]")
_HANGUL = re.compile(r"[가-힯ᄀ-ᇿ㄰-㆏]")
_LATIN = re.compile(r"[A-Za-zÀ-ɏ]")
_DIGIT = re.compile(r"[0-9]")
_GREEK = re.compile(r"[Α-ω]")


def script_profile(text: str) -> dict[str, int]:
    """Counts of characters per script family."""
    return {
        "han": len(_HAN.findall(text)),
        "kana": len(_KANA.findall(text)),
        "hangul": len(_HANGUL.findall(text)),
        "latin": len(_LATIN.findall(text)),
        "digit": len(_DIGIT.findall(text)),
        "greek": len(_GREEK.findall(text)),
        "total": sum(1 for c in text if not c.isspace()),
    }


def letters_of_script(text: str, lang: Lang | str) -> int:
    """Number of letters in ``text`` that belong to the main script of ``lang``."""
    p = script_profile(text)
    s = info(lang).script
    if s == "han":
        return p["han"]
    if s == "kana_han":
        return p["han"] + p["kana"]
    if s == "hangul":
        return p["hangul"] + p["han"]  # hanja is tolerated in Korean
    return p["latin"]


def foreign_letters(text: str, lang: Lang | str) -> int:
    """Letters that do *not* belong to the script of ``lang`` (Latin is tolerated
    everywhere because variables, units and names are written in Latin letters)."""
    p = script_profile(text)
    s = info(lang).script
    if s == "han":
        return p["kana"] + p["hangul"]
    if s == "kana_han":
        return p["hangul"]
    if s == "hangul":
        return p["kana"]
    return p["han"] + p["kana"] + p["hangul"]


def script_ratio(text: str, lang: Lang | str) -> float:
    """Share of letters (all scripts) that are in the expected script of ``lang``."""
    p = script_profile(text)
    letters = p["han"] + p["kana"] + p["hangul"] + p["latin"]
    if letters == 0:
        return 1.0
    return letters_of_script(text, lang) / letters


# --------------------------------------------------------------------------- #
# Detection
# --------------------------------------------------------------------------- #

_STOP = {
    Lang.EN: {"the", "and", "of", "to", "in", "is", "that", "for", "it", "as", "with", "be", "on", "are",
              "this", "by", "an", "or", "from", "at", "which", "we", "if", "then", "each", "find", "given",
              "so", "not", "than", "have", "has", "all", "can", "will", "its", "into", "two", "one", "three",
              "such", "let", "where", "when", "there", "what", "how", "many", "number", "area", "triangle"},
    Lang.ES: {"el", "la", "de", "que", "y", "en", "un", "una", "los", "las", "del", "es", "son", "por", "con",
              "para", "como", "se", "no", "al", "lo", "su", "sus", "más", "pero", "este", "esta", "cada",
              "entre", "cuando", "donde", "también", "hay", "sea", "sean", "calcule", "halle", "halla",
              "determine", "cuál", "cuánto", "cuántos", "ejercicio", "ejercicios", "ecuación", "triángulo",
              "área", "número", "números", "siguiente", "siguientes", "entonces", "resuelve", "encuentra"},
    Lang.PT: {"o", "a", "os", "as", "de", "do", "da", "dos", "das", "que", "e", "em", "um", "uma", "para",
              "é", "são", "com", "não", "no", "na", "nos", "nas", "se", "por", "mais", "como", "mas", "ao",
              "à", "seu", "sua", "ou", "quando", "muito", "também", "cada", "entre", "então", "onde",
              "calcule", "determine", "encontre", "qual", "quanto", "quantos", "exercício", "exercícios",
              "equação", "triângulo", "área", "número", "números", "seguinte", "seguintes", "resolva",
              "sendo", "dado", "dados", "assim", "logo", "portanto", "já", "você", "isso", "esse", "essa"},
}

_WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")


def detect_language(text: str) -> Optional[Lang]:
    """Best-effort detection among the six supported languages. Returns None for
    text without letters (e.g. pure numbers)."""
    p = script_profile(text)
    letters = p["han"] + p["kana"] + p["hangul"] + p["latin"]
    if letters == 0:
        return None
    if p["hangul"] > 0 and p["hangul"] >= 0.15 * letters:
        return Lang.KO
    if p["kana"] > 0 and p["kana"] >= 0.05 * letters:
        return Lang.JA
    if p["han"] > 0 and p["han"] >= 0.3 * letters:
        # Han without kana: Chinese (Japanese text normally contains kana).
        return Lang.ZH
    if p["latin"] == 0:
        if p["kana"]:
            return Lang.JA
        if p["hangul"]:
            return Lang.KO
        return Lang.ZH
    low = text.lower()
    words = _WORD_RE.findall(low)
    scores = {lang: 0.0 for lang in (Lang.EN, Lang.ES, Lang.PT)}
    for w in words:
        for lang, stop in _STOP.items():
            if w in stop:
                scores[lang] += 1.0
    # diacritic hints
    scores[Lang.PT] += 2.0 * sum(low.count(c) for c in "ãõç")
    scores[Lang.PT] += 1.0 * (low.count("ê") + low.count("ô"))
    scores[Lang.ES] += 2.0 * sum(low.count(c) for c in "ñ¿¡")
    best = max(scores.items(), key=lambda kv: kv[1])
    if best[1] == 0:
        return Lang.EN
    return best[0]


def normalize_for_compare(text: str) -> str:
    """NFKC-normalise and collapse whitespace; used by QA comparisons."""
    t = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", t).strip()
