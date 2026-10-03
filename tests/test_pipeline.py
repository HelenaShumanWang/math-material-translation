"""End-to-end tests of the pipeline with the offline mock translator."""
import json

import pymupdf
import pytest

from mathtrans.models import Lang, PipelineOptions
from mathtrans.pipeline import run_pipeline


def _image_bboxes(pdf):
    d = pymupdf.open(str(pdf))
    out = []
    for p in d:
        out.append(sorted(tuple(round(v) for v in i["bbox"]) for i in p.get_image_info()))
    return out


@pytest.fixture(scope="module")
def zh_en_result(tmp_path_factory, samples_dir):
    from mathtrans.config import reset_settings
    from mathtrans.samples import make_sample_pdf

    mp = pytest.MonkeyPatch()
    mp.delenv("ANTHROPIC_API_KEY", raising=False)
    mp.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    reset_settings()
    try:
        src = make_sample_pdf(samples_dir / "e2e_zh.pdf", "zh")
        out = tmp_path_factory.mktemp("zh_en")
        opts = PipelineOptions(target_lang=Lang.EN, bilingual=True, export_docx=True, translator="mock")
        res = run_pipeline(src, out, opts)
        yield src, out, res
    finally:
        mp.undo()
        reset_settings()


def test_e2e_zh_to_en_completes(zh_en_result):
    src, out, res = zh_en_result
    assert res.status == "completed", res.error
    assert res.qa_report is not None and res.qa_report.passed
    assert res.stats.pages == 2 and res.stats.text_segments >= 10
    assert res.stats.translated >= 10 and res.stats.qa_rounds >= 1
    assert res.stats.image_segments >= 1  # OCR found labels inside the figures


def test_e2e_output_is_layout_preserving(zh_en_result):
    src, out, res = zh_en_result
    d_src, d_out = pymupdf.open(str(src)), pymupdf.open(str(res.output_pdf))
    assert d_out.page_count == d_src.page_count
    for a, b in zip(d_src, d_out):
        assert abs(a.rect.width - b.rect.width) < 0.5 and abs(a.rect.height - b.rect.height) < 0.5
    assert _image_bboxes(src) == _image_bboxes(res.output_pdf)


def test_e2e_output_text_translated(zh_en_result):
    src, out, res = zh_en_result
    d = pymupdf.open(str(res.output_pdf))
    text = "\n".join(p.get_text() for p in d)
    assert "Pythagorean theorem" in text  # glossary term applied
    assert "勾股定理" not in text and "直角三角形" not in text
    assert "a² + b² = c²" in text  # formula kept verbatim
    assert "25" in text and "3 cm" in text
    base14 = ("Helvetica", "Times", "Courier", "Symbol", "ZapfDingbats", "Arial")
    for f in d[0].get_fonts():
        # fonts we add must be embedded; standard base-14 fonts of the source need not be
        assert f[1] != "n/a" or f[3].startswith(base14), f


def test_e2e_artifacts_written(zh_en_result):
    src, out, res = zh_en_result
    assert (out / "output.pdf").is_file() and (out / "segments.json").is_file()
    assert (out / "qa_report.json").is_file() and (out / "qa_report.md").is_file()
    assert res.bilingual_pdf and pymupdf.open(res.bilingual_pdf)[0].rect.width > 1000
    assert res.docx and res.docx.endswith(".docx")
    assert len(res.preview_pages) == 2 and all(p.endswith(".png") for p in res.preview_pages)
    segs = json.loads((out / "segments.json").read_text(encoding="utf-8"))
    assert segs["source_lang"] == "zh" and segs["target_lang"] == "en"
    assert any(s["kind"] == "image_text" for s in segs["segments"])


def test_e2e_qa_loop_fixes_faulty_translation(samples_dir, tmp_path):
    from mathtrans.translate.mock import MockTranslator

    src = samples_dir / "e2e_zh.pdf"
    opts = PipelineOptions(target_lang=Lang.EN, translator="mock", max_qa_rounds=3)
    res = run_pipeline(src, tmp_path, opts, translator=MockTranslator(drop_placeholders=True))
    assert res.status == "completed", res.error
    assert res.qa_report.passed and len(res.qa_report.rounds) >= 2
    assert any(r.retranslated for r in res.qa_report.rounds)


def test_e2e_qa_failure_blocks_output(samples_dir, tmp_path):
    from mathtrans.translate.mock import MockTranslator

    src = samples_dir / "e2e_zh.pdf"
    opts = PipelineOptions(target_lang=Lang.EN, translator="mock", max_qa_rounds=1)
    res = run_pipeline(src, tmp_path / "strict", opts, translator=MockTranslator(leave_untranslated=True))
    assert res.status == "qa_failed" and res.qa_report is not None and not res.qa_report.passed
    assert (tmp_path / "strict" / "output.pdf").is_file()  # kept for inspection
    opts2 = PipelineOptions(target_lang=Lang.EN, translator="mock", max_qa_rounds=1, require_qa_pass=False)
    res2 = run_pipeline(src, tmp_path / "lenient", opts2, translator=MockTranslator(leave_untranslated=True))
    assert res2.status == "completed" and not res2.qa_report.passed


