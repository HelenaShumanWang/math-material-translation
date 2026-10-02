"""Protect formulas, numbers and other verbatim fragments with placeholders.

Translators receive text in which every fragment that must survive verbatim
(formulas, numbers, variable names, units, LaTeX, URLs) is replaced by ``⟦n⟧``.
The originals are restored after translation, and QA verifies that every
placeholder came back exactly once.
"""
from __future__ import annotations

import re
from typing import Iterable, Optional

from .languages import is_cjk
from .models import PLACEHOLDER_RE, Lang, make_placeholder, restore_placeholders  # noqa: F401

FUNCTIONS = {
    "sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh",
    "log", "ln", "lg", "exp", "lim", "max", "min", "sup", "inf", "sqrt", "mod", "det", "gcd", "lcm",
    "abs", "dim", "ker", "deg", "rad", "arg",
}
UNITS = {
    "mm", "cm", "dm", "km", "mg", "kg", "ml", "cl", "dl", "ms", "mm²", "cm²", "dm²", "km²", "mm³",
    "cm³", "dm³", "km³", "kb", "mb", "gb", "hz", "khz", "mhz", "kw", "kwh", "km/h", "m/s",
}

OPERATORS = "=+−–×÷±≤≥≠≈∑∏∫√∞∠°∂∇∈∉⊂⊃⊆⊇∪∩∥⊥∝′″‰%^/|·∘⊕⊗→←↔⇒⇔∧∨¬∀∃∅ℝℕℤℚℂ∼≅≡≪≫⌊⌋⌈⌉△▱□⊙⌒≮≯∟∶∷∽≌"
SUPERSUB = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓ"

_TOKEN_RE = re.compile(
    r"""
    (?P<latex>\$\$[^$]+\$\$|\$[^$\n]+\$|\\\([^)]*\\\)|\\\[[^\]]*\\\])
  | (?P<url>https?://\S+|www\.\S+|[\w.+-]+@[\w-]+\.[\w.]+)
  | (?P<num>[0-9０-９]+(?:[.,．][0-9０-９]+)*)
  | (?P<word>[A-Za-zÀ-ÖØ-öø-ɏＡ-Ｚａ-ｚ][A-Za-zÀ-ÖØ-öø-ɏＡ-Ｚａ-ｚ'’]*)
  | (?P<greek>[Α-Ωα-ω])
  | (?P<supsub>[""" + SUPERSUB + r"""]+)
  | (?P<op>[""" + re.escape(OPERATORS) + r"""\-'’!])
  | (?P<br>[()\[\]{}])
  | (?P<dot>[.,:;])
  | (?P<sp>[ \t ]+)
  | (?P<other>.)
    """,
    re.VERBOSE | re.DOTALL,
)

_LABEL_RE = re.compile(r"[A-Z]{1,4}['’]*")

GEOMETRY_WORDS = {
    # en
    "triangle", "triangles", "segment", "segments", "line", "lines", "angle", "angles", "point", "points",
    "quadrilateral", "parallelogram", "rectangle", "square", "circle", "side", "sides", "arc", "chord", "ray",
    "vector", "vectors", "polygon", "trapezoid", "trapezium", "rhombus", "rt", "diagonal", "diagonals", "vertex",
    "vertices", "edge", "edges", "face", "faces", "matrix", "matrices", "set", "sets", "interval", "prism", "pyramid",
    "cube", "cuboid", "sphere", "cone", "cylinder", "plane", "planes", "midpoint", "altitude", "median", "bisector",
    "hypotenuse", "leg", "legs", "base", "height", "radius", "diameter", "tangent", "secant", "centre", "center",
    "pentagon", "hexagon", "octagon", "kite", "tetrahedron",
    # es
    "triángulo", "triángulos", "segmento", "segmentos", "recta", "rectas", "ángulo", "ángulos", "punto", "puntos",
    "cuadrilátero", "paralelogramo", "rectángulo", "cuadrado", "círculo", "lado", "lados", "arco", "cuerda",
    "vértice", "vértices", "diagonal", "vector", "polígono", "trapecio", "rombo", "radio", "diámetro", "altura",
    "mediana", "bisectriz", "hipotenusa", "cateto", "catetos", "centro", "plano", "cubo", "esfera", "cono",
    # pt
    "triângulo", "triângulos", "reta", "retas", "ângulo", "ângulos", "ponto", "pontos", "quadrilátero",
    "retângulo", "quadrado", "lado", "lados", "corda", "vetor", "polígono", "trapézio", "losango", "raio",
    "diâmetro", "mediana", "bissetriz", "hipotenusa", "cateto", "catetos", "plano", "esfera",
}
"""Words after which an upper-case token (``triangle ABC``) is a geometric label."""


