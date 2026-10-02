"""Tests for the automatic QA package (rule checks, output checks, loop, report)."""
from __future__ import annotations

import pymupdf

from mathtrans.glossary import default_glossary
from mathtrans.interfaces import TranslationError
from mathtrans.models import (BBox, ImageRef, Lang, PipelineOptions, QAIssue, QAReport, QARound, RenderInfo,
                              ReviewFinding, SegmentKind, TextSegment, TranslatedDocument,
                              make_placeholder)
from mathtrans.protect import protect_text
from mathtrans.qa import CHECKS, issues_by_page, output_checks, report_markdown, rule_checks, run_qa_loop, summarize
from mathtrans.qa import checks as C
from mathtrans.qa.loop import apply_feedback, review_issue
from mathtrans.samples import sample_texts

BOX = BBox(x0=60, y0=100, x1=300, y1=140)


def seg(sid: str, source: str, translated: str | None, *, src: str = "zh", page: int = 0,
        raw: str | None = None, kind: SegmentKind = SegmentKind.TEXT, translate: bool = True,
        render: RenderInfo | None = None, protect: bool = True, bbox: BBox = BOX, **kw) -> TextSegment:
    """Build a segment the way the extractor + translator would (placeholders filled in)."""
    protected_text, fragments = protect_text(source, src) if protect else (source, [])
    if raw is None and translated is not None and fragments:
        raw = translated
        for i, frag in sorted(enumerate(fragments), key=lambda p: -len(p[1])):
            raw = raw.replace(frag, make_placeholder(i), 1)
    return TextSegment(id=sid, page=page, kind=kind, bbox=bbox, source_text=source, protected_text=protected_text,
                       protected=fragments, translate=translate, translation_raw=raw, translated_text=translated,
                       render=render, **kw)


def doc(*segments: TextSegment, src: str = "zh", tgt: str = "en") -> TranslatedDocument:
    pages = sorted({s.page for s in segments} | {0})
    return TranslatedDocument(source_path="sample.pdf", source_lang=Lang(src), target_lang=Lang(tgt),
                              pages=[{"index": p, "width": 595, "height": 842} for p in range(max(pages) + 1)],
                              segments=list(segments))


def opts(tgt: str = "en", **kw) -> PipelineOptions:
    return PipelineOptions(target_lang=Lang(tgt), **kw)


def names(issues: list[QAIssue], check: str | None = None) -> list[str]:
    return [i.check for i in issues if check is None or i.check == check]


# --------------------------------------------------------------------------- #
# rule checks
# --------------------------------------------------------------------------- #


def test_registry_names_and_severities():
    assert [c[0] for c in CHECKS] == ["completeness", "placeholders", "numbers", "untranslated", "target_script",
                                      "glossary", "length_ratio", "formatting", "layout_fit", "image_text"]
    assert dict((c[0], c[1]) for c in CHECKS)["length_ratio"] == "warning"
    assert all(callable(c[2]) for c in CHECKS)


def test_completeness_positive_negative_and_skipped_segments():
    d = doc(seg("a", "求斜边的长度。", None), seg("b", "求斜边的长度。", "Find the hypotenuse."),
            seg("c", "纯数字 123", None, translate=False), seg("d", "   ", None))
    issues = C.completeness(d, opts(), [])
    assert [i.segment_id for i in issues] == ["a"]
    assert issues[0].severity == "error" and issues[0].fixable and issues[0].page == 0


def test_placeholders_missing_and_ok():
    source = "解：由勾股定理得 c² = 3² + 4² = 25，所以 c = 5 cm。"
    good = seg("ok", source, "Solution: by the Pythagorean theorem c² = 3² + 4² = 25, so c = 5 cm.")
    assert good.translation_raw is not None and "⟦0⟧" in good.translation_raw
    bad = seg("bad", source, "Solution: by the Pythagorean theorem, so c = 5 cm.",
              raw="Solution: by the Pythagorean theorem, so ⟦1⟧.")
    issues = C.placeholders(doc(good, bad), opts(), [])
    assert [i.segment_id for i in issues] == ["bad"]
    assert "missing placeholders: ⟦0⟧" in issues[0].message and "c² = 3² + 4² = 25" in issues[0].message
    # without a raw translation the restored fragments themselves must survive
    no_raw = TextSegment(id="r", page=0, bbox=BOX, source_text="AB = 6", protected_text="⟦0⟧",
                         protected=["AB = 6"], translated_text="AB equals six")
    assert names(C.placeholders(doc(no_raw), opts(), [])) == ["placeholders"]


def test_numbers_missing_fullwidth_and_cjk_numerals():
    missing = seg("m", "斜边长为 13，一条直角边长为 5。", "The hypotenuse is 13 and one leg is 6.",
                  raw="The hypotenuse is ⟦0⟧ and one leg is 6.")
    fullwidth = seg("f", "共有２５道题。", "There are 25 problems.", raw="There are 25 problems.")
    spelled = seg("s", "4 congruent triangles", "四个全等的三角形", src="en", raw="四个全等的三角形")
    cjk_source = seg("c", "三个正方形", "three squares")
    issues = C.numbers(doc(missing, fullwidth, spelled, cjk_source), opts(), [])
    assert [i.segment_id for i in issues] == ["m"]
    assert 'Number "5" from the source is missing' in issues[0].message and issues[0].details["number"] == "5"
    # enclosed numbers are the same number in another style; three-digit CJK numerals count
    circled = seg("c", "① 求斜边。", "1. Find the hypotenuse.", raw="1. Find the hypotenuse.")
    paren = seg("p", "(1) 求斜边。", "① Find the hypotenuse.", raw="① Find the hypotenuse.")
    hundreds = seg("h", "Sum 105 and 120 and 200", "一百零五と百二十と二百を足す", src="en", raw="一百零五と百二十と二百を足す")
    lost = seg("x", "Sum 105 and 120", "一百五十と百二十を足す", src="en", raw="一百五十と百二十を足す")
    issues = C.numbers(doc(circled, paren, hundreds, lost, src="en", tgt="ja"), opts("ja"), [])
    assert [(i.segment_id, i.details["number"]) for i in issues] == [("x", "105")]
    assert C._cjk_numerals("13") == ("十三",) and C._cjk_numerals("105") == ("一百零五", "百五")
    assert C._cjk_numerals("1000") == () and "两百" in C._cjk_numerals("200") and "百十" in C._cjk_numerals("110")
    assert C._spelled_count("十五个", "5") == 0 and C._spelled_count("五个和十五个", "5") == 1
    assert C._spelled_count("二十五", "25") == 1 and C._spelled_count("第一百二十五页", "125") == 1


