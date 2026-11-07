"""Tests for the project store and the REST API (offline, with a fake pipeline runner)."""
from __future__ import annotations

import json
import os
import re
import shutil
import threading
import time
from pathlib import Path
from typing import Optional

import pymupdf
import pytest
from fastapi.testclient import TestClient

from mathtrans.api import (MAX_GLOSSARY_ENTRIES, MAX_GLOSSARY_NAME_CHARS, MAX_GLOSSARY_TERM_CHARS, create_app,
                           cross_site_reason)
from mathtrans.config import Settings
from mathtrans.models import (BBox, Lang, PageInfo, PipelineOptions, PipelineResult, PipelineStats, QAIssue,
                              QAReport, QARound, TextSegment, TranslatedDocument)
from mathtrans.projects import PdfTooLarge, ProjectBusy, ProjectNotFound, ProjectStore, ProjectUnreadable, safe_name


class FakeRunner:
    """Stands in for ``mathtrans.pipeline.run_pipeline``: copies the source as the output,
    writes segments.json / qa_report.json / one preview PNG and returns a result whose
    status depends on the flags. ``finished`` is set after every call (for async tests)."""

    def __init__(self, fail_qa: bool = False, raise_error: bool = False, error_result: bool = False,
                 delay: float = 0.0):
        self.fail_qa = fail_qa
        self.raise_error = raise_error
        self.error_result = error_result
        self.delay = delay
        self.calls: list[dict] = []
        self.finished = threading.Event()

    def __call__(self, source_pdf, out_dir, options: PipelineOptions, settings=None, progress=None) -> PipelineResult:
        try:
            return self._run(source_pdf, out_dir, options, settings, progress)
        finally:
            self.finished.set()

    def _run(self, source_pdf, out_dir, options: PipelineOptions, settings, progress) -> PipelineResult:
        source_pdf, out_dir = Path(source_pdf), Path(out_dir)
        self.calls.append({"source": source_pdf, "out_dir": out_dir, "options": options, "settings": settings})
        out_dir.mkdir(parents=True, exist_ok=True)
        if progress:
            progress("extract", "Extracting text", 5)
            progress("translate", "Translating 12 segments", 45)
        if self.delay:
            time.sleep(self.delay)
        if self.raise_error:
            raise RuntimeError("runner exploded")
        if self.error_result:
            return PipelineResult(status="error", error="Source language equals the target language")

        shutil.copyfile(source_pdf, out_dir / "output.pdf")
        src_lang = options.source_lang or Lang.ZH
        seg = TextSegment(id="p0_b0", page=0, bbox=BBox(x0=60, y0=50, x1=535, y1=90), source_text="勾股定理",
                          translated_text="Pythagorean theorem")
        doc = TranslatedDocument(source_path=str(source_pdf), source_lang=src_lang, target_lang=options.target_lang,
                                 pages=[PageInfo(index=0, width=595, height=842)], segments=[seg])
        (out_dir / "segments.json").write_text(doc.model_dump_json(), encoding="utf-8")
        issues = []
        if self.fail_qa:
            issues = [QAIssue(check="untranslated", severity="error", message="source text left in translation",
                              segment_id="p0_b0", page=0)]
        report = QAReport(passed=not self.fail_qa, rounds=[QARound(round=1, issues=issues, passed=not self.fail_qa)],
                          checks_run=["completeness", "untranslated"], final_issues=issues,
                          errors=len(issues), warnings=0, summary="QA failed: 1 error" if self.fail_qa else "QA passed")
        (out_dir / "qa_report.json").write_text(report.model_dump_json(), encoding="utf-8")
        previews = out_dir / "previews"
        previews.mkdir(exist_ok=True)
        with pymupdf.open(str(out_dir / "output.pdf")) as pdf:
            pdf[0].get_pixmap(dpi=30).save(str(previews / "page-001.png"))
        result = PipelineResult(
            status="qa_failed" if self.fail_qa else "completed",
            output_pdf=str(out_dir / "output.pdf"),
            segments_json=str(out_dir / "segments.json"),
            qa_report_json=str(out_dir / "qa_report.json"),
            qa_report=report,
            stats=PipelineStats(pages=2, text_segments=12, translated=12, qa_rounds=1, translator="fake",
                                source_lang=src_lang.value, target_lang=options.target_lang.value),
            preview_pages=[str(previews / "page-001.png")],
        )
        if options.bilingual:
            shutil.copyfile(source_pdf, out_dir / "bilingual.pdf")
            result.bilingual_pdf = str(out_dir / "bilingual.pdf")
        if options.export_docx:
            (out_dir / "output.docx").write_bytes(b"PK\x03\x04fake-docx")
            result.docx = str(out_dir / "output.docx")
        if self.fail_qa:
            result.error = "QA did not pass: 1 error"
        if progress:
            progress("done", report.summary, 100)
        return result


@pytest.fixture
def pdf_bytes(sample_pdf_zh) -> bytes:
    return sample_pdf_zh.read_bytes()


@pytest.fixture
def make_client(offline_settings):
    """Factory: make_client(runner=..., sync=True, settings=...) -> TestClient."""
    clients: list[TestClient] = []

    def _make(runner: Optional[FakeRunner] = None, sync: bool = True, settings: Optional[Settings] = None) -> TestClient:
        app = create_app(settings=settings or offline_settings, runner=runner or FakeRunner(), sync=sync)
        client = TestClient(app)
        client.__enter__()
        clients.append(client)
        return client

    yield _make
    for c in clients:
        c.__exit__(None, None, None)


def _upload(client: TestClient, pdf_bytes: bytes, names=("book.pdf",), **fields) -> dict:
    data = {"target_lang": "en"}
    data.update({k: str(v) for k, v in fields.items()})
    files = [("files", (name, pdf_bytes, "application/pdf")) for name in names]
    r = client.post("/api/projects", files=files, data=data)
    assert r.status_code == 201, r.text
    return r.json()


# --------------------------------------------------------------------------- #
# Basics
# --------------------------------------------------------------------------- #


def test_languages_list(make_client):
    r = make_client().get("/api/languages")
    assert r.status_code == 200
    codes = [l["code"] for l in r.json()]
    assert codes == ["zh", "en", "pt", "es", "ja", "ko"]
    assert all({"code", "name", "native"} <= set(l) for l in r.json())


def test_index_html_served(make_client):
    r = make_client().get("/")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/html")
    assert "/api/projects" in r.text and "数学资料翻译" in r.text and "Math Material Translation" in r.text
    assert "<script" in r.text and "src=\"http" not in r.text  # self-contained, no CDN
    # the retranslate form must encode an emptied skip-pages field as "" (clears it), never as null (keeps it)
    assert "value.trim() || null" not in r.text and 'skip_pages: $("re-skip").value.trim(),' in r.text


# --------------------------------------------------------------------------- #
# Create / status / get
# --------------------------------------------------------------------------- #


def test_create_batch_of_two_files_shares_batch_id(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    res = _upload(client, pdf_bytes, names=("第一册.pdf", "volume2.PDF"))
    projects = res["projects"]
    assert len(projects) == 2 and res["batch_id"]
    assert {p["batch_id"] for p in projects} == {res["batch_id"]}
    assert [p["name"] for p in projects] == ["第一册", "volume2"]
    assert all(p["status"] == "completed" for p in projects)  # sync mode ran both jobs inline
    assert len(runner.calls) == 2
    listed = client.get("/api/projects", params={"batch_id": res["batch_id"]}).json()
    assert {p["id"] for p in listed} == {p["id"] for p in projects}
    assert client.get("/api/projects", params={"batch_id": "nope"}).json() == []
    assert len(client.get("/api/projects").json()) == 2


def test_invalid_uploads_are_rejected(make_client, pdf_bytes):
    client = make_client()
    r = client.post("/api/projects", files=[("files", ("notes.pdf", b"hello world", "application/pdf"))],
                    data={"target_lang": "en"})
    assert r.status_code == 400 and "%PDF" in r.json()["detail"]
    r = client.post("/api/projects", files=[("files", ("notes.txt", pdf_bytes, "text/plain"))], data={"target_lang": "en"})
    assert r.status_code == 400 and ".pdf" in r.json()["detail"]
    r = client.post("/api/projects", data={"target_lang": "en"})
    assert r.status_code == 400
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf"))], data={"target_lang": "xx"})
    assert r.status_code == 400 and "language" in r.json()["detail"]
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf"))],
                    data={"target_lang": "zh", "source_lang": "zh"})
    assert r.status_code == 400 and "differ" in r.json()["detail"]
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf"))],
                    data={"target_lang": "en", "glossary_id": "deadbeef0000"})
    assert r.status_code == 400 and "glossary" in r.json()["detail"]
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf"))],
                    data={"target_lang": "en", "bilingual": "maybe"})
    assert r.status_code == 400 and "bilingual" in r.json()["detail"]
    # a corrupt file with a PDF header is rejected too, and nothing is left behind
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf")),
                                            ("files", ("b.pdf", b"%PDF-1.7 garbage", "application/pdf"))],
                    data={"target_lang": "en"})
    assert r.status_code == 400 and "b.pdf" in r.json()["detail"]
    assert client.get("/api/projects").json() == []