class _Tok:
    __slots__ = ("kind", "text")

    def __init__(self, kind: str, text: str):
        self.kind = kind
        self.text = text


def _classify_word(w: str) -> str:
    """Return the atom class of a Latin word: func | unit | label | letter | word."""
    lw = w.lower().rstrip("'’")
    if lw in FUNCTIONS:
        return "func"
    if lw in UNITS:
        return "unit"
    if _LABEL_RE.fullmatch(w):
        return "label" if (len(lw) >= 2 or "'" in w or "’" in w) else "letter"
    if len(lw) == 1:
        return "letter"
    return "word"


def _tokenize(text: str, cjk_source: bool = True) -> list[_Tok]:
    toks: list[_Tok] = []
    for m in _TOKEN_RE.finditer(text):
        kind = m.lastgroup or "other"
        t = m.group(0)
        if kind == "word":
            kind = _classify_word(t)
        toks.append(_Tok(kind, t))
    if not cjk_source:
        _demote_isolated_letters(toks)
    return toks


def _demote_isolated_letters(toks: list[_Tok]) -> None:
    """In Latin-script sources a lone letter is usually a word ("a", "y", "I"),
    not a variable, and an upper-case word of 2-4 letters is often a heading or
    acronym ("STEP 1", "UNIT 3", "NOTE", "PDF") rather than a geometric label.
    Keep them as math atoms only when they are glued to another atom ("2x",
    "f(x)", "x²", "AB²"), sit next to an operator ("x = 3", "AB = 5", "∠ABC") or,
    for labels, follow a geometric noun ("triangle ABC", "segmento PQ")."""
    n = len(toks)

    def neighbour(idx: int, step: int) -> tuple[Optional[_Tok], bool]:
        j = idx + step
        spaced = False
        while 0 <= j < n and toks[j].kind == "sp":
            spaced = True
            j += step
        return (toks[j] if 0 <= j < n else None), spaced

    for i, t in enumerate(toks):
        if t.kind not in ("letter", "label"):
            continue
        prev, prev_sp = neighbour(i, -1)
        nxt, nxt_sp = neighbour(i, +1)
        glued = (prev is not None and not prev_sp and prev.kind in _ATOMS) or \
                (nxt is not None and not nxt_sp and nxt.kind in _ATOMS)
        near_op = (prev is not None and prev.kind == "op") or (nxt is not None and nxt.kind == "op")
        after_geometry = t.kind == "label" and prev is not None and prev.kind == "word" \
            and prev.text.lower() in GEOMETRY_WORDS
        if not (glued or near_op or after_geometry):
            t.kind = "word"


_ATOMS = {"num", "greek", "supsub", "op", "br", "func", "unit", "label", "letter"}


def _qualifies(run: list[_Tok], cjk_source: bool) -> bool:
    kinds = {t.kind for t in run}
    n_alnum = sum(1 for t in run if t.kind in ("num", "greek", "letter", "label", "func", "unit"))
    if n_alnum == 0:
        return False
    if "num" in kinds or "greek" in kinds or "supsub" in kinds or "label" in kinds:
        return True
    ops = [t for t in run if t.kind == "op"]
    if ops and n_alnum >= 1:
        return True
    if "br" in kinds and ("letter" in kinds or "func" in kinds):
        return True
    if cjk_source and ("letter" in kinds or "func" in kinds):
        return True
    return False


def _clean_run(text: str) -> str:
    """Strip sentence punctuation and unbalanced brackets at the run edges."""
    t = text.strip()
    while t and t[-1] in ".,:;-–− ":
        t = t[:-1]
    while t and t[0] in ".,:; ":
        t = t[1:]
    if t.startswith("(") and ")" not in t:
        t = t[1:]
    if t.endswith(")") and "(" not in t:
        t = t[:-1]
    if t.startswith("[") and "]" not in t:
        t = t[1:]
    if t.endswith("]") and "[" not in t:
        t = t[:-1]
    return t.strip()


