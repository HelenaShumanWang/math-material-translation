"""Scanned pages in overlay mode: OCR lines -> paragraphs -> erased image + editable text."""
import hashlib

import pymupdf
import pytest

from mathtrans.extract import extract_document
from mathtrans.images import extract_image_segments
from mathtrans.models import Lang, PipelineOptions, SegmentKind
from mathtrans.ocr import RapidOcrEngine
from mathtrans.pipeline import run_pipeline
from mathtrans.samples import make_sample_pdf
from mathtrans.scanned import MERGED, erase_merged_lines, group_ocr_lines, is_scanned_page, scanned_pages


@pytest.fixture(scope="module")
def scanned_pdf(tmp_path_factory):
    base = tmp_path_factory.mktemp("scan")
    src = make_sample_pdf(base / "src.pdf", "zh")
    d = pymupdf.open(str(src))
    out = pymupdf.open()
    for p in d:
        pix = p.get_pixmap(dpi=150)
        page = out.new_page(width=p.rect.width, height=p.rect.height)
        page.insert_image(page.rect, stream=pix.tobytes("jpg"))
    path = base / "scanned.pdf"
    out.save(str(path))
    return path


@pytest.fixture(scope="module")
def ocr_lines(scanned_pdf):
    doc = extract_document(scanned_pdf, target_lang=Lang.EN, source_lang=Lang.ZH)
    assert not doc.text_segments()
    lines = extract_image_segments(scanned_pdf, doc, RapidOcrEngine(), pages=[0])
    doc.segments.extend(lines)
    return doc, lines


def test_is_scanned_page(scanned_pdf, sample_pdf_zh):
    assert scanned_pages(scanned_pdf) == {0, 1}
    assert scanned_pages(sample_pdf_zh) == set()
    assert is_scanned_page(pymupdf.open(str(scanned_pdf))[0])


def test_lines_are_grouped_into_paragraphs(ocr_lines):
    doc, lines = ocr_lines
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH)
    assert paragraphs and all(p.kind == SegmentKind.TEXT and p.origin == "ocr" for p in paragraphs)
    body = [p for p in paragraphs if "直角三角形" in p.source_text and "勾股定理" in p.source_text]
    assert body, [p.source_text[:30] for p in paragraphs]
    para = max(body, key=lambda p: len(p.members))
    assert len(para.members) >= 2 and "⟦" in para.protected_text  # formula protected inside the paragraph
    by_id = {l.id: l for l in lines}
    for mid in para.members:
        assert by_id[mid].skip_reason.startswith(MERGED) and not by_id[mid].translate
        assert para.bbox.contains(by_id[mid].bbox, tol=1.0)
    assert 5 <= para.style.size <= 40 and 1.0 <= para.style.line_height <= 1.8
    title = [p for p in paragraphs if "勾股定理" in p.source_text and len(p.members) == 1]
    assert any(p.style.role == "heading" for p in title)
    assert all(l.translate or l.skip_reason for l in lines)


def test_erase_merged_lines_changes_the_image(ocr_lines, scanned_pdf):
    doc, lines = ocr_lines
    group_ocr_lines(lines, 0, Lang.ZH)
    pdf = pymupdf.open(str(scanned_pdf))
    xref = pdf[0].get_image_info(xrefs=True)[0]["xref"]
    before = hashlib.md5(pdf.extract_image(xref)["image"]).hexdigest()
    assert erase_merged_lines(pdf, doc) == 1
    after = hashlib.md5(pdf.extract_image(pdf[0].get_image_info(xrefs=True)[0]["xref"])["image"]).hexdigest()
    assert before != after
    assert all(l.render is not None for l in lines if l.skip_reason.startswith(MERGED))


def test_overlay_pipeline_produces_editable_text(scanned_pdf, tmp_path):
    res = run_pipeline(scanned_pdf, tmp_path, PipelineOptions(
        target_lang=Lang.EN, translator="mock", scanned_mode="overlay", require_qa_pass=False))
    assert res.status == "completed", res.error
    out = pymupdf.open(res.output_pdf)
    assert out.page_count == 2
    text = out[0].get_text()
    assert "Pythagorean theorem" in text and "勾股定理" not in text  # real, extractable text on a scanned page
    src = pymupdf.open(str(scanned_pdf))
    assert [i["bbox"] for i in out[0].get_image_info()] == [i["bbox"] for i in src[0].get_image_info()]
    import json
    segs = json.load(open(res.segments_json, encoding="utf-8"))["segments"]
    paragraphs = [s for s in segs if s["origin"] == "ocr"]
    assert paragraphs and all(s["translated_text"] for s in paragraphs if s["translate"])
    assert not any(s["kind"] == "image_text" and s["translate"] and s.get("translated_text") for s in segs
                   if s["page"] == 0 and s["skip_reason"].startswith(MERGED))


