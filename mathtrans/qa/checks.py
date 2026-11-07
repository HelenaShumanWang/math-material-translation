"""Rule-based QA checks on a translated document and on the exported PDF.

Every rule check is a plain function ``(doc, options, glossary_pairs) ->
list[QAIssue]`` registered in :data:`CHECKS` under a stable name. Issue messages
are written *for the translator*: the QA loop feeds them back verbatim as
instructions for the next attempt, so each one says what to change ("keep the
number 25", "translate 斜边 as hypotenuse", "shorten to at most 38 characters").

Only segments with ``translate=True`` are examined. ``layout_fit`` looks at the
:class:`~mathtrans.models.RenderInfo` of native text segments, ``image_text`` at
that of text recognised inside raster images; the other checks apply to both
kinds.

:func:`output_checks` works on files instead: it compares the exported PDF with
the source PDF (page count, page sizes, image placement, extractable translated
text, source-script leftovers, embedded fonts).
"""
from __future__ import annotations

import logging
import re
import unicodedata
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Callable, Optional, Union

import pymupdf

from ..glossary import is_enforced_source_term, term_present
from ..languages import LANGUAGES, info, is_cjk, normalize_for_compare, script_profile
from ..languages import letters_of_script as _source_script_letters
from ..models import (ANCHOR_RE, PLACEHOLDER_RE, Lang, PipelineOptions, QAIssue, SegmentKind, Severity, TextSegment,
                      TranslatedDocument)
from ..protect import FUNCTIONS, UNITS, _is_bare_label, is_fully_protected, verify_placeholders

log = logging.getLogger("mathtrans.qa.checks")

GlossaryPairs = list[tuple[str, str]]
CheckFn = Callable[[TranslatedDocument, PipelineOptions, Optional[GlossaryPairs]], list[QAIssue]]

LENGTH_RATIO_MIN = 0.35
"""Lower bound of the accepted translation/source length ratio, as a multiple of the expected ratio."""
LENGTH_RATIO_MAX = 3.0
"""Upper bound of the accepted translation/source length ratio, as a multiple of the expected ratio."""
LENGTH_RATIO_MIN_SOURCE_CHARS = 8
"""Sources shorter than this (translatable characters) are not length-checked."""
TARGET_SCRIPT_MIN_RATIO = 0.6
"""Minimum share of target-script letters among all letters of a translation."""
MIN_LETTERS_FOR_SCRIPT_CHECKS = 4
"""Translations / sources with fewer letters are too short for script statistics."""
TINY_LABEL_MAX_LETTERS = 3
"""Sources with at most this many letters may keep up to :data:`TINY_LABEL_FOREIGN_ALLOWANCE` foreign
letters (a stray unit or variable) - unless the translation is a verbatim copy of the source."""
TINY_LABEL_FOREIGN_ALLOWANCE = 2
COPIED_RUN_MIN_WORDS = 3
"""Consecutive source words (>= 2 letters each) copied verbatim into a CJK translation that count as untranslated."""
IDENTICAL_SAME_SCRIPT_MIN_WORDS = 4
"""Same-script pairs (en -> es, zh -> ja): an identical translation is reported from this many Latin words ..."""
IDENTICAL_SAME_SCRIPT_MIN_LETTERS = 12
"""... or this many CJK letters (shorter identical labels are usually cognates: "Total", "直角三角形")."""
OUTPUT_TEXT_PREFIX_CHARS = 12
"""Characters of each translation that must be extractable from the output page."""
OUTPUT_TEXT_MIN_FOUND = 0.5
"""Minimum share of translated blocks per page whose prefix is extractable."""
OUTPUT_LEFTOVER_MAX_SHARE = 0.05
"""Maximum share of unexplained source-script letters among the letters of an output page."""
OUTPUT_LEFTOVER_MAX_ABSOLUTE = 30
"""Unexplained source-script letters at or above this count are reported regardless of the share."""
GEOMETRY_TOLERANCE_PT = 1.0
PAGE_SIZE_TOLERANCE_PT = 0.5

# --------------------------------------------------------------------------- #
# Script helpers
# --------------------------------------------------------------------------- #

# Character classes of mathtrans.languages.script_profile, written as escapes so
# that look-alike code points cannot creep in (U+F900 is the compatibility
# ideograph block; the visually identical U+8C48 would swallow all of Hangul).
_RANGES = {
    "han": "\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff",
    "kana": "\u3041-\u309f\u30a0-\u30ff\uff66-\uff9f",
    "hangul": "\uac00-\ud7af\u1100-\u11ff\u3130-\u318f",
    "latin": "A-Za-z\u00c0-\u024f",
}
_SCRIPT_KEYS: dict[str, tuple[str, ...]] = {
    "han": ("han",), "kana_han": ("han", "kana"), "hangul": ("hangul",), "latin": ("latin",),
}
"""Script-profile keys that make up the writing system of each script family.

Unlike :func:`mathtrans.languages.letters_of_script` (which tolerates hanja in
Korean), Korean is hangul only here: modern Korean textbooks do not use hanja,
so Han characters in a Korean translation are untranslated Chinese or Japanese.
"""
_ALL_KEYS: tuple[str, ...] = ("han", "kana", "hangul", "latin")
_FULLWIDTH_DIGITS = str.maketrans("０１２３４５６７８９", "0123456789")
_DIGIT_RUN_RE = re.compile(r"[0-9]+")
_ENCLOSED_NUMBER_RE = re.compile(r"[\u2460-\u2473\u2474-\u2487\u2488-\u249b\u24f5-\u24fe\u24eb-\u24f4\uff10-\uff19]")
_CJK_DIGITS = "零一二三四五六七八九"
_LATIN_WORD_RE = re.compile(r"[A-Za-z\u00c0-\u024f]{2,}")
_NOTATION_WORDS = frozenset(w for w in FUNCTIONS | UNITS if w.isalpha())
"""Function names and unit symbols (``sin``, ``cos``, ``tan``, ``km``, ``cm`` ...): written in
Latin letters in every target language, so they are neither untranslated text nor foreign script."""
_CAPS_LABEL_RE = re.compile(r"[A-Z]{2,4}")
"""Shape of an upper-case point label (``AB``, ``CD``, ``PQRS``); ``protect._is_bare_label`` tells
such labels apart from words set in capitals (``UNIT``, ``STEP``, ``NOTE``)."""
_LATIN_RUN_RE = re.compile(r"[" + _RANGES["latin"] + r"]+")
_SENTENCE_END = ".!?:;…。！？：\n"


def _is_notation(word: str) -> bool:
    """Whether a Latin word is mathematical notation that stays in Latin letters in every
    language: a function name, a unit symbol or an upper-case point label (``sin``, ``cm``, ``AB``)."""
    return word.casefold() in _NOTATION_WORDS or (_CAPS_LABEL_RE.fullmatch(word) is not None and _is_bare_label(word))


def _strip_notation(text: str) -> str:
    """``text`` with every notation word (see :func:`_is_notation`) blanked out; a word is
    a maximal run of Latin letters, so ``sin`` inside ``sine`` is left alone."""
    return _LATIN_RUN_RE.sub(lambda m: " " if _is_notation(m.group(0)) else m.group(0), text)


@lru_cache(maxsize=16)
def _runs_re(keys: tuple[str, ...]) -> re.Pattern[str]:
    return re.compile("[" + "".join(_RANGES[k] for k in keys) + "]+")


