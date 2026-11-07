"""Deterministic offline translator and reviewer.

The mock translator never touches the network. It produces output that *looks*
like a translation to the rule-based QA checks: glossary terms and a built-in
mini dictionary are substituted literally, chapter/page/"在…中" patterns are
rewritten, and whatever source-script text remains is replaced by deterministic
pseudo-words in the target script (hash-seeded, so the same input always yields
the same output). Placeholders ``⟦n⟧`` and list markers are kept in place and
terminal punctuation is converted to the target language's convention.

Fault flags (``drop_placeholders``, ``leave_untranslated``, ``truncate``,
``wrong_numbers``) corrupt the *first* translation of each item id only, so a
QA loop that re-translates flagged segments converges on the second attempt.

Line breaks and list markers (``1.``, ``(a)``, ``①``, ``一、`` ...) are kept so
that the formatting QA check passes; a Chinese-numeral marker becomes ``1.``
for Latin-script and Korean targets.
"""
from __future__ import annotations

import hashlib
import logging
import random
import re
import threading
from functools import lru_cache
from typing import Union

from ..languages import LANGUAGES, is_cjk
from ..models import (PLACEHOLDER_RE, Lang, ReviewFinding, ReviewItem, TranslationItem,
                      TranslationResult)
from .base import BaseTranslator

log = logging.getLogger("mathtrans.translate.mock")

BAD_MARKER = "[[BAD]]"
"""Translations containing this marker are reported as errors by :class:`MockReviewer`."""

# --------------------------------------------------------------------------- #
# Mini dictionary: one row per concept, columns zh / en / pt / es / ja / ko.
# An empty cell means "drop the word" in that language (function words such as
# 的). The first row that defines a source term wins, so put the preferred
# translation of an ambiguous word (e.g. "square") first.
# --------------------------------------------------------------------------- #

_COLUMNS = ("zh", "en", "pt", "es", "ja", "ko")

