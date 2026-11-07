"""Tests for mathtrans.extract (text extraction, protection, style, reading order)."""
from __future__ import annotations

import io
import json
from collections import Counter
from pathlib import Path

import pymupdf
import pytest
from PIL import Image

from mathtrans.extract import (
    TEXT_FLAGS,
    _find_table_cells,
    build_page_info,
    build_page_segments,
    detect_document_language,
    extract_document,
    is_caption,
    is_list_item,
    is_math_font,
    rotation_from_dir,
    sort_reading_order,
)
from mathtrans.models import BBox, Lang, PipelineOptions, SegmentKind, TextSegment, restore_placeholders
from mathtrans.samples import sample_texts


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _seg_with(doc, needle: str) -> TextSegment:
    matches = [s for s in doc.segments if needle in s.source_text]
    assert matches, f"no segment contains {needle!r}"
    return matches[0]


def _page_blocks(page: pymupdf.Page, lang: str = "en") -> list[TextSegment]:
    return build_page_segments(page, 0, Lang.parse(lang))


@pytest.fixture(scope="module")
def doc_zh(sample_pdf_zh):
    return extract_document(sample_pdf_zh, target_lang=Lang.EN)


@pytest.fixture(scope="module")
def doc_en(sample_pdf_en):
    return extract_document(sample_pdf_en, target_lang="zh")


# --------------------------------------------------------------------------- #
# Document structure
# --------------------------------------------------------------------------- #


def test_segment_count_ids_and_reading_order(doc_zh):
    # 9 text blocks on page 1, 6 on page 2 (see samples.make_sample_pdf)
    assert len(doc_zh.segments) == 15
    assert all(s.kind == SegmentKind.TEXT for s in doc_zh.segments)
    ids = [s.id for s in doc_zh.segments]
    assert len(set(ids)) == len(ids)
    assert ids[0] == "p0_b0" and ids[-1] == "p1_b5"
    for s in doc_zh.segments:
        assert s.id == f"p{s.page}_b{s.reading_order}"
    # segments of a page are contiguous and numbered 0..n-1 in order
    for page in (0, 1):
        on_page = [s for s in doc_zh.segments if s.page == page]
        assert [s.reading_order for s in on_page] == list(range(len(on_page)))
        first = doc_zh.segments.index(on_page[0])
        assert doc_zh.segments[first:first + len(on_page)] == on_page
    assert doc_zh.source_lang is Lang.ZH and doc_zh.target_lang is Lang.EN
    assert doc_zh.title == sample_texts("zh")["title"]


def test_bboxes_inside_page(doc_zh, doc_en):
    for doc in (doc_zh, doc_en):
        assert [p.index for p in doc.pages] == [0, 1]
        for s in doc.segments:
            info = doc.pages[s.page]
            assert (info.width, info.height, info.rotation) == (595.0, 842.0, 0)
            b = s.bbox
            assert 0 <= b.x0 < b.x1 <= info.width + 0.5
            assert 0 <= b.y0 < b.y1 <= info.height + 0.5
            for span in s.spans:
                assert b.expanded(1.0).contains(span.bbox)


def test_image_bboxes_populated(doc_zh, sample_pdf_zh):
    assert [len(p.image_bboxes) for p in doc_zh.pages] == [1, 1]
    assert doc_zh.pages[0].image_bboxes[0].as_tuple() == pytest.approx((80, 225, 320, 405))
    assert doc_zh.pages[1].image_bboxes[0].as_tuple() == pytest.approx((330, 200, 510, 380))
    with pymupdf.open(str(sample_pdf_zh)) as pdf:
        info = build_page_info(pdf[0], 0)
    assert info == doc_zh.pages[0]


def test_language_detection(sample_pdf_zh, sample_pdf_en):
    assert detect_document_language(sample_pdf_zh) is Lang.ZH
    assert detect_document_language(sample_pdf_en) is Lang.EN
    with pymupdf.open(str(sample_pdf_en)) as pdf:
        assert detect_document_language(pdf) is Lang.EN
        assert not pdf.is_closed  # a caller-owned document is left open
    auto = extract_document(sample_pdf_en, target_lang="ko")
    assert auto.source_lang is Lang.EN and auto.target_lang is Lang.KO
    forced = extract_document(sample_pdf_en, target_lang="ko", source_lang="pt")
    assert forced.source_lang is Lang.PT


def test_language_detection_falls_back_to_zh(tmp_path, caplog):
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 100), "12 + 34 = 46", fontname="helv")
    path = tmp_path / "numbers.pdf"
    pdf.save(str(path))
    pdf.close()
    with caplog.at_level("WARNING", logger="mathtrans.extract"):
        assert detect_document_language(path) is Lang.ZH
    assert "assuming source language zh" in caplog.text


def test_pages_filter(sample_pdf_zh):
    doc = extract_document(sample_pdf_zh, target_lang="en", pages=[1])
    assert len(doc.pages) == 2  # PageInfo for every page
    assert {s.page for s in doc.segments} == {1}
    assert len(doc.segments) == 6
    assert doc.segments[0].id == "p1_b0"
    with pytest.raises(ValueError):
        extract_document(sample_pdf_zh, target_lang="en", pages=[2])
    with pytest.raises(ValueError):
        extract_document(sample_pdf_zh, target_lang="en", pages=[-1])


def test_open_errors(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_document(tmp_path / "missing.pdf", target_lang="en")
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"this is not a pdf")
    with pytest.raises(ValueError):
        extract_document(bad, target_lang="en")


# --------------------------------------------------------------------------- #
# Roles, styles and protection on the samples
# --------------------------------------------------------------------------- #


