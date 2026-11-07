"""Tests for the DeepSeek backend (offline: the HTTP API is replaced by httpx.MockTransport)."""
from __future__ import annotations

import json
from typing import Any, Callable

import httpx
import pytest

from mathtrans.config import Settings
from mathtrans.interfaces import TranslationError
from mathtrans.models import Lang, ReviewItem, TranslationItem
from mathtrans.translate import MockTranslator, get_reviewer, get_translator
from mathtrans.translate import deepseek as ds
from mathtrans.translate.deepseek import (DEFAULT_MODEL, MAX_OUTPUT_TOKENS, MIN_OUTPUT_TOKENS, DeepSeekReviewer,
                                          DeepSeekTranslator, output_budget, system_text)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #


def make_settings(**overrides: Any) -> Settings:
    values: dict[str, Any] = {"DEEPSEEK_API_KEY": "sk-deepseek-test", "batch_chars": 6000}
    values.update(overrides)
    return Settings(_env_file=None, **values)


def completion(payload: Any, finish_reason: str = "stop", status: int = 200) -> httpx.Response:
    content = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    body = {
        "id": "chatcmpl-test",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": finish_reason}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "prompt_cache_hit_tokens": 0},
    }
    return httpx.Response(status, json=body)


def error(status: int, message: str) -> httpx.Response:
    return httpx.Response(status, json={"error": {"message": message, "type": "test"}})


def items_in_request(body: dict[str, Any]) -> list[dict[str, Any]]:
    user = [m for m in body["messages"] if m["role"] == "user"][0]["content"]
    return json.loads(user.split("Return JSON only.\n", 1)[1])


def echo(body: dict[str, Any], prefix: str = "EN ") -> dict[str, Any]:
    return {"translations": [{"id": it["id"], "text": prefix + it["text"]} for it in items_in_request(body)]}


class Recorder:
    """A MockTransport handler that records every request body."""

    def __init__(self, responder: Callable[[dict[str, Any], int], httpx.Response]) -> None:
        self.responder = responder
        self.requests: list[httpx.Request] = []
        self.bodies: list[dict[str, Any]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        body = json.loads(request.content)
        self.bodies.append(body)
        return self.responder(body, len(self.bodies))

    @property
    def client(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self))


def make_translator(responder: Callable[[dict[str, Any], int], httpx.Response], **kw: Any) -> tuple[DeepSeekTranslator, Recorder]:
    rec = Recorder(responder)
    settings = kw.pop("settings", None) or make_settings()
    return DeepSeekTranslator(settings=settings, client=rec.client, **kw), rec


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(ds.time, "sleep", lambda *_: None)


# --------------------------------------------------------------------------- #
# budget / plumbing
# --------------------------------------------------------------------------- #


def test_output_budget_bounds():
    assert output_budget("") == MIN_OUTPUT_TOKENS
    assert output_budget("x" * 100) == max(MIN_OUTPUT_TOKENS, 1000 + 600)
    assert output_budget("x" * 100_000) == MAX_OUTPUT_TOKENS
    assert MAX_OUTPUT_TOKENS <= 8192


def test_system_text_joins_blocks():
    assert system_text([{"type": "text", "text": "a"}, {"type": "text", "text": ""}, {"type": "text", "text": "b"}]) == "a\n\nb"


def test_missing_key_is_an_error():
    with pytest.raises(TranslationError, match="DEEPSEEK_API_KEY"):
        DeepSeekTranslator(settings=make_settings(DEEPSEEK_API_KEY=None))


# --------------------------------------------------------------------------- #
# translation
# --------------------------------------------------------------------------- #


def test_translate_round_trip_uses_json_mode():
    tr, rec = make_translator(lambda body, n: completion(echo(body)))
    items = [TranslationItem(id="a", text="三角形的面积是 ⟦0⟧"), TranslationItem(id="b", text="第 ⟦0⟧ 页")]
    results = tr.translate(items, Lang.ZH, Lang.EN, [("三角形", "triangle")])
    assert [(r.id, r.text) for r in results] == [("a", "EN 三角形的面积是 ⟦0⟧"), ("b", "EN 第 ⟦0⟧ 页")]
    assert len(rec.requests) == 1
    req, body = rec.requests[0], rec.bodies[0]
    assert str(req.url) == "https://api.deepseek.com/chat/completions"
    assert req.headers["authorization"] == "Bearer sk-deepseek-test"
    assert body["model"] == DEFAULT_MODEL == "deepseek-chat"
    assert body["response_format"] == {"type": "json_object"}
    assert body["stream"] is False
    assert MIN_OUTPUT_TOKENS <= body["max_tokens"] <= MAX_OUTPUT_TOKENS
    system = body["messages"][0]
    assert system["role"] == "system"
    assert "json" in system["content"].lower()  # DeepSeek JSON mode requires the word in the prompt
    assert "triangle" in system["content"] and "JSON schema" in system["content"]
    assert tr.name == "deepseek" and tr.model == "deepseek-chat"