_TABLE: tuple[tuple[str, str, str, str, str, str], ...] = (
    ("勾股定理", "Pythagorean theorem", "teorema de Pitágoras", "teorema de Pitágoras", "三平方の定理", "피타고라스 정리"),
    ("直角三角形", "right triangle", "triângulo retângulo", "triángulo rectángulo", "直角三角形", "직각삼각형"),
    ("等腰三角形", "isosceles triangle", "triângulo isósceles", "triángulo isósceles", "二等辺三角形", "이등변삼각형"),
    ("三角形", "triangle", "triângulo", "triángulo", "三角形", "삼각형"),
    ("大正方形", "large square", "quadrado grande", "cuadrado grande", "大きな正方形", "큰 정사각형"),
    ("小正方形", "small square", "quadrado pequeno", "cuadrado pequeño", "小さな正方形", "작은 정사각형"),
    ("正方形", "square", "quadrado", "cuadrado", "正方形", "정사각형"),
    ("两条直角边", "the two legs", "os dois catetos", "los dos catetos", "直角をはさむ二辺", "두 변"),
    ("斜边", "hypotenuse", "hipotenusa", "hipotenusa", "斜辺", "빗변"),
    ("直角边", "leg", "cateto", "cateto", "直角をはさむ辺", "직각을 낀 변"),
    ("直角", "right angle", "ângulo reto", "ángulo recto", "直角", "직각"),
    ("边长", "side length", "comprimento do lado", "longitud del lado", "辺の長さ", "변의 길이"),
    ("长度", "length", "comprimento", "longitud", "長さ", "길이"),
    ("平方和", "sum of the squares", "soma dos quadrados", "suma de los cuadrados", "平方の和", "제곱의 합"),
    ("平方", "square", "quadrado", "cuadrado", "平方", "제곱"),
    ("面积关系", "area relation", "relação de áreas", "relación de áreas", "面積の関係", "넓이의 관계"),
    ("面积", "area", "área", "área", "面積", "넓이"),
    ("等于", "equals", "é igual a", "es igual a", "に等しい", "과 같다"),
    ("相等", "equal", "iguais", "iguales", "等しい", "같다"),
    ("求", "find", "calcule", "calcula", "求めよ", "구하시오"),
    ("已知", "given", "dado", "dado", "与えられた", "주어진"),
    ("解", "solution", "solução", "solución", "解", "풀이"),
    ("例题", "example", "exemplo", "ejemplo", "例題", "예제"),
    ("练习", "exercises", "exercícios", "ejercicios", "練習", "연습"),
    ("定理", "theorem", "teorema", "teorema", "定理", "정리"),
    ("证明", "prove", "demonstre", "demuestra", "証明しなさい", "증명하시오"),
    ("判断", "decide", "decida", "decide", "判断せよ", "판단하시오"),
    ("思考", "think", "pense", "piensa", "考えよう", "생각해 보기"),
    ("如图所示", "as shown in the figure", "como mostra a figura", "como muestra la figura", "図のように", "그림과 같이"),
    ("分别为", "are respectively", "são respectivamente", "son respectivamente", "それぞれ", "각각"),
    ("那么", "then", "então", "entonces", "すると", "그러면"),
    ("这就是", "this is", "este é", "este es", "これが", "이것이"),
    ("著名的", "the famous", "o famoso", "el famoso", "有名な", "유명한"),
    ("两条", "two", "dois", "dos", "二つの", "두"),
    ("四个", "four", "quatro", "cuatro", "四つの", "네 개의"),
    ("另一条", "the other", "o outro", "el otro", "もう一つの", "다른"),
    ("一个", "a", "um", "un", "一つの", "한"),
    ("一条", "one", "um", "un", "一つの", "한"),
    ("全等的", "congruent", "congruentes", "congruentes", "合同な", "합동인"),
    ("可以拼成", "can form", "podem formar", "pueden formar", "を作ることができ", "만들 수 있다"),
    ("中间", "in the middle", "no centro", "en el centro", "中央に", "가운데에"),
    ("留下", "leaves", "deixa", "deja", "残る", "남는다"),
    ("请利用", "use", "use", "usa", "を使って", "을 이용하여"),
    ("利用", "using", "usando", "usando", "を使って", "을 이용하여"),
    ("探索", "exploring", "explorando", "explorando", "を調べよう", "탐구"),
    ("图形", "figure", "figura", "figura", "図形", "도형"),
    ("图", "figure", "figura", "figura", "図", "그림"),
    ("计算", "calculate", "calcule", "calcula", "計算せよ", "계산하시오"),
    ("方程", "equation", "equação", "ecuación", "方程式", "방정식"),
    ("函数", "function", "função", "función", "関数", "함수"),
    ("因为", "because", "porque", "porque", "なぜなら", "왜냐하면"),
    ("因此", "therefore", "portanto", "por lo tanto", "したがって", "따라서"),
    ("所以", "so", "logo", "así que", "よって", "따라서"),
    ("如果", "if", "se", "si", "もし", "만약"),
    ("其中", "where", "onde", "donde", "ここで", "여기서"),
    ("是", "is", "é", "es", "である", "이다"),
    ("为", "is", "é", "es", "は", "는"),
    ("和", "and", "e", "y", "と", "와"),
    ("在", "in", "em", "en", "では", "에서"),
    ("由", "by", "pelo", "por", "より", "에 의해"),
    ("得", "we get", "obtemos", "obtenemos", "", "얻는다"),
    ("用", "with", "com", "con", "で", "로"),
    ("设", "let", "seja", "sea", "とする", "라 하자"),
    ("则", "then", "então", "entonces", "すると", "그러면"),
    ("若", "if", "se", "si", "もし", "만약"),
    ("长", "length", "comprimento", "longitud", "長さ", "길이"),
    ("边", "side", "lado", "lado", "辺", "변"),
    ("角", "angle", "ângulo", "ángulo", "角", "각"),
    ("数", "number", "número", "número", "数", "수"),
    ("点", "point", "ponto", "punto", "点", "점"),
    ("线", "line", "linha", "línea", "線", "선"),
    ("页", "page", "página", "página", "ページ", "쪽"),
    ("章", "chapter", "capítulo", "capítulo", "章", "장"),
    ("的", "", "", "", "の", "의"),
    ("中", "", "", "", "", ""),
    ("吗", "", "", "", "か", "인가"),
    ("个", "", "", "", "個の", "개의"),
    ("条", "", "", "", "本の", ""),
    ("请", "", "", "", "", ""),
)