def test_untranslated_foreign_letters_identical_and_tiny_label_allowance():
    leftover = seg("l", "在直角三角形中，斜边最长。", "In a right triangle the 斜边 is the longest.",
                   raw="In a right triangle the 斜边 is the longest.")
    identical = seg("i", "求斜边的长度。", "求斜边的长度。", raw="求斜边的长度。")
    tiny = seg("t", "斜边 c", "斜边 c")  # 2 source letters: up to 2 foreign letters tolerated
    formula = seg("x", "a²+b²=c²", "a²+b²=c²")  # fully protected: identical is fine
    fine = seg("ok", "求斜边的长度。", "Find the length of the hypotenuse.")
    issues = C.untranslated(doc(leftover, identical, tiny, formula, fine), opts(), [])
    assert sorted(i.segment_id for i in issues) == ["i", "l"]
    by_id = {i.segment_id: i for i in issues}
    assert '"斜边"' in by_id["l"].message and "6 letter(s)" in by_id["i"].message
    # same-script pair: an untouched sentence is caught by the identity rule, a short
    # identical label is accepted as a cognate ("Nota", "Figura 1-1", "Teorema de Pitágoras")
    copied = seg("c", "Find the length of the hypotenuse.", "Find the length of the hypotenuse.", src="en")
    cognate = seg("n", "Nota", "Nota", src="en")
    figure = seg("f", "Teorema de Pitágoras", "Teorema de Pitágoras", src="es")
    issues = C.untranslated(doc(copied, cognate, figure, src="en", tgt="es"), opts("es"), [])
    assert [i.segment_id for i in issues] == ["c"] and "identical" in issues[0].message
    # zh -> ja share Han: short identical terms are fine, a whole identical sentence is not
    term = seg("t", "直角三角形", "直角三角形")
    sentence = seg("s", "直角三角形两直角边的平方和等于斜边的平方", "直角三角形两直角边的平方和等于斜边的平方")
    issues = C.untranslated(doc(term, sentence, tgt="ja"), opts("ja"), [])
    assert [i.segment_id for i in issues] == ["s"]


def test_untranslated_hanja_in_korean_and_copied_latin_runs():
    # Han characters are untranslated text in a Korean translation (hanja is not used in textbooks)
    hanja = seg("h", "求斜边的长度。", "斜边의 길이를 구하시오.", raw="斜边의 길이를 구하시오.")
    fine = seg("k", "求斜边的长度。", "빗변의 길이를 구하시오.")
    issues = C.untranslated(doc(hanja, fine, tgt="ko"), opts("ko"), [])
    assert [i.segment_id for i in issues] == ["h"] and '"斜边"' in issues[0].message
    assert C.distinctive_source_keys("zh", "ko") == ("han",)
    assert C.target_script(doc(hanja, tgt="ko"), opts("ko"), []) == []  # 2 of 8 letters are Han: ratio 0.75
    # a run of >= 3 source words copied verbatim into a CJK translation is untranslated even
    # though Latin letters are tolerated in general (variables "a" and "b" are fine)
    copied = seg("c", "The sum of the squares of the legs equals the square of the hypotenuse.",
                 "直角边 squares of the legs 等于斜边的平方。", src="en", raw="直角边 squares of the legs 等于斜边的平方。")
    variables = seg("v", "If the legs have lengths a and b, then a²+b²=c².", "如果直角边的长为 a 和 b，那么 a²+b²=c²。",
                    src="en")
    name = seg("n", "This is the theorem of Pythagoras of Samos.", "这是 Pythagoras of Samos 的定理。", src="en",
               raw="这是 Pythagoras of Samos 的定理。")
    issues = C.untranslated(doc(copied, variables, name, src="en", tgt="zh"), opts("zh"), [])
    assert sorted(i.segment_id for i in issues) == ["c", "n"]
    by_id = {i.segment_id: i for i in issues}
    assert by_id["c"].details["copied_runs"] == ["squares of the legs"] and "copied untranslated" in by_id["c"].message
    # not applied between Latin languages (shared words are normal) nor for CJK sources
    same = seg("s", "The area of the square", "El área of the square", src="en")
    assert C.untranslated(doc(same, src="en", tgt="es"), opts("es"), []) == []


def test_target_script_positive_and_negative():
    mixed = seg("m", "Find the length of the hypotenuse.", "Find the length 的斜边。", src="en",
                raw="Find the length 的斜边。")
    good = seg("g", "Find the length of the hypotenuse.", "求斜边的长度。", src="en", raw="求斜边的长度。")
    short = seg("s", "AB", "AB 边", src="en")  # fewer than 4 letters: not judged
    issues = C.target_script(doc(mixed, good, short, src="en", tgt="zh"), opts("zh"), [])
    assert [i.segment_id for i in issues] == ["m"] and "Chinese" in issues[0].message