def test_custom_model_and_base_url():
    settings = make_settings(deepseek_model="deepseek-v4-pro", deepseek_base_url="https://proxy.example/v1/")
    tr, rec = make_translator(lambda body, n: completion(echo(body)), settings=settings)
    tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert rec.bodies[0]["model"] == "deepseek-v4-pro"
    assert str(rec.requests[0].url) == "https://proxy.example/v1/chat/completions"
    tr2, rec2 = make_translator(lambda body, n: completion(echo(body)), model="deepseek-flash")
    tr2.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert rec2.bodies[0]["model"] == "deepseek-flash"


def test_length_cutoff_splits_the_batch():
    def responder(body: dict[str, Any], n: int) -> httpx.Response:
        items = items_in_request(body)
        if len(items) > 1:
            return completion('{"translations": [{"id": "a", "te', finish_reason="length")
        return completion(echo(body))

    tr, rec = make_translator(responder)
    items = [TranslationItem(id=f"i{k}", text=f"第 {k} 题") for k in range(4)]
    results = tr.translate(items, Lang.ZH, Lang.EN, [])
    assert [r.id for r in results] == [it.id for it in items]
    # 1 request for 4, 2 for the halves, 4 for the singles
    assert [len(items_in_request(b)) for b in rec.bodies] == [4, 2, 1, 1, 2, 1, 1]


def test_single_item_cutoff_is_not_fatal(caplog):
    tr, rec = make_translator(lambda body, n: completion("{", finish_reason="length"))
    with caplog.at_level("ERROR", logger="mathtrans.translate.deepseek"):
        results = tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert results == []
    assert "exceeded the output budget" in caplog.text
    assert len(rec.requests) == 2  # the missing id is retried once


def test_missing_ids_are_retried_once():
    def responder(body: dict[str, Any], n: int) -> httpx.Response:
        data = echo(body)
        if n == 1:
            data["translations"] = data["translations"][:1]
        return completion(data)

    tr, rec = make_translator(responder)
    items = [TranslationItem(id="a", text="一"), TranslationItem(id="b", text="二")]
    results = tr.translate(items, Lang.ZH, Lang.EN, [])
    assert [r.id for r in results] == ["a", "b"]
    assert [[it["id"] for it in items_in_request(b)] for b in rec.bodies] == [["a", "b"], ["b"]]


def test_placeholder_problems_are_retried_with_feedback():
    def responder(body: dict[str, Any], n: int) -> httpx.Response:
        items = items_in_request(body)
        if n == 1:
            return completion({"translations": [{"id": it["id"], "text": "dropped"} for it in items]})
        assert any("Placeholder problem" in fb for fb in items[0].get("feedback", []))
        return completion({"translations": [{"id": it["id"], "text": "EN ⟦0⟧ fixed"} for it in items]})

    tr, rec = make_translator(responder)
    results = tr.translate([TranslationItem(id="a", text="⟦0⟧ 元")], Lang.ZH, Lang.EN, [])
    assert results[0].text == "EN ⟦0⟧ fixed"
    assert len(rec.requests) == 2


def test_unparseable_or_malformed_json_yields_no_results(caplog):
    tr, _ = make_translator(lambda body, n: completion("not json at all"))
    assert tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, []) == []
    tr2, _ = make_translator(lambda body, n: completion({"translations": "nope"}))
    assert tr2.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, []) == []
    tr3, _ = make_translator(lambda body, n: completion({"translations": [{"id": "zzz", "text": "x"}, {"id": "a", "text": "  "}, 5]}))
    assert tr3.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, []) == []


def test_markdown_fenced_json_is_accepted():
    tr, _ = make_translator(lambda body, n: completion("```json\n" + json.dumps(echo(body)) + "\n```"))
    results = tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert results[0].text == "EN 你好"


def test_batches_respect_max_chars():
    tr, rec = make_translator(lambda body, n: completion(echo(body)), max_chars=40)
    items = [TranslationItem(id=f"i{k}", text="字" * 15) for k in range(6)]
    results = tr.translate(items, Lang.ZH, Lang.EN, [])
    assert len(results) == 6 and len(rec.requests) >= 3
    assert all(len(items_in_request(b)) <= 2 for b in rec.bodies)


def test_default_batch_is_smaller_than_claude():
    tr, _ = make_translator(lambda body, n: completion(echo(body)), settings=make_settings(batch_chars=12000))
    assert tr.max_chars == ds.DEFAULT_BATCH_CHARS


