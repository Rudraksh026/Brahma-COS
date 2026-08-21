"""Production-safe LiteLLM configuration for BRAHMA COS agents."""

from __future__ import annotations

import os
from typing import Any, Dict, List

try:
    from litellm import completion
except ImportError:  # pragma: no cover
    completion = None


DEFAULT_MODEL = "ollama/llama3.2:3b"
DEFAULT_OLLAMA_BASE = "http://localhost:11434"
DEFAULT_OPENROUTER_BASE = "https://openrouter.ai/api/v1"


def get_model() -> str:
    return os.getenv("LLM_MODEL", DEFAULT_MODEL).strip()


def is_ollama(model: str) -> bool:
    return model.startswith("ollama/")


def is_openrouter(model: str) -> bool:
    return model.startswith("openrouter/")


def _base_kwargs(model: str) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        "model": model,
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0")),
        "timeout": float(os.getenv("LLM_TIMEOUT", "60")),
    }

    if is_ollama(model):
        kwargs["api_base"] = os.getenv("OLLAMA_API_BASE", DEFAULT_OLLAMA_BASE)

    if is_openrouter(model):
        # LiteLLM reads OPENROUTER_API_KEY automatically. Keep the explicit
        # check here so deployment errors are clear instead of mysterious.
        if not os.getenv("OPENROUTER_API_KEY"):
            raise RuntimeError("OPENROUTER_API_KEY is not configured")
        kwargs["api_base"] = os.getenv("OPENROUTER_API_BASE", DEFAULT_OPENROUTER_BASE)

        # Optional attribution headers accepted by OpenRouter.
        site_url = os.getenv("OPENROUTER_SITE_URL", "").strip()
        app_name = os.getenv("OPENROUTER_APP_NAME", "BRAHMA COS").strip()
        if site_url:
            kwargs["extra_headers"] = {
                "HTTP-Referer": site_url,
                "X-Title": app_name,
            }

    return kwargs


def llm_completion(
    messages: List[Dict[str, str]],
    *,
    json_mode: bool = True,
) -> Any:
    """Call the configured LLM with provider-aware settings.

    JSON mode is requested when possible. If the provider rejects the
    parameter, retry once without it. The caller still validates the output.
    """
    if completion is None:
        raise RuntimeError("LiteLLM is not installed")

    model = get_model()
    kwargs = _base_kwargs(model)
    kwargs["messages"] = messages

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    try:
        return completion(**kwargs)
    except Exception as first_error:
        if not json_mode:
            raise

        # Some OpenAI-compatible providers/models do not accept response_format.
        # Retry without it, then validate strictly in the calling node.
        kwargs.pop("response_format", None)
        try:
            return completion(**kwargs)
        except Exception:
            raise first_error