def test_title_and_section_are_headings(doc_zh, doc_en):
    t = sample_texts("zh")
    title = _seg_with(doc_zh, "勾股定理")
    assert title.source_text == t["title"]
    assert title.style.role == "heading" and title.style.size == 22.0
    assert title.style.color == 0x1F3A93 and title.reading_order == 0
    section = _seg_with(doc_zh, t["section"])
    assert section.style.role == "heading"
    en_title = _seg_with(doc_en, "Chapter 1")
    assert en_title.style.role == "heading" and en_title.style.bold is True and en_title.style.italic is False
    assert en_title.style.serif is False
    assert "Bold" in en_title.style.font


def test_caption_role(doc_zh, doc_en):
    cap = _seg_with(doc_zh, "图 1-1")
    assert cap.style.role == "caption" and cap.style.size == 9.0 and cap.style.color == 0x555555
    assert cap.translate is True and "1-1" in cap.protected
    assert _seg_with(doc_en, "Figure 1-1").style.role == "caption"
    assert is_caption("表 2 常见勾股数") and is_caption("Tabla 3: valores") and not is_caption("表示方法")


def test_formula_line_is_not_translated(doc_zh, doc_en):
    for doc in (doc_zh, doc_en):
        formula = _seg_with(doc, "a² + b² = c²")
        assert formula.translate is False
        assert formula.skip_reason
        assert formula.protected == ["a² + b² = c²"]
        assert formula.protected_text == "⟦0⟧"
        assert formula.style.role != "heading"
        assert formula.style.color == 0x1F3B94 and formula.style.size == 16.0


def test_page_numbers_are_not_translated(doc_zh, doc_en):
    for doc in (doc_zh, doc_en):
        number = [s for s in doc.segments if s.page == 0 and s.source_text == "1"]
        assert len(number) == 1 and number[0].translate is False
        assert number[0].style.align == "center"  # centred page number
    assert _seg_with(doc_zh, "第 2 页").translate is True
    assert _seg_with(doc_en, "Page 2").translate is True


def test_para1_protection_round_trip(doc_zh, doc_en):
    t = sample_texts("zh")
    para = _seg_with(doc_zh, "这就是著名的勾股定理")
    assert "a²+b²=c²" in para.protected
    assert para.translate is True and para.style.role == "body"
    assert restore_placeholders(para.protected_text, para.protected) == para.source_text
    assert "⟦" in para.protected_text and "a²" not in para.protected_text
    # CJK lines joined with "" and the block's "a 和 b" spacing convention restored at the break
    assert para.source_text == t["para1"]
    assert para.style.line_height == pytest.approx(1.3, abs=0.05)
    en_para = _seg_with(doc_en, "famous Pythagorean theorem")
    assert "a²+b²=c²" in en_para.protected
    assert restore_placeholders(en_para.protected_text, en_para.protected) == en_para.source_text
    for doc in (doc_zh, doc_en):
        for s in doc.segments:
            assert restore_placeholders(s.protected_text, s.protected) == s.source_text


def test_list_role_and_cjk_joining(doc_zh):
    t = sample_texts("zh")
    ex3 = _seg_with(doc_zh, "判断")
    assert ex3.source_text == t["ex3"]  # "直角三\n角形吗" joined with ""
    assert ex3.style.role == "list"
    ex1 = _seg_with(doc_zh, "Rt△ABC")
    assert ex1.source_text == t["ex1"]  # "BC =" + "8" keeps its space
    assert ex1.style.role == "list"
    assert any(sp.is_math and sp.text == "△" for sp in ex1.spans)
    assert "BC = 8" in ex1.protected and "AB" in ex1.protected
    assert is_list_item("(1) first") and is_list_item("① 第一") and is_list_item("• bullet")
    assert not is_list_item("1.1 Exploring") and not is_list_item("12.5 cm")


def test_latin_space_joining(doc_en):
    t = sample_texts("en")
    para = _seg_with(doc_en, "famous Pythagorean theorem")
    assert para.source_text == t["para1"]  # three lines joined with single spaces
    think = _seg_with(doc_en, "Think:")
    assert think.source_text == t["think"]  # the "ﬁ" ligature is expanded to "fi"
    assert "ﬁ" not in think.source_text
    assert think.style.align == "left"


def test_two_column_reading_order_page2(doc_zh, doc_en):
    for doc, think_key in ((doc_zh, "思考"), (doc_en, "Think:")):
        page2 = [s for s in doc.segments if s.page == 1]
        heading = page2[0]
        assert heading.style.role == "heading"
        exercises = [s for s in page2 if is_list_item(s.source_text)]
        assert len(exercises) == 3
        think = _seg_with(doc, think_key)
        assert all(e.reading_order < think.reading_order for e in exercises)
        assert [e.source_text[0] for e in sorted(exercises, key=lambda s: s.reading_order)] == ["1", "2", "3"]
        footer = page2[-1]
        assert footer.source_text in ("第 2 页", "Page 2")


def test_sort_reading_order_single_column_rows():
    def seg(i, x0, y0, x1, y1):
        return TextSegment(id=str(i), page=0, bbox=BBox(x0=x0, y0=y0, x1=x1, y1=y1), source_text=str(i))

    # one wide paragraph, a figure caption on the left, a formula on the right (same row), a footer
    segs = [seg("footer", 290, 790, 310, 802), seg("formula", 340, 282, 418, 305),
            seg("caption", 137, 300, 263, 312), seg("para", 61, 134, 532, 164), seg("title", 61, 48, 221, 78)]
    order = [s.id for s in sort_reading_order(segs)]
    assert order == ["title", "para", "caption", "formula", "footer"]


def test_sort_reading_order_two_columns_with_spanning_heading():
    def seg(i, x0, y0, x1, y1):
        return TextSegment(id=str(i), page=0, bbox=BBox(x0=x0, y0=y0, x1=x1, y1=y1), source_text=str(i))

    segs = [
        seg("R1", 311, 95, 531, 140), seg("L2", 61, 150, 286, 200), seg("L1", 61, 95, 286, 140),
        seg("head", 61, 50, 535, 80), seg("R2", 311, 150, 531, 200), seg("L3", 61, 205, 286, 255),
        seg("mid", 61, 270, 535, 300), seg("L4", 61, 310, 286, 360), seg("R3", 311, 310, 531, 360),
        seg("foot", 283, 790, 311, 802),
    ]
    order = [s.id for s in sort_reading_order(segs)]
    assert order == ["head", "L1", "L2", "L3", "R1", "R2", "mid", "L4", "R3", "foot"]


