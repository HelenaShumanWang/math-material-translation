"""Persistent project store: uploaded sources, translation runs and custom glossaries.

Layout on disk (``data_dir`` defaults to ``Settings.data_dir``)::

    data/
      projects/<project id>/
        project.json              # the Project record (current run + history)
        source.pdf                # the uploaded file
        runs/<run id>/            # one directory per translation run
          output.pdf  bilingual.pdf  output.docx  segments.json  qa_report.json  previews/
      glossaries/<glossary id>.json

Project and run ids are lower-case hexadecimal strings; every id coming from
outside is validated before it is turned into a path, so a crafted id can never
escape the data directory. All writes go through one lock and are atomic
(write to a temporary file, then ``os.replace``), so a concurrently polling
reader always sees a complete ``project.json``.
"""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from .glossary import default_glossary
from .models import Glossary, Lang, PipelineOptions, PipelineResult

log = logging.getLogger("mathtrans.projects")

ProjectStatus = Literal["queued", "running", "completed", "qa_failed", "error"]
ACTIVE_STATUSES: tuple[str, ...] = ("queued", "running")
FINISHED_STATUSES: tuple[str, ...] = ("completed", "qa_failed", "error")

DEFAULT_GLOSSARY_ID = "default"
_ID_RE = re.compile(r"^[0-9a-f]{8,64}$")
_SOURCE_FILE = "source.pdf"
_PROJECT_FILE = "project.json"
_RUNS_DIR = "runs"

#: Files a run may produce, keyed by the download ``format`` used by the API / CLI.
RUN_OUTPUTS: dict[str, str] = {
    "pdf": "output.pdf",
    "bilingual": "bilingual.pdf",
    "docx": "output.docx",
    "segments": "segments.json",
    "qa": "qa_report.json",
}


class ProjectError(Exception):
    """Base class for store errors."""


class InvalidId(ProjectError, ValueError):
    """An id that is not a valid project / run / glossary id."""


class ProjectNotFound(ProjectError, LookupError):
    """No project with this id exists."""


class ProjectUnreadable(ProjectError, ValueError):
    """The project's ``project.json`` exists but cannot be parsed."""


class GlossaryNotFound(ProjectError, LookupError):
    """No glossary with this id exists."""


class ProjectBusy(ProjectError):
    """The project has a queued or running job and cannot be modified."""


_clock_lock = threading.Lock()
_last_tick = 0.0


def _now() -> str:
    """UTC timestamp (ISO 8601, millisecond resolution) that is strictly increasing
    within the process, so ``created_at`` orders projects of one batch deterministically
    and ``updated_at`` changes on every write (the UI polls for that)."""
    global _last_tick
    with _clock_lock:
        tick = max(time.time(), _last_tick + 0.001)
        _last_tick = tick
    return datetime.fromtimestamp(tick, timezone.utc).isoformat(timespec="milliseconds")


def new_id() -> str:
    """A fresh 32-character hexadecimal id."""
    return uuid.uuid4().hex


def new_run_id() -> str:
    """A fresh 16-character hexadecimal run id."""
    return uuid.uuid4().hex[:16]


def validate_id(value: str, what: str = "id") -> str:
    """Return ``value`` if it is a safe hexadecimal id, else raise :class:`InvalidId`."""
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise InvalidId(f"invalid {what}: {value!r}")
    return value


def safe_name(filename: str, fallback: str = "document") -> str:
    """A display name derived from an uploaded filename (no directories, no extension)."""
    base = Path(filename.replace("\\", "/")).name
    stem = Path(base).stem if base.lower().endswith(".pdf") else base
    stem = re.sub(r"[\x00-\x1f\x7f]", "", stem).strip().strip(".")
    return stem[:120] or fallback


class ProjectProgress(BaseModel):
    """Live progress of the current run, updated by the pipeline's progress callback."""

    stage: str = ""
    message: str = ""
    percent: float = 0.0


