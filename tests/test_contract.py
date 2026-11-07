"""Tests for the shared contract modules (models, protect, languages, glossary, fonts, samples)."""
import pymupdf

from mathtrans.glossary import default_glossary, missing_glossary_terms, parse_glossary_text
from mathtrans.languages import detect_language, foreign_letters, script_ratio
from mathtrans.models import BBox, Lang, TextSegment, restore_placeholders
from mathtrans.protect import is_fully_protected, protect_text, verify_placeholders


def test_lang_parse_aliases():
    assert Lang.parse("zh-CN") is Lang.ZH
    assert Lang.parse("English") is Lang.EN
    assert Lang.parse("日本語") is Lang.JA


def test_bbox_geometry():
    a = BBox(x0=0, y0=0, x1=10, y1=10)
    b = BBox(x0=5, y0=5, x1=15, y1=15)
    assert a.intersection_area(b) == 25
    assert a.union(b).as_tuple() == (0, 0, 15, 15)
    assert a.contains(BBox(x0=1, y0=1, x1=9, y1=9))


def test_protect_roundtrip_zh():
    text = "解：由勾股定理得 c² = 3² + 4² = 25，所以 c = 5 cm。"
    p, frags = protect_text(text, "zh")
    assert "⟦0⟧" in p and "c² = 3² + 4² = 25" in frags
    assert restore_placeholders(p, frags) == text
    assert not is_fully_protected(p)
    assert is_fully_protected(protect_text("a²+b²=c²", "zh")[0])


def test_protect_latin_articles_not_swallowed():
    p, frags = protect_text("El área del triángulo es 12 cm² y su perímetro es 16 cm.", "es")
    assert frags == ["12 cm²", "16 cm"]
    p, frags = protect_text("Let x = 3 and y = 4.", "en")
    assert frags == ["x = 3", "y = 4"]


def test_verify_placeholders():
    assert verify_placeholders("⟦0⟧ ⟦1⟧", "⟦1⟧ foo ⟦0⟧") == []
    assert verify_placeholders("⟦0⟧ ⟦1⟧", "⟦0⟧ only")


def test_detect_language():
    assert detect_language("勾股定理：直角三角形") is Lang.ZH
    assert detect_language("三平方の定理は") is Lang.JA
    assert detect_language("피타고라스 정리") is Lang.KO
    assert detect_language("The area of the triangle is") is Lang.EN
    assert detect_language("El área del triángulo es") is Lang.ES
    assert detect_language("A área do triângulo não é") is Lang.PT
    assert detect_language("123") is None


def test_script_helpers():
    assert foreign_letters("hypotenuse 斜边", "en") == 2
    assert script_ratio("直角三角形 ABC", "zh") > 0.5


def test_default_glossary_and_checks():
    g = default_glossary()
    pairs = g.pairs("zh", "en")
    assert ("勾股定理", "Pythagorean theorem") in pairs
    assert missing_glossary_terms("直角三角形的斜边", "the hypotenuse of a right triangle", pairs, "zh", "en") == []
    missing = missing_glossary_terms("直角三角形的斜边", "the long side", pairs, "zh", "en")
    assert ("斜边", "hypotenuse") in missing
    custom = parse_glossary_text("zh,en\n斜边,hypotenuse side\n")
    merged = g.merged_with(custom)
    assert merged.pairs("zh", "en")[0] != ("斜边", "hypotenuse side")  # longest first
    assert ("斜边", "hypotenuse side") in merged.pairs("zh", "en")
    assert ("斜边", "hypotenuse") not in merged.pairs("zh", "en")  # the custom entry replaces the built-in one
    # precedence is per source term and language pair: the built-in entry stays for the
    # languages the custom entry does not define
    assert len(merged.entries) == len(g.entries) + 1
    assert ("斜边", "hipotenusa") in merged.pairs("zh", "pt")


def test_sample_pdf(sample_pdf_zh):
    doc = pymupdf.open(str(sample_pdf_zh))
    assert doc.page_count == 2
    assert "勾股定理" in doc[0].get_text()
    assert len(doc[0].get_image_info()) == 1


def test_segment_effective_text():
    s = TextSegment(id="p0_b0", page=0, bbox=BBox(x0=0, y0=0, x1=1, y1=1), source_text="x")
    assert s.effective_text == "x"
    s.translated_text = "y"
    assert s.effective_text == "y"


def test_protect_uppercase_words_in_latin_sources():
    p, frags = protect_text("STEP 1: Draw triangle ABC with AB = 3 cm. NOTE: UNIT 2 follows.", "en")
    assert frags == ["1", "ABC", "AB = 3 cm", "2"]
    assert "STEP" in p and "NOTE" in p and "UNIT" in p
    p, frags = protect_text("En el triángulo PQR, ∠PQR = 90°.", "es")
    assert "PQR" in frags and "∠PQR = 90°" in frags
    # CJK sources keep upper-case tokens as labels (they are never ordinary words there)
    p, frags = protect_text("在△ABC中，AB=5。", "zh")
    assert "△ABC" in frags and "AB=5" in frags


def test_pipeline_progress_is_monotonic(sample_pdf_zh, tmp_path):
    from mathtrans.models import Lang, PipelineOptions
    from mathtrans.pipeline import run_pipeline

    seen = []
    run_pipeline(sample_pdf_zh, tmp_path, PipelineOptions(target_lang=Lang.EN, translator="mock"),
                 progress=lambda stage, msg, pct: seen.append(pct))
    assert seen and all(b >= a for a, b in zip(seen, seen[1:])) and seen[-1] == 100