# --------------------------------------------------------------------------- #
# Synthetic PDFs
# --------------------------------------------------------------------------- #


def test_math_font_span_detection():
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 100), "Let ", fontsize=12, fontname="helv")
    page.insert_text((72, 100), "x", fontsize=12, fontname="tiit")  # Times-Italic single letter
    page.insert_text((80, 100), " be a real number and ", fontsize=12, fontname="helv")
    page.insert_text((200, 100), "y", fontsize=12, fontname="heit")  # Helvetica-Oblique
    page.insert_text((208, 100), " its square.", fontsize=12, fontname="helv")
    page.insert_text((50, 140), "This whole sentence is italic.", fontsize=12, fontname="tiit")
    segs = _page_blocks(page, "en")
    first = segs[0]
    assert first.source_text == "Let x be a real number and y its square."
    math_spans = [sp for sp in first.spans if sp.is_math]
    assert sorted(sp.text.strip() for sp in math_spans) == ["x", "y"]
    assert all(sp.italic for sp in math_spans)
    assert "x" in first.protected and "y" in first.protected
    assert first.translate is True
    assert "Let ⟦" in first.protected_text
    sentence = segs[1]
    assert sentence.style.italic is True and sentence.style.serif is True
    assert not any(sp.is_math for sp in sentence.spans)
    assert is_math_font("CMMI10") and is_math_font("Cambria Math") and is_math_font("STIXGeneral")
    assert is_math_font("SymbolMT") and is_math_font("MTExtra") and not is_math_font("NimbusSans-Regular")
    assert not is_math_font("Times-Italic") and not is_math_font("")


def test_rotated_text_detection():
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=400)
    page.insert_text((50, 60), "Normal text here", fontsize=12, fontname="helv")
    page.insert_text((60, 300), "Rotated upward label", fontsize=12, fontname="helv", rotate=90)
    page.insert_text((200, 150), "Rotated downward", fontsize=12, fontname="helv", rotate=270)
    page.insert_text((350, 380), "Upside down", fontsize=12, fontname="helv", rotate=180)
    by_text = {s.source_text: s for s in _page_blocks(page, "en")}
    assert by_text["Normal text here"].style.rotation == 0
    up = by_text["Rotated upward label"]
    assert up.style.rotation == 90 and up.translate is True and up.style.is_vertical is False
    assert up.bbox.height > up.bbox.width  # the box of upward text is tall
    assert by_text["Rotated downward"].style.rotation == 270
    assert by_text["Upside down"].style.rotation == 180
    assert rotation_from_dir((1, 0)) == 0 and rotation_from_dir((0, -1)) == 90
    assert rotation_from_dir((-1, 0)) == 180 and rotation_from_dir((0, 1)) == 270


def test_vertical_cjk_text_is_marked_vertical():
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=400)
    page.insert_text((50, 350), "直角三角形的斜边", fontsize=14, fontname="china-s", rotate=90)
    segs = _page_blocks(page, "zh")
    assert len(segs) == 1
    assert segs[0].style.rotation == 90 and segs[0].style.is_vertical is True
    assert segs[0].translate is True


def test_latin_dehyphenation_and_paragraph_breaks():
    pdf = pymupdf.open()
    page = pdf.new_page()
    css = "p {margin: 0; font-family: sans-serif; font-size: 11px; line-height: 1.3;}"
    # a narrow box forces explicit hyphenated line breaks; <br> keeps them where we want them
    page.insert_htmlbox(
        pymupdf.Rect(50, 50, 260, 120),
        "<p>The length of the hypo-<br>tenuse of a Cauchy-<br>Schwarz style triangle is long.</p>",
        css=css,
    )
    segs = _page_blocks(page, "en")
    assert len(segs) == 1
    assert segs[0].source_text == "The length of the hypotenuse of a Cauchy-Schwarz style triangle is long."
    # a sentence end followed by a list item starts a new paragraph inside the block
    pdf2 = pymupdf.open()
    page2 = pdf2.new_page()
    page2.insert_htmlbox(pymupdf.Rect(50, 50, 400, 120),
                         "<p>Solve the following.<br>1. Find x.<br>2. Find y.</p>", css=css)
    seg = _page_blocks(page2, "en")[0]
    assert seg.source_text == "Solve the following.\n1. Find x.\n2. Find y."


def test_skip_reasons_and_single_letter_label():
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 60), "A", fontsize=12, fontname="helv")  # vertex label
    page.insert_text((50, 100), "42", fontsize=12, fontname="helv")
    page.insert_text((50, 140), "피타고라스", fontsize=12, fontname="korea")  # Korean inside a Chinese doc
    page.insert_text((50, 180), "斜边 c", fontsize=12, fontname="china-s")
    by_text = {s.source_text: s for s in _page_blocks(page, "zh")}
    assert by_text["A"].translate is False  # a lone Latin letter is a formula atom in a CJK source
    assert by_text["42"].translate is False and "numbers" in by_text["42"].skip_reason
    assert by_text["피타고라스"].translate is False and "source script" in by_text["피타고라스"].skip_reason
    assert by_text["斜边 c"].translate is True and by_text["斜边 c"].protected == ["c"]
    assert by_text["斜边 c"].style.role == "label"
    # in a Latin source a lone letter is not a protected atom, so the label rule has to catch it
    en_doc = _page_blocks(page, "en")
    letter = next(s for s in en_doc if s.source_text == "A")
    assert letter.translate is False and "label" in letter.skip_reason


