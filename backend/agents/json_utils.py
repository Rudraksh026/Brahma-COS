"""Defensive parsing helpers for structured LLM responses."""

from __future__ import annotations

import json
import re
from typing import Any


def clean_json_text(content: str) -> str:
    if not isinstance(content, str) or not content.strip():
        raise ValueError("LLM returned an empty response")

    text = content.strip()

    # Remove markdown fences.
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    # Extract the outermost JSON object if the model added prose.
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"LLM did not return a JSON object: {text[:300]}")

    return text[start:end + 1]


def parse_json_object(content: str) -> dict[str, Any]:
    text = clean_json_text(content)

    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        # A common failure from smaller models is single-quoted Python dict output.
        # Do not use eval. Try only a conservative quote normalization fallback.
        normalized = re.sub(r"(?<!\\)'", '"', text)
        try:
            value = json.loads(normalized)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON from LLM: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError("LLM JSON response must be an object")

    return value


def reject_schema_object(value: dict[str, Any], agent_name: str) -> None:
    """Detect the exact failure seen in the original MVP.

    Smaller models sometimes echo Pydantic's JSON schema instead of an instance.
    """
    schema_markers = {"properties", "required", "$defs", "definitions"}
    if schema_markers.intersection(value.keys()):
        raise ValueError(
            f"{agent_name} returned a JSON schema instead of an actual object"
        )