def _letters(text: str) -> int:
    """Letters of any supported script (digits, punctuation and symbols excluded)."""
    p = script_profile(text)
    return p["han"] + p["kana"] + p["hangul"] + p["latin"]


def _lang_name(lang: Lang | str) -> str:
    return info(lang).name_en


def _script_keys(lang: Lang | str) -> tuple[str, ...]:
    return _SCRIPT_KEYS[info(lang).script]


def _foreign_keys(tgt: Lang | str) -> tuple[str, ...]:
    """Script keys that must not occur in a translation into ``tgt`` (Latin letters
    are tolerated everywhere: variables, units and names are written in Latin)."""
    valid = _script_keys(tgt)
    return tuple(k for k in _ALL_KEYS if k != "latin" and k not in valid)


def foreign_letters(text: str, tgt: Lang | str) -> int:
    """Letters of ``text`` written in a script that is not valid in ``tgt``.

    Same as :func:`mathtrans.languages.foreign_letters` except that Han
    characters count as foreign in Korean (see :data:`_SCRIPT_KEYS`).
    """
    p = script_profile(text)
    return sum(p[k] for k in _foreign_keys(tgt))


def script_ratio(text: str, tgt: Lang | str) -> float:
    """Share of the letters of ``text`` that belong to the script of ``tgt``
    (1.0 when there are no letters); hangul only for Korean. Unlike
    :func:`mathtrans.languages.script_ratio`, notation that stays in Latin letters in
    every language (``sin``, ``cos``, ``km``, ``AB``; see :func:`_is_notation`) is not counted."""
    p = script_profile(_strip_notation(text))
    letters = sum(p[k] for k in _ALL_KEYS)
    if letters == 0:
        return 1.0
    return sum(p[k] for k in _script_keys(tgt)) / letters


def distinctive_source_keys(src: Lang | str, tgt: Lang | str) -> tuple[str, ...]:
    """Script-profile keys of letters that belong to the source script but are *not*
    valid in the target script (empty when the scripts overlap, e.g. zh -> ja)."""
    tgt_keys = _script_keys(tgt)
    return tuple(k for k in _script_keys(src) if k not in tgt_keys)


def _cjk_numerals(run: str) -> tuple[str, ...]:
    """Chinese/Japanese spellings of an integer below 1000: ``"13"`` -> ``("十三",)``,
    ``"105"`` -> ``("一百零五", "百五")``, ``"110"`` -> ``("一百一十", "一百十", "百十")``;
    empty for longer numbers."""
    if not run or len(run) > 3:
        return ()
    n = int(run)
    if n < 10:
        return (_CJK_DIGITS[n], "两") if n == 2 else (_CJK_DIGITS[n],)
    hundreds, rest = divmod(n, 100)
    tens, ones = divmod(rest, 10)
    ones_text = _CJK_DIGITS[ones] if ones else ""
    if hundreds == 0:
        return (("" if tens == 1 else _CJK_DIGITS[tens]) + "十" + ones_text,)
    # after an explicit hundreds digit a skipped tens place needs 零 (一百零五; 一百五 means 150),
    # the Japanese bare 百 does not (百五 = 105)
    if tens == 0:
        full_tails, bare_tails = ([""], [""]) if ones == 0 else (["零" + ones_text], [ones_text])
    elif tens == 1:
        full_tails, bare_tails = ["一十" + ones_text, "十" + ones_text], ["十" + ones_text]
    else:
        full_tails = bare_tails = [_CJK_DIGITS[tens] + "十" + ones_text]
    heads = [_CJK_DIGITS[hundreds] + "百"] + (["两百"] if hundreds == 2 else [])
    variants = [h + t for h in heads for t in full_tails]
    if hundreds == 1:
        variants += ["百" + t for t in bare_tails]
    return tuple(dict.fromkeys(variants))


_CJK_NUMERAL_CHARS = "零〇一二三四五六七八九两十百"


@lru_cache(maxsize=512)
def _spelled_re(spelling: str) -> re.Pattern[str]:
    """``spelling`` as a whole numeral: not inside a longer one (五 in 十五, 百五 in 百五十)."""
    return re.compile(f"(?<![{_CJK_NUMERAL_CHARS}]){re.escape(spelling)}(?![{_CJK_NUMERAL_CHARS}])")


def _spelled_count(text: str, run: str) -> int:
    """How often the number ``run`` is written with CJK numerals in ``text``."""
    return sum(len(_spelled_re(alt).findall(text)) for alt in _cjk_numerals(run))


def _digits_normalised(text: str) -> str:
    """ASCII digits for full-width digits and enclosed numbers (``①`` -> ``1``, ``⑴`` -> ``(1)``)."""
    return _ENCLOSED_NUMBER_RE.sub(lambda m: unicodedata.normalize("NFKC", m.group(0)), text)


def _copied_word_runs(source: str, translation: str, min_words: int = COPIED_RUN_MIN_WORDS) -> list[str]:
    """Runs of >= ``min_words`` consecutive Latin words (>= 2 letters each) of
    ``source`` that reappear, in order and unchanged, in ``translation``. Notation
    (``sin, cos, tan``, ``km, cm, mm``, ``AB, CD``) is skipped on both sides: a list of
    function names or units is not copied prose, and a run of copied prose is still
    found as the words around a ``max`` or ``cm`` in it."""
    src_words = [w.casefold() for w in _LATIN_WORD_RE.findall(source) if not _is_notation(w)]
    tr_words = [w for w in _LATIN_WORD_RE.findall(translation) if not _is_notation(w)]
    if len(src_words) < min_words or len(tr_words) < min_words:
        return []
    grams = {tuple(src_words[i: i + min_words]) for i in range(len(src_words) - min_words + 1)}
    runs: list[str] = []
    i = 0
    while i <= len(tr_words) - min_words:
        if tuple(w.casefold() for w in tr_words[i: i + min_words]) not in grams:
            i += 1
            continue
        j = i + min_words
        while j < len(tr_words) and tuple(w.casefold() for w in tr_words[j - min_words + 1: j + 1]) in grams:
            j += 1
        runs.append(" ".join(tr_words[i:j]))
        i = j
    return runs


def copied_names(source: str, translation: str) -> list[str]:
    """Latin words of ``translation`` that are proper names copied verbatim from
    ``source``: words with an inner capital (``GeoGebra``, ``LaTeX``, ``iPad``) anywhere,
    and capitalised words containing lower-case letters (``Excel``, ``Python``, ``Desmos``)
    that do not open a sentence of the source. Such names have no rendering in the
    target language, so they count neither as untranslated text nor against the
    target-script share (one entry per occurrence in the translation)."""
    names: set[str] = set()
    for m in _LATIN_WORD_RE.finditer(source):
        w = m.group(0)
        if not any(ch.islower() for ch in w) or not any(ch.isupper() for ch in w):
            continue
        inner_cap = any(ch.isupper() for ch in w[1:])
        before = source[: m.start()].rstrip()
        sentence_initial = not before or before[-1] in _SENTENCE_END
        if inner_cap or (w[0].isupper() and not sentence_initial):
            names.add(w)
    return [w for w in _LATIN_WORD_RE.findall(translation) if w in names]


# --------------------------------------------------------------------------- #
# Segment helpers
# --------------------------------------------------------------------------- #


def _checked(doc: TranslatedDocument) -> list[TextSegment]:
    return [s for s in doc.segments if s.translate]


def _is_translated(seg: TextSegment) -> bool:
    return seg.translated_text is not None and bool(seg.translated_text.strip())


def _translated(doc: TranslatedDocument) -> list[TextSegment]:
    return [s for s in _checked(doc) if _is_translated(s)]


