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


def _text_image(size, bg, items):
    import numpy as np
    from PIL import Image, ImageDraw
    from mathtrans.fonts import pil_font

    img = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(img)
    for kind, args, colour in items:
        if kind == "rect":
            d.rectangle(args, fill=colour)
        else:
            xy, text, px = args
            d.text(xy, text, fill=colour, font=pil_font("zh", px))
    return np.array(img)


def test_glyph_erase_handles_coloured_words_and_two_colour_cells():
    import numpy as np
    from mathtrans.scanned import _erase_glyphs

    # a red word inside black text on paper: every glyph goes, whatever its colour
    original = _text_image((320, 60), (255, 255, 255), [
        ("text", ((10, 12), "位是", 32), (20, 20, 20)), ("text", ((80, 12), "百位", 32), (225, 30, 35))])
    canvas = original.copy()
    _erase_glyphs(canvas, None, original, None, (0, 5, 160, 55))
    region = canvas[5:55, 0:160].astype(int)
    assert (region.max(axis=2) < 120).sum() == 0                                  # no dark ink left
    assert ((region[:, :, 0] > 150) & (region[:, :, 1] < 110)).sum() == 0         # no red ink left
    # two label cells of different colours on one OCR line keep their own backgrounds
    original = _text_image((240, 50), (255, 255, 255), [
        ("rect", [0, 0, 119, 49], (205, 255, 255)), ("rect", [120, 0, 239, 49], (255, 250, 205)),
        ("text", ((20, 8), "十位", 30), (10, 10, 10)), ("text", ((140, 8), "个位", 30), (10, 10, 10))])
    canvas = original.copy()
    _erase_glyphs(canvas, None, original, None, (0, 0, 240, 50))
    assert np.abs(canvas[10:40, 15:100].astype(int) - [205, 255, 255]).max() < 40
    assert np.abs(canvas[10:40, 135:220].astype(int) - [255, 250, 205]).max() < 40


def test_glyph_erase_takes_trailing_punctuation_and_keeps_pictograms():
    import numpy as np
    from mathtrans.scanned import _erase_glyphs

    # the OCR box ends before the full stop: the small blob right of it is erased too
    original = _text_image((260, 60), (255, 255, 255), [("text", ((10, 10), "试一试。", 34), (20, 20, 20))])
    ink_cols = np.flatnonzero((original.max(axis=2) < 100).any(axis=0))
    box_right = int(ink_cols.max()) - 30          # cut the box before the 。
    canvas = original.copy()
    _erase_glyphs(canvas, None, original, None, (0, 5, box_right, 55))
    assert (canvas.max(axis=2) < 100).sum() == 0
    # ... unless another OCR line starts right there
    canvas = original.copy()
    _erase_glyphs(canvas, None, original, None, (0, 5, box_right, 55), [(box_right + 5, 5, 260, 55)])
    assert (canvas[:, box_right + 2:].max(axis=2) < 100).sum() > 0
    # a solid coloured pictogram inside the line survives, the glyphs around it go
    original = _text_image((300, 60), (255, 255, 255), [
        ("text", ((10, 10), "用", 34), (20, 20, 20)), ("rect", [60, 12, 100, 50], (240, 160, 20)),
        ("text", ((110, 10), "表示人", 34), (20, 20, 20))])
    canvas = original.copy()
    _erase_glyphs(canvas, None, original, None, (0, 5, 230, 55))
    assert np.abs(canvas[20:45, 68:92].astype(int) - [240, 160, 20]).max() < 30
    assert (canvas.max(axis=2) < 100).sum() == 0


