"""Terminology glossaries: loading, saving, prompt rendering and adherence checks."""
from __future__ import annotations

import csv
import io
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Optional

from .languages import is_cjk
from .models import SUPPORTED_LANGS, Glossary, GlossaryEntry, Lang, clean_term

DEFAULT_GLOSSARY_PATH = Path(__file__).parent / "data" / "default_glossary.csv"
LANG_CODES = [lang.value for lang in SUPPORTED_LANGS]
CJK_MIN_ENFORCED_TERM_CHARS = 2
"""Shortest CJK source term whose use is *enforced* by the QA glossary check. One-character
terms (解, 角, 圆, 高 / 円, 弧 / 각, 원, 호, 현) occur inside unrelated words (解释, 5 角, 圆柱,
120 円, 각 변, 500원, 번호), so they stay in the prompt as hints but are never checked."""


def parse_glossary_text(text: str, fmt: Optional[str] = None, glossary_id: str = "custom",
                        name: str = "Custom glossary") -> Glossary:
    """Parse CSV/TSV (header with language codes, optional ``note`` column) or JSON."""
    text = text.lstrip("﻿").strip()
    if not text:
        return Glossary(id=glossary_id, name=name, entries=[])
    if fmt is None:
        fmt = "json" if text[0] in "[{" else "csv"
    if fmt == "json":
        data = json.loads(text)
        if isinstance(data, dict) and "entries" in data:
            g = Glossary.model_validate(data)
            if glossary_id != "custom":
                g.id = glossary_id
            return g
        entries = []
        for row in data:
            if "terms" in row:
                entries.append(GlossaryEntry.model_validate(row))
            else:
                terms = {k: clean_term(v) for k, v in row.items() if k in LANG_CODES and v and clean_term(v)}
                entries.append(GlossaryEntry(terms=terms, note=clean_term(row.get("note", ""))))
        return Glossary(id=glossary_id, name=name, entries=entries)
    dialect = "excel-tab" if ("\t" in text.splitlines()[0] and "," not in text.splitlines()[0]) else "excel"
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    entries = []
    for row in reader:
        terms = {}
        note = ""
        for k, v in row.items():
            if k is None or v is None:
                continue
            key = k.strip().lower()
            cleaned = clean_term(v)  # one line of plain text (a quoted CSV cell may wrap)
            if key in LANG_CODES and cleaned:
                terms[key] = cleaned
            elif key in ("note", "notes", "comment", "备注"):
                note = cleaned
        if len(terms) >= 2:
            entries.append(GlossaryEntry(terms=terms, note=note))
    return Glossary(id=glossary_id, name=name, entries=entries)


def load_glossary(path: str | Path, glossary_id: Optional[str] = None) -> Glossary:
    p = Path(path)
    fmt = "json" if p.suffix.lower() == ".json" else "csv"
    return parse_glossary_text(p.read_text(encoding="utf-8"), fmt=fmt,
                               glossary_id=glossary_id or p.stem, name=p.stem)


def save_glossary(glossary: Glossary, path: str | Path) -> None:
    p = Path(path)
    if p.suffix.lower() == ".json":
        p.write_text(glossary.model_dump_json(indent=2), encoding="utf-8")
        return
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(LANG_CODES + ["note"])
        for e in glossary.entries:
            w.writerow([e.terms.get(c, "") for c in LANG_CODES] + [e.note])


def glossary_template_csv() -> str:
    return "zh,en,pt,es,ja,ko,note\n勾股定理,Pythagorean theorem,Teorema de Pitágoras,Teorema de Pitágoras,三平方の定理,피타고라스 정리,example row\n"


@lru_cache(maxsize=1)
def default_glossary() -> Glossary:
    return load_glossary(DEFAULT_GLOSSARY_PATH, glossary_id="default")


def effective_glossary(custom: Optional[Glossary], use_default: bool = True) -> Glossary:
    """Custom entries take precedence over the built-in default glossary, per source
    term and language pair (``Glossary.pairs``): a custom zh/en entry replaces the
    built-in zh->en pair of the same term and leaves its pt/es/ja/ko pairs in place."""
    base = default_glossary() if use_default else Glossary(id="empty", name="empty", entries=[])
    return base.merged_with(custom) if custom else base


def glossary_prompt_block(pairs: list[tuple[str, str]], limit: int = 400) -> str:
    """Render term pairs for inclusion in a prompt, one pair per line as
    ``"source" => "target"`` with JSON-quoted terms (stable order = cache friendly).
    Quoting keeps every term inside its line whatever it contains (line breaks become
    ``\\n``), so glossary data can never add a line of its own to the system prompt."""
    if not pairs:
        return ""
    lines = [f"{json.dumps(s, ensure_ascii=False)} => {json.dumps(t, ensure_ascii=False)}"
             for s, t in pairs[:limit]]
    return "\n".join(lines)


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).casefold()