def test_e2e_en_to_zh(samples_dir, tmp_path):
    from mathtrans.samples import make_sample_pdf

    src = make_sample_pdf(samples_dir / "e2e_en.pdf", "en")
    res = run_pipeline(src, tmp_path, PipelineOptions(target_lang=Lang.ZH, translator="mock"))
    assert res.status == "completed", res.error
    text = "\n".join(p.get_text() for p in pymupdf.open(str(res.output_pdf)))
    assert "勾股定理" in text and "Pythagorean theorem" not in text


def test_e2e_same_language_is_an_error(samples_dir, tmp_path):
    src = samples_dir / "e2e_zh.pdf"
    res = run_pipeline(src, tmp_path, PipelineOptions(target_lang=Lang.ZH, translator="mock"))
    assert res.status == "error" and "target" in (res.error or "")


def test_pipeline_rejects_too_many_pages(sample_pdf_zh, tmp_path):
    """``Settings.max_pages`` bounds the pages a run may process (memory grows per rendered page);
    the selection made with ``pages`` / ``skip_pages`` counts, so a long book can still be
    translated chapter by chapter."""
    from mathtrans.config import Settings

    src = sample_pdf_zh
    settings = Settings(translator="mock", ocr_engine="none", max_pages=1)
    result = run_pipeline(src, tmp_path / "all", PipelineOptions(target_lang=Lang.EN, translate_images=False),
                          settings=settings)
    assert result.status == "error" and "2 pages" in result.error and "MATHTRANS_MAX_PAGES" in result.error
    assert not (tmp_path / "all" / "output.pdf").exists()
    result = run_pipeline(src, tmp_path / "one", PipelineOptions(target_lang=Lang.EN, translate_images=False, pages=[0]),
                          settings=settings)
    assert result.status in ("completed", "qa_failed"), result.error
    with pymupdf.open(str(tmp_path / "one" / "output.pdf")) as out:
        assert out.page_count == 2
    unlimited = Settings(translator="mock", ocr_engine="none", max_pages=0)
    assert run_pipeline(src, tmp_path / "skip", PipelineOptions(target_lang=Lang.EN, translate_images=False, skip_pages=[1]),
                        settings=unlimited).status != "error"


# --------------------------------------------------------------------------- #
# Runs that translate nothing must never be reported as a successful translation
# --------------------------------------------------------------------------- #


def _scanned_pdf(path, page_number: bool = False):
    """One page that is a single raster image containing Chinese sentences (a scan);
    with ``page_number`` the text layer holds only the page number ``12``."""
    from PIL import Image, ImageDraw

    from mathtrans.fonts import pil_font

    img = Image.new("RGB", (1200, 1600), "white")
    draw = ImageDraw.Draw(img)
    font = pil_font(Lang.ZH, 48)
    draw.text((100, 100), "第一章 勾股定理", font=font, fill="black")
    draw.text((100, 220), "直角三角形的两条直角边的平方和等于斜边的平方。", font=font, fill="black")
    png = path.with_suffix(".png")
    img.save(png)
    pdf = pymupdf.open()
    page = pdf.new_page(width=600, height=800)
    page.insert_image(pymupdf.Rect(20, 20, 580, 760), filename=str(png))
    if page_number:
        page.insert_text((290, 790), "12", fontsize=9)
    pdf.save(str(path))
    pdf.close()
    return path


def test_scanned_pdf_whose_images_are_not_read_is_not_reported_as_completed(tmp_path):
    """A scan whose text was never recognised (image translation off, no OCR engine, or OCR
    failing) must not end as 'completed / QA passed' with an untranslated copy of the source."""
    from mathtrans.ocr import OcrError

    class FailingOcr:
        name = "claude"

        def recognize(self, image_rgb, hint_langs=None):
            raise OcrError("Claude vision OCR request failed (RateLimitError): 429")

    scan = _scanned_pdf(tmp_path / "scan.pdf")
    res = run_pipeline(scan, tmp_path / "no_images",
                       PipelineOptions(target_lang=Lang.EN, source_lang=Lang.ZH, translator="mock",
                                       translate_images=False))
    assert res.status == "error" and res.stats.translated == 0
    assert "no text layer" in res.error and "disabled" in res.error
    assert not (tmp_path / "no_images" / "output.pdf").exists()

    res = run_pipeline(scan, tmp_path / "engine_none",
                       PipelineOptions(target_lang=Lang.EN, source_lang=Lang.ZH, translator="mock",
                                       ocr_engine="none"))
    assert res.status == "error" and "no OCR engine" in res.error and res.stats.ocr_engine == "none"

    res = run_pipeline(scan, tmp_path / "ocr_fails",
                       PipelineOptions(target_lang=Lang.EN, source_lang=Lang.ZH, translator="mock"),
                       ocr_engine=FailingOcr())
    assert res.status == "error" and res.stats.ocr_failures == 1 and res.stats.translated == 0
    assert "OCR failed on 1 image(s)" in res.error and "429" in res.error
    assert not (tmp_path / "ocr_fails" / "output.pdf").exists()

    # A text layer that holds nothing but a page number does not make the scan translatable.
    numbered = _scanned_pdf(tmp_path / "scan_numbered.pdf", page_number=True)
    res = run_pipeline(numbered, tmp_path / "numbered",
                       PipelineOptions(target_lang=Lang.EN, source_lang=Lang.ZH, translator="mock",
                                       translate_images=False))
    assert res.status == "error" and res.stats.text_segments == 1 and res.stats.translated == 0
    assert "1 image(s) was not recognised" in res.error and "disabled" in res.error


