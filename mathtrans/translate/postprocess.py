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


def postprocess_translation(text: str, tgt: Lang | str) -> str:
    """Clean ``text`` for ``tgt``; a no-op for CJK targets apart from whitespace."""
    if not text:
        return text
    lang = Lang.parse(tgt)
    if info(lang).script == "latin":
        text = latinise_punctuation(text)
        text = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)
        if lang == Lang.EN:
            text = fix_ordinals(text)
    text = _MULTI_SPACE_RE.sub(" ", text)
    return "\n".join(line.strip() for line in text.split("\n")).strip()


__all__ = ["postprocess_translation", "fix_ordinals", "latinise_punctuation", "english_ordinal_suffix"]