def test_formula_lines_stay_in_the_picture():
    from mathtrans.models import BBox, ImageRef, SegmentStyle, TextSegment

    def line(i, y, text, translate, reason=""):
        ref = ImageRef(xref=9, page=0, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                       pixel_box=(100, int(y * 2), 600, int(y * 2) + 24))
        return TextSegment(id=f"l{i}", page=0, kind=SegmentKind.IMAGE_TEXT, bbox=BBox(x0=50, y0=y, x1=300, y1=y + 12),
                           source_text=text, protected_text=text, image=ref, style=SegmentStyle(size=10),
                           translate=translate, skip_reason=reason)

    lines = [
        line(0, 100, "解：先算一共有多少只", True),
        line(1, 114, "4×4=16", False, "pure number / formula"),
        line(2, 128, "16-1=15", False, "pure number / formula"),
        line(3, 142, "所以还剩 15 只。", True),
    ]
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH)
    assert [p.members for p in paragraphs] == [["l0"], ["l3"]]
    assert lines[1].skip_reason == "pure number / formula" and lines[2].skip_reason == "pure number / formula"
    assert all(p.translate for p in paragraphs)


def test_watermark_fragments_are_suppressed_and_trimmed():
    from mathtrans.models import BBox, ImageRef, PageInfo, SegmentStyle, TextSegment, TranslatedDocument
    from mathtrans.scanned import WATERMARK, suppress_watermark_fragments, watermark_alphabet

    def line(i, text, translate=True, reason="", confidence=0.97):
        ref = ImageRef(xref=9, page=0, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                       pixel_box=(10, 10 + 30 * i, 300, 34 + 30 * i), confidence=confidence)
        return TextSegment(id=f"l{i}", page=0, kind=SegmentKind.IMAGE_TEXT,
                           bbox=BBox(x0=5, y0=5 + 15 * i, x1=150, y1=17 + 15 * i),
                           source_text=text, protected_text=text, image=ref, style=SegmentStyle(size=10),
                           translate=translate, skip_reason=reason)

    doc = TranslatedDocument(source_path="x.pdf", source_lang=Lang.ZH, target_lang=Lang.EN,
                             pages=[PageInfo(index=0, width=500, height=700)])
    doc.segments = [
        line(0, "北京师范大学出版社", False, "slanted text (17°): watermark"),
        line(1, "师范大学出版", False, "slanted text (15°): watermark"),
        line(2, "北京师范大学出版社", False, "slanted text (18°): watermark"),
        line(3, "五社", confidence=0.71),     # low-confidence misread of "出版社"
        line(7, "学校", confidence=0.99),     # genuine label sharing one letter: kept
        line(4, "观察物体！版社"),              # genuine title with a glued fragment
        line(5, "数学是由无数个数学故事组成的。"),  # genuine text sharing letters (数, 学) with the watermark
        line(6, "大学"),                      # short, only watermark letters -> suppressed (acceptable loss)
    ]
    assert {"北", "京", "师", "范", "大", "学", "出", "版", "社"} <= watermark_alphabet(doc)
    changed = suppress_watermark_fragments(doc)
    by = {s.id: s for s in doc.segments}
    assert by["l3"].translate is False and by["l3"].skip_reason == WATERMARK
    assert by["l4"].translate and by["l4"].source_text == "观察物体！"
    assert by["l5"].translate and by["l5"].source_text.startswith("数学是由")
    assert by["l6"].translate is False
    assert by["l7"].translate and by["l7"].source_text == "学校"
    assert changed == 3


def test_lines_with_different_colours_are_not_merged():
    from mathtrans.models import BBox, ImageRef, SegmentStyle, TextSegment

    def line(i, y, text, color):
        ref = ImageRef(xref=9, page=0, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                       pixel_box=(100, int(y * 2), 600, int(y * 2) + 24))
        return TextSegment(id=f"c{i}", page=0, kind=SegmentKind.IMAGE_TEXT, bbox=BBox(x0=50, y0=y, x1=300, y1=y + 12),
                           source_text=text, protected_text=text, image=ref, style=SegmentStyle(size=10, color=color))

    white_heading = line(0, 100, "植树", 0xFFFFFF)
    black_body = line(1, 113, "平均每班分到多少棵树苗？", 0x202020)
    black_body2 = line(2, 126, "分一分，算一算。", 0x242424)
    paragraphs = group_ocr_lines([white_heading, black_body, black_body2], 0, Lang.ZH)
    assert [p.members for p in paragraphs] == [["c0"], ["c1", "c2"]]
    assert paragraphs[0].style.color == 0xFFFFFF and paragraphs[1].style.color == 0x202020