class Project(BaseModel):
    """One uploaded document and its translation runs."""

    id: str
    name: str
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    source_file: str = _SOURCE_FILE  # file name inside the project directory
    source_name: str = ""  # original upload name (for download file names)
    source_size: int = 0
    page_count: int = 0
    source_lang: Optional[Lang] = None  # None => auto-detect
    target_lang: Lang
    options: dict[str, Any] = Field(default_factory=dict)  # PipelineOptions without the glossary object
    glossary_id: Optional[str] = None  # None / "default" => built-in glossary only
    batch_id: Optional[str] = None
    status: ProjectStatus = "queued"
    progress: ProjectProgress = Field(default_factory=ProjectProgress)
    result: Optional[PipelineResult] = None
    error: Optional[str] = None
    current_run: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    history: list[dict[str, Any]] = Field(default_factory=list)

    @property
    def is_active(self) -> bool:
        return self.status in ACTIVE_STATUSES

    def qa_summary(self) -> Optional[dict[str, Any]]:
        """Compact QA numbers for listings and the UI (None before a run finished)."""
        if self.result is None or self.result.qa_report is None:
            return None
        r = self.result.qa_report
        return {
            "passed": r.passed,
            "rounds": len(r.rounds),
            "errors": r.errors,
            "warnings": r.warnings,
            "summary": r.summary,
        }


def options_to_dict(options: PipelineOptions | dict[str, Any]) -> dict[str, Any]:
    """JSON-safe pipeline options without the (file-backed) glossary object."""
    if isinstance(options, PipelineOptions):
        data = options.model_dump(exclude={"glossary"})
    else:
        data = dict(options)
    data.pop("glossary", None)
    # normalise through the model so stored options are always valid
    options = PipelineOptions.model_validate(data)
    if isinstance(options.max_qa_rounds, bool) or options.max_qa_rounds < 1:
        raise ValueError(f"max_qa_rounds must be a positive integer, got {options.max_qa_rounds!r}")
    return options.model_dump(mode="json", exclude={"glossary"})