def test_alignment_detection():
    pdf = pymupdf.open()
    page = pdf.new_page()
    css = "p {margin: 0; font-family: sans-serif; font-size: 11px; line-height: 1.3;}"
    page.insert_htmlbox(pymupdf.Rect(50, 50, 300, 110),
                        '<p style="text-align:center">short line<br>a noticeably longer second line<br>mid</p>', css=css)
    page.insert_htmlbox(pymupdf.Rect(50, 150, 300, 210),
                        '<p style="text-align:right">short line<br>a noticeably longer second line<br>mid</p>', css=css)
    page.insert_htmlbox(pymupdf.Rect(50, 250, 300, 330),
                        '<p style="text-align:justify">' + "word " * 60 + "</p>", css=css)
    page.insert_htmlbox(pymupdf.Rect(50, 350, 300, 410),
                        "<p>short line<br>a noticeably longer second line<br>mid</p>", css=css)
    # MuPDF may split the tiny "mid" line into its own block; identify blocks by their text
    segs = sorted((s for s in _page_blocks(page, "en") if s.source_text.startswith(("short", "word"))),
                  key=lambda s: s.bbox.y0)
    assert [s.style.align for s in segs] == ["center", "right", "justify", "left"]
    assert all(s.style.line_height == pytest.approx(1.3, abs=0.05) for s in segs)


def test_superscript_spans_become_unicode():
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 100), "x", fontsize=12, fontname="helv")
    page.insert_text((57, 95), "2", fontsize=7, fontname="helv")
    page.insert_text((62, 100), " + y", fontsize=12, fontname="helv")
    page.insert_text((80, 95), "2", fontsize=7, fontname="helv")
    page.insert_text((85, 100), " = 1", fontsize=12, fontname="helv")
    seg = _page_blocks(page, "en")[0]
    assert seg.source_text == "x² + y² = 1"
    assert seg.translate is False


def test_image_bboxes_deduplicated_and_clipped():
    pdf = pymupdf.open()
    page = pdf.new_page(width=300, height=300)
    buf = io.BytesIO()
    Image.new("RGB", (40, 40), "red").save(buf, format="PNG")
    stream = buf.getvalue()
    page.insert_image(pymupdf.Rect(20, 20, 120, 120), stream=stream)
    xref = page.get_images()[0][0]
    page.insert_image(pymupdf.Rect(20, 20, 120, 120), xref=xref)  # same placement twice
    page.insert_image(pymupdf.Rect(250, 250, 400, 400), xref=xref)  # partly off the page
    info = build_page_info(page, 0)
    assert (info.width, info.height, info.rotation) == (300.0, 300.0, 0)
    assert [b.as_tuple() for b in info.image_bboxes] == [(20.0, 20.0, 120.0, 120.0), (250.0, 250.0, 300.0, 300.0)]


def test_rotated_page_dimensions_match_text_space(tmp_path):
    pdf = pymupdf.open()
    page = pdf.new_page(width=300, height=500)
    page.insert_text((20, 50), "Hello rotated page", fontsize=12, fontname="helv")
    page.set_rotation(90)
    path = tmp_path / "rotated.pdf"
    pdf.save(str(path))
    pdf.close()
    doc = extract_document(path, target_lang="zh", source_lang="en")
    info = doc.pages[0]
    assert (info.width, info.height, info.rotation) == (300.0, 500.0, 90)
    seg = doc.segments[0]
    assert seg.source_text == "Hello rotated page" and seg.style.rotation == 0
    assert seg.bbox.x1 <= info.width and seg.bbox.y1 <= info.height


def test_dominant_style_by_character_count():
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_htmlbox(
        pymupdf.Rect(50, 50, 500, 90),
        '<p style="font-family:sans-serif;font-size:11px;margin:0"><b>Note:</b> '
        'this long explanation is set in the regular weight, <span style="color:#ff0000">red</span> aside.</p>',
    )
    seg = _page_blocks(page, "en")[0]
    assert seg.style.bold is False and seg.style.color == 0 and seg.style.size == 11.0
    assert seg.style.role == "body"
    assert Counter(sp.bold for sp in seg.spans)[True] >= 1
    assert any(sp.color == 0xFF0000 for sp in seg.spans)


def test_korean_line_joining(tmp_path):
    from mathtrans.samples import make_sample_pdf

    # MuPDF wraps Korean between syllables: tight breaks are joined without a space,
    # a Hangul -> digit break keeps its space and a particle attaches to a Latin token.
    doc = extract_document(make_sample_pdf(tmp_path / "ko.pdf", "ko"), target_lang="en")
    assert doc.source_lang is Lang.KO
    think = _seg_with(doc, "생각해 보기")
    assert "작은 정사각형이 생긴다" in think.source_text and "피타고라스 정리" in think.source_text
    assert "삼각형 4개로" in think.source_text
    assert _seg_with(doc, "두 변의 길이를").source_text == sample_texts("ko")["para1"]
    page2 = [s for s in doc.segments if s.page == 1]
    assert [s.source_text[:1] for s in page2[1:4]] == ["1", "2", "3"] and page2[4].source_text.startswith("생각해")
    # word-wrapped Korean (a loose break: the next word would have fitted) stands for a space
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_htmlbox(pymupdf.Rect(50, 50, 500, 110),
                        "<p>두 변의 합은<br>빗변의 제곱과 같다는 것이 피타고라스 정리이다.</p>",
                        css="p {margin: 0; font-family: sans-serif; font-size: 11px;}")
    seg = _page_blocks(page, "ko")[0]
    assert seg.source_text == "두 변의 합은 빗변의 제곱과 같다는 것이 피타고라스 정리이다."


# --------------------------------------------------------------------------- #
# Adversarial edge cases (verifier)
# --------------------------------------------------------------------------- #


def _single_page_pdf(path: Path, text: str = "some text") -> Path:
    pdf = pymupdf.open()
    pdf.new_page().insert_text((50, 50), text, fontname="helv")
    pdf.save(str(path))
    pdf.close()
    return path


