"""Tests for mathtrans.layout (redaction + re-insertion of translated text, previews).

The segments are built here directly from ``page.get_text("dict")`` blocks of
the sample PDFs (the real extractor lives in ``mathtrans.extract`` and is not
used), with hand-written translations.
"""
from __future__ import annotations

import os
import shutil
import unicodedata
from pathlib import Path
from typing import Optional

import pymupdf
import pytest
from PIL import Image

from mathtrans import fonts as fonts_module
from mathtrans.languages import is_cjk
from mathtrans.layout import (REDACT_SHRINK, _PageSpace, html_rotation, page_css, render_document,
                              render_page_previews, segment_html)
from mathtrans.models import (BBox, Lang, PageInfo, SegmentKind, SegmentStyle, TextSegment,
                              TranslatedDocument)
from mathtrans.samples import sample_texts

PAGE_KEYS = ["title", "section", "para1", "caption", "example", "solution", "theorem",
             "exercises", "ex1", "ex2", "ex3", "think", "footer"]
ROLES = {"title": "heading", "section": "heading", "exercises": "heading", "caption": "caption",
         "ex1": "list", "ex2": "list", "ex3": "list"}
ALIGNS = {"caption": "center", "footer": "center"}

# ~2.5x the capacity of its box (225 x 29 pt at 11 px): exercises shrink-to-fit
LONG_EX3 = ("3. Decide whether a triangle whose three side lengths are 7, 24 and 25 is a right "
            "triangle, and explain carefully how the converse of the Pythagorean theorem "
            "justifies your answer in every case.")
# absurdly long for a 28 x 12 pt page-number box: exercises the overflow path
ABSURD_FOOTER = "Page 2 " + ("of the exercise booklet for the first chapter on the Pythagorean "
                             "theorem and its many applications in geometry, ") * 8
NOTO_DIRS = [
    os.environ.get("MATHTRANS_TEST_FONTS_DIR", ""),
    str(Path(__file__).resolve().parent.parent / "fonts"),
    "/tmp/claude-0/-home-user-math-material-translation/1e147c18-6fbd-5cf2-9102-87b84ab13c2e/scratchpad/fonts",
]
NO_LIGATURES = pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_LIGATURES


def _norm(text: str) -> str:
    """NFKC-normalised text without any whitespace (line wrapping differs between
    the original and the re-rendered text, and CJK lines join without spaces)."""
    return "".join(unicodedata.normalize("NFKC", text).split())


def page_text(page: pymupdf.Page, clip: Optional[pymupdf.Rect] = None) -> str:
    """Page text with ligatures expanded and whitespace removed (compare with ``_norm``)."""
    return _norm(page.get_text("text", clip=clip, flags=NO_LIGATURES))


def sample_translations(src: Lang, tgt: Lang, overrides: Optional[dict[str, str]] = None) -> dict[str, str]:
    """{key: (source prefix, translation)} for the 13 page texts of the sample textbook."""
    s, t = sample_texts(src.value), sample_texts(tgt.value)
    out = {k: (s[k][:10], t[k]) for k in PAGE_KEYS}
    for k, v in (overrides or {}).items():
        out[k] = (out[k][0], v)
    return out


def build_document(pdf_path: Path, src: Lang, tgt: Lang, translations: dict[str, tuple[str, str]],
                   rotation_from_dir: bool = False) -> TranslatedDocument:
    """One TextSegment per text block of ``pdf_path``; blocks whose text contains a
    source prefix of ``translations`` get that translation, others stay untranslated."""
    pdf = pymupdf.open(str(pdf_path))
    doc = TranslatedDocument(source_path=str(pdf_path), source_lang=src, target_lang=tgt)
    order = 0
    for pno, page in enumerate(pdf):
        doc.pages.append(PageInfo(index=pno, width=page.rect.width, height=page.rect.height,
                                  image_bboxes=[BBox.from_rect(i["bbox"]) for i in page.get_image_info()]))
        for n, block in enumerate(page.get_text("dict", flags=NO_LIGATURES)["blocks"]):
            if block["type"] != 0:
                continue
            lines = ["".join(s["text"] for s in line["spans"]).strip() for line in block["lines"]]
            text = ("" if is_cjk(src) else " ").join(lines).strip()
            spans = [s for line in block["lines"] for s in line["spans"]]
            dom = max(spans, key=lambda s: len(s["text"]))
            style = SegmentStyle(font=dom["font"], size=dom["size"], color=dom["color"],
                                 bold=bool(dom["flags"] & 16), italic=bool(dom["flags"] & 2),
                                 serif=bool(dom["flags"] & 4), line_height=1.25)
            if rotation_from_dir:  # the extractor's convention: the insert_htmlbox ``rotate`` value
                dx, dy = block["lines"][0]["dir"]
                style.rotation = {(1, 0): 0, (0, -1): 90, (-1, 0): 180, (0, 1): 270}[(round(dx), round(dy))]
            seg = TextSegment(id=f"p{pno}_b{n}", page=pno, bbox=BBox.from_rect(block["bbox"]),
                              source_text=text, style=style, reading_order=order)
            order += 1
            for key, (prefix, translation) in translations.items():
                if text.startswith(prefix):
                    seg.translated_text = translation
                    seg.style.role = ROLES.get(key, "body")
                    seg.style.align = ALIGNS.get(key, "left")
                    break
            if seg.translated_text is None:
                seg.translate = False
                seg.skip_reason = "not translated in this test"
            doc.segments.append(seg)
    pdf.close()
    return doc


def segment_for(doc: TranslatedDocument, key: str, translations: dict[str, tuple[str, str]]) -> TextSegment:
    prefix = translations[key][0]
    return next(s for s in doc.segments if prefix in s.source_text)


@pytest.fixture(scope="module")
def zh_en(sample_pdf_zh, tmp_path_factory):
    """Render the Chinese sample into English once for the read-only assertions."""
    translations = sample_translations(Lang.ZH, Lang.EN, {"ex3": LONG_EX3, "footer": ABSURD_FOOTER})
    doc = build_document(sample_pdf_zh, Lang.ZH, Lang.EN, translations)
    out = tmp_path_factory.mktemp("layout") / "zh_en.pdf"
    infos = render_document(sample_pdf_zh, doc, out, min_font_scale=0.55)
    return doc, out, infos, translations


# --------------------------------------------------------------------------- #
# insert_htmlbox contract and HTML generation
# --------------------------------------------------------------------------- #


