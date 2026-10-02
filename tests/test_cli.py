"""Tests for the command-line interface (pipeline runner monkeypatched)."""
from __future__ import annotations

import shutil
from pathlib import Path

import pymupdf
import pytest

from mathtrans import cli
from mathtrans.models import Lang, PipelineOptions, PipelineResult, PipelineStats, QAIssue, QAReport, QARound


class RecordingRunner:
    """Fake pipeline that records its call and returns a configurable result."""

    def __init__(self, status: str = "completed", raise_error: bool = False):
        self.status = status
        self.raise_error = raise_error
        self.calls: list[dict] = []

    def __call__(self, source_pdf, out_dir, options: PipelineOptions, settings=None, progress=None) -> PipelineResult:
        self.calls.append({"source": Path(source_pdf), "out_dir": Path(out_dir), "options": options,
                           "settings": settings})
        if self.raise_error:
            raise RuntimeError("backend unavailable")
        if progress:
            progress("extract", "Extracting", 5)
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        if self.status == "error":
            return PipelineResult(status="error", error="Source file is not a PDF",
                                  stats=PipelineStats(target_lang=options.target_lang.value))
        shutil.copyfile(source_pdf, out_dir / "output.pdf")
        failed = self.status == "qa_failed"
        issues = [QAIssue(check="numbers", severity="error", message="number 25 missing", segment_id="p0_b3", page=0)] \
            if failed else []
        report = QAReport(passed=not failed, rounds=[QARound(round=1, issues=issues, passed=not failed)],
                          checks_run=["numbers"], final_issues=issues, errors=len(issues),
                          summary="QA failed: 1 error" if failed else "QA passed: 1 round, 0 errors")
        result = PipelineResult(
            status=self.status, output_pdf=str(out_dir / "output.pdf"), segments_json=str(out_dir / "segments.json"),
            qa_report_json=str(out_dir / "qa_report.json"), qa_report=report,
            stats=PipelineStats(pages=2, text_segments=12, translated=12, qa_rounds=1, translator="fake",
                                source_lang="zh", target_lang=options.target_lang.value, duration_s=1.5),
            preview_pages=[str(out_dir / "previews" / "page-001.png"), str(out_dir / "previews" / "page-002.png")],
        )
        if options.bilingual:
            result.bilingual_pdf = str(out_dir / "bilingual.pdf")
        if options.export_docx:
            result.docx = str(out_dir / "output.docx")
        if failed:
            result.error = "QA did not pass"
        return result


@pytest.fixture
def runner(monkeypatch, offline_settings):
    r = RecordingRunner()
    monkeypatch.setattr(cli, "_get_runner", lambda: r)
    return r


def test_translate_completed_exits_0_and_prints_paths(runner, sample_pdf_zh, tmp_path, capsys):
    out = tmp_path / "out"
    code = cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--out", str(out), "--bilingual", "--docx",
                     "--no-images", "--max-rounds", "4", "--from", "zh", "--translator", "mock"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Status:" in captured.out and "completed" in captured.out
    assert str(out / "output.pdf") in captured.out and str(out / "bilingual.pdf") in captured.out
    assert str(out / "output.docx") in captured.out and "QA: PASSED" in captured.out
    assert "[  5%] extract" in captured.err  # progress goes to stderr
    call = runner.calls[0]
    assert call["source"] == sample_pdf_zh and call["out_dir"] == out
    opts = call["options"]
    assert opts.target_lang is Lang.EN and opts.source_lang is Lang.ZH
    assert opts.bilingual and opts.export_docx and not opts.translate_images
    assert opts.max_qa_rounds == 4 and opts.require_qa_pass and opts.translator == "mock" and opts.glossary is None
    assert call["settings"] is not None and call["settings"].translator == "mock"


def test_translate_qa_failed_exits_2(monkeypatch, offline_settings, sample_pdf_zh, tmp_path, capsys):
    r = RecordingRunner(status="qa_failed")
    monkeypatch.setattr(cli, "_get_runner", lambda: r)
    code = cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--out", str(tmp_path / "o"), "--no-require-qa"])
    assert code == 2
    out = capsys.readouterr().out
    assert "qa_failed" in out and "QA: FAILED" in out and "number 25 missing" in out and "p1" in out
    assert r.calls[0]["options"].require_qa_pass is False


def test_translate_error_exits_1(monkeypatch, offline_settings, sample_pdf_zh, tmp_path, capsys):
    r = RecordingRunner(status="error")
    monkeypatch.setattr(cli, "_get_runner", lambda: r)
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--out", str(tmp_path / "o")]) == 1
    assert "Error:" in capsys.readouterr().out
    r2 = RecordingRunner(raise_error=True)
    monkeypatch.setattr(cli, "_get_runner", lambda: r2)
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--out", str(tmp_path / "o2")]) == 1
    assert "backend unavailable" in capsys.readouterr().err