def test_glossary_check_uses_pairs():
    pairs = default_glossary().pairs("zh", "en")
    wrong = seg("w", "直角三角形的斜边", "the long side of a right triangle")
    right = seg("r", "直角三角形的斜边", "the hypotenuse of a right triangle")
    issues = C.glossary(doc(wrong, right), opts(), pairs)
    assert [(i.segment_id, i.message) for i in issues] == [("w", 'Glossary: translate "斜边" as "hypotenuse"')]
    assert issues[0].details == {"source_term": "斜边", "target_term": "hypotenuse"}
    assert C.glossary(doc(wrong), opts(), []) == []


def test_glossary_latin_sources_use_inflected_whole_words():
    pairs_es = default_glossary().pairs("es", "zh")
    # "rectángulos" is the adjective of "triángulos rectángulos": only the longer term counts
    used = C.used_glossary_pairs("Cuatro triángulos rectángulos congruentes forman un cuadrado.", pairs_es, "es")
    assert ("triángulo rectángulo", "直角三角形") in used and ("rectángulo", "矩形") not in used
    assert ("triángulo", "三角形") not in used and ("cuadrado", "正方形") in used
    pairs_en = default_glossary().pairs("en", "zh")
    used = C.used_glossary_pairs("The legs of an elegant triangle; the lego legend.", pairs_en, "en")
    assert ("leg", "直角边") in used and ("triangle", "三角形") in used and len(used) == 2
    plural = seg("p", "The legs of a right triangle are 3 cm and 4 cm.", "直角三角形的两条直角边分别为 3 cm 和 4 cm。",
                 src="en")
    missing = seg("m", "The legs of a right triangle are 3 cm and 4 cm.", "直角三角形的两条边分别为 3 cm 和 4 cm。",
                  src="en")
    issues = C.glossary(doc(plural, missing, src="en", tgt="zh"), opts("zh"), pairs_en)
    assert [(i.segment_id, i.details["target_term"]) for i in issues] == [("m", "直角边")]
    pairs_pt = default_glossary().pairs("pt", "en")
    assert ("equação", "equation") in C.used_glossary_pairs("Resolva as equações.", pairs_pt, "pt")
    # the inflected form must also be *enforced*, not only detected
    wrong = seg("w", "Resolva as equações.", "Solve the formulas.", src="pt")
    right = seg("r", "Resolva as equações.", "Solve the equations.", src="pt")
    issues = C.glossary(doc(wrong, right, src="pt", tgt="en"), opts(), pairs_pt)
    assert [(i.segment_id, i.details["target_term"]) for i in issues] == [("w", "equation")]
    # CJK shadowing is per occurrence: a standalone 三角形 next to 直角三角形 still counts
    pairs_zh = default_glossary().pairs("zh", "en")
    used = C.used_glossary_pairs("直角三角形是三角形。", pairs_zh, "zh")
    assert ("直角三角形", "right triangle") in used and ("三角形", "triangle") in used
    assert ("三角形", "triangle") not in C.used_glossary_pairs("直角三角形。", pairs_zh, "zh")
    # pairs default to the document glossary when a check is called the (doc, options) way
    d = doc(seg("g", "直角三角形的斜边", "the long side of a right triangle"))
    d.glossary = default_glossary()
    assert [i.details["target_term"] for i in C.glossary(d, opts())] == ["hypotenuse"]
    assert "glossary" in names(rule_checks(d, opts())) and C.glossary(doc(wrong, src="pt", tgt="en"), opts()) == []


def test_length_ratio_warning_bounds():
    source = "在直角三角形中，两条直角边的平方和等于斜边的平方。"
    too_short = seg("s", source, "Legs.")
    too_long = seg("l", source, "In a right triangle " * 20)
    normal = seg("n", source, "In a right triangle, the sum of the squares of the legs equals the square of the hypotenuse.")
    tiny = seg("t", "求斜边。", "x")  # source shorter than 8 characters: skipped
    issues = C.length_ratio(doc(too_short, too_long, normal, tiny), opts(), [])
    assert sorted(i.segment_id for i in issues) == ["l", "s"]
    assert all(i.severity == "warning" for i in issues)
    assert "too short" in next(i.message for i in issues if i.segment_id == "s")


def test_formatting_list_markers():
    lost = seg("lost", "1. 在 Rt△ABC 中，求 AB 的长。", "In Rt△ABC, find AB.")
    kept = seg("kept", "1. 在 Rt△ABC 中，求 AB 的长。", "1. In Rt△ABC, find AB.")
    changed = seg("chg", "(2) 求另一条直角边的长。", "(3) Find the other leg.")
    style = seg("sty", "(2) 求另一条直角边的长。", "2. Find the other leg.")  # same number, other style: fine
    circled = seg("cir", "① 判断下列说法", "① Decide whether the following")
    bullet = seg("bul", "• 周长公式", "- Perimeter formula")  # any bullet counts as a bullet
    cjk = seg("cjk", "一、填空题", "I. Fill in the blanks")  # CJK numeral marker: any marker accepted
    cjk_lost = seg("cjk2", "一、填空题", "Fill in the blanks")
    section = seg("sec", "1.1 探索勾股定理", "1.1 Exploring the Pythagorean theorem")
    issues = C.formatting(doc(lost, kept, changed, style, circled, bullet, cjk, cjk_lost, section), opts(), [])
    assert sorted(i.segment_id for i in issues) == ["chg", "cjk2", "lost"]
    by_id = {i.segment_id: i for i in issues}
    assert 'list marker "1."' in by_id["lost"].message
    assert 'found "(3)"' in by_id["chg"].message


def test_formatting_wrappers_and_raw_placeholders():
    source = "求斜边的长度。"
    quoted = seg("q", source, '"Find the length of the hypotenuse."')
    prefixed = seg("p", source, "Translation: Find the length of the hypotenuse.")
    json_like = seg("j", source, '{"id": "p0_b1", "text": "Find the length of the hypotenuse."}')
    raw_left = seg("r", source, "Find the ⟦7⟧ of the hypotenuse.", raw="Find the ⟦7⟧ of the hypotenuse.")
    fine = seg("f", source, "Find the length of the hypotenuse.")
    answer = seg("a", "答：斜边长 5 cm。", "Answer: the hypotenuse is 5 cm.")  # 答： is a legitimate "Answer:"
    solution = seg("s", "解：由勾股定理得。", "Solution: by the Pythagorean theorem.")
    issues = C.formatting(doc(quoted, prefixed, json_like, raw_left, fine, answer, solution), opts(), [])
    assert sorted(i.segment_id for i in issues) == ["j", "p", "q", "r"]
    assert "⟦7⟧" in next(i.message for i in issues if i.segment_id == "r")