def find_protected_fragments(text: str, src_lang: Lang | str | None = None) -> list[tuple[int, int, str]]:
    """Return (start, end, fragment) for every fragment that must be kept verbatim."""
    cjk_source = bool(src_lang) and is_cjk(src_lang)
    toks = _tokenize(text, cjk_source)
    spans: list[tuple[int, int, str]] = []
    pos = 0
    i = 0
    n = len(toks)
    while i < n:
        tok = toks[i]
        start = pos
        if tok.kind in ("latex", "url"):
            spans.append((start, start + len(tok.text), tok.text))
            pos += len(tok.text)
            i += 1
            continue
        if tok.kind not in _ATOMS:
            pos += len(tok.text)
            i += 1
            continue
        # build a run of atoms, allowing single spaces between atoms
        run: list[_Tok] = []
        j = i
        run_end = pos
        p = pos
        while j < n:
            t = toks[j]
            if t.kind == "dot":
                nxt = toks[j + 1] if j + 1 < n else None
                if nxt is None or nxt.kind not in _ATOMS:
                    break  # sentence punctuation or a list separator ("2, 3, 5") ends the run
                run.append(t)
                p += len(t.text)
                run_end = p
                j += 1
                continue
            if t.kind in _ATOMS:
                run.append(t)
                p += len(t.text)
                run_end = p
                j += 1
                continue
            if t.kind == "sp" and j + 1 < n and toks[j + 1].kind in _ATOMS and run:
                run.append(t)
                p += len(t.text)
                j += 1
                continue
            break
        # trim trailing dots / spaces from the run token list for qualification
        core = [t for t in run if t.kind not in ("sp", "dot")]
        if core and _qualifies(core, cjk_source):
            raw = text[start:run_end]
            frag = _clean_run(raw)
            if frag:
                offset = raw.find(frag)
                spans.append((start + offset, start + offset + len(frag), frag))
        pos = run_end if run else pos + len(tok.text)
        i = j if run else i + 1
    # filter: drop fragments that are only punctuation/brackets
    out = []
    for s, e, f in spans:
        if any(ch.isalnum() or ch in SUPERSUB or ("Α" <= ch <= "ω") for ch in f):
            out.append((s, e, f))
    return out


def protect_text(
    text: str,
    src_lang: Lang | str | None = None,
    extra_fragments: Optional[Iterable[str]] = None,
) -> tuple[str, list[str]]:
    """Replace verbatim fragments by placeholders.

    ``extra_fragments`` are exact substrings (e.g. spans typeset in a math font)
    that are protected first, before the heuristic scan.
    Returns ``(protected_text, fragments)`` where ``fragments[n]`` is the
    original of ``⟦n⟧``.
    """
    fragments: list[str] = []
    protected_ranges: list[tuple[int, int, str]] = []

    extras = sorted({f for f in (extra_fragments or []) if f and f.strip()}, key=len, reverse=True)
    taken = [False] * len(text)
    for frag in extras:
        start = 0
        while True:
            idx = text.find(frag, start)
            if idx < 0:
                break
            if not any(taken[idx: idx + len(frag)]):
                protected_ranges.append((idx, idx + len(frag), frag))
                for k in range(idx, idx + len(frag)):
                    taken[k] = True
            start = idx + len(frag)

    for s, e, f in find_protected_fragments(text, src_lang):
        if not any(taken[s:e]):
            protected_ranges.append((s, e, f))
            for k in range(s, e):
                taken[k] = True

    protected_ranges.sort()
    out: list[str] = []
    last = 0
    for s, e, f in protected_ranges:
        out.append(text[last:s])
        out.append(make_placeholder(len(fragments)))
        fragments.append(f)
        last = e
    out.append(text[last:])
    return "".join(out), fragments


def is_fully_protected(protected_text: str) -> bool:
    """True when nothing translatable remains (only placeholders, punctuation, spaces)."""
    rest = PLACEHOLDER_RE.sub("", protected_text)
    return not any(ch.isalpha() for ch in rest)


def verify_placeholders(protected_text: str, translated_raw: str) -> list[str]:
    """Problems with placeholder usage in a translation (empty list = OK)."""
    expected = sorted(int(m.group(1)) for m in PLACEHOLDER_RE.finditer(protected_text))
    got = sorted(int(m.group(1)) for m in PLACEHOLDER_RE.finditer(translated_raw))
    problems: list[str] = []
    exp_set, got_set = set(expected), set(got)
    missing = sorted(exp_set - got_set)
    unknown = sorted(got_set - exp_set)
    dup = sorted({g for g in got if got.count(g) > 1 and expected.count(g) < got.count(g)})
    if missing:
        problems.append("missing placeholders: " + ", ".join(make_placeholder(i) for i in missing))
    if unknown:
        problems.append("unknown placeholders: " + ", ".join(make_placeholder(i) for i in unknown))
    if dup:
        problems.append("duplicated placeholders: " + ", ".join(make_placeholder(i) for i in dup))
    # malformed look-alikes such as "⟦ 3 ⟧" or "[[3]]"
    if re.search(r"⟦\s+\d+\s*⟧|⟦\d+\s+⟧|\[\[\d+\]\]", translated_raw):
        problems.append("malformed placeholder syntax")
    return problems
