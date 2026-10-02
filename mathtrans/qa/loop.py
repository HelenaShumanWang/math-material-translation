"""The QA loop: check, feed back, re-translate, repeat.

Round ``r`` (1 .. ``options.max_qa_rounds``) collects the rule-check issues, the
findings of the optional LLM reviewer and the issues of an optional render
check. The round passes when no issue has severity ``error``. Otherwise every
*fixable* error that names a segment has its message appended to that segment's
``feedback`` (de-duplicated; warnings about the same segment are added as extra
hints), the previous translation is kept as ``previous`` for the translator, and
``retranslate(ids)`` is called before the next round. Issues without a segment
or marked ``fixable=False`` never trigger a re-translation; when nothing can be
fixed the loop stops early.

This module never imports the translation or layout packages - it only calls
the callbacks it is given.
"""
from __future__ import annotations

import logging
import time
from typing import Callable, Iterable, Optional

from ..interfaces import ProgressCallback, Reviewer, TranslationError
from ..models import (PipelineOptions, QAIssue, QAReport, QARound, ReviewFinding, ReviewItem, SegmentKind,
                      TextSegment, TranslatedDocument)
from .checks import check_names, rule_checks
from .report import summarize

log = logging.getLogger("mathtrans.qa.loop")

RetranslateCallback = Callable[[list[str]], None]
RenderCheck = Callable[[TranslatedDocument], list[QAIssue]]

REVIEW_ERROR_CATEGORIES = frozenset({"meaning", "omission", "number", "terminology", "untranslated", "format"})
"""Reviewer finding categories reported as errors; every other category is a warning."""
REVIEW_CHECK_NAME = "llm_review"
RENDER_CHECK_NAME = "render_check"
RETRANSLATE_CHECK_NAME = "retranslate"
REVIEW_BATCH_ITEMS = 60
REVIEW_BATCH_CHARS = 12000


def _review_context(seg: TextSegment) -> str:
    if seg.kind == SegmentKind.IMAGE_TEXT:
        return "label inside a figure image"
    context = seg.style.role if seg.style.role != "body" else "paragraph"
    return context + (", vertical text" if seg.style.is_vertical else "")


def _review_batches(items: list[ReviewItem]) -> Iterable[list[ReviewItem]]:
    batch: list[ReviewItem] = []
    chars = 0
    for item in items:
        size = len(item.source) + len(item.translation)
        if batch and (len(batch) >= REVIEW_BATCH_ITEMS or chars + size > REVIEW_BATCH_CHARS):
            yield batch
            batch, chars = [], 0
        batch.append(item)
        chars += size
    if batch:
        yield batch


def review_issue(finding: ReviewFinding, segments: dict[str, TextSegment]) -> QAIssue:
    """Map a reviewer finding to a QA issue (severity by category, see
    :data:`REVIEW_ERROR_CATEGORIES`)."""
    category = (finding.category or "other").strip().lower() or "other"
    severity = "error" if category in REVIEW_ERROR_CATEGORIES else "warning"
    seg = segments.get(finding.id)
    text = finding.message.strip() or "the translation was flagged without an explanation"
    message = f"Reviewer ({category}): {text}"
    suggested = (finding.suggested_fix or "").strip()
    if suggested:
        message += f' Suggested translation: "{suggested}"'
    if seg is None:
        log.warning("reviewer finding for unknown segment id %r ignored for feedback", finding.id)
    return QAIssue(
        check=REVIEW_CHECK_NAME, severity=severity, message=message,
        segment_id=seg.id if seg else None, page=seg.page if seg else None,
        details={"category": category, "reviewer_severity": finding.severity,
                 "suggested_fix": suggested or None, "reviewer_id": finding.id},
        fixable=seg is not None,
    )


def _review_failure(batch: list[ReviewItem], exc: BaseException) -> QAIssue:
    return QAIssue(
        check=REVIEW_CHECK_NAME, severity="warning", fixable=False,
        message=f"LLM review of {len(batch)} segment(s) failed and was skipped: {exc}",
        details={"segment_ids": [item.id for item in batch], "error": f"{type(exc).__name__}: {exc}"})


def review_document(doc: TranslatedDocument, reviewer: Reviewer, glossary_pairs: list[tuple[str, str]]) -> list[QAIssue]:
    """Run the LLM reviewer over all translated segments.

    The reviewer is advisory: a failing or malformed review call never raises.
    It is logged and reported as one unfixable ``llm_review`` warning per batch,
    so the report shows that those segments were not reviewed.
    """
    segments = {s.id: s for s in doc.segments if s.translate}
    items = [ReviewItem(id=s.id, source=s.source_text, translation=s.translated_text or "",
                        context=_review_context(s))
             for s in segments.values() if s.translated_text is not None and s.translated_text.strip()]
    if not items:
        return []
    issues: list[QAIssue] = []
    for batch in _review_batches(items):
        try:
            findings = reviewer.review(batch, doc.source_lang, doc.target_lang, glossary_pairs)
            mapped = [review_issue(f if isinstance(f, ReviewFinding) else ReviewFinding.model_validate(f), segments)
                      for f in (findings or [])]
        except Exception as exc:  # noqa: BLE001 - the reviewer is advisory, never fatal
            log.warning("LLM review of %d segment(s) failed and is skipped: %s", len(batch), exc)
            issues.append(_review_failure(batch, exc))
            continue
        issues.extend(mapped)
    log.info("LLM review (%s): %d finding(s) on %d segment(s)", getattr(reviewer, "name", "?"), len(issues), len(items))
    return issues


