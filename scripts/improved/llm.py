"""
LLM client for Anthropic or OpenAI. Supports structured JSON output.
"""

import json
import os
from pathlib import Path

# Load .env from project root so ANTHROPIC_API_KEY / OPENAI_API_KEY are available
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


def complete(prompt: str, system: str | None = None, model: str | None = None) -> str:
    """
    Send prompt to LLM and return raw text.
    Uses ANTHROPIC_API_KEY or OPENAI_API_KEY (prefers Anthropic).
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        return _anthropic_complete(prompt, system, model)
    if os.environ.get("OPENAI_API_KEY"):
        return _openai_complete(prompt, system, model)
    raise RuntimeError("Set ANTHROPIC_API_KEY or OPENAI_API_KEY")


def complete_json(prompt: str, system: str | None = None, model: str | None = None) -> dict | list:
    """Send prompt and parse response as JSON."""
    text = complete(prompt, system, model)
    text = _strip_markdown_json(text)
    return json.loads(text)


def _anthropic_complete(prompt: str, system: str | None, model: str | None) -> str:
    from anthropic import Anthropic

    client = Anthropic()
    m = model or "claude-sonnet-4-20250514"
    kwargs = {
        "model": m,
        "max_tokens": 16000,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    msg = client.messages.create(**kwargs)
    return msg.content[0].text if msg.content else ""


def _openai_complete(prompt: str, system: str | None, model: str | None) -> str:
    from openai import OpenAI

    client = OpenAI()
    m = model or "gpt-4o"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=m,
        messages=messages,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content or ""