def test_translate_argument_errors(runner, sample_pdf_zh, tmp_path, capsys):
    assert cli.main(["translate", str(tmp_path / "missing.pdf"), "--to", "en"]) == 1
    assert "not found" in capsys.readouterr().err
    not_pdf = tmp_path / "x.pdf"
    not_pdf.write_bytes(b"hello")
    assert cli.main(["translate", str(not_pdf), "--to", "en"]) == 1
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "zh", "--from", "zh"]) == 1
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "xx"]) == 1
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--glossary", str(tmp_path / "none.csv")]) == 1
    assert runner.calls == []
    with pytest.raises(SystemExit):
        cli.main(["translate", str(sample_pdf_zh)])  # --to is required


def test_translate_with_glossary_and_default_out_dir(runner, sample_pdf_zh, tmp_path, monkeypatch):
    glossary = tmp_path / "terms.csv"
    glossary.write_text("zh,en\n斜边,hypotenuse side\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--glossary", str(glossary)]) == 0
    call = runner.calls[0]
    assert call["out_dir"] == Path("output") / f"{sample_pdf_zh.stem}_en"
    assert call["options"].glossary is not None
    assert call["options"].glossary.pairs("zh", "en") == [("斜边", "hypotenuse side")]


def test_sample_creates_pdf(tmp_path, capsys):
    out = tmp_path / "samples" / "sample_ja.pdf"
    assert cli.main(["sample", str(out), "--lang", "ja"]) == 0
    assert out.is_file() and str(out) in capsys.readouterr().out
    with pymupdf.open(str(out)) as doc:
        assert doc.page_count == 2 and "三平方の定理" in doc[0].get_text()


def test_glossary_template(tmp_path, capsys):
    out = tmp_path / "g" / "template.csv"
    assert cli.main(["glossary-template", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("zh,en,pt,es,ja,ko,note") and "Pythagorean theorem" in text
    assert str(out) in capsys.readouterr().out


def test_serve_runs_uvicorn(monkeypatch, offline_settings):
    import uvicorn

    calls: list[dict] = []
    monkeypatch.setattr(uvicorn, "run", lambda app, **kw: calls.append({"app": app, **kw}))
    assert cli.main(["serve", "--host", "0.0.0.0", "--port", "9999"]) == 0
    assert calls and calls[0]["host"] == "0.0.0.0" and calls[0]["port"] == 9999
    assert calls[0]["app"].title == "mathtrans"


def test_default_runner_is_the_pipeline():
    from mathtrans.pipeline import run_pipeline

    assert cli._get_runner() is run_pipeline


def test_translate_rejects_bad_rounds_and_empty_glossary(runner, sample_pdf_zh, tmp_path, capsys):
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--max-rounds", "0"]) == 1
    assert "max-rounds" in capsys.readouterr().err
    empty = tmp_path / "empty.csv"
    empty.write_text("zh,en\n", encoding="utf-8")
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--glossary", str(empty)]) == 1
    assert "no entries" in capsys.readouterr().err
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    assert cli.main(["translate", str(sample_pdf_zh), "--to", "en", "--glossary", str(broken)]) == 1
    assert "cannot load glossary" in capsys.readouterr().err
    assert runner.calls == []


def test_uvicorn_log_level_mapping(monkeypatch, offline_settings):
    assert cli._uvicorn_log_level("INFO") == "info"
    assert cli._uvicorn_log_level("WARN") == "warning"
    assert cli._uvicorn_log_level(" Debug ") == "debug"
    assert cli._uvicorn_log_level("bogus") == "info"
    import uvicorn

    from mathtrans.config import reset_settings

    monkeypatch.setenv("MATHTRANS_LOG_LEVEL", "WARN")
    reset_settings()
    calls: list[dict] = []
    monkeypatch.setattr(uvicorn, "run", lambda app, **kw: calls.append(kw))
    assert cli.main(["serve"]) == 0
    assert calls[0]["log_level"] == "warning" and calls[0]["host"] == "127.0.0.1" and calls[0]["port"] == 8000
    reset_settings()


def test_translate_summary_lists_issues_with_pages_and_truncates(capsys, tmp_path):
    issues = [QAIssue(check="numbers", severity="error", message=f"number {i} missing", segment_id=f"p1_b{i}", page=1)
              for i in range(25)]
    report = QAReport(passed=False, rounds=[QARound(round=1, issues=issues)], final_issues=issues, errors=25, summary="25 errors")
    result = PipelineResult(status="qa_failed", output_pdf=str(tmp_path / "output.pdf"), qa_report=report,
                            stats=PipelineStats(pages=2, text_segments=3, translated=3, qa_rounds=1))
    cli.print_summary(result, tmp_path / "in.pdf", Lang.EN, tmp_path)
    out = capsys.readouterr().out
    assert "QA: FAILED - 1 round(s), 25 error(s), 0 warning(s)" in out
    assert out.count("number ") == 20 and "... 5 more issue(s)" in out and "p2 p1_b0" in out