class ProjectStore:
    """File-system backed store for projects, runs and glossaries (thread-safe)."""

    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.projects_dir = self.data_dir / "projects"
        self.glossaries_dir = self.data_dir / "glossaries"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.glossaries_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        log.debug("project store at %s", self.data_dir)

    # ------------------------------------------------------------------ paths
    def project_dir(self, project_id: str) -> Path:
        return self.projects_dir / validate_id(project_id, "project id")

    def source_path(self, project_id: str) -> Path:
        return self.project_dir(project_id) / _SOURCE_FILE

    def run_dir(self, project_id: str, run_id: str) -> Path:
        return self.project_dir(project_id) / _RUNS_DIR / validate_id(run_id, "run id")

    def current_run_dir(self, project: Project) -> Optional[Path]:
        if not project.current_run:
            return None
        return self.run_dir(project.id, project.current_run)

    def run_file(self, project: Project, fmt: str) -> Optional[Path]:
        """Path of an output of the current run (``pdf``/``bilingual``/``docx``/``segments``/``qa``)
        if the file exists, else None."""
        if fmt not in RUN_OUTPUTS:
            raise ValueError(f"unknown output format: {fmt!r}")
        run_dir = self.current_run_dir(project)
        if run_dir is None:
            return None
        path = run_dir / RUN_OUTPUTS[fmt]
        return path if path.is_file() else None

    def preview_path(self, project: Project, page: int) -> Optional[Path]:
        """PNG preview of 1-based ``page`` from the current run, if it exists."""
        run_dir = self.current_run_dir(project)
        if run_dir is None or page < 1:
            return None
        path = run_dir / "previews" / f"page-{page:03d}.png"
        return path if path.is_file() else None

    def preview_count(self, project: Project) -> int:
        run_dir = self.current_run_dir(project)
        if run_dir is None:
            return 0
        previews = run_dir / "previews"
        if not previews.is_dir():
            return 0
        return sum(1 for p in previews.iterdir() if p.suffix == ".png" and p.name.startswith("page-"))

    # --------------------------------------------------------------- projects
    def create(
        self,
        name: str,
        pdf_bytes: bytes,
        options: PipelineOptions | dict[str, Any],
        glossary_id: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> Project:
        """Store an uploaded PDF and create a queued project with its first run."""
        if not pdf_bytes.startswith(b"%PDF"):
            raise ValueError("the uploaded file is not a PDF")
        opts = options_to_dict(options)
        glossary_id = self._normalise_glossary_id(glossary_id)
        project_id = new_id()
        pdir = self.projects_dir / project_id
        page_count = _pdf_page_count(pdf_bytes)
        project = Project(
            id=project_id,
            name=safe_name(name),
            source_name=Path(name.replace("\\", "/")).name or f"{safe_name(name)}.pdf",
            source_size=len(pdf_bytes),
            page_count=page_count,
            source_lang=Lang.parse(opts["source_lang"]) if opts.get("source_lang") else None,
            target_lang=Lang.parse(opts["target_lang"]),
            options=opts,
            glossary_id=glossary_id,
            batch_id=batch_id,
            current_run=new_run_id(),
        )
        with self._lock:
            pdir.mkdir(parents=True, exist_ok=False)
            (pdir / _RUNS_DIR / project.current_run).mkdir(parents=True)
            _atomic_write_bytes(pdir / _SOURCE_FILE, pdf_bytes)
            self._write(project)
        log.info("created project %s (%s, %d pages, -> %s)", project.id, project.name, page_count,
                 project.target_lang.value)
        return project

    def get(self, project_id: str) -> Project:
        path = self.project_dir(project_id) / _PROJECT_FILE
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return Project.model_validate(data)
        except FileNotFoundError:
            raise ProjectNotFound(f"project not found: {project_id}") from None
        except ValueError as exc:  # JSONDecodeError / pydantic ValidationError
            raise ProjectUnreadable(f"project record {path} is unreadable: {exc}") from exc

    def exists(self, project_id: str) -> bool:
        try:
            return (self.project_dir(project_id) / _PROJECT_FILE).is_file()
        except InvalidId:
            return False

    def list(self, batch_id: Optional[str] = None) -> list[Project]:
        """All projects, newest first (optionally only one batch)."""
        projects: list[Project] = []
        for pdir in self.projects_dir.iterdir():
            if not pdir.is_dir() or not _ID_RE.fullmatch(pdir.name):
                continue
            try:
                project = self.get(pdir.name)
            except ProjectNotFound:
                log.debug("skipping project directory without a record: %s", pdir)
                continue
            except ProjectUnreadable as exc:
                log.warning("skipping unreadable project %s: %s", pdir.name, exc)
                continue
            if batch_id is None or project.batch_id == batch_id:
                projects.append(project)
        projects.sort(key=lambda p: (p.created_at, p.id), reverse=True)
        return projects

    def update(self, project: Project) -> Project:
        """Persist ``project`` (atomically). Raises ProjectNotFound if it was deleted."""
        with self._lock:
            if not self.project_dir(project.id).is_dir():
                raise ProjectNotFound(f"project not found: {project.id}")
            project.updated_at = _now()
            self._write(project)
        return project

    def delete(self, project_id: str, force: bool = False) -> None:
        """Remove the project directory. Active projects are refused unless ``force``."""
        with self._lock:
            project = self.get(project_id)
            if project.is_active and not force:
                raise ProjectBusy(f"project {project_id} is {project.status}; wait for it to finish")
            shutil.rmtree(self.project_dir(project_id))
        log.info("deleted project %s", project_id)

    def discard_orphan_dir(self, project_id: str) -> bool:
        """Remove ``projects/<id>`` when it holds no ``project.json`` (a job that kept
        writing after the project was force-deleted). Returns True when removed."""
        with self._lock:
            pdir = self.project_dir(project_id)
            if not pdir.is_dir() or (pdir / _PROJECT_FILE).exists():
                return False
            shutil.rmtree(pdir, ignore_errors=True)
        log.info("removed orphan directory of deleted project %s", project_id)
        return True

    def begin_run(
        self,
        project_id: str,
        target_lang: Lang | str,
        *,
        source_lang: Lang | str | None = None,
        glossary_id: Optional[str] = None,
        options: Optional[dict[str, Any]] = None,
    ) -> Project:
        """Queue a new run on the same source (re-translation). The previous run is
        appended to ``history``; the new run inherits the old options unless overridden."""
        with self._lock:
            project = self.get(project_id)
            if project.is_active:
                raise ProjectBusy(f"project {project_id} is {project.status}; wait for it to finish")
            if project.current_run:
                project.history.append(self._history_entry(project))
            opts = dict(project.options)
            opts.update({k: v for k, v in (options or {}).items() if k != "glossary"})
            opts["target_lang"] = Lang.parse(target_lang).value
            opts["source_lang"] = Lang.parse(source_lang).value if source_lang else None
            project.options = options_to_dict(opts)
            project.target_lang = Lang.parse(opts["target_lang"])
            project.source_lang = Lang.parse(opts["source_lang"]) if opts["source_lang"] else None
            project.glossary_id = self._normalise_glossary_id(glossary_id)
            project.current_run = new_run_id()
            project.status = "queued"
            project.progress = ProjectProgress()
            project.result = None
            project.error = None
            project.started_at = None
            project.finished_at = None
            self.run_dir(project.id, project.current_run).mkdir(parents=True)
            self.update(project)
        log.info("project %s: new run %s -> %s", project.id, project.current_run, project.target_lang.value)
        return project

    def mark_running(self, project: Project) -> Project:
        project.status = "running"
        project.started_at = _now()
        project.progress = ProjectProgress(stage="start", message="Starting", percent=0.0)
        return self.update(project)

    def set_progress(self, project: Project, stage: str, message: str, percent: float) -> Project:
        project.progress = ProjectProgress(stage=stage, message=message,
                                           percent=max(0.0, min(100.0, float(percent))))
        return self.update(project)

    def finish(self, project: Project, result: PipelineResult) -> Project:
        """Store the pipeline result and derive the final status from it."""
        project.result = result
        project.status = result.status
        project.error = result.error
        project.finished_at = _now()
        stage = "done" if result.status != "error" else "error"
        project.progress = ProjectProgress(stage=stage, message=_result_message(result), percent=100.0)
        return self.update(project)

    def fail(self, project: Project, message: str) -> Project:
        """Mark the current run as failed with an error message (runner crashed etc.)."""
        project.status = "error"
        project.error = message
        project.result = None
        project.finished_at = _now()
        project.progress = ProjectProgress(stage="error", message=message, percent=100.0)
        return self.update(project)

    def recover_interrupted(self) -> list[str]:
        """Mark projects left ``queued``/``running`` by a previous process as errors.

        Called once at service start-up: their jobs died with the old process."""
        recovered: list[str] = []
        for project in self.list():
            if project.is_active:
                self.fail(project, "Interrupted: the service was restarted before the job finished")
                recovered.append(project.id)
        if recovered:
            log.warning("marked %d interrupted project(s) as error", len(recovered))
        return recovered

    def pipeline_options(self, project: Project) -> PipelineOptions:
        """Build the :class:`PipelineOptions` for the project's current run, with the
        custom glossary loaded from disk."""
        data = dict(project.options)
        glossary = None
        if project.glossary_id and project.glossary_id != DEFAULT_GLOSSARY_ID:
            glossary = self.get_glossary(project.glossary_id)
        data["glossary"] = glossary
        return PipelineOptions.model_validate(data)

    # -------------------------------------------------------------- glossaries
    def glossary_path(self, glossary_id: str) -> Path:
        return self.glossaries_dir / f"{validate_id(glossary_id, 'glossary id')}.json"

    def save_glossary(self, glossary: Glossary) -> Glossary:
        """Persist a custom glossary. A glossary whose id is not a custom id gets a new one."""
        if not _ID_RE.fullmatch(glossary.id or ""):
            glossary.id = uuid.uuid4().hex[:12]
        if not glossary.name or glossary.name == "Custom glossary":
            glossary.name = f"Custom glossary {glossary.id[:6]}"
        with self._lock:
            _atomic_write_text(self.glossary_path(glossary.id), glossary.model_dump_json(indent=1))
        log.info("saved glossary %s (%s, %d entries)", glossary.id, glossary.name, len(glossary.entries))
        return glossary

    def get_glossary(self, glossary_id: str) -> Glossary:
        """The built-in glossary for ``"default"``, otherwise a saved custom glossary."""
        if glossary_id == DEFAULT_GLOSSARY_ID:
            return default_glossary()
        try:
            path = self.glossary_path(glossary_id)
        except InvalidId:
            raise GlossaryNotFound(f"glossary not found: {glossary_id}") from None
        try:
            return Glossary.model_validate_json(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise GlossaryNotFound(f"glossary not found: {glossary_id}") from None

    def has_glossary(self, glossary_id: str) -> bool:
        if glossary_id == DEFAULT_GLOSSARY_ID:
            return True
        try:
            return self.glossary_path(glossary_id).is_file()
        except InvalidId:
            return False

    def list_glossaries(self) -> list[dict[str, Any]]:
        """Built-in glossary first, then the custom ones by name."""
        builtin = default_glossary()
        out = [{"id": DEFAULT_GLOSSARY_ID, "name": builtin.name, "entries": len(builtin.entries), "builtin": True}]
        custom: list[dict[str, Any]] = []
        for path in self.glossaries_dir.glob("*.json"):
            if not _ID_RE.fullmatch(path.stem):
                continue
            try:
                g = Glossary.model_validate_json(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                log.warning("skipping unreadable glossary %s: %s", path.name, exc)
                continue
            custom.append({"id": path.stem, "name": g.name, "entries": len(g.entries), "builtin": False})
        custom.sort(key=lambda g: (g["name"].lower(), g["id"]))
        return out + custom

    # ---------------------------------------------------------------- internal
    def _normalise_glossary_id(self, glossary_id: Optional[str]) -> Optional[str]:
        if not glossary_id or glossary_id == DEFAULT_GLOSSARY_ID:
            return None
        if not self.has_glossary(glossary_id):
            raise GlossaryNotFound(f"glossary not found: {glossary_id}")
        return glossary_id

    def _write(self, project: Project) -> None:
        _atomic_write_text(self.project_dir(project.id) / _PROJECT_FILE, project.model_dump_json(indent=1))

    def _history_entry(self, project: Project) -> dict[str, Any]:
        result = project.result
        entry: dict[str, Any] = {
            "run_id": project.current_run,
            "target_lang": project.target_lang.value,
            "source_lang": project.source_lang.value if project.source_lang else None,
            "glossary_id": project.glossary_id,
            "options": dict(project.options),
            "status": project.status,
            "error": project.error,
            "started_at": project.started_at,
            "finished_at": project.finished_at,
            "archived_at": _now(),
            "outputs": {},
            "qa": project.qa_summary(),
        }
        if result is not None:
            entry["outputs"] = {
                "pdf": result.output_pdf,
                "bilingual": result.bilingual_pdf,
                "docx": result.docx,
                "segments": result.segments_json,
            }
        return entry


def _result_message(result: PipelineResult) -> str:
    if result.status == "error":
        return result.error or "Pipeline failed"
    if result.qa_report is not None and result.qa_report.summary:
        return result.qa_report.summary
    return "Completed" if result.status == "completed" else "QA did not pass"


def _pdf_page_count(pdf_bytes: bytes) -> int:
    """Page count of an in-memory PDF; raises ValueError if PyMuPDF cannot open it."""
    import pymupdf

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
            if doc.needs_pass:
                raise ValueError("the PDF is password protected")
            count = doc.page_count
    except ValueError:
        raise
    except Exception as exc:  # pymupdf raises various error types for broken files
        raise ValueError(f"the file is not a readable PDF: {exc}") from exc
    if count < 1:
        raise ValueError("the PDF has no pages")
    return count


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def _atomic_write_text(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


__all__ = [
    "ACTIVE_STATUSES",
    "DEFAULT_GLOSSARY_ID",
    "FINISHED_STATUSES",
    "RUN_OUTPUTS",
    "GlossaryNotFound",
    "InvalidId",
    "Project",
    "ProjectBusy",
    "ProjectError",
    "ProjectNotFound",
    "ProjectProgress",
    "ProjectStatus",
    "ProjectStore",
    "ProjectUnreadable",
    "new_id",
    "new_run_id",
    "options_to_dict",
    "safe_name",
    "validate_id",
]
