"""System prompts, JSON schemas and message builders for the Claude backends.

The system prompt is split into a *stable* block (identical for every request,
so it can be served from the prompt cache) and a *per-document* block holding
the language pair and the glossary pairs. Keep the stable block free of anything
that changes between documents.
"""
from __future__ import annotations

import json
from typing import Any

from ..glossary import glossary_prompt_block
from ..languages import info
from ..models import Lang, ReviewItem, TranslationItem

TRANSLATION_SYSTEM_PROMPT = """\
You are a professional translator of mathematics learning materials (school and university \
textbooks, worksheets, exercise books). The texts you receive were extracted from PDF pages and \
your translations are inserted back into the original page layout, so they must be precise, \
complete and compact.

Rules
1. Placeholders. The source contains placeholders of the form ⟦n⟧ (a number between ⟦ and ⟧). \
Each one stands for a fragment that is kept verbatim: a formula, a number, a variable name, a \
unit, a reference such as a figure number. Copy every placeholder into the translation exactly \
once and unchanged, at the position where the fragment belongs in the target language. Never \
drop, duplicate, merge, split, renumber or invent placeholders and never write anything inside one.
2. Structure. Keep list markers, numbering, bullets and line breaks (\\n) exactly as in the \
source, with the same number of lines. A heading stays a heading, a question stays a question, \
an instruction stays an instruction.
3. Terminology. When glossary pairs are given (source term => target term) use the target term \
every time the source term occurs, consistently. Otherwise use the standard mathematical \
terminology of the target language as used in school textbooks.
4. Length. The translation replaces the original text in a box of the same size, so keep it \
about as long as the original and avoid paraphrases that make it longer. When an item has \
"max_chars" the translation must not exceed that many characters; abbreviate if necessary.
5. Register. Use the clear, concise and formal style of a textbook in the target language. \
Translate everything that is text, including headings, captions, labels, footers and page \
numbers written in words. Do not leave source-language words untranslated except proper names \
that are normally not translated.
6. Feedback. An item may carry "context" (for example heading, figure caption, label inside a \
diagram), "feedback" from an automatic quality check of a previous attempt and "previous" (the \
rejected previous translation). Fix every point of the feedback and deliver a better translation.
7. Output. Respond with JSON only, no explanations, no notes, no markdown: \
{"translations": [{"id": "...", "text": "..."}]} with exactly one entry for every input item id, \
in the same order as the input. "text" is the translation alone: no surrounding quotes, no \
"Translation:" prefix, no comments.
"""

REVIEW_SYSTEM_PROMPT = """\
You are a senior bilingual reviewer of translated mathematics learning materials. For each item \
you receive the source text, its translation and optionally its context, and you report every \
problem a human proof-reader would have to fix.

Check each item for
- meaning: mistranslations, changed meaning, wrong mathematical statements;
- omission: missing sentences, clauses, list items or qualifiers, and additions absent from the source;
- number: numbers, formulas, variable names, units or references (figure, exercise, chapter \
numbers) that differ from the source;
- terminology: deviations from the glossary pairs, inconsistent or non-standard mathematical terms;
- untranslated: source-language fragments left untranslated (proper names and symbols are fine);
- grammar: grammar, spelling, punctuation and wording that is unnatural for a textbook;
- format: lost list markers, numbering or line breaks, wrong casing for headings.

Placeholders of the form ⟦n⟧ appear in both the source and the translation. They stand for \
identical verbatim fragments (formulas, numbers, variables, units) and are correct as long as the \
translation contains the same placeholders as the source. Never report a placeholder as \
untranslated or as a number problem; report one only when it is missing, duplicated or placed \
where it changes the meaning.

Severity: "error" for anything that changes the meaning or would mislead a student (meaning, \
omission, number, terminology, untranslated, a missing placeholder); "warning" for grammar, \
style and format issues that do not change the meaning.

Report only real problems; an item without problems gets no finding. Respond with JSON only: \
{"findings": [{"id": "...", "severity": "error" | "warning", "category": "...", "message": "...", \
"suggested_fix": "..." | null}]} where "message" is a short explanation in English and \
"suggested_fix" is the complete corrected translation of the item (with its placeholders) or null.
"""