def test_insert_htmlbox_contract():
    """The empirical behaviour layout.py branches on (documented in its module docstring)."""
    css = "* {font-family: sans-serif;} p {margin:0}"
    rect = pymupdf.Rect(60, 100, 300, 140)
    sentence = "The sum of the squares of the two legs equals the square of the hypotenuse. "

    def attempt(text, scale_low):
        doc = pymupdf.open()
        page = doc.new_page()
        spare, scale = page.insert_htmlbox(rect, f'<p style="font-size:11px">{text}</p>', css=css,
                                           scale_low=scale_low)
        return spare, scale, len(page.get_text().strip())

    spare, scale, n = attempt("Hello world", 0.55)
    assert spare > 0 and scale == 1.0 and n == len("Hello world")
    spare, scale, n = attempt(sentence * 2, 0.55)  # fits after shrinking
    assert spare >= 0 and 0.55 <= scale < 1.0 and n > 0
    spare, scale, n = attempt(sentence * 8, 0.55)  # does not fit: nothing written, scale == scale_low
    assert spare == -1 and scale == 0.55 and n == 0
    spare, scale, n = attempt(sentence * 8, 1.0)
    assert spare == -1 and scale == 1.0 and n == 0
    spare, scale, n = attempt(sentence * 8, 0)  # unlimited shrinking always fits
    assert spare >= 0 and 0 < scale < 0.55 and n > 0


def test_segment_html_escapes_and_styles():
    seg = TextSegment(id="s", page=0, bbox=BBox(x0=0, y0=0, x1=10, y1=10), source_text="x",
                      style=SegmentStyle(size=12.5, color=0x1F3A93, bold=True, italic=True, align="center",
                                         line_height=1.4))
    html = segment_html(seg, "a < b & c\nsecond line")
    assert html.startswith('<p style="') and html.endswith("</p>")
    assert "a &lt; b &amp; c<br>second line" in html
    for prop in ("font-size:12.50px", "color:#1f3a93", "font-weight:bold", "font-style:italic",
                 "text-align:center", "line-height:1.40"):
        assert prop in html
    assert "line-height:1.10" in segment_html(seg, "x", line_height=1.1)
    plain = segment_html(TextSegment(id="t", page=0, bbox=seg.bbox, source_text="x"), "x")
    assert "font-weight:normal" in plain and "font-style:normal" in plain and "text-align:left" in plain


def test_page_css_family_and_fonts_dir():
    css, _archive = page_css(Lang.ZH)  # wqy-zenhei is a .ttc => built-in fonts
    assert css.endswith("* {font-family: sans-serif;} p {margin:0}")
    css_en, archive_en = page_css(Lang.EN)  # DejaVuSans.ttf is found on this system
    assert "@font-face" in css_en and archive_en is not None
    assert css_en.endswith("* {font-family: mtfont;} p {margin:0}")
    assert "DejaVuSans-Bold.ttf" in css_en and "font-weight: bold" in css_en


def test_html_rotation_mapping():
    """style.rotation is the insert_htmlbox ``rotate`` value (extractor convention) and
    passes through unchanged; vertical text without a rotation runs down the page."""
    for rotation in (0, 90, 180, 270):
        assert html_rotation(SegmentStyle(rotation=rotation)) == rotation
    assert html_rotation(SegmentStyle(rotation=0, is_vertical=True)) == 270
    assert html_rotation(SegmentStyle(rotation=90, is_vertical=True)) == 90
    assert html_rotation(SegmentStyle(rotation=-90)) == 270
    assert html_rotation(SegmentStyle(rotation=450)) == 90


# --------------------------------------------------------------------------- #
# render_document
# --------------------------------------------------------------------------- #


def test_render_replaces_text_and_preserves_graphics(sample_pdf_zh, zh_en):
    doc, out, infos, translations = zh_en
    src = pymupdf.open(str(sample_pdf_zh))
    res = pymupdf.open(str(out))
    assert res.page_count == src.page_count
    for pno in range(src.page_count):
        assert res[pno].rect == src[pno].rect
        assert [i["bbox"] for i in res[pno].get_image_info()] == [i["bbox"] for i in src[pno].get_image_info()]
        assert len(res[pno].get_drawings()) == len(src[pno].get_drawings())
        assert len(res[pno].get_drawings()) == (2 if pno == 0 else 0)
    translated = [s for s in doc.segments if s.translated_text]
    assert len(infos) == len(translated) == 13
    for seg in translated:
        text = page_text(res[seg.page])
        assert _norm(seg.source_text) not in text
        assert seg.render is not None and seg.render.bbox is not None and seg.render.font_size > 0
        if not seg.render.overflow:
            assert _norm(seg.translated_text) in text
    # the yellow example box kept its fill and the frame survived
    fills = [d for d in res[0].get_drawings() if d.get("fill")]
    assert len(fills) == 1 and fills[0]["rect"] == pymupdf.Rect(60, 445, 535, 530)


def test_render_keeps_untranslated_text_and_fonts_embedded(zh_en):
    _doc, out, _infos, _translations = zh_en
    res = pymupdf.open(str(out))
    assert _norm("a² + b² = c²") in page_text(res[0])  # translate=False formula untouched
    assert page_text(res[0], clip=pymupdf.Rect(280, 785, 320, 810)) == "1"  # page number untouched
    for pno in range(res.page_count):
        names = [f[3] for f in res.get_page_fonts(pno)]
        assert names, "translated text must use embedded fonts"
        assert any("Nimbus" in n or "DejaVu" in n or "Noto" in n for n in names)


def test_render_extends_heading_into_free_space(zh_en):
    doc, _out, _infos, translations = zh_en
    title = segment_for(doc, "title", translations)
    info = title.render
    assert info.scale == 1.0 and not info.overflow and info.font_size == pytest.approx(22.0)
    assert info.bbox.width > 2 * title.bbox.width and info.bbox.x0 == title.bbox.x0
    assert info.bbox.height <= 1.5 * title.bbox.height + 0.01
    assert "extended" in info.notes
    page_info = doc.pages[0]
    others = [s.bbox for s in doc.segments if s.page == 0 and s.id != title.id] + page_info.image_bboxes
    assert all(info.bbox.intersection_area(b) == 0 for b in others)
    assert BBox(x0=0, y0=0, x1=page_info.width, y1=page_info.height).contains(info.bbox)
    # a box right of an image stops short of it (exercise 3 vs the square figure, 2pt gap)
    ex3 = segment_for(doc, "ex3", translations)
    image = doc.pages[1].image_bboxes[0]
    assert ex3.render.bbox.x1 <= image.x0 - 2 + 1e-6 and ex3.render.bbox.x1 > ex3.bbox.x1