def _strip_placeholders(text: str) -> str:
    return PLACEHOLDER_RE.sub(" ", text)


def _remove_fragments(text: str, fragments: list[str]) -> str:
    for frag in sorted(set(fragments), key=len, reverse=True):
        if frag:
            text = text.replace(frag, " ")
    return text


def source_body(seg: TextSegment) -> str:
    """The translatable part of the source (protected fragments removed)."""
    if seg.protected_text:
        return _strip_placeholders(seg.protected_text)
    return seg.source_text


def translation_body(seg: TextSegment) -> str:
    """The translation with the protected fragments removed (placeholders when the raw
    translation is known, otherwise the restored fragments themselves)."""
    if seg.translation_raw is not None:
        return _strip_placeholders(seg.translation_raw)
    return _remove_fragments(seg.translated_text or "", seg.protected)


def _excerpt(text: str, limit: int = 40) -> str:
    t = " ".join(text.split())
    return t if len(t) <= limit else t[: limit - 1] + "…"


def _issue(check: str, severity: Severity, seg: TextSegment, message: str, *, fixable: bool = True,
           **details: object) -> QAIssue:
    return QAIssue(check=check, severity=severity, message=message, segment_id=seg.id, page=seg.page,
                   details=dict(details), fixable=fixable)


def shorten_hint(text: str, scale: float, min_scale: Optional[float] = None) -> int:
    """Maximum number of characters a translation should have so that it fits the box
    in which it had to be rendered at ``scale`` (the engine's shrink factor).

    With ``min_scale`` (text boxes re-flowed by the layout engine) the text is
    allowed the area it would occupy at ``min_scale``: a text that just fits at
    ``scale`` needs ``(min_scale / scale)²`` times its area at ``min_scale``, so
    about ``(scale / min_scale)²`` of its characters fit. Without ``min_scale``
    (single-line labels inside images, where width grows linearly) the share is
    ``scale`` itself. Always strictly shorter than the current text.
    """
    n = len(text.strip())
    if n <= 1:
        return 1
    if scale <= 0:
        factor = 0.5
    elif min_scale is not None and min_scale > 0:
        factor = min(1.0, (scale / min_scale) ** 2) * 0.9
    else:
        factor = min(1.0, scale) * 0.95
    return max(1, min(int(n * factor), n - 1))


# --------------------------------------------------------------------------- #
# Rule checks
# --------------------------------------------------------------------------- #


