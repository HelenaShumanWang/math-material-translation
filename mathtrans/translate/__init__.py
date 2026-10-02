"""Translation backends: Claude (online) and a deterministic mock (offline).

Public API::

    get_translator(name, settings, model=None) -> BaseTranslator
    get_reviewer(name, settings, model=None) -> Reviewer | None
    translate_segments(doc, translator, *, max_chars, doc_context="", only_ids=None, progress=None)
"""
from __future__ import annotations

import logging
from typing import Callable, Iterable, Optional

from ..config import Settings, get_settings
from ..interfaces import Reviewer, TranslationError, TranslationRefused
from ..models import (Lang, SegmentKind, TextSegment, TranslatedDocument, TranslationItem,
                      TranslationResult, restore_placeholders)
from ..protect import protect_text
from .base import BaseTranslator, chunk_by_chars, chunk_items, item_size
from .claude import ClaudeReviewer, ClaudeTranslator, make_client
from .mock import BAD_MARKER, MockReviewer, MockTranslator, mini_dictionary, pseudo_translate_text

__all__ = [
    "BAD_MARKER", "BaseTranslator", "ClaudeReviewer", "ClaudeTranslator", "MockReviewer",
    "MockTranslator", "TranslationError", "TranslationRefused", "chunk_by_chars", "chunk_items",
    "get_reviewer", "get_translator", "item_context", "item_size", "make_client", "mini_dictionary",
    "pseudo_translate_text", "translate_segments",
]

log = logging.getLogger("mathtrans.translate")

TranslateProgress = Callable[[int, int], None]
"""``(done_segments, total_segments)`` after every translated chunk."""

IMAGE_LABEL_CONTEXT = "label inside a diagram"
IMAGE_LABEL_LENGTH_FACTOR = 1.6

_ROLE_CONTEXT = {
    "heading": "heading",
    "caption": "figure or table caption",
    "label": "short label",
    "list": "list item",
    "table": "table cell",
    "body": "body paragraph",
    "other": "",
}

_NO_CREDENTIALS_MESSAGE = (
    "The Claude translator needs credentials: set ANTHROPIC_API_KEY (or MATHTRANS_ANTHROPIC_API_KEY / "
    "ANTHROPIC_AUTH_TOKEN) in the environment or .env, or choose the offline translator "
    "(--translator mock / MATHTRANS_TRANSLATOR=mock)."
)


def _require_credentials(settings: Settings) -> None:
    """Fail early with an actionable message instead of at the first API call
    (``Settings.has_api_key`` covers ``ANTHROPIC_API_KEY`` and ``ANTHROPIC_AUTH_TOKEN``)."""
    if not settings.has_api_key:
        raise TranslationError(_NO_CREDENTIALS_MESSAGE)


def get_translator(name: str, settings: Optional[Settings] = None, model: Optional[str] = None) -> BaseTranslator:
    """Translator backend by name: ``"mock"``, ``"claude"`` or ``"auto"`` (settings decide)."""
    settings = settings or get_settings()
    key = (name or "auto").strip().lower()
    if key == "auto":
        key = settings.resolved_translator("auto")
    if key == "mock":
        return MockTranslator()
    if key == "claude":
        _require_credentials(settings)
        return ClaudeTranslator(model=model, settings=settings)
    raise ValueError(f"Unknown translator {name!r}; expected one of auto, claude, mock")


def get_reviewer(name: Optional[str], settings: Optional[Settings] = None,
                 model: Optional[str] = None) -> Optional[Reviewer]:
    """Reviewer backend by name: ``"claude"``, ``"mock"``, ``"none"`` (-> ``None``) or
    ``"auto"`` (Claude when credentials exist, else the mock)."""
    settings = settings or get_settings()
    key = (name or "none").strip().lower()
    if key == "auto":
        key = settings.resolved_translator("auto")
    if key in ("none", "off", "no"):
        return None
    if key == "mock":
        return MockReviewer()
    if key == "claude":
        _require_credentials(settings)
        return ClaudeReviewer(model=model, settings=settings)
    raise ValueError(f"Unknown reviewer {name!r}; expected one of auto, claude, mock, none")


