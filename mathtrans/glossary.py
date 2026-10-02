"""Terminology glossaries: loading, saving, prompt rendering and adherence checks."""
from __future__ import annotations

import csv
import io
import json
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Optional

from .languages import is_cjk
from .models import SUPPORTED_LANGS, Glossary, GlossaryEntry, Lang

DEFAULT_GLOSSARY_PATH = Path(__file__).parent / "data" / "default_glossary.csv"
LANG_CODES = [lang.value for lang in SUPPORTED_LANGS]


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
                terms = {k: str(v) for k, v in row.items() if k in LANG_CODES and v}
                entries.append(GlossaryEntry(terms=terms, note=str(row.get("note", ""))))
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
            if key in LANG_CODES and v.strip():
                terms[key] = v.strip()
            elif key in ("note", "notes", "comment", "备注"):
                note = v.strip()
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
    """Custom entries take precedence over the built-in default glossary."""
    base = default_glossary() if use_default else Glossary(id="empty", name="empty", entries=[])
    return base.merged_with(custom) if custom else base


def glossary_prompt_block(pairs: list[tuple[str, str]], limit: int = 400) -> str:
    """Render term pairs for inclusion in a prompt (stable order = cache friendly)."""
    if not pairs:
        return ""
    lines = [f"{s} => {t}" for s, t in pairs[:limit]]
    return "\n".join(lines)


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).casefold()


def term_present(term: str, text: str, lang: Lang | str) -> bool:
    """Whether ``term`` appears in ``text`` (case-insensitive; tolerant to simple
    inflection for Latin-script languages, e.g. plural endings)."""
    t, x = _norm(term), _norm(text)
    if not t:
        return True
    if t in x:
        return True
    if is_cjk(lang):
        return False
    # crude stemming: drop the last 1-2 characters of the final word of the term
    words = t.split()
    if not words:
        return False
    last = words[-1]
    for cut in (1, 2):
        if len(last) - cut >= 4:
            stem = " ".join(words[:-1] + [last[:-cut]])
            if stem in x:
                return True
    return False


def missing_glossary_terms(source: str, translation: str, pairs: list[tuple[str, str]],
                           src_lang: Lang | str, tgt_lang: Lang | str) -> list[tuple[str, str]]:
    """Pairs whose source term occurs in ``source`` but whose target term is absent
    from ``translation``. Longer source terms shadow shorter ones they contain
    (``直角三角形`` hides ``三角形``)."""
    src_norm = _norm(source)
    used: list[tuple[str, str]] = []
    covered: list[str] = []
    for s, t in pairs:  # pairs are sorted longest source first
        sn = _norm(s)
        if sn and sn in src_norm and not any(sn in c for c in covered):
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
