"""Tests for mathtrans.ocr and mathtrans.images (OCR + in-image text replacement)."""
from __future__ import annotations

import base64
import io
import json
import logging
import re
import sys
import types
from pathlib import Path

import anthropic
import httpx2 as httpx
import numpy as np
import pymupdf
import pytest
from PIL import Image, ImageDraw

from mathtrans.config import Settings, get_settings, reset_settings
from mathtrans.fonts import pil_font
from mathtrans.images import (MAX_IMAGE_PX, UNRELIABLE_OCR_KO, LoadedImage, classify_ocr_text, estimate_background,
                              extract_image_segments, load_image, pixel_polygon_to_page, render_image_segments,
                              replace_image, restore_superscripts)
from mathtrans.models import (BBox, ImageRef, Lang, OcrResult, PageInfo, PipelineOptions, RenderInfo, SegmentKind,
                              TextSegment, TranslatedDocument)
from mathtrans.ocr import (DOWNSCALE_MAX_SIDE, ClaudeVisionOcrEngine, NullOcrEngine, OcrError, OcrUnavailableError,
                           RapidOcrEngine, get_ocr_engine, ocr_low_trust, parse_vision_ocr_json)
from mathtrans.pipeline import run_pipeline
from mathtrans.qa import checks as qa_checks
from mathtrans.samples import make_sample_pdf
from mathtrans.translate.mock import MockTranslator

SEG_ID_RE = re.compile(r"^p(\d+)_i(\d+)_(\d+)$")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #


def make_doc(pdf_path: Path | str, src: Lang, tgt: Lang) -> TranslatedDocument:
    with pymupdf.open(str(pdf_path)) as pdf:
        pages = [PageInfo(index=p.number, width=p.rect.width, height=p.rect.height) for p in pdf]
    return TranslatedDocument(source_path=str(pdf_path), source_lang=src, target_lang=tgt, pages=pages)


class FakeOcr:
    """Returns canned results for every image (polygons are rectangles)."""

    name = "fake"

    def __init__(self, items: list[tuple[str, tuple[int, int, int, int], float]]):
        self.items = items
        self.calls = 0

    def recognize(self, image_rgb, hint_langs=None):
        self.calls += 1
        out = []
        for text, (x0, y0, x1, y1), conf in self.items:
            out.append(OcrResult(text=text, polygon=[[x0, y0], [x1, y0], [x1, y1], [x0, y1]], confidence=conf))
        return out


class FakeMessages:
    def __init__(self, response):
        self.response = response
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class FakeClient:
    def __init__(self, response):
        self.messages = FakeMessages(response)


def text_response(text: str, stop_reason: str = "end_turn"):
    block = types.SimpleNamespace(type="text", text=text)
    return types.SimpleNamespace(content=[block], stop_reason=stop_reason)


def draw_label_image(size: tuple[int, int], text: str, lang: str, xy: tuple[int, int], px: int,
                     fill=(0, 0, 0), background="white", mode: str = "RGB") -> tuple[Image.Image, tuple[int, int, int, int]]:
    """Image with one text label; returns the image and the ink box of the label."""
    img = Image.new(mode, size, background)
    d = ImageDraw.Draw(img)
    font = pil_font(lang, px)
    d.text(xy, text, fill=fill, font=font)
    box = d.textbbox(xy, text, font=font)
    return img, tuple(int(v) for v in box)


def pdf_with_image(path: Path, image: Image.Image, rect: pymupdf.Rect, *, extra_pages: int = 0,
                   share_on_pages: int = 0) -> int:
    """Write a PDF placing ``image`` at ``rect``; optionally re-use the same xref on more pages."""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=400)
    xref = page.insert_image(rect, stream=buf.getvalue())
    for _ in range(share_on_pages):
        p = pdf.new_page(width=400, height=400)
        p.insert_image(pymupdf.Rect(20, 20, 220, 120), xref=xref)
    for _ in range(extra_pages):
        pdf.new_page(width=400, height=400)
    pdf.save(str(path))
    pdf.close()
    return xref


def image_segment(seg_id: str, page: int, xref: int, image_bbox: BBox, size: tuple[int, int],
                  box: tuple[int, int, int, int], text: str, translated: str, src: Lang) -> TextSegment:
    ref = ImageRef(xref=xref, page=page, bbox=image_bbox, width=size[0], height=size[1], pixel_box=box,
                   polygon=[[box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]])
    sx, sy = image_bbox.width / size[0], image_bbox.height / size[1]
    bbox = BBox(x0=image_bbox.x0 + box[0] * sx, y0=image_bbox.y0 + box[1] * sy,
                x1=image_bbox.x0 + box[2] * sx, y1=image_bbox.y0 + box[3] * sy)
    protected, frags, translate, reason = classify_ocr_text(text, src)
    return TextSegment(id=seg_id, page=page, kind=SegmentKind.IMAGE_TEXT, bbox=bbox, source_text=text,
                       protected_text=protected, protected=frags, image=ref, translate=translate,
                       skip_reason=reason, translated_text=translated)


def page_image_info(pdf: pymupdf.Document, page_index: int) -> dict:
    infos = pdf[page_index].get_image_info(xrefs=True, hashes=True)
    assert len(infos) == 1
    return infos[0]


@pytest.fixture(scope="module")
def rapid() -> RapidOcrEngine:
    engine = RapidOcrEngine()
    assert engine.recognize(np.full((80, 200, 3), 255, dtype=np.uint8)) == []  # warms the model up
    return engine


@pytest.fixture(scope="module")
def zh_segments(sample_pdf_zh, rapid):
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    return doc, extract_image_segments(sample_pdf_zh, doc, rapid)


# --------------------------------------------------------------------------- #
# extraction with the real OCR engine
# --------------------------------------------------------------------------- #


def test_rapid_ocr_finds_labels_in_sample_zh(zh_segments, sample_pdf_zh):
    doc, segs = zh_segments
    assert segs and all(s.kind == SegmentKind.IMAGE_TEXT and s.image is not None for s in segs)
    assert all(SEG_ID_RE.match(s.id) for s in segs)
    assert len({s.id for s in segs}) == len(segs)
    page0 = [s for s in segs if s.page == 0]
    texts = [s.source_text.replace(" ", "") for s in page0]
    assert any("斜边" in t for t in texts)
    assert any("图" in t and "1-1" in t for t in texts)
    with pymupdf.open(str(sample_pdf_zh)) as pdf:
        info = page_image_info(pdf, 0)
    image_bbox = BBox.from_rect(info["bbox"])
    for s in page0:
        assert s.image.xref == info["xref"]
        assert s.image.bbox == image_bbox
        assert (s.image.width, s.image.height) == (info["width"], info["height"])
        assert image_bbox.contains(s.bbox), (s.id, s.bbox, image_bbox)
        assert s.bbox.width > 0 and s.bbox.height > 0
        x0, y0, x1, y1 = s.image.pixel_box
        assert 0 <= x0 < x1 <= info["width"] and 0 <= y0 < y1 <= info["height"]
        assert s.style.size > 0
    label = next(s for s in page0 if "斜边" in s.source_text)
    assert label.translate and label.protected_text.startswith("斜边")
    assert label.style.size == pytest.approx(13, abs=3)  # 26 px glyphs placed at half scale
    r, g, b = label.style.color >> 16, (label.style.color >> 8) & 255, label.style.color & 255
    assert r > 150 and g < 90 and b < 90  # the label is red in the sample
    assert any(s.page == 1 and "正方形" in s.source_text for s in segs)
    assert [s.reading_order for s in segs] == list(range(len(segs)))


def test_label_letters_are_not_translatable(zh_segments):
    _doc, segs = zh_segments
    letters = [s for s in segs if s.source_text.strip() in {"A", "B", "C", "a", "b"}]
    assert len(letters) >= 3
    for s in letters:
        assert s.translate is False
        assert s.skip_reason == "single letter"


def test_render_replaces_text_in_image(zh_segments, sample_pdf_zh, rapid, tmp_path):
    doc, segs = zh_segments
    doc = doc.model_copy(deep=True)
    doc.segments = [s.model_copy(deep=True) for s in segs]
    for s in doc.segments:
        if "斜边" in s.source_text:
            s.translated_text = "hypotenuse c"
        elif "图" in s.source_text:
            s.translated_text = "Figure 1-1"
    pdf = pymupdf.open(str(sample_pdf_zh))
    before = page_image_info(pdf, 0)
    modified = render_image_segments(pdf, doc)
    assert modified == 1  # only the page-0 image has translations
    out = tmp_path / "out.pdf"
    pdf.save(str(out), garbage=3)
    pdf.close()

    rendered = [s for s in doc.segments if s.translated_text]
    assert len(rendered) == 2
    for s in rendered:
        assert s.render is not None and s.render.font_size > 0 and 0 < s.render.scale <= 1.0
        assert s.render.bbox is not None and s.image.bbox.contains(s.render.bbox, tol=1.0)
        assert not s.render.overflow
    assert all(s.render is None for s in doc.segments if not s.translated_text)

    with pymupdf.open(str(out)) as pdf2:
        assert pdf2.page_count == 2
        after = page_image_info(pdf2, 0)
        assert after["bbox"] == before["bbox"]
        assert (after["width"], after["height"]) == (before["width"], before["height"])
        assert after["digest"] != before["digest"]
        loaded = load_image(pdf2, after["xref"])
        assert loaded.rgb.shape == (before["height"], before["width"], 3)
        texts = [r.text for r in rapid.recognize(loaded.rgb)]
        assert page_image_info(pdf2, 1)["digest"] == page_image_info(pymupdf.open(str(sample_pdf_zh)), 1)["digest"]
    joined = " ".join(texts)
    assert "hypotenuse" in joined
    assert "Figure" in joined
    assert "斜边" not in joined and "图" not in joined
    assert any(t in {"A", "B", "C"} for t in texts)  # untouched labels still there


def test_cjk_target_drawing(sample_pdf_en, rapid, tmp_path):
    doc = make_doc(sample_pdf_en, Lang.EN, Lang.ZH)
    doc.segments = extract_image_segments(sample_pdf_en, doc, rapid, pages=[0])
    seg = next(s for s in doc.segments if "hypotenuse" in s.source_text.lower())
    assert seg.translate
    seg.translated_text = "斜边 c"
    pdf = pymupdf.open(str(sample_pdf_en))
    assert render_image_segments(pdf, doc) == 1
    out = tmp_path / "en_zh.pdf"
    pdf.save(str(out))
    pdf.close()
    with pymupdf.open(str(out)) as pdf2:
        info = page_image_info(pdf2, 0)
        loaded = load_image(pdf2, info["xref"])
    x0, y0, x1, y1 = seg.image.pixel_box
    region = loaded.rgb[y0:y1, x0:x1]
    assert region.size and (region.min(axis=2) < 200).sum() > 40  # glyph pixels drawn
    assert region.min(axis=2).min() < 120
    assert "斜边" in "".join(r.text for r in rapid.recognize(loaded.rgb)).replace(" ", "")
    assert seg.render is not None and seg.render.font_size > 0 and not seg.render.overflow


# --------------------------------------------------------------------------- #
# extraction with a fake engine
# --------------------------------------------------------------------------- #


def test_min_confidence_filtering(sample_pdf_zh):
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    engine = FakeOcr([("斜边 c", (250, 150, 330, 180), 0.9), ("直角边", (100, 100, 180, 130), 0.3)])
    segs = extract_image_segments(sample_pdf_zh, doc, engine, pages=[0])
    assert [s.source_text for s in segs] == ["斜边 c"]
    assert engine.calls == 1
    segs = extract_image_segments(sample_pdf_zh, doc, engine, pages=[0], min_confidence=0.2)
    assert [s.source_text for s in segs] == ["斜边 c", "直角边"]
    assert [s.id for s in segs] == [f"p0_i{segs[0].image.xref}_0", f"p0_i{segs[0].image.xref}_1"]
    assert segs[1].image.confidence == pytest.approx(0.3)