def test_render_shrinks_long_translation_to_fit(zh_en):
    doc, out, _infos, translations = zh_en
    ex3 = segment_for(doc, "ex3", translations)
    info = ex3.render
    assert 0.55 <= info.scale < 1.0 and not info.overflow and info.spare_height >= 0
    assert info.font_size == pytest.approx(11.0 * info.scale, abs=0.01)
    assert _norm(LONG_EX3) in page_text(pymupdf.open(str(out))[1])


def test_render_flags_overflow_but_keeps_text_editable(zh_en):
    doc, out, _infos, translations = zh_en
    footer = segment_for(doc, "footer", translations)
    info = footer.render
    assert info.overflow and info.scale < 0.55 and info.spare_height < 0  # missing height estimate
    assert "does not fit" in info.notes
    text = page_text(pymupdf.open(str(out))[1])
    assert _norm("Page 2 of the exercise booklet") in text  # still real, extractable text
    assert _norm("第 2 页") not in text


def test_render_en_to_zh_with_builtin_fonts(sample_pdf_en, tmp_path, monkeypatch):
    monkeypatch.setattr(fonts_module, "find_font_file", lambda *a, **k: None)  # force PyMuPDF built-ins
    translations = sample_translations(Lang.EN, Lang.ZH)
    doc = build_document(sample_pdf_en, Lang.EN, Lang.ZH, translations)
    out = tmp_path / "en_zh.pdf"
    infos = render_document(sample_pdf_en, doc, out)
    assert len(infos) == 13 and not any(i.overflow for i in infos)
    res = pymupdf.open(str(out))
    zh = sample_texts("zh")
    assert _norm(zh["title"]) in page_text(res[0]) and _norm(zh["theorem"]) in page_text(res[0])
    assert _norm(zh["ex2"]) in page_text(res[1]) and "Pythagorean" not in page_text(res[0])
    assert any("Droid" in f[3] for f in res.get_page_fonts(0))


def test_render_zh_to_ja(sample_pdf_zh, tmp_path):
    translations = sample_translations(Lang.ZH, Lang.JA)
    doc = build_document(sample_pdf_zh, Lang.ZH, Lang.JA, translations)
    out = tmp_path / "zh_ja.pdf"
    render_document(sample_pdf_zh, doc, out)
    res = pymupdf.open(str(out))
    ja = sample_texts("ja")
    assert _norm(ja["title"]) in page_text(res[0]) and _norm(ja["think"]) in page_text(res[1])
    assert "勾股定理" not in page_text(res[0])
    assert all(s.render.scale >= 0.55 and not s.render.overflow for s in doc.segments if s.render)


def test_render_with_noto_fonts_dir(sample_pdf_zh, tmp_path):
    fonts_dir = next((d for d in NOTO_DIRS if d and (Path(d) / "NotoSansJP-Regular.ttf").is_file()), None)
    if fonts_dir is None:
        pytest.skip("Noto Sans fonts not available (run scripts/fetch_fonts.py)")
    translations = sample_translations(Lang.ZH, Lang.JA)
    doc = build_document(sample_pdf_zh, Lang.ZH, Lang.JA, translations)
    out = tmp_path / "zh_ja_noto.pdf"
    render_document(sample_pdf_zh, doc, out, fonts_dir=fonts_dir)
    res = pymupdf.open(str(out))
    assert _norm(sample_texts("ja")["example"]) in page_text(res[0])
    assert any("Noto" in f[3] for f in res.get_page_fonts(0))


def test_render_rotated_segment(tmp_path):
    """Rotated segments keep their writing direction: style.rotation follows the
    extractor's convention (90 = running up the page, 270 = running down)."""
    css = "* {font-family: sans-serif;} p {margin:0}"
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=400)
    page.insert_htmlbox(pymupdf.Rect(40, 40, 300, 70), '<p style="font-size:12px">Horizontal label</p>', css=css)
    page.insert_htmlbox(pymupdf.Rect(340, 40, 370, 340), '<p style="font-size:12px">Downward label</p>',
                        css=css, rotate=270)  # text runs down the page: dir (0, 1)
    page.insert_htmlbox(pymupdf.Rect(300, 40, 330, 340), '<p style="font-size:12px">Upward label</p>',
                        css=css, rotate=90)  # text runs up the page: dir (0, -1)
    page.insert_htmlbox(pymupdf.Rect(40, 300, 300, 330), '<p style="font-size:12px">Upside down label</p>',
                        css=css, rotate=180)
    src = tmp_path / "rotated.pdf"
    pdf.save(str(src))
    translations = {"h": ("Horizontal", "Etiqueta horizontal"), "d": ("Downward", "Etiqueta hacia abajo"),
                    "u": ("Upward", "Etiqueta hacia arriba"), "f": ("Upside", "Etiqueta invertida")}
    doc = build_document(src, Lang.EN, Lang.ES, translations, rotation_from_dir=True)
    assert segment_for(doc, "d", translations).style.rotation == 270
    assert segment_for(doc, "u", translations).style.rotation == 90
    assert segment_for(doc, "f", translations).style.rotation == 180
    out = tmp_path / "rotated_es.pdf"
    infos = render_document(src, doc, out)
    assert len(infos) == 4 and not any(i.overflow for i in infos)
    by_dir: dict[tuple, str] = {}
    for b in pymupdf.open(str(out))[0].get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            by_dir[tuple(line["dir"])] = by_dir.get(tuple(line["dir"]), "") + "".join(s["text"] for s in line["spans"])
    assert _norm(by_dir[(0.0, 1.0)]) == _norm("Etiqueta hacia abajo")  # still running down the page
    assert _norm(by_dir[(0.0, -1.0)]) == _norm("Etiqueta hacia arriba")  # still running up
    assert _norm(by_dir[(-1.0, 0.0)]) == _norm("Etiqueta invertida")
    assert _norm(by_dir[(1.0, 0.0)]) == _norm("Etiqueta horizontal")
    for key in ("d", "u"):  # rotated boxes are never grown
        seg = segment_for(doc, key, translations)
        assert seg.render.bbox == seg.bbox


