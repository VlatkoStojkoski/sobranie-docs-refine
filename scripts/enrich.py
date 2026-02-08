#!/usr/bin/env python3
"""
LLM enrichment: analyze collected samples against docs, output aggregated report.

1. For each operation: load samples from collected/
2. Send to LLM: compare response to docs/API_DOCS.md schema
3. Aggregate all LLM responses into docs/ENRICHMENT_REPORT.md

Use the report to prompt an assistant to update API_INDEX.md and API_DOCS.md.

Run: python scripts/enrich.py
Env: ANTHROPIC_API_KEY required
"""

import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
COLLECTED = ROOT / "collected"
LOG_DIR = ROOT / "logs" / "enrich"


def get_latest_collected() -> Path | None:
    if not COLLECTED.exists():
        return None
    runs = sorted(COLLECTED.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    return runs[0] if runs else None


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY")
        return 1

    try:
        from anthropic import Anthropic
    except ImportError:
        print("pip install anthropic")
        return 1

    run_dir = get_latest_collected()
    if not run_dir:
        print("Run collect.py first")
        return 1

    api_docs = (DOCS / "API_DOCS.md").read_text(encoding="utf-8") if (DOCS / "API_DOCS.md").exists() else ""

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_run = LOG_DIR / ts
    log_run.mkdir(parents=True, exist_ok=True)
    print(f"Logging prompts/responses to {log_run}")

    client = Anthropic()
    report_parts = []

    for f in sorted(run_dir.glob("*.json")):
        if f.name == "manifest.json":
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        method = data.get("method", f.stem)
        samples = data.get("samples", [])

        ok_samples = [s for s in samples if s.get("response") and not (isinstance(s["response"], dict) and s["response"].get("_error"))]
        if not ok_samples:
            continue

        # Truncate for token limit
        sample = ok_samples[0]
        resp = sample["response"]
        resp_str = json.dumps(resp, ensure_ascii=False, indent=2)
        if len(resp_str) > 6000:
            resp_str = resp_str[:6000] + "\n... (truncated)"

        prompt = f"""Compare this API response to the documented schema for {method}.

## Documented schema (from API_DOCS.md)
{api_docs[:8000]}

## Actual response (sample)
```json
{resp_str}
```

List any: (1) Fields in response not in docs, (2) Types/values that differ, (3) Schema improvements. Be concise. If nothing to add, say "OK"."""

        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in method)
        (log_run / f"prompt_{safe_name}.txt").write_text(prompt, encoding="utf-8")

        try:
            msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = msg.content[0].text if msg.content else ""
        except Exception as e:
            text = f"ERROR: {e}"

        (log_run / f"response_{safe_name}.txt").write_text(text, encoding="utf-8")
        report_parts.append(f"## {method}\n\n{text}\n")

    DOCS.mkdir(parents=True, exist_ok=True)
    report = "# Enrichment Report\n\nFrom collected samples vs docs/API_DOCS.md.\n\nUse this to prompt an assistant to update API_INDEX.md and API_DOCS.md.\n\n" + "\n---\n\n".join(report_parts)
    (DOCS / "ENRICHMENT_REPORT.md").write_text(report, encoding="utf-8")
    print(f"Wrote {DOCS}/ENRICHMENT_REPORT.md ({len(report_parts)} operations)")


if __name__ == "__main__":
    exit(main())
