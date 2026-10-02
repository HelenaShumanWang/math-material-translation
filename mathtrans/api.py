"""REST API + web UI for the translation service.

``create_app(settings, runner, sync)`` returns a FastAPI application. Uploaded
PDFs become projects (one per file, sharing a ``batch_id``) whose translation
jobs run on a small thread pool; with ``sync=True`` jobs run inline, which is
what the tests use. ``runner`` is any callable with the signature of
``mathtrans.pipeline.run_pipeline`` and defaults to that function, imported
lazily on first use so the API module never imports the pipeline at import time.

Endpoints (see ARCHITECTURE.md):

    GET    /                                   web UI
    GET    /api/languages
    GET    /api/glossaries        POST /api/glossaries (multipart ``file`` / form or JSON ``text``)
    GET    /api/glossaries/template
    POST   /api/projects          GET /api/projects[?batch_id=]   GET /api/projects/{id}
    POST   /api/projects/{id}/retranslate      {target_lang, source_lang?, glossary_id?, options?}
    GET    /api/projects/{id}/qa[?format=md]
    GET    /api/projects/{id}/preview/{page}   (1-based page, PNG)
    GET    /api/projects/{id}/download?format=pdf|bilingual|docx|segments[&force=1]
    DELETE /api/projects/{id}[?force=1]
"""
from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Callable, Mapping, Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, Response
from pydantic import BaseModel, Field
from starlette.datastructures import UploadFile as StarletteUploadFile

from .config import Settings, get_settings
from .glossary import glossary_template_csv, parse_glossary_text
from .languages import language_choices
from .models import Lang, PipelineOptions, PipelineResult, QAReport, TranslatedDocument, parse_page_spec
from .projects import (DEFAULT_GLOSSARY_ID, GlossaryNotFound, InvalidId, Project, ProjectBusy,
                       ProjectNotFound, ProjectStore, ProjectUnreadable, new_id)

log = logging.getLogger("mathtrans.api")

WEB_DIR = Path(__file__).resolve().parent / "web"
MAX_FILES_PER_BATCH = 50
MAX_QA_ROUNDS_LIMIT = 10
DEFAULT_MAX_UPLOAD_MB = 100
MAX_GLOSSARY_NAME_CHARS = 120

Runner = Callable[..., PipelineResult]
"""``runner(source_pdf, out_dir, options, settings=..., progress=...) -> PipelineResult``"""

_MEDIA_TYPES = {
    "pdf": "application/pdf",
    "bilingual": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "segments": "application/json",
}
_DOWNLOAD_SUFFIX = {
    "pdf": ".pdf",
    "bilingual": "_bilingual.pdf",
    "docx": ".docx",
    "segments": "_segments.json",
}
_RETRANSLATE_OPTION_KEYS = frozenset({"translate_images", "bilingual", "export_docx", "max_qa_rounds",
                                      "require_qa_pass", "subset_fonts", "pages", "skip_pages", "scanned_mode"})
_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


def _default_runner(*args: Any, **kwargs: Any) -> PipelineResult:
    """Resolve ``mathtrans.pipeline.run_pipeline`` at call time."""
    from .pipeline import run_pipeline

    return run_pipeline(*args, **kwargs)


class RetranslateRequest(BaseModel):
    """JSON body of ``POST /api/projects/{id}/retranslate``."""

    target_lang: str
    source_lang: Optional[str] = None
    glossary_id: Optional[str] = None
    options: dict[str, Any] = Field(default_factory=dict)


# --------------------------------------------------------------------------- #
# Form parsing helpers (raise HTTP 400 with a clear message)
# --------------------------------------------------------------------------- #


def _bad(message: str, status: int = 400) -> HTTPException:
    return HTTPException(status_code=status, detail=message)


def parse_bool(value: Any, default: bool, field: str) -> bool:
    """Boolean from a form string (true/false/1/0/yes/no/on/off) or a JSON boolean."""
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    v = str(value).strip().lower()
    if v in _TRUE:
        return True
    if v in _FALSE:
        return False
    raise _bad(f"{field}: expected true/false, got {value!r}")