def test_non_pdf_files_are_rejected_and_extension_is_ignored(tmp_path):
    # PyMuPDF happily opens text files and images as documents; extract must not
    txt = tmp_path / "notes.txt"
    txt.write_text("Hello world, this is not a PDF\n", encoding="utf-8")
    with pytest.raises(ValueError, match="PDF"):
        extract_document(txt, target_lang="zh")
    png = tmp_path / "img.png"
    Image.new("RGB", (40, 40), "red").save(png)
    with pytest.raises(ValueError, match="not a PDF"):
        detect_document_language(png)
    # a real PDF behind an unknown extension is accepted (content decides)
    hidden = _single_page_pdf(tmp_path / "upload.bin", "Hidden extension")
    doc = extract_document(hidden, target_lang="zh", source_lang="en")
    assert [s.source_text for s in doc.segments] == ["Hidden extension"]
    # a caller-owned non-PDF document is rejected as well
    with pymupdf.open(str(png)) as img_doc:
        with pytest.raises(ValueError, match="not a PDF"):
            extract_document(img_doc, target_lang="zh")


def test_in_memory_document_and_page_filter_validation():
    pdf = pymupdf.open()  # in-memory: Document.name is None
    pdf.new_page().insert_text((50, 50), "page one", fontname="helv")
    pdf.new_page().insert_text((50, 50), "page two", fontname="helv")
    doc = extract_document(pdf, target_lang="zh", source_lang="en", pages=[1, 1, 0])
    assert doc.source_path == "" and [s.id for s in doc.segments] == ["p0_b0", "p1_b0"]
    assert extract_document(pdf, target_lang="zh", source_lang="en", pages=[]).segments == []
    for bad in ([True], [1.0], ["0"]):
        with pytest.raises(ValueError, match="integers"):
            extract_document(pdf, target_lang="zh", source_lang="en", pages=bad)
    assert not pdf.is_closed
    empty = pymupdf.open()
    with pytest.raises(ValueError, match="no pages"):
        extract_document(empty, target_lang="en")
    with pytest.raises(ValueError, match="no pages"):
        detect_document_language(empty)
    pdf.close()
    with pytest.raises(ValueError, match="closed"):
        extract_document(pdf, target_lang="en")


def test_encrypted_pdfs(tmp_path):
    pdf = pymupdf.open()
    pdf.new_page().insert_text((50, 50), "secret text", fontname="helv")
    locked = tmp_path / "locked.pdf"
    pdf.save(str(locked), encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="user", owner_pw="owner")
    owner_only = tmp_path / "owner.pdf"
    pdf.save(str(owner_only), encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="", owner_pw="owner")
    pdf.close()
    with pytest.raises(ValueError, match="password"):
        extract_document(locked, target_lang="zh")
    doc = extract_document(owner_only, target_lang="zh", source_lang="en")  # opens without a password
    assert [s.source_text for s in doc.segments] == ["secret text"]


def test_whitespace_only_blocks_and_corrupt_content_stream(tmp_path):
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 50), "   ", fontname="helv")
    page.insert_text((50, 100), "   ", fontname="helv")
    page.insert_text((50, 150), "��", fontname="helv")  # unmapped glyphs
    page.insert_text((50, 200), "real", fontname="helv")
    segs = _page_blocks(page, "en")
    empties = [s for s in segs if s.source_text == ""]
    assert len(empties) == 2
    assert all(s.translate is False and s.skip_reason == "empty" and s.style.role == "other" for s in empties)
    assert all(restore_placeholders(s.protected_text, s.protected) == s.source_text for s in segs)
    assert [s.source_text for s in segs if s.translate] == ["real"]
    # a syntax error in the content stream must not abort extraction of the readable text
    for i, xref in enumerate(page.get_contents()):  # insert_text appended one stream per call
        pdf.update_stream(xref, b"BT /helv 12 Tf 50 700 Td (partial) Tj ET q BAD ))) Q BT garbage" if i == 0 else b"")
    path = tmp_path / "corrupt.pdf"
    pdf.save(str(path))
    pdf.close()
    doc = extract_document(path, target_lang="zh", source_lang="en")
    assert [s.source_text for s in doc.segments] == ["partial"]


def test_three_column_reading_order():
    pdf = pymupdf.open()
    page = pdf.new_page()
    css = "p {margin: 0; font-family: sans-serif; font-size: 11px;}"
    page.insert_htmlbox(pymupdf.Rect(40, 40, 550, 70), '<p style="font-size:18px">Three column heading</p>', css=css)
    for col, x in enumerate((40, 220, 400)):
        for row in range(3):
            page.insert_htmlbox(
                pymupdf.Rect(x, 100 + row * 120, x + 150, 190 + row * 120),
                f"<p>Column {col + 1} paragraph {row + 1} with enough words to wrap over a few lines.</p>", css=css)
    page.insert_htmlbox(pymupdf.Rect(40, 790, 120, 810), "<p>12</p>", css=css)  # page number, left margin
    segs = _page_blocks(page, "en")
    assert [s.source_text[:22] for s in segs] == [
        "Three column heading",
        "Column 1 paragraph 1 w", "Column 1 paragraph 2 w", "Column 1 paragraph 3 w",
        "Column 2 paragraph 1 w", "Column 2 paragraph 2 w", "Column 2 paragraph 3 w",
        "Column 3 paragraph 1 w", "Column 3 paragraph 2 w", "Column 3 paragraph 3 w",
        "12",
    ]
    assert segs[0].style.role == "heading" and segs[-1].translate is False