def _build_dictionary(src: str, tgt: str) -> list[tuple[str, str]]:
    si, ti = _COLUMNS.index(src), _COLUMNS.index(tgt)
    seen: dict[str, str] = {}
    for row in _TABLE:
        s, t = row[si], row[ti]
        if s and s not in seen:
            seen[s] = t
    return sorted(seen.items(), key=lambda p: (-len(p[0]), p[0]))


_DICTIONARIES: dict[tuple[str, str], list[tuple[str, str]]] = {
    (s, t): _build_dictionary(s, t) for s in _COLUMNS for t in _COLUMNS if s != t
}


def mini_dictionary(src: Lang | str, tgt: Lang | str) -> list[tuple[str, str]]:
    """Built-in (source term, target term) pairs for a language pair, longest first."""
    return list(_DICTIONARIES[(Lang.parse(src).value, Lang.parse(tgt).value)])


# --------------------------------------------------------------------------- #
# Pattern rules (chapter / page numbering, "在…中"). A template is a list of
# parts: a str is emitted verbatim, an int inserts the matched group as source
# text that still gets translated, ("num", n) inserts the group converted to a
# Western numeral.
# --------------------------------------------------------------------------- #

TemplatePart = Union[str, int, tuple[str, int]]

_CN_NUM = r"(?:[一二三四五六七八九十百零〇\d]+|⟦\d+⟧)"
_LAT_NUM = r"(?:\d+|⟦\d+⟧)"

_PATTERNS: dict[str, list[tuple[re.Pattern[str], dict[str, list[TemplatePart]]]]] = {
    "zh": [
        (re.compile(rf"第\s*({_CN_NUM})\s*章"), {
            "en": ["Chapter ", ("num", 1)], "es": ["Capítulo ", ("num", 1)], "pt": ["Capítulo ", ("num", 1)],
            "ja": ["第", ("num", 1), "章"], "ko": ["제", ("num", 1), "장"],
        }),
        (re.compile(rf"第\s*({_CN_NUM})\s*页"), {
            "en": ["Page ", ("num", 1)], "es": ["Página ", ("num", 1)], "pt": ["Página ", ("num", 1)],
            "ja": [("num", 1), " ページ"], "ko": [("num", 1), "쪽"],
        }),
        (re.compile(r"在([^，。；：！？\n]{1,16}?)中(?=[，,])"), {
            "en": ["In ", 1], "es": ["En ", 1], "pt": ["Em ", 1], "ja": [1, "では"], "ko": [1, "에서"],
        }),
    ],
    "en": [
        (re.compile(rf"\bChapter\s+({_LAT_NUM})", re.IGNORECASE), {
            "zh": ["第", ("num", 1), "章"], "ja": ["第", ("num", 1), "章"], "ko": ["제", ("num", 1), "장"],
            "es": ["Capítulo ", ("num", 1)], "pt": ["Capítulo ", ("num", 1)],
        }),
        (re.compile(rf"\bPage\s+({_LAT_NUM})", re.IGNORECASE), {
            "zh": ["第", ("num", 1), "页"], "ja": [("num", 1), " ページ"], "ko": [("num", 1), "쪽"],
            "es": ["Página ", ("num", 1)], "pt": ["Página ", ("num", 1)],
        }),
    ],
    "ja": [
        (re.compile(rf"第\s*({_CN_NUM})\s*章"), {
            "en": ["Chapter ", ("num", 1)], "es": ["Capítulo ", ("num", 1)], "pt": ["Capítulo ", ("num", 1)],
            "zh": ["第", ("num", 1), "章"], "ko": ["제", ("num", 1), "장"],
        }),
    ],
    "ko": [
        (re.compile(rf"제\s*({_LAT_NUM})\s*장"), {
            "en": ["Chapter ", ("num", 1)], "es": ["Capítulo ", ("num", 1)], "pt": ["Capítulo ", ("num", 1)],
            "zh": ["第", ("num", 1), "章"], "ja": ["第", ("num", 1), "章"],
        }),
    ],
}

