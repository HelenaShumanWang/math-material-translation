"""Automatic multi-dimensional QA: rule checks, LLM review loop and reporting.

Public API
----------
* :func:`mathtrans.qa.checks.rule_checks` / :data:`mathtrans.qa.checks.CHECKS` -
  rule-based checks on a :class:`~mathtrans.models.TranslatedDocument`.
* :func:`mathtrans.qa.checks.output_checks` - checks on the exported PDF against
  the source PDF (page count, geometry, extractable text, leftovers, fonts).
* :func:`mathtrans.qa.loop.run_qa_loop` - the check / feedback / re-translate loop.
* :func:`mathtrans.qa.report.report_markdown`, :func:`~mathtrans.qa.report.summarize`,
  :func:`~mathtrans.qa.report.issues_by_page` - report rendering.
"""
from .checks import CHECKS, check_names, output_checks, rule_checks
from .loop import run_qa_loop
from .report import issues_by_page, report_markdown, summarize

__all__ = [
    "CHECKS",
    "check_names",
    "rule_checks",
    "output_checks",
    "run_qa_loop",
    "report_markdown",
    "summarize",
    "issues_by_page",
]