def item_context(seg: TextSegment) -> str:
    """Short description of where a segment lives, given to the translator as context."""
    if seg.kind == SegmentKind.IMAGE_TEXT:
        return IMAGE_LABEL_CONTEXT
    context = _ROLE_CONTEXT.get(seg.style.role, "")
    if seg.style.is_vertical:
        context = (context + ", vertical text").strip(", ")
    return context


def _build_item(seg: TextSegment, source_lang: Lang) -> Optional[TranslationItem]:
    if not seg.protected_text and seg.source_text.strip():
        # Segments created outside the extractor (tests, callers) may lack protection.
        seg.protected_text, seg.protected = protect_text(seg.source_text, source_lang)
        log.debug("protected segment %s on the fly", seg.id)
    if not seg.protected_text.strip():
        log.debug("segment %s has no text to translate", seg.id)
        return None
    max_chars = None
    if seg.kind == SegmentKind.IMAGE_TEXT:
        max_chars = int(len(seg.source_text) * IMAGE_LABEL_LENGTH_FACTOR) + 2
    return TranslationItem(
        id=seg.id,
        text=seg.protected_text,
        kind=seg.kind,
        context=item_context(seg),
        max_chars=max_chars,
        feedback=list(seg.feedback),
        previous=seg.translation_raw,
    )


def _apply_results(segments: dict[str, TextSegment], results: Iterable[TranslationResult]) -> int:
    applied = 0
    for result in results:
        seg = segments.get(result.id)
        if seg is None:
            log.warning("ignoring translation for unknown segment id %r", result.id)
            continue
        seg.translation_raw = result.text
        seg.translated_text = restore_placeholders(result.text, seg.protected)
        seg.attempts += 1
        seg.feedback = []
        applied += 1
    return applied


def translate_segments(
    doc: TranslatedDocument,
    translator: BaseTranslator,
    *,
    max_chars: int,
    doc_context: str = "",
    only_ids: Optional[Iterable[str]] = None,
    progress: Optional[TranslateProgress] = None,
) -> None:
    """Translate the translatable segments of ``doc`` in place.

    Builds a :class:`TranslationItem` per segment (``protected_text`` plus context,
    QA feedback and the previous translation), calls ``translator`` chunk by chunk
    (``max_chars`` source characters per request, document order kept) and writes
    ``translation_raw`` / ``translated_text`` (placeholders restored), increments
    ``attempts`` and clears ``feedback``. Results for unknown ids are ignored and
    segments that received no result are left untouched (``translated_text`` stays
    ``None`` for a first translation); nothing is raised for them. Backend failures
    (:class:`TranslationError`) propagate.
    """
    if doc.source_lang == doc.target_lang:
        log.warning("source and target language are both %s; translating anyway", doc.source_lang.value)
    wanted = set(only_ids) if only_ids is not None else None
    segments = [s for s in doc.segments if s.translate and (wanted is None or s.id in wanted)]
    if wanted is not None:
        unknown = wanted - {s.id for s in segments}
        if unknown:
            log.debug("only_ids not translatable or unknown: %s", sorted(unknown))
    by_id = {s.id: s for s in segments}
    items = [it for it in (_build_item(s, doc.source_lang) for s in segments) if it is not None]
    total = len(items)
    pairs = doc.glossary.pairs(doc.source_lang, doc.target_lang) if doc.glossary else []
    if progress:
        progress(0, total)
    if not items:
        log.info("nothing to translate (%d candidate segments)", len(segments))
        return
    done = 0
    for chunk in chunk_items(items, max_chars):
        results = translator.translate(chunk, doc.source_lang, doc.target_lang, pairs, doc_context)
        got_ids = {r.id for r in results}
        applied = _apply_results(by_id, results)
        missing = [it.id for it in chunk if it.id not in got_ids]
        if missing:
            log.warning("%d/%d segments received no translation: %s", len(missing), len(chunk),
                        ", ".join(missing[:10]) + (" ..." if len(missing) > 10 else ""))
        done += len(chunk)
        log.debug("chunk of %d items: %d translations applied", len(chunk), applied)
        if progress:
            progress(done, total)
    translated = sum(1 for s in segments if s.translated_text is not None)
    log.info("translated %d/%d segments (%s -> %s) with %s", translated, len(segments),
             doc.source_lang.value, doc.target_lang.value, translator.name)