def test_formatting_newlines_and_terminal_punctuation():
    breaks = seg("b", "第一行\n第二行\n第三行", "Line one Line two Line three")
    question = seg("q", "边长为 7、24、25 的三角形是直角三角形吗？", "A triangle with sides 7, 24 and 25 is right-angled.")
    not_question = seg("n", "这是直角三角形。", "Is this a right triangle?")
    cjk_period = seg("c", "这是直角三角形。", "This is a right triangle.")
    two_lines = seg("t", "第一行\n第二行", "Line one\nLine two")
    issues = C.formatting(doc(breaks, question, not_question, cjk_period, two_lines), opts(), [])
    assert sorted(i.segment_id for i in issues) == ["b", "n", "q"]
    assert "question mark" in next(i.message for i in issues if i.segment_id == "q")


def test_layout_fit_from_render_info():
    text = "This translation is far too long for the little box it has to go into"
    overflow = seg("o", "太长了", text, render=RenderInfo(font_size=6, scale=0.4, spare_height=-12, overflow=True))
    shrunk = seg("s", "太长了", text, render=RenderInfo(font_size=5.5, scale=0.5, overflow=False))
    fits = seg("f", "太长了", text, render=RenderInfo(font_size=11, scale=0.8, overflow=False))
    unrendered = seg("u", "太长了", text)
    issues = C.layout_fit(doc(overflow, shrunk, fits, unrendered), opts(min_font_scale=0.55), [])
    assert sorted(i.segment_id for i in issues) == ["o", "s"]
    o = next(i for i in issues if i.segment_id == "o")
    # a box re-flowed at scale 0.4 holds (0.4 / 0.55)^2 of the text at the minimum scale
    assert o.details["max_chars"] == int(len(text) * (0.4 / 0.55) ** 2 * 0.9) and o.severity == "error"
    assert f"at most {o.details['max_chars']} characters" in o.message and "original box" in o.message
    assert C.layout_fit(doc(shrunk), opts(min_font_scale=0.5), []) == []


def test_shorten_hint_boundaries():
    assert C.shorten_hint("", 0.5) == 1 and C.shorten_hint("x", 0.5) == 1 and C.shorten_hint("  ab ", 0.99) == 1
    assert C.shorten_hint("abcdefghij", 0.0) == 5  # unknown scale: halve
    assert C.shorten_hint("abcdefghij", 1.0, 0.55) == 9 and C.shorten_hint("abcdefghij", 5.0) == 9  # always shorter
    assert C.shorten_hint("a" * 100, 0.3) == 28  # single-line label: width grows linearly
    assert C.shorten_hint("a" * 100, 0.3, 0.55) == int(100 * (0.3 / 0.55) ** 2 * 0.9)
    assert 1 <= C.shorten_hint("ab", 0.01, 0.55) < 2


def test_image_text_check():
    ref = ImageRef(xref=50, page=0, bbox=BBox(x0=80, y0=225, x1=320, y1=405), width=480, height=360,
                   pixel_box=(250, 150, 330, 180))
    pending = seg("p0_i50_0", "斜边 c", "hypotenuse c", kind=SegmentKind.IMAGE_TEXT, image=ref)
    overflow = seg("p0_i50_1", "斜边 c", "hypotenuse c", kind=SegmentKind.IMAGE_TEXT, image=ref,
                   render=RenderInfo(font_size=6, scale=0.6, overflow=True))
    # a label that would have to shrink to 1-3 characters cannot be fixed by re-translation
    hopeless = seg("p0_i50_4", "150米", "150 metres", kind=SegmentKind.IMAGE_TEXT, image=ref,
                   render=RenderInfo(font_size=2.3, scale=0.13, overflow=True))
    done = seg("p0_i50_2", "斜边 c", "hypotenuse c", kind=SegmentKind.IMAGE_TEXT, image=ref,
               render=RenderInfo(font_size=9, scale=0.9, overflow=False))
    # images.render_image_segments marks "nothing drawn" with font_size == scale == 0
    failed = seg("p0_i50_3", "斜边 c", "hypotenuse c", kind=SegmentKind.IMAGE_TEXT, image=ref,
                 render=RenderInfo(font_size=0, scale=0, overflow=True, notes="not rendered: image decoding failed"))
    issues = C.image_text(doc(pending, overflow, done, failed, hopeless), opts(), [])
    by_id = {i.segment_id: i for i in issues}
    assert set(by_id) == {"p0_i50_0", "p0_i50_1", "p0_i50_3", "p0_i50_4"}
    assert by_id["p0_i50_4"].severity == "warning" and not by_id["p0_i50_4"].fixable
    assert "does not fit" in by_id["p0_i50_4"].message
    assert by_id["p0_i50_0"].severity == "warning" and not by_id["p0_i50_0"].fixable
    assert by_id["p0_i50_1"].severity == "error" and by_id["p0_i50_1"].details["max_chars"] < len("hypotenuse c")
    assert by_id["p0_i50_1"].fixable and "Shorten" in by_id["p0_i50_1"].message
    assert by_id["p0_i50_3"].severity == "error" and not by_id["p0_i50_3"].fixable
    assert "could not be painted" in by_id["p0_i50_3"].message and "decoding failed" in by_id["p0_i50_3"].message