def test_render_pages_subset_and_in_place(sample_pdf_zh, tmp_path):
    src = tmp_path / "work.pdf"
    shutil.copy(sample_pdf_zh, src)
    translations = sample_translations(Lang.ZH, Lang.EN)
    doc = build_document(src, Lang.ZH, Lang.EN, translations)
    infos = render_document(src, doc, src, pages=[1])  # out == src
    assert all(i.bbox is not None for i in infos) and len(infos) == 6
    res = pymupdf.open(str(src))
    assert res.page_count == 2
    assert "勾股定理" in page_text(res[0]) and "Pythagorean" not in page_text(res[0])
    assert _norm("Exercises 1.1") in page_text(res[1]) and "练习" not in page_text(res[1])
    assert all(s.render is None for s in doc.segments if s.page == 0)


def test_render_document_argument_validation(sample_pdf_zh, tmp_path):
    doc = build_document(sample_pdf_zh, Lang.ZH, Lang.EN, sample_translations(Lang.ZH, Lang.EN))
    with pytest.raises(ValueError):
        render_document(sample_pdf_zh, doc, tmp_path / "x.pdf", min_font_scale=0)
    with pytest.raises(ValueError):
        render_document(sample_pdf_zh, doc, tmp_path / "x.pdf", pages=[5])
    assert not (tmp_path / "x.pdf").exists()


def test_redaction_spares_adjacent_untranslated_line(tmp_path):
    """Two one-line segments whose boxes touch: redacting the first (box shrunk by
    0.3pt) must keep the second line's glyphs."""
    assert REDACT_SHRINK == pytest.approx(0.3)
    css = "* {font-family: sans-serif;} p {margin:0}"
    pdf = pymupdf.open()
    page = pdf.new_page(width=300, height=200)
    page.insert_htmlbox(pymupdf.Rect(20, 20, 280, 60),
                        '<p style="font-size:11px;line-height:1.1">first line of text<br>second line of text</p>', css=css)
    src = tmp_path / "adjacent.pdf"
    pdf.save(str(src))
    page = pymupdf.open(str(src))[0]
    lines = [line for b in page.get_text("dict")["blocks"] if b["type"] == 0 for line in b["lines"]]
    assert len(lines) == 2 and lines[0]["bbox"][3] >= lines[1]["bbox"][1] - 0.5  # boxes touch
    doc = TranslatedDocument(source_path=str(src), source_lang=Lang.EN, target_lang=Lang.ES,
                             pages=[PageInfo(index=0, width=300, height=200)])
    for n, line in enumerate(lines):
        text = "".join(sp["text"] for sp in line["spans"])
        doc.segments.append(TextSegment(id=f"p0_l{n}", page=0, bbox=BBox.from_rect(line["bbox"]), source_text=text,
                                        style=SegmentStyle(size=11, line_height=1.1), reading_order=n,
                                        translated_text="primera línea del texto" if n == 0 else None,
                                        translate=n == 0))
    out = tmp_path / "adjacent_es.pdf"
    infos = render_document(src, doc, out)
    assert len(infos) == 1 and not infos[0].overflow
    text = page_text(pymupdf.open(str(out))[0])
    assert _norm("second line of text") in text
    assert _norm("primera línea del texto") in text and _norm("first line") not in text


def test_render_bold_segment_uses_bold_face(tmp_path):
    """A bold segment is set in the bold face declared by page_css (DejaVu Sans Bold here)."""
    css = "* {font-family: sans-serif;} p {margin:0}"
    pdf = pymupdf.open()
    page = pdf.new_page(width=300, height=100)
    page.insert_htmlbox(pymupdf.Rect(20, 20, 280, 50), '<p style="font-size:14px;font-weight:bold">Teorema</p>', css=css)
    src = tmp_path / "bold.pdf"
    pdf.save(str(src))
    translations = {"t": ("Teorema", "Theorem")}
    doc = build_document(src, Lang.ES, Lang.EN, translations)
    seg = segment_for(doc, "t", translations)
    assert seg.style.bold
    out = tmp_path / "bold_en.pdf"
    render_document(src, doc, out)
    spans = [s for b in pymupdf.open(str(out))[0].get_text("dict")["blocks"] for l in b.get("lines", [])
             for s in l["spans"]]
    assert [s["text"] for s in spans] == ["Theorem"]
    assert spans[0]["flags"] & 16 and "Bold" in spans[0]["font"]
    assert spans[0]["size"] == pytest.approx(14.0) and spans[0]["color"] == 0


# --------------------------------------------------------------------------- #
# previews
# --------------------------------------------------------------------------- #


def test_render_page_previews(zh_en, tmp_path):
    _doc, out, _infos, _translations = zh_en
    paths = render_page_previews(out, tmp_path / "previews" / "nested", dpi=110)
    assert [Path(p).name for p in paths] == ["page-001.png", "page-002.png"]
    for p in paths:
        assert Path(p).is_file() and Path(p).stat().st_size > 1000
        with Image.open(p) as im:
            assert im.format == "PNG"
            assert abs(im.width - 595 * 110 / 72) <= 2 and abs(im.height - 842 * 110 / 72) <= 2
    only_second = render_page_previews(pymupdf.open(str(out)), tmp_path / "subset", dpi=40, pages=[1])
    assert [Path(p).name for p in only_second] == ["page-002.png"]
    with Image.open(only_second[0]) as im:
        assert abs(im.width - 595 * 40 / 72) <= 2
    with pytest.raises(ValueError):
        render_page_previews(out, tmp_path / "bad", pages=[2])


# --------------------------------------------------------------------------- #
# adversarial: unusual PDFs, odd segments, unicode, size, concurrency
# --------------------------------------------------------------------------- #

CSS_PLAIN = "* {font-family: sans-serif;} p {margin:0}"


def _one_segment_doc(src: Path, src_lang: Lang, tgt_lang: Lang, translation: str, **style) -> TranslatedDocument:
    """Document with exactly one translated segment: the first text block of page 0."""
    page = pymupdf.open(str(src))[0]
    block = next(b for b in page.get_text("dict", flags=NO_LIGATURES)["blocks"] if b["type"] == 0)
    text = " ".join("".join(s["text"] for s in line["spans"]) for line in block["lines"]).strip()
    doc = TranslatedDocument(source_path=str(src), source_lang=src_lang, target_lang=tgt_lang,
                             pages=[PageInfo(index=0, width=page.rect.width, height=page.rect.height)])
    doc.segments.append(TextSegment(id="p0_b0", page=0, bbox=BBox.from_rect(block["bbox"]), source_text=text,
                                    style=SegmentStyle(size=block["lines"][0]["spans"][0]["size"], **style),
                                    translated_text=translation))
    return doc