def test_furniture_on_two_column_page_is_read_first_and_last():
    def seg(i, x0, y0, x1, y1):
        return TextSegment(id=str(i), page=0, bbox=BBox(x0=x0, y0=y0, x1=x1, y1=y1), source_text=str(i))

    # running head at the top right, page number in the left margin at the bottom
    segs = [seg("foot", 61, 790, 90, 802), seg("R1", 311, 95, 531, 140), seg("L2", 61, 150, 286, 200),
            seg("L1", 61, 95, 286, 140), seg("head", 61, 50, 535, 80), seg("R2", 311, 150, 531, 200),
            seg("runhead", 400, 20, 535, 32)]
    assert [s.id for s in sort_reading_order(segs, page_height=842)] == \
        ["runhead", "head", "L1", "L2", "R1", "R2", "foot"]
    # a short sub-heading at the top of the left column still belongs to that column
    segs = [seg("sub", 61, 60, 140, 72), seg("L1", 61, 80, 286, 140), seg("L2", 61, 150, 286, 200),
            seg("R1", 311, 50, 531, 140), seg("R2", 311, 150, 531, 200)]
    assert [s.id for s in sort_reading_order(segs, page_height=842)] == ["sub", "L1", "L2", "R1", "R2"]
    assert sort_reading_order([]) == [] and [s.id for s in sort_reading_order(segs[:1])] == ["sub"]


def test_text_running_off_the_page_is_clipped():
    pdf = pymupdf.open()
    page = pdf.new_page(width=200, height=200)
    page.insert_text((150, 100), "This text runs off the right edge", fontname="helv")
    page.insert_text((50, 300), "fully outside the page", fontname="helv")
    segs = _page_blocks(page, "en")
    assert len(segs) == 1 and segs[0].source_text.startswith("This text")
    assert segs[0].bbox.x1 <= 200.0 and segs[0].bbox.x0 == pytest.approx(150.0)
    info = build_page_info(page, 0)
    assert (info.width, info.height, info.image_bboxes) == (200.0, 200.0, [])


def test_small_unraised_span_is_not_a_superscript():
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 100), "Note", fontsize=12, fontname="helv")
    page.insert_text((80, 100), "2", fontsize=7, fontname="helv")  # same baseline: a footnote-sized digit
    seg = _page_blocks(page, "en")[0]
    assert seg.source_text == "Note 2" and seg.protected == ["2"]


def test_fullwidth_markers_and_foreign_script_captions():
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 50), "（１）全角の番号", fontsize=12, fontname="japan")
    page.insert_text((50, 80), "①第一項目", fontsize=12, fontname="japan")
    page.insert_text((50, 110), "図 ２ 三角形", fontsize=12, fontname="japan")
    page.insert_text((50, 140), "그림 1-2 직각삼각형", fontsize=12, fontname="korea")
    by_text = {s.source_text: s for s in _page_blocks(page, "ja")}
    assert by_text["（１）全角の番号"].style.role == "list" and by_text["（１）全角の番号"].protected == ["１"]
    assert by_text["①第一項目"].style.role == "list" and by_text["①第一項目"].translate is True
    assert by_text["図 ２ 三角形"].style.role == "caption"
    korean = by_text["그림 1-2 직각삼각형"]
    assert korean.translate is False and "source script (ja)" in korean.skip_reason
    assert korean.style.role == "caption"


def test_vertical_japanese_running_downward():
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=400)
    page.insert_text((300, 50), "縦書きの文章です", fontsize=14, fontname="japan", rotate=270)
    page.insert_text((50, 50), "横書き", fontsize=14, fontname="japan")
    by_text = {s.source_text: s for s in _page_blocks(page, "ja")}
    down = by_text["縦書きの文章です"]
    assert down.style.rotation == 270 and down.style.is_vertical is True and down.translate is True
    assert down.bbox.height > down.bbox.width
    assert by_text["横書き"].style.rotation == 0 and by_text["横書き"].style.is_vertical is False


def test_all_sample_languages_round_trip(tmp_path):
    from mathtrans.samples import make_sample_pdf

    for lang in ("ja", "ko", "es", "pt"):
        doc = extract_document(make_sample_pdf(tmp_path / f"{lang}.pdf", lang), target_lang="zh" if lang != "zh" else "en")
        assert doc.source_lang is Lang.parse(lang), lang
        assert len(doc.segments) == 15 and doc.title == sample_texts(lang)["title"]
        for s in doc.segments:
            assert restore_placeholders(s.protected_text, s.protected) == s.source_text
            assert s.id == f"p{s.page}_b{s.reading_order}"
        assert [s.style.role for s in doc.segments[:2]] == ["heading", "heading"]
        assert sum(1 for s in doc.segments if not s.translate) == 2  # formula + page number "1"


