"""Defensive parsing helpers for structured LLM responses."""

from __future__ import annotations

import json
from typing import Any


def clean_json_text(content: str) -> str:
    if not isinstance(content, str) or not content.strip():
        raise ValueError("LLM returned an empty response")

    text = content.strip()

    # Remove common markdown fences.
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        else:
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    # Some models prepend a short sentence. Extract the outermost JSON object.
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"LLM did not return a JSON object: {text[:300]}")

    return text[start : end + 1]


def parse_json_object(content: str) -> dict[str, Any]:
    text = clean_json_text(content)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON from LLM: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError("LLM JSON response must be an object")

    return value
