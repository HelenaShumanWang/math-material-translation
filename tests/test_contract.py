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
    assert len(merged.entries) == len(g.entries)


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
