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
    # the replaced page image leaves no never-drawn duplicate behind (it would double the file size)
    for page in out:
        assert len(page.get_images()) == len(page.get_image_info()) == 1
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
    black_body2 = line(2, 126, "每班分到的树苗一样多。", 0x242424)
    paragraphs = group_ocr_lines([white_heading, black_body, black_body2], 0, Lang.ZH)
    assert [p.members for p in paragraphs] == [["c0"], ["c1", "c2"]]
    assert paragraphs[0].style.color == 0xFFFFFF and paragraphs[1].style.color == 0x202020


def _gline(i, x0, y, x1, text, h=12.0, color=0x202020):
    from mathtrans.models import BBox, ImageRef, SegmentStyle, TextSegment

    ref = ImageRef(xref=9, page=0, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                   pixel_box=(int(x0 * 2), int(y * 2), int(x1 * 2), int((y + h) * 2)))
    return TextSegment(id=f"g{i}", page=0, kind=SegmentKind.IMAGE_TEXT, bbox=BBox(x0=x0, y0=y, x1=x1, y1=y + h),
                       source_text=text, protected_text=text, image=ref, style=SegmentStyle(size=10, color=color))


def test_answer_lines_and_instruction_verbs_start_new_paragraphs():
    lines = [
        _gline(0, 50, 100, 330, "还剩下多少个苹果？"),
        _gline(1, 50, 113, 250, "答：还剩下____个。"),          # answer line: its own paragraph
        _gline(2, 50, 126, 300, "做一做，说一说，再填一填。"),    # reduplicated verb: new paragraph
        _gline(3, 50, 139, 320, "用你喜欢的方法算一算。"),       # continues the instruction above
        _gline(4, 50, 152, 300, "● 比一比，谁的多？"),           # bullet: new paragraph
    ]
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH)
    assert [p.members for p in paragraphs] == [["g0"], ["g1"], ["g2", "g3"], ["g4"]]


def test_speech_bubble_beside_instruction_is_not_merged():
    lines = [
        _gline(0, 50, 100, 400, "小明和小红一共有多少本书？请你算一算吧"),
        _gline(1, 200, 113, 330, "我有17本书。"),                 # bubble: x0 jumps, not centred
        _gline(2, 50, 113, 380, "然后和同伴说一说你是怎样想的"),     # left-aligned continuation
    ]
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH)
    assert sorted(p.members for p in paragraphs) == [["g0", "g2"], ["g1"]]


def test_line_after_a_finished_sentence_needs_alignment_and_no_gap():
    lines = [
        _gline(0, 50, 100, 300, "淘气有15个苹果，"),
        _gline(1, 50, 113, 300, "笑笑有8个苹果。"),
        _gline(2, 50, 132, 300, "他们一共有多少个苹果"),  # gap of 7 pt (> 0.5 h) after a full stop
    ]
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH)
    assert [p.members for p in paragraphs] == [["g0", "g1"], ["g2"]]
    # a centred multi-line bubble still joins (the left edges differ, the centres agree)
    centred = [_gline(5, 100, 200, 260, "鸡比鹅多得多，"), _gline(6, 112, 213, 248, "鹅比鸭少一些")]
    assert [p.members for p in group_ocr_lines(centred, 0, Lang.ZH)] == [["g5", "g6"]]


def test_grouping_keeps_questions_labels_and_answer_lines_apart():
    from mathtrans.models import BBox, ImageRef, SegmentStyle, TextSegment

    def line(i, x0, y, w, text, h=12):
        ref = ImageRef(xref=9, page=0, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                       pixel_box=(int(x0 * 2), int(y * 2), int((x0 + w) * 2), int((y + h) * 2)))
        return TextSegment(id=f"g{i}", page=0, kind=SegmentKind.IMAGE_TEXT, bbox=BBox(x0=x0, y0=y, x1=x0 + w, y1=y + h),
                           source_text=text, protected_text=text, image=ref, style=SegmentStyle(size=10, color=0x202020))

    lines = [
        line(0, 50, 100, 300, "1.笑笑一共需要多少元？"),
        line(1, 60, 114, 40, "18元"),                      # narrow diagram label right under the question
        line(2, 50, 128, 300, "答："),                      # answer line followed by a blank
        line(3, 50, 142, 300, "2.淘气买了3本书，每本8元。"),   # next exercise: list marker
        line(4, 50, 156, 300, "一共花了多少元？"),           # continuation of exercise 2
    ]
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH)
    members = [p.members for p in paragraphs]
    assert ["g0"] in members and ["g2"] in members and ["g3", "g4"] in members
    assert all("g1" not in m for m in members) or ["g1"] in members