def test_skip_rules_for_numbers_letters_and_foreign_script(sample_pdf_zh):
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    items = [("123", (10, 10, 40, 30), 0.99), ("a²+b²=c²", (10, 40, 120, 60), 0.99), ("ABC", (10, 70, 60, 90), 0.99),
             ("斜边 c", (10, 100, 90, 130), 0.99), ("x", (10, 140, 20, 160), 0.99), ("   ", (10, 170, 20, 180), 0.99),
             ("Figure", (10, 190, 80, 210), 0.99), ("빗변", (10, 220, 80, 240), 0.99), ("图", (10, 250, 40, 280), 0.99)]
    segs = extract_image_segments(sample_pdf_zh, doc, FakeOcr(items), pages=[0])
    by_text = {s.source_text: s for s in segs}
    assert len(segs) == 9
    assert (by_text["123"].translate, by_text["123"].skip_reason) == (False, "pure number / formula")
    assert (by_text["a²+b²=c²"].translate, by_text["a²+b²=c²"].skip_reason) == (False, "pure number / formula")
    assert (by_text["ABC"].translate, by_text["ABC"].skip_reason) == (False, "pure number / formula")  # label
    # Latin words inside a CJK document's figure are translated, like the text extractor does;
    # text in a third script (hangul in a Chinese book) is left alone
    assert (by_text["Figure"].translate, by_text["Figure"].skip_reason) == (True, "")
    assert (by_text["빗변"].translate, by_text["빗변"].skip_reason) == (False, "no source-script letters")
    assert (by_text["x"].translate, by_text["x"].skip_reason) == (False, "single letter")
    assert (by_text["图"].translate, by_text["图"].skip_reason) == (True, "")  # a single CJK character is a word
    assert (by_text[""].translate, by_text[""].skip_reason) == (False, "empty")
    assert by_text["斜边 c"].translate and by_text["斜边 c"].protected_text == "斜边 ⟦0⟧"
    assert by_text["斜边 c"].protected == ["c"]
    # Latin-script source
    assert classify_ocr_text("Figure 1-1", Lang.EN)[2:] == (True, "")
    assert classify_ocr_text("AB", Lang.EN)[2:] == (False, "pure number / formula")
    assert classify_ocr_text("a", Lang.EN)[2:] == (False, "single letter")
    assert classify_ocr_text("α", Lang.EN)[2:] == (False, "single letter")
    assert classify_ocr_text("Area = c²", Lang.EN)[2:] == (True, "")
    assert classify_ocr_text("斜边", Lang.EN)[2:] == (False, "no source-script letters")
    # Korean sanity gate: the zh/en OCR models misread hangul as look-alike Han characters
    # ("빗변 c" -> "臣C"); Han-only text in a Korean figure is a misread, not a hanja label
    assert classify_ocr_text("臣C", Lang.KO)[2] is False
    assert classify_ocr_text("二 1-1", Lang.KO)[2] is False
    assert classify_ocr_text("豇=c2", Lang.KO)[2] is False
    assert classify_ocr_text("빗변 c", Lang.KO)[2:] == (True, "")
    assert classify_ocr_text("Area = c²", Lang.KO)[2:] == (True, "")
    assert classify_ocr_text("斜辺 c", Lang.JA)[2:] == (True, "")


def test_pages_filter_and_min_image_px(sample_pdf_zh):
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    engine = FakeOcr([("斜边 c", (10, 10, 90, 40), 0.9)])
    segs = extract_image_segments(sample_pdf_zh, doc, engine, pages=[1])
    assert segs and all(s.page == 1 for s in segs)
    assert engine.calls == 1
    assert extract_image_segments(sample_pdf_zh, doc, engine, min_image_px=1000) == []
    assert extract_image_segments(sample_pdf_zh, doc, NullOcrEngine()) == []


def test_shared_image_processed_once_and_replaced_everywhere(tmp_path):
    img, box = draw_label_image((300, 150), "斜边 c", "zh", (40, 50), 36, fill=(200, 30, 30))
    path = tmp_path / "shared.pdf"
    xref = pdf_with_image(path, img, pymupdf.Rect(50, 50, 350, 200), share_on_pages=1)
    doc = make_doc(path, Lang.ZH, Lang.EN)
    engine = FakeOcr([("斜边 c", box, 0.95)])
    segs = extract_image_segments(path, doc, engine)
    assert engine.calls == 1
    assert [(s.page, s.image.xref) for s in segs] == [(0, xref)]
    segs[0].translated_text = "hypotenuse c"
    doc.segments = segs
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1
    out = tmp_path / "shared_out.pdf"
    pdf.save(str(out), garbage=3)
    pdf.close()
    with pymupdf.open(str(out)) as pdf2:
        a, b = page_image_info(pdf2, 0), page_image_info(pdf2, 1)
        assert a["digest"] == b["digest"]
        assert a["bbox"] == (50.0, 50.0, 350.0, 200.0) and b["bbox"] == (20.0, 20.0, 220.0, 120.0)
        loaded = load_image(pdf2, a["xref"])
    assert loaded.rgb.shape == (150, 300, 3)
    x0, y0, x1, y1 = box
    region = loaded.rgb[y0:y1, x0:x1].astype(int)
    assert ((region[..., 0] > 150) & (region[..., 1] < 90)).sum() > 30  # red glyphs drawn
    assert not np.array_equal(region, np.array(img)[y0:y1, x0:x1])


# --------------------------------------------------------------------------- #
# rendering details
# --------------------------------------------------------------------------- #


def test_rgba_image_keeps_alpha_after_replacement(tmp_path):
    img, box = draw_label_image((320, 120), "斜边 c", "zh", (30, 30), 40, fill=(0, 0, 0), background=(0, 0, 0, 0),
                                mode="RGBA")
    path = tmp_path / "rgba.pdf"
    rect = pymupdf.Rect(40, 40, 360, 160)
    xref = pdf_with_image(path, img, rect)
    pdf = pymupdf.open(str(path))
    loaded = load_image(pdf, xref)
    assert loaded.alpha is not None and loaded.alpha.max() == 255 and loaded.alpha.min() == 0
    seg = image_segment("p0_i%d_0" % xref, 0, xref, BBox.from_rect(rect), (320, 120), box, "斜边 c", "hypotenuse c",
                        Lang.ZH)
    doc = make_doc(path, Lang.ZH, Lang.EN)
    doc.segments = [seg]
    assert render_image_segments(pdf, doc) == 1
    out = tmp_path / "rgba_out.pdf"
    pdf.save(str(out), garbage=3)
    pdf.close()
    with pymupdf.open(str(out)) as pdf2:
        info = page_image_info(pdf2, 0)
        assert info["bbox"] == tuple(rect) and (info["width"], info["height"]) == (320, 120)
        assert pdf2.extract_image(info["xref"])["smask"] != 0
        after = load_image(pdf2, info["xref"])
        pix = pdf2[0].get_pixmap(dpi=72)
    assert after.alpha is not None and after.alpha.shape == (120, 320)
    x0, y0, x1, y1 = box
    outside = np.ones_like(after.alpha, dtype=bool)
    outside[y0:y1, x0:x1] = False
    assert after.alpha[outside].max() == 0  # transparency outside the box untouched
    assert (after.alpha[y0:y1, x0:x1] > 100).sum() > 50  # new glyphs are opaque (edges anti-aliased)
    assert (after.alpha[y0:y1, x0:x1] == 0).sum() > 50  # box background stays transparent
    glyphs = after.rgb[y0:y1, x0:x1][after.alpha[y0:y1, x0:x1] > 200]
    assert glyphs.size and glyphs.max() < 60  # black text stays black
    page = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    assert tuple(page[45, 45][:3]) == (255, 255, 255)  # transparent corner shows the white page


def test_non_uniform_background_is_inpainted(tmp_path):
    w, h = 360, 120
    gradient = np.linspace(40, 230, w, dtype=np.uint8)
    arr = np.dstack([np.tile(gradient, (h, 1))] * 3)
    img = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(img)
    font = pil_font("en", 34)
    d.text((20, 40), "Gradient label text", fill=(0, 0, 0), font=font)
    box = tuple(int(v) for v in d.textbbox((20, 40), "Gradient label text", font=font))
    path = tmp_path / "gradient.pdf"
    rect = pymupdf.Rect(20, 20, 380, 140)
    xref = pdf_with_image(path, img, rect)
    seg = image_segment("p0_i%d_0" % xref, 0, xref, BBox.from_rect(rect), (w, h), box, "Gradient label text", "Hi",
                        Lang.EN)
    doc = make_doc(path, Lang.EN, Lang.ZH)
    doc.segments = [seg]
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1
    out = load_image(pdf, xref).rgb
    pdf.close()
    assert seg.render is not None and seg.render.notes.startswith("inpainted")
    x0, y0, x1, y1 = box
    left = out[y0:y1, x0:x0 + 12]  # original glyphs started here; the short centred text does not reach it
    assert (np.array(img)[y0:y1, x0:x0 + 12].min(axis=2) < 30).any()
    assert not (left.min(axis=2) < 30).any()
    expected = gradient[x0:x0 + 12].astype(int)
    assert np.abs(left[..., 0].astype(int) - expected[None, :]).mean() < 25  # gradient reconstructed
    assert (out[y0:y1, x0:x1].min(axis=2) < 30).any()  # new black text present


def test_render_skips_untranslated_and_overflow_is_reported(tmp_path):
    img, box = draw_label_image((200, 60), "ab", "en", (10, 10), 30)
    path = tmp_path / "tiny.pdf"
    rect = pymupdf.Rect(0, 0, 200, 60)
    xref = pdf_with_image(path, img, rect)
    doc = make_doc(path, Lang.EN, Lang.ZH)
    untouched = image_segment("p0_i%d_0" % xref, 0, xref, BBox.from_rect(rect), (200, 60), box, "ab", None, Lang.EN)
    untouched.translate = True
    pdf = pymupdf.open(str(path))
    doc.segments = [untouched]
    assert render_image_segments(pdf, doc) == 0 and untouched.render is None
    skipped = image_segment("p0_i%d_1" % xref, 0, xref, BBox.from_rect(rect), (200, 60), box, "AB", "xyz", Lang.EN)
    assert skipped.translate is False  # "AB" is a protected geometry label
    doc.segments = [skipped]
    assert render_image_segments(pdf, doc) == 0
    # a very long translation into a small box ends at the minimum size with overflow flagged
    # (even after growing into the free background next to the box)
    long_seg = image_segment("p0_i%d_2" % xref, 0, xref, BBox.from_rect(rect), (200, 60), (10, 10, 50, 30),
                             "Hello", "an extremely long translated label that cannot possibly fit into the "
                             "tiny box, not even at the minimum font size and spread over two lines", Lang.EN)
    long_seg.translate = True
    doc.segments = [long_seg]
    assert render_image_segments(pdf, doc) == 1
    pdf.close()
    assert long_seg.render is not None and long_seg.render.overflow
    assert long_seg.render.scale < 1.0 and long_seg.render.font_size > 0


OPTIONAL_FONTS = Path("/tmp/claude-0/-home-user-math-material-translation/1e147c18-6fbd-5cf2-9102-87b84ab13c2e/scratchpad/fonts")


@pytest.mark.skipif(not (OPTIONAL_FONTS / "NotoSansKR-Regular.ttf").is_file(), reason="optional Noto fonts absent")
def test_fonts_dir_override_is_used(tmp_path):
    img, box = draw_label_image((320, 100), "hypotenuse c", "en", (20, 30), 32, fill=(200, 30, 30))
    path = tmp_path / "fonts.pdf"
    rect = pymupdf.Rect(0, 0, 320, 100)
    xref = pdf_with_image(path, img, rect)
    seg = image_segment("p0_i%d_0" % xref, 0, xref, BBox.from_rect(rect), (320, 100), box, "hypotenuse c", "빗변 c",
                        Lang.EN)
    doc = make_doc(path, Lang.EN, Lang.KO)
    doc.segments = [seg]
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc, fonts_dir=OPTIONAL_FONTS) == 1
    out = load_image(pdf, xref).rgb
    pdf.close()
    assert seg.render is not None and seg.render.notes.endswith("font NotoSansKR-Regular.ttf")
    x0, y0, x1, y1 = box
    region = out[y0:y1, x0:x1].astype(int)
    assert ((region[..., 0] > 150) & (region[..., 1] < 90)).sum() > 40  # red hangul glyphs drawn
    doc.segments[0].render = None
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1  # without the override the system CJK font is used
    pdf.close()
    assert "wqy-zenhei" in seg.render.notes or "Droid" in seg.render.notes or "Noto" in seg.render.notes