def test_rule_checks_runs_everything_and_ignores_untranslatable_segments():
    pairs = default_glossary().pairs("zh", "en")
    skipped = seg("skip", "斜边", "斜边", translate=False)
    d = doc(seg("a", "直角三角形的斜边", "the long side"), seg("b", "斜边长为 13。", None), skipped)
    issues = rule_checks(d, opts(), pairs)
    assert "glossary" in names(issues) and "completeness" in names(issues)
    assert all(i.segment_id != "skip" for i in issues)
    assert all(i.page == 0 for i in issues)


# --------------------------------------------------------------------------- #
# loop
# --------------------------------------------------------------------------- #


def _faulty_doc() -> TranslatedDocument:
    source = "解：由勾股定理得 c² = 3² + 4² = 25，所以 c = 5 cm。"
    broken = seg("p0_b1", source, "Solution: by the Pythagorean theorem, so c = 5 cm.",
                 raw="Solution: by the Pythagorean theorem, so ⟦1⟧.")
    fine = seg("p0_b0", "第一章 勾股定理", "Chapter 1 The Pythagorean theorem")
    return doc(fine, broken)


def test_loop_converges_in_round_two_with_fixing_retranslate():
    d = _faulty_doc()
    calls: list[tuple[list[str], list[str]]] = []

    def retranslate(ids: list[str]) -> None:
        s = d.segment(ids[0])
        calls.append((list(ids), list(s.feedback)))
        s.translation_raw = "Solution: by the Pythagorean theorem ⟦0⟧, so ⟦1⟧."
        s.translated_text = "Solution: by the Pythagorean theorem c² = 3² + 4² = 25, so c = 5 cm."
        s.feedback = []
        s.attempts += 1

    progress: list[tuple[str, str, float]] = []
    report = run_qa_loop(d, opts(max_qa_rounds=3), glossary_pairs=[], retranslate=retranslate,
                         progress=lambda st, msg, pct: progress.append((st, msg, pct)))
    assert report.passed and len(report.rounds) == 2
    assert not report.rounds[0].passed and report.rounds[0].retranslated == ["p0_b1"]
    assert report.rounds[1].passed and report.rounds[1].retranslated == []
    assert calls and calls[0][0] == ["p0_b1"] and any("⟦0⟧" in fb for fb in calls[0][1])
    assert report.final_issues == [] and report.errors == 0
    assert "passed after 2 rounds" in report.summary and report.checks_run[:2] == ["completeness", "placeholders"]
    assert progress and all(st == "qa" for st, _, _ in progress) and progress[-1][2] <= 100


def test_loop_exhausts_max_rounds_and_keeps_previous_translation():
    d = _faulty_doc()
    before = d.segment("p0_b1").translated_text
    calls: list[list[str]] = []
    report = run_qa_loop(d, opts(max_qa_rounds=3), glossary_pairs=[], retranslate=lambda ids: calls.append(list(ids)))
    assert not report.passed and len(report.rounds) == 3 and calls == [["p0_b1"], ["p0_b1"]]
    assert report.final_issues and report.errors >= 1 and "FAILED after 3 rounds" in report.summary
    assert d.segment("p0_b1").translated_text == before  # never cleared
    assert d.segment("p0_b1").feedback  # feedback accumulated without duplicates
    assert len(d.segment("p0_b1").feedback) == len(set(d.segment("p0_b1").feedback))


def test_loop_maps_reviewer_findings_to_severities():
    d = doc(seg("p0_b0", "求斜边的长度。", "Find the length of the hypotenuse."),
            seg("p0_b1", "这是直角三角形。", "This is a right triangle."))

    class FakeReviewer:
        name = "fake"
        calls = 0

        def review(self, items, src, tgt, pairs):
            type(self).calls += 1
            assert {i.id for i in items} == {"p0_b0", "p0_b1"} and src is Lang.ZH and tgt is Lang.EN
            return [ReviewFinding(id="p0_b0", severity="error", category="meaning", message="wrong verb",
                                  suggested_fix="Find the length of the hypotenuse."),
                    ReviewFinding(id="p0_b1", severity="warning", category="grammar", message="awkward"),
                    ReviewFinding(id="ghost", severity="error", category="omission", message="no such segment")]

    retranslated: list[list[str]] = []
    report = run_qa_loop(d, opts(max_qa_rounds=1), glossary_pairs=[], retranslate=lambda ids: retranslated.append(ids),
                         reviewer=FakeReviewer())
    review = [i for i in report.final_issues if i.check == "llm_review"]
    by_id = {i.segment_id: i for i in review}
    assert by_id["p0_b0"].severity == "error" and by_id["p0_b0"].fixable and "Suggested" in by_id["p0_b0"].message
    assert by_id["p0_b1"].severity == "warning" and by_id[None].fixable is False
    assert not report.passed and retranslated == [] and "llm_review" in report.checks_run
    # llm_review disabled -> the reviewer is never called
    FakeReviewer.calls = 0
    report2 = run_qa_loop(d, opts(max_qa_rounds=1, llm_review=False), glossary_pairs=[], retranslate=lambda ids: None,
                          reviewer=FakeReviewer())
    assert FakeReviewer.calls == 0 and report2.passed and "llm_review" not in report2.checks_run


def test_loop_survives_reviewer_exceptions():
    d = doc(seg("p0_b0", "求斜边的长度。", "Find the length of the hypotenuse."))

    class Exploding:
        name = "boom"

        def review(self, items, src, tgt, pairs):
            raise RuntimeError("API down")

    report = run_qa_loop(d, opts(max_qa_rounds=2), glossary_pairs=[], retranslate=lambda ids: None, reviewer=Exploding())
    assert report.passed and len(report.rounds) == 1
    # the failure is not hidden: one unfixable warning per skipped batch
    assert [(i.check, i.severity, i.fixable) for i in report.final_issues] == [("llm_review", "warning", False)]
    assert "API down" in report.final_issues[0].message and report.final_issues[0].details["segment_ids"] == ["p0_b0"]
    assert report.warnings == 1 and "1 warning" in report.summary


