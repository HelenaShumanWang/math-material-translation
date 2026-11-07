"""Claude translation and review backends (official ``anthropic`` SDK).

Both backends send one user turn with the items as JSON and ask for structured
JSON output (``output_config.format``). The system prompt is a stable, cached
block followed by a per-document language/glossary block. Refusals, truncated
outputs, missing ids and placeholder problems are handled here so that callers
only see :class:`~mathtrans.interfaces.TranslationError` or clean results.
"""
from __future__ import annotations

import inspect
import json
import logging
from typing import Any, Callable, Optional, Sequence, TypeVar

import anthropic

from ..config import Settings, get_settings
from ..interfaces import TranslationError, TranslationRefused
from ..models import Lang, ReviewFinding, ReviewItem, TranslationItem, TranslationResult
from ..protect import verify_placeholders
from .base import BaseTranslator, chunk_by_chars, chunk_items
from .prompts import (REVIEW_CATEGORIES, REVIEW_SCHEMA, STYLE_CATEGORIES, TRANSLATION_SCHEMA, review_system_blocks,
                      review_user_message, translation_system_blocks, translation_user_message)

log = logging.getLogger("mathtrans.translate.claude")

MAX_TOKENS = 16000
MIN_TOKENS = 4000
TOKENS_PER_INPUT_CHAR = 12


def output_budget(user_text: str) -> int:
    """``max_tokens`` for a request: generous for big batches, tight for single items so
    that a runaway generation costs a few thousand tokens instead of 16k (thinking tokens
    count against the budget on models with adaptive thinking)."""
    return max(MIN_TOKENS, min(MAX_TOKENS, 1500 + TOKENS_PER_INPUT_CHAR * len(user_text)))
FALLBACK_BETA = "server-side-fallback-2026-07-01"
FALLBACK_MODE = "default"

T = TypeVar("T")


def make_client(settings: Optional[Settings] = None) -> anthropic.Anthropic:
    """Build the SDK client. ``api_key=None`` lets the SDK resolve the key from
    ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN`` / a stored profile."""
    settings = settings or get_settings()
    try:
        return anthropic.Anthropic(api_key=settings.anthropic_api_key)
    except anthropic.AnthropicError as exc:
        raise TranslationError(f"Could not create the Anthropic client: {exc}") from exc


def _supports_fallbacks(client: Any) -> bool:
    """Whether ``client.beta.messages.create`` accepts the ``betas`` / ``fallbacks``
    keyword arguments (true for anthropic >= 1.11; older SDKs would raise TypeError)."""
    try:
        create = client.beta.messages.create
        params = inspect.signature(create).parameters
    except (AttributeError, TypeError, ValueError):
        return False
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()):
        return True
    return "fallbacks" in params and "betas" in params


def _first_text(response: Any) -> str:
    for block in getattr(response, "content", None) or []:
        if getattr(block, "type", None) == "text":
            return getattr(block, "text", "") or ""
    return ""


def _parse_json_object(text: str) -> Optional[dict[str, Any]]:
    """Parse the model output as a JSON object; tolerate a markdown code fence."""
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
        if candidate.lower().startswith("json"):
            candidate = candidate[4:]
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