_CN_DIGITS = {"零": 0, "〇": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def chinese_numeral_to_int(text: str) -> str:
    """``一`` → ``1``, ``二十三`` → ``23``, ``一百零五`` → ``105``; digits and placeholders pass through."""
    t = text.strip()
    if not t or t.isdigit() or PLACEHOLDER_RE.fullmatch(t):
        return t
    if any(ch not in _CN_DIGITS and ch not in "十百" for ch in t):
        return t
    total = 0
    current = 0
    for ch in t:
        if ch == "百":
            total += (current or 1) * 100
            current = 0
        elif ch == "十":
            total += (current or 1) * 10
            current = 0
        else:
            current = _CN_DIGITS[ch]
    return str(total + current)


# --------------------------------------------------------------------------- #
# Pseudo-words per target language (used for source text no rule covers)
# --------------------------------------------------------------------------- #

_WORDS: dict[str, tuple[str, ...]] = {
    "en": ("the", "of", "and", "with", "this", "that", "each", "which", "number", "value", "side",
           "line", "point", "figure", "shown", "below", "find", "using", "these", "equal", "then",
           "also", "from", "into", "given", "where", "there", "between", "called", "whole", "part"),
    "es": ("el", "la", "de", "con", "este", "que", "cada", "número", "valor", "lado", "línea",
           "punto", "figura", "dado", "entonces", "también", "desde", "entre", "llamado", "parte",
           "según", "igual", "usando", "donde", "hay", "los", "las", "para", "como", "por"),
    "pt": ("o", "a", "de", "com", "este", "que", "cada", "número", "valor", "lado", "linha",
           "ponto", "figura", "dado", "então", "também", "desde", "entre", "chamado", "parte",
           "segundo", "igual", "usando", "onde", "há", "os", "as", "para", "como", "por"),
    "zh": ("的", "是", "在", "和", "与", "为", "有", "这", "那", "其", "两", "个", "条", "边", "角",
           "形", "数", "值", "点", "线", "图", "题", "求", "得", "则", "所以", "因为", "如果", "可以",
           "我们", "一个", "这个", "关系", "问题"),
    "ja": ("の", "は", "が", "を", "に", "で", "と", "も", "です", "ます", "こと", "もの", "この",
           "その", "また", "よって", "ゆえに", "とき", "なら", "から", "まで", "辺", "角", "図", "数",
           "値", "点", "線", "形", "求め", "考え", "ように"),
    "ko": ("의", "는", "은", "이", "가", "를", "을", "에", "와", "과", "로", "하다", "이다", "것",
           "그", "이것", "또한", "따라서", "때", "면", "부터", "까지", "변", "각", "그림", "수", "값",
           "점", "선", "형", "구하", "생각", "같이"),
}

_SCRIPT_RUN: dict[str, re.Pattern[str]] = {
    "han": re.compile(r"[一-鿿㐀-䶿豈-﫿]+"),
    "kana_han": re.compile(r"[一-鿿㐀-䶿豈-﫿ぁ-ゟ゠-ヿｦ-ﾟ]+"),
    "hangul": re.compile(r"[가-힯ᄀ-ᇿ㄰-㆏一-鿿]+"),
    "latin": re.compile(r"[A-Za-zÀ-ɏ]+"),
}

_LIST_MARKER_RE = re.compile(
    r"^\s*(?:"
    r"(?:⟦\d+⟧|\d{1,3}|[A-Za-z]|[ivxIVX]{1,6}|[①-⑳⑴-⒇⒈-⒛])[.)．、）]"  # 1.  ⟦0⟧.  a)  iv.  ①.
    r"|[(（](?:⟦\d+⟧|\d{1,3}|[A-Za-z]|[ivxIVX]{1,6})[)）]"               # (1)  (a)  （⟦0⟧）
    r"|(?P<cjk>[一二三四五六七八九十]{1,3})[、.．]"                       # 一、  十二、
    r"|[①-⑳⑴-⒇⒈-⒛㈠-㈩⓵-⓾•·▪◦‣■□●○◆◇★☆※▶►➢✓*]"                      # ① •
    r"|[-–—](?=\s)"                                                      # - item
    r")\s*"
)


def _translate_marker(marker: str, match: re.Match[str], tgt: str) -> str:
    """List marker for the target language: a Chinese-numeral marker (``一、``)
    becomes ``1.`` for Latin-script and Korean targets, everything else is kept."""
    core = match.group("cjk")
    if core and tgt in _SPACED:
        return f"{chinese_numeral_to_int(core)}. "
    return marker

_CJK_CHAR = r"[一-鿿㐀-䶿ぁ-ゟ゠-ヿ가-힯]"
_CJK_SPACE_RE = re.compile(rf"(?<={_CJK_CHAR}) +(?={_CJK_CHAR})")

_TO_LATIN_PUNCT = {
    "。": ". ", "，": ", ", "、": ", ", "：": ": ", "；": "; ", "？": "? ", "！": "! ",
    "（": " (", "）": ") ", "“": '"', "”": '"', "‘": "'", "’": "'", "《": '"', "》": '"',
    "「": '"', "」": '"', "．": ".",
}
_LATIN_TO_CJK = [
    (re.compile(r"(?<![\d.])\.(?=\s|$)"), "。"),
    (re.compile(r"(?<!\d),\s*"), "，"),
    (re.compile(r":\s+"), "："),
    (re.compile(r";\s*"), "；"),
    (re.compile(r"\?"), "？"),
    (re.compile(r"!"), "！"),
]
_PUNCT_STYLE = {"zh": "cjk", "ja": "ja", "ko": "latin", "en": "latin", "es": "latin", "pt": "latin"}
_JA_QUESTION_END_RE = re.compile(r"(か|かな|かしら)。(?=\s|$)")
"""Textbook Japanese ends a question with か。 (no ？): other languages need the question mark."""
_SPACED = frozenset({"en", "es", "pt", "ko"})
"""Languages that separate words with spaces (Korean does, Chinese and Japanese do not)."""


def _pseudo_words(run: str, tgt: str, target_len: float) -> str:
    """Deterministic pseudo-text in the script of ``tgt`` roughly ``target_len`` characters long."""
    seed = int(hashlib.md5(f"{tgt}|{run}".encode("utf-8")).hexdigest()[:16], 16)
    rng = random.Random(seed)
    words = _WORDS[tgt]
    sep = " " if tgt in _SPACED else ""
    out: list[str] = [rng.choice(words)]
    while len(sep.join(out)) < target_len:
        out.append(rng.choice(words))
    return sep.join(out)


# --------------------------------------------------------------------------- #
# Piece-based rewriting: ("src", text) still needs translating, ("fixed", text) is done.
# --------------------------------------------------------------------------- #

Piece = tuple[str, str]


def _expand_template(template: list[TemplatePart], match: re.Match[str]) -> list[Piece]:
    """Instantiate a template; adjacent fixed parts are merged so that no word
    spacing is inserted between them later (``제`` + ``1`` + ``장`` -> ``제1장``)."""
    pieces: list[Piece] = []
    for part in template:
        if isinstance(part, int):
            pieces.append(("src", match.group(part)))
            continue
        text = part if isinstance(part, str) else chinese_numeral_to_int(match.group(part[1]))
        if pieces and pieces[-1][0] == "fixed":
            pieces[-1] = ("fixed", pieces[-1][1] + text)
        else:
            pieces.append(("fixed", text))
    return pieces


def _apply_patterns(pieces: list[Piece], src: str, tgt: str) -> list[Piece]:
    for regex, templates in _PATTERNS.get(src, []):
        template = templates.get(tgt)
        if template is None:
            continue
        out: list[Piece] = []
        for kind, text in pieces:
            if kind != "src":
                out.append((kind, text))
                continue
            pos = 0
            for m in regex.finditer(text):
                if m.start() > pos:
                    out.append(("src", text[pos:m.start()]))
                out.extend(_expand_template(template, m))
                pos = m.end()
            if pos < len(text):
                out.append(("src", text[pos:]))
        pieces = out
    return pieces


_LATIN_PLURAL = r"(?:s|es)?"
"""Optional plural ending tolerated after each word of a Latin-script term (the
glossary QA check expects ``leg`` to be translated in ``the two legs`` too)."""


@lru_cache(maxsize=None)
def _term_regex(term: str, src_is_cjk: bool) -> re.Pattern[str]:
    if src_is_cjk:
        return re.compile(re.escape(term))
    words = r"\s+".join(re.escape(w) + _LATIN_PLURAL for w in term.split())
    return re.compile(rf"(?<![A-Za-zÀ-ɏ]){words}(?![A-Za-zÀ-ɏ])", re.IGNORECASE)


def _apply_terms(pieces: list[Piece], pairs: list[tuple[str, str]], src_is_cjk: bool) -> list[Piece]:
    for term, replacement in pairs:
        if not term:
            continue
        regex = _term_regex(term, src_is_cjk)
        out: list[Piece] = []
        for kind, text in pieces:
            if kind != "src":
                out.append((kind, text))
                continue
            pos = 0
            for m in regex.finditer(text):
                if m.start() > pos:
                    out.append(("src", text[pos:m.start()]))
                out.append(("fixed", replacement))
                pos = m.end()
            if pos < len(text):
                out.append(("src", text[pos:]))
        pieces = out
    return pieces


def _pseudo_translate(pieces: list[Piece], src: str, tgt: str, ratio: float) -> list[Piece]:
    run_re = _SCRIPT_RUN[LANGUAGES[Lang(src)].script]
    out: list[Piece] = []
    for kind, text in pieces:
        if kind != "src":
            out.append((kind, text))
            continue
        pos = 0
        for m in run_re.finditer(text):
            if m.start() > pos:
                out.append(("fixed", text[pos:m.start()]))
            run = m.group(0)
            out.append(("fixed", _pseudo_words(run, tgt, max(1.0, len(run) * ratio))))
            pos = m.end()
        if pos < len(text):
            out.append(("fixed", text[pos:]))
    return out


def _join(pieces: list[Piece], tgt: str) -> str:
    """Concatenate pieces; spaced targets get a space between adjacent words."""
    spaced = tgt in _SPACED
    parts: list[str] = []
    for _kind, text in pieces:
        if not text:
            continue
        if spaced and parts:
            prev = parts[-1][-1]
            nxt = text[0]
            if (prev.isalnum() or prev in "⟧)") and (nxt.isalnum() or nxt in "⟦("):
                parts.append(" ")
        parts.append(text)
    return "".join(parts)


def _convert_punctuation(text: str, tgt: str) -> str:
    style = _PUNCT_STYLE[tgt]
    chunks = PLACEHOLDER_RE.split(text)  # odd indices are placeholder numbers
    out: list[str] = []
    for i, chunk in enumerate(chunks):
        if i % 2 == 1:
            out.append(f"⟦{chunk}⟧")
            continue
        if style == "latin":
            for cjk, lat in _TO_LATIN_PUNCT.items():
                chunk = chunk.replace(cjk, lat)
        else:
            for regex, repl in _LATIN_TO_CJK:
                chunk = regex.sub(repl, chunk)
            chunk = chunk.replace("、", "，").replace("．", "。")
            if style == "ja":
                chunk = chunk.replace("，", "、")
        out.append(chunk)
    return "".join(out)


def _tidy_spacing(text: str, src: str, tgt: str) -> str:
    """Normalise horizontal spacing for the target language; line breaks are kept
    (QA requires the translation to have the same number of lines as the source)."""
    if tgt in _SPACED:
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r" +(?=[.,:;?!)])", "", text)
        text = re.sub(r"\( +", "(", text)
    else:
        if src in _SPACED:  # word spaces of the source do not belong in zh / ja text
            text = _CJK_SPACE_RE.sub("", text)
        text = re.sub(r"[ \t]+(?=[。，、：；？！])", "", text)
        text = re.sub(r"(?<=[。，、：；？！])[ \t]+(?=\S)", "", text)
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    return text.strip()