def completeness(doc: TranslatedDocument, options: PipelineOptions,
                 pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """Every translatable segment with text must have a non-empty translation, and a
    source with words must not be translated into bare punctuation / symbols."""
    issues: list[QAIssue] = []
    for seg in _checked(doc):
        if not seg.source_text.strip():
            continue
        if not _is_translated(seg):
            issues.append(_issue("completeness", "error", seg,
                                 "The segment has no translation; translate the complete source text"))
            continue
        translation = seg.translated_text or ""
        if _letters(seg.source_text) and not _letters(translation) and not _DIGIT_RUN_RE.search(translation):
            issues.append(_issue(
                "completeness", "error", seg,
                f"The translation \"{_excerpt(translation, 20)}\" contains no words; translate the complete "
                f"source text", translation=translation))
    return issues


def placeholders(doc: TranslatedDocument, options: PipelineOptions,
                 pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """Every protected fragment (formula, number, variable) must come back exactly once."""
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        if seg.translation_raw is not None and seg.protected_text:
            for problem in verify_placeholders(seg.protected_text, seg.translation_raw):
                legend = ", ".join(
                    f"⟦{i}⟧ = \"{_excerpt(seg.protected[i], 30)}\""
                    for i in sorted({int(m) for m in re.findall(r"⟦(\d+)⟧", problem)}) if i < len(seg.protected)
                )
                message = (f"Placeholder problem: {problem}. Keep every ⟦n⟧ placeholder of the source exactly "
                           f"once, unchanged, at the matching position")
                if legend:
                    message += f" ({legend})"
                issues.append(_issue("placeholders", "error", seg, message, problem=problem))
            continue
        # No raw translation available (segment built outside the translator): the
        # restored fragments themselves must survive verbatim.
        counts = Counter(seg.protected)
        for frag, n in counts.items():
            have = (seg.translated_text or "").count(frag)
            if have < n:
                issues.append(_issue(
                    "placeholders", "error", seg,
                    f"Protected fragment \"{_excerpt(frag, 30)}\" from the source is missing in the translation; "
                    f"copy it verbatim", fragment=frag))
    return issues


def numbers(doc: TranslatedDocument, options: PipelineOptions,
            pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """Every digit sequence of the source must appear in the translation (full-width
    digits and enclosed numbers such as ``①`` are normalised on both sides; a number
    below 1000 spelled with CJK numerals counts as present)."""
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        src_runs = Counter(_DIGIT_RUN_RE.findall(_digits_normalised(seg.source_text).translate(_FULLWIDTH_DIGITS)))
        translated = _digits_normalised(seg.translated_text or "").translate(_FULLWIDTH_DIGITS)
        tr_runs = Counter(_DIGIT_RUN_RE.findall(translated))
        for run, missing in sorted((src_runs - tr_runs).items()):
            if _spelled_count(translated, run) >= missing:
                continue
            issues.append(_issue(
                "numbers", "error", seg,
                f"Number \"{run}\" from the source is missing in the translation; keep every number exactly as "
                f"written in the source", number=run, missing=missing))
    return issues


def _identical_is_untranslated(seg: TextSegment, src: Lang, tgt: Lang) -> bool:
    """Whether a translation equal to the source counts as untranslated.

    Between different scripts any identical text of >= 4 letters is untranslated.
    Between languages sharing a script (en -> es, zh -> ja) short identical labels
    are usually cognates (``Total``, ``Figura 1-1``, ``直角三角形``), so only longer
    texts are reported (:data:`IDENTICAL_SAME_SCRIPT_MIN_WORDS` Latin words or
    :data:`IDENTICAL_SAME_SCRIPT_MIN_LETTERS` CJK letters).
    """
    letters = _letters(seg.source_text)
    if letters < MIN_LETTERS_FOR_SCRIPT_CHECKS:
        return False
    if is_fully_protected(seg.protected_text or seg.source_text):
        return False
    if normalize_for_compare(seg.translated_text or "") != normalize_for_compare(seg.source_text):
        return False
    if distinctive_source_keys(src, tgt):
        return True
    if is_cjk(src):
        return letters >= IDENTICAL_SAME_SCRIPT_MIN_LETTERS
    return len(_LATIN_WORD_RE.findall(source_body(seg))) >= IDENTICAL_SAME_SCRIPT_MIN_WORDS


def _only_copied_names(seg: TextSegment) -> bool:
    """Whether every word of the source is a proper name copied into the translation."""
    words = _LATIN_WORD_RE.findall(source_body(seg))
    return bool(words) and set(words) <= set(copied_names(source_body(seg), translation_body(seg)))


def untranslated(doc: TranslatedDocument, options: PipelineOptions,
                 pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """No source-script text may remain outside protected fragments (tiny labels may
    keep up to two stray letters, unless the translation is a verbatim copy of the
    source), no run of source words may be copied verbatim into a CJK translation,
    and the translation must differ from the source (a label made of copied proper
    names such as ``GeoGebra`` excepted)."""
    src, tgt = doc.source_lang, doc.target_lang
    latin_into_cjk = "latin" in distinctive_source_keys(src, tgt)
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        body = _TALLY_RUN_RE.sub("", translation_body(seg))  # 正 tally marks stay by convention
        src_letters = _letters(seg.source_text)
        foreign = foreign_letters(body, tgt)
        # a tiny label may keep a stray letter, but a verbatim copy of the source is untranslated
        copied = normalize_for_compare(body) == normalize_for_compare(source_body(seg))
        allowance = TINY_LABEL_FOREIGN_ALLOWANCE if src_letters <= TINY_LABEL_MAX_LETTERS and not copied else 0
        if foreign > allowance:
            runs = _runs_re(_foreign_keys(tgt)).findall(body)
            sample = ", ".join(f"\"{r}\"" for r in dict.fromkeys(runs[:3]))
            issues.append(_issue(
                "untranslated", "error", seg,
                f"{foreign} letter(s) of the source script remain untranslated ({sample}); translate all text "
                f"into {_lang_name(tgt)}", foreign_letters=foreign, fragments=runs[:5]))
            continue
        if latin_into_cjk:
            copied = _copied_word_runs(source_body(seg), body)
            if copied:
                issues.append(_issue(
                    "untranslated", "error", seg,
                    f"The source words \"{_excerpt(copied[0], 50)}\" were copied untranslated; translate them "
                    f"into {_lang_name(tgt)} (only formulas, variable names and units stay in Latin letters)",
                    copied_runs=copied[:5]))
                continue
        if _source_script_letters(seg.source_text, src) == 0:
            continue  # romanised names, acronyms, codes: nothing to translate ("SHUXUE", "ISBN")
        if _only_copied_names(seg):
            continue  # a label that is a product / software name ("GeoGebra") has no translation
        if _identical_is_untranslated(seg, src, tgt):
            issues.append(_issue(
                "untranslated", "error", seg,
                f"The translation is identical to the source text; translate it into {_lang_name(tgt)}"))
    return issues


def target_script(doc: TranslatedDocument, options: PipelineOptions,
                  pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """The translation must be written mainly in the script of the target language."""
    tgt = doc.target_lang
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        body = translation_body(seg)
        names = copied_names(source_body(seg), body)
        for name in names:  # copied proper names are neither target-script nor foreign text
            body = body.replace(name, " ", 1)
        if _letters(body) < MIN_LETTERS_FOR_SCRIPT_CHECKS:
            continue
        ratio = script_ratio(body, tgt)
        if ratio < TARGET_SCRIPT_MIN_RATIO:
            issues.append(_issue(
                "target_script", "error", seg,
                f"Only {ratio:.0%} of the letters in the translation are in the {_lang_name(tgt)} script; write "
                f"the whole translation in {_lang_name(tgt)} (formulas, variable names, units and proper names "
                f"copied from the source excepted)",
                script_ratio=round(ratio, 3), copied_names=names))
    return issues


_LATIN_PLURAL = r"(?:s|es)?"
"""Optional plural ending tolerated after each word of a Latin-script glossary term."""


def _latin_word_re(word: str) -> str:
    if word.endswith("ão"):  # Portuguese: equação -> equações, mão -> mãos, pão -> pães
        return re.escape(word[:-2]) + r"(?:ão|ões|ãos|ães)"
    return re.escape(word) + _LATIN_PLURAL


@lru_cache(maxsize=4096)
def _latin_term_re(term: str) -> re.Pattern[str]:
    words = unicodedata.normalize("NFKC", term).casefold().split()
    body = r"\s+".join(_latin_word_re(w) for w in words)
    return re.compile(rf"(?<![{_RANGES['latin']}]){body}(?![{_RANGES['latin']}])")


@lru_cache(maxsize=4096)
def _cjk_term_re(term: str) -> re.Pattern[str]:
    return re.compile(re.escape(unicodedata.normalize("NFKC", term).casefold()))


@lru_cache(maxsize=8)
def _compiled_pairs(pairs: tuple[tuple[str, str], ...], src_lang: Lang) -> tuple[tuple[str, str, re.Pattern[str]], ...]:
    """``(source term, target term, compiled source pattern)`` for every enforced pair
    (non-blank source; for CJK sources at least two characters, see
    :func:`mathtrans.glossary.is_enforced_source_term`), compiled once per glossary. The
    per-term caches above hold 4096 patterns: a larger glossary would evict cyclically and
    recompile every pattern for every segment in every QA round (seconds per segment for
    20k entries)."""
    term_re = _cjk_term_re.__wrapped__ if is_cjk(src_lang) else _latin_term_re.__wrapped__
    return tuple((s, t, term_re(s)) for s, t in pairs if is_enforced_source_term(s, src_lang))


def used_glossary_pairs(source: str, pairs: GlossaryPairs, src_lang: Lang | str) -> GlossaryPairs:
    """The pairs whose source term occurs in ``source``.

    CJK sources use substring matching; Latin-script sources need whole words with
    optional inflection ("legs", "triángulos rectángulos", "equações"). Pairs are
    tried longest source term first and an occurrence inside the match of a longer
    term is shadowed ("三角形" inside "直角三角形", "rectángulo" inside "triángulos
    rectángulos"), so a term counts only where it occurs on its own. One-character
    CJK terms ("解", "角", "円", "각") are never enforced: they occur inside unrelated
    words ("解释", "5 角", "120 円", "각 변") far too often.
    """
    text = unicodedata.normalize("NFKC", source).casefold()
    used: GlossaryPairs = []
    covered: list[tuple[int, int]] = []
    for s, t, rx in _compiled_pairs(tuple((s, t) for s, t in pairs), Lang.parse(src_lang)):  # longest source first
        spans = [m.span() for m in rx.finditer(text)]
        if spans and not all(any(a <= x0 and x1 <= b for a, b in covered) for x0, x1 in spans):
            used.append((s, t))
            covered.extend(spans)
    return used


def _doc_pairs(doc: TranslatedDocument) -> GlossaryPairs:
    """Glossary pairs attached to the document (used when a check is called without pairs)."""
    return doc.glossary.pairs(doc.source_lang, doc.target_lang) if doc.glossary is not None else []


def glossary(doc: TranslatedDocument, options: PipelineOptions,
             pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """Glossary terms occurring in the source must be rendered with their fixed translation
    (:func:`mathtrans.glossary.term_present`: case- and accent-insensitive, inflection-
    tolerant per word for Latin targets, whitespace-insensitive for CJK targets).
    ``pairs`` defaults to the pairs of ``doc.glossary``."""
    if pairs is None:
        pairs = _doc_pairs(doc)
    if not pairs:
        return []
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        translation = seg.translated_text or ""
        for s, t in used_glossary_pairs(seg.source_text, pairs, doc.source_lang):
            if not term_present(t, translation, doc.target_lang):
                issues.append(_issue("glossary", "error", seg, f"Glossary: translate \"{s}\" as \"{t}\"",
                                     source_term=s, target_term=t))
    return issues


def length_ratio(doc: TranslatedDocument, options: PipelineOptions,
                 pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """The translation length must be plausible for the language pair (warning only)."""
    expected = LANGUAGES[doc.target_lang].length_vs_zh / LANGUAGES[doc.source_lang].length_vs_zh
    lo, hi = LENGTH_RATIO_MIN * expected, LENGTH_RATIO_MAX * expected
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        n_src = len(" ".join(source_body(seg).split()))
        if n_src < LENGTH_RATIO_MIN_SOURCE_CHARS:
            continue
        n_tr = len(" ".join(translation_body(seg).split()))
        ratio = n_tr / n_src
        if lo <= ratio <= hi:
            continue
        verdict = "short" if ratio < lo else "long"
        advice = "check that nothing was omitted" if ratio < lo else "check that nothing was added or explained"
        issues.append(_issue(
            "length_ratio", "warning", seg,
            f"The translation looks too {verdict}: {n_tr} characters for {n_src} translatable source characters "
            f"(ratio {ratio:.2f}, about {expected:.2f} expected); {advice}",
            ratio=round(ratio, 3), expected=round(expected, 3), source_chars=n_src, translation_chars=n_tr))
    return issues


# ---- formatting -------------------------------------------------------------

_MARKER_RE = re.compile(
    r"^\s*(?:"
    r"[(（](?P<paren>[0-9０-９]{1,3}|[A-Za-zａ-ｚＡ-Ｚ]|[ivxIVX]{1,6})[)）]"
    r"|(?P<num>[0-9０-９]{1,3})[.)．、）:：](?![0-9０-９])"
    r"|(?P<alpha>[A-Za-z])[.)）](?=\s)"
    r"|(?P<circled>[①-⑳⑴-⒇⒈-⒛㈠-㈩⓵-⓾])"
    r"|(?P<bullet>[•·▪◦‣■□●○◆◇★☆※*])"
    r"|(?P<dash>[-–—])(?=\s)"
    r"|(?P<cjk>[一二三四五六七八九十]{1,3})[、.．,，]"
    r")"
)
_WRAPPER_PREFIX_RE = re.compile(
    r"^\s*(?:translation|translated text|translated|译文|翻译|翻訳|訳文|번역|traducción|tradução|traduction)"
    r"\s*[:：]", re.IGNORECASE)
"""Prefixes a model may add around its output. Deliberately *not* "Answer:" / "Solution:",
which are legitimate translations of 答：/ 解："""
_QUOTE_PAIRS = {'"': '"', "“": "”", "'": "'", "‘": "’", "「": "」", "『": "』", "«": "»", "„": "“"}
_OPENING_QUOTES = set(_QUOTE_PAIRS)
_TRAILING_CLOSERS = ")）]】」』”\"'’》〉›»"
_JSON_HINT_RE = re.compile(r"\"(?:id|text|translations?)\"\s*:")


_CJK_NUMERAL_RUN_RE = re.compile(r"^\s*[零〇一二三四五六七八九十百千万两]")
"""A Chinese number word follows: ``五、十、十五`` is a counting sequence, not an enumerator."""
_TALLY_RUN_RE = re.compile(r"(?<![\u4e00-\u9fff])正+(?![\u4e00-\u9fff])")
"""Standalone tally marks (正 used for counting strokes), kept verbatim by convention."""


def _marker(text: str) -> Optional[tuple[str, str]]:
    """``(kind, normalised core)`` of the list marker starting ``text`` (None = no marker)."""
    m = _MARKER_RE.match(text)
    if not m:
        return None
    kind = m.lastgroup or ""
    core = m.group(kind)
    if kind in ("bullet", "dash"):
        return kind, "•"
    if kind == "cjk":
        rest = text[m.end():]
        if not rest.strip() or _CJK_NUMERAL_RUN_RE.match(rest):
            return None  # 五、十、十五… / 九十八、九十九: number words read aloud, not a list marker
        return kind, core
    norm = unicodedata.normalize("NFKC", core).casefold()
    return kind, re.sub(r"[^0-9a-z]", "", norm) or norm


_JA_QUESTION_END_RE = re.compile(r"(?:か|かな|かしら)[。．.]?$")
"""Textbook Japanese ends a question with the particle か and a full stop (か。); ？ is optional."""
_ZH_QUESTION_END_RE = re.compile(r"[吗呢][。．.]?$")
"""Chinese questions ending in 吗 / 呢 may carry a full stop instead of ？."""


def _terminal_class(text: str, lang: Optional[Lang] = None) -> str:
    """Class of the sentence-final punctuation (question / exclamation / period / colon /
    comma / none). With ``lang`` the language's own question endings count too."""
    t = text.rstrip().rstrip(_TRAILING_CLOSERS).rstrip()
    if not t:
        return "none"
    if lang == Lang.JA and _JA_QUESTION_END_RE.search(t):
        return "question"
    if lang == Lang.ZH and _ZH_QUESTION_END_RE.search(t):
        return "question"
    ch = t[-1]
    if ch in "?？":
        return "question"
    if ch in "!！":
        return "exclamation"
    if ch in ".。．":
        return "period"
    if ch in ":：":
        return "colon"
    if ch in ",，、;；":
        return "comma"
    return "none"


def _wrapped_in_quotes(text: str) -> bool:
    t = text.strip()
    if len(t) < 2 or t[0] not in _OPENING_QUOTES:
        return False
    return t[-1] == _QUOTE_PAIRS[t[0]]


def _formatting_issues(seg: TextSegment, src_lang: Lang, tgt_lang: Lang) -> list[QAIssue]:
    src, tr = seg.source_text, seg.translated_text or ""
    issues: list[QAIssue] = []

    def add(message: str, severity: Severity = "error", **details: object) -> None:
        issues.append(_issue("formatting", severity, seg, message, **details))

    # list markers
    src_marker, tr_marker = _marker(src), _marker(tr)
    if src_marker is not None:
        marker_text = _MARKER_RE.match(src).group(0).strip()  # type: ignore[union-attr]
        if tr_marker is None:
            add(f"Start the translation with the list marker \"{marker_text}\" exactly as in the source",
                marker=marker_text)
        elif src_marker[0] != "cjk" and src_marker[1] != tr_marker[1]:
            found = _MARKER_RE.match(tr).group(0).strip()  # type: ignore[union-attr]
            add(f"Keep the list marker \"{marker_text}\" at the start of the translation (found \"{found}\")",
                marker=marker_text, found=found)
    # raw placeholders that could not be restored
    leftovers = re.findall(r"⟦[^⟧]*⟧?|⟧", tr)
    if leftovers:
        add(f"The translation still contains the raw placeholder \"{leftovers[0]}\"; use only the ⟦n⟧ "
            f"placeholders that occur in the source, each exactly once", leftover=leftovers[0])
    # wrappers added by the model
    if _WRAPPER_PREFIX_RE.match(tr) and not _WRAPPER_PREFIX_RE.match(src):
        add("Remove the \"Translation:\" style prefix; output only the translated text")
    stripped = tr.strip()
    if stripped.startswith("```") or (stripped[:1] in "{[" and _JSON_HINT_RE.search(stripped)):
        add("Output the translation as plain text, not as JSON or a code block")
    if _wrapped_in_quotes(tr) and not _wrapped_in_quotes(src) and src.strip()[:1] not in _OPENING_QUOTES:
        add("Remove the quotation marks wrapping the translation; the source is not quoted")
    # line breaks
    n_src, n_tr = src.count("\n"), tr.count("\n")
    if abs(n_src - n_tr) > 1:
        add(f"Keep the line breaks of the source: it has {n_src} line break(s), the translation has {n_tr}",
            source_breaks=n_src, translation_breaks=n_tr)
    # terminal punctuation class (a Japanese か。 or Chinese 吗。 question counts as a question)
    src_cls, tr_cls = _terminal_class(src, src_lang), _terminal_class(tr, tgt_lang)
    for cls, mark in (("question", "question mark"), ("exclamation", "exclamation mark")):
        # CJK textbooks rarely write "!": an imperative "Let's try it!" is やってみよう。/ 试一试。
        # and vice versa, so an exclamation mismatch with a CJK side is a hint, not an error
        severity: Severity = "warning" if cls == "exclamation" and (is_cjk(src_lang) or is_cjk(tgt_lang)) else "error"
        if src_cls == cls and tr_cls != cls:
            add(f"The source ends with a {mark}; end the translation with a {mark} too", severity,
                source_ending=src_cls, translation_ending=tr_cls)
        elif tr_cls == cls and src_cls != cls and not _contains_mark(src, cls):
            # a mark that occurs inside the source (fill-in-the-blank "？个", "How many ... ?" phrased
            # differently) may legitimately move to the end of the translation
            add(f"The source does not end with a {mark}; do not end the translation with one", severity,
                source_ending=src_cls, translation_ending=tr_cls)
    return issues


_MARKS = {"question": "?？", "exclamation": "!！"}


def _contains_mark(text: str, cls: str) -> bool:
    return any(ch in text for ch in _MARKS.get(cls, ""))


def formatting(doc: TranslatedDocument, options: PipelineOptions,
               pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """List markers, line breaks and sentence-final punctuation must be preserved; no
    wrappers (quotes, "Translation:", JSON) or raw placeholders may be added. Japanese
    か。 and Chinese 吗。 count as question endings; an exclamation mark missing or added
    on a CJK side is a warning."""
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        issues.extend(_formatting_issues(seg, doc.source_lang, doc.target_lang))
        issues.extend(_convention_issues(seg))
    return issues


_PLACEHOLDER_UNIT_RE = re.compile(r"\((?:pieces?|items?|pcs\.?|units?|ones|no\.|nos\.|each|counts?)\)", re.IGNORECASE)
_KEPT_SYMBOLS = "○△□●▲■◇◆☆★✓√"


def _convention_issues(seg: TextSegment) -> list[QAIssue]:
    """Textbook conventions: no placeholder nouns for measure words, symbols kept."""
    out: list[QAIssue] = []
    tr = seg.translated_text or ""
    m = _PLACEHOLDER_UNIT_RE.search(tr)
    if m:
        out.append(_issue(
            "formatting", "error", seg,
            f"\"{m.group(0)}\" is not a translation of a measure word: write the plural noun of the counted thing "
            f"((apples), (chicks), (sticks)) or, when the exercise does not name it, drop the parentheses",
            placeholder_unit=m.group(0)))
    src_symbols = Counter(ch for ch in seg.source_text if ch in _KEPT_SYMBOLS)
    tr_symbols = Counter(ch for ch in tr if ch in _KEPT_SYMBOLS)
    missing = src_symbols - tr_symbols
    if missing:
        listed = " ".join(f"{ch}×{n}" if n > 1 else ch for ch, n in sorted(missing.items()))
        out.append(_issue(
            "formatting", "error", seg,
            f"Keep the symbol(s) {listed} of the source in the translation, at the matching position",
            missing_symbols=dict(missing)))
    added = tr_symbols - src_symbols
    if added:
        listed = " ".join(f"{ch}×{n}" if n > 1 else ch for ch, n in sorted(added.items()))
        out.append(_issue(
            "formatting", "error", seg,
            f"Remove the symbol(s) {listed}: they are not in the source (a picture in the book is not a symbol; "
            f"leave it out rather than inventing one)", added_symbols=dict(added)))
    return out


# ---- layout -----------------------------------------------------------------


IMAGE_MIN_FEASIBLE_CHARS = 5
"""An image label shorter than this cannot be asked for; the fit is reported as a warning."""
UNRELIABLE_OCR_PREFIX = "unreliable OCR"
LEFT_IN_PICTURE_REASONS = (
    "unreadable symbol in quotes (left in the picture)",
    "inline pictograms the OCR cannot read (left in the picture)",
)
"""``skip_reason`` values (images.UNREADABLE_SYMBOL / INLINE_PICTOGRAMS) of source text that
stays in the picture untranslated; reported as warnings for a human check."""
"""``skip_reason`` prefix of OCR lines rejected as misreads by ``images.classify_ocr_text``."""
IMAGE_MIN_FEASIBLE_SHARE = 0.35
SHORT_LABEL_CHARS = 12
"""Translations up to this length are labels / names: they cannot be halved, so a
shorten request below half their length is infeasible."""
SHORT_LABEL_SHARE = 0.5


def _feasible_share(current: int) -> float:
    return SHORT_LABEL_SHARE if current <= SHORT_LABEL_CHARS else IMAGE_MIN_FEASIBLE_SHARE
"""A shorten request below this share of the current length is considered infeasible."""


def layout_fit(doc: TranslatedDocument, options: PipelineOptions,
               pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """Rendered native-text translations must fit their boxes without shrinking below
    ``options.min_font_scale``; otherwise ask for a shorter translation."""
    issues: list[QAIssue] = []
    for seg in _translated(doc):
        r = seg.render
        if seg.kind != SegmentKind.TEXT or r is None:
            continue
        if r.overflow or r.scale < options.min_font_scale:
            current = len((seg.translated_text or "").strip())
            max_chars = shorten_hint(seg.translated_text or "", r.scale, options.min_font_scale)
            why = "overflows its box" if r.overflow else f"had to be shrunk to {r.scale:.0%} of the original size"
            if max_chars < max(IMAGE_MIN_FEASIBLE_CHARS, int(_feasible_share(current) * current)):
                # No translation this short can carry the meaning (tiny OCR box, huge expansion):
                # report it for a human instead of blocking the export on a hopeless re-translation.
                issues.append(_issue(
                    "layout_fit", "warning", seg,
                    f"The translation {why} and was rendered at {r.scale:.0%} of the original size; even a "
                    f"much shorter text would not fit, check this box in the preview",
                    fixable=False, max_chars=max_chars, scale=round(r.scale, 3), overflow=r.overflow,
                    min_font_scale=options.min_font_scale))
                continue
            issues.append(_issue(
                "layout_fit", "error", seg,
                f"Shorten the translation to at most {max_chars} characters so it fits the original box "
                f"(the current translation of {current} characters {why}; "
                f"the minimum allowed size is {options.min_font_scale:.0%})",
                max_chars=max_chars, scale=round(r.scale, 3), overflow=r.overflow,
                min_font_scale=options.min_font_scale))
    return issues


def image_text(doc: TranslatedDocument, options: PipelineOptions,
               pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """Translated text inside images must have been painted and must fit its region.

    ``render`` is None before the image stage ran (warning). A render with no font
    size and no scale means nothing was drawn (the image could not be decoded or
    replaced): the original text is still in the picture, which no re-translation
    can fix (unfixable error). An overflow of drawn text asks for a shorter one.

    Two document-level facts recorded by the OCR stage are reported here too:
    ``doc.ocr_failures`` (images whose OCR request failed, so their text was never
    translated: an unfixable warning, or an error when no image was read at all)
    and ``doc.ocr_low_trust`` (a Japanese / Korean source read by the offline
    zh/en OCR models: every translated in-image text gets an unfixable warning
    asking for a look at the preview, because the recognised source may be wrong).
    """
    issues: list[QAIssue] = []
    if doc.ocr_failures:
        recognised = {s.image.xref for s in doc.image_segments() if s.image is not None}
        failed = len(doc.ocr_failures)
        issues.append(QAIssue(
            check="image_text", severity="warning" if recognised else "error", fixable=False,
            message=f"OCR failed on {failed} of {failed + len(recognised)} image(s); the text inside them was not "
                    f"translated: {doc.ocr_failures[0]}",
            details={"ocr_failures": list(doc.ocr_failures)}))
    source = LANGUAGES[doc.source_lang].name_en
    if doc.ocr_low_trust:
        for seg in _checked(doc):
            if seg.kind == SegmentKind.IMAGE_TEXT or seg.origin == "ocr":
                issues.append(_issue(
                    "image_text", "warning", seg,
                    f"Text inside this image was recognised by the offline Chinese/English OCR models, which read "
                    f"{source} unreliably (the source text may be misread): check the figure in the preview, or use "
                    f"the Claude vision OCR (MATHTRANS_OCR_ENGINE=claude / --ocr-engine claude)",
                    fixable=False, ocr_low_trust=True))
    for seg in doc.image_segments():
        if not seg.translate and seg.skip_reason.startswith(UNRELIABLE_OCR_PREFIX):
            # images.classify_ocr_text rejected the OCR result (e.g. Han-only text in a Korean figure):
            # the label was left untouched rather than overpainted with a translation of garbage
            issues.append(_issue(
                "image_text", "warning", seg,
                f"The text {seg.source_text!r} recognised inside this image is not plausible {source} "
                f"({seg.skip_reason}); it was left untouched - check the figure in the preview, or use the "
                f"Claude vision OCR (MATHTRANS_OCR_ENGINE=claude / --ocr-engine claude)",
                fixable=False, unreliable_ocr=True))
        elif not seg.translate and seg.skip_reason in LEFT_IN_PICTURE_REASONS:
            issues.append(_issue(
                "image_text", "warning", seg,
                f"The text {seg.source_text!r} was left in the source language ({seg.skip_reason}): the line is "
                f"built around symbols or pictures the OCR could not read - check the page in the preview",
                fixable=False, left_in_picture=True))
    for seg in _translated(doc):
        if seg.kind != SegmentKind.IMAGE_TEXT:
            continue
        r = seg.render
        if r is None:
            issues.append(_issue(
                "image_text", "warning", seg,
                "The translated text inside the image has not been rendered yet", fixable=False))
        elif r.font_size <= 0 and r.scale <= 0:
            reason = f" ({r.notes})" if r.notes else ""
            issues.append(_issue(
                "image_text", "error", seg,
                f"The translated text could not be painted into the image{reason}; the original text is still "
                f"visible in the picture", fixable=False, notes=r.notes))
        elif r.overflow:
            current = len((seg.translated_text or "").strip())
            max_chars = shorten_hint(seg.translated_text or "", r.scale)
            if max_chars < max(IMAGE_MIN_FEASIBLE_CHARS, int(_feasible_share(current) * current)):
                # Even a drastically shorter text would not fit (tiny label, huge glyphs):
                # re-translating cannot fix it, so report it for a human instead of blocking.
                issues.append(_issue(
                    "image_text", "warning", seg,
                    f"The translation does not fit the tiny text region inside the image even at the minimum "
                    f"font size; it was drawn at the minimum size and may overflow its box - check the preview",
                    fixable=False, max_chars=max_chars, scale=round(r.scale, 3), overflow=True))
            else:
                issues.append(_issue(
                    "image_text", "error", seg,
                    f"Shorten the translation to at most {max_chars} characters so it fits the text region inside "
                    f"the image (the current {current}-character translation overflows it)",
                    max_chars=max_chars, scale=round(r.scale, 3), overflow=True))
    return issues


CHECKS: list[tuple[str, Severity, CheckFn]] = [
    ("completeness", "error", completeness),
    ("placeholders", "error", placeholders),
    ("numbers", "error", numbers),
    ("untranslated", "error", untranslated),
    ("target_script", "error", target_script),
    ("glossary", "error", glossary),
    ("length_ratio", "warning", length_ratio),
    ("formatting", "error", formatting),
    ("layout_fit", "error", layout_fit),
    ("image_text", "error", image_text),
]
"""Registry of rule checks: ``(name, default severity, function)`` in execution order."""


def check_names() -> list[str]:
    return [name for name, _severity, _fn in CHECKS]


def rule_checks(doc: TranslatedDocument, options: PipelineOptions,
                pairs: Optional[GlossaryPairs] = None) -> list[QAIssue]:
    """Run every registered rule check and return all issues (page/segment filled in).
    ``pairs`` are the glossary pairs for the language pair; None uses ``doc.glossary``."""
    if pairs is None:
        pairs = _doc_pairs(doc)
    issues: list[QAIssue] = []
    for name, _severity, fn in CHECKS:
        found = fn(doc, options, pairs)
        if found:
            log.debug("check %s: %d issue(s)", name, len(found))
        issues.extend(found)
    log.info("rule checks: %d issue(s) on %d translatable segment(s)", len(issues), len(_checked(doc)))
    return issues


# --------------------------------------------------------------------------- #
# Output-file checks
# --------------------------------------------------------------------------- #

OUTPUT_CHECK_NAMES = ("output_pages", "output_geometry", "output_text", "output_leftovers", "output_fonts")


def _output_issue(check: str, severity: Severity, message: str, page: Optional[int] = None,
                  **details: object) -> QAIssue:
    return QAIssue(check=check, severity=severity, message=message, page=page, details=dict(details),
                   fixable=False)


def _image_boxes(page: pymupdf.Page) -> list[tuple[float, float, float, float]]:
    boxes = []
    for entry in page.get_image_info():
        x0, y0, x1, y1 = entry["bbox"]
        if x1 - x0 > 0 and y1 - y0 > 0:
            boxes.append((float(x0), float(y0), float(x1), float(y1)))
    return boxes


def _unmatched_boxes(a: list[tuple[float, float, float, float]], b: list[tuple[float, float, float, float]],
                     tol: float) -> tuple[list[tuple[float, ...]], list[tuple[float, ...]]]:
    """Boxes of ``a`` without a counterpart in ``b`` (within ``tol`` on every edge) and vice versa."""
    remaining = list(b)
    only_a: list[tuple[float, ...]] = []
    for box in a:
        for j, other in enumerate(remaining):
            if all(abs(u - v) <= tol for u, v in zip(box, other)):
                remaining.pop(j)
                break
        else:
            only_a.append(box)
    return only_a, remaining


def _format_boxes(boxes: list[tuple[float, ...]]) -> str:
    return ", ".join("(" + ", ".join(f"{v:.1f}" for v in box) + ")" for box in boxes)


def _inline_picture_areas(doc: Optional[TranslatedDocument], index: int) -> list[tuple[float, float, float, float]]:
    """Rendered boxes of the segments on page ``index`` that draw inline pictures."""
    if doc is None:
        return []
    out = []
    for seg in doc.segments:
        if seg.page == index and seg.anchors and seg.render is not None and seg.render.bbox is not None:
            b = seg.render.bbox
            out.append((b.x0 - 12, b.y0 - 12, b.x1 + 12, b.y1 + 12))  # a picture may stand proud of its line
    return out


def _geometry_issues(src_page: pymupdf.Page, out_page: pymupdf.Page, index: int,
                     doc: Optional[TranslatedDocument] = None) -> list[QAIssue]:
    issues: list[QAIssue] = []
    sw, sh, ow, oh = src_page.rect.width, src_page.rect.height, out_page.rect.width, out_page.rect.height
    if abs(sw - ow) > PAGE_SIZE_TOLERANCE_PT or abs(sh - oh) > PAGE_SIZE_TOLERANCE_PT \
            or src_page.rotation != out_page.rotation:
        issues.append(_output_issue(
            "output_geometry", "error",
            f"Page {index + 1} changed size: {sw:.1f} x {sh:.1f} pt (rotation {src_page.rotation}) in the source, "
            f"{ow:.1f} x {oh:.1f} pt (rotation {out_page.rotation}) in the output", index,
            source_size=[round(sw, 2), round(sh, 2)], output_size=[round(ow, 2), round(oh, 2)]))
    missing, added = _unmatched_boxes(_image_boxes(src_page), _image_boxes(out_page), GEOMETRY_TOLERANCE_PT)
    areas = _inline_picture_areas(doc, index)
    added = [b for b in added if not any(a[0] <= b[0] and a[1] <= b[1] and b[2] <= a[2] and b[3] <= a[3]
                                         for a in areas)]  # inline pictures drawn inside translated text
    if missing or added:
        parts = []
        if missing:
            parts.append(f"{len(missing)} image(s) missing or moved from {_format_boxes(missing)}")
        if added:
            parts.append(f"{len(added)} unexpected image placement(s) at {_format_boxes(added)}")
        issues.append(_output_issue(
            "output_geometry", "error", f"Image placement on page {index + 1} differs from the source: "
            + "; ".join(parts), index, missing=[list(b) for b in missing], added=[list(b) for b in added]))
    return issues


def _norm_text(text: str) -> str:
    t = unicodedata.normalize("NFKC", ANCHOR_RE.sub("", text)).casefold().replace("\xad", "")
    return re.sub(r"\s+", "", t)


def _text_issues(doc: TranslatedDocument, page_texts: dict[int, str]) -> list[QAIssue]:
    issues: list[QAIssue] = []
    for index, text in page_texts.items():
        segs = [s for s in doc.segments
                if s.page == index and s.kind == SegmentKind.TEXT and s.translate and _is_translated(s)]
        if not segs:
            continue
        page_norm = _norm_text(text)
        found = [s for s in segs if _norm_text(s.translated_text or "")[:OUTPUT_TEXT_PREFIX_CHARS] in page_norm]
        if len(found) < OUTPUT_TEXT_MIN_FOUND * len(segs):
            missing = [s for s in segs if s not in found]
            issues.append(_output_issue(
                "output_text", "error",
                f"Only {len(found)} of {len(segs)} translated text blocks on page {index + 1} are extractable from "
                f"the output PDF (at least half are required); e.g. \"{_excerpt(missing[0].translated_text or '')}\" "
                f"was not placed as real text", index, found=len(found), expected=len(segs),
                missing_segments=[s.id for s in missing[:20]]))
    return issues


def _leftover_issues(doc: TranslatedDocument, page_texts: dict[int, str]) -> list[QAIssue]:
    keys = distinctive_source_keys(doc.source_lang, doc.target_lang)
    if not keys:
        log.info("leftover check skipped: %s and %s share a script", doc.source_lang.value, doc.target_lang.value)
        return []
    runs_re = _runs_re(keys)
    issues: list[QAIssue] = []
    for index, text in page_texts.items():
        segs = [s for s in doc.segments if s.page == index and s.kind == SegmentKind.TEXT]
        if not any(s.translate and _is_translated(s) for s in segs):
            continue  # page not processed by the layout stage
        expected_texts = [s.effective_text for s in segs]
        profile = script_profile(text)
        found = sum(profile[k] for k in keys)
        expected = sum(sum(script_profile(t)[k] for k in keys) for t in expected_texts)
        leftover = found - expected
        total = _letters(text)
        if leftover <= 0 or (leftover < OUTPUT_LEFTOVER_MAX_ABSOLUTE and leftover <= OUTPUT_LEFTOVER_MAX_SHARE * total):
            continue
        examples = [r for r in dict.fromkeys(runs_re.findall(text))
                    if len(r) >= 2 and not any(r in t for t in expected_texts)][:3]
        sample = f" (e.g. {', '.join(repr(e) for e in examples)})" if examples else ""
        issues.append(_output_issue(
            "output_leftovers", "error",
            f"About {leftover} letters of {_lang_name(doc.source_lang)} text remain on page {index + 1} outside "
            f"protected fragments and untranslated blocks ({leftover / max(total, 1):.0%} of the letters on the "
            f"page){sample}; the original text was not fully replaced", index,
            leftover_letters=leftover, page_letters=total, examples=examples))
    return issues


def _font_issues(src: pymupdf.Document, out: pymupdf.Document) -> list[QAIssue]:
    inherited = {entry[3] for page in src for entry in page.get_fonts() if entry[1] == "n/a"}
    issues: list[QAIssue] = []
    for page in out:
        seen: set[str] = set()
        for entry in page.get_fonts():
            basefont = entry[3]
            if entry[1] != "n/a" or basefont in seen:
                continue
            seen.add(basefont)
            if basefont in inherited:
                issues.append(_output_issue(
                    "output_fonts", "warning",
                    f"Font \"{basefont}\" on page {page.number + 1} is not embedded (inherited from the source "
                    f"file; viewers substitute a standard font for it)", page.number, font=basefont, inherited=True))
            else:
                issues.append(_output_issue(
                    "output_fonts", "error",
                    f"Font \"{basefont}\" used for new text on page {page.number + 1} is not embedded; the output "
                    f"must embed every font so it renders identically everywhere", page.number, font=basefont,
                    inherited=False))
    return issues


def output_checks(out_pdf: Union[str, Path], src_pdf: Union[str, Path], doc: TranslatedDocument) -> list[QAIssue]:
    """Compare the exported PDF with the source PDF and the translated document.

    Issues (all ``fixable=False``): ``output_pages`` (page count), ``output_geometry``
    (page size / rotation and image placement), ``output_text`` (translated text is
    extractable), ``output_leftovers`` (source-script text that should have been
    replaced) and ``output_fonts`` (non-embedded fonts; a warning when the source
    file already used that non-embedded font).
    """
    try:
        out = pymupdf.open(str(out_pdf))
    except Exception as exc:  # noqa: BLE001 - reported as a QA issue, never raised
        return [_output_issue("output_pages", "error", f"The output PDF cannot be opened: {exc}")]
    try:
        src = pymupdf.open(str(src_pdf))
    except Exception as exc:  # noqa: BLE001
        out.close()
        return [_output_issue("output_pages", "error", f"The source PDF cannot be opened for comparison: {exc}")]
    issues: list[QAIssue] = []
    try:
        if out.page_count != src.page_count:
            issues.append(_output_issue(
                "output_pages", "error",
                f"The output has {out.page_count} page(s) but the source has {src.page_count}",
                source_pages=src.page_count, output_pages=out.page_count))
        common = min(out.page_count, src.page_count)
        for i in range(common):
            issues.extend(_geometry_issues(src[i], out[i], i, doc))
        page_texts = {i: out[i].get_text() for i in range(common)}
        issues.extend(_text_issues(doc, page_texts))
        issues.extend(_leftover_issues(doc, page_texts))
        issues.extend(_font_issues(src, out))
    finally:
        out.close()
        src.close()
    log.info("output checks on %s: %d issue(s)", out_pdf, len(issues))
    return issues


__all__ = [
    "CHECKS", "OUTPUT_CHECK_NAMES", "check_names", "rule_checks", "output_checks", "shorten_hint",
    "distinctive_source_keys", "foreign_letters", "script_ratio", "source_body", "translation_body",
    "used_glossary_pairs", "copied_names",
    "completeness", "placeholders", "numbers", "untranslated", "target_script", "glossary", "length_ratio",
    "formatting", "layout_fit", "image_text",
]