def test_render_page_with_rotate_entry(tmp_path):
    """A landscape page displayed with /Rotate 90: text, image and drawing coordinates
    live in the unrotated 400 x 200 space while page.rect is 200 x 400. The text sits
    at x > 200, so clipping against page.rect would wrongly drop it."""
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=200)
    page.insert_htmlbox(pymupdf.Rect(230, 20, 390, 50), '<p style="font-size:14px">Hello rotated page</p>', css=CSS_PLAIN)
    page.insert_image(pymupdf.Rect(20, 100, 100, 180),
                      stream=pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 8, 8), 0).tobytes("png"))
    page.draw_rect(pymupdf.Rect(230, 60, 390, 90), color=(1, 0, 0), width=1)
    page.set_rotation(90)
    src = tmp_path / "rotated_page.pdf"
    pdf.save(str(src))
    src_page = pymupdf.open(str(src))[0]
    assert src_page.rect == pymupdf.Rect(0, 0, 200, 400) and src_page.rotation == 90
    doc = _one_segment_doc(src, Lang.EN, Lang.ES, "Página girada")
    seg = doc.segments[0]
    assert seg.bbox.x0 > 200  # beyond the displayed width: only correct in the unrotated space
    out = tmp_path / "rotated_page_es.pdf"
    infos = render_document(src, doc, out)
    assert len(infos) == 1 and not infos[0].overflow and infos[0].scale == 1.0
    res = pymupdf.open(str(out))[0]
    assert res.rect == src_page.rect and res.rotation == 90
    assert [i["bbox"] for i in res.get_image_info()] == [i["bbox"] for i in src_page.get_image_info()]
    assert [d["rect"] for d in res.get_drawings()] == [d["rect"] for d in src_page.get_drawings()]
    assert "Hello" not in page_text(res) and _norm("Página girada") in page_text(res)
    new_block = next(b for b in res.get_text("dict")["blocks"] if b["type"] == 0)
    assert abs(new_block["bbox"][0] - seg.bbox.x0) < 3 and abs(new_block["bbox"][1] - seg.bbox.y0) < 3
    # the growth limits were computed in the unrotated space: the grown box stays inside it
    assert infos[0].bbox.x1 <= 400 and infos[0].bbox.y1 <= 200
    previews = render_page_previews(out, tmp_path / "prev", dpi=72)
    with Image.open(previews[0]) as im:
        assert (im.width, im.height) == (200, 400)  # displayed orientation


@pytest.mark.parametrize("rotation", [90, 180, 270])
@pytest.mark.parametrize("box", ["cropbox", "mediabox"])
def test_render_rotated_page_with_box_offset(tmp_path, rotation, box):
    """A /Rotate page whose CropBox or MediaBox origin is not (0, 0) (auto-cropped
    landscape scans, imposed PDFs). PyMuPDF's insert_htmlbox ignores the box offset on
    rotated pages and used to put the translation partly off the page (the first letters
    of every line clipped, x0 < 0), while the redaction had already removed the source
    text; the layout must neutralise the rotation while it inserts."""
    pdf = pymupdf.open()
    if box == "cropbox":
        page = pdf.new_page(width=700, height=950)
    else:
        page = pdf.new_page(width=595, height=842)
        pdf.xref_set_key(page.xref, "MediaBox", "[100 200 695 1042]")
        page = pdf[0]
    page.insert_htmlbox(pymupdf.Rect(80, 80, 380, 110), '<p style="font-size:14px">Hello offset page</p>',
                        css=CSS_PLAIN)
    if box == "cropbox":
        page.set_cropbox(pymupdf.Rect(50, 50, 650, 900))
    page.set_rotation(rotation)
    src = tmp_path / f"{box}_{rotation}.pdf"
    pdf.save(str(src))
    src_page = pymupdf.open(str(src))[0]
    assert src_page.rotation == rotation
    if box == "cropbox":
        assert src_page.cropbox == pymupdf.Rect(50, 50, 650, 900)
    else:
        assert src_page.mediabox == pymupdf.Rect(100, 200, 695, 1042)
    doc = _one_segment_doc(src, Lang.EN, Lang.ES, "Página con desplazamiento")
    seg = doc.segments[0]
    assert seg.bbox.x0 > 0 and seg.bbox.y0 > 0
    out = tmp_path / f"{box}_{rotation}_es.pdf"
    infos = render_document(src, doc, out)
    assert len(infos) == 1 and infos[0].scale == 1.0 and not infos[0].overflow
    res = pymupdf.open(str(out))[0]
    assert res.rotation == rotation and res.rect == src_page.rect  # geometry untouched
    assert res.cropbox == src_page.cropbox and res.mediabox == src_page.mediabox
    text = page_text(res)
    assert "Hello" not in text and _norm("Página con desplazamiento") in text
    block = next(b for b in res.get_text("dict")["blocks"] if b["type"] == 0)
    assert block["bbox"][0] >= 0, "translation starts off the page"
    assert abs(block["bbox"][0] - seg.bbox.x0) < 3 and abs(block["bbox"][1] - seg.bbox.y0) < 3
    assert "".join(s["text"] for s in block["lines"][0]["spans"]) == "Página con desplazamiento"


def _link_facts(page: pymupdf.Page) -> list[tuple]:
    """(kind, from-rect, uri / destination page, destination point) of every link."""
    facts = []
    for link in page.get_links():
        to = link.get("to")
        facts.append((link["kind"], tuple(round(v) for v in link["from"]), link.get("uri") or link.get("page"),
                      (round(to.x), round(to.y)) if to is not None else None))
    return sorted(facts, key=str)


def _annot_facts(page: pymupdf.Page) -> list[tuple]:
    return sorted((a.type[1], tuple(round(v) for v in a.rect), a.info.get("content", "")) for a in page.annots())


def _widget_facts(page: pymupdf.Page) -> list[tuple]:
    return sorted((w.field_name, w.field_value, tuple(round(v) for v in w.rect)) for w in page.widgets())


def _html(page: pymupdf.Page, rect: pymupdf.Rect, text: str, size: int = 11) -> None:
    page.insert_htmlbox(rect, f'<p style="font-size:{size}px">{text}</p>', css=CSS_PLAIN)