_SENTENCE_START_RE = re.compile(r"(^[^A-Za-zÀ-ɏ]*|[.?!]\s+)([a-zà-ɏ])")


def _capitalise(text: str) -> str:
    return _SENTENCE_START_RE.sub(lambda m: m.group(1) + m.group(2).upper(), text)


def pseudo_translate_text(
    text: str,
    src: Lang | str,
    tgt: Lang | str,
    glossary_pairs: list[tuple[str, str]] | None = None,
    max_chars: int | None = None,
) -> str:
    """Translate one protected text deterministically (the core of :class:`MockTranslator`)."""
    src_code, tgt_code = Lang.parse(src).value, Lang.parse(tgt).value
    if src_code == tgt_code:
        return text
    marker_match = _LIST_MARKER_RE.match(text)
    marker = marker_match.group(0) if marker_match else ""
    body = text[len(marker):]
    if not body.strip():
        return text
    if marker_match is not None:
        marker = _translate_marker(marker, marker_match, tgt_code)

    ratio = LANGUAGES[Lang(tgt_code)].length_vs_zh / LANGUAGES[Lang(src_code)].length_vs_zh
    if max_chars is not None and max_chars > 0:
        expected = len(body) * ratio
        if expected > max_chars:
            ratio *= max(0.3, max_chars / expected)

    if src_code == "ja":  # a か。 question keeps its question mark in every other language
        body = _JA_QUESTION_END_RE.sub(r"\1？", body)
    src_cjk = is_cjk(src_code)
    pieces: list[Piece] = [("src", body)]
    pieces = _apply_patterns(pieces, src_code, tgt_code)
    pieces = _apply_terms(pieces, glossary_pairs or [], src_cjk)
    pieces = _apply_terms(pieces, _DICTIONARIES[(src_code, tgt_code)], src_cjk)
    pieces = _pseudo_translate(pieces, src_code, tgt_code, ratio)
    out = _join(pieces, tgt_code)
    out = _convert_punctuation(out, tgt_code)
    out = _tidy_spacing(out, src_code, tgt_code)
    if not is_cjk(tgt_code):
        out = _capitalise(out)
    return marker + out