def test_watermark_alphabet_ignores_letters_common_in_upright_text():
    from mathtrans.models import BBox, ImageRef, PageInfo, SegmentStyle, TextSegment, TranslatedDocument
    from mathtrans.scanned import watermark_alphabet

    def line(i, text, translate=True, reason=""):
        ref = ImageRef(xref=9, page=0, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                       pixel_box=(10, 10 + 20 * i, 300, 30 + 20 * i))
        return TextSegment(id=f"w{i}", page=0, kind=SegmentKind.IMAGE_TEXT, bbox=BBox(x0=5, y0=5 + 10 * i, x1=150, y1=15 + 10 * i),
                           source_text=text, protected_text=text, image=ref, style=SegmentStyle(size=10),
                           translate=translate, skip_reason=reason)

    doc = TranslatedDocument(source_path="x.pdf", source_lang=Lang.ZH, target_lang=Lang.EN,
                             pages=[PageInfo(index=0, width=500, height=700)])
    doc.segments = [line(i, t, False, "slanted text (16°): watermark")
                    for i, t in enumerate(["北京师范大学出版社", "师范大学", "出版社", "410米", "305米"])]
    doc.segments += [line(10 + i, t) for i, t in enumerate(["200米", "150米", "75米", "4米", "10米", "一共多少米"])]
    alphabet = watermark_alphabet(doc)
    assert {"师", "范", "出", "版", "社"} <= alphabet and "米" not in alphabet


def test_single_characters_and_equations():
    from mathtrans.models import BBox, ImageRef, SegmentStyle, TextSegment
    from mathtrans.scanned import _join_lines

    def line(i, x0, y, w, text):
        ref = ImageRef(xref=9, page=0, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                       pixel_box=(int(x0 * 2), int(y * 2), int((x0 + w) * 2), int((y + 12) * 2)))
        return TextSegment(id=f"q{i}", page=0, kind=SegmentKind.IMAGE_TEXT, bbox=BBox(x0=x0, y0=y, x1=x0 + w, y1=y + 12),
                           source_text=text, protected_text=text, image=ref, style=SegmentStyle(size=10, color=0x202020))

    cells = [line(0, 50, 100, 14, "四"), line(1, 50, 114, 14, "四"), line(2, 50, 128, 14, "四")]
    assert all(len(p.members) == 1 for p in group_ocr_lines(cells, 0, Lang.ZH))
    assert _join_lines(["160-35=125（千米)", "350-160=190(千米)", "555-350=205(千米)"], Lang.ZH) == \
        "160-35=125（千米)\n350-160=190(千米)\n555-350=205(千米)"
    assert _join_lines(["数学是由无数个数", "学故事组成的。"], Lang.ZH) == "数学是由无数个数学故事组成的。"
    assert _join_lines(["In a right", "triangle"], Lang.EN) == "In a right triangle"


def test_glyph_erase_keeps_picture_content():
    import numpy as np
    from PIL import Image, ImageDraw
    from mathtrans.fonts import pil_font
    from mathtrans.scanned import _erase_glyphs

    img = Image.new("RGB", (300, 80), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 60, 300, 80], fill=(30, 120, 200))        # a blue ruling / bar crossing the box bottom
    d.text((10, 10), "斜边 c", fill=(20, 20, 20), font=pil_font("zh", 28))
    original = np.array(img)
    canvas = original.copy()
    how = _erase_glyphs(canvas, None, original, None, (0, 0, 300, 80))
    assert how in ("glyphs filled", "glyphs inpainted")
    # the dark ink is gone ...
    ink_before = (original.max(axis=2) < 80).sum()
    ink_after = (canvas.max(axis=2) < 80).sum()
    assert ink_after < 0.1 * ink_before
    # ... while the blue bar inside the box survives (a whole-box fill would have erased it)
    bar = canvas[65:78, 150:290]
    assert np.abs(bar.astype(int) - np.array([30, 120, 200])).max() < 40


def test_scanned_page_boxes_grow_only_into_plain_background(tmp_path):
    import numpy as np
    from PIL import Image, ImageDraw
    from mathtrans.layout import render_document
    from mathtrans.models import BBox, PageInfo, SegmentStyle, TextSegment, TranslatedDocument

    # a "scan": white page image with a dark picture on the right half, below the text box
    img = Image.new("RGB", (1000, 1400), (255, 255, 255))
    ImageDraw.Draw(img).rectangle([520, 150, 980, 900], fill=(60, 90, 160))  # points x 260-490, y 75-450
    img_path = tmp_path / "scan.png"; img.save(img_path)
    pdf = pymupdf.open(); page = pdf.new_page(width=500, height=700)
    page.insert_image(page.rect, filename=str(img_path))
    src = tmp_path / "scan.pdf"; pdf.save(str(src))
    seg = TextSegment(id="p0_s0", page=0, bbox=BBox(x0=40, y0=100, x1=240, y1=124), source_text="一句很短的中文",
                      protected_text="一句很短的中文", style=SegmentStyle(size=12, color=0x202020), origin="ocr",
                      translated_text="A translation that is far too long for the little box it has to go into, so it must grow")
    doc = TranslatedDocument(source_path=str(src), source_lang=Lang.ZH, target_lang=Lang.EN,
                             pages=[PageInfo(index=0, width=500, height=700)], segments=[seg])
    render_document(src, doc, tmp_path / "out.pdf")
    used = seg.render.bbox
    assert used.y1 > 124 or used.x1 > 240  # it grew into the white area ...
    assert used.x1 <= 262  # ... but never over the dark picture that starts at x = 260 points
    assert seg.render.scale > 0.6