# --------------------------------------------------------------------------- #
# error mapping / retries
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("status, needle", [
    (401, "DEEPSEEK_API_KEY"),
    (403, "DEEPSEEK_API_KEY"),
    (402, "insufficient balance"),
    (400, "rejected the request"),
    (404, "rejected the request"),
    (422, "rejected the request"),
])
def test_fatal_http_errors(status, needle):
    tr, rec = make_translator(lambda body, n: error(status, "boom"))
    with pytest.raises(TranslationError, match=needle) as exc:
        tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert "boom" in str(exc.value)
    assert len(rec.requests) == 1  # no retry on a definitive failure


def test_transient_errors_are_retried_then_succeed():
    tr, rec = make_translator(lambda body, n: error(503, "busy") if n < 3 else completion(echo(body)))
    results = tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert results[0].text == "EN 你好" and len(rec.requests) == 3


def test_rate_limit_retry_honours_retry_after(monkeypatch):
    waits: list[float] = []
    monkeypatch.setattr(ds.time, "sleep", lambda s: waits.append(s))

    def responder(body: dict[str, Any], n: int) -> httpx.Response:
        if n == 1:
            return httpx.Response(429, json={"error": {"message": "slow down"}}, headers={"retry-after": "7"})
        return completion(echo(body))

    tr, rec = make_translator(responder)
    tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert waits == [7.0] and len(rec.requests) == 2


def test_persistent_server_errors_raise_after_retries():
    tr, rec = make_translator(lambda body, n: error(500, "down"))
    with pytest.raises(TranslationError, match="500"):
        tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert len(rec.requests) == 4  # 1 + max_retries


def test_network_errors_raise_translation_error():
    def responder(body: dict[str, Any], n: int) -> httpx.Response:
        raise httpx.ConnectError("no route")

    tr, rec = make_translator(responder)
    with pytest.raises(TranslationError, match="Could not reach"):
        tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert len(rec.requests) == 4


def test_unexpected_body_is_an_error():
    tr, _ = make_translator(lambda body, n: httpx.Response(200, json={"weird": True}))
    with pytest.raises(TranslationError, match="unexpected response"):
        tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])


def test_usage_is_logged(caplog):
    tr, _ = make_translator(lambda body, n: completion(echo(body)))
    with caplog.at_level("INFO", logger="mathtrans.translate.deepseek"):
        tr.translate([TranslationItem(id="a", text="你好")], Lang.ZH, Lang.EN, [])
    assert "deepseek deepseek-chat: in=100 out=50 cache_read=0 cache_write=0 stop=stop" in caplog.text


# --------------------------------------------------------------------------- #
# review
# --------------------------------------------------------------------------- #


def test_reviewer_parses_findings():
    payload = {"findings": [
        {"id": "a", "severity": "error", "category": "number", "message": "wrong number", "suggested_fix": "fixed ⟦0⟧"},
        {"id": "b", "severity": "nonsense", "category": "grammar", "message": "awkward"},
        {"id": "ghost", "severity": "error", "category": "meaning", "message": "unknown id"},
        {"id": "a", "message": ""},
        "junk",
    ]}
    rec = Recorder(lambda body, n: completion(payload))
    reviewer = DeepSeekReviewer(settings=make_settings(), client=rec.client)
    items = [ReviewItem(id="a", source="共 ⟦0⟧ 元", translation="⟦0⟧ yuan in total"),
             ReviewItem(id="b", source="你好", translation="Hello")]
    findings = reviewer.review(items, Lang.ZH, Lang.EN, [])
    assert [(f.id, f.severity, f.category) for f in findings] == [("a", "error", "number"), ("b", "warning", "grammar")]
    assert findings[0].suggested_fix == "fixed ⟦0⟧" and findings[1].suggested_fix is None
    body = rec.bodies[0]
    assert body["response_format"] == {"type": "json_object"} and "findings" in body["messages"][0]["content"]
    assert reviewer.name == "deepseek"
    assert reviewer.review([], Lang.ZH, Lang.EN, []) == []


def test_reviewer_splits_on_length_and_tolerates_bad_json():
    def responder(body: dict[str, Any], n: int) -> httpx.Response:
        user = [m for m in body["messages"] if m["role"] == "user"][0]["content"]
        count = len(json.loads(user.split("Return JSON only.\n", 1)[1]))
        if count > 1:
            return completion("{", finish_reason="length")
        return completion("garbage" if n == 2 else {"findings": [{"id": "b", "message": "meh"}]})

    rec = Recorder(responder)
    reviewer = DeepSeekReviewer(settings=make_settings(), client=rec.client)
    items = [ReviewItem(id="a", source="一", translation="one"), ReviewItem(id="b", source="二", translation="two")]
    findings = reviewer.review(items, Lang.ZH, Lang.EN, [])
    assert [f.id for f in findings] == ["b"] and len(rec.requests) == 3