def test_pixel_polygon_to_page_mapping():
    poly = [[170, 13], [245, 13], [245, 41], [170, 41]]
    bbox = pixel_polygon_to_page(poly, 480, 360, (240.0, 0.0, 0.0, 180.0, 80.0, 225.0))
    assert bbox.as_tuple() == pytest.approx((165.0, 231.5, 202.5, 245.5))
    # 90 degree rotated placement: unit square -> page x = 320 - 240*v, page y = 225 + 180*u
    rotated = pixel_polygon_to_page([[0, 0], [48, 0], [48, 36], [0, 36]], 480, 360,
                                    (0.0, 180.0, -240.0, 0.0, 320.0, 225.0))
    assert rotated.as_tuple() == pytest.approx((296.0, 225.0, 320.0, 243.0))


def test_load_image_handles_gray_and_cmyk(tmp_path):
    pdf = pymupdf.open()
    page = pdf.new_page()
    g = io.BytesIO()
    Image.new("L", (100, 50), 128).save(g, format="PNG")
    page.insert_image(pymupdf.Rect(0, 0, 100, 50), stream=g.getvalue())
    c = io.BytesIO()
    Image.new("CMYK", (100, 50), (0, 255, 255, 0)).save(c, format="JPEG")
    page.insert_image(pymupdf.Rect(0, 60, 100, 110), stream=c.getvalue())
    infos = page.get_image_info(xrefs=True)
    gray = load_image(pdf, infos[0]["xref"])
    cmyk = load_image(pdf, infos[1]["xref"])
    pdf.close()
    assert gray.rgb.shape == (50, 100, 3) and gray.alpha is None and abs(int(gray.rgb[25, 50, 0]) - 128) <= 2
    assert cmyk.rgb.shape == (50, 100, 3) and cmyk.alpha is None
    r, g_, b = (int(v) for v in cmyk.rgb[25, 50])
    assert r > 150 and g_ < 100 and b < 100  # C=0, M=Y=255 is red


# --------------------------------------------------------------------------- #
# OCR engines
# --------------------------------------------------------------------------- #


def test_claude_vision_engine_parses_canned_response(offline_settings):
    canned = {"items": [{"text": "斜边 c", "box": [500, 400, 700, 500]},
                        {"text": "", "box": [0, 0, 10, 10]},
                        {"text": "bad", "box": [1, 2]},
                        {"text": "A", "box": [10, 20, 30, 40], "confidence": 0.5}]}
    client = FakeClient(text_response(json.dumps(canned)))
    engine = ClaudeVisionOcrEngine(client=client, settings=offline_settings)
    assert engine.name == "claude" and engine.model == offline_settings.claude_model
    image = np.full((360, 480, 3), 255, dtype=np.uint8)
    results = engine.recognize(image, hint_langs=[Lang.ZH])
    assert [r.text for r in results] == ["斜边 c", "A"]
    assert results[0].polygon == [[240.0, 144.0], [336.0, 144.0], [336.0, 180.0], [240.0, 180.0]]
    assert results[0].box == (240, 144, 336, 180) and results[0].confidence == 1.0
    assert results[1].confidence == 0.5
    assert len(client.messages.calls) == 1
    req = client.messages.calls[0]
    assert req["model"] == offline_settings.claude_model and req["max_tokens"] == 16000
    assert "thinking" not in req
    assert req["output_config"]["format"]["type"] == "json_schema"
    assert req["output_config"]["format"]["schema"]["required"] == ["items"]
    content = req["messages"][0]["content"]
    assert content[0]["type"] == "image" and content[0]["source"]["media_type"] == "image/png"
    png = Image.open(io.BytesIO(base64.standard_b64decode(content[0]["source"]["data"])))
    assert png.size == (480, 360)
    assert content[1]["type"] == "text" and "Chinese" in content[1]["text"]
    # bare list answers and explicit model override are accepted too
    engine2 = ClaudeVisionOcrEngine(client=FakeClient(text_response(json.dumps([{"text": "x", "box": [0, 0, 1000, 1000]}]))),
                                    model="claude-sonnet-5-5", settings=offline_settings)
    assert engine2.model == "claude-sonnet-5-5"
    assert engine2.recognize(image)[0].box == (0, 0, 480, 360)


def test_claude_vision_engine_errors(offline_settings):
    image = np.full((100, 100, 3), 255, dtype=np.uint8)
    refused = ClaudeVisionOcrEngine(client=FakeClient(text_response("", stop_reason="refusal")),
                                    settings=offline_settings)
    assert refused.recognize(image) == []
    broken = ClaudeVisionOcrEngine(client=FakeClient(text_response("not json")), settings=offline_settings)
    with pytest.raises(OcrError, match="invalid JSON"):
        broken.recognize(image)
    truncated = ClaudeVisionOcrEngine(client=FakeClient(text_response("[", stop_reason="max_tokens")),
                                      settings=offline_settings)
    with pytest.raises(OcrError, match="truncated"):
        truncated.recognize(image)

    class Boom:
        def create(self, **kwargs):
            raise RuntimeError("network down")

    failing = ClaudeVisionOcrEngine(client=types.SimpleNamespace(messages=Boom()), settings=offline_settings)
    with pytest.raises(OcrError, match="network down"):
        failing.recognize(image)
    with pytest.raises(OcrError):
        parse_vision_ocr_json({"foo": 1}, 10, 10)
    # big images are downscaled before upload but coordinates stay in the original pixel space
    big = ClaudeVisionOcrEngine(client=FakeClient(text_response(json.dumps({"items": [{"text": "t", "box": [0, 0, 500, 500]}]}))),
                                settings=offline_settings)
    res = big.recognize(np.full((2000, 4000, 3), 255, dtype=np.uint8))
    assert res[0].box == (0, 0, 2000, 1000)
    sent = Image.open(io.BytesIO(base64.standard_b64decode(
        big._client.messages.calls[0]["messages"][0]["content"][0]["source"]["data"])))
    assert max(sent.size) == 1568


def test_get_ocr_engine_selection(offline_settings, monkeypatch, caplog):
    assert isinstance(get_ocr_engine("rapid", offline_settings), RapidOcrEngine)
    assert isinstance(get_ocr_engine("none", offline_settings), NullOcrEngine)
    assert isinstance(get_ocr_engine("auto", offline_settings), RapidOcrEngine)
    assert isinstance(get_ocr_engine("AUTO", offline_settings), RapidOcrEngine)
    with caplog.at_level(logging.WARNING, logger="mathtrans.ocr"):
        assert isinstance(get_ocr_engine("claude", offline_settings), RapidOcrEngine)  # no key -> fallback
    assert any("no ANTHROPIC_API_KEY" in r.message for r in caplog.records)
    with pytest.raises(ValueError, match="unknown OCR engine"):
        get_ocr_engine("tesseract", offline_settings)

    monkeypatch.setattr(RapidOcrEngine, "available", staticmethod(lambda: False))
    assert isinstance(get_ocr_engine("auto", offline_settings), NullOcrEngine)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    reset_settings()
    try:
        keyed = get_settings()
        assert keyed.has_api_key
        engine = get_ocr_engine("auto", keyed)
        assert isinstance(engine, ClaudeVisionOcrEngine) and engine.model == keyed.claude_model
        assert isinstance(get_ocr_engine("claude", keyed), ClaudeVisionOcrEngine)
        assert isinstance(get_ocr_engine("rapid", keyed), RapidOcrEngine)
    finally:
        reset_settings()


def test_rapid_engine_import_failure_returns_empty(monkeypatch, caplog):
    RapidOcrEngine.reset()
    try:
        monkeypatch.setitem(sys.modules, "rapidocr_onnxruntime", None)  # makes the import raise ImportError
        engine = RapidOcrEngine()
        image = np.full((50, 50, 3), 255, dtype=np.uint8)
        with caplog.at_level(logging.WARNING, logger="mathtrans.ocr"):
            assert engine.recognize(image) == []
            assert engine.recognize(image) == []
            assert RapidOcrEngine().recognize(image) == []
        warnings = [r for r in caplog.records if "RapidOCR is unavailable" in r.message]
        assert len(warnings) == 1
        assert RapidOcrEngine.available() is False
    finally:
        monkeypatch.undo()
        RapidOcrEngine.reset()
    assert RapidOcrEngine.available()


def test_rapid_engine_upscales_small_images_and_scales_boxes_back(rapid):
    img, box = draw_label_image((300, 90), "斜边 c", "zh", (20, 20), 36)
    arr = np.array(img)
    results = rapid.recognize(arr, hint_langs=[Lang.ZH])
    assert results
    hit = next(r for r in results if "斜边" in r.text)
    x0, y0, x1, y1 = hit.box
    assert 0 <= x0 <= box[0] + 6 and x1 >= box[2] - 6 and x1 <= 300  # boxes are back in 300x90 space
    assert 0 <= y0 <= box[1] + 6 and y1 >= box[3] - 6 and y1 <= 90
    assert 0 < hit.confidence <= 1.0
    # gray and RGBA inputs are accepted too
    assert any("斜边" in r.text for r in rapid.recognize(np.array(img.convert("L"))))
    assert any("斜边" in r.text for r in rapid.recognize(np.array(img.convert("RGBA"))))
    assert NullOcrEngine().recognize(arr) == [] and NullOcrEngine().name == "none"


# --------------------------------------------------------------------------- #
# adversarial cases (verifier)
# --------------------------------------------------------------------------- #


def stencil_mask_pdf(path: Path, text: str, lang: str, px: int, rect: pymupdf.Rect) -> tuple[int, tuple[int, int, int, int]]:
    """A PDF whose only image is a 1-bit stencil mask (``/ImageMask true``), painted in dark blue."""
    img = Image.new("1", (240, 90), 1)
    d = ImageDraw.Draw(img)
    font = pil_font(lang, px)
    d.text((12, 20), text, fill=0, font=font)
    box = tuple(int(v) for v in d.textbbox((12, 20), text, font=font))
    bits = np.packbits(np.array(img, dtype=np.uint8), axis=1).tobytes()  # sample 0 = paint
    doc = pymupdf.open()
    page = doc.new_page(width=400, height=300)
    xref = doc.get_new_xref()
    doc.update_object(xref, "<< /Type /XObject /Subtype /Image /Width 240 /Height 90 /ImageMask true "
                            "/BitsPerComponent 1 >>")
    doc.update_stream(xref, bits)
    doc.xref_set_key(page.xref, "Resources", f"<< /XObject << /ImMask {xref} 0 R >> >>")
    cx = doc.get_new_xref()
    doc.update_object(cx, "<< >>")
    doc.update_stream(cx, f"q 0 0 0.5 rg {rect.width} 0 0 {rect.height} {rect.x0} {300 - rect.y1} cm /ImMask Do Q".encode())
    doc.xref_set_key(page.xref, "Contents", f"{cx} 0 R")
    doc.save(str(path))
    doc.close()
    return xref, box


def test_render_after_layout_save_renumbers_xrefs(zh_segments, sample_pdf_zh, rapid, tmp_path, caplog):
    """The pipeline extracts from the source PDF, lays text out, saves with garbage=4 (xrefs are
    renumbered) and only then replaces the images: the segments must still find their images."""
    doc, segs = zh_segments
    doc = doc.model_copy(deep=True)
    doc.segments = [s.model_copy(deep=True) for s in segs]
    for s in doc.segments:
        if "斜边" in s.source_text:
            s.translated_text = "hypotenuse c"
        elif "正方形" in s.source_text:
            s.translated_text = "small square"
    laid_out = tmp_path / "laid_out.pdf"
    with pymupdf.open(str(sample_pdf_zh)) as pdf:
        for page in pdf:
            for block in page.get_text("blocks")[:3]:
                page.add_redact_annot(pymupdf.Rect(block[:4]))
            page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
            page.insert_htmlbox(pymupdf.Rect(60, 50, 500, 90), "<p>translated heading</p>")
        pdf.save(str(laid_out), garbage=4, deflate=True)
    with pymupdf.open(str(laid_out)) as pdf:
        new_xrefs = {page.number: page_image_info(pdf, page.number)["xref"] for page in pdf}
    old_xrefs = {s.page: s.image.xref for s in doc.segments}
    assert new_xrefs != old_xrefs, "the scenario needs renumbered xrefs"

    pdf = pymupdf.open(str(laid_out))
    with caplog.at_level(logging.INFO, logger="mathtrans.images"):
        assert render_image_segments(pdf, doc) == 2
    assert any("renumbered" in r.message for r in caplog.records)
    out = tmp_path / "renumbered_out.pdf"
    pdf.save(str(out), garbage=3)
    pdf.close()
    with pymupdf.open(str(out)) as pdf2:
        assert "translated heading" in pdf2[0].get_text()
        for page_no, expected, gone in [(0, "hypotenuse", "斜边"), (1, "small square", "小正方形")]:
            info = page_image_info(pdf2, page_no)
            assert info["bbox"] == page_image_info(pymupdf.open(str(sample_pdf_zh)), page_no)["bbox"]
            texts = " ".join(r.text for r in rapid.recognize(load_image(pdf2, info["xref"]).flattened()))
            assert expected in texts and gone not in texts
    for s in doc.segments:
        if s.translated_text:
            assert s.render is not None and not s.render.overflow and s.render.scale > 0.8
            assert s.image.bbox.contains(s.render.bbox, tol=1.0)


