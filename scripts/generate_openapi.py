#!/usr/bin/env python3
"""
Generate docs/openapi.yaml from docs/API_DOCS.md via single LLM call.

Run: python scripts/generate_openapi.py
Env: ANTHROPIC_API_KEY required
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY")
        return 1

    try:
        from anthropic import Anthropic
    except ImportError:
        print("pip install anthropic")
        return 1

    api_docs = (DOCS / "API_DOCS.md").read_text(encoding="utf-8")
    api_index = (DOCS / "API_INDEX.md").read_text(encoding="utf-8") if (DOCS / "API_INDEX.md").exists() else ""

    prompt = f"""Convert the following API documentation into a valid OpenAPI 3.0 YAML spec.

## API Index (routes, formats)
{api_index[:4000]}

## API Docs (request/response schemas)
{api_docs[:16000]}

Produce a complete openapi.yaml with:
- info, servers
- paths: /Routing/MakePostRequest (POST, examples for each method), plus non-standard paths for GetCustomEventsCalendar, LoadLanguage, GetOfficialVisitsForUser
- components/schemas: AspDate, RpcRequest, and response schemas per operation
- All arrays must have items. Use nullable: true for optional nulls.
- Request examples in the MakePostRequest requestBody examples

Output ONLY valid YAML, no markdown fences."""

    client = Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text if msg.content else ""

    # Strip markdown if present
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    (DOCS / "openapi.yaml").write_text(text, encoding="utf-8")
    print(f"Wrote {DOCS}/openapi.yaml")


if __name__ == "__main__":
    exit(main())
