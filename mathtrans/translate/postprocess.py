"""Deterministic clean-up of model output before it is used (per target script).

Models occasionally leave source-script punctuation in a Latin-script translation
(``。`` ``，`` ``：``), write invalid English ordinals (``2th``) or double spaces;
these are fixed here rather than sent back through a QA round.
"""
from __future__ import annotations

import re

from ..languages import info
from ..models import Lang

_CJK_PUNCT = {"。": ".", "，": ",", "：": ":", "；": ";", "！": "!", "？": "?", "（": "(", "）": ")",
              "、": ",", "“": '"', "”": '"', "‘": "'", "’": "'", "．": "."}
_CJK_PUNCT_RE = re.compile("[" + "".join(re.escape(c) for c in _CJK_PUNCT) + "]")
_HAN_RE = re.compile(r"[㐀-鿿]")
_ORDINAL_RE = re.compile(r"\b(\d+)(st|nd|rd|th)\b")
_SPACE_BEFORE_PUNCT_RE = re.compile(r" +([,.;:!?)])")
_MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
_EMPTY_BRACKET_RE = re.compile(r"\([ \t\u00a0\u2002\u3000]*\)")
_UNIT_RE = re.compile(r"(?<![\w.⟧])(\d+(?:\.\d+)?)(mm|cm|dm|km|m|kg|g|mL|ml|L)(?=$|[\s.,;:!?)\]²³/])")
"""A number written against its metric unit ("2.4m"): English style sets a space between them."""
ANSWER_BRACKET = "(" + "\u00a0" * 6 + ")"
"""An answer blank in brackets ("（  ）" in the source): room to write, which plain spaces would not
keep - they collapse when the text is set - and which never splits over two lines."""


def english_ordinal_suffix(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def fix_ordinals(text: str) -> str:
    """``1th`` -> ``1st``, ``2th`` -> ``2nd``, ``23th`` -> ``23rd``; ``11th`` stays."""
    return _ORDINAL_RE.sub(lambda m: m.group(1) + english_ordinal_suffix(int(m.group(1))), text)


def latinise_punctuation(text: str) -> str:
    """Full-width CJK punctuation becomes its ASCII counterpart (only called for
    Latin-script targets, and never inside Han text that was deliberately kept)."""
    out: list[str] = []
    for i, ch in enumerate(text):
        rep = _CJK_PUNCT.get(ch)
        if rep is None:
            out.append(ch)
            continue
        prev = text[i - 1] if i else ""
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if _HAN_RE.match(prev) or _HAN_RE.match(nxt):
            out.append(ch)  # punctuation attached to kept Han text (names, tally marks) stays
            continue
        out.append(rep)
        if rep in ".,;:!?" and nxt and nxt not in " \n" and not nxt.isdigit() and nxt not in "⟦)\"'":
            out.append(" ")
    return "".join(out)


def space_units(text: str) -> str:
    """``2.4m`` -> ``2.4 m``, ``500g`` -> ``500 g`` (only metric units right after a number)."""
    return _UNIT_RE.sub("\\1\u00a0\\2", text)


# One spelling throughout the English books: British, as most of the text already is ("metre", "colour").
# A meter that measures (an electricity meter, a thermometer) keeps its spelling; so do perimeter and
# diameter, which are other words.
_BRITISH = [
    (re.compile(r"(?<!electricity )(?<!water )(?<!gas )(?<!parking )\b(kilo|centi|milli|deci|micro)?meter(s?)\b",
                re.I), r"\1metre\2"),
    (re.compile(r"\b(milli|centi|deci)?liter(s?)\b", re.I), r"\1litre\2"),
    (re.compile(r"\bcolor(s|ed|ing|ful|less)?\b", re.I), r"colour\1"),
    (re.compile(r"\bcenter(s?)\b", re.I), r"centre\1"),
    (re.compile(r"\bcentered\b", re.I), "centred"),
    (re.compile(r"\bgray(s|er|ish)?\b", re.I), r"grey\1"),
    (re.compile(r"\bfavorite(s?)\b", re.I), r"favourite\1"),
    (re.compile(r"\banalyz(e|es|ed|ing)\b", re.I), r"analys\1"),
    (re.compile(r"\bmath\b", re.I), "maths"),
]


def british_spelling(text: str) -> str:
    """``The perimeter is 12 meters; color it gray.`` -> ``The perimeter is 12 metres; colour it grey.``
    (the first letter keeps its case)."""
    for pattern, repl in _BRITISH:
        def sub(m: re.Match, repl: str = repl) -> str:
            out = m.expand(repl)
            return out[:1].upper() + out[1:] if m.group(0)[:1].isupper() else out
        text = pattern.sub(sub, text)
    return text


def postprocess_translation(text: str, tgt: Lang | str) -> str:
    """Clean ``text`` for ``tgt``; a no-op for CJK targets apart from whitespace."""
    if not text:
        return text
    lang = Lang.parse(tgt)
    if info(lang).script == "latin":
        text = latinise_punctuation(text)
        text = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)
        text = _EMPTY_BRACKET_RE.sub(ANSWER_BRACKET, text)
        text = space_units(text)
        if lang == Lang.EN:
            text = fix_ordinals(text)
            text = british_spelling(text)
    text = _MULTI_SPACE_RE.sub(" ", text)
    return "\n".join(line.strip() for line in text.split("\n")).strip()


__all__ = ["postprocess_translation", "fix_ordinals", "latinise_punctuation", "english_ordinal_suffix", "space_units",
           "british_spelling"]