def test_upload_size_limit_from_settings(make_client, pdf_bytes):
    class TinySettings(Settings):
        max_upload_mb: int = 0

    client = make_client(settings=TinySettings())
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf"))], data={"target_lang": "en"})
    assert r.status_code == 413


def test_get_project_after_sync_run(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    pid = _upload(client, pdf_bytes, source_lang="zh", bilingual="true")["projects"][0]["id"]
    r = client.get(f"/api/projects/{pid}")
    assert r.status_code == 200
    p = r.json()
    assert p["status"] == "completed" and p["progress"]["percent"] == 100 and p["progress"]["stage"] == "done"
    assert p["source_lang"] == "zh" and p["target_lang"] == "en" and p["page_count"] == 2
    assert p["result"]["status"] == "completed" and p["result"]["qa_report"]["passed"] is True
    assert p["qa"] == {"passed": True, "rounds": 1, "errors": 0, "warnings": 0, "summary": "QA passed"}
    assert p["downloads"] == {"pdf": True, "bilingual": True, "docx": False, "segments": True}
    assert p["preview_pages"] == 1 and p["current_run"] and p["history"] == []
    assert p["started_at"] and p["finished_at"] and p["download_requires_force"] is False
    call = runner.calls[0]
    assert call["source"].name == "source.pdf" and call["out_dir"].name == p["current_run"]
    assert call["settings"] is client.app.state.settings
    assert client.get("/api/projects/" + "0" * 32).status_code == 404


def test_options_parsed_from_form(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    gid = client.post("/api/glossaries", data={"text": "zh,en\n斜边,hypotenuse side\n", "name": "mine"}).json()["id"]
    _upload(client, pdf_bytes, target_lang="ja", source_lang="auto", glossary_id=gid, translate_images="0",
            bilingual="false", export_docx="1", require_qa_pass="False", max_qa_rounds="5")
    opts: PipelineOptions = runner.calls[0]["options"]
    assert opts.target_lang is Lang.JA and opts.source_lang is None
    assert opts.translate_images is False and opts.bilingual is False and opts.export_docx is True
    assert opts.require_qa_pass is False and opts.max_qa_rounds == 5
    assert opts.glossary is not None and opts.glossary.id == gid and opts.glossary.entries[0].terms["en"] == "hypotenuse side"
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf"))],
                    data={"target_lang": "en", "max_qa_rounds": "99"})
    assert r.status_code == 400


def test_ocr_engine_option_is_parsed_and_validated(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    pid = _upload(client, pdf_bytes, ocr_engine="claude")["projects"][0]["id"]
    assert runner.calls[0]["options"].ocr_engine == "claude"
    assert _upload(client, pdf_bytes)["projects"][0]["options"]["ocr_engine"] == "auto"
    r = client.post("/api/projects", files=[("files", ("a.pdf", pdf_bytes, "application/pdf"))],
                    data={"target_lang": "en", "ocr_engine": "tesseract"})
    assert r.status_code == 400 and "ocr_engine" in r.text
    r = client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja", "options": {"ocr_engine": "none"}})
    assert r.status_code == 202, r.text
    assert r.json()["options"]["ocr_engine"] == "none" and runner.calls[-1]["options"].ocr_engine == "none"
    r = client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja", "options": {"ocr_engine": "x"}})
    assert r.status_code == 400


# --------------------------------------------------------------------------- #
# QA / preview / download
# --------------------------------------------------------------------------- #


def test_qa_report_json_and_markdown(make_client, pdf_bytes):
    client = make_client(FakeRunner(fail_qa=True))
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    r = client.get(f"/api/projects/{pid}/qa")
    assert r.status_code == 200
    rep = r.json()
    assert rep["passed"] is False and rep["errors"] == 1 and rep["final_issues"][0]["check"] == "untranslated"
    r = client.get(f"/api/projects/{pid}/qa", params={"format": "md"})
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/markdown")
    assert "untranslated" in r.text and "p0_b0" in r.text
    assert client.get(f"/api/projects/{pid}/qa", params={"format": "xml"}).status_code == 400


def test_qa_report_missing_before_run(make_client, pdf_bytes):
    client = make_client(FakeRunner(raise_error=True))
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    assert client.get(f"/api/projects/{pid}/qa").status_code == 404


def test_preview_png(make_client, pdf_bytes):
    client = make_client()
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    r = client.get(f"/api/projects/{pid}/preview/1")
    assert r.status_code == 200 and r.headers["content-type"] == "image/png"
    assert r.content.startswith(b"\x89PNG")
    assert client.get(f"/api/projects/{pid}/preview/2").status_code == 404
    assert client.get(f"/api/projects/{pid}/preview/0").status_code == 404


def test_download_formats(make_client, pdf_bytes):
    client = make_client()
    pid = _upload(client, pdf_bytes, names=("教材 第一册.pdf",), bilingual="true", export_docx="true")["projects"][0]["id"]
    r = client.get(f"/api/projects/{pid}/download", params={"format": "pdf"})
    assert r.status_code == 200 and r.headers["content-type"] == "application/pdf"
    assert r.content.startswith(b"%PDF") and "_en.pdf" in r.headers["content-disposition"]
    r = client.get(f"/api/projects/{pid}/download", params={"format": "bilingual"})
    assert r.status_code == 200 and "_bilingual.pdf" in r.headers["content-disposition"]
    r = client.get(f"/api/projects/{pid}/download", params={"format": "docx"})
    assert r.status_code == 200 and r.headers["content-type"].startswith("application/vnd.openxmlformats")
    r = client.get(f"/api/projects/{pid}/download", params={"format": "segments"})
    assert r.status_code == 200 and r.headers["content-type"].startswith("application/json")
    assert r.json()["segments"][0]["translated_text"] == "Pythagorean theorem"
    assert client.get(f"/api/projects/{pid}/download", params={"format": "xlsx"}).status_code == 400
    # outputs that were not requested do not exist
    pid2 = _upload(client, pdf_bytes)["projects"][0]["id"]
    assert client.get(f"/api/projects/{pid2}/download", params={"format": "docx"}).status_code == 404


def test_qa_failed_download_refused_unless_forced(make_client, pdf_bytes):
    client = make_client(FakeRunner(fail_qa=True))
    p = _upload(client, pdf_bytes)["projects"][0]
    assert p["status"] == "qa_failed" and p["download_requires_force"] is True
    r = client.get(f"/api/projects/{p['id']}/download", params={"format": "pdf"})
    assert r.status_code == 409 and "force=1" in r.json()["detail"]
    r = client.get(f"/api/projects/{p['id']}/download", params={"format": "pdf", "force": "1"})
    assert r.status_code == 200 and r.content.startswith(b"%PDF")
    r = client.get(f"/api/projects/{p['id']}/download", params={"format": "segments", "force": "true"})
    assert r.status_code == 200


# --------------------------------------------------------------------------- #
# Retranslate / glossaries / delete / ids
# --------------------------------------------------------------------------- #


def test_retranslate_creates_new_run_and_keeps_history(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    first = _upload(client, pdf_bytes, bilingual="true")["projects"][0]
    gid = client.post("/api/glossaries", data={"text": "zh,pt\n斜边,hipotenusa\n"}).json()["id"]
    r = client.post(f"/api/projects/{first['id']}/retranslate",
                    json={"target_lang": "pt", "glossary_id": gid, "options": {"bilingual": False, "max_qa_rounds": 2}})
    assert r.status_code == 202, r.text
    p = r.json()
    assert p["status"] == "completed" and p["target_lang"] == "pt" and p["glossary_id"] == gid
    assert p["current_run"] != first["current_run"]
    assert len(p["history"]) == 1
    old = p["history"][0]
    assert old["run_id"] == first["current_run"] and old["target_lang"] == "en" and old["status"] == "completed"
    assert old["qa"]["passed"] is True
    # what the archived run directory holds (never server paths), like a project view's "downloads"
    assert old["outputs"] == {"pdf": True, "bilingual": True, "docx": False, "segments": True}
    assert old["preview_pages"] == 1
    assert p["options"]["bilingual"] is False and p["options"]["max_qa_rounds"] == 2
    assert p["downloads"]["bilingual"] is False and p["downloads"]["pdf"] is True
    assert len(runner.calls) == 2 and runner.calls[1]["options"].target_lang is Lang.PT
    assert runner.calls[1]["options"].glossary.id == gid
    # old run directory is kept on disk
    store: ProjectStore = client.app.state.store
    assert (store.run_dir(p["id"], old["run_id"]) / "output.pdf").is_file()
    # validation
    assert client.post(f"/api/projects/{p['id']}/retranslate", json={"target_lang": "pt", "options": {"model": "x"}}).status_code == 400
    assert client.post(f"/api/projects/{p['id']}/retranslate", json={"target_lang": "klingon"}).status_code == 400
    assert client.post(f"/api/projects/{p['id']}/retranslate", json={}).status_code == 400
    assert client.post("/api/projects/" + "f" * 32 + "/retranslate", json={"target_lang": "en"}).status_code == 404


def test_previous_runs_remain_viewable_and_downloadable(make_client, pdf_bytes):
    """After a re-translation the previous run's outputs, QA report and previews are still
    served (``?run=<run_id>`` from the history), judged by that run's own status."""

    class StampedRunner(FakeRunner):
        """QA fails for Korean targets; output.pdf is stamped with the target language so the runs differ."""

        def _run(self, source_pdf, out_dir, options, settings, progress):
            self.fail_qa = options.target_lang is Lang.KO
            result = super()._run(source_pdf, out_dir, options, settings, progress)
            with open(Path(out_dir) / "output.pdf", "ab") as fh:
                fh.write(f"\n%target={options.target_lang.value}\n".encode())
            return result

    client = make_client(StampedRunner())
    store: ProjectStore = client.app.state.store
    first = _upload(client, pdf_bytes, bilingual="true")["projects"][0]
    pid, en_run = first["id"], first["current_run"]
    url = f"/api/projects/{pid}"
    r = client.post(f"{url}/retranslate", json={"target_lang": "ko", "options": {"bilingual": False}})
    assert r.status_code == 202, r.text
    p = r.json()
    ko_run = p["current_run"]
    assert p["status"] == "qa_failed" and p["downloads"]["bilingual"] is False and ko_run != en_run
    old = p["history"][0]
    assert old["run_id"] == en_run and old["status"] == "completed" and old["target_lang"] == "en"
    assert old["outputs"] == {"pdf": True, "bilingual": True, "docx": False, "segments": True}
    assert old["preview_pages"] == 1
    # the previous run's PDF is served with ?run= and is the old file, not the current one
    r = client.get(f"{url}/download", params={"format": "pdf", "run": en_run})
    assert r.status_code == 200 and r.headers["content-type"] == "application/pdf"
    assert r.content == (store.run_dir(pid, en_run) / "output.pdf").read_bytes()
    assert r.content != (store.run_dir(pid, ko_run) / "output.pdf").read_bytes()
    assert "_en.pdf" in r.headers["content-disposition"]
    # ... without force, since that run passed QA, while the current (QA-failed) run still needs it
    assert client.get(f"{url}/download", params={"format": "pdf"}).status_code == 409
    r = client.get(f"{url}/download", params={"format": "pdf", "force": "1"})
    assert r.status_code == 200 and "_ko.pdf" in r.headers["content-disposition"]
    assert r.content == (store.run_dir(pid, ko_run) / "output.pdf").read_bytes()
    # outputs only the previous run produced
    r = client.get(f"{url}/download", params={"format": "bilingual", "run": en_run})
    assert r.status_code == 200 and "_en_bilingual.pdf" in r.headers["content-disposition"]
    assert client.get(f"{url}/download", params={"format": "bilingual", "force": "1"}).status_code == 404
    assert client.get(f"{url}/download", params={"format": "docx", "run": en_run}).status_code == 404
    r = client.get(f"{url}/download", params={"format": "segments", "run": en_run})
    assert r.status_code == 200 and r.json()["target_lang"] == "en"
    # QA report (JSON and markdown) and previews of the previous run
    assert client.get(f"{url}/qa").json()["passed"] is False
    r = client.get(f"{url}/qa", params={"run": en_run})
    assert r.status_code == 200 and r.json()["passed"] is True
    r = client.get(f"{url}/qa", params={"run": en_run, "format": "md"})
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/markdown") and r.text.strip()
    r = client.get(f"{url}/preview/1", params={"run": en_run})
    assert r.status_code == 200 and r.headers["content-type"] == "image/png" and r.content.startswith(b"\x89PNG")
    assert client.get(f"{url}/preview/2", params={"run": en_run}).status_code == 404
    # the current run's id and an empty run address the current run (the UI's preview URLs carry it)
    for run in (ko_run, ""):
        assert client.get(f"{url}/download", params={"format": "pdf", "force": "1", "run": run}).status_code == 200
        assert client.get(f"{url}/preview/1", params={"run": run}).status_code == 200
        assert client.get(f"{url}/qa", params={"run": run}).json()["passed"] is False
    # unknown and malformed run ids are 404 everywhere (never turned into a path)
    for bad in ("0" * 16, "../x", "..%2F..%2Fsource.pdf", en_run.upper(), "x" * 16, en_run + "/../" + ko_run):
        assert client.get(f"{url}/download", params={"format": "pdf", "force": "1", "run": bad}).status_code == 404, bad
        assert client.get(f"{url}/qa", params={"run": bad}).status_code == 404, bad
        assert client.get(f"{url}/preview/1", params={"run": bad}).status_code == 404, bad
    # a QA-failed previous run needs force=1 like the current one, and its file name carries its language
    r = client.post(f"{url}/retranslate", json={"target_lang": "en"})
    assert r.status_code == 202 and r.json()["status"] == "completed"
    assert [h["run_id"] for h in r.json()["history"]] == [en_run, ko_run]
    assert r.json()["history"][1]["status"] == "qa_failed"
    r = client.get(f"{url}/download", params={"format": "pdf", "run": ko_run})
    assert r.status_code == 409 and "force=1" in r.json()["detail"]
    r = client.get(f"{url}/download", params={"format": "pdf", "run": ko_run, "force": "1"})
    assert r.status_code == 200 and "_ko.pdf" in r.headers["content-disposition"]
    assert r.content == (store.run_dir(pid, ko_run) / "output.pdf").read_bytes()
    assert client.get(f"{url}/download", params={"format": "pdf"}).status_code == 200  # the current run passed
    assert client.get(f"{url}/qa", params={"run": ko_run}).json()["passed"] is False
    assert client.get(f"{url}/qa", params={"run": en_run}).json()["passed"] is True
    # store level: the run id is validated before it becomes a path
    with pytest.raises(ValueError):
        store.run_file(store.get(pid), "pdf", run_id="../x")
    assert store.find_run(store.get(pid), "0" * 16) is None and store.find_run(store.get(pid), ko_run)["status"] == "qa_failed"


def test_legacy_history_entries_with_server_paths_are_normalised(make_client, pdf_bytes):
    """Records written before ``outputs`` became booleans hold the pipeline's absolute paths:
    the API reports what is on disk instead and still serves the run."""
    client = make_client()
    store: ProjectStore = client.app.state.store
    first = _upload(client, pdf_bytes, bilingual="true")["projects"][0]
    pid, en_run = first["id"], first["current_run"]
    assert client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja", "options": {"bilingual": False}}).status_code == 202
    project = store.get(pid)
    old_dir = store.run_dir(pid, en_run)
    project.history[0]["outputs"] = {"pdf": str(old_dir / "output.pdf"), "bilingual": str(old_dir / "bilingual.pdf"),
                                     "docx": None, "segments": str(old_dir / "segments.json")}
    del project.history[0]["preview_pages"]
    project.history.append({"run_id": "not a run id", "target_lang": "ko", "status": "error", "outputs": {}})
    store.update(project)
    p = client.get(f"/api/projects/{pid}").json()
    assert p["history"][0]["outputs"] == {"pdf": True, "bilingual": True, "docx": False, "segments": True}
    assert p["history"][0]["preview_pages"] == 1
    assert p["history"][1]["outputs"] == {"pdf": False, "bilingual": False, "docx": False, "segments": False}
    assert p["history"][1]["preview_pages"] == 0
    assert not any(isinstance(v, str) for h in p["history"] for v in h["outputs"].values())
    assert str(old_dir) not in client.get(f"/api/projects/{pid}").text
    r = client.get(f"/api/projects/{pid}/download", params={"format": "bilingual", "run": en_run})
    assert r.status_code == 200 and "_en_bilingual.pdf" in r.headers["content-disposition"]
    assert client.get(f"/api/projects/{pid}/download", params={"format": "pdf", "run": "not a run id"}).status_code == 404
    # the view never rewrites the stored record
    assert store.get(pid).history[0]["outputs"]["pdf"] == str(old_dir / "output.pdf")


def test_glossary_upload_list_and_template(make_client):
    client = make_client()
    r = client.get("/api/glossaries")
    assert r.status_code == 200 and r.json()[0]["id"] == "default" and r.json()[0]["entries"] > 50
    r = client.post("/api/glossaries", files={"file": ("terms.csv", "zh,en,note\n斜边,hypotenuse,x\n直角,right angle,\n".encode(), "text/csv")})
    assert r.status_code == 201, r.text
    g = r.json()
    assert g["entries"] == 2 and g["name"] == "terms" and g["id"] != "default"
    r = client.post("/api/glossaries", json={"text": "zh\ten\n三角形\ttriangle\n", "name": "tsv"})
    assert r.status_code == 201 and r.json()["entries"] == 1 and r.json()["name"] == "tsv"
    r = client.post("/api/glossaries", files={"file": ("g.json", '[{"zh": "面积", "en": "area"}]'.encode(), "application/json")})
    assert r.status_code == 201 and r.json()["entries"] == 1
    ids = [x["id"] for x in client.get("/api/glossaries").json()]
    assert ids[0] == "default" and g["id"] in ids and len(ids) == 4
    assert client.post("/api/glossaries", data={"text": "   "}).status_code == 400
    assert client.post("/api/glossaries", data={"text": "foo,bar\n1,2\n"}).status_code == 400
    assert client.post("/api/glossaries", json={"text": "{not json"}).status_code == 400
    r = client.get("/api/glossaries/template")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/csv")
    assert r.text.startswith("zh,en,pt,es,ja,ko,note") and "glossary_template.csv" in r.headers["content-disposition"]


def test_delete_project(make_client, pdf_bytes):
    client = make_client()
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    store: ProjectStore = client.app.state.store
    assert store.project_dir(pid).is_dir()
    r = client.delete(f"/api/projects/{pid}")
    assert r.status_code == 200 and r.json() == {"deleted": pid}
    assert not store.project_dir(pid).exists()
    assert client.get(f"/api/projects/{pid}").status_code == 404
    assert client.delete(f"/api/projects/{pid}").status_code == 404
    assert client.get("/api/projects").json() == []


def test_project_id_traversal_is_rejected(make_client, pdf_bytes):
    client = make_client()
    _upload(client, pdf_bytes)
    for bad in ("..%2F..%2Fetc%2Fpasswd", "..", "%2e%2e", "ZZZZZZZZZZZZZZZZ", "abc", "0" * 32 + "%00"):
        assert client.get(f"/api/projects/{bad}").status_code == 404, bad
        assert client.get(f"/api/projects/{bad}/qa").status_code == 404, bad
        assert client.get(f"/api/projects/{bad}/preview/1").status_code == 404, bad
        assert client.get(f"/api/projects/{bad}/download").status_code == 404, bad
        assert client.delete(f"/api/projects/{bad}").status_code == 404, bad
    store: ProjectStore = client.app.state.store
    with pytest.raises(ValueError):
        store.project_dir("../../etc")
    with pytest.raises(ProjectNotFound):
        store.get("a" * 32)
    assert client.get(f"/api/projects/{store.list()[0].id}").status_code == 200


# --------------------------------------------------------------------------- #
# Failure handling and background execution
# --------------------------------------------------------------------------- #


def test_runner_exception_becomes_error_status(make_client, pdf_bytes):
    client = make_client(FakeRunner(raise_error=True))
    p = _upload(client, pdf_bytes)["projects"][0]
    assert p["status"] == "error" and "runner exploded" in p["error"]
    assert p["progress"]["stage"] == "error" and p["result"] is None
    r = client.get(f"/api/projects/{p['id']}/download", params={"format": "pdf"})
    assert r.status_code == 409
    # a retranslate is allowed after an error and records the failed run in the history
    client2 = make_client(FakeRunner())
    r = client2.post(f"/api/projects/{p['id']}/retranslate", json={"target_lang": "ko"})
    assert r.status_code == 202 and r.json()["status"] == "completed"
    failed = r.json()["history"][0]
    assert failed["status"] == "error" and failed["preview_pages"] == 0
    assert failed["outputs"] == {"pdf": False, "bilingual": False, "docx": False, "segments": False}
    # the failed previous run is refused like a failed current run would be
    r = client2.get(f"/api/projects/{p['id']}/download", params={"format": "pdf", "run": failed["run_id"]})
    assert r.status_code == 409 and "runner exploded" in r.json()["detail"]
    assert client2.get(f"/api/projects/{p['id']}/qa", params={"run": failed["run_id"]}).status_code == 404
    assert client2.get(f"/api/projects/{p['id']}/preview/1", params={"run": failed["run_id"]}).status_code == 404
    assert client2.get(f"/api/projects/{p['id']}/download", params={"format": "pdf"}).status_code == 200


def test_runner_error_result(make_client, pdf_bytes):
    client = make_client(FakeRunner(error_result=True))
    p = _upload(client, pdf_bytes)["projects"][0]
    assert p["status"] == "error" and "Source language" in p["error"]


def test_background_execution_with_thread_pool(make_client, pdf_bytes):
    runner = FakeRunner(delay=0.3)
    client = make_client(runner, sync=False)
    res = _upload(client, pdf_bytes, names=("a.pdf", "b.pdf"))
    assert {p["status"] for p in res["projects"]} <= {"queued", "running"}
    deadline = time.time() + 15
    while time.time() < deadline:
        projects = client.get("/api/projects").json()
        if all(p["status"] == "completed" for p in projects):
            break
        time.sleep(0.1)
    projects = client.get("/api/projects").json()
    assert [p["status"] for p in projects] == ["completed", "completed"]
    assert all(p["progress"]["percent"] == 100 for p in projects)
    assert len(runner.calls) == 2


# --------------------------------------------------------------------------- #
# Store-level behaviour
# --------------------------------------------------------------------------- #


def test_store_concurrent_updates_keep_project_json_valid(tmp_path, pdf_bytes):
    store = ProjectStore(tmp_path / "data")
    project = store.create("book.pdf", pdf_bytes, PipelineOptions(target_lang=Lang.EN), batch_id="abc123")
    errors: list[Exception] = []

    def writer(n: int) -> None:
        try:
            for i in range(40):
                store.set_progress(project, "translate", f"writer {n} step {i}", i)
        except Exception as exc:  # pragma: no cover - reported through the assertion below
            errors.append(exc)

    def reader() -> None:
        try:
            for _ in range(80):
                store.get(project.id)
        except Exception as exc:  # pragma: no cover
            errors.append(exc)

    threads = [threading.Thread(target=writer, args=(n,)) for n in range(4)] + [threading.Thread(target=reader)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert errors == []
    data = json.loads((store.project_dir(project.id) / "project.json").read_text(encoding="utf-8"))
    assert data["id"] == project.id and data["progress"]["stage"] == "translate"
    assert not list(store.project_dir(project.id).glob("*.tmp"))


def test_store_recovers_interrupted_jobs(tmp_path, pdf_bytes):
    store = ProjectStore(tmp_path / "data")
    p1 = store.create("a.pdf", pdf_bytes, {"target_lang": "en"})
    p2 = store.create("b.pdf", pdf_bytes, {"target_lang": "ja", "source_lang": "zh"})
    store.mark_running(p2)
    assert store.get(p2.id).status == "running" and store.get(p2.id).source_lang is Lang.ZH
    recovered = ProjectStore(tmp_path / "data").recover_interrupted()
    assert set(recovered) == {p1.id, p2.id}
    assert all(p.status == "error" and "Interrupted" in (p.error or "") for p in store.list())
    # pipeline options are rebuilt from the stored dict
    opts = store.pipeline_options(store.get(p2.id))
    assert opts.target_lang is Lang.JA and opts.source_lang is Lang.ZH and opts.glossary is None


# --------------------------------------------------------------------------- #
# Adversarial edge cases: malformed input, hostile names, unusual PDFs, races
# --------------------------------------------------------------------------- #


def test_malformed_glossary_bodies_are_rejected(make_client):
    client = make_client()
    before = len(client.get("/api/glossaries").json())
    # JSON shapes the parser does not understand must give 400, never a server error
    for text in ('{"a": 1}', "[1, 2]", '{"entries": 5}', '[{"terms": 5}]', '{"entries": [{"terms": "oops"}]}',
                 '"just a string"', "null", "[]", "{}"):
        r = client.post("/api/glossaries", json={"text": text})
        assert r.status_code == 400, (text, r.status_code, r.text)
        assert r.json()["detail"]
    assert client.post("/api/glossaries", json={"text": "zh,en\n斜边,hypotenuse\n", "name": ["x"]}).status_code == 400
    assert client.post("/api/glossaries", json={"text": 42}).status_code == 400
    assert client.post("/api/glossaries", json=[1, 2]).status_code == 400
    assert client.post("/api/glossaries", content=b"\xff\xfe", headers={"content-type": "application/json"}).status_code == 400
    # uploads: not UTF-8, empty, binary junk with a .json name
    assert client.post("/api/glossaries", files={"file": ("g.csv", b"zh,en\n\xff\xfe\xfd,x\n", "text/csv")}).status_code == 400
    assert client.post("/api/glossaries", files={"file": ("g.csv", b"", "text/csv")}).status_code == 400
    assert client.post("/api/glossaries", files={"file": ("g.json", b"zh,en\n\xe6\x96\x9c,hyp\n", "application/json")}).status_code == 400
    assert client.post("/api/glossaries", content=b"zh,en\n", headers={"content-type": "text/plain"}).status_code == 400
    assert len(client.get("/api/glossaries").json()) == before
    # a padded / over-long name is normalised, a glossary object body is accepted
    r = client.post("/api/glossaries", json={"text": "zh,en\n斜边,hypotenuse\n", "name": "  my   terms  " + "x" * 500})
    assert r.status_code == 201 and r.json()["name"].startswith("my terms x") and len(r.json()["name"]) <= 120
    r = client.post("/api/glossaries", json={"id": "default", "name": "posted", "entries": [{"terms": {"zh": "面积", "en": "area"}}]})
    assert r.status_code == 201 and r.json()["id"] != "default" and r.json()["entries"] == 1
    assert client.app.state.store.get_glossary(r.json()["id"]).entries[0].terms["en"] == "area"


def test_validation_errors_are_json_even_with_exception_context(make_client, pdf_bytes):
    client = make_client()
    # `files` given as a plain form string: pydantic puts a ValueError *object* in the error ctx
    r = client.post("/api/projects", data={"files": "x", "target_lang": "en"})
    assert r.status_code == 400
    body = r.json()
    assert body["detail"] == "invalid request" and body["errors"][0]["loc"] == ["body", "files", 0]
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    assert client.get(f"/api/projects/{pid}/preview/abc").status_code == 400
    assert client.get(f"/api/projects/{pid}/preview/-1").status_code == 404
    assert client.get(f"/api/projects/{pid}/preview/99999999999999999999").status_code == 404
    r = client.post(f"/api/projects/{pid}/retranslate", content=b"{bad", headers={"content-type": "application/json"})
    assert r.status_code == 400 and r.json()["errors"][0]["type"] == "json_invalid"
    assert client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja", "options": "x"}).status_code == 400
    assert client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": 123}).status_code == 400
    assert client.get(f"/api/projects/{pid}/download", params={"format": "pdf", "force": "maybe"}).status_code == 400
    assert client.delete(f"/api/projects/{pid}", params={"force": "sure"}).status_code == 400
    assert client.get(f"/api/projects/{pid}").status_code == 200  # nothing above changed the project


def test_retranslate_option_values_are_validated(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    url = f"/api/projects/{pid}/retranslate"
    for opts in ({"max_qa_rounds": 0}, {"max_qa_rounds": 11}, {"max_qa_rounds": True}, {"max_qa_rounds": 2.5},
                 {"max_qa_rounds": "many"}, {"max_qa_rounds": -3}, {"bilingual": "maybe"}, {"bilingual": 2},
                 {"export_docx": [True]}, {"translate_images": {"on": True}}, {"min_font_scale": 0.1}):
        r = client.post(url, json={"target_lang": "ja", "options": opts})
        assert r.status_code == 400, (opts, r.text)
    assert len(runner.calls) == 1  # nothing was queued
    p = client.get(f"/api/projects/{pid}").json()
    assert p["status"] == "completed" and p["history"] == [] and p["options"]["max_qa_rounds"] == 3
    # boundary values and JSON / string spellings are accepted; null keeps the current value
    r = client.post(url, json={"target_lang": "ja", "options": {"max_qa_rounds": 10, "bilingual": "yes",
                                                                "require_qa_pass": False, "export_docx": None}})
    assert r.status_code == 202, r.text
    o = r.json()["options"]
    assert o["max_qa_rounds"] == 10 and o["bilingual"] is True and o["require_qa_pass"] is False and o["export_docx"] is False
    r = client.post(url, json={"target_lang": "ko", "source_lang": "auto", "options": {"max_qa_rounds": "1"}})
    assert r.status_code == 202 and r.json()["source_lang"] is None
    assert r.json()["options"]["max_qa_rounds"] == 1 and r.json()["options"]["bilingual"] is True  # inherited
    assert len(r.json()["history"]) == 2 and runner.calls[-1]["options"].max_qa_rounds == 1


def test_batch_listing_is_newest_first_and_stable(make_client, pdf_bytes):
    client = make_client()
    names = tuple(f"vol{i}.pdf" for i in range(6))
    res = _upload(client, pdf_bytes, names=names)
    created_order = [p["name"] for p in res["projects"]]
    assert created_order == [n[:-4] for n in names]
    stamps = [p["created_at"] for p in res["projects"]]
    assert stamps == sorted(stamps) and len(set(stamps)) == len(stamps)
    listed = [p["name"] for p in client.get("/api/projects").json()]
    assert listed == created_order[::-1]
    for _ in range(3):
        assert [p["name"] for p in client.get("/api/projects").json()] == listed
    newer = _upload(client, pdf_bytes, names=("latest.pdf",))["projects"][0]
    assert client.get("/api/projects").json()[0]["id"] == newer["id"]
    # every write bumps updated_at (the UI polls for that)
    p = client.get(f"/api/projects/{newer['id']}").json()
    assert p["updated_at"] > p["created_at"]


def test_force_delete_while_running_leaves_no_orphan_directory(make_client, pdf_bytes):
    runner = FakeRunner(delay=0.8)
    client = make_client(runner, sync=False)
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    store: ProjectStore = client.app.state.store
    deadline = time.time() + 10
    while time.time() < deadline and client.get(f"/api/projects/{pid}").json()["status"] != "running":
        time.sleep(0.02)
    assert client.get(f"/api/projects/{pid}").json()["status"] == "running"
    assert client.delete(f"/api/projects/{pid}").status_code == 409  # busy
    assert client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja"}).status_code == 409
    assert client.delete(f"/api/projects/{pid}", params={"force": "1"}).status_code == 200
    assert client.get(f"/api/projects/{pid}").status_code == 404
    assert runner.finished.wait(10)
    deadline = time.time() + 5
    while time.time() < deadline and store.project_dir(pid).exists():
        time.sleep(0.02)
    assert not store.project_dir(pid).exists()
    assert client.get("/api/projects").json() == []


def test_corrupt_project_record_is_reported_not_crashing(make_client, pdf_bytes):
    client = make_client()
    pid = _upload(client, pdf_bytes)["projects"][0]["id"]
    other = _upload(client, pdf_bytes)["projects"][0]["id"]
    store: ProjectStore = client.app.state.store
    (store.project_dir(pid) / "project.json").write_text("{not json", encoding="utf-8")
    r = client.get(f"/api/projects/{pid}")
    assert r.status_code == 500 and "unreadable" in r.json()["detail"]
    assert client.get(f"/api/projects/{pid}/download", params={"format": "pdf"}).status_code == 500
    assert [p["id"] for p in client.get("/api/projects").json()] == [other]
    with pytest.raises(ProjectUnreadable):
        store.get(pid)
    # a record with the wrong shape, and a directory without any record, are skipped too
    (store.project_dir(pid) / "project.json").write_text('{"id": "x"}', encoding="utf-8")
    (store.projects_dir / ("e" * 32)).mkdir()
    assert [p["id"] for p in client.get("/api/projects").json()] == [other]
    assert client.get(f"/api/projects/{'e' * 32}").status_code == 404
    assert client.delete(f"/api/projects/{'e' * 32}").status_code == 404


def test_unusual_pdfs_are_rejected_cleanly(make_client, pdf_bytes):
    client = make_client()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        encrypted = doc.tobytes(encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="secret", owner_pw="owner")
    for name, data, hint in (("encrypted.pdf", encrypted, "password"), ("empty.pdf", b"", "%PDF"),
                             ("header-only.pdf", b"%PDF-1.7\n", ""), ("junk.pdf", b"%PDF-1.4\n" + b"\x00" * 4096, "")):
        r = client.post("/api/projects", files=[("files", (name, data, "application/pdf"))], data={"target_lang": "en"})
        assert r.status_code == 400, (name, r.status_code, r.text)
        assert name in r.json()["detail"] and hint in r.json()["detail"]
    # all-or-nothing: a good file followed by a bad one creates nothing
    r = client.post("/api/projects", files=[("files", ("good.pdf", pdf_bytes, "application/pdf")),
                                            ("files", ("encrypted.pdf", encrypted, "application/pdf"))],
                    data={"target_lang": "en"})
    assert r.status_code == 400 and "encrypted.pdf" in r.json()["detail"]
    assert client.get("/api/projects").json() == []
    store: ProjectStore = client.app.state.store
    assert list(store.projects_dir.iterdir()) == []
    # too many files
    r = client.post("/api/projects", files=[("files", (f"f{i}.pdf", b"%PDF-", "application/pdf")) for i in range(51)],
                    data={"target_lang": "en"})
    assert r.status_code == 400 and "50" in r.json()["detail"]


def test_unicode_and_hostile_filenames(make_client, pdf_bytes):
    client = make_client()
    res = _upload(client, pdf_bytes, names=("../../etc/数学 教材 (第1册).pdf", "C:\\Users\\me\\Übung.PDF", "   .pdf",
                                             "weird\x7fname.pdf"))
    assert [p["name"] for p in res["projects"]] == ["数学 教材 (第1册)", "Übung", "document", "weirdname"]
    # control characters and directories never reach the stored name (httpx encodes \x01 itself, so test directly)
    assert safe_name("..\\..\\weird\x01na\nme\t.PDF") == "weirdname" and safe_name("\x00\x01") == "document"
    store: ProjectStore = client.app.state.store
    assert all(store.project_dir(p["id"]).is_dir() for p in res["projects"])
    assert all(len(store.project_dir(p["id"]).relative_to(store.projects_dir).parts) == 1 for p in res["projects"])
    pid = res["projects"][0]["id"]
    r = client.get(f"/api/projects/{pid}/download", params={"format": "pdf"})
    assert r.status_code == 200
    cd = r.headers["content-disposition"]
    assert cd.startswith("attachment;") and "filename*=utf-8''" in cd and "%E6%95%B0%E5%AD%A6" in cd
    assert "\n" not in cd and "\r" not in cd
    r = client.get(f"/api/projects/{res['projects'][1]['id']}/download", params={"format": "pdf"})
    assert r.status_code == 200 and "bung_en.pdf" in r.headers["content-disposition"]


def test_runner_returning_garbage_marks_project_error(make_client, pdf_bytes):
    class GarbageRunner:
        def __init__(self, value):
            self.value = value

        def __call__(self, *args, **kwargs):
            return self.value

    for value, hint in ((None, "ValidationError"), ({"status": "weird"}, "ValidationError"), ("done", "ValidationError")):
        client = make_client(GarbageRunner(value))
        p = _upload(client, pdf_bytes)["projects"][0]
        assert p["status"] == "error" and hint in p["error"], (value, p["error"])
        assert p["result"] is None and p["downloads"] == {"pdf": False, "bilingual": False, "docx": False, "segments": False}
    # a well-formed result pointing at files that do not exist: completed, but nothing to download
    client = make_client(GarbageRunner({"status": "completed", "output_pdf": "/nonexistent/output.pdf"}))
    p = _upload(client, pdf_bytes)["projects"][0]
    assert p["status"] == "completed" and p["downloads"]["pdf"] is False and p["qa"] is None
    assert client.get(f"/api/projects/{p['id']}/download", params={"format": "pdf"}).status_code == 404
    assert client.get(f"/api/projects/{p['id']}/qa").status_code == 404
    assert client.get(f"/api/projects/{p['id']}/preview/1").status_code == 404


def test_store_begin_run_is_exclusive_under_concurrency(tmp_path, pdf_bytes):
    store = ProjectStore(tmp_path / "data")
    project = store.create("book.pdf", pdf_bytes, {"target_lang": "en"})
    store.finish(project, PipelineResult(status="completed"))
    results: list[str] = []
    barrier = threading.Barrier(8)

    def worker(lang: str) -> None:
        barrier.wait()
        try:
            store.begin_run(project.id, lang)
            results.append("ok")
        except ProjectBusy:
            results.append("busy")

    threads = [threading.Thread(target=worker, args=(("ja", "ko", "pt", "es")[i % 4],)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(results) == ["busy"] * 7 + ["ok"]
    p = store.get(project.id)
    assert p.status == "queued" and len(p.history) == 1 and p.history[0]["status"] == "completed"
    assert len(list((store.project_dir(project.id) / "runs").iterdir())) == 2
    with pytest.raises(ValueError):
        store.create("x.pdf", pdf_bytes, {"target_lang": "en", "max_qa_rounds": 0})
    # invalid option overrides are refused before anything is persisted
    store.finish(store.get(project.id), PipelineResult(status="error", error="boom"))
    with pytest.raises(ValueError):
        store.begin_run(project.id, "zh", options={"max_qa_rounds": 0})
    after = store.get(project.id)
    assert after.status == "error" and after.target_lang is not Lang.ZH and len(after.history) == 1


# --------------------------------------------------------------------------- #
# Page limit (one upload must not be able to exhaust the shared service)
# --------------------------------------------------------------------------- #


def test_upload_page_limit_from_settings(make_client, pdf_bytes):
    class OnePage(Settings):
        max_pages: int = 1

    files = [("files", ("a.pdf", pdf_bytes, "application/pdf")), ("files", ("b.pdf", pdf_bytes, "application/pdf"))]
    client = make_client(settings=OnePage())
    r = client.post("/api/projects", files=files, data={"target_lang": "en"})
    assert r.status_code == 413, r.text
    assert "pages" in r.json()["detail"] and "a.pdf" in r.json()["detail"] and "1 pages" in r.json()["detail"]
    assert client.get("/api/projects").json() == []  # the batch is all-or-nothing
    assert list(client.app.state.store.projects_dir.iterdir()) == []
    # a project uploaded under a higher limit cannot be re-translated once the limit is below its page count
    default = make_client()  # default limit (500) accepts the 2-page sample
    pid = _upload(default, pdf_bytes)["projects"][0]["id"]
    r = client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja"})
    assert r.status_code == 413 and "pages" in r.json()["detail"]
    p = default.get(f"/api/projects/{pid}").json()
    assert p["status"] == "completed" and p["history"] == [] and p["target_lang"] == "en"  # nothing was queued

    class TwoPages(Settings):
        max_pages: int = 2

    assert make_client(settings=TwoPages()).post("/api/projects", files=files[:1], data={"target_lang": "en"}).status_code == 201


def test_store_page_limit(tmp_path, pdf_bytes):
    store = ProjectStore(tmp_path / "data", max_pages=1)
    with pytest.raises(PdfTooLarge, match="2 pages"):
        store.create("a.pdf", pdf_bytes, {"target_lang": "en"})
    assert list(store.projects_dir.iterdir()) == []
    unlimited = ProjectStore(tmp_path / "data")
    assert unlimited.max_pages is None and ProjectStore(tmp_path / "data", max_pages=0).max_pages is None
    project = unlimited.create("a.pdf", pdf_bytes, {"target_lang": "en"})
    unlimited.finish(project, PipelineResult(status="completed"))
    with pytest.raises(PdfTooLarge):
        store.begin_run(project.id, "ja")
    after = store.get(project.id)
    assert after.status == "completed" and after.history == [] and after.target_lang is Lang.EN
    assert ProjectStore(tmp_path / "data", max_pages=2).begin_run(project.id, "ja").status == "queued"


# --------------------------------------------------------------------------- #
# Access control: cross-site mutations and the optional API token
# --------------------------------------------------------------------------- #


def test_cross_site_mutations_are_rejected(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    evil = {"Origin": "http://evil.example"}
    glossary = {"text": "zh,en\n勾股定理,CSRF-planted\n"}
    files = [("files", ("a.pdf", pdf_bytes, "application/pdf"))]
    r = client.post("/api/glossaries", data=glossary, headers=evil)
    assert r.status_code == 403 and "cross-site" in r.json()["detail"]
    assert client.post("/api/glossaries", data=glossary, headers={"Sec-Fetch-Site": "cross-site"}).status_code == 403
    r = client.post("/api/projects", files=files, data={"target_lang": "en"}, headers=evil)
    assert r.status_code == 403
    assert client.get("/api/projects").json() == [] and runner.calls == []
    assert len(client.get("/api/glossaries").json()) == 1  # nothing was planted
    # the web UI's same-origin fetch and header-less clients (curl, CLI) keep working
    r = client.post("/api/projects", files=files, data={"target_lang": "en"},
                    headers={"Origin": "http://testserver", "Sec-Fetch-Site": "same-origin"})
    assert r.status_code == 201, r.text
    pid = r.json()["projects"][0]["id"]
    assert client.post("/api/glossaries", data=glossary).status_code == 201
    # reads are unaffected (the browser's CORS policy already hides their responses from other origins)
    assert client.get("/api/projects", headers=evil).status_code == 200
    assert client.get(f"/api/projects/{pid}", headers={"Sec-Fetch-Site": "cross-site"}).status_code == 200
    # Origin: null (sandboxed frame, redirect) and cross-site JSON / DELETE requests are refused too
    assert client.delete(f"/api/projects/{pid}", headers={"Origin": "null"}).status_code == 403
    assert client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja"}, headers=evil).status_code == 403
    p = client.get(f"/api/projects/{pid}").json()
    assert p["status"] == "completed" and p["history"] == [] and len(runner.calls) == 1
    assert client.delete(f"/api/projects/{pid}", headers={"Origin": "http://testserver"}).status_code == 200
    # default ports and a reverse proxy's X-Forwarded-Host count as the same site
    assert cross_site_reason({"origin": "http://testserver:80", "host": "testserver"}) is None
    assert cross_site_reason({"origin": "https://Books.example", "host": "10.0.0.5:8000",
                              "x-forwarded-host": "books.example, 10.0.0.5:8000"}) is None
    assert cross_site_reason({"origin": "https://books.example:444", "host": "books.example"})
    assert cross_site_reason({"origin": "http://evil.example", "host": "evil.example.com"})
    assert cross_site_reason({"host": "testserver"}) is None


def test_api_token_required_when_configured(make_client, offline_settings, pdf_bytes):
    client = make_client(settings=offline_settings.model_copy(update={"api_token": "s3cret"}))
    files = [("files", ("a.pdf", pdf_bytes, "application/pdf"))]
    r = client.get("/api/projects")
    assert r.status_code == 401 and r.headers["www-authenticate"] == "Bearer" and "token" in r.json()["detail"]
    assert client.post("/api/projects", files=files, data={"target_lang": "en"}).status_code == 401
    assert client.post("/api/glossaries", data={"text": "zh,en\n斜边,x\n"}).status_code == 401
    for bad in ({"Authorization": "Bearer wrong"}, {"Authorization": "Bearer s3cre"}, {"Authorization": "Basic s3cret"},
                {"X-API-Key": "S3CRET"}, {"Cookie": "mathtrans_token=nope"}):
        assert client.get("/api/projects", headers=bad).status_code == 401, bad
    assert client.get("/").status_code == 200 and client.get("/api/languages").status_code == 200  # UI bootstraps
    ok = {"Authorization": "Bearer s3cret"}
    assert client.get("/api/projects", headers=ok).json() == []
    assert client.get("/api/projects", headers={"X-API-Key": "s3cret"}).status_code == 200
    r = client.post("/api/projects", files=files, data={"target_lang": "en"}, headers=ok)
    assert r.status_code == 201, r.text
    pid = r.json()["projects"][0]["id"]
    # the cookie set by the web UI lets <a href> downloads and <img> previews through (same-origin only)
    assert client.get(f"/api/projects/{pid}/preview/1").status_code == 401
    cookie = {"Cookie": "mathtrans_token=s3cret"}
    assert client.get(f"/api/projects/{pid}/preview/1", headers=cookie).status_code == 200
    assert client.get(f"/api/projects/{pid}/download", params={"format": "pdf"}, headers=cookie).status_code == 200
    # a cross-site form POST never carries the SameSite=Strict cookie, and is refused before the token check anyway
    assert client.post("/api/projects", files=files, data={"target_lang": "en"},
                       headers={"Origin": "http://evil.example", **cookie}).status_code == 403
    assert client.delete(f"/api/projects/{pid}", headers=ok).status_code == 200
    # a blank token means no authentication
    blank = make_client(settings=offline_settings.model_copy(update={"api_token": "   "}))
    assert blank.get("/api/projects").status_code == 200


# --------------------------------------------------------------------------- #
# Glossary ingest bounds (every path: form text, file upload, JSON Glossary object)
# --------------------------------------------------------------------------- #


def test_glossary_name_cap_applies_to_json_object_and_json_file(make_client):
    client = make_client()
    body = {"id": "x", "name": "N" * 1000, "entries": [{"terms": {"zh": "斜边", "en": "hypotenuse"}}]}
    r = client.post("/api/glossaries", json=body)
    assert r.status_code == 201 and len(r.json()["name"]) == MAX_GLOSSARY_NAME_CHARS
    assert len(client.app.state.store.get_glossary(r.json()["id"]).name) == MAX_GLOSSARY_NAME_CHARS
    r = client.post("/api/glossaries", files={"file": ("g.json", json.dumps(body).encode(), "application/json")},
                    data={"name": "short"})
    assert r.status_code == 201 and len(r.json()["name"]) == MAX_GLOSSARY_NAME_CHARS
    assert all(len(g["name"]) <= MAX_GLOSSARY_NAME_CHARS for g in client.get("/api/glossaries").json())
    # a posted object without a name falls back to the form / default name
    r = client.post("/api/glossaries", json={"entries": [{"terms": {"zh": "斜边", "en": "hypotenuse"}}]})
    assert r.status_code == 201 and r.json()["name"].startswith("Custom glossary")


def test_glossary_entry_and_term_caps(make_client):
    client = make_client()

    def entries(n: int) -> list[dict]:
        return [{"terms": {"zh": f"术语{i}", "en": f"term{i}"}} for i in range(n)]

    r = client.post("/api/glossaries", json={"name": "huge", "entries": entries(MAX_GLOSSARY_ENTRIES + 1)})
    assert r.status_code == 413 and "entries" in r.json()["detail"]
    csv_text = "zh,en\n" + "".join(f"术语{i},term{i}\n" for i in range(MAX_GLOSSARY_ENTRIES + 1))
    r = client.post("/api/glossaries", files={"file": ("big.csv", csv_text.encode(), "text/csv")})
    assert r.status_code == 413
    r = client.post("/api/glossaries", json={"name": "max", "entries": entries(MAX_GLOSSARY_ENTRIES)})
    assert r.status_code == 201 and r.json()["entries"] == MAX_GLOSSARY_ENTRIES
    long_term = "x" * (MAX_GLOSSARY_TERM_CHARS + 1)
    r = client.post("/api/glossaries", json={"entries": [{"terms": {"zh": "斜边", "en": long_term}}]})
    assert r.status_code == 400 and "characters" in r.json()["detail"]
    assert client.post("/api/glossaries", data={"text": f"zh,en\n斜边,{long_term}\n"}).status_code == 400
    assert client.post("/api/glossaries", files={"file": ("t.csv", f"zh,en\n斜边,{long_term}\n".encode(), "text/csv")}).status_code == 400
    assert client.post("/api/glossaries", data={"text": f"zh,en\n斜边,{'x' * MAX_GLOSSARY_TERM_CHARS}\n"}).status_code == 201
    assert len(client.get("/api/glossaries").json()) == 3  # default + "max" + the one at the term limit


def test_glossary_json_body_size_limit(make_client):
    class TinySettings(Settings):
        max_upload_mb: int = 0

    client = make_client(settings=TinySettings())
    assert client.post("/api/glossaries", json={"text": "zh,en\n斜边,hypotenuse\n"}).status_code == 413
    r = client.post("/api/glossaries", content=b'{"text": "' + b" " * 4096 + b'"}', headers={"content-type": "application/json"})
    assert r.status_code == 413
    assert client.post("/api/glossaries", files={"file": ("g.csv", b"zh,en\n", "text/csv")}).status_code == 413
    assert len(client.get("/api/glossaries").json()) == 1


# --------------------------------------------------------------------------- #
# Web UI contract (retranslate options, keyboard operability, stable table, forced downloads)
# --------------------------------------------------------------------------- #


def test_retranslate_empty_skip_pages_clears_previous(make_client, pdf_bytes):
    runner = FakeRunner()
    client = make_client(runner)
    pid = _upload(client, pdf_bytes, skip_pages="2")["projects"][0]["id"]
    assert client.get(f"/api/projects/{pid}").json()["options"]["skip_pages"] == [1]
    assert runner.calls[-1]["options"].skip_pages == [1]
    # the web UI sends "" for an emptied field: that clears the stored pages ...
    r = client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ja", "options": {"skip_pages": ""}})
    assert r.status_code == 202, r.text
    assert r.json()["options"]["skip_pages"] is None and runner.calls[-1]["options"].skip_pages is None
    # ... a new specification replaces them, and null keeps the current value (documented contract)
    r = client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "ko", "options": {"skip_pages": "1"}})
    assert r.status_code == 202 and r.json()["options"]["skip_pages"] == [0]
    r = client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "pt", "options": {"skip_pages": None}})
    assert r.status_code == 202 and r.json()["options"]["skip_pages"] == [0]
    assert runner.calls[-1]["options"].skip_pages == [0]
    assert client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "es", "options": {"skip_pages": "0"}}).status_code == 400
    assert client.post(f"/api/projects/{pid}/retranslate", json={"target_lang": "es", "options": {"skip_pages": "x"}}).status_code == 400
    assert len(runner.calls) == 4


def test_index_html_drop_zone_is_keyboard_operable(make_client):
    html = make_client().get("/").text
    drop = re.search(r'<div class="drop" id="drop"([^>]*)>', html).group(1)
    assert 'tabindex="0"' in drop and 'role="button"' in drop and "aria-label=" in drop
    assert '$("drop").addEventListener("keydown"' in html and "fileInput.click()" in html
    assert ".drop:focus-visible" in html  # visible focus indicator
    assert 'label for="file-input"' not in html  # together with the click handler that would open two choosers


def test_index_html_project_table_rendering_is_stable(make_client):
    html = make_client().get("/").text
    render = html.split("function renderProjects()")[1].split("function loadProjects()")[0]
    assert "body.dataset.sig" in render and "updated_at" in render and "state.selected" in render
    assert "document.activeElement" in render and "b.focus()" in render
    assert "setInterval(loadProjects, 2000)" in html  # the poll itself stays


def test_index_html_history_rows_link_to_previous_runs(make_client):
    html = make_client().get("/").text
    # every history row links the outputs the run still holds, its previews and its QA report via ?run=
    assert "historyLinks(p, h)" in html.split('"历史 / History"')[1][:400]
    links = html.split("function historyLinks(p, h)")[1].split("function renderQA(p)")[0]
    assert "download?format=${fmt}&run=${run}" in links and "qa?format=md&run=${run}" in links
    assert "preview/1?run=${run}" in links and "outs[fmt]" in links and "h.preview_pages" in links
    # a QA-failed previous run is downloadable only forced, with the same confirmation as the current run
    assert 'data-force="1"' in links and "&force=1" in links and "forced" in links
    assert '$("detail-kv").addEventListener("click"' in links and 'closest("a[data-force]")' in links
    assert "confirm(" in links and "preventDefault()" in links


def test_index_html_forced_downloads_are_marked_and_confirmed(make_client):
    html = make_client().get("/").text
    downloads = html.split("function renderDownloads(p)")[1].split('$("retranslate-form")')[0]
    assert 'data-force="1"' in downloads and "forced" in downloads and 'class="msg err"' in downloads
    handler = downloads.split('$("downloads").addEventListener("click"')[1][:400]
    assert 'closest("a[data-force]")' in handler and "confirm(" in handler and "preventDefault()" in handler
    options_row = html.split('"选项 / Options"')[1][:400]
    assert "skip_pages" in options_row and "pages_skipped" in html


# --------------------------------------------------------------------------- #
# Browser-level checks (skipped when Playwright or a Chromium build is unavailable)
# --------------------------------------------------------------------------- #


class TargetSensitiveRunner(FakeRunner):
    """FakeRunner whose QA fails for Korean targets, so one app can hold both kinds of projects."""

    def _run(self, source_pdf, out_dir, options, settings, progress):
        self.fail_qa = options.target_lang is Lang.KO
        return super()._run(source_pdf, out_dir, options, settings, progress)


@pytest.fixture
def live_app(offline_settings):
    """The real app served by uvicorn in a daemon thread (sync jobs), for browser tests."""
    import socket

    import uvicorn

    runner = TargetSensitiveRunner()
    app = create_app(settings=offline_settings, runner=runner, sync=True)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 20
    while not server.started and time.time() < deadline:
        time.sleep(0.05)
    assert server.started, "uvicorn did not start"
    yield f"http://127.0.0.1:{port}", runner
    server.should_exit = True
    thread.join(10)


def _chromium_executable() -> Optional[str]:
    """A Chromium binary Playwright can drive: its default install, or any build under
    PLAYWRIGHT_BROWSERS_PATH / /opt/pw-browsers (CI images often pin an older build)."""
    from playwright.sync_api import sync_playwright

    candidates: list[str] = []
    try:
        with sync_playwright() as pw:
            candidates.append(pw.chromium.executable_path)
    except Exception:  # noqa: BLE001 - no driver available
        pass
    for root in (os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), "/opt/pw-browsers"):
        if root and Path(root).is_dir():
            candidates += sorted((str(p) for p in Path(root).glob("chromium-*/chrome-linux/chrome")), reverse=True)
    return next((c for c in candidates if c and Path(c).is_file()), None)


@pytest.fixture
def browser_page():
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright

    executable = _chromium_executable()
    if executable is None:
        pytest.skip("no Chromium build for Playwright")
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(executable_path=executable, headless=True, args=["--no-sandbox"])
        except Exception as exc:  # noqa: BLE001 - missing system libraries etc.
            pytest.skip(f"cannot launch Chromium: {exc}")
        page = browser.new_page()
        try:
            yield page
        finally:
            browser.close()


def test_web_ui_in_browser(live_app, browser_page, sample_pdf_zh):
    base, runner = live_app
    page = browser_page
    pdf = sample_pdf_zh.read_bytes()

    def post_project(name: str, **fields: str) -> dict:
        multipart = {"files": {"name": name, "mimeType": "application/pdf", "buffer": pdf}, "target_lang": "en", **fields}
        r = page.request.post(f"{base}/api/projects", multipart=multipart)
        assert r.ok, r.text()
        return r.json()["projects"][0]

    # Playwright switches file-chooser interception on asynchronously when the first listener is attached;
    # a click that reaches Chromium before that is silently lost, so listen before the page even loads
    # (expect_file_chooser has the same race on key presses).
    choosers: list = []
    page.on("filechooser", lambda fc: choosers.append(fc))
    page.goto(base + "/")
    page.wait_for_function("document.querySelectorAll('#target-lang option').length > 0")  # init() finished

    # 1. The file picker is reachable and operable from the keyboard (Tab, Enter, Space); mouse still works.
    page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement.id") == "drop"
    for key in ("Enter", " "):
        page.keyboard.press(key)
        page.wait_for_timeout(300)
    assert len(choosers) == 2 and page.evaluate("window.scrollY") == 0
    page.click("#drop")
    page.wait_for_timeout(300)
    assert len(choosers) == 3  # exactly one chooser per click
    choosers[-1].set_files(str(sample_pdf_zh))
    page.wait_for_selector("#file-list li")
    assert sample_pdf_zh.name in page.inner_text("#file-list")

    # 2. The project table is not rebuilt by idle polls; keyboard focus survives them and reaches the detail panel.
    first = post_project("first.pdf", skip_pages="2")
    failed = post_project("failed.pdf", target_lang="ko")
    view = f'#projects-body button[data-view="{first["id"]}"]'
    page.wait_for_selector(view)
    page.focus(view)
    page.wait_for_timeout(2600)  # past at least one 2-second poll
    assert page.evaluate("document.activeElement.dataset.view") == first["id"]
    removed = page.evaluate("""() => new Promise((resolve) => {
        let n = 0;
        new MutationObserver((muts) => muts.forEach((m) => { n += m.removedNodes.length; }))
            .observe(document.getElementById("projects-body"), { childList: true, subtree: true });
        setTimeout(() => resolve(n), 4500);
    })""")
    assert removed == 0
    assert page.evaluate("document.activeElement.dataset.view") == first["id"]
    page.keyboard.press("Enter")
    page.wait_for_selector("#detail:not([hidden])")
    assert "skip=2" in page.inner_text("#detail-kv")
    assert page.locator("#downloads a[data-force]").count() == 0

    # 3. Clearing the skip-pages field of the retranslate form really clears the stored value.
    assert page.input_value("#re-skip") == "2"
    page.fill("#re-skip", "")
    page.select_option("#re-target", "ja")
    page.click("#re-btn")
    page.wait_for_selector("#re-msg.ok")
    project = page.request.get(f"{base}/api/projects/{first['id']}").json()
    assert project["target_lang"] == "ja" and project["options"]["skip_pages"] is None
    assert runner.calls[-1]["options"].skip_pages is None
    page.wait_for_function("document.getElementById('detail-kv').innerText.includes('skip=–')")

    # 4. Downloads of a QA-failed run are labelled as forced and need a confirmation.
    page.click(f'#projects-body button[data-view="{failed["id"]}"]')
    page.wait_for_selector('#downloads a[data-force="1"]')
    assert "forced" in page.inner_text("#downloads") and page.locator("#downloads .msg.err").count() == 1
    downloads: list = []
    page.on("download", lambda d: downloads.append(d))
    page.once("dialog", lambda d: d.dismiss())
    page.click('#downloads a[data-force="1"] >> nth=0')
    page.wait_for_timeout(600)
    assert downloads == []  # cancelled in the confirmation: nothing was downloaded
    page.once("dialog", lambda d: d.accept())
    with page.expect_download() as dl:
        page.click('#downloads a[data-force="1"] >> nth=0')
    assert dl.value.suggested_filename.endswith("_ko.pdf")