def test_rgba_transparent_background_is_ocrd(tmp_path, rapid):
    """The colour stored under transparent pixels is black here: OCR must see the flattened image."""
    img, box = draw_label_image((320, 120), "斜边 c", "zh", (30, 30), 40, fill=(0, 0, 0), background=(0, 0, 0, 0),
                                mode="RGBA")
    path = tmp_path / "rgba_ocr.pdf"
    pdf_with_image(path, img, pymupdf.Rect(40, 40, 360, 160))
    doc = make_doc(path, Lang.ZH, Lang.EN)
    with pymupdf.open(str(path)) as pdf:
        loaded = load_image(pdf, page_image_info(pdf, 0)["xref"])
    assert loaded.rgb[5, 5].tolist() == [0, 0, 0] and loaded.flattened()[5, 5].tolist() == [255, 255, 255]
    assert rapid.recognize(loaded.rgb) == []  # raw pixels: black on black, nothing to read
    segs = extract_image_segments(path, doc, rapid)
    assert any("斜边" in s.source_text for s in segs)
    seen: list[np.ndarray] = []

    class Spy:
        name = "spy"

        def recognize(self, image_rgb, hint_langs=None):
            seen.append(image_rgb.copy())
            return []

    extract_image_segments(path, doc, Spy())
    assert len(seen) == 1 and seen[0][5, 5].tolist() == [255, 255, 255]


def test_stencil_mask_image_round_trip(tmp_path, rapid):
    path = tmp_path / "stencil.pdf"
    rect = pymupdf.Rect(60, 60, 300, 150)
    xref, box = stencil_mask_pdf(path, "斜边 c", "zh", 36, rect)
    with pymupdf.open(str(path)) as pdf:
        loaded = load_image(pdf, xref)
        assert loaded.is_mask and loaded.alpha is not None
        assert loaded.alpha.max() == 255 and loaded.alpha[2, 2] == 0  # ink opaque, background transparent
        assert loaded.rgb[2, 2].tolist() == [255, 255, 255]
        painted = loaded.alpha > 0
        assert loaded.rgb[painted].max() == 0  # ink is black
    doc = make_doc(path, Lang.ZH, Lang.EN)
    doc.segments = extract_image_segments(path, doc, rapid)
    seg = next(s for s in doc.segments if "斜边" in s.source_text)
    assert seg.translate and seg.image.xref == xref
    seg.translated_text = "hypotenuse c"
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1
    out = tmp_path / "stencil_out.pdf"
    pdf.save(str(out), garbage=3)
    pdf.close()
    with pymupdf.open(str(out)) as pdf2:
        info = page_image_info(pdf2, 0)
        assert info["bbox"] == tuple(rect) and (info["width"], info["height"]) == (240, 90)
        after = load_image(pdf2, info["xref"])
        pix = pdf2[0].get_pixmap(dpi=72)
    assert after.alpha is not None
    x0, y0, x1, y1 = box
    assert after.alpha[2, 2] == 0 and after.alpha[85, 230] == 0  # background still transparent
    assert (after.alpha[y0:y1, x0:x1] == 0).sum() > 50 and (after.alpha[y0:y1, x0:x1] > 200).sum() > 50
    texts = " ".join(r.text for r in rapid.recognize(after.flattened()))
    assert "hypotenuse" in texts and "斜边" not in texts
    page = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    assert tuple(page[65, 65][:3]) == (255, 255, 255)  # no opaque box: the page shows through
    assert (page[int(rect.y0):int(rect.y1), int(rect.x0):int(rect.x1), :3].min(axis=2) < 80).sum() > 50  # new glyphs


def test_unchanged_translation_leaves_image_untouched(tmp_path):
    img, box = draw_label_image((300, 100), "Figure 1", "en", (20, 30), 32)
    path = tmp_path / "same.pdf"
    rect = pymupdf.Rect(0, 0, 300, 100)
    xref = pdf_with_image(path, img, rect)
    seg = image_segment("p0_i%d_0" % xref, 0, xref, BBox.from_rect(rect), (300, 100), box, "Figure 1", " Figure 1 ",
                        Lang.EN)
    doc = make_doc(path, Lang.EN, Lang.ES)
    doc.segments = [seg]
    pdf = pymupdf.open(str(path))
    before = page_image_info(pdf, 0)["digest"]
    assert render_image_segments(pdf, doc) == 0
    assert page_image_info(pdf, 0)["digest"] == before
    pdf.close()
    assert seg.render is not None and seg.render.scale == 1.0 and not seg.render.overflow
    assert seg.render.notes.startswith("unchanged")


def test_vision_json_edge_cases():
    data = {"items": [
        {"text": None, "box": [0, 0, 100, 100]},  # null text -> skipped
        {"text": "flipped", "box": [900, 500, 100, 100]},  # reversed corners -> sorted
        {"text": "strings", "box": ["0", "0", "500", "250"], "confidence": "7"},  # numeric strings, conf clipped
        {"text": "outside", "box": [-50, 800, 2000, 1500]},  # clamped to the grid
        {"text": "below", "box": [0, 1200, 500, 1500]},  # entirely outside -> no area -> skipped
        {"text": "degenerate", "box": [10, 10, 10, 50]},  # zero width -> skipped
        "not a dict", 42, {"text": "no box"}, {"text": "short box", "box": [1, 2, 3]},
        {"text": "  spaced  ", "box": [0, 0, 1000, 1000], "confidence": -3},
    ]}
    results = parse_vision_ocr_json(data, 200, 100)
    assert [r.text for r in results] == ["flipped", "strings", "outside", "spaced"]
    assert results[0].box == (20, 10, 180, 50)
    assert results[1].box == (0, 0, 100, 25) and results[1].confidence == 1.0
    assert results[2].box == (0, 80, 200, 100)
    assert results[3].confidence == 0.0
    # alternative container keys and a bare list
    assert [r.text for r in parse_vision_ocr_json({"regions": [{"text": "r", "box": [0, 0, 10, 10]}]}, 10, 10)] == ["r"]
    assert parse_vision_ocr_json([], 10, 10) == []
    with pytest.raises(OcrError):
        parse_vision_ocr_json("just a string", 10, 10)
    with pytest.raises(OcrError):
        parse_vision_ocr_json({"items": "nope"}, 10, 10)


def test_ocr_boxes_outside_the_image_are_dropped_or_clamped(sample_pdf_zh):
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    engine = FakeOcr([("斜边 c", (600, 10, 700, 40), 0.9),  # entirely right of the 480 px image
                      ("直角边", (-20, 500, 60, 700), 0.9),  # entirely below
                      ("面积", (440, 330, 520, 420), 0.9),  # partially outside -> clamped
                      ("图", (-5, -5, 5, 5), 0.9)])  # one visible pixel row/column -> kept, clamped
    segs = extract_image_segments(sample_pdf_zh, doc, engine, pages=[0])
    assert [s.source_text for s in segs] == ["面积", "图"]
    assert segs[0].image.pixel_box == (440, 330, 480, 360)
    assert segs[1].image.pixel_box == (0, 0, 5, 5)
    assert [s.id.rsplit("_", 1)[1] for s in segs] == ["2", "3"]  # index = position in the OCR result list
    for s in segs:
        assert s.image.bbox.contains(s.bbox, tol=0.01)
    assert [s.reading_order for s in segs] == [0, 1]


def test_multiline_translation_is_drawn_as_given_lines(tmp_path):
    img, box = draw_label_image((400, 160), "面积 = c²", "zh", (40, 40), 60)
    path = tmp_path / "multiline.pdf"
    rect = pymupdf.Rect(0, 0, 400, 160)
    xref = pdf_with_image(path, img, rect)
    seg = image_segment("p0_i%d_0" % xref, 0, xref, BBox.from_rect(rect), (400, 160), box, "面积 = c²",
                        "Area\n= c²\n", Lang.ZH)
    doc = make_doc(path, Lang.ZH, Lang.EN)
    doc.segments = [seg]
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1
    out = load_image(pdf, xref).rgb
    pdf.close()
    assert seg.render is not None and "2 line(s)" in seg.render.notes and not seg.render.overflow
    x0, y0, x1, y1 = box
    rows_with_ink = np.where((out[y0:y1, x0:x1].min(axis=2) < 100).any(axis=1))[0]
    gaps = np.diff(rows_with_ink)
    assert gaps.max() >= 3  # a blank band separates the two lines
    assert seg.render.font_size < 0.6 * (y1 - y0)  # each line uses about half of the box height


