"""DeepSeek translation and review backends.

DeepSeek exposes an OpenAI-compatible ``/chat/completions`` endpoint; this module
talks to it directly over HTTPS (``httpx``), with JSON mode for structured
output, and reuses the prompts, schemas, batching and retry policy of the
Claude backend. The service is text-only, so OCR of text inside images keeps
using RapidOCR (or the Claude vision engine when an Anthropic key exists).
"""
from __future__ import annotations

import json
import logging
import time
from typing import Any, Callable, Optional, Sequence, TypeVar

import httpx

from ..config import Settings, get_settings
from ..interfaces import TranslationError
from ..models import Lang, ReviewFinding, ReviewItem, TranslationItem, TranslationResult
from ..protect import verify_placeholders
from .base import BaseTranslator, chunk_by_chars, chunk_items
from .claude import _parse_finding, _parse_json_object
from .prompts import (REVIEW_SCHEMA, TRANSLATION_SCHEMA, review_system_blocks, review_user_message,
                      translation_system_blocks, translation_user_message)

log = logging.getLogger("mathtrans.translate.deepseek")

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
MAX_OUTPUT_TOKENS = 8192  # the chat endpoint's output ceiling
MIN_OUTPUT_TOKENS = 2000
TOKENS_PER_INPUT_CHAR = 6
DEFAULT_BATCH_CHARS = 3000  # smaller batches than Claude: the output ceiling is 8k tokens
RETRY_STATUS = {408, 409, 429, 500, 502, 503, 504}

T = TypeVar("T")


def output_budget(user_text: str) -> int:
    return max(MIN_OUTPUT_TOKENS, min(MAX_OUTPUT_TOKENS, 1000 + TOKENS_PER_INPUT_CHAR * len(user_text)))


def system_text(blocks: list[dict[str, Any]]) -> str:
    """The Claude-style system blocks joined into one system message."""
    return "\n\n".join(str(b.get("text", "")) for b in blocks if b.get("text"))


def _schema_hint(schema: dict[str, Any]) -> str:
    return "Return a JSON object matching this JSON schema exactly:\n" + json.dumps(schema, ensure_ascii=False)


class _DeepSeekChat:
    """Shared request plumbing (retries, error mapping, usage logging, splitting)."""

    def __init__(self, api_key: str, model: str, base_url: str = DEFAULT_BASE_URL, *,
                 timeout: float = 240.0, max_retries: int = 3, client: Optional[httpx.Client] = None,
                 temperature: float = 1.0) -> None:
        if not api_key:
            raise TranslationError("DeepSeek backend selected but no API key: set DEEPSEEK_API_KEY")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.temperature = temperature
        self.client = client or httpx.Client(timeout=timeout)
        self._headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    def request(self, system: str, user_text: str, max_tokens: int) -> tuple[str, str]:
        """One chat completion in JSON mode. Returns ``(content, finish_reason)``."""
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_text}],
            "response_format": {"type": "json_object"},
            "max_tokens": int(max_tokens),
            "temperature": self.temperature,
            "stream": False,
        }
        url = f"{self.base_url}/chat/completions"
        last_error: Optional[str] = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.client.post(url, headers=self._headers, json=body)
            except httpx.HTTPError as exc:
                last_error = f"network error: {exc}"
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise TranslationError(f"Could not reach the DeepSeek API ({last_error})") from exc
            if resp.status_code == 200:
                return self._parse(resp)
            detail = _error_detail(resp)
            if resp.status_code in (401, 403):
                raise TranslationError(f"DeepSeek authentication failed ({resp.status_code}): check DEEPSEEK_API_KEY. {detail}")
            if resp.status_code == 402:
                raise TranslationError(f"DeepSeek account has insufficient balance (402): top up at platform.deepseek.com. {detail}")
            if resp.status_code == 400 or resp.status_code == 404 or resp.status_code == 422:
                raise TranslationError(f"DeepSeek rejected the request ({resp.status_code}) for model {self.model!r}: {detail}")
            if resp.status_code in RETRY_STATUS and attempt < self.max_retries:
                wait = float(resp.headers.get("retry-after") or (2 ** attempt))
                log.warning("DeepSeek returned %d; retrying in %.0fs (%s)", resp.status_code, wait, detail[:120])
                time.sleep(min(wait, 30.0))
                continue
            raise TranslationError(f"DeepSeek API error {resp.status_code}: {detail}")
        raise TranslationError(f"DeepSeek API request failed after retries: {last_error}")

    def _parse(self, resp: httpx.Response) -> tuple[str, str]:
        try:
            data = resp.json()
            choice = data["choices"][0]
            content = choice.get("message", {}).get("content") or ""
            finish = str(choice.get("finish_reason") or "stop")
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise TranslationError(f"DeepSeek returned an unexpected response body: {resp.text[:200]!r}") from exc
        usage = data.get("usage") or {}
        log.info("deepseek %s: in=%s out=%s cache_read=%s cache_write=%s stop=%s", self.model,
                 usage.get("prompt_tokens", "?"), usage.get("completion_tokens", "?"),
                 usage.get("prompt_cache_hit_tokens", 0), 0, finish)
        return content, finish

    def request_items(self, items: Sequence[T], system: str, build_user: Callable[[list[T]], str],
                      describe: Callable[[T], str]) -> list[dict[str, Any]]:
        """Request ``items``; split the batch in two when the output was cut off."""
        batch = list(items)
        if not batch:
            return []
        user_text = build_user(batch)
        content, finish = self.request(system, user_text, output_budget(user_text))
        if finish == "length":
            if len(batch) <= 1:
                log.error("DeepSeek output for item %s exceeded the output budget; the item is left without a result",
                          describe(batch[0]))
                return []
            half = len(batch) // 2
            log.warning("output cut off for %d items; splitting into %d + %d", len(batch), half, len(batch) - half)
            return (self.request_items(batch[:half], system, build_user, describe)
                    + self.request_items(batch[half:], system, build_user, describe))
        data = _parse_json_object(content)
        if data is None:
            log.warning("could not parse JSON from DeepSeek response (%d chars): %.200r", len(content), content)
            return []
        return [data]