def test_loop_tolerates_malformed_reviewer_output():
    d = doc(seg("p0_b0", "求斜边的长度。", "Find the length of the hypotenuse."),
            seg("p0_b1", "这是直角三角形。", "This is a right triangle."))

    class Weird:
        name = "weird"
        answers = iter([
            None,  # nothing at all
            [{"id": "p0_b0", "severity": "warning", "category": "", "message": "   "}],  # plain dicts, blanks
            [{"id": "p0_b1", "severity": "error"}],  # missing required fields -> validation error
        ])

        def review(self, items, src, tgt, pairs):
            return next(type(self).answers)

    reviewer = Weird()
    issues = [i for i in run_qa_loop(d, opts(max_qa_rounds=1), glossary_pairs=[], retranslate=lambda ids: None,
                                     reviewer=reviewer).final_issues]
    assert issues == []
    issues = run_qa_loop(d, opts(max_qa_rounds=1), glossary_pairs=[], retranslate=lambda ids: None,
                         reviewer=reviewer).final_issues
    assert len(issues) == 1 and issues[0].severity == "warning" and issues[0].segment_id == "p0_b0"
    assert issues[0].details["category"] == "other" and "without an explanation" in issues[0].message
    issues = run_qa_loop(d, opts(max_qa_rounds=1), glossary_pairs=[], retranslate=lambda ids: None,
                         reviewer=reviewer).final_issues
    assert len(issues) == 1 and issues[0].check == "llm_review" and not issues[0].fixable
    assert "ValidationError" in issues[0].details["error"]


def test_loop_render_check_feedback_and_unfixable_stop():
    d = doc(seg("p0_b0", "求斜边的长度。", "Find the length of the hypotenuse."))
    rounds_seen: list[int] = []

    def render_check(document: TranslatedDocument) -> list[QAIssue]:
        rounds_seen.append(1)
        return [QAIssue(check="layout_fit", severity="error", segment_id="p0_b0", page=0,
                        message="Shorten the translation to at most 20 characters so it fits the original box",
                        details={"max_chars": 20})]

    calls: list[list[str]] = []
    report = run_qa_loop(d, opts(max_qa_rounds=2), glossary_pairs=[], retranslate=lambda ids: calls.append(list(ids)),
                         render_check=render_check)
    assert calls == [["p0_b0"]] and len(rounds_seen) == 2 and not report.passed
    assert "at most 20 characters" in d.segment("p0_b0").feedback[0] and "render_check" in report.checks_run
    # an unfixable error without a segment stops the loop after the first round
    unfixable = lambda document: [QAIssue(check="output_pages", severity="error", message="page count", fixable=False)]  # noqa: E731
    calls.clear()
    report = run_qa_loop(d, opts(max_qa_rounds=3), glossary_pairs=[], retranslate=lambda ids: calls.append(list(ids)),
                         render_check=unfixable)
    assert calls == [] and len(report.rounds) == 1 and not report.passed and report.rounds[0].retranslated == []


def test_loop_retranslate_failure_is_recorded():
    d = _faulty_doc()

    def failing(ids: list[str]) -> None:
        raise TranslationError("rate limited")

    report = run_qa_loop(d, opts(max_qa_rounds=3), glossary_pairs=[], retranslate=failing)
    assert not report.passed and len(report.rounds) == 1
    assert any(i.check == "retranslate" and "rate limited" in i.message for i in report.final_issues)


def test_apply_feedback_and_review_issue_helpers():
    d = doc(seg("p0_b0", "求斜边的长度。", "Find the length."), seg("p0_b1", "斜边", "leg", translate=False))
    issues = [QAIssue(check="glossary", severity="error", segment_id="p0_b0", message="Glossary: translate \"斜边\" as \"hypotenuse\""),
              QAIssue(check="length_ratio", severity="warning", segment_id="p0_b0", message="too short"),
              QAIssue(check="glossary", severity="error", segment_id="p0_b0", message="Glossary: translate \"斜边\" as \"hypotenuse\""),
              QAIssue(check="x", severity="error", segment_id="p0_b1", message="not translatable"),
              QAIssue(check="y", severity="error", segment_id="p0_b0", message="unfixable", fixable=False)]
    assert apply_feedback(d, issues) == ["p0_b0"]
    # errors and warnings are fed back once each; unfixable messages are not instructions
    assert d.segment("p0_b0").feedback == ["Glossary: translate \"斜边\" as \"hypotenuse\"", "too short"]
    assert d.segment("p0_b1").feedback == []
    assert apply_feedback(d, issues) == ["p0_b0"] and len(d.segment("p0_b0").feedback) == 2  # idempotent
    assert apply_feedback(d, [issues[1], issues[4]]) == []  # warnings / unfixable alone never trigger
    issue = review_issue(ReviewFinding(id="p0_b0", severity="warning", category="Number", message="25 became 52"),
                         {s.id: s for s in d.segments})
    assert issue.severity == "error" and issue.page == 0 and issue.details["reviewer_severity"] == "warning"


# --------------------------------------------------------------------------- #
# output checks on real PDFs
# --------------------------------------------------------------------------- #


def _english_doc() -> TranslatedDocument:
    """A zh->en document whose translations are the strings of the English sample PDF."""
    en, zh = sample_texts("en"), sample_texts("zh")
    page_of = {k: (1 if k in ("exercises", "ex1", "ex2", "ex3", "think", "footer") else 0) for k in en}
    segments = [seg(f"p{page_of[k]}_b{i}", zh[k], en[k], page=page_of[k])
                for i, k in enumerate(k for k in en if not k.startswith("img"))]
    segments.append(seg("p0_b99", "a² + b² = c²", None, translate=False))
    return doc(*segments)