def test_concurrent_extraction_is_thread_safe(sample_pdf_zh, rapid):
    import threading

    results: dict[int, list[str]] = {}
    errors: list[BaseException] = []

    def work(i: int) -> None:
        try:
            doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
            results[i] = [s.source_text for s in extract_image_segments(sample_pdf_zh, doc, rapid)]
        except BaseException as exc:  # noqa: BLE001 - we want to see anything a thread raises
            errors.append(exc)

    threads = [threading.Thread(target=work, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    assert len(results) == 3 and results[0] == results[1] == results[2]
    assert any("斜边" in t for t in results[0])


def test_render_reports_missing_page_and_missing_image(tmp_path):
    img, box = draw_label_image((200, 80), "hypotenuse", "en", (10, 20), 30)
    path = tmp_path / "missing.pdf"
    rect = pymupdf.Rect(0, 0, 200, 80)
    xref = pdf_with_image(path, img, rect)
    doc = make_doc(path, Lang.EN, Lang.ZH)
    wrong_page = image_segment("p7_i%d_0" % xref, 7, xref, BBox.from_rect(rect), (200, 80), box, "hypotenuse", "斜边",
                               Lang.EN)
    wrong_place = image_segment("p0_i999_0", 0, 999, BBox(x0=50, y0=50, x1=150, y1=90), (200, 80), box, "hypotenuse",
                                "斜边", Lang.EN)
    doc.segments = [wrong_page, wrong_place]
    pdf = pymupdf.open(str(path))
    digest = page_image_info(pdf, 0)["digest"]
    assert render_image_segments(pdf, doc) == 0
    assert page_image_info(pdf, 0)["digest"] == digest
    pdf.close()
    for seg in doc.segments:
        assert seg.render is not None and seg.render.overflow and seg.render.notes.startswith("not rendered")
    # a stale xref with the right placement is resolved; a stale xref alone is not trusted
    good = image_segment("p0_i999_1", 0, 999, BBox.from_rect(rect), (200, 80), box, "hypotenuse", "斜边", Lang.EN)
    doc.segments = [good]
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1
    pdf.close()
    assert good.render is not None and not good.render.overflow


def test_rotated_placement_maps_boxes_through_the_transform(tmp_path, rapid):
    img, box = draw_label_image((300, 100), "斜边 c", "zh", (40, 30), 40, fill=(200, 30, 30))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    path = tmp_path / "rotated.pdf"
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=500)
    rect = pymupdf.Rect(100, 50, 200, 350)  # 100 x 300: the 300 x 100 image rotated by 90 degrees
    page.insert_image(rect, stream=buf.getvalue(), rotate=90)
    pdf.save(str(path))
    pdf.close()
    doc = make_doc(path, Lang.ZH, Lang.EN)
    doc.segments = extract_image_segments(path, doc, rapid)
    seg = next(s for s in doc.segments if "斜边" in s.source_text)
    assert seg.image.bbox == BBox.from_rect(rect)
    assert seg.image.bbox.contains(seg.bbox, tol=0.5)
    assert seg.bbox.height > seg.bbox.width  # a horizontal label becomes vertical on the page
    px_box = seg.image.pixel_box
    assert px_box[1] <= box[1] + 4 and px_box[3] >= box[3] - 4  # OCR box encloses the glyphs
    assert seg.style.size == pytest.approx(0.85 * (px_box[3] - px_box[1]) * (rect.width / 100), abs=0.1)
    seg.translated_text = "hypotenuse c"
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1
    out = tmp_path / "rotated_out.pdf"
    pdf.save(str(out))
    pdf.close()
    assert seg.render is not None and seg.image.bbox.contains(seg.render.bbox, tol=0.5)
    assert seg.render.bbox.height > seg.render.bbox.width
    with pymupdf.open(str(out)) as pdf2:
        info = page_image_info(pdf2, 0)
        assert info["bbox"] == tuple(rect) and (info["width"], info["height"]) == (300, 100)
        texts = " ".join(r.text for r in rapid.recognize(load_image(pdf2, info["xref"]).rgb))
    assert "hypotenuse" in texts


def test_pdf_without_images_and_empty_page_filter(tmp_path):
    path = tmp_path / "noimg.pdf"
    pdf = pymupdf.open()
    pdf.new_page().insert_text((50, 50), "only text")
    pdf.save(str(path))
    pdf.close()
    doc = make_doc(path, Lang.EN, Lang.ZH)
    engine = FakeOcr([("x", (0, 0, 10, 10), 1.0)])
    assert extract_image_segments(path, doc, engine) == []
    assert engine.calls == 0
    with pymupdf.open(str(path)) as opened:  # an already open document is accepted and left open
        assert extract_image_segments(opened, doc, engine) == []
        assert not opened.is_closed
    assert extract_image_segments(path, doc, engine, pages=[]) == []
    assert render_image_segments(pymupdf.open(str(path)), doc) == 0


def test_growth_never_overlaps_neighbouring_labels(tmp_path):
    """A long translation grows into free background but stops before the next label."""
    img = Image.new("RGB", (420, 100), "white")
    d = ImageDraw.Draw(img)
    font = pil_font("zh", 34)
    d.text((20, 30), "斜边", fill=(0, 0, 0), font=font)
    left_box = tuple(int(v) for v in d.textbbox((20, 30), "斜边", font=font))
    d.text((120, 30), "B", fill=(0, 0, 0), font=font)
    right_box = tuple(int(v) for v in d.textbbox((120, 30), "B", font=font))
    path = tmp_path / "neighbours.pdf"
    rect = pymupdf.Rect(0, 0, 420, 100)
    xref = pdf_with_image(path, img, rect)
    label = image_segment("p0_i%d_0" % xref, 0, xref, BBox.from_rect(rect), (420, 100), left_box, "斜边",
                          "hypotenuse of the triangle", Lang.ZH)
    letter = image_segment("p0_i%d_1" % xref, 0, xref, BBox.from_rect(rect), (420, 100), right_box, "B", None, Lang.ZH)
    assert letter.translate is False
    doc = make_doc(path, Lang.ZH, Lang.EN)
    doc.segments = [label, letter]
    pdf = pymupdf.open(str(path))
    assert render_image_segments(pdf, doc) == 1
    out = load_image(pdf, xref).rgb
    pdf.close()
    original = np.array(img)
    rx0, ry0, rx1, ry1 = right_box
    assert np.array_equal(out[ry0:ry1, rx0 - 2:rx1 + 2], original[ry0:ry1, rx0 - 2:rx1 + 2])  # "B" untouched
    assert label.render is not None and "grown" in label.render.notes
    drawn = label.render.bbox
    assert drawn.x1 <= rx0 - 1  # the text ends before the neighbour
    assert drawn.x0 >= 0 and drawn.x0 < left_box[0]  # it did use the free space on the left
    assert (out[left_box[1]:left_box[3], int(drawn.x0):int(drawn.x1)].min(axis=2) < 100).sum() > 100


def test_free_extension_and_two_line_balance():
    from mathtrans.images import LoadedImage, free_extension, split_two_lines

    rgb = np.full((40, 200, 3), 255, dtype=np.uint8)
    rgb[:, 150:152] = 0  # a vertical line to the right
    rgb[10:30, 20:60] = 128  # the "label" region (its content does not matter)
    loaded = LoadedImage(xref=1, rgb=rgb)
    bg = np.array([255, 255, 255], dtype=np.uint8)
    left, right = free_extension(loaded, (20, 10, 60, 30), bg, [], 500)
    assert (left, right) == (20 - 2, 150 - 60 - 2)
    left, right = free_extension(loaded, (20, 10, 60, 30), bg, [(100, 0, 110, 40)], 500)
    assert right == 100 - 60 - 2
    assert free_extension(loaded, (20, 10, 60, 30), bg, [], 10) == (8, 8)
    assert free_extension(loaded, (20, 10, 60, 30), bg, [(0, 35, 200, 40)], 500) == (18, 88)  # no row overlap
    alpha = np.zeros((40, 200), dtype=np.uint8)
    alpha[:, :100] = 255
    assert free_extension(LoadedImage(xref=1, rgb=rgb, alpha=alpha), (20, 10, 60, 30), bg, [], 500) == (18, 38)
    font = pil_font("en", 20)
    assert split_two_lines("hypotenuse c", Lang.EN, font) is None  # "c" alone is not a line
    assert split_two_lines("small square label", Lang.EN, font) in (["small square", "label"], ["small", "square label"])
    assert split_two_lines("小正方形", Lang.ZH, pil_font("zh", 20)) == ["小正", "方形"]
    assert split_two_lines("c", Lang.EN, font) is None


# --------------------------------------------------------------------------- #
# regressions: ja/ko text misread by RapidOCR must never be painted as garbage
# --------------------------------------------------------------------------- #


class FakeRapid(FakeOcr):
    """Canned results from an engine that calls itself ``rapid`` (what ``auto`` picks offline)."""

    name = "rapid"


@pytest.fixture(scope="module")
def sample_pdf_ko(samples_dir) -> Path:
    return make_sample_pdf(samples_dir / "sample_ko.pdf", "ko")


def test_korean_han_only_ocr_lines_are_unreliable():
    # RapidOCR's zh/en models read the labels of the Korean sample figure as '二 1-1' (그림 1-1),
    # '臣C' (빗변 c) and '豇=c2' (넓이 = c²): Han characters but no hangul at all
    for text in ("臣C", "二 1-1", "豇=c2", "小正方形"):
        protected, _frags, translate, reason = classify_ocr_text(text, Lang.KO)
        assert (translate, reason) == (False, UNRELIABLE_OCR_KO), text
        assert protected  # still protected so the segment JSON stays complete
    # genuine Korean, Latin-only labels and a mixed line are translated as before
    for text in ("빗변 c", "그림 1-1", "넓이 = c²", "Area = c²", "작은 정사각형", "한자 漢字"):
        assert classify_ocr_text(text, Lang.KO)[2:] == (True, ""), text
    # kanji-only labels are legitimate Japanese; Chinese is unaffected; the string form of the language works too
    assert classify_ocr_text("斜辺 c", Lang.JA)[2:] == (True, "")
    assert classify_ocr_text("小正方形", Lang.JA)[2:] == (True, "")
    assert classify_ocr_text("斜边 c", Lang.ZH)[2:] == (True, "")
    assert classify_ocr_text("臣C", "ko")[2:] == (False, UNRELIABLE_OCR_KO)
    assert UNRELIABLE_OCR_KO.startswith(qa_checks.UNRELIABLE_OCR_PREFIX)


def test_misread_korean_label_is_left_untouched_and_qa_warns(sample_pdf_ko, tmp_path, offline_settings):
    """Pipeline-level: a 'rapid' engine that reads '빗변 c' as '臣C' must not erase the label and
    paint a translation of the garbage; the pixels stay as they are and the QA report says so."""
    with pymupdf.open(str(sample_pdf_ko)) as pdf:
        before = load_image(pdf, page_image_info(pdf, 0)["xref"]).rgb
    engine = FakeRapid([("臣C", (250, 150, 330, 180), 0.7)])
    opts = PipelineOptions(target_lang=Lang.ZH, source_lang=Lang.KO, translator="mock", llm_review=False)
    res = run_pipeline(sample_pdf_ko, tmp_path, opts, settings=offline_settings, translator=MockTranslator(),
                       ocr_engine=engine)
    assert res.status == "completed", res.error
    assert res.stats.ocr_engine == "rapid" and engine.calls == 2 and res.stats.image_segments == 2
    segs = json.loads((tmp_path / "segments.json").read_text(encoding="utf-8"))
    assert segs["ocr_low_trust"] is True and segs["ocr_failures"] == []
    image_segs = [s for s in segs["segments"] if s["kind"] == "image_text"]
    assert len(image_segs) == 2
    for s in image_segs:
        assert s["source_text"] == "臣C" and s["translate"] is False and s["translated_text"] is None
        assert s["skip_reason"] == UNRELIABLE_OCR_KO and s["render"] is None
    with pymupdf.open(res.output_pdf) as out:
        after = load_image(out, page_image_info(out, 0)["xref"]).rgb
    assert np.array_equal(after, before)  # nothing was erased or drawn
    issues = [i for i in res.qa_report.final_issues if i.check == "image_text"]
    assert len(issues) == 2 and all(i.severity == "warning" and not i.fixable for i in issues)
    assert all("臣C" in i.message and "left untouched" in i.message and "--ocr-engine claude" in i.message
               for i in issues)
    assert {i.segment_id for i in issues} == {s["id"] for s in image_segs}
    assert res.qa_report.passed and "unreliable OCR" in (tmp_path / "qa_report.md").read_text(encoding="utf-8")


def test_low_trust_rapid_ocr_warns_once_and_is_reported(rapid, monkeypatch, caplog):
    monkeypatch.setattr(RapidOcrEngine, "_low_trust_warned", False)
    image = np.full((80, 200, 3), 255, dtype=np.uint8)
    with caplog.at_level(logging.WARNING, logger="mathtrans.ocr"):
        rapid.recognize(image, hint_langs=[Lang.ZH])
        rapid.recognize(image, hint_langs=[Lang.EN])
        assert not [r for r in caplog.records if "only partially" in r.message]
        rapid.recognize(image, hint_langs=[Lang.KO])
        rapid.recognize(image, hint_langs=["ja"])
        RapidOcrEngine().recognize(image, hint_langs=[Lang.KO])
    warned = [r for r in caplog.records if "only partially" in r.message]
    assert len(warned) == 1 and "Korean" in warned[0].message and "--ocr-engine claude" in warned[0].message
    assert ocr_low_trust(rapid, Lang.KO) and ocr_low_trust(rapid, "ja") and ocr_low_trust(RapidOcrEngine(), Lang.JA)
    assert not ocr_low_trust(rapid, Lang.ZH) and not ocr_low_trust(rapid, None)
    assert not ocr_low_trust(NullOcrEngine(), Lang.KO) and not ocr_low_trust(None, Lang.KO)
    assert not ocr_low_trust(ClaudeVisionOcrEngine(client=object(), settings=get_settings()), Lang.KO)


def test_auto_engine_prefers_claude_vision_for_ja_ko_with_api_key(offline_settings, monkeypatch):
    # offline, ja/ko still get RapidOCR (there is nothing better) - the pipeline then flags low trust
    assert isinstance(get_ocr_engine("auto", offline_settings, source_lang=Lang.KO), RapidOcrEngine)
    assert isinstance(get_ocr_engine("auto", offline_settings, source_lang=Lang.JA), RapidOcrEngine)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    reset_settings()
    try:
        keyed = get_settings()
        assert keyed.has_api_key
        assert isinstance(get_ocr_engine("auto", keyed, source_lang=Lang.KO), ClaudeVisionOcrEngine)
        assert isinstance(get_ocr_engine("auto", keyed, source_lang="ja"), ClaudeVisionOcrEngine)
        for lang in (Lang.ZH, Lang.EN, Lang.PT, Lang.ES, None):
            assert isinstance(get_ocr_engine("auto", keyed, source_lang=lang), RapidOcrEngine), lang
        # an explicit choice always wins
        assert isinstance(get_ocr_engine("rapid", keyed, source_lang=Lang.KO), RapidOcrEngine)
        assert isinstance(get_ocr_engine("none", keyed, source_lang=Lang.KO), NullOcrEngine)
    finally:
        reset_settings()


def test_pipeline_auto_picks_vision_ocr_for_korean_with_api_key(sample_pdf_ko, sample_pdf_zh, tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    settings = Settings(_env_file=None, ANTHROPIC_API_KEY="sk-ant-test", translator="mock", ocr_engine="auto",
                        data_dir=tmp_path / "data")
    assert settings.has_api_key
    hints: list = []
    monkeypatch.setattr(ClaudeVisionOcrEngine, "recognize",
                        lambda self, image_rgb, hint_langs=None: hints.append(hint_langs) or [])
    opts = PipelineOptions(target_lang=Lang.ZH, translator="mock", llm_review=False, require_qa_pass=False)
    res = run_pipeline(sample_pdf_ko, tmp_path / "ko", opts, settings=settings, translator=MockTranslator())
    assert res.status == "completed", res.error
    assert res.stats.ocr_engine == "claude" and res.stats.source_lang == "ko"
    assert hints == [[Lang.KO], [Lang.KO]]  # one request per image, with the language hint
    segs = json.loads((tmp_path / "ko" / "segments.json").read_text(encoding="utf-8"))
    assert segs["ocr_low_trust"] is False
    # a Chinese source keeps the offline engine even with an API key
    hints.clear()
    opts_en = PipelineOptions(target_lang=Lang.EN, translator="mock", llm_review=False, require_qa_pass=False)
    res = run_pipeline(sample_pdf_zh, tmp_path / "zh", opts_en, settings=settings, translator=MockTranslator())
    assert res.status == "completed", res.error
    assert res.stats.ocr_engine == "rapid" and hints == [] and res.stats.image_segments > 0


def test_image_text_check_reports_ocr_failures_low_trust_and_unreliable_lines(sample_pdf_zh):
    doc = make_doc(sample_pdf_zh, Lang.KO, Lang.EN)
    engine = FakeOcr([("빗변 c", (250, 150, 330, 180), 0.9), ("臣C", (10, 10, 60, 30), 0.7)])
    doc.segments = extract_image_segments(sample_pdf_zh, doc, engine, pages=[0])
    good, bad = doc.segments
    assert good.translate and not bad.translate and bad.skip_reason == UNRELIABLE_OCR_KO
    good.translated_text = "hypotenuse c"
    good.render = RenderInfo(font_size=9, scale=0.9)
    doc.ocr_failures = ["page 2 image xref 79: Claude vision OCR hit the Anthropic rate limit (429)"]
    doc.ocr_low_trust = True
    issues = qa_checks.image_text(doc, PipelineOptions(target_lang=Lang.EN), [])
    assert all(i.check == "image_text" and not i.fixable for i in issues)
    failure = [i for i in issues if "OCR failed" in i.message]
    assert len(failure) == 1 and failure[0].severity == "warning"  # one image was still recognised
    assert "1 of 2 image(s)" in failure[0].message and "429" in failure[0].message
    assert failure[0].details["ocr_failures"] == doc.ocr_failures and failure[0].segment_id is None
    low = [i for i in issues if i.details.get("ocr_low_trust")]
    assert [i.segment_id for i in low] == [good.id] and low[0].severity == "warning"
    assert "Korean" in low[0].message and "preview" in low[0].message
    unreliable = [i for i in issues if i.details.get("unreliable_ocr")]
    assert [i.segment_id for i in unreliable] == [bad.id] and "'臣C'" in unreliable[0].message
    assert len(issues) == 3
    # nothing recognised at all -> the failure blocks the export (unfixable error)
    doc.segments, doc.ocr_low_trust = [], False
    issues = qa_checks.image_text(doc, PipelineOptions(target_lang=Lang.EN), [])
    assert len(issues) == 1 and issues[0].severity == "error" and "1 of 1 image(s)" in issues[0].message
    doc.ocr_failures = []
    assert qa_checks.image_text(doc, PipelineOptions(target_lang=Lang.EN), []) == []


# --------------------------------------------------------------------------- #
# regressions: oversized images (memory budget)
# --------------------------------------------------------------------------- #


def bomb_pdf(path: Path, width: int, height: int) -> int:
    """A tiny PDF whose single page shows a huge, flate-compressed constant-colour RGB image."""
    import zlib

    compressor = zlib.compressobj(1)
    row_block = b"\x00" * (3 * width * 64)
    parts = [compressor.compress(row_block) for _ in range(height // 64)]
    parts.append(compressor.compress(b"\x00" * (3 * width * (height % 64))))
    parts.append(compressor.flush())
    doc = pymupdf.open()
    page = doc.new_page(width=400, height=400)
    xref = doc.get_new_xref()
    doc.update_object(xref, f"<< /Type /XObject /Subtype /Image /Width {width} /Height {height} /ColorSpace /DeviceRGB "
                            f"/BitsPerComponent 8 /Filter /FlateDecode >>")
    doc.update_stream(xref, b"".join(parts), compress=0)
    doc.xref_set_key(page.xref, "Resources", f"<< /XObject << /Im0 {xref} 0 R >> >>")
    cx = doc.get_new_xref()
    doc.update_object(cx, "<< >>")
    doc.update_stream(cx, b"q 400 0 0 400 0 0 cm /Im0 Do Q")
    doc.xref_set_key(page.xref, "Contents", f"{cx} 0 R")
    doc.save(str(path))
    doc.close()
    return xref


class NeverCalled:
    name = "spy"

    def recognize(self, image_rgb, hint_langs=None):
        raise AssertionError("an oversized image must not reach the OCR engine")


def test_oversized_images_are_skipped_before_decoding(sample_pdf_zh, tmp_path, caplog):
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    with caplog.at_level(logging.WARNING, logger="mathtrans.images"):
        assert extract_image_segments(sample_pdf_zh, doc, NeverCalled(), max_image_px=100) == []
    skipped = [r for r in caplog.records if "oversized" in r.message]
    assert len(skipped) == 2 and "480x360" in skipped[0].message and "MATHTRANS_MAX_IMAGE_MEGAPIXELS" in skipped[0].message
    # exactly at the budget the image is still processed; 0 disables the guard
    counting = FakeOcr([])
    extract_image_segments(sample_pdf_zh, doc, counting, max_image_px=480 * 360)
    assert counting.calls == 2
    extract_image_segments(sample_pdf_zh, doc, counting, max_image_px=0)
    assert counting.calls == 4
    # the default budget lets textbook figures and 600 dpi A4 scans through but stops a decompression bomb:
    # an 838 KB PDF declaring an 8000x8000 (64 MP, ~192 MB decoded) image is skipped without decoding it
    assert 4960 * 7016 < MAX_IMAGE_PX < 8000 * 8000
    path = tmp_path / "bomb.pdf"
    xref = bomb_pdf(path, 8000, 8000)
    assert path.stat().st_size < 2_000_000
    bomb_doc = make_doc(path, Lang.ZH, Lang.EN)
    caplog.clear()
    with caplog.at_level(logging.WARNING, logger="mathtrans.images"):
        assert extract_image_segments(path, bomb_doc, NeverCalled()) == []
    assert any(f"xref {xref} (8000x8000 px" in r.message for r in caplog.records)
    assert Settings(_env_file=None).max_image_megapixels * 1_000_000 == MAX_IMAGE_PX


def test_rapid_engine_downscales_huge_images_and_maps_boxes_back(monkeypatch):
    seen: list[tuple[int, int]] = []

    def fake_engine(bgr):
        seen.append(bgr.shape[:2])
        return [[[[10, 10], [50, 10], [50, 20], [10, 20]], "x", 0.9]], 0.0

    monkeypatch.setattr(RapidOcrEngine, "_engine", classmethod(lambda cls: fake_engine))
    engine = RapidOcrEngine(downscale_max_side=100)
    results = engine.recognize(np.full((300, 600, 3), 255, dtype=np.uint8))
    assert seen == [(50, 100)]  # recognised at 1/6 of the size ...
    assert results[0].polygon == [[60.0, 60.0], [300.0, 60.0], [300.0, 120.0], [60.0, 120.0]]  # ... boxes in full-res pixels
    assert results[0].box == (60, 60, 300, 120) and results[0].text == "x" and results[0].confidence == 0.9
    # small images are still upscaled 2x, medium ones passed through untouched
    seen.clear()
    engine.recognize(np.full((100, 100, 3), 255, dtype=np.uint8))
    RapidOcrEngine(upscale_max_side=10, downscale_max_side=100).recognize(np.full((80, 90, 3), 255, dtype=np.uint8))
    assert seen == [(200, 200), (80, 90)]
    assert DOWNSCALE_MAX_SIDE == 4000 and RapidOcrEngine().downscale_max_side == DOWNSCALE_MAX_SIDE


# --------------------------------------------------------------------------- #
# regressions: Claude vision OCR API errors (typed, most specific first)
# --------------------------------------------------------------------------- #

_API_REQUEST = httpx.Request("POST", "https://api.anthropic.com/v1/messages")


def api_error(cls, status: int, message: str = "api error"):
    return cls(message, response=httpx.Response(status, request=_API_REQUEST), body=None)


class RaisingClient:
    """``client.messages.create`` raises ``exc`` every time and counts the attempts."""

    def __init__(self, exc: BaseException):
        self.exc = exc
        self.calls = 0
        self.messages = self

    def create(self, **kwargs):
        self.calls += 1
        raise self.exc


def vision_engine(exc: BaseException, settings) -> tuple[ClaudeVisionOcrEngine, RaisingClient]:
    client = RaisingClient(exc)
    return ClaudeVisionOcrEngine(client=client, settings=settings), client


def test_vision_ocr_credential_errors_abort_after_the_first_image(sample_pdf_zh, offline_settings):
    image = np.full((50, 50, 3), 255, dtype=np.uint8)
    for cls, status, hint in ((anthropic.AuthenticationError, 401, "ANTHROPIC_API_KEY"),
                              (anthropic.PermissionDeniedError, 403, "--model"),
                              (anthropic.NotFoundError, 404, "MATHTRANS_CLAUDE_MODEL")):
        engine, client = vision_engine(api_error(cls, status), offline_settings)
        with pytest.raises(OcrUnavailableError, match=str(status)) as info:
            engine.recognize(image)
        assert isinstance(info.value, OcrError) and info.value.__cause__ is client.exc
        assert hint in str(info.value) and "MATHTRANS_OCR_ENGINE=rapid|none" in str(info.value)
    # a missing credential / unknown request parameter surfaces as a bare TypeError from the SDK
    engine, _client = vision_engine(TypeError("unexpected keyword argument 'output_config'"), offline_settings)
    with pytest.raises(OcrUnavailableError, match="anthropic >= 1.0"):
        engine.recognize(image)
    # extraction stops at the first image instead of sending one failing request per image
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    engine, client = vision_engine(api_error(anthropic.AuthenticationError, 401, "invalid x-api-key"), offline_settings)
    failures: list[str] = []
    with pytest.raises(OcrUnavailableError, match="invalid x-api-key"):
        extract_image_segments(sample_pdf_zh, doc, engine, failures=failures)
    assert client.calls == 1 and failures == []


def test_vision_ocr_transient_errors_skip_the_image_and_are_recorded(sample_pdf_zh, offline_settings, caplog):
    image = np.full((50, 50, 3), 255, dtype=np.uint8)
    for exc, hint in ((api_error(anthropic.RateLimitError, 429, "slow down"), "automatic retries"),
                      (api_error(anthropic.InternalServerError, 500, "boom"), "retry later"),
                      (api_error(anthropic.BadRequestError, 400, "bad image"), "check the request / image"),
                      (anthropic.APIConnectionError(request=_API_REQUEST), "network/proxy/timeout"),
                      (RuntimeError("network down"), "network down")):
        engine, client = vision_engine(exc, offline_settings)
        with pytest.raises(OcrError, match=re.escape(hint)) as info:
            engine.recognize(image)
        assert not isinstance(info.value, OcrUnavailableError) and client.calls == 1
    doc = make_doc(sample_pdf_zh, Lang.ZH, Lang.EN)
    engine, client = vision_engine(api_error(anthropic.RateLimitError, 429, "slow down"), offline_settings)
    failures: list[str] = []
    with caplog.at_level(logging.WARNING, logger="mathtrans.images"):
        assert extract_image_segments(sample_pdf_zh, doc, engine, failures=failures) == []
    assert client.calls == 2  # one request per image, none of them aborts the stage
    assert len(failures) == 2 and all("429" in f and "slow down" in f for f in failures)
    assert failures[0].startswith("page 1 image xref ") and failures[1].startswith("page 2 image xref ")
    assert sum("OCR failed on image xref" in r.message for r in caplog.records) == 2
    assert extract_image_segments(sample_pdf_zh, doc, engine) == []  # without a list the failures are only logged


def test_pipeline_surfaces_vision_ocr_failures(sample_pdf_zh, tmp_path, offline_settings):
    opts = PipelineOptions(target_lang=Lang.EN, source_lang=Lang.ZH, translator="mock", ocr_engine="claude",
                           llm_review=False)
    # credentials / model problems stop the job with the reason (no silently untranslated figures)
    engine, client = vision_engine(api_error(anthropic.AuthenticationError, 401, "invalid x-api-key"), offline_settings)
    res = run_pipeline(sample_pdf_zh, tmp_path / "auth", opts, settings=offline_settings, translator=MockTranslator(),
                       ocr_engine=engine)
    assert res.status == "error" and client.calls == 1
    assert "401" in res.error and "ANTHROPIC_API_KEY" in res.error and "MATHTRANS_OCR_ENGINE=rapid|none" in res.error
    assert "401" in (tmp_path / "auth" / "error.txt").read_text(encoding="utf-8")
    # per-image failures are counted, listed in the QA report and block the export when nothing was read
    engine, client = vision_engine(api_error(anthropic.RateLimitError, 429, "slow down"), offline_settings)
    res = run_pipeline(sample_pdf_zh, tmp_path / "rate", opts, settings=offline_settings, translator=MockTranslator(),
                       ocr_engine=engine)
    assert res.status == "qa_failed" and client.calls == 2
    assert res.stats.ocr_failures == 2 and res.stats.image_segments == 0 and res.stats.ocr_engine == "claude"
    issue = next(i for i in res.qa_report.final_issues if i.check == "image_text")
    assert issue.severity == "error" and not issue.fixable and "OCR failed on 2 of 2 image(s)" in issue.message
    assert len(issue.details["ocr_failures"]) == 2 and "429" in issue.message
    segs = json.loads((tmp_path / "rate" / "segments.json").read_text(encoding="utf-8"))
    assert len(segs["ocr_failures"]) == 2 and (tmp_path / "rate" / "output.pdf").is_file()
    assert "OCR failed" in (tmp_path / "rate" / "qa_report.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# superscripts flattened by OCR (c² read as c2) are restored from the glyph geometry
# --------------------------------------------------------------------------- #


def superscript_canvas(base: str, trailing: str, *, base_px: int = 40, trailing_px: int = 22, raise_px: int = 12,
                       lang: str = "en", background=(255, 255, 255),
                       fill=(0, 0, 0)) -> tuple[LoadedImage, tuple[int, int, int, int]]:
    """A 300x60 canvas with ``base`` followed by ``trailing`` drawn ``raise_px`` higher at ``trailing_px``
    (``raise_px=0`` with the same size = flat text); returns the image and an OCR-like box (2 px padding)."""
    img = Image.new("RGB", (300, 60), background)
    draw = ImageDraw.Draw(img)
    base_font, trailing_font = pil_font(lang, base_px), pil_font(lang, trailing_px)
    draw.text((10, 48), base, font=base_font, fill=fill, anchor="ls")
    draw.text((10 + base_font.getlength(base) + 2, 48 - raise_px), trailing, font=trailing_font, fill=fill, anchor="ls")
    arr = np.array(img)
    ys, xs = np.where(np.abs(arr.astype(int) - np.array(background)).max(axis=2) > 24)
    box = (int(xs.min()) - 2, int(ys.min()) - 2, int(xs.max()) + 3, int(ys.max()) + 3)
    return LoadedImage(xref=1, rgb=arr), box


def test_restore_superscripts_raised_trailing_digit():
    white = np.array([255, 255, 255], dtype=np.uint8)
    # the sample's figure label: a small "2" sitting above the baseline of "面积 = c"
    loaded, box = superscript_canvas("面积 = c", "2", lang="zh")
    assert restore_superscripts(loaded, box, "面积= c2", white) == "面积= c²"
    assert restore_superscripts(loaded, box, " 面积= c2 ", white) == "面积= c²"
    # two raised digits, a raised digit after an x-height letter at 60 % size, light text on a dark background
    loaded, box = superscript_canvas("x", "10", trailing_px=24, raise_px=14)
    assert restore_superscripts(loaded, box, "x10", white) == "x¹⁰"
    loaded, box = superscript_canvas("x", "2", trailing_px=24, raise_px=14)
    assert restore_superscripts(loaded, box, "x2", white) == "x²"
    loaded, box = superscript_canvas("c", "2", background=(20, 30, 40), fill=(255, 255, 255))
    assert restore_superscripts(loaded, box, "c2", np.array([20, 30, 40], dtype=np.uint8)) == "c²"
    # flat digits (same size on the same baseline) are left alone, also after a descender or in a caption
    for base, text in (("面积 = c", "面积= c2"), ("g", "g2"), ("Figure 1", "Figure 12"), ("y", "y2")):
        loaded, box = superscript_canvas(base, text[-1], trailing_px=40, raise_px=0, lang="zh" if "面" in base else "en")
        assert restore_superscripts(loaded, box, text, white) == text, text
    # a subscript (lowered digit) is not a superscript; nothing to do without trailing digits
    loaded, box = superscript_canvas("a", "1", trailing_px=24, raise_px=-10)
    assert restore_superscripts(loaded, box, "a1", white) == "a1"
    loaded, box = superscript_canvas("Figure 1-1", "", trailing_px=24)
    assert restore_superscripts(loaded, box, "Figure 1-1", white) == "Figure 1-1"
    # too coarse to judge: a tiny box; invisible: a fully transparent trailing glyph
    loaded, box = superscript_canvas("c", "2", base_px=9, trailing_px=6, raise_px=3)
    assert box[3] - box[1] < 12 and restore_superscripts(loaded, box, "c2", white) == "c2"
    loaded, box = superscript_canvas("c", "2")
    alpha = np.full(loaded.rgb.shape[:2], 255, dtype=np.uint8)
    alpha[:, int(10 + pil_font("en", 40).getlength("c")):] = 0
    assert restore_superscripts(LoadedImage(xref=1, rgb=loaded.rgb, alpha=alpha), box, "c2", white) == "c2"


def test_extracted_superscript_is_protected_and_painted_raised(tmp_path):
    loaded, box = superscript_canvas("Area = c", "2")
    pdf_path = tmp_path / "sup.pdf"
    pdf_with_image(pdf_path, Image.fromarray(loaded.rgb), pymupdf.Rect(50, 50, 350, 110))
    doc = make_doc(pdf_path, Lang.EN, Lang.ZH)
    doc.segments = extract_image_segments(pdf_path, doc, FakeOcr([("Area = c2", box, 0.95)]))
    assert len(doc.segments) == 1
    seg = doc.segments[0]
    assert seg.source_text == "Area = c²" and seg.translate
    assert seg.protected_text == "Area ⟦0⟧" and seg.protected == ["= c²"]  # the exponent is protected, not re-typed
    seg.translated_text = "面积 = c²"
    pdf = pymupdf.open(str(pdf_path))
    assert render_image_segments(pdf, doc) == 1
    out = tmp_path / "out.pdf"
    pdf.save(str(out))
    pdf.close()
    assert seg.render is not None and not seg.render.overflow and seg.render.font_size > 0
    with pymupdf.open(str(out)) as pdf2:
        painted = load_image(pdf2, page_image_info(pdf2, 0)["xref"])
    # the repainted label ends in a small raised glyph again (the geometry reads it back as a superscript)
    wide = (0, box[1] - 2, painted.width, box[3] + 2)
    bg = estimate_background(painted.rgb, wide)[0]
    assert restore_superscripts(painted, wide, "面积 = c2", bg) == "面积 = c²"


def test_pipeline_restores_superscript_in_the_sample_figure(sample_pdf_zh, rapid, tmp_path, offline_settings):
    opts = PipelineOptions(target_lang=Lang.EN, source_lang=Lang.ZH, translator="mock", llm_review=False)
    res = run_pipeline(sample_pdf_zh, tmp_path, opts, settings=offline_settings, translator=MockTranslator(),
                       ocr_engine=rapid)
    assert res.status == "completed" and res.qa_report is not None and res.qa_report.passed
    segs = json.loads((tmp_path / "segments.json").read_text(encoding="utf-8"))["segments"]
    label = next(s for s in segs if s["kind"] == "image_text" and "面积" in s["source_text"])
    assert label["source_text"].endswith("c²") and "c2" not in label["source_text"]
    assert label["translated_text"] == "Area = c²"
    assert label["render"]["overflow"] is False and label["render"]["font_size"] > 0


# --------------------------------------------------------------------------- #
# replace_image leaves no second copy of the image in the page resources
# --------------------------------------------------------------------------- #


def image_objects(pdf: pymupdf.Document) -> list[int]:
    return [x for x in range(1, pdf.xref_length()) if pdf.xref_is_image(x)]


def test_replaced_images_are_stored_once(zh_segments, sample_pdf_zh, tmp_path):
    doc, segs = zh_segments
    doc = doc.model_copy(deep=True)
    doc.segments = [s.model_copy(deep=True) for s in segs]
    for s in doc.segments:
        if "斜边" in s.source_text:
            s.translated_text = "hypotenuse c"
        elif "面积" in s.source_text:
            s.translated_text = "Area = c²"
    pdf = pymupdf.open(str(sample_pdf_zh))
    assert render_image_segments(pdf, doc) == 2
    out = tmp_path / "out.pdf"
    pdf.save(str(out), garbage=3)  # what pipeline._atomic_save uses
    pdf.close()
    with pymupdf.open(str(sample_pdf_zh)) as src, pymupdf.open(str(out)) as pdf2:
        assert len(image_objects(pdf2)) == len(image_objects(src)) == 2
        for page_index in (0, 1):
            images = pdf2[page_index].get_images(full=True)
            assert len(images) == len(src[page_index].get_images(full=True)) == 1
            content = b"".join(pdf2.xref_stream(c) for c in pdf2[page_index].get_contents())
            for im in images:  # every image object of the page is drawn by its content stream
                assert re.search(rb"/" + re.escape(im[7].encode()) + rb"\s+Do", content), im[7]
            info = page_image_info(pdf2, page_index)
            assert info["xref"] == images[0][0] and info["digest"] != page_image_info(src, page_index)["digest"]


def test_replace_image_cleans_up_indirect_and_inherited_resources(tmp_path):
    img, _box = draw_label_image((200, 80), "c", "en", (20, 20), 30)
    pdf_path = tmp_path / "img.pdf"
    pdf_with_image(pdf_path, img, pymupdf.Rect(20, 20, 220, 100))
    buf = io.BytesIO()
    Image.new("RGB", (200, 80), (0, 128, 0)).save(buf, format="PNG")
    green = buf.getvalue()

    def xobject_indirect(pdf: pymupdf.Document, page: pymupdf.Page) -> None:
        kind, value = pdf.xref_get_key(page.xref, "Resources")
        owner, key = (int(value.split()[0]), "XObject") if kind == "xref" else (page.xref, "Resources/XObject")
        new = pdf.get_new_xref()
        pdf.update_object(new, pdf.xref_get_key(owner, key)[1])
        pdf.xref_set_key(owner, key, f"{new} 0 R")
        assert pdf.xref_get_key(page.xref, "Resources/XObject")[0] == "xref"

    def resources_inherited(pdf: pymupdf.Document, page: pymupdf.Page) -> None:
        kind, value = pdf.xref_get_key(page.xref, "Resources")
        if kind == "dict":  # make it an indirect object first so it can move to the /Pages node
            new = pdf.get_new_xref()
            pdf.update_object(new, value)
            value = f"{new} 0 R"
        parent = int(pdf.xref_get_key(page.xref, "Parent")[1].split()[0])
        pdf.xref_set_key(parent, "Resources", value)
        pdf.xref_set_key(page.xref, "Resources", "null")
        assert pdf.xref_get_key(page.xref, "Resources")[0] == "null"

    for n, layout in enumerate((None, xobject_indirect, resources_inherited)):
        pdf = pymupdf.open(str(pdf_path))
        page = pdf[0]
        if layout is not None:
            layout(pdf, page)
        before = page.get_images(full=True)
        assert len(before) == 1
        replace_image(page, before[0][0], green)
        assert [im[7] for im in page.get_images(full=True)] == [before[0][7]]
        out = tmp_path / f"out{n}.pdf"
        pdf.save(str(out), garbage=3)
        pdf.close()
        with pymupdf.open(str(out)) as pdf2:
            assert len(image_objects(pdf2)) == 1
            info = page_image_info(pdf2, 0)
            assert tuple(load_image(pdf2, info["xref"]).rgb[40, 100]) == (0, 128, 0)  # the new pixels are drawn
            assert pdf2[0].get_pixmap(dpi=36).width > 0


def test_tally_marks_are_kept_as_symbols():
    from mathtrans.images import classify_ocr_text
    from mathtrans.models import Lang

    assert classify_ocr_text("正正", Lang.ZH)[2:] == (False, "tally marks")
    assert classify_ocr_text("正 正 正", Lang.ZH)[2:] == (False, "tally marks")
    assert classify_ocr_text("正方形", Lang.ZH)[2:] == (True, "")


def test_ocr_noise_rules():
    from mathtrans.images import classify_ocr_text
    from mathtrans.models import Lang

    assert classify_ocr_text("118十104", Lang.ZH)[2:] == (False, "pure number / formula")
    assert classify_ocr_text("7一3=4", Lang.ZH)[2:] == (False, "pure number / formula")
    assert classify_ocr_text("一共十个", Lang.ZH)[2:] == (True, "")


def test_merge_ocr_passes_keeps_only_new_regions():
    from mathtrans.models import OcrResult
    from mathtrans.ocr import merge_ocr_passes

    def r(text, x0, y0, x1, y1):
        return OcrResult(text=text, polygon=[[x0, y0], [x1, y0], [x1, y1], [x0, y1]], confidence=0.9)

    first = [r("数一数", 10, 10, 110, 40), r("8", 200, 10, 220, 40)]
    second = [r("数一数。", 8, 9, 118, 41),      # same line, slightly larger box: duplicate
              r("比一比", 10, 60, 110, 90),      # new line below: kept
              r("8", 199, 12, 221, 38),          # same label: duplicate
              r("个", 112, 12, 130, 38)]          # touches the first box only slightly: kept
    extra = merge_ocr_passes(first, second)
    assert [e.text for e in extra] == ["比一比", "个"]
    assert merge_ocr_passes([], second[:2]) == second[:2] and merge_ocr_passes(first, []) == []


def test_rapid_second_pass_adds_missed_lines(monkeypatch):
    from mathtrans.ocr import RapidOcrEngine

    calls = []

    def fake_engine(bgr):
        inverted = bgr.mean() < 128  # the second pass runs on the colour-inverted page
        tile = bgr.shape[:2] != (1000, 1400)
        calls.append(("tile" if tile else "inv" if inverted else "plain", bgr.shape[1], bgr.shape[0]))
        box_a = [[10, 10], [110, 10], [110, 40], [10, 40]]
        if tile:
            if len([c for c in calls if c[0] == "tile"]) == 1:  # the top-left tile (upscaled 1.5x) finds a label
                return [([[150, 150], [270, 150], [270, 195], [150, 195]], "七八", 0.97)], 0.1
            return [], 0.1
        if not inverted:
            return [(box_a, "数一数", 0.95)], 0.1
        return [(box_a, "数一数", 0.9),  # same line: dropped as a duplicate
                ([[10, 60], [110, 60], [110, 90], [10, 90]], "比一比", 0.93),  # missed by the first pass: added
                ([[10, 120], [110, 120], [110, 150], [10, 150]], "junk", 0.5)], 0.1  # low confidence: dropped

    monkeypatch.setattr(RapidOcrEngine, "_engine", classmethod(lambda cls: fake_engine))
    engine = RapidOcrEngine(second_pass_min_side=1200)
    page = np.full((1000, 1400, 3), 255, dtype=np.uint8)
    out = engine.recognize(page)
    assert calls[:2] == [("plain", 1400, 1000), ("inv", 1400, 1000)]
    assert [c[0] for c in calls[2:]] == ["tile"] * 12        # a 3 x 4 grid of overlapping tiles
    assert [o.text for o in out] == ["数一数", "比一比", "七八"]
    assert out[1].polygon[0] == [10.0, 60.0] and out[1].polygon[2] == [110.0, 90.0]
    assert out[2].polygon[0] == [100.0, 100.0]              # tile pixels / 1.5 + tile origin (0, 0)
    # small figures (below the page-size threshold) get no second pass
    calls.clear()
    engine.recognize(np.full((300, 1100, 3), 255, dtype=np.uint8))
    assert len(calls) == 1
    # disabled explicitly
    calls.clear()
    RapidOcrEngine(second_pass=False).recognize(page)
    assert len(calls) == 1


# --------------------------------------------------------------------------- #
# lower-grade OCR rules: answer boxes, plain numbers, unit labels, unreadable symbols
# --------------------------------------------------------------------------- #


def test_fill_in_templates_stay_in_the_picture():
    from mathtrans.images import FILL_IN_TEMPLATE, is_fill_in_template

    for text in ["O-O=O (只)", "□-□=□（只）", "□OO=0（个）", "OOO=0", "DOO=O ()", "□○□=□", "□+3=□", "△○"]:
        assert is_fill_in_template(text), text
        assert classify_ocr_text(text, Lang.ZH)[2:] == (False, FILL_IN_TEMPLATE)
    for text in ["100=100", "10-0=10", "5+3=8", "0", "O", "OO", "8-□=5", "北乐O0O-O(T)", "共有多少个？"]:
        assert not is_fill_in_template(text), text


def test_superscripts_are_never_restored_on_plain_numbers():
    from mathtrans.images import _TRAILING_DIGITS_RE

    # restore_superscripts bails out before looking at pixels when the base is a digit
    loaded = types.SimpleNamespace(rgb=np.zeros((10, 10, 3), np.uint8), alpha=None)
    for text in ["26", "小于50", "2个50", "42颗"]:
        assert restore_superscripts(loaded, (0, 0, 10, 10), text, np.array([255, 255, 255])) == text
    assert _TRAILING_DIGITS_RE.search("c2") and _TRAILING_DIGITS_RE.search("m2")


def test_digit_look_alikes_in_number_tokens():
    from mathtrans.images import normalize_ocr_digits as norm

    assert norm("h5") == "15" and norm("I5") == "15" and norm("5O") == "50" and norm("2O个") == "20个"
    assert norm("第h5页") == "第15页"
    for text in ["l1", "直线l1", "Hello", "5h", "50cm", "h", "BOX 2"]:
        assert norm(text) == text, text


def test_unit_labels_unreadable_symbols_and_pictogram_gaps():
    from mathtrans.images import INLINE_PICTOGRAMS, UNREADABLE_SYMBOL

    assert classify_ocr_text("（只）", Lang.ZH)[2] is True
    for text in ["（画“”）", '画""', "想一想，羊可能有多少只？（画“”)"]:
        assert classify_ocr_text(text, Lang.ZH)[2:] == (False, UNREADABLE_SYMBOL), text
    for text in ["用表示人，用表示椅子", "比少个", "比多几个", "图中有个有个有个有_个○", "在的面"]:
        assert classify_ocr_text(text, Lang.ZH)[2:] == (False, INLINE_PICTOGRAMS), text
    for text in ["淘气比笑笑多3个。", "比一比，谁多？", "比赛开始了。", "比较大小", "谁比谁多？", "长方形的面积",
                 "有几只小鸭？", "画“✓”", "比20小。", "比6大8。", "比99多1。", "比18多得多。", "鸡、鸭、鹅相比", "比90本"]:
        assert classify_ocr_text(text, Lang.ZH)[2] is True, text


def test_place_value_header_is_split_from_its_digit():
    from mathtrans.images import split_place_value

    label, box = split_place_value("十位5", (100, 10, 200, 40))
    assert label == "十位" and box[0] == 100 and 160 < box[2] < 180 and box[1:4:2] == (10, 40)
    label, box = split_place_value("7个位", (100, 10, 200, 40))
    assert label == "个位" and box[2] == 200 and 115 < box[0] < 135
    assert split_place_value("十位", (0, 0, 10, 10)) is None
    assert split_place_value("十位上是5", (0, 0, 10, 10)) is None


def test_quoted_marks_are_read_from_the_pixels():
    from PIL import Image, ImageDraw
    from mathtrans.fonts import pil_font
    from mathtrans.images import detect_quoted_marks, fill_empty_quotes

    img = Image.new("RGB", (560, 70), (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = pil_font("zh", 40)
    d.text((10, 12), "多的画“", fill=(20, 20, 20), font=font)
    d.line([(150, 38), (162, 52), (184, 18)], fill=(20, 20, 20), width=3)          # a tick between the quotes
    d.text((190, 12), "”，少的画“", fill=(20, 20, 20), font=font)
    d.ellipse([(392, 20), (424, 52)], outline=(20, 20, 20), width=3)               # a circle between the quotes
    d.text((430, 12), "”", fill=(20, 20, 20), font=font)
    rgb = np.array(img)
    marks = detect_quoted_marks(rgb, (0, 5, 560, 65))
    assert marks == ["✓", "○"]
    assert fill_empty_quotes("多的画“”，少的画“”", marks) == "多的画“✓”，少的画“○”"
    assert fill_empty_quotes("多的画“”", marks) == "多的画“”"           # counts differ: unchanged
    assert fill_empty_quotes("画“√”，画“”", ["✓", "○"]) == "画“√”，画“○”"  # read marks stay, empty ones are filled


def test_inline_pictures_become_anchors_in_the_text():
    from PIL import Image, ImageDraw
    from mathtrans.fonts import pil_font
    from mathtrans.images import detect_anchors
    from mathtrans.models import ANCHOR_RE

    img = Image.new("RGB", (520, 60), (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = pil_font("zh", 40)
    d.text((10, 8), "第", fill=(20, 20, 20), font=font)
    d.rounded_rectangle([(62, 8), (104, 52)], radius=8, outline=(230, 40, 40), width=4)   # red answer box
    d.text((112, 8), "节，第几只是", fill=(20, 20, 20), font=font)
    d.ellipse([(370, 12), (420, 50)], fill=(60, 170, 70), outline=(30, 90, 40), width=2)  # a green picture
    d.text((428, 8), "？", fill=(20, 20, 20), font=font)
    rgb = np.array(img)
    never_text = lambda crop: False
    text, anchors = detect_anchors(rgb, (0, 4, 520, 58), "第节，第几只是？", "x", never_text)
    keys = ANCHOR_RE.findall(text)
    assert keys == ["x.0", "x.1"] and set(anchors) == {"x.0", "x.1"}
    plain = ANCHOR_RE.sub("#", text)
    assert plain == "第#节，第几只是#？"
    assert 55 <= anchors["x.0"][0] <= 66 and anchors["x.0"][2] >= 100   # pixel box of the answer box
    # a candidate the recogniser reads as text (a red word) is no picture; without a recogniser nothing happens
    assert detect_anchors(rgb, (0, 4, 520, 58), "第节，第几只是？", "x", lambda crop: True) == ("第节，第几只是？", {})
    assert detect_anchors(rgb, (0, 4, 520, 58), "第节，第几只是？", "x", None) == ("第节，第几只是？", {})
    # formulas and answer-box templates are never anchored
    assert detect_anchors(rgb, (0, 4, 520, 58), "□+3=8", "x", never_text)[1] == {}


def test_anchor_markers_survive_protection_and_render_as_images():
    from mathtrans.layout import anchor_name, segment_html
    from mathtrans.models import BBox, TextSegment, anchor_marker
    from mathtrans.protect import protect_text, restore_placeholders

    text = "用" + anchor_marker("9.1.0") + "表示人"
    protected, fragments = protect_text(text, "zh")
    assert protected == "用⟦0⟧表示人" and fragments == [anchor_marker("9.1.0")]
    translated = restore_placeholders("Use ⟦0⟧ for people", fragments)
    seg = TextSegment(id="s", page=0, bbox=BBox(x0=0, y0=0, x1=100, y1=10), source_text=text,
                      anchors={"9.1.0": [9, 10, 10, 50, 30]})
    html = segment_html(seg, translated)
    assert f'src="{anchor_name("9.1.0")}"' in html and "Use " in html and " for people" in html
    assert "" not in html and "width:2.50em" in html   # aspect 40 x 20 at 1.25 em high



def test_unit_labels_after_answer_boxes_are_split_off_and_dropped():
    from mathtrans.images import _split_template_units
    from mathtrans.models import OcrResult

    def r(text):
        return OcrResult(text=text, polygon=[[0, 0], [200, 0], [200, 30], [0, 30]], confidence=0.9)

    out = _split_template_units([r("O-O=O (只)"), r("13-9=□（个）"), r("10÷5=2（元）"), r("还剩几个？")])
    assert [o.text for o in out] == ["O-O=O ", "(只)", "13-9=□", "（个）", "10÷5=2（元）", "还剩几个？"]
    assert out[1].polygon[0][0] > out[0].polygon[1][0]                 # the unit part sits right of the cut
    # a standalone unit label is dropped (erased on scanned pages, never set as "(pieces)")
    assert classify_ocr_text("（只）", Lang.ZH)[2] is True             # plain text classification ...