class _ClaudeMessages:
    """Shared request plumbing for the translator and the reviewer."""

    def __init__(self, client: Any, model: str, effort: str, enable_fallbacks: bool) -> None:
        self.client = client
        self.model = model
        self.effort = effort
        self.enable_fallbacks = enable_fallbacks and _supports_fallbacks(client)
        if enable_fallbacks and not self.enable_fallbacks:
            log.warning("installed anthropic SDK does not accept server-side fallbacks; using client.messages")

    # ------------------------------------------------------------------ raw call
    def request(self, system: list[dict[str, Any]], user_text: str, schema: dict[str, Any],
                max_tokens: int = MAX_TOKENS) -> Any:
        """One Messages API call with structured JSON output; maps SDK errors."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user_text}],
            "output_config": {"effort": self.effort, "format": {"type": "json_schema", "schema": schema}},
        }
        try:
            if self.enable_fallbacks:
                response = self.client.beta.messages.create(
                    **kwargs, betas=[FALLBACK_BETA], fallbacks=FALLBACK_MODE)
            else:
                response = self.client.messages.create(**kwargs)
        except anthropic.AuthenticationError as exc:
            raise TranslationError(
                "Anthropic authentication failed (401): check ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN, "
                f"or run with --translator mock. {exc}") from exc
        except anthropic.PermissionDeniedError as exc:
            raise TranslationError(
                f"The Anthropic API key is not allowed to use model {self.model!r} (403): {exc}") from exc
        except anthropic.NotFoundError as exc:
            raise TranslationError(
                f"Model {self.model!r} was not found (404): check MATHTRANS_CLAUDE_MODEL / --model. {exc}") from exc
        except anthropic.RateLimitError as exc:
            raise TranslationError(
                "Anthropic rate limit reached (429) even after the SDK's automatic retries; "
                f"wait and retry, or lower MATHTRANS_MAX_WORKERS. {exc}") from exc
        except anthropic.APIStatusError as exc:
            hint = "retry later" if exc.status_code >= 500 else "check the request parameters and model name"
            raise TranslationError(
                f"Anthropic API error {exc.status_code} for model {self.model!r} ({hint}): {exc}") from exc
        except anthropic.APIConnectionError as exc:
            raise TranslationError(
                f"Could not reach the Anthropic API (network/proxy/timeout): {exc}") from exc
        except anthropic.APIError as exc:
            raise TranslationError(f"Anthropic API request failed: {exc}") from exc
        except TypeError as exc:
            # The SDK raises a bare TypeError when no credential can be resolved at request
            # time, and when an older SDK does not know a request parameter.
            raise TranslationError(
                "The Anthropic SDK rejected the request. Set ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN (or "
                f"choose --translator mock) and make sure anthropic >= 1.0 is installed: {exc}") from exc
        self._log_response(response)
        if getattr(response, "stop_reason", None) == "refusal":
            raise TranslationRefused(_refusal_message(response))
        return response

    def _log_response(self, response: Any) -> None:
        usage = getattr(response, "usage", None)
        served = getattr(response, "model", None) or self.model
        if usage is not None:
            log.info("claude %s (served by %s): in=%s out=%s cache_read=%s cache_write=%s stop=%s",
                     self.model, served, getattr(usage, "input_tokens", "?"),
                     getattr(usage, "output_tokens", "?"), getattr(usage, "cache_read_input_tokens", None),
                     getattr(usage, "cache_creation_input_tokens", None), getattr(response, "stop_reason", "?"))
        iterations = getattr(usage, "iterations", None) or []
        if any(getattr(it, "type", None) == "fallback_message" for it in iterations):
            log.warning("model %s declined the request; the server-side fallback model %s answered instead",
                        self.model, served)

    # ----------------------------------------------------- splitting on max_tokens
    def request_items(
        self,
        items: Sequence[T],
        system: list[dict[str, Any]],
        build_user: Callable[[list[T]], str],
        schema: dict[str, Any],
        describe: Callable[[T], str],
    ) -> list[dict[str, Any]]:
        """Request ``items``; when the output is cut off (``max_tokens``) split the
        batch in two and retry each half. Returns the parsed JSON objects (one per
        successful request; a malformed body yields no object and is logged)."""
        batch = list(items)
        if not batch:
            return []
        user_text = build_user(batch)
        response = self.request(system, user_text, schema, max_tokens=output_budget(user_text))
        if getattr(response, "stop_reason", None) == "max_tokens":
            if len(batch) <= 1:
                # A runaway generation on a single item (seen with structured output + retry
                # feedback) must not abort the whole document: the item simply gets no result
                # and the QA loop reports / retries it.
                log.error("model output for item %s exceeded the output budget (%d tokens); the item is "
                          "left without a result", describe(batch[0]), output_budget(user_text))
                return []
            half = len(batch) // 2
            log.warning("output hit max_tokens for %d items; splitting into %d + %d",
                        len(batch), half, len(batch) - half)
            return (self.request_items(batch[:half], system, build_user, schema, describe)
                    + self.request_items(batch[half:], system, build_user, schema, describe))
        text = _first_text(response)
        data = _parse_json_object(text)
        if data is None:
            log.warning("could not parse JSON from model response (%d chars): %.200r", len(text), text)
            return []
        return [data]


def _refusal_message(response: Any) -> str:
    details = getattr(response, "stop_details", None)
    category = getattr(details, "category", None)
    explanation = getattr(details, "explanation", None)
    msg = "The model declined this request (stop_reason=refusal"
    if category:
        msg += f", category={category}"
    msg += ")"
    if explanation:
        msg += f": {explanation}"
    return msg


class ClaudeTranslator(BaseTranslator):
    """Translator backed by the Claude Messages API with structured JSON output."""

    name = "claude"

    def __init__(
        self,
        client: Any = None,
        model: Optional[str] = None,
        effort: Optional[str] = None,
        enable_fallbacks: Optional[bool] = None,
        settings: Optional[Settings] = None,
        max_chars: Optional[int] = None,
    ) -> None:
        settings = settings or get_settings()
        self.settings = settings
        self.model = model or settings.claude_model
        self.effort = effort or settings.claude_effort
        self.enable_fallbacks = settings.enable_fallbacks if enable_fallbacks is None else enable_fallbacks
        self.max_chars = max_chars or settings.batch_chars
        self.client = client if client is not None else make_client(settings)
        self._api = _ClaudeMessages(self.client, self.model, self.effort, self.enable_fallbacks)

    # ------------------------------------------------------------------ public
    def translate(
        self,
        items: list[TranslationItem],
        src: Lang,
        tgt: Lang,
        glossary_pairs: list[tuple[str, str]],
        doc_context: str = "",
    ) -> list[TranslationResult]:
        if not items:
            return []
        src, tgt = Lang.parse(src), Lang.parse(tgt)
        system = translation_system_blocks(src, tgt, glossary_pairs)
        results: dict[str, str] = {}
        for chunk in chunk_items(items, self.max_chars):
            got = self._translate_batch(chunk, system, doc_context)
            missing = [it for it in chunk if it.id not in got]
            if missing:
                log.warning("%d/%d ids missing from the response; retrying them once", len(missing), len(chunk))
                got.update(self._translate_batch(missing, system, doc_context))
            results.update(got)
            self._retry_placeholder_problems(chunk, results, system, doc_context)
        return [TranslationResult(id=it.id, text=results[it.id]) for it in items if it.id in results]

    # ---------------------------------------------------------------- internals
    def _translate_batch(self, items: list[TranslationItem], system: list[dict[str, Any]],
                         doc_context: str) -> dict[str, str]:
        wanted = {it.id for it in items}
        found: dict[str, str] = {}
        objects = self._api.request_items(
            items, system, lambda batch: translation_user_message(batch, doc_context), TRANSLATION_SCHEMA,
            lambda it: f"{it.id!r} ({len(it.text)} chars)")
        for data in objects:
            entries = data.get("translations")
            if not isinstance(entries, list):
                log.warning("response JSON has no 'translations' list: keys=%s", list(data))
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                item_id, text = entry.get("id"), entry.get("text")
                if not isinstance(item_id, str) or not isinstance(text, str):
                    log.warning("ignoring malformed translation entry: %r", entry)
                    continue
                if item_id not in wanted:
                    log.warning("ignoring translation for unknown id %r", item_id)
                    continue
                if item_id in found:
                    log.warning("duplicate translation for id %r; keeping the first", item_id)
                    continue
                if not text.strip():
                    log.warning("empty translation for id %r; treating it as missing", item_id)
                    continue
                found[item_id] = text.strip()
        return found

    def _retry_placeholder_problems(self, chunk: list[TranslationItem], results: dict[str, str],
                                    system: list[dict[str, Any]], doc_context: str) -> None:
        retry: list[TranslationItem] = []
        problems_by_id: dict[str, list[str]] = {}
        for it in chunk:
            text = results.get(it.id)
            if text is None:
                continue
            problems = verify_placeholders(it.text, text)
            if problems:
                problems_by_id[it.id] = problems
                feedback = list(it.feedback) + [
                    "Placeholder problem in the previous translation: " + "; ".join(problems)
                    + ". Every ⟦n⟧ of the source must appear exactly once, unchanged."]
                retry.append(it.model_copy(update={"feedback": feedback, "previous": text}))
        if not retry:
            return
        log.warning("placeholder problems in %d translations; retrying them once with feedback", len(retry))
        got = self._translate_batch(retry, system, doc_context)
        for it in retry:
            new_text = got.get(it.id)
            if new_text is None:
                continue
            if len(verify_placeholders(it.text, new_text)) <= len(problems_by_id[it.id]):
                results[it.id] = new_text


class ClaudeReviewer:
    """Semantic review of translations by Claude (meaning, omissions, numbers, terms, grammar)."""

    name = "claude"

    def __init__(self, client: Any = None, model: Optional[str] = None,
                 settings: Optional[Settings] = None, max_chars: Optional[int] = None) -> None:
        settings = settings or get_settings()
        self.settings = settings
        self.model = model or settings.review_model()
        self.effort = settings.claude_effort
        self.enable_fallbacks = settings.enable_fallbacks
        self.max_chars = max_chars or settings.batch_chars
        self.client = client if client is not None else make_client(settings)
        self._api = _ClaudeMessages(self.client, self.model, self.effort, self.enable_fallbacks)

    def review(
        self,
        items: list[ReviewItem],
        src: Lang,
        tgt: Lang,
        glossary_pairs: list[tuple[str, str]],
    ) -> list[ReviewFinding]:
        if not items:
            return []
        src, tgt = Lang.parse(src), Lang.parse(tgt)
        system = review_system_blocks(src, tgt, glossary_pairs)
        known = {it.id for it in items}
        findings: list[ReviewFinding] = []
        chunks = chunk_by_chars(items, self.max_chars, lambda it: len(it.source) + len(it.translation))
        for chunk in chunks:
            objects = self._api.request_items(chunk, system, review_user_message, REVIEW_SCHEMA,
                                              lambda it: f"{it.id!r} ({len(it.source)} chars)")
            for data in objects:
                entries = data.get("findings")
                if not isinstance(entries, list):
                    log.warning("review JSON has no 'findings' list: keys=%s", list(data))
                    continue
                for entry in entries:
                    finding = _parse_finding(entry, known)
                    if finding is not None:
                        findings.append(finding)
        log.info("claude review: %d findings for %d items", len(findings), len(items))
        return findings


def _parse_finding(entry: Any, known_ids: set[str]) -> Optional[ReviewFinding]:
    if not isinstance(entry, dict):
        return None
    item_id = entry.get("id")
    message = entry.get("message")
    if not isinstance(item_id, str) or not isinstance(message, str) or not message.strip():
        log.warning("ignoring malformed review finding: %r", entry)
        return None
    if item_id not in known_ids:
        log.warning("ignoring review finding for unknown id %r", item_id)
        return None
    severity = str(entry.get("severity", "warning")).strip().lower()
    if severity not in ("error", "warning"):
        severity = "warning"
    category = str(entry.get("category", "")).strip().lower() or "meaning"
    if category not in REVIEW_CATEGORIES:
        log.debug("non-standard review category %r for %s", category, item_id)
    if category in STYLE_CATEGORIES and severity == "error":
        # the prompt's own policy: grammar / format findings never change the meaning
        severity = "warning"
    fix = entry.get("suggested_fix")
    suggested_fix = fix.strip() if isinstance(fix, str) and fix.strip() else None
    return ReviewFinding(id=item_id, severity=severity, category=category,  # type: ignore[arg-type]
                         message=message.strip(), suggested_fix=suggested_fix)
