"""
LLM client for Anthropic Claude. Supports structured JSON output.
"""

import json
import logging
import os
import time
from pathlib import Path

log = logging.getLogger("llm")

# Load .env from project root so ANTHROPIC_API_KEY is available
try:
    from dotenv import load_dotenv
    root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(root / ".env")
except ImportError:
    pass


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



def complete_structured(
    prompt: str,
    schema: dict,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int | None = None,
) -> dict:
    """
    Send prompt with structured output (output_config.format).
    Returns parsed JSON matching schema. Requires models with structured output support
    (claude-sonnet-4-5, claude-haiku-4-5, claude-opus-4-5, claude-opus-4-6).
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("Set ANTHROPIC_API_KEY")
    return _anthropic_complete_structured(
        prompt, schema, system, model, max_tokens
    )


def _anthropic_complete(
    prompt: str,
    system: str | None,
    model: str | None,
    max_tokens: int | None,
) -> str:
    from anthropic import Anthropic

    client = Anthropic()
    m = model or "claude-sonnet-4-20250514"
    log.debug("complete: model=%s", m)
    t0 = time.perf_counter()
    kwargs = {
        "model": m,
        "max_tokens": max_tokens if max_tokens is not None else 16000,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    msg = client.messages.create(**kwargs)
    elapsed = time.perf_counter() - t0
    usage = getattr(msg, "usage", None)
    tok = f", in={usage.input_tokens} out={usage.output_tokens}" if usage else ""
    stop = getattr(msg, "stop_reason", None)
    log.info("complete done: %.1fs%s, stop=%s", elapsed, tok, stop)
    if stop == "max_tokens":
        log.warning("complete response truncated (stop_reason=max_tokens)")
    return msg.content[0].text if msg.content else ""


def _anthropic_complete_structured(
    prompt: str,
    schema: dict,
    system: str | None,
    model: str | None,
    max_tokens: int | None,
) -> dict:
    from anthropic import Anthropic

    # Structured output can be large; use 20min timeout to avoid "Streaming is required" error
    client = Anthropic(timeout=1200.0)
    m = model or "claude-haiku-4-5"
    log.debug("complete_structured: model=%s", m)
    t0 = time.perf_counter()
    kwargs = {
        "model": m,
        "max_tokens": max_tokens if max_tokens is not None else 16000,
        "messages": [{"role": "user", "content": prompt}],
        "output_config": {
            "format": {"type": "json_schema", "schema": schema},
        },
    }
    if system:
        kwargs["system"] = system
    msg = client.messages.create(**kwargs)
    elapsed = time.perf_counter() - t0
    usage = getattr(msg, "usage", None)
    tok = f", in={usage.input_tokens} out={usage.output_tokens}" if usage else ""
    stop = getattr(msg, "stop_reason", None)
    log.info("complete_structured done: %.1fs%s, stop=%s", elapsed, tok, stop)
    if stop == "max_tokens":
        raise RuntimeError(
            f"Structured output truncated (stop_reason=max_tokens, "
            f"max_tokens={kwargs.get('max_tokens')}). "
            f"Response may be incomplete; skipping to avoid data corruption."
        )
    text = msg.content[0].text if msg.content else "{}"
    return json.loads(text)
