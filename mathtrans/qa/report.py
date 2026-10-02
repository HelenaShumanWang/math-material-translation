"""Human-readable rendering of :class:`~mathtrans.models.QAReport`."""
from __future__ import annotations

from collections import Counter
from typing import Optional

from ..models import QAIssue, QAReport, TranslatedDocument

EXCERPT_CHARS = 60


def _plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def _counts(report: QAReport) -> tuple[int, int]:
    if report.final_issues:
        return (sum(1 for i in report.final_issues if i.severity == "error"),
                sum(1 for i in report.final_issues if i.severity == "warning"))
    return report.errors, report.warnings


def summarize(report: QAReport) -> str:
    """One line such as ``QA passed after 2 rounds: 0 errors, 1 warning (3.4 s)``."""
    if not report.rounds:
        return "QA not run"
    errors, warnings = _counts(report)
    status = "passed" if report.passed else "FAILED"
    text = f"QA {status} after {_plural(len(report.rounds), 'round')}: {_plural(errors, 'error')}, {_plural(warnings, 'warning')}"
    if report.duration_s:
        text += f" ({report.duration_s:.1f} s)"
    return text


def issues_by_page(report: QAReport) -> dict[Optional[int], list[QAIssue]]:
    """Final issues grouped by 0-based page (document-level issues under ``None``, last)."""
    grouped: dict[Optional[int], list[QAIssue]] = {}
    for issue in report.final_issues:
        grouped.setdefault(issue.page, []).append(issue)
    ordered = sorted((k for k in grouped if k is not None))
    out: dict[Optional[int], list[QAIssue]] = {k: grouped[k] for k in ordered}
    if None in grouped:
        out[None] = grouped[None]
    return out


def _cell(text: str, limit: int = 0) -> str:
    t = " ".join(str(text).split()).replace("|", "\\|")
    if limit and len(t) > limit:
        t = t[: limit - 1] + "…"
    return t


def _check_breakdown(issues: list[QAIssue]) -> str:
    counts = Counter(i.check for i in issues)
    return ", ".join(f"{name} ×{n}" for name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def report_markdown(report: QAReport, doc: Optional[TranslatedDocument] = None) -> str:
    """Markdown report: summary, per-round table, final issues grouped by check with
    page, segment and source/translation excerpts (when ``doc`` is given)."""
    lines: list[str] = ["# QA report", "", f"**Result:** {report.summary or summarize(report)}", ""]
    if doc is not None:
        lines += [f"**Document:** {doc.title or doc.source_path} ({doc.source_lang.value} → {doc.target_lang.value}, "
                  f"{doc.page_count} page(s), {len(doc.translatable())} translatable segment(s))", ""]
    if report.checks_run:
        lines += ["**Checks run:** " + ", ".join(f"`{c}`" for c in report.checks_run), ""]

    lines += ["## Rounds", "", "| Round | Errors | Warnings | Re-translated | Passed | Duration |",
              "|---|---|---|---|---|---|"]
    for rnd in report.rounds:
        errors = sum(1 for i in rnd.issues if i.severity == "error")
        warnings = sum(1 for i in rnd.issues if i.severity == "warning")
        lines.append(f"| {rnd.round} | {errors} | {warnings} | {len(rnd.retranslated)} segment(s) | "
                     f"{'yes' if rnd.passed else 'no'} | {rnd.duration_s:.1f} s |")
    if not report.rounds:
        lines.append("| – | – | – | – | – | – |")
    lines.append("")
    for rnd in report.rounds:
        if rnd.issues:
            lines.append(f"- Round {rnd.round}: {_check_breakdown(rnd.issues)}")
    if any(r.issues for r in report.rounds):
        lines.append("")

    lines += [f"## Final issues ({len(report.final_issues)})", ""]
    if not report.final_issues:
        lines += ["No issues.", ""]
        return "\n".join(lines)
    by_check: dict[str, list[QAIssue]] = {}
    for issue in report.final_issues:
        by_check.setdefault(issue.check, []).append(issue)
    severity_rank = {"error": 0, "warning": 1}
    for check, issues in sorted(by_check.items(), key=lambda kv: (min(severity_rank[i.severity] for i in kv[1]), kv[0])):
        errors = sum(1 for i in issues if i.severity == "error")
        warnings = len(issues) - errors
        lines += [f"### `{check}` — {_plural(errors, 'error')}, {_plural(warnings, 'warning')}", "",
                  "| Severity | Page | Segment | Message | Source | Translation |", "|---|---|---|---|---|---|"]
        for issue in sorted(issues, key=lambda i: (severity_rank[i.severity], i.page if i.page is not None else -1,
                                                   i.segment_id or "")):
            page = "" if issue.page is None else str(issue.page + 1)
            source = translation = ""
            seg = doc.segment(issue.segment_id) if (doc is not None and issue.segment_id) else None
            if seg is not None:
                source = _cell(seg.source_text, EXCERPT_CHARS)
                translation = _cell(seg.translated_text or "", EXCERPT_CHARS)
            lines.append(f"| {issue.severity} | {page} | {_cell(issue.segment_id or '')} | {_cell(issue.message)} | "
                         f"{source} | {translation} |")
        lines.append("")
    return "\n".join(lines)


__all__ = ["report_markdown", "summarize", "issues_by_page"]
