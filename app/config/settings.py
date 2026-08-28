"""Central configuration. Every value comes from the environment (or a
Kaggle Secret), never from a committed literal.

ARCHITECTURE NOTE — do not "improve" this into a network config.
RedixFi's MongoDB is bound to loopback on its VM and its ChromaDB is an
embedded chromadb.PersistentClient over a local directory. There is
therefore CHROMA_PATH and deliberately no CHROMA_HOST/CHROMA_PORT. The
data-access settings below are used ONLY by scripts/export_fixtures.py,
which runs ON the RedixFi VM. Kaggle never reads a database.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional


def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


def _env_int(key: str, default: int) -> int:
    raw = _env(key)
    try:
        return int(raw) if raw else default
    except ValueError:
        return default


def _env_float(key: str, default: float) -> float:
    raw = _env(key)
    try:
        return float(raw) if raw else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    # --- inference ---------------------------------------------------------
    backend: str = field(default_factory=lambda: _env("LLM_BACKEND", "echo"))
    model: str = field(default_factory=lambda: _env("LLM_MODEL", "qwen3-14b-awq"))
    vllm_base_url: str = field(
        default_factory=lambda: _env("VLLM_BASE_URL", "http://127.0.0.1:8000/v1")
    )
    temperature: float = field(default_factory=lambda: _env_float("LLM_TEMPERATURE", 0.0))
    seed: int = field(default_factory=lambda: _env_int("LLM_SEED", 0))
    max_tokens: int = field(default_factory=lambda: _env_int("LLM_MAX_TOKENS", 1024))
    request_timeout_sec: int = field(
        default_factory=lambda: _env_int("LLM_REQUEST_TIMEOUT_SEC", 180)
    )

    # --- this project's own API -------------------------------------------
    api_host: str = field(default_factory=lambda: _env("API_HOST", "0.0.0.0"))
    api_port: int = field(default_factory=lambda: _env_int("API_PORT", 8080))
    api_auth_token: str = field(default_factory=lambda: _env("API_AUTH_TOKEN"))

    # --- credentials (never logged) ---------------------------------------
    hf_token: str = field(default_factory=lambda: _env("HF_TOKEN"))
    openai_api_key: str = field(default_factory=lambda: _env("OPENAI_API_KEY"))

    # --- RedixFi read-only access (VM only; see module docstring) ---------
    mongo_uri: str = field(
        default_factory=lambda: _env("MONGO_URI", "mongodb://127.0.0.1:27017")
    )
    mongo_db_name: str = field(default_factory=lambda: _env("MONGO_DB_NAME", "redixfi"))
    mongo_app_db_name: str = field(
        default_factory=lambda: _env("MONGO_APP_DB_NAME", "redixfi_app")
    )
    chroma_path: str = field(
        default_factory=lambda: _env(
            "CHROMA_PATH", "/home/ubuntu/redixfi-backend/data/chroma_production"
        )
    )
    redixfi_root: str = field(
        default_factory=lambda: _env("REDIXFI_ROOT", "/home/ubuntu/redixfi-backend")
    )

    def redacted(self) -> dict:
        """Safe-to-log view. Secrets become a presence flag, never a value."""
        return {
            "backend": self.backend,
            "model": self.model,
            "vllm_base_url": self.vllm_base_url,
            "temperature": self.temperature,
            "seed": self.seed,
            "max_tokens": self.max_tokens,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "api_auth_token_set": bool(self.api_auth_token),
            "hf_token_set": bool(self.hf_token),
            "openai_api_key_set": bool(self.openai_api_key),
            "mongo_db_name": self.mongo_db_name,
            "chroma_path": self.chroma_path,
        }


_settings: Optional[Settings] = None


def get_settings(refresh: bool = False) -> Settings:
    global _settings
    if _settings is None or refresh:
        _load_dotenv_if_present()
        _settings = Settings()
    return _settings


def _load_dotenv_if_present() -> None:
    """Minimal .env loader — avoids a python-dotenv dependency on Kaggle,
    where the package may not be installed. Existing environment variables
    always win, so a Kaggle Secret is never overwritten by a stray file."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, ".env")
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        pass
