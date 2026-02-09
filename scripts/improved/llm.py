"""
LLM client for Anthropic Claude. Supports structured JSON output.
"""

import json
import os
from pathlib import Path

# Load .env from project root so ANTHROPIC_API_KEY is available
try:
    from dotenv import load_dotenv
    root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(root / ".env")
except ImportError:
    pass
import re


def _strip_markdown_json(text: str) -> str:
    """Remove markdown code fences from response."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text


def complete(
    prompt: str,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int | None = None,
) -> str:
    """
    Send prompt to Claude and return raw text.
    Requires ANTHROPIC_API_KEY.
    max_tokens: override default; use 8192 for Haiku (e.g. claude-3-5-haiku).
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("Set ANTHROPIC_API_KEY")
    return _anthropic_complete(prompt, system, model, max_tokens)


def complete_json(
    prompt: str,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int | None = None,
) -> dict | list:
    """Send prompt and parse response as JSON."""
    text = complete(prompt, system, model, max_tokens)
    text = _strip_markdown_json(text)
    return json.loads(text)


def _anthropic_complete(
    prompt: str,
    system: str | None,
    model: str | None,
    max_tokens: int | None,
) -> str:
    from anthropic import Anthropic

    client = Anthropic()
    m = model or "claude-sonnet-4-20250514"
    kwargs = {
        "model": m,
        "max_tokens": max_tokens if max_tokens is not None else 16000,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    msg = client.messages.create(**kwargs)
    return msg.content[0].text if msg.content else ""