def apply_feedback(doc: TranslatedDocument, issues: list[QAIssue]) -> list[str]:
    """Append issue messages to the ``feedback`` of segments that must be re-translated.

    A segment is re-translated when at least one fixable error names it; every
    fixable issue (errors and warnings) about such a segment becomes feedback,
    without duplicates. Unfixable issues are never fed back - by definition the
    translator cannot act on them. Returns the sorted ids to re-translate.
    """
    segments = {s.id: s for s in doc.segments if s.translate}
    targets: dict[str, TextSegment] = {}
    for issue in issues:
        if issue.severity == "error" and issue.fixable and issue.segment_id in segments:
            targets[issue.segment_id] = segments[issue.segment_id]  # type: ignore[index]
    for issue in issues:
        seg = targets.get(issue.segment_id or "")
        if seg is not None and issue.fixable and issue.message not in seg.feedback:
            seg.feedback.append(issue.message)
    return sorted(targets)


def _count(issues: list[QAIssue], severity: str) -> int:
    return sum(1 for i in issues if i.severity == severity)


def run_qa_loop(
    doc: TranslatedDocument,
    options: PipelineOptions,
    *,
    glossary_pairs: list[tuple[str, str]],
    retranslate: RetranslateCallback,
    reviewer: Optional[Reviewer] = None,
    render_check: Optional[RenderCheck] = None,
    progress: Optional[ProgressCallback] = None,
) -> QAReport:
    """Run up to ``options.max_qa_rounds`` rounds of checks with feedback-driven
    re-translation and return the report (``final_issues`` = issues of the last round).

    ``retranslate(ids)`` must translate those segments again using their
    ``feedback`` (the pipeline wires it to ``translate_segments(only_ids=ids)`` and
    re-renders). ``reviewer`` is used only when ``options.llm_review`` is true.
    ``render_check(doc)`` may contribute layout issues each round.
    """
    t0 = time.perf_counter()
    max_rounds = max(1, int(options.max_qa_rounds))
    use_reviewer = reviewer is not None and options.llm_review
    checks_run = check_names()
    if use_reviewer:
        checks_run.append(REVIEW_CHECK_NAME)
    if render_check is not None:
        checks_run.append(RENDER_CHECK_NAME)
    report = QAReport(checks_run=checks_run)

    def notify(message: str, fraction: float) -> None:
        if progress is not None:
            progress("qa", message, 100.0 * max(0.0, min(fraction, 1.0)))

    for r in range(1, max_rounds + 1):
        round_start = time.perf_counter()
        notify(f"QA round {r}/{max_rounds}: running checks", (r - 1) / max_rounds)
        issues = rule_checks(doc, options, glossary_pairs)
        if use_reviewer:
            issues.extend(review_document(doc, reviewer, glossary_pairs))  # type: ignore[arg-type]
        if render_check is not None:
            issues.extend(render_check(doc))
        n_err, n_warn = _count(issues, "error"), _count(issues, "warning")
        current = QARound(round=r, issues=issues, passed=n_err == 0)
        report.rounds.append(current)
        log.info("QA round %d/%d: %d error(s), %d warning(s)", r, max_rounds, n_err, n_warn)
        if current.passed:
            notify(f"QA round {r}/{max_rounds}: passed ({n_warn} warning(s))", r / max_rounds)
            current.duration_s = round(time.perf_counter() - round_start, 3)
            break
        if r >= max_rounds:
            notify(f"QA round {r}/{max_rounds}: {n_err} error(s) remain after the last round", 1.0)
            current.duration_s = round(time.perf_counter() - round_start, 3)
            break
        ids = apply_feedback(doc, issues)
        if not ids:
            log.warning("QA round %d: %d error(s) but none can be fixed by re-translation; stopping", r, n_err)
            notify(f"QA round {r}/{max_rounds}: {n_err} error(s) cannot be fixed by re-translation", 1.0)
            current.duration_s = round(time.perf_counter() - round_start, 3)
            break
        current.retranslated = ids
        notify(f"QA round {r}/{max_rounds}: re-translating {len(ids)} segment(s) with feedback", (r - 0.5) / max_rounds)
        try:
            retranslate(ids)
        except TranslationError as exc:
            log.error("re-translation after QA round %d failed: %s", r, exc)
            current.issues.append(QAIssue(
                check=RETRANSLATE_CHECK_NAME, severity="error", fixable=False,
                message=f"Re-translation of {len(ids)} segment(s) failed: {exc}", details={"segment_ids": ids}))
            current.duration_s = round(time.perf_counter() - round_start, 3)
            break
        current.duration_s = round(time.perf_counter() - round_start, 3)

    last = report.rounds[-1]
    report.final_issues = list(last.issues)
    report.passed = last.passed
    report.errors = _count(report.final_issues, "error")
    report.warnings = _count(report.final_issues, "warning")
    report.duration_s = round(time.perf_counter() - t0, 3)
    report.summary = summarize(report)
    log.info("%s", report.summary)
    return report


__all__ = ["run_qa_loop", "apply_feedback", "review_document", "review_issue", "REVIEW_ERROR_CATEGORIES"]