def _error_detail(resp: httpx.Response) -> str:
    try:
        data = resp.json()
        err = data.get("error") if isinstance(data, dict) else None
        if isinstance(err, dict):
            return str(err.get("message") or err)
        return str(data)[:300]
    except ValueError:
        return resp.text[:300]


class DeepSeekTranslator(BaseTranslator):
    """Translator backed by DeepSeek chat completions in JSON mode."""

    name = "deepseek"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None,
                 settings: Optional[Settings] = None, max_chars: Optional[int] = None,
                 client: Optional[httpx.Client] = None) -> None:
        settings = settings or get_settings()
        self.settings = settings
        self.model = model or settings.deepseek_model
        self.max_chars = max_chars or min(settings.batch_chars, DEFAULT_BATCH_CHARS)
        self._api = _DeepSeekChat(api_key or settings.deepseek_api_key or "", self.model,
                                  base_url or settings.deepseek_base_url, client=client)

    def translate(self, items: list[TranslationItem], src: Lang, tgt: Lang,
                  glossary_pairs: list[tuple[str, str]], doc_context: str = "") -> list[TranslationResult]:
        if not items:
            return []
        src, tgt = Lang.parse(src), Lang.parse(tgt)
        system = system_text(translation_system_blocks(src, tgt, glossary_pairs)) + "\n\n" + _schema_hint(TRANSLATION_SCHEMA)
        results: dict[str, str] = {}
        for chunk in chunk_items(items, self.max_chars):
            got = self._translate_batch(chunk, system, doc_context)
            missing = [it for it in chunk if it.id not in got]
            if missing:
                log.warning("%d/%d ids missing from the DeepSeek response; retrying them once", len(missing), len(chunk))
                got.update(self._translate_batch(missing, system, doc_context))
            results.update(got)
            self._retry_placeholder_problems(chunk, results, system, doc_context)
        return [TranslationResult(id=it.id, text=results[it.id]) for it in items if it.id in results]

    def _translate_batch(self, items: list[TranslationItem], system: str, doc_context: str) -> dict[str, str]:
        wanted = {it.id for it in items}
        found: dict[str, str] = {}
        for data in self._api.request_items(items, system, lambda b: translation_user_message(b, doc_context),
                                            lambda it: f"{it.id!r} ({len(it.text)} chars)"):
            entries = data.get("translations")
            if not isinstance(entries, list):
                log.warning("DeepSeek JSON has no 'translations' list: keys=%s", list(data))
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                item_id, text = entry.get("id"), entry.get("text")
                if not isinstance(item_id, str) or not isinstance(text, str) or item_id not in wanted:
                    continue
                if item_id in found or not text.strip():
                    continue
                found[item_id] = text.strip()
        return found

    def _retry_placeholder_problems(self, chunk: list[TranslationItem], results: dict[str, str],
                                    system: str, doc_context: str) -> None:
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
            if new_text is not None and len(verify_placeholders(it.text, new_text)) <= len(problems_by_id[it.id]):
                results[it.id] = new_text


class DeepSeekReviewer:
    """Semantic review of translations by DeepSeek."""

    name = "deepseek"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None,
                 settings: Optional[Settings] = None, max_chars: Optional[int] = None,
                 client: Optional[httpx.Client] = None) -> None:
        settings = settings or get_settings()
        self.model = model or settings.deepseek_model
        self.max_chars = max_chars or min(settings.batch_chars, DEFAULT_BATCH_CHARS)
        self._api = _DeepSeekChat(api_key or settings.deepseek_api_key or "", self.model,
                                  base_url or settings.deepseek_base_url, client=client)

    def review(self, items: list[ReviewItem], src: Lang, tgt: Lang,
               glossary_pairs: list[tuple[str, str]]) -> list[ReviewFinding]:
        if not items:
            return []
        src, tgt = Lang.parse(src), Lang.parse(tgt)
        system = system_text(review_system_blocks(src, tgt, glossary_pairs)) + "\n\n" + _schema_hint(REVIEW_SCHEMA)
        known = {it.id for it in items}
        findings: list[ReviewFinding] = []
        for chunk in chunk_by_chars(items, self.max_chars, lambda it: len(it.source) + len(it.translation)):
            for data in self._api.request_items(chunk, system, review_user_message,
                                                lambda it: f"{it.id!r} ({len(it.source)} chars)"):
                entries = data.get("findings")
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    finding = _parse_finding(entry, known)
                    if finding is not None:
                        findings.append(finding)
        log.info("deepseek review: %d findings for %d items", len(findings), len(items))
        return findings


__all__ = ["DeepSeekTranslator", "DeepSeekReviewer", "output_budget", "system_text", "DEFAULT_MODEL"]
