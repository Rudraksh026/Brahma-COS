"""Production-safe LiteLLM configuration for BRAHMA COS."""

from __future__ import annotations

import os
from typing import Any, Dict, List

try:
    from litellm import completion
except ImportError:  # pragma: no cover
    completion = None


DEFAULT_MODEL = "openrouter/free"
DEFAULT_OLLAMA_BASE = "http://localhost:11434"
DEFAULT_OPENROUTER_BASE = "https://openrouter.ai/api/v1"


def get_model() -> str:
    return os.getenv("LLM_MODEL", DEFAULT_MODEL).strip()


def is_ollama(model: str) -> bool:
    return model.lower().startswith("ollama/")


def is_openrouter(model: str) -> bool:
    return model.lower().startswith("openrouter/")


def _base_kwargs(model: str) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        "model": model,
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0")),
        "timeout": float(os.getenv("LLM_TIMEOUT", "60")),
    }

    if is_ollama(model):
        kwargs["api_base"] = os.getenv(
            "OLLAMA_API_BASE", DEFAULT_OLLAMA_BASE
        )

    if is_openrouter(model):
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")
        kwargs["api_key"] = api_key
        kwargs["api_base"] = os.getenv(
            "OPENROUTER_API_BASE", DEFAULT_OPENROUTER_BASE
        )

        site_url = os.getenv("OPENROUTER_SITE_URL", "").strip()
        app_name = os.getenv("OPENROUTER_APP_NAME", "BRAHMA COS").strip()
        headers = {"X-Title": app_name}
        if site_url:
            headers["HTTP-Referer"] = site_url
        kwargs["extra_headers"] = headers

    return kwargs


def llm_completion(
    messages: List[Dict[str, str]],
    *,
    json_mode: bool = True,
) -> Any:
    """Call the configured provider.

    We intentionally do not force response_format for openrouter/free because
    the free router can select models with different structured-output support.
    The agents enforce JSON through prompts plus strict Pydantic validation.
    """
    if completion is None:
        raise RuntimeError("LiteLLM is not installed")

    model = get_model()
    kwargs = _base_kwargs(model)
    kwargs["messages"] = messages

    # Only request JSON mode when explicitly enabled for a provider known to
    # support it. openrouter/free is intentionally left prompt-constrained.
    if json_mode and not is_openrouter(model):
        kwargs["response_format"] = {"type": "json_object"}

    return completion(**kwargs)