def test_formula_only_page_completes_with_a_completeness_warning(tmp_path):
    """A page that contains only numbers / formulas is legitimately left as it is: the run
    completes, QA passes, and the report says explicitly that nothing was translated."""
    src = tmp_path / "formulas.pdf"
    pdf = pymupdf.open()
    page = pdf.new_page()
    for y, line in ((100, "3 + 4 = 7"), (130, "12 × 5 = 60"), (160, "x² + y² = z²")):
        page.insert_text((72, y), line, fontsize=14)
    pdf.save(str(src))
    pdf.close()
    res = run_pipeline(src, tmp_path / "out",
                       PipelineOptions(target_lang=Lang.ZH, source_lang=Lang.EN, translator="mock",
                                       translate_images=False))
    assert res.status == "completed", res.error
    assert res.qa_report.passed and res.qa_report.errors == 0
    assert res.stats.text_segments == 3 and res.stats.skipped == 3 and res.stats.translated == 0
    notes = [i for i in res.qa_report.final_issues if i.check == "completeness"]
    assert len(notes) == 1 and notes[0].severity == "warning" and notes[0].segment_id is None
    assert "Nothing to translate" in notes[0].message and "identical to the source" in notes[0].message
    assert not notes[0].fixable and res.qa_report.warnings >= 1
    assert "1 warning" in res.qa_report.summary or "2 warnings" in res.qa_report.summary
    text = pymupdf.open(res.output_pdf)[0].get_text()
    assert "3 + 4 = 7" in text and "x² + y² = z²" in text
    assert "Nothing to translate" in (tmp_path / "out" / "qa_report.md").read_text(encoding="utf-8")


def test_e2e_retranslate_failure_keeps_artifacts_consistent(sample_pdf_zh, tmp_path):
    """A TranslationError half-way through a multi-chunk QA re-translation rolls the already
    applied chunks back, so output.pdf, segments.json and the QA report describe the same
    translations (the previous round's) instead of a half-updated document."""
    import re
    import unicodedata

    from mathtrans.config import Settings
    from mathtrans.interfaces import TranslationError
    from mathtrans.models import TranslatedDocument
    from mathtrans.translate.mock import MockTranslator

    class Flaky(MockTranslator):
        """Faulty first attempt (so QA re-translates), then an outage on the 2nd re-translation chunk."""

        def __init__(self):
            super().__init__(drop_placeholders=True)
            self.retranslate_calls = 0

        def translate(self, items, src, tgt, pairs, doc_context=""):
            if any(it.feedback for it in items):
                self.retranslate_calls += 1
                if self.retranslate_calls == 2:
                    raise TranslationError("simulated API outage on chunk 2 of the re-translation")
            return super().translate(items, src, tgt, pairs, doc_context)

    def norm(text: str) -> str:
        return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text)).casefold()

    flaky = Flaky()
    settings = Settings(translator="mock", ocr_engine="none", batch_chars=60)  # tiny chunks: several requests
    res = run_pipeline(sample_pdf_zh, tmp_path,
                       PipelineOptions(target_lang=Lang.EN, translator="mock", max_qa_rounds=3,
                                       translate_images=False),
                       settings=settings, translator=flaky)
    assert flaky.retranslate_calls == 2, "the first re-translation chunk must have been applied before the outage"
    assert res.status == "qa_failed" and not res.qa_report.passed
    assert any(i.check == "retranslate" for i in res.qa_report.final_issues)
    retried = res.qa_report.rounds[0].retranslated
    assert retried and len(res.qa_report.rounds) == 1

    doc = TranslatedDocument.model_validate_json((tmp_path / "segments.json").read_text(encoding="utf-8"))
    pdf_text = norm("\n".join(p.get_text() for p in pymupdf.open(str(tmp_path / "output.pdf"))))
    report_md = (tmp_path / "qa_report.md").read_text(encoding="utf-8")
    for seg_id in retried:
        seg = doc.segment(seg_id)
        assert seg.attempts == 1 and seg.render is not None, seg_id   # rolled back to the rendered round
        assert seg.feedback, seg_id                                     # the QA feedback is still pending
        assert norm(seg.translated_text) in pdf_text, (seg_id, seg.translated_text)
    # the markdown report quotes the same translation as segments.json
    seg = doc.segment(retried[0])
    rows = [line for line in report_md.splitlines() if f"| {seg.id} |" in line]
    assert rows and all(line.rstrip("| ").endswith(seg.translated_text[:40]) or seg.translated_text[:40] in line
                        for line in rows)
