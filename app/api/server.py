"""OpenAI-compatible API — the future drop-in seam for RedixFi.

WHY THIS EXISTS
---------------
RedixFi calls `https://api.openai.com/v1/chat/completions` from exactly
three places (annual_report_summarizer.py, risk_flag_classifier.py,
core/ask.py), all with the same JSON-mode/temperature-0 shape. Serving that
same contract here means a future switch is a base-URL change per call
site, not an architectural change.

NOTHING IN REDIXFI POINTS HERE YET, and nothing should until the evaluation
is complete. This service is EXPERIMENTAL.

Endpoints:
  POST /v1/chat/completions   (streaming supported via `stream: true`)
  GET  /v1/models
  GET  /health
  GET  /metrics               (in-process counters, not Prometheus)
"""
from __future__ import annotations

import json
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..config.settings import get_settings
from ..inference.base import GenerationRequest, Message
from ..inference.factory import build_backend
from ..models.registry import list_models
from ..obs.logging import RequestLog, get_logger

logger = get_logger(__name__)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: List[ChatMessage]
    temperature: float = 0.0
    max_tokens: int = 1024
    seed: Optional[int] = 0
    stream: bool = False
    stop: Optional[List[str]] = None
    response_format: Optional[Dict[str, Any]] = None
    # Accepted and ignored, for OpenAI client compatibility.
    top_p: Optional[float] = None
    n: Optional[int] = Field(default=1)
    user: Optional[str] = None


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="RedixFi self-hosted LLM (EXPERIMENTAL)",
        version="0.1.0",
        description=(
            "OpenAI-compatible inference service. EXPERIMENTAL — not integrated "
            "into RedixFi production."
        ),
    )
    app.state.backend = build_backend(settings)
    app.state.settings = settings
    app.state.request_log = RequestLog()

    def require_auth(authorization: Optional[str] = Header(default=None)) -> None:
        token = settings.api_auth_token
        if not token:
            return  # open by default; set API_AUTH_TOKEN to lock it down
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="missing bearer token")
        if authorization[len("Bearer "):].strip() != token:
            raise HTTPException(status_code=401, detail="invalid bearer token")

    @app.get("/health")
    def health() -> Dict[str, Any]:
        backend_health = app.state.backend.health()
        return {
            "status": "ok" if backend_health.get("status") in ("ok", "unknown") else "degraded",
            "experimental": True,
            "integrated_into_redixfi": False,
            "backend": backend_health,
            "config": settings.redacted(),
            "uptime_sec": round(app.state.request_log.uptime_sec(), 1),
        }

    @app.get("/metrics")
    def metrics() -> Dict[str, Any]:
        return app.state.request_log.snapshot()

    @app.get("/v1/models")
    def models(_: None = Depends(require_auth)) -> Dict[str, Any]:
        return {
            "object": "list",
            "data": [
                {"id": name, "object": "model", "owned_by": "redixfi-llm"}
                for name in list_models()
            ],
        }

    @app.post("/v1/chat/completions")
    def chat_completions(
        body: ChatCompletionRequest, _: None = Depends(require_auth)
    ) -> Any:
        model = body.model or settings.model
        json_mode = bool(
            body.response_format and body.response_format.get("type") == "json_object"
        )
        request = GenerationRequest(
            messages=[Message(m.role, m.content) for m in body.messages],
            model=model,
            temperature=body.temperature,
            max_tokens=body.max_tokens,
            seed=body.seed,
            json_mode=json_mode,
            stop=body.stop,
        )
        completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
        created = int(time.time())

        if body.stream:
            def event_stream():
                started = time.perf_counter()
                emitted = 0
                for piece in app.state.backend.stream(request):
                    emitted += len(piece)
                    chunk = {
                        "id": completion_id, "object": "chat.completion.chunk",
                        "created": created, "model": model,
                        "choices": [{"index": 0, "delta": {"content": piece},
                                     "finish_reason": None}],
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                done = {
                    "id": completion_id, "object": "chat.completion.chunk",
                    "created": created, "model": model,
                    "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                }
                yield f"data: {json.dumps(done)}\n\n"
                yield "data: [DONE]\n\n"
                app.state.request_log.record(
                    model=model, latency_sec=time.perf_counter() - started,
                    prompt_tokens=0, completion_tokens=0, ok=True, streamed=True,
                )
            return StreamingResponse(event_stream(), media_type="text/event-stream")

        result = app.state.backend.generate(request)
        app.state.request_log.record(
            model=model, latency_sec=result.latency_sec,
            prompt_tokens=result.prompt_tokens,
            completion_tokens=result.completion_tokens,
            ok=result.ok, streamed=False,
        )
        if not result.ok:
            logger.error("generation failed: %s", result.error)
            raise HTTPException(status_code=502, detail=result.error)

        return {
            "id": completion_id,
            "object": "chat.completion",
            "created": created,
            "model": result.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": result.text},
                "finish_reason": result.finish_reason or "stop",
            }],
            "usage": {
                "prompt_tokens": result.prompt_tokens,
                "completion_tokens": result.completion_tokens,
                "total_tokens": result.total_tokens,
            },
        }

    return app


app = create_app()
