"""Protocols implemented by pluggable backends (translators, reviewers, OCR, QA checks)."""
from __future__ import annotations

from typing import Callable, Optional, Protocol, runtime_checkable

import numpy as np

from .models import (Lang, OcrResult, PipelineOptions, QAIssue, ReviewFinding, ReviewItem,
                     TranslatedDocument, TranslationItem, TranslationResult)

ProgressCallback = Callable[[str, str, float], None]
"""(stage, message, percent 0-100)"""


@runtime_checkable
class Translator(Protocol):
    name: str

    def translate(
        self,
        items: list[TranslationItem],
        src: Lang,
        tgt: Lang,
        glossary_pairs: list[tuple[str, str]],
        doc_context: str = "",
    ) -> list[TranslationResult]:
        """Translate ``items`` (texts contain ``⟦n⟧`` placeholders that must be kept
        verbatim). Must return one result per item id; may raise TranslationError."""
        ...


@runtime_checkable
class Reviewer(Protocol):
    name: str

    def review(
        self,
        items: list[ReviewItem],
        src: Lang,
        tgt: Lang,
        glossary_pairs: list[tuple[str, str]],
    ) -> list[ReviewFinding]:
        ...


@runtime_checkable
class OcrEngine(Protocol):
    name: str

    def recognize(self, image_rgb: np.ndarray, hint_langs: Optional[list[Lang]] = None) -> list[OcrResult]:
        """``image_rgb`` is an HxWx3 uint8 array."""
        ...


@runtime_checkable
class QACheck(Protocol):
    name: str
    severity: str  # "error" | "warning"

    def run(self, doc: TranslatedDocument, options: PipelineOptions) -> list[QAIssue]:
        ...


class TranslationError(RuntimeError):
    """Raised when a translation backend cannot produce a result."""


class TranslationRefused(TranslationError):
    """The model declined the request (stop_reason == "refusal")."""