def test_same_row_sentence_pieces_are_joined_with_a_blank():
    lines = [
        _gline(0, 50, 100, 110, "七巧板由"),
        _gline(1, 160, 100, 400, "种图形组成，其中有—个三角形。"),   # after an answer blank
        _gline(2, 50, 125, 110, "种类"), _gline(3, 140, 125, 200, "文学类"), _gline(4, 230, 125, 290, "科普类"),
        _gline(5, 50, 170, 150, "是18吗？"), _gline(6, 170, 170, 290, "比18多得多。"),  # two bubbles
    ]
    unjoined = group_ocr_lines([l.model_copy() for l in lines], 0, Lang.ZH)  # no pixels: nothing joins
    assert all(len(p.members) == 1 for p in unjoined)
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH, blank_check=lambda a, b: True)
    texts = {p.source_text: p.members for p in paragraphs}
    assert texts["七巧板由___种图形组成，其中有—个三角形。"] == ["g0", "g1"]
    assert "种类" in texts and "文学类" in texts and "科普类" in texts      # table cells stay apart
    assert "是18吗？" in texts and "比18多得多。" in texts                  # a finished sentence is not continued
    by = {l.id: l for l in lines}
    assert by["g0"].skip_reason == by["g1"].skip_reason and by["g0"].translate is False


def test_watermark_band_catches_upright_fragments_on_the_diagonal():
    from mathtrans.models import BBox, ImageRef, PageInfo, SegmentStyle, TextSegment, TranslatedDocument
    from mathtrans.scanned import WATERMARK, suppress_watermark_fragments, watermark_alphabet, watermark_band

    def seg(i, page, cx, cy, text, translate=True, reason="", confidence=0.97, w=40.0):
        ref = ImageRef(xref=9, page=page, bbox=BBox(x0=0, y0=0, x1=500, y1=700), width=1000, height=1400,
                       pixel_box=(int((cx - w / 2) * 2), int((cy - 6) * 2), int((cx + w / 2) * 2), int((cy + 6) * 2)),
                       confidence=confidence)
        return TextSegment(id=f"w{i}", page=page, kind=SegmentKind.IMAGE_TEXT,
                           bbox=BBox(x0=cx - w / 2, y0=cy - 6, x1=cx + w / 2, y1=cy + 6), source_text=text,
                           protected_text=text, image=ref, style=SegmentStyle(size=10), translate=translate,
                           skip_reason=reason)

    def on_diag(x):  # the watermark runs from lower left to upper right: y = 0.66 - 0.3 x (page-relative)
        return 700 * (0.66 - 0.3 * x / 500)

    pages = [PageInfo(index=i, width=500, height=700) for i in range(3)]
    doc = TranslatedDocument(source_path="x.pdf", source_lang=Lang.ZH, target_lang=Lang.EN, pages=pages)
    slanted = "slanted text (17°): watermark or decoration, kept as is"
    doc.segments = [
        seg(0, 0, 150, on_diag(150), "北京师范", False, slanted), seg(1, 0, 340, on_diag(340), "学出版社", False, slanted),
        seg(2, 1, 170, on_diag(170), "京师范大", False, slanted), seg(3, 1, 330, on_diag(330), "出版社", False, slanted),
        seg(4, 2, 250, on_diag(250), "范大学出", False, slanted), seg(5, 2, 360, on_diag(360), "版社", False, slanted),
        seg(10, 0, 260, on_diag(260) + 3, "学", w=12),               # upright piece on the diagonal
        seg(11, 1, 290, on_diag(290) - 4, "五", w=12),               # misread of 出 on the diagonal
        seg(12, 2, 200, on_diag(200), "反社", w=24),                 # misread of 版社
        seg(13, 1, 260, on_diag(260) + 120, "五", w=12),             # a real label (五) far from the band
        seg(14, 2, 300, on_diag(300), "学校门口", w=60),             # real text on the band, other letters
        seg(15, 0, 250, on_diag(250), "大小比一比，谁大？", w=150),    # long genuine line crossing the band
    ]
    alphabet = watermark_alphabet(doc)
    band = watermark_band(doc, alphabet)
    assert band is not None and abs(band[0] - (-0.3 * 500 / 700 * 700 / 500)) < 0.05
    suppress_watermark_fragments(doc)
    by = {s.id: s for s in doc.segments}
    assert [by[k].skip_reason for k in ("w10", "w11", "w12")] == [WATERMARK] * 3
    assert by["w13"].translate and by["w14"].translate and by["w15"].translate



