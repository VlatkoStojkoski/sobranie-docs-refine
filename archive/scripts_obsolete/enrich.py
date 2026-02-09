#!/usr/bin/env python3
"""
LLM enrichment: analyze collected samples against docs, output aggregated report.

1. For each operation: load samples from collected/
2. Extract that operation's schema from API_DOCS.md (full context, not truncated)
3. Include $defs, Common patterns, schema_inference when available
4. Use multiple samples (up to 3) for richer comparison
5. Aggregate all LLM responses into docs/ENRICHMENT_REPORT.md

Use the report to prompt an assistant to update API_INDEX.md and API_DOCS.md.

Run: python scripts/enrich.py
Env: ANTHROPIC_API_KEY required
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
COLLECTED = ROOT / "collected"
LOG_DIR = ROOT / "logs" / "enrich"

MAX_SAMPLES = 3
MAX_SAMPLE_CHARS = 5000


def get_latest_collected() -> Path | None:
    if not COLLECTED.exists():
        return None
    runs = sorted(COLLECTED.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    return runs[0] if runs else None


def extract_section(text: str, heading: str) -> str:
    """Extract content from ## Heading to next ## or end."""
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"\n## ", text[start:])
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def extract_prefix(text: str) -> str:
    """Extract $defs and Common patterns (everything before first operation)."""
    first_op = re.search(r"\n## GetAll|\n## Get[A-Z]", text)
    if not first_op:
        return text[:4000]
    return text[: first_op.start()].strip()


def build_prompt(method: str, doc_section: str, prefix: str, samples: list, inferred: dict | None) -> str:
    """Build enrichment prompt with full context."""
    samples_text = []
    for i, s in enumerate(samples[:MAX_SAMPLES]):
        resp = s.get("response")
        if resp is None:
            continue
        resp_str = json.dumps(resp, ensure_ascii=False, indent=2)
        if len(resp_str) > MAX_SAMPLE_CHARS:
            resp_str = resp_str[:MAX_SAMPLE_CHARS] + "\n... (truncated)"
        lbl = f"Sample {i + 1}" if len(samples) > 1 else "Actual response"
        samples_text.append(f"### {lbl}\n```json\n{resp_str}\n```")

    inferred_block = ""
    if inferred:
        inferred_block = f"\n## Inferred schema (from schema_inference.json)\n```json\n{json.dumps(inferred, indent=2)}\n```\n"

    doc_block = f"## Documented schema for {method}\n{doc_section}" if doc_section else f"(No documented schema for {method})"

    return f"""Compare the actual API response(s) below to the documented schema for {method}.

## $defs and Common patterns (from API_DOCS.md)
{prefix}

{doc_block}
{inferred_block}

## Actual response(s) from collected data
{chr(10).join(samples_text)}

List:
1. Fields in response not in docs
2. Types/values that differ from docs
3. Concrete schema improvements (use $defs refs where applicable)

Be concise. If nothing to add, say "OK"."""


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
    prefix = extract_prefix(api_docs)  # $defs + Common patterns

    inference = {}
    if (ROOT / "schema_inference.json").exists():
        try:
            inference = json.loads((ROOT / "schema_inference.json").read_text())
        except Exception:
            pass

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

        ok_samples = [
            s
            for s in samples
            if s.get("response") and not (isinstance(s["response"], dict) and s["response"].get("_error"))
        ]
        if not ok_samples:
            continue

        doc_section = extract_section(api_docs, method)
        inferred = inference.get("endpoints", {}).get(method, {}).get("schema")

        prompt = build_prompt(method, doc_section, prefix, ok_samples, inferred)

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
    report = (
        "# Enrichment Report\n\nFrom collected samples vs docs/API_DOCS.md.\n\n"
        "Use this to prompt an assistant to update API_INDEX.md and API_DOCS.md.\n\n"
        + "\n---\n\n".join(report_parts)
    )
    (DOCS / "ENRICHMENT_REPORT.md").write_text(report, encoding="utf-8")
    print(f"Wrote {DOCS}/ENRICHMENT_REPORT.md ({len(report_parts)} operations)")


if __name__ == "__main__":
    exit(main())