_WS_RE = re.compile(r"\s+")


def _fold(s: str) -> str:
    """NFKD, combining marks stripped, casefolded: ``raízes`` == ``raizes``,
    ``ecuación`` == ``ecuacion`` (plurals shift accents in Spanish and Portuguese)."""
    decomposed = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).casefold()


def _latin_word_re(word: str) -> str:
    """Pattern for one (folded) word of a Latin-script term with its usual inflections:
    plural endings on *every* word (``triángulos rectángulos``), Portuguese ``-ão``
    (``equações``), ``-z`` (``raíz`` -> ``raíces`` / ``raízes``), ``-m`` (``afim`` ->
    ``afins``), Latin plurals (``vertex`` -> ``vertices``, ``axis`` -> ``axes``, ``radius``
    -> ``radii``) and English ``-y`` -> ``-ies``. A term that is already plural
    (``coordinates``) also matches its singular (``coordinate axes``)."""
    if word.endswith("ao"):
        return re.escape(word[:-2]) + r"(?:ao|oes|aos|aes)"
    if word.endswith("z"):
        return re.escape(word[:-1]) + r"(?:z|zes|ces)"
    if word.endswith("m"):
        return re.escape(word[:-1]) + r"(?:m|ms|ns)"
    if word.endswith(("ex", "ix")):
        return re.escape(word[:-2]) + r"(?:ex|ix|ices|exes|ixes)"
    if word.endswith("is"):
        return re.escape(word[:-2]) + r"(?:is|es)"
    if word.endswith("us"):
        return re.escape(word[:-2]) + r"(?:us|i|uses)"
    if word.endswith("y") and len(word) > 2 and word[-2] not in "aeiou":
        return re.escape(word[:-1]) + r"(?:y|ies)"
    if word.endswith("s") and len(word) > 3:
        word = word[:-1]
    return re.escape(word) + r"(?:s|es)?"


@lru_cache(maxsize=4096)
def _latin_term_re(term: str) -> re.Pattern[str]:
    """Substring pattern (deliberately without word boundaries, as before: a presence
    check on the target side must stay lenient) for a folded Latin-script term."""
    return re.compile(r"[\s\-]+".join(_latin_word_re(w) for w in term.split()))


def term_present(term: str, text: str, lang: Lang | str) -> bool:
    """Whether ``term`` appears in ``text``: case- and accent-insensitive with the usual
    inflections of every word for Latin-script languages (``triángulos rectángulos``,
    ``raízes quadradas``, ``equações``), whitespace-insensitive for CJK languages
    (``직각 삼각형`` == ``직각삼각형``)."""
    if is_cjk(lang):
        t, x = _norm(term).strip(), _norm(text)
        return not t or t in x or _WS_RE.sub("", t) in _WS_RE.sub("", x)
    t = _fold(term).strip()
    return not t or _latin_term_re(t).search(_fold(text)) is not None


def is_enforced_source_term(term: str, src_lang: Lang | str) -> bool:
    """Whether the QA glossary check enforces ``term`` when it occurs in a source of
    ``src_lang``: every non-blank term except one-character CJK terms (see
    :data:`CJK_MIN_ENFORCED_TERM_CHARS`). The prompt shows every term regardless."""
    t = unicodedata.normalize("NFKC", term).strip()
    if not t:
        return False
    return not is_cjk(src_lang) or len(t) >= CJK_MIN_ENFORCED_TERM_CHARS


def missing_glossary_terms(source: str, translation: str, pairs: list[tuple[str, str]],
                           src_lang: Lang | str, tgt_lang: Lang | str) -> list[tuple[str, str]]:
    """Pairs whose source term occurs in ``source`` but whose target term is absent
    from ``translation``. Longer source terms shadow shorter ones they contain
    (``直角三角形`` hides ``三角形``); one-character CJK source terms are never enforced
    (:func:`is_enforced_source_term`)."""
    src_norm = _norm(source)
    used: list[tuple[str, str]] = []
    covered: list[str] = []
    for s, t in pairs:  # pairs are sorted longest source first
        if not is_enforced_source_term(s, src_lang):
            continue
        sn = _norm(s)
        if sn in src_norm and not any(sn in c for c in covered):
            used.append((s, t))
            covered.append(sn)
    return [(s, t) for s, t in used if not term_present(t, translation, tgt_lang)]


def apply_glossary_literal(text: str, pairs: list[tuple[str, str]]) -> str:
    """Deterministic literal substitution (used by the offline mock translator)."""
    out = text
    for s, t in pairs:
        if s:
            out = out.replace(s, t)
    return out