def test_underline_blank_check_looks_for_a_rule_in_the_gap():
    import types
    import numpy as np
    from mathtrans.scanned import underline_blank_check

    rgb = np.full((60, 400, 3), 255, np.uint8)
    rgb[46:49, 130:250] = 30            # an answer-blank underline between x 120 and 260
    rgb[10:45, 300:340] = (240, 160, 20)  # a picture in the second gap (x 280 .. 360)
    loaded = types.SimpleNamespace(rgb=rgb)
    check = underline_blank_check(lambda xref: loaded)
    left, mid, right = _gline(0, 10, 10, 60, "七巧板由"), _gline(1, 130, 10, 140, "种图形"), _gline(2, 180, 10, 200, "个。")
    left.image = left.image.model_copy(update={"pixel_box": (20, 12, 120, 44)})
    mid.image = mid.image.model_copy(update={"pixel_box": (260, 12, 280, 44)})
    right.image = right.image.model_copy(update={"pixel_box": (360, 12, 395, 44)})
    assert check(left, mid) is True
    assert check(mid, right) is False
    # a narrow empty gap (one sentence split at a quoted mark) joins too; a wide empty one does not
    near = _gline(3, 10, 10, 60, "多的画")
    near.image = near.image.model_copy(update={"pixel_box": (290, 12, 300, 44)})
    after = _gline(4, 10, 10, 60, "“✓”。")
    after.image = after.image.model_copy(update={"pixel_box": (330, 12, 340, 44)})
    rgb[10:45, 300:340] = 255
    assert check(near, after) is True
    after.image = after.image.model_copy(update={"pixel_box": (395, 12, 399, 44)})
    assert check(near, after) is False


def test_watermark_lines_are_not_layout_obstacles():
    import pymupdf
    from mathtrans.layout import _PageSpace
    from mathtrans.models import PageInfo, TranslatedDocument

    pdf = pymupdf.open()
    page = pdf.new_page(width=500, height=700)
    wm = _gline(0, 200, 300, 420, "北京师范大学出版社")
    wm.translate, wm.skip_reason = False, "slanted text (20°): watermark or decoration, kept as is"
    frag = _gline(1, 300, 320, 330, "版社")
    frag.translate, frag.skip_reason = False, "watermark fragment"
    label = _gline(2, 50, 400, 90, "12")
    label.translate, label.skip_reason = False, "pure number / formula"
    doc = TranslatedDocument(source_path="x.pdf", source_lang=Lang.ZH, target_lang=Lang.EN,
                             pages=[PageInfo(index=0, width=500, height=700)], segments=[wm, frag, label])
    space = _PageSpace(page, 0, doc)
    assert set(space.occupied) == {"g2"}   # numbers left in the picture still block, the watermark does not



def test_left_aligned_tail_of_a_sentence_joins_its_paragraph():
    lines = [
        _gline(0, 90, 477, 464, "请用轴对称或平移的知识，为自己的班级设计班徽。与同伴说一说你的"),
        _gline(1, 90, 491, 146, "设计意图。"),                 # short tail, left-aligned, sentence unfinished above
        _gline(2, 300, 520, 340, "合计"),                     # a short label under a long line stays alone
        _gline(3, 90, 540, 460, "这是一句完整的话，到这里结束了。"),
        _gline(4, 90, 554, 140, "下一题"),                    # after a full stop: not a tail
    ]
    paragraphs = group_ocr_lines(lines, 0, Lang.ZH)
    members = sorted(p.members for p in paragraphs)
    assert ["g0", "g1"] in members and ["g2"] in members and ["g3"] in members and ["g4"] in members


def test_dropped_unit_labels_are_marked_for_erasing():
    from mathtrans.scanned import UNIT_DROPPED

    unit = _gline(0, 200, 100, 230, "（个）")
    unit.translate, unit.skip_reason = False, UNIT_DROPPED
    sentence = _gline(1, 50, 130, 300, "树上有8个桃子，摘了3个。")
    paragraphs = group_ocr_lines([unit, sentence], 0, Lang.ZH)
    assert [p.members for p in paragraphs] == [["g1"]]                 # nothing is set for the unit ...
    assert unit.skip_reason == f"{MERGED} {UNIT_DROPPED}"              # ... but it is erased with the merged lines