def test_render_keeps_links_and_annotations(tmp_path):
    """MuPDF's redaction deletes every Link and FreeText annotation whose rectangle meets
    a redaction rectangle - i.e. the hyperlinks sitting on translated text (a clickable
    table of contents, cross references, URLs) and notes overlapping a paragraph. They
    must come out of the layout stage unchanged, also across a checkpoint and whether the
    page keeps its /Annots as a direct or an indirect array; annotations the redaction
    leaves alone (highlight, form field) must not be duplicated."""
    pdf = pymupdf.open()
    pdf.new_page(width=595, height=842)
    pdf.new_page(width=595, height=842)
    toc = pdf[0]
    _html(toc, pymupdf.Rect(60, 50, 535, 90), "目录", size=22)
    _html(toc, pymupdf.Rect(60, 100, 300, 120), "第一章 勾股定理 ............ 2", size=12)
    _html(toc, pymupdf.Rect(60, 130, 300, 150), "第二章 实数 ............ 2", size=12)
    _html(toc, pymupdf.Rect(60, 180, 400, 200), "参考资料见网站：数学学习网")
    _html(toc, pymupdf.Rect(60, 500, 535, 560), "在直角三角形中，两条直角边的平方和等于斜边的平方。")
    toc.insert_image(pymupdf.Rect(60, 250, 360, 450),
                     stream=pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 8, 8), 0).tobytes("png"))
    toc.insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(60, 100, 300, 120), "page": 1,
                     "to": pymupdf.Point(0, 50)})
    toc.insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(60, 130, 300, 150), "page": 1,
                     "to": pymupdf.Point(0, 300)})
    toc.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(60, 180, 400, 200), "uri": "https://example.com/math"})
    toc.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(60, 250, 360, 450), "uri": "https://example.com/image"})
    toc.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(400, 600, 500, 650), "uri": "https://example.com/blank"})
    paragraph = next(b for b in toc.get_text("dict")["blocks"] if b["type"] == 0 and b["bbox"][1] > 490)
    note = toc.add_freetext_annot(pymupdf.Rect(200, paragraph["bbox"][3] - 2, 420, paragraph["bbox"][3] + 38),
                                  "注意：斜边是最长的边。", fontsize=11, fontname="china-s",
                                  text_color=(0.8, 0, 0), fill_color=(1, 1, 0.8))
    note.update()
    toc.add_highlight_annot(pymupdf.Rect(60, 100, 300, 115))
    field = pymupdf.Widget()
    field.field_name, field.field_type, field.field_value = "answer", pymupdf.PDF_WIDGET_TYPE_TEXT, "5"
    field.rect = pymupdf.Rect(320, 130, 530, 150)
    toc.add_widget(field)
    chapter = pdf[1]
    _html(chapter, pymupdf.Rect(60, 50, 535, 90), "第一章 勾股定理", size=22)
    _html(chapter, pymupdf.Rect(60, 100, 200, 120), "返回目录")
    chapter.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(60, 50, 535, 90), "uri": "https://example.com/ch1"})
    chapter.insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(60, 100, 200, 120), "page": 0,
                         "to": pymupdf.Point(0, 0)})
    kind, value = pdf.xref_get_key(chapter.xref, "Annots")  # make page 2 keep its annotations indirectly
    assert kind == "array"
    array_xref = pdf.get_new_xref()
    pdf.update_object(array_xref, value)
    pdf.xref_set_key(chapter.xref, "Annots", f"{array_xref} 0 R")
    src = tmp_path / "linked.pdf"
    pdf.save(str(src), garbage=4, deflate=True)
    pdf.close()

    source = pymupdf.open(str(src))
    assert source.xref_get_key(source[1].xref, "Annots")[0] == "xref"
    expected = [(_link_facts(p), _annot_facts(p), _widget_facts(p), len(p.annot_xrefs())) for p in source]
    assert len(expected[0][0]) == 5 and len(expected[0][1]) == 2 and len(expected[0][2]) == 1
    assert len(expected[1][0]) == 2
    translations = {"title": ("目录", "Contents"), "toc1": ("第一章 勾股定理 ....", "Chapter 1 Pythagorean theorem ............ 2"),
                    "toc2": ("第二章", "Chapter 2 Real numbers ............ 2"),
                    "ref": ("参考资料", "References: see the maths learning site"),
                    "para": ("在直角三角形中", "In a right triangle the sum of the squares of the legs equals the square of the hypotenuse."),
                    "ch": ("第一章 勾股定理", "Chapter 1 Pythagorean theorem"), "back": ("返回目录", "Back to contents")}
    doc = build_document(src, Lang.ZH, Lang.EN, translations)
    assert sum(1 for s in doc.segments if s.translated_text) == 7
    out = tmp_path / "linked_en.pdf"
    infos = render_document(src, doc, out, checkpoint_pages=1)  # checkpoint between the two pages
    assert len(infos) == 7 and not any(i.overflow for i in infos)
    res = pymupdf.open(str(out))
    for pno, page in enumerate(res):
        assert (_link_facts(page), _annot_facts(page), _widget_facts(page), len(page.annot_xrefs())) == expected[pno], pno
    text0, text1 = page_text(res[0]), page_text(res[1])
    assert _norm("Chapter 1 Pythagorean theorem ............ 2") in text0 and _norm("Contents") in text0
    assert "目录" not in text0 and "勾股定理" not in text0 and _norm("在直角三角形中") not in text0
    assert _norm("注意：斜边是最长的边。") in text0  # the note is still there, with its text
    assert _norm("Back to contents") in text1 and "返回目录" not in text1
    assert [i["bbox"] for i in res[0].get_image_info()] == [i["bbox"] for i in source[0].get_image_info()]