# --------------------------------------------------------------------------- #
# configuration / factories
# --------------------------------------------------------------------------- #


def test_settings_resolution(monkeypatch):
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "DEEPSEEK_API_KEY", "MATHTRANS_TRANSLATOR"):
        monkeypatch.delenv(var, raising=False)
    none = Settings(_env_file=None)
    assert none.resolved_translator() == "mock" and not none.has_deepseek_key
    only_ds = Settings(_env_file=None, DEEPSEEK_API_KEY="sk-x")
    assert only_ds.resolved_translator() == "deepseek" and only_ds.has_deepseek_key
    assert only_ds.resolved_translator("mock") == "mock"
    both = Settings(_env_file=None, DEEPSEEK_API_KEY="sk-x", ANTHROPIC_API_KEY="sk-ant")
    assert both.resolved_translator() == "claude"
    assert both.resolved_translator("deepseek") == "deepseek"
    forced = Settings(_env_file=None, DEEPSEEK_API_KEY="sk-x", ANTHROPIC_API_KEY="sk-ant", translator="deepseek")
    assert forced.resolved_translator() == "deepseek"
    monkeypatch.setenv("MATHTRANS_DEEPSEEK_API_KEY", "sk-alias")
    monkeypatch.setenv("MATHTRANS_DEEPSEEK_MODEL", "deepseek-v4-pro")
    env = Settings(_env_file=None)
    assert env.deepseek_api_key == "sk-alias" and env.deepseek_model == "deepseek-v4-pro"
    assert env.resolved_translator() == "deepseek"


def test_factories(monkeypatch):
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "DEEPSEEK_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    without = Settings(_env_file=None, translator="auto")
    with pytest.raises(TranslationError, match="DEEPSEEK_API_KEY"):
        get_translator("deepseek", without)
    with pytest.raises(TranslationError, match="DEEPSEEK_API_KEY"):
        get_reviewer("deepseek", without)
    assert isinstance(get_translator("auto", without), MockTranslator)
    with_key = make_settings(translator="auto")
    tr = get_translator("auto", with_key)
    assert isinstance(tr, DeepSeekTranslator) and tr.model == "deepseek-chat"
    tr2 = get_translator("DeepSeek", with_key, model="deepseek-v4-pro")
    assert tr2.model == "deepseek-v4-pro"
    rv = get_reviewer("deepseek", with_key)
    assert isinstance(rv, DeepSeekReviewer) and rv.model == "deepseek-chat"
    with pytest.raises(ValueError, match="deepseek"):
        get_translator("bing", with_key)


def test_pipeline_uses_deepseek_reviewer_and_records_model(sample_pdf_zh, tmp_path, monkeypatch):
    from mathtrans.pipeline import PipelineOptions, run_pipeline

    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-deepseek-test")
    monkeypatch.setenv("MATHTRANS_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("MATHTRANS_OCR_ENGINE", "none")
    from mathtrans.config import get_settings, reset_settings
    reset_settings()
    try:
        settings = get_settings()
        assert settings.resolved_translator() == "deepseek"
        mock = MockTranslator()

        def responder(body: dict[str, Any], n: int) -> httpx.Response:
            user = [m for m in body["messages"] if m["role"] == "user"][0]["content"]
            raw = json.loads(user.split("Return JSON only.\n", 1)[1])
            if "translations" in body["messages"][0]["content"] and raw and "text" in raw[0]:
                items = [TranslationItem(id=it["id"], text=it["text"]) for it in raw]
                out = mock.translate(items, Lang.ZH, Lang.EN, [])
                return completion({"translations": [{"id": r.id, "text": r.text} for r in out]})
            return completion({"findings": []})

        rec = Recorder(responder)
        clients = iter([rec.client, rec.client])
        monkeypatch.setattr(ds.httpx, "Client", lambda *a, **kw: next(clients))
        opts = PipelineOptions(target_lang=Lang.EN, translator="auto", max_qa_rounds=1, require_qa_pass=False,
                               translate_images=False)
        res = run_pipeline(sample_pdf_zh, tmp_path / "out", opts, settings=settings)
        assert res.stats.translator == "deepseek" and res.stats.model == "deepseek-chat"
        assert any("findings" in b["messages"][0]["content"] for b in rec.bodies), "reviewer was not called"
        assert any("translations" in b["messages"][0]["content"] for b in rec.bodies)
        assert (tmp_path / "out" / "translated.pdf").exists() or any(p.suffix == ".pdf" for p in (tmp_path / "out").iterdir())
    finally:
        reset_settings()
