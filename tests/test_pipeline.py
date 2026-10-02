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