def test_page_space_ignores_annotation_text(tmp_path):
    """Text inside annotations (notes, stamps, form field values) is not page content: the
    redaction cannot remove it and the annotation survives the layout stage, so it is
    neither text that the redactions must spare (a note over a paragraph would otherwise
    cut the paragraph's redaction short and leave source glyphs) nor an obstacle."""
    pdf = pymupdf.open()
    page = pdf.new_page(width=400, height=300)
    page.insert_htmlbox(pymupdf.Rect(20, 20, 380, 60), '<p style="font-size:11px">first line of the paragraph<br>'
                        'second line of the paragraph</p>', css=CSS_PLAIN)
    note = page.add_freetext_annot(pymupdf.Rect(120, 40, 380, 100), "a note over the text", fontsize=11,
                                   fill_color=(1, 1, 0.8))
    note.update()
    src = tmp_path / "note.pdf"
    pdf.save(str(src))
    page = pymupdf.open(str(src))[0]
    assert _norm("a note over the text") in page_text(page)  # get_text does see the note ...
    lines = {"".join(s["text"] for s in line["spans"]): pymupdf.Rect(line["bbox"])
             for b in page.get_text("dict", flags=NO_LIGATURES)["blocks"] if b["type"] == 0 for line in b["lines"]}
    assert set(lines) == {"first line of the paragraph", "second line of the paragraph", "a note over the text"}
    paragraph = lines["first line of the paragraph"] | lines["second line of the paragraph"]
    assert (paragraph & lines["a note over the text"]).get_area() > 0  # ... and MuPDF merges it into the paragraph
    doc = TranslatedDocument(source_path=str(src), source_lang=Lang.EN, target_lang=Lang.ES,
                             pages=[PageInfo(index=0, width=400, height=300)])
    seg = TextSegment(id="p0_b0", page=0, bbox=BBox.from_rect(paragraph),
                      source_text="first line of the paragraph second line of the paragraph",
                      style=SegmentStyle(size=11), translated_text="primera línea del párrafo segunda línea")
    doc.segments.append(seg)
    space = _PageSpace(page, 0, doc)
    assert space.staying_text([seg.bbox]) == []  # the note's glyphs are not page text to spare
    assert space.fixed == []  # nor an obstacle
    out = tmp_path / "note_es.pdf"
    infos = render_document(src, doc, out)
    assert len(infos) == 1 and not infos[0].overflow
    res = pymupdf.open(str(out))[0]
    text = page_text(res)
    assert _norm("first line") not in text and _norm("of the paragraph") not in text
    assert _norm("primera línea del párrafo") in text
    assert _norm("a note over the text") in text  # the note survived with its text
    assert [(a.type[1], tuple(round(v) for v in a.rect)) for a in res.annots()] == [("FreeText", (120, 40, 380, 100))]


def test_render_unicode_and_special_characters(sample_pdf_en, tmp_path):
    """HTML-sensitive characters, placeholders brackets, maths symbols, accents,
    CR/LF and tabs all come out as the expected extractable text."""
    tricky = ("<b>a &amp; b</b> \"q\" 'q'\r\nAB ∠C = 90° ⟦0⟧ a²+b²=c²\tñ é ü ß\n"
              "α β γ ≤ ≥ ≠ √2 ∞ — “curly” 【方括号】、，。")
    doc = _one_segment_doc(sample_pdf_en, Lang.EN, Lang.ZH, tricky)
    out = tmp_path / "tricky.pdf"
    infos = render_document(sample_pdf_en, doc, out)
    assert len(infos) == 1
    text = page_text(pymupdf.open(str(out))[0])
    for piece in ("<b>a&b</b>\"q\"'q'", "AB∠C=90°⟦0⟧a2+b2=c2", "ñéüß", "αβγ≤≥≠√2∞", "—“curly”", "【方括号】、，。"):
        assert _norm(piece) in text, piece
    assert "&amp;" not in text and "<br>" not in text
    lines = [line for b in pymupdf.open(str(out))[0].get_text("dict")["blocks"] if b["type"] == 0
             for line in b["lines"] if "ñ" in "".join(s["text"] for s in line["spans"])
             or "curly" in "".join(s["text"] for s in line["spans"])]
    assert len(lines) >= 2  # "\r\n" and "\n" both produced line breaks


def test_render_skips_degenerate_and_unrenderable_segments(sample_pdf_en, tmp_path, caplog):
    page = pymupdf.open(str(sample_pdf_en))[0]
    blocks = [b for b in page.get_text("dict", flags=NO_LIGATURES)["blocks"] if b["type"] == 0]
    title = BBox.from_rect(blocks[0]["bbox"])
    doc = TranslatedDocument(source_path=str(sample_pdf_en), source_lang=Lang.EN, target_lang=Lang.ES,
                             pages=[PageInfo(index=0, width=595, height=842)])
    def mk(sid: str, bbox: BBox = title, **kw) -> TextSegment:
        return TextSegment(id=sid, page=0, bbox=bbox, source_text="Chapter 1", **kw)

    doc.segments += [
        mk("zero_area", bbox=BBox(x0=100, y0=100, x1=100, y1=100), translated_text="nada"),
        mk("outside", bbox=BBox(x0=700, y0=900, x1=800, y1=950), translated_text="fuera"),
        TextSegment(id="bad_page", page=7, bbox=title, source_text="x", translated_text="y"),
        mk("empty", translated_text="   "),
        mk("same", translated_text="Chapter 1"),
        mk("img", kind=SegmentKind.IMAGE_TEXT, translated_text="y"),
        mk("none"),
    ]
    out = tmp_path / "degenerate.pdf"
    with caplog.at_level("WARNING", logger="mathtrans.layout"):
        infos = render_document(sample_pdf_en, doc, out)
    assert infos == []  # nothing was renderable
    assert "bad_page" in caplog.text and "page 7" in caplog.text
    by_id = {s.id: s for s in doc.segments}
    assert by_id["zero_area"].render is not None and "not rendered" in by_id["zero_area"].render.notes
    assert by_id["outside"].render is not None and "not rendered" in by_id["outside"].render.notes
    assert all(by_id[i].render is None for i in ("bad_page", "empty", "same", "img", "none"))
    res = pymupdf.open(str(out))
    assert res.page_count == 2 and _norm("Chapter 1 The Pythagorean Theorem") in page_text(res[0])
    assert "nada" not in page_text(res[0]) and "fuera" not in page_text(res[0])


def test_render_rejects_encrypted_pdf(tmp_path):
    pdf = pymupdf.open()
    pdf.new_page().insert_htmlbox(pymupdf.Rect(20, 20, 200, 50), "<p>secret</p>", css=CSS_PLAIN)
    src = tmp_path / "locked.pdf"
    pdf.save(str(src), encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="pw", owner_pw="owner")
    doc = TranslatedDocument(source_path=str(src), source_lang=Lang.EN, target_lang=Lang.ES)
    with pytest.raises(ValueError, match="encrypted"):
        render_document(src, doc, tmp_path / "out.pdf")
    assert not (tmp_path / "out.pdf").exists()


def test_render_document_without_segments_copies_the_file(sample_pdf_zh, tmp_path):
    doc = TranslatedDocument(source_path=str(sample_pdf_zh), source_lang=Lang.ZH, target_lang=Lang.EN)
    out = tmp_path / "copy.pdf"
    assert render_document(sample_pdf_zh, doc, out) == []
    res, src = pymupdf.open(str(out)), pymupdf.open(str(sample_pdf_zh))
    assert res.page_count == 2 and all(page_text(res[i]) == page_text(src[i]) for i in range(2))