class MockTranslator(BaseTranslator):
    """Offline, deterministic translator for tests and key-less environments.

    Fault flags corrupt the first translation of each item id only (ids are
    remembered in ``seen_ids``), so a QA loop can observe a defect and see it
    fixed by the re-translation:

    * ``drop_placeholders`` removes the first ``⟦n⟧`` placeholder;
    * ``leave_untranslated`` returns the source text unchanged;
    * ``truncate`` keeps only the first 40 % of the translation;
    * ``wrong_numbers`` bumps every digit written outside placeholders by one
      or, when there is none (numbers are normally protected), glues a spurious
      ``9`` in front of every placeholder so that a protected number such as
      ``3 cm`` comes back as ``93 cm``. The placeholders themselves stay
      intact, so only the ``numbers`` QA check fires.
    """

    name = "mock"

    def __init__(
        self,
        *,
        drop_placeholders: bool = False,
        leave_untranslated: bool = False,
        truncate: bool = False,
        wrong_numbers: bool = False,
    ) -> None:
        self.drop_placeholders = drop_placeholders
        self.leave_untranslated = leave_untranslated
        self.truncate = truncate
        self.wrong_numbers = wrong_numbers
        self.seen_ids: set[str] = set()
        self._lock = threading.Lock()  # one instance may serve several pipeline threads

    @property
    def has_faults(self) -> bool:
        return self.drop_placeholders or self.leave_untranslated or self.truncate or self.wrong_numbers

    def reset(self) -> None:
        """Forget which ids were seen (fault flags apply to the next attempt again)."""
        with self._lock:
            self.seen_ids.clear()

    def _first_attempt(self, item_id: str) -> bool:
        with self._lock:
            first = item_id not in self.seen_ids
            self.seen_ids.add(item_id)
            return first

    def translate(
        self,
        items: list[TranslationItem],
        src: Lang,
        tgt: Lang,
        glossary_pairs: list[tuple[str, str]],
        doc_context: str = "",
    ) -> list[TranslationResult]:
        src, tgt = Lang.parse(src), Lang.parse(tgt)
        results: list[TranslationResult] = []
        for item in items:
            first_attempt = self._first_attempt(item.id)
            text = pseudo_translate_text(item.text, src, tgt, glossary_pairs, item.max_chars)
            if first_attempt and self.has_faults:
                text = self._inject_faults(item, text)
            results.append(TranslationResult(id=item.id, text=text))
        log.debug("mock translated %d items %s->%s", len(items), src.value, tgt.value)
        return results

    def _inject_faults(self, item: TranslationItem, text: str) -> str:
        if self.leave_untranslated:
            text = item.text
        if self.drop_placeholders:
            text = re.sub(r"  +", " ", PLACEHOLDER_RE.sub("", text, count=1)).strip()
        if self.wrong_numbers:
            text = self._corrupt_numbers(text)
        if self.truncate:
            text = text[: max(1, (len(text) * 2) // 5)].rstrip()
        log.debug("mock fault injected for %s: %r", item.id, text)
        return text

    @staticmethod
    def _corrupt_numbers(text: str) -> str:
        changed = False

        def bump(m: re.Match[str]) -> str:
            nonlocal changed
            tok = m.group(0)
            if tok.startswith("⟦"):
                return tok
            changed = True
            return str((int(tok) + 1) % 10)

        out = re.sub(r"⟦\d+⟧|\d", bump, text)
        if not changed:
            out = PLACEHOLDER_RE.sub(lambda m: "9" + m.group(0), text)
        return out


class MockReviewer:
    """Reviewer stand-in: flags translations containing ``[[BAD]]`` and nothing else."""

    name = "mock"

    def review(
        self,
        items: list[ReviewItem],
        src: Lang,
        tgt: Lang,
        glossary_pairs: list[tuple[str, str]],
    ) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []
        for item in items:
            if BAD_MARKER in item.translation:
                findings.append(ReviewFinding(
                    id=item.id,
                    severity="error",
                    category="meaning",
                    message=f"translation contains the {BAD_MARKER} marker",
                    suggested_fix=item.translation.replace(BAD_MARKER, "").strip() or None,
                ))
        return findings
