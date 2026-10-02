"""Common base class for translation backends and request chunking helpers."""
from __future__ import annotations

import logging
from typing import Callable, Sequence, TypeVar

from ..models import Lang, TranslationItem, TranslationResult

log = logging.getLogger("mathtrans.translate")

T = TypeVar("T")

DEFAULT_MAX_ITEMS_PER_CHUNK = 80
"""Upper bound on items per request, independent of their size: a chunk of many
tiny labels still has to come back as one JSON document, so keep it readable."""


class BaseTranslator:
    """Interface shared by every translator backend.

    Subclasses implement :meth:`translate` and set a short ``name`` (``"mock"``,
    ``"claude"``) that the pipeline reports in its statistics. The texts in the
    items contain ``⟦n⟧`` placeholders that stand for verbatim fragments; a
    backend must copy them into the translation unchanged.
    """

    name: str = "base"

    def translate(
        self,
        items: list[TranslationItem],
        src: Lang,
        tgt: Lang,
        glossary_pairs: list[tuple[str, str]],
        doc_context: str = "",
    ) -> list[TranslationResult]:
        """Translate ``items`` from ``src`` to ``tgt``.

        Returns one :class:`TranslationResult` per item that could be translated,
        in item order. Items without a result are simply absent (the caller keeps
        them untranslated). Raises :class:`~mathtrans.interfaces.TranslationError`
        when the backend cannot work at all (network, credentials, refusal).
        """
        raise NotImplementedError

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<{type(self).__name__} name={self.name!r}>"


def item_size(item: TranslationItem) -> int:
    """Approximate request size of one item in characters (text + feedback + previous)."""
    size = len(item.text) + len(item.context)
    size += sum(len(f) for f in item.feedback)
    if item.previous:
        size += len(item.previous)
    return size


def chunk_by_chars(
    items: Sequence[T],
    max_chars: int,
    measure: Callable[[T], int],
    *,
    max_items: int = DEFAULT_MAX_ITEMS_PER_CHUNK,
) -> list[list[T]]:
    """Greedily group ``items`` (keeping their order) so that the summed
    ``measure`` of each group stays within ``max_chars``.

    An item larger than ``max_chars`` forms a group of its own; a non-positive
    ``max_chars`` disables the character limit (only ``max_items`` applies).
    """
    if max_items <= 0:
        raise ValueError("max_items must be positive")
    chunks: list[list[T]] = []
    current: list[T] = []
    current_size = 0
    for item in items:
        size = max(0, measure(item))
        too_big = max_chars > 0 and current and current_size + size > max_chars
        too_many = len(current) >= max_items
        if too_big or too_many:
            chunks.append(current)
            current, current_size = [], 0
        current.append(item)
        current_size += size
    if current:
        chunks.append(current)
    return chunks


def chunk_items(
    items: Sequence[TranslationItem],
    max_chars: int,
    *,
    max_items: int = DEFAULT_MAX_ITEMS_PER_CHUNK,
) -> list[list[TranslationItem]]:
    """Split translation items into request-sized chunks, preserving document order.

    ``max_chars`` is the approximate amount of source characters (plus feedback
    and previous translations) per request. Items larger than the limit are sent
    alone rather than dropped.
    """
    return chunk_by_chars(items, max_chars, item_size, max_items=max_items)