def test_output_size_does_not_grow_per_segment(tmp_path):
    """insert_htmlbox embeds a full font copy per call; saving must merge them so a
    page with 30 translated lines is not 30 x the font size (DejaVu Sans here)."""
    pdf = pymupdf.open()
    page = pdf.new_page()
    for i in range(30):
        page.insert_htmlbox(pymupdf.Rect(50, 40 + i * 24, 540, 60 + i * 24),
                            f'<p style="font-size:11px">Zeile {i} mit etwas Text für den Umbruch</p>', css=CSS_PLAIN)
    src = tmp_path / "many.pdf"
    pdf.save(str(src), garbage=4, deflate=True)
    translations = {f"l{i}": (f"Zeile {i} ", f"Line {i} with some text for wrapping") for i in range(30)}
    doc = build_document(src, Lang.EN, Lang.EN, translations)  # German text declared as en: style only
    out = tmp_path / "many_en.pdf"
    infos = render_document(src, doc, out)
    assert len(infos) == 30
    assert "@font-face" in page_css(Lang.EN)[0]  # a real font file is embedded (not a built-in)
    size = out.stat().st_size
    assert size < 1_200_000, f"output is {size} bytes: fonts were embedded once per segment"
    res = pymupdf.open(str(out))
    assert all(_norm(f"Line {i} with some text") in page_text(res[0]) for i in range(30))
    assert sum(1 for f in res.get_page_fonts(0) if f[1] == "n/a") == 0  # everything embedded


def test_render_concurrently_in_threads(sample_pdf_zh, sample_pdf_en, tmp_path):
    """The web service runs several pipelines at once: parallel renders of
    different documents must not interfere (shared font index / Story engine)."""
    import threading

    errors: list[str] = []

    def work(n: int) -> None:
        try:
            if n % 2 == 0:
                doc = build_document(sample_pdf_zh, Lang.ZH, Lang.EN, sample_translations(Lang.ZH, Lang.EN))
                src, probe, gone = sample_pdf_zh, "Pythagorean", "勾股定理"
            else:
                doc = build_document(sample_pdf_en, Lang.EN, Lang.ZH, sample_translations(Lang.EN, Lang.ZH))
                src, probe, gone = sample_pdf_en, "勾股定理", "Pythagorean"
            out = tmp_path / f"thread_{n}.pdf"
            render_document(src, doc, out)
            text = page_text(pymupdf.open(str(out))[0])
            if _norm(probe) not in text or gone in text:
                errors.append(f"thread {n}: unexpected text")
            render_page_previews(out, tmp_path / f"prev_{n}", dpi=20)
        except Exception as exc:  # noqa: BLE001 - reported by the main thread
            errors.append(f"thread {n}: {exc!r}")

    threads = [threading.Thread(target=work, args=(n,)) for n in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=300)
    assert not any(t.is_alive() for t in threads)
    assert errors == []
    assert all((tmp_path / f"prev_{n}" / "page-002.png").is_file() for n in range(4))


def test_render_document_checkpoint_matches_single_pass(tmp_path):
    """Long documents are checkpointed (saved with duplicate merging + reopened) every
    ``checkpoint_pages`` rendered pages so the per-call font copies of insert_htmlbox do
    not pile up in memory; the output must equal a single-pass render and no temporary
    checkpoint file may be left behind."""
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 16, 16), False)
    pix.clear_with(180)
    png = pix.tobytes("png")
    pdf = pymupdf.open()
    n_pages, per_page = 12, 5
    for pno in range(n_pages):
        page = pdf.new_page()
        page.insert_image(pymupdf.Rect(420, 40 + pno, 560, 120 + pno), stream=png)
        for i in range(per_page):
            page.insert_htmlbox(pymupdf.Rect(50, 160 + i * 30, 400, 184 + i * 30),
                                f'<p style="font-size:11px">Seite {pno} Zeile {i} mit etwas Text</p>', css=CSS_PLAIN)
    src = tmp_path / "long.pdf"
    pdf.save(str(src), garbage=4, deflate=True)
    pdf.close()
    translations = {f"p{p}l{i}": (f"Seite {p} Zeile {i} ", f"Page {p} line {i} with some text")
                    for p in range(n_pages) for i in range(per_page)}

    def render(name: str, checkpoint_pages: int):
        doc = build_document(src, Lang.EN, Lang.EN, translations)
        out = tmp_path / name
        infos = render_document(src, doc, out, checkpoint_pages=checkpoint_pages)
        return out, [(i.scale, i.overflow, i.bbox.as_tuple() if i.bbox else None) for i in infos]

    out_ckpt, infos_ckpt = render("ckpt.pdf", 4)
    out_single, infos_single = render("single.pdf", 0)
    assert len(infos_ckpt) == n_pages * per_page and infos_ckpt == infos_single
    assert not list(tmp_path.glob("*checkpoint*")), "checkpoint file left behind"
    with pymupdf.open(str(out_ckpt)) as a, pymupdf.open(str(out_single)) as b, pymupdf.open(str(src)) as s:
        assert a.page_count == b.page_count == n_pages
        for pno in range(n_pages):
            assert page_text(a[pno]) == page_text(b[pno])
            assert _norm(f"Page {pno} line 4 with some text") in page_text(a[pno]) and "Seite" not in page_text(a[pno])
            assert [i["bbox"] for i in a[pno].get_image_info()] == [i["bbox"] for i in s[pno].get_image_info()]
            assert a[pno].rect == s[pno].rect
        assert sum(1 for f in a.get_page_fonts(n_pages - 1) if f[1] == "n/a") == 0
    assert out_ckpt.stat().st_size < 1.25 * out_single.stat().st_size  # fonts merged in both cases
    # in-place rendering with checkpoints works too (the checkpoint lives next to the output)
    doc = build_document(src, Lang.EN, Lang.EN, translations)
    shutil.copyfile(src, tmp_path / "inplace.pdf")
    render_document(tmp_path / "inplace.pdf", doc, tmp_path / "inplace.pdf", checkpoint_pages=5)
    with pymupdf.open(str(tmp_path / "inplace.pdf")) as c:
        assert c.page_count == n_pages and _norm("Page 11 line 0") in page_text(c[11])
    assert not list(tmp_path.glob("*checkpoint*"))
