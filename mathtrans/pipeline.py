"""End-to-end orchestration: PDF in, translated (and QA-checked) PDF out.

Stages (progress percent in brackets):
    extract [5] -> ocr [15] -> translate [45] -> qa loop [70] -> layout [85]
    -> output checks [90] -> exports [97] -> previews [100]

The QA loop re-renders the document after every re-translation so that
layout-fit problems are judged on fresh geometry. Output files are written
even when QA fails (status ``qa_failed``) so that a reviewer can inspect them;
the web API refuses to serve them unless explicitly forced.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import time
import traceback
from pathlib import Path
from typing import Callable, Optional

import pymupdf

from .config import Settings, get_settings
from .glossary import effective_glossary
from .interfaces import OcrEngine, ProgressCallback, Reviewer, Translator
from .models import (Lang, PipelineOptions, PipelineResult, PipelineStats, QAIssue, QAReport, QARound,
                     SegmentKind, TranslatedDocument)

log = logging.getLogger("mathtrans.pipeline")


class PipelineError(RuntimeError):
    """A fatal, user-facing pipeline failure."""


def _noop_progress(stage: str, message: str, percent: float) -> None:  # pragma: no cover - trivial
    log.info("[%3.0f%%] %s: %s", percent, stage, message)


def _document_context(doc: TranslatedDocument) -> str:
    """A short description of the document given to the translator for context."""
    headings = [s.source_text for s in doc.segments
                if s.kind == SegmentKind.TEXT and s.style.role == "heading" and s.source_text.strip()]
    title = doc.title or (headings[0] if headings else "")
    if not title:
        for s in doc.segments:
            if s.kind == SegmentKind.TEXT and s.translate:
                title = s.source_text[:80]
                break
    doc.title = title
    parts = ["Mathematics learning material (textbook / worksheet)."]
    if title:
        parts.append(f"Title or first heading: {title[:120]}")
    if headings[1:4]:
        parts.append("Other headings: " + " | ".join(h[:60] for h in headings[1:4]))
    return " ".join(parts)


def _atomic_save(doc: pymupdf.Document, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    doc.save(str(tmp), garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, path)


def _write_json(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def run_pipeline(
    source_pdf: str | Path,
    out_dir: str | Path,
    options: PipelineOptions,
    settings: Optional[Settings] = None,
    progress: Optional[ProgressCallback] = None,
    *,
    translator: Optional[Translator] = None,
    reviewer: Optional[Reviewer] = None,
    ocr_engine: Optional[OcrEngine] = None,
) -> PipelineResult:
    """Translate ``source_pdf`` into ``out_dir`` according to ``options``.

    ``translator`` / ``reviewer`` / ``ocr_engine`` override the backends chosen
    from the settings (used by tests and by callers that already hold a client).
    """
    from .extract import extract_document
    from .layout import render_document, render_page_previews
    from .qa.checks import output_checks
    from .qa.loop import run_qa_loop
    from .qa.report import report_markdown, summarize
    from .translate import get_reviewer, get_translator, translate_segments

    t0 = time.time()
    settings = settings or get_settings()
    report_progress = progress or _noop_progress
    source_pdf = Path(source_pdf)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / "output.pdf"
    stats = PipelineStats(target_lang=options.target_lang.value)

    try:
        if not source_pdf.is_file():
            raise PipelineError(f"Source file not found: {source_pdf}")
        with source_pdf.open("rb") as fh:
            if fh.read(5) != b"%PDF-":
                raise PipelineError("Source file is not a PDF")

        # ------------------------------------------------------------ extract
        report_progress("extract", "Extracting text and layout", 1)
        doc = extract_document(source_pdf, target_lang=options.target_lang,
                               source_lang=options.source_lang, pages=options.pages)
        if doc.source_lang == options.target_lang:
            raise PipelineError(
                f"Source language ({doc.source_lang.value}) equals the target language; choose a different target")
        glossary = effective_glossary(options.glossary, options.use_default_glossary)
        doc.glossary = glossary
        pairs = glossary.pairs(doc.source_lang, doc.target_lang)
        stats.pages = doc.page_count
        stats.source_lang = doc.source_lang.value
        stats.text_segments = len(doc.text_segments())
        report_progress("extract", f"{stats.text_segments} text blocks on {stats.pages} pages "
                                   f"(source language: {doc.source_lang.value})", 5)

        # ---------------------------------------------------------------- ocr
        engine_name = "none"
        if options.translate_images:
            from .images import extract_image_segments
            from .ocr import get_ocr_engine

            engine = ocr_engine or get_ocr_engine(settings.resolved_ocr(options.ocr_engine), settings)
            if engine is not None and engine.name != "none":
                engine_name = engine.name
                report_progress("ocr", f"Recognising text inside images ({engine_name})", 7)
                image_segments = extract_image_segments(source_pdf, doc, engine, pages=options.pages)
                doc.segments.extend(image_segments)
                stats.image_segments = len(image_segments)
                stats.images_processed = len({s.image.xref for s in image_segments if s.image})
            else:
                report_progress("ocr", "No OCR engine available; text inside images is kept as is", 10)
        stats.ocr_engine = engine_name
        report_progress("ocr", f"{stats.image_segments} text regions found in images", 15)

        # ---------------------------------------------------------- translate
        translator_name = settings.resolved_translator(options.translator)
        if translator is None:
            translator = get_translator(translator_name, settings, model=options.model)
        else:
            translator_name = getattr(translator, "name", translator_name)
        if reviewer is None and options.llm_review and translator_name == "claude":
            reviewer = get_reviewer("claude", settings, model=options.model)
        stats.translator = translator_name
        stats.model = options.model or (settings.claude_model if translator_name == "claude" else "")
        doc_context = _document_context(doc)
        translatable = doc.translatable()
        stats.skipped = len(doc.segments) - len(translatable)

        def translate_progress(done: int, total: int) -> None:
            pct = 15 + 30 * (done / max(total, 1))
            report_progress("translate", f"Translated {done}/{total} segments", pct)

        report_progress("translate", f"Translating {len(translatable)} segments ({translator_name})", 16)
        translate_segments(doc, translator, max_chars=settings.batch_chars, doc_context=doc_context,
                           progress=translate_progress)
        stats.translated = sum(1 for s in translatable if s.translated_text is not None)
        report_progress("translate", f"{stats.translated}/{len(translatable)} segments translated", 45)

        # ------------------------------------------------------------- layout
        def render_all(message: str = "Laying out translated text") -> None:
            report_progress("layout", message, 60)
            render_document(source_pdf, doc, out_pdf, min_font_scale=options.min_font_scale,
                            fonts_dir=settings.fonts_dir, pages=options.pages)
            image_targets = [s for s in doc.image_segments() if s.translated_text and s.translate]
            if image_targets:
                from .images import render_image_segments

                pdf_doc = pymupdf.open(str(out_pdf))
                try:
                    n = render_image_segments(pdf_doc, doc, fonts_dir=settings.fonts_dir)
                    log.info("replaced text in %d images", n)
                    _atomic_save(pdf_doc, out_pdf)
                finally:
                    if not pdf_doc.is_closed:
                        pdf_doc.close()

        render_all()

        # ------------------------------------------------------------ QA loop
        def retranslate(ids: list[str]) -> None:
            for seg in doc.segments:
                if seg.id in ids:
                    seg.render = None
            report_progress("qa", f"Re-translating {len(ids)} segments with QA feedback", 55)
            translate_segments(doc, translator, max_chars=settings.batch_chars, doc_context=doc_context,
                               only_ids=ids)
            render_all("Re-laying out corrected segments")

        def qa_progress(stage: str, message: str, percent: float) -> None:
            report_progress("qa", message, 45 + 25 * max(0.0, min(percent, 100.0)) / 100.0)

        report_progress("qa", "Running automatic quality checks", 46)
        report = run_qa_loop(doc, options, glossary_pairs=pairs, retranslate=retranslate,
                             reviewer=reviewer, progress=qa_progress)
        stats.qa_rounds = len(report.rounds)
        report_progress("qa", summarize(report), 70)

        # ------------------------------------------------------ output checks
        report_progress("check", "Verifying the output file", 86)
        out_issues: list[QAIssue] = output_checks(out_pdf, source_pdf, doc)
        if out_issues:
            errs = [i for i in out_issues if i.severity == "error"]
            report.rounds.append(QARound(round=len(report.rounds) + 1, issues=out_issues,
                                         retranslated=[], passed=not errs))
            report.final_issues = [i for i in report.final_issues if i.severity != "error"] + out_issues \
                if report.passed else report.final_issues + out_issues
            report.errors = sum(1 for i in report.final_issues if i.severity == "error")
            report.warnings = sum(1 for i in report.final_issues if i.severity == "warning")
            if errs:
                report.passed = False
            report.summary = summarize(report)
        if "output_checks" not in report.checks_run:
            report.checks_run.append("output_checks")
        report.duration_s = round(time.time() - t0, 2)
        report_progress("check", summarize(report), 90)

        # ------------------------------------------------------------ exports
        result = PipelineResult(status="completed", output_pdf=str(out_pdf), qa_report=report, stats=stats)
        _write_json(out_dir / "segments.json", doc.model_dump_json(indent=1))
        result.segments_json = str(out_dir / "segments.json")
        _write_json(out_dir / "qa_report.json", report.model_dump_json(indent=1))
        result.qa_report_json = str(out_dir / "qa_report.json")
        try:
            (out_dir / "qa_report.md").write_text(report_markdown(report, doc), encoding="utf-8")
        except Exception:  # pragma: no cover - report rendering must never break the run
            log.exception("could not render the markdown QA report")

        if options.bilingual:
            from .export import make_bilingual_pdf

            report_progress("export", "Building the bilingual side-by-side PDF", 92)
            result.bilingual_pdf = make_bilingual_pdf(source_pdf, out_pdf, out_dir / "bilingual.pdf")
        if options.export_docx:
            from .export import export_docx

            report_progress("export", "Exporting the Word document", 95)
            result.docx = export_docx(out_pdf, out_dir / "output.docx", doc)
        report_progress("export", "Exports written", 97)

        # ----------------------------------------------------------- previews
        report_progress("preview", "Rendering page previews", 98)
        preview_dir = out_dir / "previews"
        if preview_dir.exists():
            shutil.rmtree(preview_dir)
        result.preview_pages = render_page_previews(out_pdf, preview_dir, dpi=options.preview_dpi)

        stats.duration_s = round(time.time() - t0, 2)
        if options.require_qa_pass and not report.passed:
            result.status = "qa_failed"
            result.error = f"QA did not pass: {summarize(report)}"
        report_progress("done", summarize(report), 100)
        return result

    except Exception as exc:  # noqa: BLE001 - converted into a result for the caller
        log.error("pipeline failed: %s\n%s", exc, traceback.format_exc())
        stats.duration_s = round(time.time() - t0, 2)
        try:
            (out_dir / "error.txt").write_text(f"{exc}\n\n{traceback.format_exc()}", encoding="utf-8")
        except OSError:  # pragma: no cover
            pass
        report_progress("error", str(exc), 100)
        return PipelineResult(status="error", error=str(exc), stats=stats)


__all__ = ["run_pipeline", "PipelineError"]
