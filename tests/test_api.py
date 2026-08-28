"""API contract tests — the OpenAI-compatible surface RedixFi would call."""
from __future__ import annotations

import json
import os

import pytest
from fastapi.testclient import TestClient

from app.api.server import create_app
from app.config.settings import get_settings


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "echo")
    monkeypatch.delenv("API_AUTH_TOKEN", raising=False)
    get_settings(refresh=True)
    return TestClient(create_app())


def test_health_declares_itself_experimental(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["experimental"] is True
    assert body["integrated_into_redixfi"] is False


def test_health_never_leaks_a_secret(client, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-should-never-appear")
    get_settings(refresh=True)
    body = TestClient(create_app()).get("/health").json()
    serialized = json.dumps(body)
    assert "sk-should-never-appear" not in serialized
    assert body["config"]["openai_api_key_set"] is True


def test_models_endpoint_lists_the_registry(client):
    data = client.get("/v1/models").json()
    ids = [m["id"] for m in data["data"]]
    assert "qwen3-14b-awq" in ids
    assert "qwen3-30b-a3b-awq" in ids


def test_chat_completions_matches_the_openai_shape(client):
    response = client.post("/v1/chat/completions", json={
        "model": "qwen3-14b-awq",
        "messages": [
            {"role": "system", "content": "You answer questions about a fact packet."},
            {"role": "user", "content": "Fact packet:\n{}\n\nQuestion: hi"},
        ],
        "temperature": 0,
        "max_tokens": 64,
        "response_format": {"type": "json_object"},
    })
    assert response.status_code == 200
    body = response.json()
    assert body["object"] == "chat.completion"
    assert body["id"].startswith("chatcmpl-")
    assert body["choices"][0]["message"]["role"] == "assistant"
    assert set(body["usage"]) == {"prompt_tokens", "completion_tokens", "total_tokens"}
    # RedixFi parses the content as JSON — it must be parseable.
    assert json.loads(body["choices"][0]["message"]["content"])


def test_streaming_emits_sse_and_terminates(client):
    with client.stream("POST", "/v1/chat/completions", json={
        "messages": [{"role": "user", "content": "hi"}],
        "stream": True,
    }) as response:
        assert response.status_code == 200
        payload = "".join(response.iter_text())
    assert "data: " in payload
    assert payload.rstrip().endswith("[DONE]")


def test_auth_is_enforced_when_a_token_is_configured(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "echo")
    monkeypatch.setenv("API_AUTH_TOKEN", "secret-token")
    get_settings(refresh=True)
    guarded = TestClient(create_app())

    assert guarded.get("/v1/models").status_code == 401
    assert guarded.get(
        "/v1/models", headers={"Authorization": "Bearer wrong"}
    ).status_code == 401
    assert guarded.get(
        "/v1/models", headers={"Authorization": "Bearer secret-token"}
    ).status_code == 200
    # /health stays open so a container probe works without a credential.
    assert guarded.get("/health").status_code == 200


def test_metrics_count_requests(client):
    client.post("/v1/chat/completions",
                json={"messages": [{"role": "user", "content": "hi"}]})
    metrics = client.get("/metrics").json()
    assert metrics["requests"] >= 1
    assert "by_model" in metrics
