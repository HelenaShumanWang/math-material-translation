"""Command-line interface: ``python -m mathtrans.cli`` / ``mathtrans``.

Sub-commands::

    translate IN.pdf --to en [--from zh] [--glossary g.csv] [--out DIR] [--bilingual] [--docx]
              [--no-images] [--translator mock|claude] [--max-rounds N] [--no-require-qa]
    serve [--host H] [--port P]
    sample OUT.pdf [--lang zh]
    glossary-template OUT.csv

``translate`` exits with 0 when the run completed and QA passed, 2 when the
automatic QA did not pass (outputs are still written for inspection) and 1 on
any error.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Callable, Optional, Sequence

from .config import get_settings
from .glossary import glossary_template_csv, load_glossary
from .models import Lang, PipelineOptions, PipelineResult

log = logging.getLogger("mathtrans.cli")

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_QA_FAILED = 2
_MAX_ISSUES_SHOWN = 20
_LANG_CHOICES = [lang.value for lang in Lang]


def _get_runner() -> Callable[..., PipelineResult]:
    """Resolve the pipeline entry point lazily (tests monkeypatch this function)."""
    from .pipeline import run_pipeline

    return run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mathtrans",
        description="Layout-preserving translation of math learning materials (PDF) with automatic QA.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    tr = sub.add_parser("translate", help="translate a PDF (output: editable PDF + QA report)")
    tr.add_argument("input", metavar="IN.pdf", help="source PDF")
    tr.add_argument("--to", required=True, metavar="LANG", help="target language: zh, en, pt, es, ja, ko")
    tr.add_argument("--from", dest="source", metavar="LANG", default=None,
                    help="source language (default: auto-detect)")
    tr.add_argument("--glossary", metavar="FILE", default=None, help="custom glossary (CSV/TSV/JSON)")
    tr.add_argument("--out", metavar="DIR", default=None, help="output directory (default: output/<name>_<lang>)")
    tr.add_argument("--bilingual", action="store_true", help="also write a side-by-side bilingual PDF")
    tr.add_argument("--docx", action="store_true", help="also export a Word document")
    tr.add_argument("--no-images", action="store_true", help="do not translate text inside images")
    tr.add_argument("--translator", choices=["auto", "mock", "claude"], default="auto",
                    help="translation backend (default: auto = claude if an API key is set, else mock)")
    tr.add_argument("--max-rounds", type=int, default=None, metavar="N", help="maximum QA rounds")
    tr.add_argument("--model", metavar="MODEL", default=None,
                    help="Claude model id for translation and review (default: MATHTRANS_CLAUDE_MODEL)")
    tr.add_argument("--subset-fonts", action="store_true",
                    help="subset the embedded fonts (much smaller file; editors can only reuse embedded glyphs)")
    tr.add_argument("--no-require-qa", action="store_true",
                    help="report status 'completed' even when the automatic QA did not pass")
    tr.set_defaults(func=cmd_translate)

    sv = sub.add_parser("serve", help="run the web UI / REST API")
    sv.add_argument("--host", default="127.0.0.1")
    sv.add_argument("--port", type=int, default=8000)
    sv.set_defaults(func=cmd_serve)

    sp = sub.add_parser("sample", help="write a two-page sample textbook PDF")
    sp.add_argument("out", metavar="OUT.pdf")
    sp.add_argument("--lang", default="zh", choices=_LANG_CHOICES, help="language of the sample (default: zh)")
    sp.set_defaults(func=cmd_sample)

    gt = sub.add_parser("glossary-template", help="write a CSV glossary template")
    gt.add_argument("out", metavar="OUT.csv")
    gt.set_defaults(func=cmd_glossary_template)
    return parser


def _fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return EXIT_ERROR


def _print_progress(stage: str, message: str, percent: float) -> None:
    print(f"[{percent:3.0f}%] {stage:<9} {message}", file=sys.stderr, flush=True)


def cmd_translate(args: argparse.Namespace) -> int:
    settings = get_settings()
    source = Path(args.input)
    if not source.is_file():
        return _fail(f"input file not found: {source}")
    with source.open("rb") as fh:
        if fh.read(4) != b"%PDF":
            return _fail(f"not a PDF file: {source}")
    try:
        target = Lang.parse(args.to)
        source_lang = Lang.parse(args.source) if args.source else None
    except ValueError as exc:
        return _fail(str(exc))
    if source_lang is not None and source_lang == target:
        return _fail("--from and --to must differ")
    glossary = None
    if args.glossary:
        try:
            glossary = load_glossary(args.glossary)
        except (OSError, ValueError) as exc:
            return _fail(f"cannot load glossary {args.glossary}: {exc}")
        if not glossary.entries:
            return _fail(f"glossary {args.glossary} contains no entries")
    if args.max_rounds is not None and args.max_rounds < 1:
        return _fail("--max-rounds must be >= 1")

    out_dir = Path(args.out) if args.out else Path("output") / f"{source.stem}_{target.value}"
    options = PipelineOptions(
        target_lang=target,
        source_lang=source_lang,
        glossary=glossary,
        translate_images=not args.no_images,
        bilingual=args.bilingual,
        export_docx=args.docx,
        max_qa_rounds=args.max_rounds if args.max_rounds is not None else settings.max_qa_rounds,
        require_qa_pass=not args.no_require_qa,
        translator=args.translator,
        model=args.model,
        subset_fonts=args.subset_fonts,
        min_font_scale=settings.min_font_scale,
        preview_dpi=settings.preview_dpi,
    )
    runner = _get_runner()
    print(f"Translating {source} -> {target.value} (output: {out_dir})", file=sys.stderr)
    try:
        result = runner(source, out_dir, options, settings=settings, progress=_print_progress)
    except Exception as exc:  # noqa: BLE001 - surfaced as a CLI error, not a traceback
        log.debug("pipeline raised", exc_info=True)
        return _fail(f"translation failed: {exc}")
    print_summary(result, source, target, out_dir)
    if result.status == "completed":
        return EXIT_OK
    if result.status == "qa_failed":
        return EXIT_QA_FAILED
    return EXIT_ERROR


def print_summary(result: PipelineResult, source: Path, target: Lang, out_dir: Path) -> None:
    """Print a human-readable summary of a pipeline result to stdout."""
    stats = result.stats
    src_lang = stats.source_lang or "auto"
    rows: list[tuple[str, str]] = [
        ("Status", result.status),
        ("Source", f"{source} ({src_lang} -> {target.value})"),
        ("Output dir", str(out_dir)),
    ]
    if result.output_pdf:
        rows.append(("Output PDF", result.output_pdf))
    if result.bilingual_pdf:
        rows.append(("Bilingual PDF", result.bilingual_pdf))
    if result.docx:
        rows.append(("Word (DOCX)", result.docx))
    if result.segments_json:
        rows.append(("Segments JSON", result.segments_json))
    if result.qa_report_json:
        rows.append(("QA report", result.qa_report_json))
    if result.preview_pages:
        rows.append(("Previews", f"{len(result.preview_pages)} page(s) in {Path(result.preview_pages[0]).parent}"))
    if stats.pages:
        rows.append(("Stats", f"{stats.pages} pages, {stats.text_segments} text blocks, "
                              f"{stats.image_segments} image texts, {stats.translated} translated, "
                              f"{stats.qa_rounds} QA round(s), {stats.duration_s:.1f}s, "
                              f"translator={stats.translator or '-'}"))
    if result.error:
        rows.append(("Error", result.error))
    width = max(len(k) for k, _ in rows) + 1
    for key, value in rows:
        print(f"{key + ':':<{width}} {value}")
    report = result.qa_report
    if report is None:
        return
    verdict = "PASSED" if report.passed else "FAILED"
    print(f"QA: {verdict} - {len(report.rounds)} round(s), {report.errors} error(s), {report.warnings} warning(s)")
    if report.summary:
        print(f"    {report.summary}")
    for issue in report.final_issues[:_MAX_ISSUES_SHOWN]:
        where = f"p{issue.page + 1} " if issue.page is not None else ""
        seg = f"{issue.segment_id} " if issue.segment_id else ""
        print(f"    - [{issue.severity}] {issue.check} {where}{seg}: {issue.message}")
    if len(report.final_issues) > _MAX_ISSUES_SHOWN:
        print(f"    ... {len(report.final_issues) - _MAX_ISSUES_SHOWN} more issue(s) in the QA report")


_UVICORN_LEVELS = ("critical", "error", "warning", "info", "debug", "trace")


def _uvicorn_log_level(level: str) -> str:
    """Map a Python logging level name (``INFO``, ``WARN`` ...) to a uvicorn one."""
    name = level.strip().lower()
    if name == "warn":
        name = "warning"
    return name if name in _UVICORN_LEVELS else "info"


def cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    from .api import create_app

    settings = get_settings()
    app = create_app(settings)
    print(f"mathtrans web UI: http://{args.host}:{args.port}/  (data dir: {settings.data_dir})", file=sys.stderr)
    uvicorn.run(app, host=args.host, port=args.port, log_level=_uvicorn_log_level(settings.log_level))
    return EXIT_OK


def cmd_sample(args: argparse.Namespace) -> int:
    from .samples import make_sample_pdf

    path = make_sample_pdf(args.out, args.lang)
    print(path)
    return EXIT_OK


def cmd_glossary_template(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(glossary_template_csv(), encoding="utf-8")
    print(out)
    return EXIT_OK


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    level = logging.DEBUG if args.verbose else getattr(logging, get_settings().log_level.upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