def test_concurrent_extraction_is_deterministic(sample_pdf_zh, sample_pdf_en):
    import threading

    results: dict[str, list[dict]] = {}

    def work(name, path):
        results[name] = [extract_document(path, target_lang="ko").model_dump() for _ in range(3)]

    threads = [threading.Thread(target=work, args=("zh", sample_pdf_zh)), threading.Thread(target=work, args=("en", sample_pdf_en))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert set(results) == {"zh", "en"}
    for runs in results.values():
        assert runs[0] == runs[1] == runs[2] and len(runs[0]["segments"]) == 15


# --------------------------------------------------------------------------- #
# Tables and side-by-side lines (regression: cells of a row were one segment)
# --------------------------------------------------------------------------- #

_TABLE_CSS = "table{border-collapse:collapse} td{border:1px solid #000;padding:3px} p{margin:0}"
_ZH_ROWS = [["数的类型", "例子", "是否有限小数", "备注"], ["整数", "3, -5, 0", "是", "可以写成分数"]]
_EN_ROWS = [["Type of number", "Examples", "Finite decimal?", "Remark"],
            ["Integer", "3, -5, 0", "yes", "can be written as a fraction"]]


def _html_table_page(rows: list[list[str]]) -> tuple[pymupdf.Document, pymupdf.Page]:
    """A page with a bordered HTML table (the borders become vector drawings)."""
    pdf = pymupdf.open()
    page = pdf.new_page()
    html = "<table>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows) + "</table>"
    page.insert_htmlbox(pymupdf.Rect(50, 50, 500, 200), html, css=_TABLE_CSS)
    return pdf, page


def _raw_lines(page: pymupdf.Page) -> list[str]:
    return ["".join(s["text"] for s in ln["spans"])
            for b in page.get_text("dict", flags=TEXT_FLAGS)["blocks"] if b["type"] == 0 for ln in b["lines"]]


def test_ruled_table_cells_become_separate_segments():
    for rows, lang in ((_ZH_ROWS, "zh"), (_EN_ROWS, "en")):
        pdf, page = _html_table_page(rows)
        # MuPDF itself runs neighbouring cells together ("数的类型例子", "Type of number Examples ...")
        texts = [c for row in rows for c in row]
        assert any(ln not in texts for ln in _raw_lines(page)), lang
        cells = [c for table in _find_table_cells(page, 0) for c in table]
        assert len(cells) == 8, lang
        segs = _page_blocks(page, lang)
        assert [s.source_text for s in segs] == texts, lang  # one segment per cell, read row by row
        assert all(s.style.role == "table" for s in segs)
        assert not any("数的类型例子" in s.source_text or "number Examples" in s.source_text for s in segs)
        used: list[int] = []
        for s in segs:
            inside = [i for i, c in enumerate(cells) if BBox.from_rect(c).contains(s.bbox, tol=0.5)]
            assert len(inside) == 1, (s.source_text, s.bbox)  # the box is the cell's interior
            used.append(inside[0])
            assert all(s.bbox.expanded(1.0).contains(sp.bbox) for sp in s.spans)
            assert restore_placeholders(s.protected_text, s.protected) == s.source_text
        assert sorted(used) == list(range(8))
        assert next(s for s in segs if s.source_text == "3, -5, 0").translate is False
        pdf.close()


def test_ruled_table_cell_alignment_room_and_wrapping():
    pdf = pymupdf.open()
    page = pdf.new_page()
    x0, y0, cw, rh = 60, 90, 120, 30
    rows = [[("直角边 a", "center"), ("斜边 c", "right"), ("备注", "left")],
            [("3", "center"), ("5", "right"), ("可以写成分数，也可以写成有限小数", "left")]]
    for r in range(len(rows) + 1):
        page.draw_line(pymupdf.Point(x0, y0 + r * rh), pymupdf.Point(x0 + 3 * cw, y0 + r * rh), color=(0, 0, 0), width=0.8)
    for c in range(4):
        page.draw_line(pymupdf.Point(x0 + c * cw, y0), pymupdf.Point(x0 + c * cw, y0 + len(rows) * rh), color=(0, 0, 0), width=0.8)
    for r, row in enumerate(rows):
        for c, (text, align) in enumerate(row):
            page.insert_htmlbox(pymupdf.Rect(x0 + c * cw + 4, y0 + r * rh + 4, x0 + (c + 1) * cw - 4, y0 + (r + 1) * rh - 2),
                                f'<p style="font-size:10px;text-align:{align};margin:0">{text}</p>')
    segs = _page_blocks(page, "zh")
    by_text = {s.source_text: s for s in segs}
    assert [s.source_text for s in segs] == ["直角边 a", "斜边 c", "备注", "3", "5", "可以写成分数，也可以写成有限小数"]
    assert [by_text[t].style.align for t in ("直角边 a", "斜边 c", "备注")] == ["center", "right", "left"]
    assert all(s.style.role == "table" for s in segs)
    # the box is the cell's interior: centred text gets the whole cell (minus padding), left /
    # right-aligned text keeps its own anchor edge and gets the room on the other side
    centred = by_text["直角边 a"].bbox
    assert (centred.x0, centred.x1) == pytest.approx((x0 + 3, x0 + cw - 3), abs=0.5)
    right = by_text["斜边 c"]
    assert right.bbox.x1 == pytest.approx(max(sp.bbox.x1 for sp in right.spans), abs=0.5)
    assert right.bbox.x0 == pytest.approx(x0 + cw + 3, abs=0.5)
    left = by_text["备注"]
    assert left.bbox.x0 == pytest.approx(min(sp.bbox.x0 for sp in left.spans), abs=0.5)
    assert left.bbox.x1 == pytest.approx(x0 + 3 * cw - 3, abs=0.5)
    for s in segs:
        col = next(k for k in range(3) if x0 + k * cw < (s.bbox.x0 + s.bbox.x1) / 2 < x0 + (k + 1) * cw)
        assert x0 + col * cw <= s.bbox.x0 and s.bbox.x1 <= x0 + (col + 1) * cw  # never across a rule
        assert y0 <= s.bbox.y0 and s.bbox.y1 <= y0 + 2 * rh
    wrapped = by_text["可以写成分数，也可以写成有限小数"]  # two lines of one cell stay one segment
    assert len({round(sp.bbox.y0) for sp in wrapped.spans}) == 2
    pdf.close()


def test_frames_and_figure_grids_are_not_tables():
    pdf = pymupdf.open()
    page = pdf.new_page()
    # a frame around two paragraphs is not a table: the paragraphs stay separate body blocks
    page.draw_rect(pymupdf.Rect(60, 100, 535, 200), color=(0, 0, 1), width=1)
    page.insert_htmlbox(pymupdf.Rect(66, 106, 529, 150), "<p>Theorem: a boxed paragraph inside a frame.</p>")
    page.insert_htmlbox(pymupdf.Rect(66, 150, 529, 194), "<p>Second paragraph in the same frame.</p>")
    # a square cut into four by two lines, with a label running across the vertical line: a figure
    page.draw_rect(pymupdf.Rect(100, 300, 300, 500), color=(0, 0, 0), width=1)
    page.draw_line(pymupdf.Point(200, 300), pymupdf.Point(200, 500), color=(0, 0, 0), width=1)
    page.draw_line(pymupdf.Point(100, 400), pymupdf.Point(300, 400), color=(0, 0, 0), width=1)
    page.insert_text((185, 350), "面积 S", fontsize=12, fontname="china-s")
    segs = _page_blocks(page, "zh")
    assert [s.source_text for s in segs] == ["Theorem: a boxed paragraph inside a frame.",
                                             "Second paragraph in the same frame.", "面积 S"]
    assert [s.style.role for s in segs] == ["body", "body", "label"]
    assert segs[2].bbox.x0 < 200 < segs[2].bbox.x1  # the label was not cut at the line
    pdf.close()


def test_side_by_side_lines_become_separate_segments():
    pdf = pymupdf.open()
    page = pdf.new_page()
    # running head + right-aligned page number on one baseline (MuPDF: one block, two lines)
    page.insert_text((60, 30), "第一章 勾股定理", fontsize=8, fontname="china-s")
    page.insert_text((515, 30), "第 3 页", fontsize=8, fontname="china-s")
    # a borderless 2 x 2 table
    page.insert_text((70, 120), "直角边 a", fontsize=10, fontname="china-s")
    page.insert_text((310, 120), "斜边 c", fontsize=10, fontname="china-s")
    page.insert_text((70, 144), "3", fontsize=10, fontname="helv")
    page.insert_text((310, 144), "5", fontsize=10, fontname="helv")
    # ordinary paragraphs must not be split: a 3-line paragraph, a justified block, and a block
    # whose first line has a wide gap ("例 1" + text) but whose second line spans the width
    for i, line in enumerate(["在直角三角形中，两条直角边的平方和等于斜边", "的平方。如果两条直角边长分别为 a 和 b，斜边",
                              "长为 c，那么它们满足勾股定理。"]):
        page.insert_text((60, 300 + 14 * i), line, fontsize=10, fontname="china-s")
    page.insert_htmlbox(pymupdf.Rect(50, 400, 300, 480), '<p style="text-align:justify">' + "word " * 60 + "</p>",
                        css="p {margin: 0; font-family: sans-serif; font-size: 11px; line-height: 1.3;}")
    page.insert_text((60, 500), "例 1", fontsize=10, fontname="china-s")
    page.insert_text((200, 500), "已知直角三角形的两条直角边", fontsize=10, fontname="china-s")
    page.insert_text((60, 514), "分别为 3 和 4，求斜边的长度。求出它的面积。", fontsize=10, fontname="china-s")
    assert len([ln for ln in _raw_lines(page) if ln in ("第一章 勾股定理", "第 3 页")]) == 2
    segs = _page_blocks(page, "zh")
    texts = [s.source_text for s in segs]
    assert texts[:6] == ["第一章 勾股定理", "第 3 页", "直角边 a", "斜边 c", "3", "5"]  # row by row
    assert len(segs) == 9
    by_text = {s.source_text: s for s in segs}
    assert by_text["第 3 页"].bbox.x0 >= 500 and by_text["第一章 勾股定理"].bbox.x1 < 200
    assert by_text["直角边 a"].bbox.x1 < 300 <= by_text["斜边 c"].bbox.x0
    assert by_text["3"].bbox.x1 < 300 <= by_text["5"].bbox.x0 and by_text["3"].translate is False
    assert all(s.style.rotation == 0 for s in segs)
    assert texts[6] == "在直角三角形中，两条直角边的平方和等于斜边的平方。如果两条直角边长分别为 a 和 b，斜边长为 c，那么它们满足勾股定理。"
    assert texts[7].startswith("word word") and segs[7].style.align == "justify"
    assert texts[8].startswith("例 1") and "分别为 3 和 4" in texts[8]
    pdf.close()


def test_table_translation_stays_inside_cells(tmp_path):
    from mathtrans.pipeline import run_pipeline

    pdf, page = _html_table_page(_ZH_ROWS)
    page.insert_text((60, 30), "第一章 勾股定理", fontsize=8, fontname="china-s")
    page.insert_text((515, 30), "第 3 页", fontsize=8, fontname="china-s")
    src = tmp_path / "table.pdf"
    pdf.save(str(src))
    cells = [BBox.from_rect(c) for table in _find_table_cells(page, 0) for c in table]
    pdf.close()
    assert len(cells) == 8
    res = run_pipeline(src, tmp_path / "out", PipelineOptions(target_lang=Lang.EN, translator="mock",
                                                              translate_images=False))
    assert res.status == "completed", res.qa_report and res.qa_report.model_dump()
    with pymupdf.open(res.output_pdf) as out:
        out_page = out[0]
        for cell in cells:
            text = out_page.get_text("text", clip=cell.to_rect()).strip()
            assert text, cell  # a translation in every cell ...
            assert not any("一" <= ch <= "鿿" for ch in text), text  # ... and no source glyphs left behind
        words = out_page.get_text("words")
        table_area = cells[0]
        for c in cells[1:]:
            table_area = table_area.union(c)
        for x0, y0, x1, y1, word, *_ in words:
            box = BBox(x0=x0, y0=y0, x1=x1, y1=y1)
            if table_area.intersection_area(box) <= 0:
                continue
            assert any(c.contains(box, tol=1.0) for c in cells), (word, box)  # never across a rule
        page_number = [w for w in words if w[4] == "Page"]
        assert page_number and page_number[0][0] >= 500  # the page number stayed at the right margin
    segments = json.loads(Path(res.segments_json).read_text(encoding="utf-8"))["segments"]
    head = next(s for s in segments if s["source_text"] == "第一章 勾股定理")
    assert head["render"]["scale"] >= 0.95 and head["render"]["bbox"]["x1"] > head["bbox"]["x1"]  # grew into free space
    for s in segments:
        if s["style"]["role"] == "table" and s.get("render"):
            assert s["render"]["overflow"] is False
            assert BBox(**s["bbox"]).contains(BBox(**s["render"]["bbox"]), tol=0.5)  # rendered inside the cell box