REVIEW_CATEGORIES: tuple[str, ...] = (
    "meaning", "omission", "number", "terminology", "untranslated", "grammar", "format",
)

TRANSLATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "translations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["id", "text"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["translations"],
    "additionalProperties": False,
}

REVIEW_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "severity": {"type": "string", "enum": ["error", "warning"]},
                    "category": {"type": "string", "enum": list(REVIEW_CATEGORIES)},
                    "message": {"type": "string"},
                    "suggested_fix": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                },
                "required": ["id", "severity", "category", "message", "suggested_fix"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}


def language_label(lang: Lang | str) -> str:
    """Human readable language label used in prompts, e.g. ``Chinese (Simplified) [zh]``."""
    li = info(lang)
    return f"{li.name_en} [{li.code.value}]"


def language_pair_block(src: Lang, tgt: Lang, glossary_pairs: list[tuple[str, str]]) -> str:
    """The per-document system block: language pair plus glossary pairs."""
    lines = [f"Source language: {language_label(src)}.", f"Target language: {language_label(tgt)}."]
    block = glossary_prompt_block(glossary_pairs)
    if block:
        lines.append("")
        lines.append("Glossary (source term => target term), to be followed exactly:")
        lines.append(block)
    else:
        lines.append("No glossary is given for this document.")
    return "\n".join(lines)


def build_system_blocks(stable: str, src: Lang, tgt: Lang,
                        glossary_pairs: list[tuple[str, str]]) -> list[dict[str, Any]]:
    """System prompt as content blocks with two cache breakpoints: the stable
    block is shared by every request of every document, the language/glossary
    block by all the chunks and QA re-translation rounds of one document
    (prompt caching is prefix based, so the second breakpoint covers both)."""
    return [
        {"type": "text", "text": stable, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": language_pair_block(src, tgt, glossary_pairs),
         "cache_control": {"type": "ephemeral"}},
    ]


def translation_system_blocks(src: Lang, tgt: Lang,
                              glossary_pairs: list[tuple[str, str]]) -> list[dict[str, Any]]:
    return build_system_blocks(TRANSLATION_SYSTEM_PROMPT, src, tgt, glossary_pairs)


def review_system_blocks(src: Lang, tgt: Lang,
                         glossary_pairs: list[tuple[str, str]]) -> list[dict[str, Any]]:
    return build_system_blocks(REVIEW_SYSTEM_PROMPT, src, tgt, glossary_pairs)


def translation_item_payload(item: TranslationItem) -> dict[str, Any]:
    """JSON representation of one item for the user turn (optional fields only when set)."""
    payload: dict[str, Any] = {"id": item.id, "text": item.text}
    if item.context:
        payload["context"] = item.context
    if item.max_chars is not None:
        payload["max_chars"] = item.max_chars
    if item.feedback:
        payload["feedback"] = list(item.feedback)
    if item.previous:
        payload["previous"] = item.previous
    return payload


def translation_user_message(items: list[TranslationItem], doc_context: str = "") -> str:
    """The single user turn of a translation request."""
    parts: list[str] = []
    if doc_context.strip():
        parts.append("Document context:\n" + doc_context.strip())
    body = json.dumps([translation_item_payload(it) for it in items], ensure_ascii=False, indent=1)
    parts.append(f"Translate the following {len(items)} item(s). Return JSON only.\n{body}")
    return "\n\n".join(parts)


def review_item_payload(item: ReviewItem) -> dict[str, Any]:
    payload: dict[str, Any] = {"id": item.id, "source": item.source, "translation": item.translation}
    if item.context:
        payload["context"] = item.context
    return payload


def review_user_message(items: list[ReviewItem]) -> str:
    """The single user turn of a review request."""
    body = json.dumps([review_item_payload(it) for it in items], ensure_ascii=False, indent=1)
    return f"Review the following {len(items)} translated item(s). Return JSON only.\n{body}"