def test_pipeline_rejects_textless_pdf_without_ocr(tmp_path):
    import pymupdf
    from mathtrans.models import Lang, PipelineOptions
    from mathtrans.pipeline import run_pipeline

    doc = pymupdf.open()
    doc.new_page()
    src = tmp_path / "blank.pdf"
    doc.save(str(src))
    res = run_pipeline(src, tmp_path / "out", PipelineOptions(target_lang=Lang.EN, translator="mock",
                                                              translate_images=False))
    assert res.status == "error" and "no text layer" in (res.error or "")


def test_protect_caps_headings_are_words():
    """Dictionary words set in capitals (worksheet headings) are translated, not protected."""
    for text, expected in [
        ("STEP 1 Draw a right triangle.", ["1"]),
        ("UNIT 3 Fractions", ["3"]),
        ("PART 2", ["2"]),
        ("NOTE", []),
        ("TIPS Use a ruler.", []),
        ("TEST YOURSELF", []),
        ("AREA AND PERIMETER", []),
        ("SHOW YOUR WORK", []),
        ("NAME: ______ DATE: ______", []),
        ("HINT", []),
        ("FOR EXAMPLE", []),
        ("DID YOU KNOW?", []),
        ("ANSWER KEY", []),
        ("the PDF file", []),
        ("NASA and the USA", []),
    ]:
        protected, frags = protect_text(text, "en")
        assert frags == expected, (text, frags)
        assert not is_fully_protected(protected), text
    for text, lang, expected in [
        ("TEMA 2", "es", ["2"]),
        ("NOTA: lee con cuidado.", "es", []),
        ("MUY IMPORTANTE", "es", []),
        ("CAPÍTULO 1", "pt", ["1"]),
        ("SOLUÇÃO", "pt", []),
        ("EXERCÍCIOS", "pt", []),
        ("ÁREA DA FIGURA", "pt", []),
    ]:
        protected, frags = protect_text(text, lang)
        assert frags == expected, (text, frags)
        assert not is_fully_protected(protected), text


def test_protect_geometry_labels_stay_protected():
    """Bare point names ("AB", "ABCD", "OA") and Roman numerals survive verbatim even when
    nothing glues them to a formula."""
    for text, lang, expected in [
        ("ABCD is a square.", "en", ["ABCD"]),
        ("AB is parallel to CD", "en", ["AB", "CD"]),
        ("Segment AB is parallel to CD.", "en", ["AB", "CD"]),
        ("the radius OA and side DA", "en", ["OA", "DA"]),
        ("In △ABC, AB = 3.", "en", ["△ABC", "AB = 3"]),
        ("Find the area of triangle ABC.", "en", ["ABC"]),
        ("triangles ABC and DEF are congruent", "en", ["ABC", "DEF"]),
        ("quadrilateral PQRS", "en", ["PQRS"]),
        ("Point A' is the image of A.", "en", ["A'"]),
        ("UNIT III", "en", ["III"]),
        ("Chapter XIV", "en", ["XIV"]),
        ("El triángulo ABC es rectángulo.", "es", ["ABC"]),
        ("线段AB平行于CD", "zh", ["AB", "CD"]),
    ]:
        assert protect_text(text, lang)[1] == expected, text


def test_protect_es_pt_sin_is_a_preposition():
    """In Spanish / Portuguese "sin" means *without*; it is the sine only when its
    argument is attached or followed by more math (the sine is usually "sen" there)."""
    assert protect_text("Un polígono sin 3 lados iguales.", "es")[1] == ["3"]
    assert protect_text("Un número sin 5 divisores.", "es")[1] == ["5"]
    assert protect_text("sin30° = 1/2", "es")[1] == ["sin30° = 1/2"]
    assert protect_text("sin(x) = 1/2", "es")[1] == ["sin(x) = 1/2"]
    assert protect_text("sin 30° = 1/2", "es")[1] == ["sin 30° = 1/2"]
    frags = protect_text("Calcula sen 30° e tg 45°.", "pt")[1]
    assert frags and frags[0].startswith("sen 30°") and frags[-1].endswith("tg 45°")
    # English keeps the function
    assert protect_text("sin 3 lados", "en")[1] == ["sin 3"]


def test_pipeline_translates_caps_headings_and_keeps_labels(tmp_path):
    """Worksheet headings set in capitals are translated (no segment is skipped as
    'no translatable text') while bare geometry labels come through verbatim."""
    from mathtrans.models import Lang, PipelineOptions, TranslatedDocument
    from mathtrans.pipeline import run_pipeline

    doc = pymupdf.open()
    page = doc.new_page()
    y = 80
    for line in ["STEP 1 Draw a right triangle.", "NOTE", "SHOW YOUR WORK",
                 "AB is parallel to CD.", "ABCD is a square."]:
        page.insert_text((72, y), line, fontsize=14, fontname="helv")
        y += 40
    src = tmp_path / "worksheet.pdf"
    doc.save(str(src))
    doc.close()

    res = run_pipeline(src, tmp_path / "out", PipelineOptions(
        target_lang=Lang.ZH, source_lang=Lang.EN, translator="mock", translate_images=False))
    assert res.status == "completed", res.error
    translated = TranslatedDocument.model_validate_json(
        (tmp_path / "out" / "segments.json").read_text(encoding="utf-8"))
    skipped = [(s.source_text, s.skip_reason) for s in translated.text_segments() if not s.translate]
    assert skipped == []
    out_text = pymupdf.open(res.output_pdf)[0].get_text()
    for heading in ("STEP", "NOTE", "SHOW", "YOUR", "WORK"):
        assert heading not in out_text, out_text
    for label in ("AB", "CD", "ABCD"):
        assert label in out_text, out_text