def test_output_checks_pass_on_matching_output(sample_pdf_zh, sample_pdf_en):
    issues = output_checks(sample_pdf_en, sample_pdf_zh, _english_doc())
    assert [i for i in issues if i.severity == "error"] == [], [i.message for i in issues]
    # the only tolerated finding is the non-embedded Helvetica inherited from the source
    assert {i.check for i in issues} <= {"output_fonts"} and all(i.details.get("inherited") for i in issues)
    assert all(not i.fixable for i in issues)


def test_output_checks_detect_removed_page(sample_pdf_zh, sample_pdf_en, tmp_path):
    d = pymupdf.open(str(sample_pdf_en))
    d.delete_page(1)
    one_page = tmp_path / "one_page.pdf"
    d.save(str(one_page))
    d.close()
    issues = output_checks(one_page, sample_pdf_zh, _english_doc())
    pages = [i for i in issues if i.check == "output_pages"]
    assert len(pages) == 1 and pages[0].severity == "error" and "1 page(s)" in pages[0].message
    assert pages[0].details == {"source_pages": 2, "output_pages": 1}


def test_output_checks_detect_moved_image(sample_pdf_zh, sample_pdf_en, tmp_path):
    d = pymupdf.open(str(sample_pdf_en))
    page = d[0]
    info = page.get_image_info(xrefs=True)[0]
    stream = d.extract_image(info["xref"])["image"]
    page.delete_image(info["xref"])
    page.insert_image(pymupdf.Rect(100, 240, 340, 420), stream=stream)
    moved = tmp_path / "moved.pdf"
    d.save(str(moved), garbage=3)
    d.close()
    issues = output_checks(moved, sample_pdf_zh, _english_doc())
    geometry = [i for i in issues if i.check == "output_geometry"]
    assert len(geometry) == 1 and geometry[0].page == 0 and geometry[0].severity == "error"
    assert geometry[0].details["added"] and "100.0, 240.0" in geometry[0].message
    assert not any(i.check == "output_pages" for i in issues)


def test_output_checks_detect_untranslated_output(sample_pdf_zh):
    # the untouched Chinese file presented as the "translated" output
    issues = output_checks(sample_pdf_zh, sample_pdf_zh, _english_doc())
    checks = {i.check for i in issues if i.severity == "error"}
    assert checks == {"output_text", "output_leftovers"}
    leftovers = [i for i in issues if i.check == "output_leftovers"]
    assert {i.page for i in leftovers} == {0, 1} and leftovers[0].details["examples"]
    text = next(i for i in issues if i.check == "output_text")
    assert text.details["found"] < text.details["expected"] and "was not placed as real text" in text.message


def test_output_checks_unreadable_file(tmp_path, sample_pdf_zh):
    bogus = tmp_path / "bogus.pdf"
    bogus.write_bytes(b"not a pdf")
    issues = output_checks(bogus, sample_pdf_zh, _english_doc())
    assert len(issues) == 1 and issues[0].check == "output_pages" and not issues[0].fixable


def test_distinctive_source_keys_and_script_ranges():
    assert C.distinctive_source_keys("zh", "en") == ("han",)
    assert C.distinctive_source_keys("en", "zh") == ("latin",)
    assert C.distinctive_source_keys("zh", "ja") == ()
    assert C.distinctive_source_keys("ja", "zh") == ("kana",)
    assert C.distinctive_source_keys("ko", "en") == ("hangul",)
    assert C.distinctive_source_keys("ja", "ko") == ("han", "kana")
    # the run regexes must agree with languages.script_profile (a look-alike code point in the
    # Han range once made it swallow all of Hangul)
    samples = {"han": "斜边豈", "kana": "ひらがなカタカナ", "hangul": "빗변", "latin": "hypoténuse"}
    for key, text in samples.items():
        for other, sample in samples.items():
            assert bool(C._runs_re((key,)).fullmatch(sample)) == (key == other), (key, other)
    assert C.foreign_letters("斜边의 길이", "ko") == 2 and C.foreign_letters("斜辺の長さ", "ja") == 0
    assert C.script_ratio("斜边의 길이", "ko") == 0.6 and C.script_ratio("123", "ko") == 1.0


# --------------------------------------------------------------------------- #
# report
# --------------------------------------------------------------------------- #


def test_report_markdown_summary_and_pages():
    d = _faulty_doc()
    report = run_qa_loop(d, opts(max_qa_rounds=2), glossary_pairs=[], retranslate=lambda ids: None)
    report.final_issues.append(QAIssue(check="output_pages", severity="warning", message="doc | level"))
    md = report_markdown(report, d)
    assert "# QA report" in md and "## Rounds" in md and "| 1 |" in md and "| 2 |" in md
    assert "- Round 1: numbers ×3, placeholders ×1" in md and "| 1 | 4 | 0 | 1 segment(s) | no |" in md
    assert "### `placeholders`" in md and "### `numbers`" in md and "### `output_pages`" in md
    assert "c² = 3² + 4² = 25" in md and "doc \\| level" in md and "QA FAILED after 2 rounds" in md
    assert "zh → en" in md
    grouped = issues_by_page(report)
    assert list(grouped) == [0, None] and grouped[0][0].check == "placeholders"
    assert summarize(QAReport()) == "QA not run"
    passed = QAReport(passed=True, rounds=[QARound(round=1, passed=True)], duration_s=1.26)
    assert summarize(passed) == "QA passed after 1 round: 0 errors, 0 warnings (1.3 s)"
    assert "No issues." in report_markdown(passed)


# --------------------------------------------------------------------------- #
# adversarial edge cases
# --------------------------------------------------------------------------- #


