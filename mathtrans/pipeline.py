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
from .languages import detect_language
from .interfaces import OcrEngine, ProgressCallback, Reviewer, TranslationError, Translator
from .models import (Lang, PipelineOptions, PipelineResult, PipelineStats, QAIssue, SegmentKind,
                     TranslatedDocument)

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


def _effective_pages(source_pdf: Path, options: PipelineOptions) -> tuple[Optional[list[int]], int, int]:
    """Pages to process (None = all) after applying ``options.pages`` and
    ``options.skip_pages``; also returns how many pages are skipped and the
    document's page count."""
    with pymupdf.open(str(source_pdf)) as pdf:
        n = pdf.page_count
    base = options.pages if options.pages is not None else list(range(n))
    skip = {p for p in (options.skip_pages or []) if 0 <= p < n}
    if not skip:
        return options.pages, 0, n
    return [p for p in base if p not in skip], len(set(base) & skip), n


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
    _cb = progress or _noop_progress
    _last_pct = [0.0]

    def report_progress(stage: str, message: str, percent: float) -> None:
        # never let the reported percentage run backwards (re-layouts during QA, re-translations)
        pct = max(_last_pct[0], float(percent))
        _last_pct[0] = pct
        _cb(stage, message, pct)
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
        pages, stats.pages_skipped, total_pages = _effective_pages(source_pdf, options)
        if pages is not None and not pages:
            raise PipelineError("every page is excluded by the page selection; nothing to translate")
        # Memory grows with every rendered page (and with every segment, see layout.py), so a
        # document is refused before any work starts when it exceeds the configured page limit.
        max_pages = int(getattr(settings, "max_pages", 0) or 0)
        n_pages = len(set(pages)) if pages is not None else total_pages
        if max_pages and n_pages > max_pages:
            raise PipelineError(f"{n_pages} pages to translate exceed the limit of {max_pages} pages "
                                f"(MATHTRANS_MAX_PAGES); split the document, select fewer pages or raise the limit")
        doc = extract_document(source_pdf, target_lang=options.target_lang,
                               source_lang=options.source_lang, pages=pages)
        if doc.text_segments() and doc.source_lang == options.target_lang:
            raise PipelineError(
                f"Source language ({doc.source_lang.value}) equals the target language; choose a different target")
        glossary = effective_glossary(options.glossary, options.use_default_glossary)
        doc.glossary = glossary
        stats.pages = doc.page_count
        stats.source_lang = doc.source_lang.value
        stats.text_segments = len(doc.text_segments())
        report_progress("extract", f"{stats.text_segments} text blocks on {stats.pages} pages "
                                   f"(source language: {doc.source_lang.value})", 5)

        # ---------------------------------------------------------------- ocr
        engine_name = "none"
        if options.translate_images:
            from .images import extract_image_segments
            from .ocr import OcrUnavailableError, get_ocr_engine, ocr_low_trust

            requested_engine = settings.resolved_ocr(options.ocr_engine)
            max_image_px = int(settings.max_image_megapixels * 1_000_000)
            # The automatic choice depends on the source language (ja/ko prefer Claude vision).
            engine = ocr_engine or get_ocr_engine(requested_engine, settings, source_lang=doc.source_lang)
            if engine is not None and engine.name != "none":
                engine_name = engine.name
                try:
                    if not doc.text_segments() and options.source_lang is None:
                        # Scanned document (no text layer): detect the language from the OCR text
                        # of the first pages before classifying every image region.
                        probe_pages = (pages if pages is not None else list(range(doc.page_count)))[:2]
                        report_progress("ocr", "Scanned document: detecting the source language", 6)
                        probe = extract_image_segments(source_pdf, doc, engine, pages=probe_pages,
                                                       max_image_px=max_image_px)
                        detected = detect_language(" ".join(seg.source_text for seg in probe))
                        if detected is not None and detected != doc.source_lang:
                            log.info("scanned document: source language %s detected from OCR text (was %s)",
                                     detected.value, doc.source_lang.value)
                            doc.source_lang = detected
                            stats.source_lang = detected.value
                            if ocr_engine is None:  # re-pick: the automatic choice depends on the language
                                engine = get_ocr_engine(requested_engine, settings, source_lang=detected)
                                engine_name = engine.name
                        if doc.source_lang == options.target_lang:
                            raise PipelineError(
                                f"Source language ({doc.source_lang.value}) equals the target language; "
                                "choose a different target")
                    doc.ocr_low_trust = ocr_low_trust(engine, doc.source_lang)
                    if doc.ocr_low_trust:
                        log.warning("text inside images of this %s document is read by the offline Chinese/English "
                                    "OCR models, which read it unreliably; QA will flag every translated image "
                                    "label (use MATHTRANS_OCR_ENGINE=claude / --ocr-engine claude with an API key)",
                                    doc.source_lang.value)
                    report_progress("ocr", f"Recognising text inside images ({engine_name})", 7)
                    image_segments = extract_image_segments(source_pdf, doc, engine, pages=pages,
                                                            max_image_px=max_image_px, failures=doc.ocr_failures)
                except OcrUnavailableError as exc:
                    raise PipelineError(str(exc)) from exc
                doc.segments.extend(image_segments)
                stats.image_segments = len(image_segments)
                stats.images_processed = len({s.image.xref for s in image_segments if s.image})
                stats.ocr_failures = len(doc.ocr_failures)
                if options.scanned_mode == "overlay":
                    from .scanned import build_overlay_segments, scanned_pages

                    scanned = scanned_pages(source_pdf, pages)
                    if scanned:
                        paragraphs = build_overlay_segments(doc, scanned)
                        doc.segments.extend(paragraphs)
                        stats.text_segments += len(paragraphs)
                        report_progress("ocr", f"{len(paragraphs)} paragraphs assembled from OCR lines on "
                                               f"{len(scanned)} scanned page(s) (overlay mode)", 14)
            else:
                report_progress("ocr", "No OCR engine available; text inside images is kept as is", 10)
        stats.ocr_engine = engine_name
        pairs = glossary.pairs(doc.source_lang, doc.target_lang)
        found = f"{stats.image_segments} text regions found in images"
        if stats.ocr_failures:
            found += f"; OCR failed on {stats.ocr_failures} image(s)"
        report_progress("ocr", found, 15)
        nothing_to_translate: Optional[str] = None  # set when the run legitimately translates nothing
        if not doc.translatable():
            ocr_why = ("translation of text inside images is disabled" if not options.translate_images
                       else "no OCR engine is available" if engine_name == "none"
                       else f"OCR failed on {len(doc.ocr_failures)} image(s): {doc.ocr_failures[0]}"
                       if doc.ocr_failures else "")
            if not doc.text_segments():
                # No text layer at all: a scanned document whose images were not read, or a blank one.
                if engine_name == "none":
                    raise PipelineError(
                        f"The PDF has no text layer (scanned document) and {ocr_why}: enable OCR "
                        "(translate_images / MATHTRANS_OCR_ENGINE=rapid with rapidocr-onnxruntime installed, or "
                        "=claude with an API key) or supply a PDF with a text layer")
                if doc.ocr_failures:
                    raise PipelineError(f"The PDF has no text layer (scanned document) and {ocr_why}")
                raise PipelineError("No translatable text was found in the selected pages")
            # The text layer exists but every block is numbers / formulas / labels. That is a legitimate
            # document (a formula sheet: the output equals the source and QA says so below) unless the
            # pages carry images whose text was never read: then an untranslated scan would be served as
            # if it were done, which is exactly what the mandatory QA gate must prevent.
            processed = set(pages) if pages is not None else None
            n_images = sum(len(p.image_bboxes) for p in doc.pages if processed is None or p.index in processed)
            if n_images and ocr_why:
                raise PipelineError(
                    f"The text layer of the selected pages contains only numbers / formulas and the text inside "
                    f"their {n_images} image(s) was not recognised ({ocr_why}); enable image translation / OCR "
                    "(translate_images / MATHTRANS_OCR_ENGINE) and run again")
            nothing_to_translate = (
                f"Nothing to translate: the {stats.text_segments} text block(s) of the selected pages contain only "
                f"numbers, formulas or labels and no text was found inside images; the output is identical to "
                f"the source")
            log.warning(nothing_to_translate)

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
                            fonts_dir=settings.fonts_dir, pages=pages,
                            checkpoint_pages=int(getattr(settings, "render_checkpoint_pages", 25) or 0))
            image_targets = [s for s in doc.image_segments() if s.translated_text and s.translate]
            from .scanned import MERGED

            merged = any(s.kind == SegmentKind.IMAGE_TEXT and s.skip_reason.startswith(MERGED)
                         for s in doc.segments)
            if image_targets or merged:
                from .images import render_image_segments
                from .scanned import erase_merged_lines

                pdf_doc = pymupdf.open(str(out_pdf))
                try:
                    if merged:
                        log.info("erased OCR lines in %d scanned page images", erase_merged_lines(pdf_doc, doc))
                    if image_targets:
                        log.info("replaced text in %d images", render_image_segments(pdf_doc, doc,
                                                                                     fonts_dir=settings.fonts_dir))
                    _atomic_save(pdf_doc, out_pdf)
                finally:
                    if not pdf_doc.is_closed:
                        pdf_doc.close()

        render_all()

        # ------------------------------------------------------------ QA loop
        def retranslate(ids: list[str]) -> None:
            wanted = set(ids)
            targets = [seg for seg in doc.segments if seg.id in wanted]
            # translate_segments applies the results chunk by chunk; a backend failure half-way through
            # must leave the document exactly as it was rendered and checked (output.pdf is not re-laid
            # out after the failure), so segments.json and the QA report keep describing that file.
            snapshot = {seg.id: (seg.translation_raw, seg.translated_text, seg.attempts, list(seg.feedback),
                                 seg.render) for seg in targets}
            for seg in targets:
                seg.render = None
            report_progress("qa", f"Re-translating {len(ids)} segments with QA feedback", 55)
            try:
                translate_segments(doc, translator, max_chars=settings.batch_chars, doc_context=doc_context,
                                   only_ids=ids)
            except TranslationError:
                for seg in targets:
                    (seg.translation_raw, seg.translated_text, seg.attempts,
                     seg.feedback, seg.render) = snapshot[seg.id]
                raise
            render_all("Re-laying out corrected segments")

        def qa_progress(stage: str, message: str, percent: float) -> None:
            report_progress("qa", message, 45 + 25 * max(0.0, min(percent, 100.0)) / 100.0)

        report_progress("qa", "Running automatic quality checks", 46)
        report = run_qa_loop(doc, options, glossary_pairs=pairs, retranslate=retranslate,
                             reviewer=reviewer, progress=qa_progress)
        if nothing_to_translate:
            # Say so in the report instead of a bare "QA passed" over zero segments.
            issue = QAIssue(check="completeness", severity="warning", fixable=False, message=nothing_to_translate)
            report.rounds[-1].issues.append(issue)
            report.final_issues.append(issue)
            report.warnings += 1
            report.summary = summarize(report)
        stats.qa_rounds = len(report.rounds)
        report_progress("qa", summarize(report), 70)

        # ------------------------------------------------------ output checks
        if options.subset_fonts:
            report_progress("layout", "Subsetting embedded fonts", 85)
            try:
                pdf_doc = pymupdf.open(str(out_pdf))
                pdf_doc.subset_fonts()
                _atomic_save(pdf_doc, out_pdf)
            except Exception as exc:  # noqa: BLE001 - subsetting is an optimisation, never fatal
                log.warning("font subsetting failed; keeping fully embedded fonts: %s", exc)
        report_progress("check", "Verifying the output file", 86)
        out_issues: list[QAIssue] = output_checks(out_pdf, source_pdf, doc)
        out_errors = sum(1 for i in out_issues if i.severity == "error")
        out_warnings = len(out_issues) - out_errors
        report.final_issues = list(report.final_issues) + out_issues
        report.errors = sum(1 for i in report.final_issues if i.severity == "error")
        report.warnings = sum(1 for i in report.final_issues if i.severity == "warning")
        if out_errors:
            report.passed = False
        if "output_checks" not in report.checks_run:
            report.checks_run.append("output_checks")
        report.duration_s = round(time.time() - t0, 2)
        report.summary = (f"{summarize(report)}; output file checks: "
                          f"{out_errors} error(s), {out_warnings} warning(s)")
        report_progress("check", report.summary, 90)

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
            result.error = f"QA did not pass: {report.summary}"
        report_progress("done", report.summary, 100)
        return result

    except Exception as exc:  # noqa: BLE001 - converted into a result for the caller
        if isinstance(exc, PipelineError):
            log.error("pipeline failed: %s", exc)
        else:
            log.error("pipeline failed: %s: %s", type(exc).__name__, exc)
        log.debug("pipeline traceback:\n%s", traceback.format_exc())
        stats.duration_s = round(time.time() - t0, 2)
        try:
            (out_dir / "error.txt").write_text(f"{exc}\n\n{traceback.format_exc()}", encoding="utf-8")
        except OSError:  # pragma: no cover
            pass
        report_progress("error", str(exc), 100)
        return PipelineResult(status="error", error=str(exc), stats=stats)


__all__ = ["run_pipeline", "PipelineError"]