def parse_int(value: Any, default: int, field: str, lo: int, hi: int) -> int:
    """Integer in ``[lo, hi]`` from a form string or a JSON number (booleans are rejected)."""
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        raise _bad(f"{field}: expected an integer, got {value!r}")
    if isinstance(value, int):
        n = value
    elif isinstance(value, float) and value.is_integer():
        n = int(value)
    else:
        try:
            n = int(str(value).strip())
        except ValueError:
            raise _bad(f"{field}: expected an integer, got {value!r}") from None
    if not lo <= n <= hi:
        raise _bad(f"{field}: must be between {lo} and {hi}")
    return n


def parse_retranslate_options(options: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the ``options`` object of a retranslate request. Only the user-facing
    keys are accepted; keys set to ``null`` keep the project's current value."""
    unknown = set(options) - _RETRANSLATE_OPTION_KEYS
    if unknown:
        raise _bad(f"unsupported options: {', '.join(sorted(unknown))}")
    out: dict[str, Any] = {}
    for key in ("translate_images", "bilingual", "export_docx", "require_qa_pass", "subset_fonts"):
        if options.get(key) is not None:
            out[key] = parse_bool(options[key], False, key)
    if options.get("max_qa_rounds") is not None:
        out["max_qa_rounds"] = parse_int(options["max_qa_rounds"], 1, "max_qa_rounds", 1, MAX_QA_ROUNDS_LIMIT)
    for key in ("pages", "skip_pages"):
        if options.get(key) is not None:
            out[key] = parse_pages(options[key], key)
    if options.get("scanned_mode") is not None:
        out["scanned_mode"] = parse_scanned_mode(options["scanned_mode"])
    return out


def parse_scanned_mode(value: Any) -> str:
    mode = str(value or "overlay").strip().lower()
    if mode not in ("repaint", "overlay"):
        raise _bad("scanned_mode: expected 'repaint' or 'overlay'")
    return mode


def parse_pages(value: Any, field: str) -> Optional[list[int]]:
    """A page specification ("2,5-7", 1-based) or a JSON list of 1-based page numbers."""
    if value is None or value == "" or value == []:
        return None
    if isinstance(value, list):
        value = ",".join(str(v) for v in value)
    try:
        return parse_page_spec(str(value))
    except ValueError as exc:
        raise _bad(f"{field}: {exc}") from None


def parse_glossary_name(value: Any) -> Optional[str]:
    """Optional glossary display name (a non-empty string, trimmed and length-capped)."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise _bad("name must be a string")
    name = " ".join(value.split())
    return name[:MAX_GLOSSARY_NAME_CHARS] or None


def _upload_size(upload: StarletteUploadFile) -> Optional[int]:
    """Size of an upload in bytes without reading it (None when unknown)."""
    size = getattr(upload, "size", None)
    return int(size) if isinstance(size, int) else None


def parse_lang(value: Optional[str], field: str) -> Lang:
    if value is None or not str(value).strip():
        raise _bad(f"{field} is required")
    try:
        return Lang.parse(value)
    except ValueError:
        raise _bad(f"{field}: unsupported language {value!r} (use zh, en, pt, es, ja or ko)") from None


def parse_source_lang(value: Optional[str]) -> Optional[Lang]:
    if value is None or str(value).strip().lower() in ("", "auto", "detect"):
        return None
    return parse_lang(value, "source_lang")


def _normalise_glossary_id(store: ProjectStore, value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip() or value == DEFAULT_GLOSSARY_ID:
        return None
    if not store.has_glossary(value):
        raise _bad(f"unknown glossary: {value!r}")
    return value


# --------------------------------------------------------------------------- #
# Views
# --------------------------------------------------------------------------- #


def project_view(store: ProjectStore, project: Project, *, brief: bool = False) -> dict[str, Any]:
    """JSON representation of a project for the API (``brief`` omits history and QA details)."""
    data = project.model_dump(mode="json", exclude={"history"} if brief else None)
    if brief and data.get("result"):
        data["result"].pop("qa_report", None)
    data["qa"] = project.qa_summary()
    data["downloads"] = {fmt: store.run_file(project, fmt) is not None
                         for fmt in ("pdf", "bilingual", "docx", "segments")}
    data["preview_pages"] = store.preview_count(project)
    data["download_requires_force"] = project.status == "qa_failed"
    return data


def _fallback_markdown(report: QAReport) -> str:
    """Minimal markdown rendering used when ``mathtrans.qa.report`` is unavailable."""
    lines = [
        "# QA report",
        "",
        f"- Passed: {'yes' if report.passed else 'no'}",
        f"- Rounds: {len(report.rounds)}",
        f"- Errors: {report.errors}",
        f"- Warnings: {report.warnings}",
        f"- Checks: {', '.join(report.checks_run) or '-'}",
        f"- Duration: {report.duration_s:.1f}s",
    ]
    if report.summary:
        lines += ["", report.summary]
    for rnd in report.rounds:
        state = "passed" if rnd.passed else "failed"
        lines += ["", f"## Round {rnd.round} ({state}, {len(rnd.issues)} issues, "
                      f"{len(rnd.retranslated)} re-translated)"]
        lines += [_issue_line(i) for i in rnd.issues] or ["- no issues"]
    lines += ["", "## Final issues"]
    lines += [_issue_line(i) for i in report.final_issues] or ["- none"]
    return "\n".join(lines) + "\n"


def _issue_line(issue: Any) -> str:
    where = []
    if issue.page is not None:
        where.append(f"p{issue.page + 1}")
    if issue.segment_id:
        where.append(issue.segment_id)
    loc = f" [{' '.join(where)}]" if where else ""
    return f"- **{issue.severity}** `{issue.check}`{loc}: {issue.message}"


def qa_markdown(report: QAReport, doc: Optional[TranslatedDocument]) -> str:
    """Render the QA report with ``mathtrans.qa.report`` (which quotes the source and
    translated text of each issue when ``doc`` is given); the built-in rendering is used
    when that module is unavailable or cannot render this report."""
    try:
        from .qa.report import report_markdown

        return report_markdown(report, doc)
    except ImportError:
        log.debug("mathtrans.qa.report not importable; using the fallback markdown rendering")
    except Exception:  # noqa: BLE001 - a report must always be viewable
        log.exception("mathtrans.qa.report failed to render the report; using the fallback rendering")
    return _fallback_markdown(report)


# --------------------------------------------------------------------------- #
# Job execution
# --------------------------------------------------------------------------- #


def run_job(store: ProjectStore, runner: Runner, settings: Settings, project_id: str) -> None:
    """Execute the queued run of ``project_id`` and persist progress, result or error."""
    try:
        project = store.get(project_id)
    except ProjectNotFound:
        log.warning("job %s: project vanished before it started", project_id)
        return
    if project.status != "queued":
        log.warning("job %s: project is %s, not queued; skipping", project_id, project.status)
        return
    try:
        store.mark_running(project)
        options = store.pipeline_options(project)
        run_dir = store.current_run_dir(project)
        source = store.source_path(project.id)

        def progress(stage: str, message: str, percent: float) -> None:
            try:
                store.set_progress(project, stage, message, percent)
            except ProjectNotFound:
                log.warning("job %s: project deleted while running", project_id)

        log.info("job %s: run %s %s -> %s", project_id, project.current_run,
                 options.source_lang.value if options.source_lang else "auto", options.target_lang.value)
        result = runner(source, run_dir, options, settings=settings, progress=progress)
        if not isinstance(result, PipelineResult):
            result = PipelineResult.model_validate(result)
        store.finish(project, result)
        log.info("job %s: %s", project_id, result.status)
    except ProjectNotFound:
        log.warning("job %s: project deleted while running; result discarded", project_id)
    except Exception as exc:  # noqa: BLE001 - any failure becomes the project's error state
        log.exception("job %s failed", project_id)
        try:
            store.fail(project, f"{type(exc).__name__}: {exc}")
        except ProjectNotFound:
            log.warning("job %s: project deleted while running; error discarded", project_id)
    # a project force-deleted mid-run may have had its run directory re-created by the runner
    store.discard_orphan_dir(project_id)


# --------------------------------------------------------------------------- #
# Application factory
# --------------------------------------------------------------------------- #


def create_app(settings: Optional[Settings] = None, runner: Optional[Runner] = None,
               sync: bool = False) -> FastAPI:
    """Build the FastAPI application.

    :param settings: service settings (defaults to :func:`mathtrans.config.get_settings`).
    :param runner: pipeline callable; defaults to ``mathtrans.pipeline.run_pipeline`` (lazy).
    :param sync: run jobs inline in the request instead of on the thread pool (tests).
    """
    settings = settings or get_settings()
    runner = runner or _default_runner
    store = ProjectStore(settings.data_dir)
    recovered = store.recover_interrupted()
    max_upload_mb = int(getattr(settings, "max_upload_mb", DEFAULT_MAX_UPLOAD_MB))
    max_upload_bytes = max_upload_mb * 1024 * 1024
    executor: Optional[ThreadPoolExecutor] = None
    if not sync:
        executor = ThreadPoolExecutor(max_workers=max(1, settings.max_workers), thread_name_prefix="mathtrans-job")

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        log.info("mathtrans API ready (data dir %s, %s)", store.data_dir,
                 "sync jobs" if sync else f"{settings.max_workers} worker(s)")
        yield
        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=True)

    app = FastAPI(title="mathtrans", version="0.1.0", lifespan=lifespan,
                  description="Layout-preserving translation of math learning materials")
    app.state.settings = settings
    app.state.store = store
    app.state.runner = runner
    app.state.sync = sync
    app.state.executor = executor
    app.state.recovered = recovered

    def submit(project_id: str) -> None:
        if executor is None:
            run_job(store, runner, settings, project_id)
        else:
            executor.submit(run_job, store, runner, settings, project_id)

    app.state.submit = submit

    def load_project(project_id: str) -> Project:
        try:
            return store.get(project_id)
        except (InvalidId, ProjectNotFound):
            raise HTTPException(status_code=404, detail=f"project not found: {project_id}") from None
        except ProjectUnreadable as exc:
            log.error("project %s: %s", project_id, exc)
            raise HTTPException(status_code=500, detail=f"project record is unreadable: {project_id}") from None

    # ------------------------------------------------------------ error mapping
    @app.exception_handler(RequestValidationError)
    async def _validation_error(_request: Request, exc: RequestValidationError) -> JSONResponse:
        # errors() may carry non-JSON values (exception objects in ctx, raw inputs)
        return JSONResponse(status_code=400,
                            content={"detail": "invalid request", "errors": jsonable_encoder(exc.errors())})

    @app.exception_handler(ProjectBusy)
    async def _busy(_request: Request, exc: ProjectBusy) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(GlossaryNotFound)
    async def _glossary_missing(_request: Request, exc: GlossaryNotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    # ------------------------------------------------------------------- UI
    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def index() -> HTMLResponse:
        page = WEB_DIR / "index.html"
        if not page.is_file():
            raise HTTPException(status_code=500, detail="web UI not installed (mathtrans/web/index.html missing)")
        return HTMLResponse(page.read_text(encoding="utf-8"))

    # ------------------------------------------------------------ languages
    @app.get("/api/languages")
    def languages() -> list[dict[str, str]]:
        return language_choices()

    # ----------------------------------------------------------- glossaries
    @app.get("/api/glossaries")
    def list_glossaries() -> list[dict[str, Any]]:
        return store.list_glossaries()

    @app.get("/api/glossaries/template")
    def glossary_template() -> Response:
        return PlainTextResponse(
            glossary_template_csv(),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="glossary_template.csv"'},
        )

    @app.post("/api/glossaries", status_code=201)
    async def upload_glossary(request: Request) -> dict[str, Any]:
        """Create a custom glossary from an uploaded CSV/TSV/JSON file or pasted text."""
        content_type = request.headers.get("content-type", "")
        text: Optional[str] = None
        name: Optional[str] = None
        fmt: Optional[str] = None
        if content_type.startswith("application/json"):
            try:
                body = await request.json()
            except ValueError:
                raise _bad("invalid JSON body") from None
            if not isinstance(body, dict):
                raise _bad("JSON body must be an object with a 'text' field")
            text = body.get("text")
            name = parse_glossary_name(body.get("name"))
            if "entries" in body and text is None:  # a Glossary object posted directly
                text = json.dumps(body, ensure_ascii=False)
                fmt = "json"
        else:
            form = await request.form()
            upload = form.get("file")
            if isinstance(upload, StarletteUploadFile):  # form parsing yields Starlette's class
                size = _upload_size(upload)
                if size is not None and size > max_upload_bytes:
                    raise _bad(f"glossary file exceeds {max_upload_mb} MB", 413)
                raw = await upload.read(max_upload_bytes + 1)
                if len(raw) > max_upload_bytes:
                    raise _bad(f"glossary file exceeds {max_upload_mb} MB", 413)
                try:
                    text = raw.decode("utf-8-sig")
                except UnicodeDecodeError:
                    raise _bad("glossary file must be UTF-8 encoded text") from None
                suffix = Path(upload.filename or "").suffix.lower()
                fmt = "json" if suffix == ".json" else None
                name = parse_glossary_name(form.get("name")) or parse_glossary_name(Path(upload.filename or "").stem)
            else:
                text = form.get("text")
                name = parse_glossary_name(form.get("name"))
        if not isinstance(text, str) or not text.strip():
            raise _bad("provide a glossary 'file' (CSV/TSV/JSON) or non-empty 'text'")
        try:
            glossary = parse_glossary_text(text, fmt=fmt, glossary_id="custom", name=name or "Custom glossary")
        except (TypeError, AttributeError):  # JSON of the wrong shape (e.g. an object without 'entries')
            raise _bad("could not parse glossary: JSON must be a list of {\"zh\": ..., \"en\": ...} rows "
                       "or an object with an 'entries' list") from None
        except (ValueError, LookupError) as exc:  # json.JSONDecodeError / pydantic ValidationError
            raise _bad(f"could not parse glossary: {str(exc).splitlines()[0]}") from None
        if not glossary.entries:
            raise _bad("the glossary contains no entries (header must list language codes zh,en,pt,es,ja,ko)")
        glossary.id = "custom"  # always store under a fresh id
        glossary = store.save_glossary(glossary)
        return {"id": glossary.id, "name": glossary.name, "entries": len(glossary.entries), "builtin": False}

    # ------------------------------------------------------------- projects
    @app.post("/api/projects", status_code=201)
    def create_projects(
        files: Optional[list[UploadFile]] = File(None),
        target_lang: Optional[str] = Form(None),
        source_lang: Optional[str] = Form(None),
        glossary_id: Optional[str] = Form(None),
        translate_images: Optional[str] = Form(None),
        bilingual: Optional[str] = Form(None),
        export_docx: Optional[str] = Form(None),
        max_qa_rounds: Optional[str] = Form(None),
        require_qa_pass: Optional[str] = Form(None),
        subset_fonts: Optional[str] = Form(None),
        pages: Optional[str] = Form(None),
        skip_pages: Optional[str] = Form(None),
        scanned_mode: Optional[str] = Form(None),
    ) -> dict[str, Any]:
        """Upload 1..50 PDFs and queue one translation project per file (shared ``batch_id``)."""
        uploads = [f for f in (files or []) if f.filename]
        if not uploads:
            raise _bad("upload at least one PDF in the 'files' field")
        if len(uploads) > MAX_FILES_PER_BATCH:
            raise _bad(f"at most {MAX_FILES_PER_BATCH} files per batch")
        target = parse_lang(target_lang, "target_lang")
        source = parse_source_lang(source_lang)
        if source is not None and source == target:
            raise _bad("source_lang and target_lang must differ")
        options = PipelineOptions(
            target_lang=target,
            source_lang=source,
            translate_images=parse_bool(translate_images, True, "translate_images"),
            bilingual=parse_bool(bilingual, False, "bilingual"),
            export_docx=parse_bool(export_docx, False, "export_docx"),
            max_qa_rounds=parse_int(max_qa_rounds, settings.max_qa_rounds, "max_qa_rounds", 1, MAX_QA_ROUNDS_LIMIT),
            require_qa_pass=parse_bool(require_qa_pass, settings.require_qa_pass, "require_qa_pass"),
            subset_fonts=parse_bool(subset_fonts, False, "subset_fonts"),
            pages=parse_pages(pages, "pages"),
            skip_pages=parse_pages(skip_pages, "skip_pages"),
            scanned_mode=parse_scanned_mode(scanned_mode),
            min_font_scale=settings.min_font_scale,
            preview_dpi=settings.preview_dpi,
        )
        gid = _normalise_glossary_id(store, glossary_id)

        # Files are validated and stored one at a time (only one upload is held in memory);
        # the batch is all-or-nothing: any rejected file rolls back the projects created so far.
        batch_id = new_id()[:12]
        projects: list[Project] = []
        try:
            for upload in uploads:
                filename = upload.filename or ""
                if not filename.lower().endswith(".pdf"):
                    raise _bad(f"{filename!r}: only .pdf files are accepted")
                size = _upload_size(upload)
                if size is not None and size > max_upload_bytes:
                    raise _bad(f"{filename!r}: file exceeds the {max_upload_mb} MB upload limit", 413)
                data = upload.file.read(max_upload_bytes + 1)
                if len(data) > max_upload_bytes:
                    raise _bad(f"{filename!r}: file exceeds the {max_upload_mb} MB upload limit", 413)
                if not data.startswith(b"%PDF"):
                    raise _bad(f"{filename!r}: not a PDF file (missing %PDF header)")
                try:
                    projects.append(store.create(filename, data, options, glossary_id=gid, batch_id=batch_id))
                except ValueError as exc:
                    raise _bad(f"{filename!r}: {exc}") from None
        except HTTPException:
            for created in projects:  # roll back the partial batch (nothing was submitted yet)
                store.delete(created.id, force=True)
            raise
        for project in projects:
            submit(project.id)
        views = [project_view(store, load_project(p.id), brief=True) for p in projects]
        return {"batch_id": batch_id, "projects": views}

    @app.get("/api/projects")
    def list_projects(batch_id: Optional[str] = Query(None)) -> list[dict[str, Any]]:
        return [project_view(store, p, brief=True) for p in store.list(batch_id=batch_id)]

    @app.get("/api/projects/{project_id}")
    def get_project(project_id: str) -> dict[str, Any]:
        return project_view(store, load_project(project_id))

    @app.post("/api/projects/{project_id}/retranslate", status_code=202)
    def retranslate(project_id: str, body: RetranslateRequest) -> dict[str, Any]:
        """Start a new run on the same source with a new target language / glossary / options."""
        project = load_project(project_id)
        target = parse_lang(body.target_lang, "target_lang")
        source = parse_source_lang(body.source_lang) if body.source_lang is not None else project.source_lang
        if source is not None and source == target:
            raise _bad("source_lang and target_lang must differ")
        options = parse_retranslate_options(body.options)
        gid = _normalise_glossary_id(store, body.glossary_id) if body.glossary_id is not None else project.glossary_id
        try:
            project = store.begin_run(project.id, target, source_lang=source, glossary_id=gid, options=options)
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail=f"project not found: {project_id}") from None
        except ValueError as exc:  # stored options + overrides no longer form valid PipelineOptions
            raise _bad(f"invalid options: {str(exc).splitlines()[0]}") from None
        submit(project.id)
        return project_view(store, load_project(project.id))

    @app.get("/api/projects/{project_id}/qa")
    def project_qa(project_id: str, format: str = Query("json")) -> Response:
        """QA report of the current run as JSON, or markdown with ``?format=md``."""
        project = load_project(project_id)
        report = project.result.qa_report if project.result is not None else None
        if report is None:
            path = store.run_file(project, "qa")
            if path is not None:
                try:
                    report = QAReport.model_validate_json(path.read_text(encoding="utf-8"))
                except ValueError as exc:
                    log.error("project %s: %s is unreadable: %s", project_id, path, exc)
                    raise HTTPException(status_code=500, detail="the QA report on disk is unreadable") from None
        if report is None:
            raise HTTPException(status_code=404, detail="QA report not available yet")
        fmt = format.lower()
        if fmt in ("md", "markdown"):
            doc: Optional[TranslatedDocument] = None
            seg_path = store.run_file(project, "segments")
            if seg_path is not None:
                try:
                    doc = TranslatedDocument.model_validate_json(seg_path.read_text(encoding="utf-8"))
                except ValueError as exc:
                    log.warning("project %s: segments.json unreadable: %s", project_id, exc)
            return PlainTextResponse(qa_markdown(report, doc), media_type="text/markdown; charset=utf-8")
        if fmt != "json":
            raise _bad("format must be 'json' or 'md'")
        return JSONResponse(report.model_dump(mode="json"))

    @app.get("/api/projects/{project_id}/preview/{page}")
    def project_preview(project_id: str, page: int) -> FileResponse:
        """PNG preview of a page (1-based) of the current run."""
        project = load_project(project_id)
        path = store.preview_path(project, page)
        if path is None:
            raise HTTPException(status_code=404, detail=f"no preview for page {page}")
        return FileResponse(path, media_type="image/png")

    @app.get("/api/projects/{project_id}/download")
    def project_download(project_id: str, format: str = Query("pdf"), force: str = Query("0")) -> FileResponse:
        """Download an output of the current run. Projects that failed QA need ``force=1``."""
        fmt = format.lower()
        if fmt not in _MEDIA_TYPES:
            raise _bad("format must be one of pdf, bilingual, docx, segments")
        forced = parse_bool(force, False, "force")
        project = load_project(project_id)
        if project.status in ("queued", "running"):
            raise HTTPException(status_code=409, detail=f"project is {project.status}; outputs are not ready")
        if project.status == "error":
            raise HTTPException(status_code=409, detail=f"the run failed: {project.error or 'unknown error'}")
        if project.status == "qa_failed" and not forced:
            raise HTTPException(
                status_code=409,
                detail="automatic QA did not pass; review the QA report and add force=1 to download anyway",
            )
        path = store.run_file(project, fmt)
        if path is None:
            raise HTTPException(status_code=404, detail=f"this run has no '{fmt}' output")
        filename = f"{project.name}_{project.target_lang.value}{_DOWNLOAD_SUFFIX[fmt]}"
        return FileResponse(path, media_type=_MEDIA_TYPES[fmt], filename=filename)

    @app.delete("/api/projects/{project_id}")
    def delete_project(project_id: str, force: str = Query("0")) -> dict[str, Any]:
        """Delete a project and all its runs (running projects need ``force=1``)."""
        project = load_project(project_id)
        store.delete(project.id, force=parse_bool(force, False, "force"))
        return {"deleted": project.id}

    return app


__all__ = ["create_app", "project_view", "qa_markdown", "run_job", "RetranslateRequest", "Runner"]
