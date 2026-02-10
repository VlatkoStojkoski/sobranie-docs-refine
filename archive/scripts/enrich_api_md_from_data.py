#!/usr/bin/env python3
"""
Optional: Use LLM to merge API_DOC_FROM_DATA.md into API.md.
Keeps API.md prose ($defs, notes, common patterns) while updating
request/response schemas from collected data.

Run: python scripts/enrich_api_md_from_data.py
Env: ANTHROPIC_API_KEY required
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DOC = ROOT / "API_DOC_FROM_DATA.md"
API_MD = ROOT / "API.md"
OUTPUT = ROOT / "API_ENRICHMENT_REPORT.md"


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY to run LLM enrichment.")
        return 1

    try:
        from anthropic import Anthropic
    except ImportError:
        print("Install anthropic: pip install anthropic")
        return 1

    if not DATA_DOC.exists():
        print("Run sync_docs.py first to generate API_DOC_FROM_DATA.md")
        return 1

    data_doc = DATA_DOC.read_text(encoding="utf-8")
    api_md = API_MD.read_text(encoding="utf-8") if API_MD.exists() else ""

    client = Anthropic()
    prompt = f"""You are synchronizing API documentation. We have:

1. **API_DOC_FROM_DATA.md** — machine-generated from real API responses (100% accurate):
{data_doc[:12000]}

2. **API.md** — human-written reference with prose, $defs, common patterns:
{api_md[:12000]}

Your task: Produce a report (API_ENRICHMENT_REPORT.md) that lists:
- For each endpoint in API_DOC_FROM_DATA: Does API.md have it? Any schema differences?
- Suggested updates: Which request examples or response schemas in API.md should be replaced with the data-driven versions?
- Preserve: API.md's $defs, Common patterns, Notes, and endpoint-specific notes - these add value. Only suggest replacing the JSON blocks (request body example, response schema) where the data-driven version differs.

Output format: Markdown report suitable to save as API_ENRICHMENT_REPORT.md. Be concise."""

    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text if resp.content else ""

    OUTPUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    exit(main())