def test_empty_document_everywhere(sample_pdf_zh):
    empty = TranslatedDocument(source_path="x.pdf", source_lang=Lang.ZH, target_lang=Lang.EN)
    assert rule_checks(empty, opts(), []) == []
    for _name, _sev, fn in CHECKS:  # the ARCHITECTURE (doc, options) call form works for every check
        assert fn(empty, opts()) == []
    report = run_qa_loop(empty, opts(max_qa_rounds=0), glossary_pairs=[], retranslate=lambda ids: None)
    assert report.passed and len(report.rounds) == 1 and report.errors == report.warnings == 0
    assert "passed after 1 round" in report.summary
    assert "No issues." in report_markdown(report, empty) and issues_by_page(report) == {}
    # output checks on a document without segments: only geometry/page/font facts are checked
    issues = output_checks(sample_pdf_zh, sample_pdf_zh, empty)
    assert {i.check for i in issues} <= {"output_fonts"} and all(i.severity == "warning" for i in issues)
    # blank translations / whitespace-only sources never crash the checks
    blank = doc(seg("w", "   ", "   "), seg("e", "斜边", ""), seg("n", "", None))
    issues = rule_checks(blank, opts(), [])
    assert [(i.check, i.segment_id) for i in issues] == [("completeness", "e")]


def test_output_checks_detect_rotated_page_and_added_image(sample_pdf_zh, sample_pdf_en, tmp_path):
    d = pymupdf.open(str(sample_pdf_en))
    d[0].set_rotation(90)
    info = d[1].get_image_info(xrefs=True)[0]
    stream = d.extract_image(info["xref"])["image"]
    d[1].insert_image(pymupdf.Rect(60, 400, 120, 460), stream=stream)  # one extra placement on page 2
    changed = tmp_path / "changed.pdf"
    d.save(str(changed))
    d.close()
    issues = output_checks(changed, sample_pdf_zh, _english_doc())
    geometry = sorted(((i.page, i.message[:40]) for i in issues if i.check == "output_geometry"))
    assert [p for p, _ in geometry] == [0, 1]
    assert "rotation 90" in next(i.message for i in issues if i.check == "output_geometry" and i.page == 0)
    added = next(i for i in issues if i.check == "output_geometry" and i.page == 1)
    assert added.details["added"] == [[60.0, 400.0, 120.0, 460.0]] and added.details["missing"] == []
    assert all(not i.fixable for i in issues)


def test_loop_propagates_unexpected_retranslate_errors():
    import pytest

    d = _faulty_doc()

    def broken(ids: list[str]) -> None:
        raise ValueError("bug in the caller")

    with pytest.raises(ValueError, match="bug in the caller"):
        run_qa_loop(d, opts(max_qa_rounds=2), glossary_pairs=[], retranslate=broken)


def test_loop_is_thread_safe_across_documents():
    from concurrent.futures import ThreadPoolExecutor

    pairs = default_glossary().pairs("zh", "en")

    def run(n: int) -> tuple[bool, int, list[str]]:
        d = _faulty_doc()
        d.segments.append(seg(f"p0_b{n + 2}", "直角三角形的斜边", "the long side of a right triangle"))

        def retranslate(ids: list[str]) -> None:
            for sid in ids:
                s = d.segment(sid)
                if sid == "p0_b1":
                    s.translation_raw = "Solution: by the Pythagorean theorem ⟦0⟧, so ⟦1⟧."
                    s.translated_text = "Solution: by the Pythagorean theorem c² = 3² + 4² = 25, so c = 5 cm."
                else:
                    s.translated_text = s.translation_raw = "the hypotenuse of a right triangle"
                s.feedback = []

        report = run_qa_loop(d, opts(max_qa_rounds=3), glossary_pairs=pairs, retranslate=retranslate)
        return report.passed, len(report.rounds), report.rounds[0].retranslated

    expected = run(0)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run, range(16)))
    assert expected == (True, 2, ["p0_b1", "p0_b2"])
    assert all(r[:2] == expected[:2] and r[2][0] == "p0_b1" for r in results)


def test_unicode_edge_cases_in_checks():
    # full-width letters/digits, enclosed numbers and NFKC look-alikes must not confuse the rules
    fullwidth = seg("f", "ＡＢ＝５", "AB = 5", protect=False)
    circled_marker = seg("m", "⑴ 求斜边。", "(1) Find the hypotenuse.")
    emoji = seg("e", "求斜边的长度。😀", "Find the length of the hypotenuse. 😀")
    combining = seg("c", "求斜边的长度。", "Trouvez l'hypoténuse.")  # decomposed é (e + U+0301)
    issues = rule_checks(doc(fullwidth, circled_marker, emoji, combining), opts(), [])
    assert [i.check for i in issues if i.severity == "error"] == []
    # a translation made only of punctuation / symbols is incomplete (too short for the length
    # check, no letters for the script checks) and must still be rejected
    symbols = seg("s", "求斜边的长度。", "……")
    numeral = seg("n", "一", "1")  # a CJK numeral translated into a digit is fine
    issues = rule_checks(doc(symbols, numeral), opts(), [])
    assert [(i.check, i.segment_id) for i in issues if i.severity == "error"] == [("completeness", "s")]
    assert "contains no words" in issues[0].message


def test_report_markdown_keeps_pipeline_summary_and_escapes_cells():
    report = QAReport(passed=False, rounds=[QARound(round=1, passed=False, issues=[
        QAIssue(check="numbers", severity="error", message="pipe | and\nnewline", segment_id="p0_b0", page=0)])],
        final_issues=[QAIssue(check="numbers", severity="error", message="pipe | and\nnewline", segment_id="p0_b0",
                              page=0)], errors=1, summary="QA FAILED after 1 round: 1 error, 0 warnings; output file checks: 0 error(s)")
    d = doc(seg("p0_b0", "斜边 | 13", "hypotenuse | 31"))
    md = report_markdown(report, d)
    assert "**Result:** QA FAILED after 1 round: 1 error, 0 warnings; output file checks: 0 error(s)" in md
    assert "pipe \\| and newline" in md and "hypotenuse \\| 31" in md
    assert md.count("\n|") >= 4 and "\n\n\n" not in md
