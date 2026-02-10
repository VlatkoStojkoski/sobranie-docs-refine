#!/usr/bin/env python3
"""
HAR file analysis for API discovery. Two-level LLM filtering:

1. Level 1 (minimal tokens): Quick relevance check per request. Pass only URL, method,
   status, and tiny req/res body snippets. Goal: filter out static assets, analytics,
   third-party CDNs, etc.

2. Level 2 (detailed): For each relevant request, analyze full sanitized req/res and
   write structured notes to an aggregate file. Discovers new methods, non-standard
   routes, document/media URLs, and enrichable API patterns.

Usage:
  python scripts/analyze_har.py path/to/capture.har
  python scripts/analyze_har.py path/to/*.har   # processes all

Output: HAR_ANALYSIS_FINDINGS.md
Logs: har_analysis_logs/YYYY-MM-DD_HH-MM-SS/ (prompts, responses, index)
"""

import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Config
MAX_LEVEL1_SNIPPET = 400   # chars total for req+res in level 1
MAX_LEVEL2_BODY = 12000    # chars per body in level 2
MAX_ARRAY_ITEMS = 8
MAX_STRING_LEN = 600
OUTPUT = "HAR_ANALYSIS_FINDINGS.md"
LOG_DIR = "har_analysis_logs"
CONCURRENCY = int(os.environ.get("HAR_CONCURRENCY", "5"))  # parallel requests
BATCH_DELAY = float(os.environ.get("HAR_BATCH_DELAY", "0.5"))  # sec between batches

# Pre-filter: skip these URL patterns before Level 1 (saves tokens)
SKIP_URL_PATTERNS = (
    ".js", ".css", ".map", ".woff", ".woff2", ".ttf", ".ico",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    "google-analytics", "googletagmanager", "analytics",
    "facebook.com", "twitter.com", "doubleclick",
)


def project_root() -> Path:
    return Path(__file__).parent.parent


def approx_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return max(1, len(str(text)) // 4)


class PromptLogger:
    """Save prompts and responses to timestamped log dir for debugging."""

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.index: list[dict] = []
        self._counter = {"level1": 0, "level2": 0}
        (log_dir / "README.txt").write_text(
            "HAR analysis debug logs. Each prompt sent to Claude is saved before the API call.\n"
            "levelN_XXXX_prompt.txt = full prompt text\n"
            "levelN_XXXX_meta.json = metadata (url, estimated tokens, etc.)\n"
            "levelN_XXXX_response.txt = model response\n"
            "index.json = all interactions; run_summary.json = run stats\n",
            encoding="utf-8",
        )

    def _next_id(self, level: str) -> int:
        self._counter[level] += 1
        return self._counter[level]

    def save_prompt(self, level: str, prompt: str, meta: dict) -> str:
        """Save prompt to file, return filename stem (e.g. level1_042)."""
        n = self._next_id(level)
        stem = f"{level}_{n:04d}"
        prompt_path = self.log_dir / f"{stem}_prompt.txt"
        meta_path = self.log_dir / f"{stem}_meta.json"
        prompt_path.write_text(prompt, encoding="utf-8")
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        meta["_stem"] = stem
        meta["_prompt_path"] = str(prompt_path)
        return stem

    def save_response(self, stem: str, response: str, extra: dict | None = None):
        """Save response and append to index."""
        resp_path = self.log_dir / f"{stem}_response.txt"
        resp_path.write_text(response, encoding="utf-8")
        entry = {"stem": stem, "response_path": str(resp_path), **(extra or {})}
        self.index.append(entry)

    def save_index(self, run_summary: dict | None = None):
        """Write index.json with all logged interactions and optional run_summary.json."""
        idx_path = self.log_dir / "index.json"
        idx_path.write_text(json.dumps(self.index, indent=2), encoding="utf-8")
        if run_summary:
            summary_path = self.log_dir / "run_summary.json"
            summary_path.write_text(json.dumps(run_summary, indent=2), encoding="utf-8")


def extract_post_data(entry: dict) -> str | None:
    """Get decoded POST body from HAR entry."""
    req = entry.get("request", {})
    post = req.get("postData") or {}
    text = post.get("text")
    if not text:
        return None
    # HAR stores as string; may be JSON
    if len(text) > 2000:
        return text[:2000] + f"... (truncated, total {len(text)} chars)"
    return text


def extract_response_body(entry: dict) -> tuple[str | None, str]:
    """Return (decoded_body, content_type)."""
    res = entry.get("response", {})
    content = res.get("content", {}) or {}
    ct = (content.get("encoding") or "").lower()
    text = content.get("text")
    if not text:
        return None, content.get("mimeType", "") or ""

    # HAR can have base64-encoded content
    if ct == "base64":
        return f"[base64, {len(text)} bytes]", content.get("mimeType", "") or ""

    if isinstance(text, str) and len(text) > 3000:
        return text[:3000] + f"... (truncated, total {len(text)} chars)", content.get("mimeType", "") or ""
    return text, content.get("mimeType", "") or ""


def minimal_snippet(text: str | None, max_len: int) -> str:
    """Produce a tiny snippet for level 1."""
    if not text:
        return ""
    s = text.strip()
    if len(s) <= max_len:
        return s
    return s[:max_len].rstrip() + "..."


def parse_json_safely(text: str) -> dict | list | None:
    try:
        return json.loads(text)
    except Exception:
        return None


def extract_method_name_from_body(body: str | None) -> str | None:
    """Extract methodName/MethodName from JSON body if present."""
    if not body:
        return None
    obj = parse_json_safely(body)
    if isinstance(obj, dict):
        return obj.get("methodName") or obj.get("MethodName")


def build_level1_payload(entry: dict, index: int) -> dict:
    """Build minimal payload for relevance check. Few tokens."""
    req = entry.get("request", {})
    res = entry.get("response", {})
    url = req.get("url", "")
    method = req.get("method", "")
    status = res.get("status", 0)

    post_text = extract_post_data(entry)
    res_body, mime = extract_response_body(entry)

    method_name = extract_method_name_from_body(post_text)
    req_snip = ""
    if post_text:
        req_snip = minimal_snippet(post_text, 180)
        if method_name:
            req_snip = f"methodName={method_name} | " + req_snip[:100]

    res_snip = ""
    if res_body and isinstance(res_body, str) and not res_body.startswith("[base64"):
        res_snip = minimal_snippet(res_body, 200)

    return {
        "n": index + 1,
        "url": url,
        "method": method,
        "status": status,
        "req": req_snip,
        "res_mime": mime,
        "res_snip": res_snip,
    }


def sanitize_body(text: str | None, max_len: int) -> str:
    """Sanitize and truncate body for level 2. Strip base64, truncate arrays/strings."""
    if not text or not isinstance(text, str):
        return ""
    if text.startswith("[base64"):
        return text

    obj = parse_json_safely(text)
    if obj is not None:
        sanitized = _sanitize_json(obj)
        out = json.dumps(sanitized, ensure_ascii=False, indent=2)
        if len(out) > max_len:
            return out[:max_len] + f"\n... (truncated, total {len(json.dumps(sanitized))} chars)"
        return out

    # Non-JSON (HTML, etc.)
    if len(text) > max_len:
        return text[:max_len] + f"\n... (truncated, total {len(text)} chars)"
    return text


def _sanitize_json(obj, depth: int = 0) -> dict | list | str | int | float | bool | None:
    """Recursively sanitize: truncate arrays, shorten long strings, strip base64."""
    if depth > 15:
        return {"_depth_limit": "..."}

    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("UserImg", "Image", "content", "data") and isinstance(v, str) and len(v) > 100:
                out[k] = f"[truncated string, {len(v)} chars]"
            else:
                out[k] = _sanitize_json(v, depth + 1)
        return out

    if isinstance(obj, list):
        if len(obj) > MAX_ARRAY_ITEMS:
            head = [_sanitize_json(x, depth + 1) for x in obj[:MAX_ARRAY_ITEMS]]
            return head + [{"_truncated": len(obj) - MAX_ARRAY_ITEMS}]
        return [_sanitize_json(x, depth + 1) for x in obj]

    if isinstance(obj, str):
        if re.match(r"^[A-Za-z0-9+/=]{200,}$", obj):
            return f"[base64, {len(obj)} chars]"
        if len(obj) > MAX_STRING_LEN:
            return obj[:MAX_STRING_LEN] + f"... ({len(obj)} chars)"
        return obj

    return obj


# Anthropic structured output: https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
# Supported models (GA): claude-opus-4-6, claude-sonnet-4-5, claude-opus-4-5, claude-haiku-4-5
# claude-sonnet-4-20250514 does NOT support structured output (Sonnet 4.0).
USE_STRUCTURED_OUTPUT = os.environ.get("HAR_USE_STRUCTURED_OUTPUT", "1").strip() == "1"
MODEL_STRUCTURED = os.environ.get("HAR_MODEL", "claude-sonnet-4-5")
MODEL_FALLBACK = os.environ.get("HAR_MODEL_FALLBACK", "claude-sonnet-4-20250514")

LEVEL1_OUTPUT_FORMAT = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "reasoning": {"type": "string", "description": "One or two sentences explaining why relevant or not"},
            "answer": {"type": "string", "enum": ["YES", "NO"], "description": "Final relevance verdict"},
        },
        "required": ["reasoning", "answer"],
        "additionalProperties": False,
    },
}

LEVEL2_OUTPUT_FORMAT = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "route_type": {"type": "string"},
            "method_name": {"type": "string"},
            "parameters": {"type": "string"},
            "response_structure": {"type": "string"},
            "documentation_notes": {"type": "string"},
            "other": {"type": "string"},
        },
        "required": ["route_type", "method_name", "parameters", "response_structure", "documentation_notes", "other"],
        "additionalProperties": False,
    },
}


def _parse_level1_answer_xml(reply: str) -> bool:
    """Extract YES/NO from XML-style Level 1 fallback response."""
    reply = reply.strip().upper()
    if "<ANSWER>" in reply:
        idx = reply.find("<ANSWER>") + 8
        end = reply.find("</ANSWER>", idx)
        if end > idx:
            return reply[idx:end].strip()[:3] == "YES"
    for line in reply.split("\n")[::-1]:
        if "ANSWER:" in line.upper():
            return "YES" in line.upper().split("ANSWER:")[-1].split()
        if line.strip() in ("YES", "NO"):
            return line.strip() == "YES"
    return reply.startswith("YES")


def _level2_json_to_markdown(obj: dict) -> str:
    """Convert Level 2 JSON response to readable markdown for findings."""
    out = []
    for key in ("route_type", "method_name", "parameters", "response_structure", "documentation_notes", "other"):
        val = obj.get(key, "")
        if val:
            title = key.replace("_", " ").title()
            out.append(f"**{title}**\n{val}\n")
    return "\n".join(out) if out else json.dumps(obj)


def _level2_xml_to_markdown(text: str) -> str:
    """Convert Level 2 XML fallback response to markdown."""
    out = []
    for tag in ("route_type", "method_name", "parameters", "response_structure", "documentation_notes", "other"):
        pat = re.compile(rf"<{tag}>([\s\S]*?)</{tag}>", re.IGNORECASE)
        m = pat.search(text)
        if m:
            content = m.group(1).strip()
            title = tag.replace("_", " ").title()
            out.append(f"**{title}**\n{content}\n")
    return "\n".join(out) if out else text


async def level1_relevance(client, payload: dict, logger: PromptLogger | None) -> bool:
    """Quick relevance check. Returns True if request is worth deep analysis."""
    prompt = f"""You are classifying HTTP requests from a HAR capture of sobranie.mk (North Macedonian Parliament).

## Request to classify
- URL: {payload['url']}
- Method: {payload['method']} | Status: {payload['status']}
- Request body: {payload['req'] or '(none)'}
- Response MIME: {payload['res_mime']}
- Response snippet: {payload['res_snip'] or '(none)'}

## Relevance criteria
RELEVANT (YES): sobranie.mk API (MakePostRequest, .asmx, JSON-RPC, SOAP), document/PDF/media URLs (sp.sobranie.mk), new routes, parliament data fetches.
NOT RELEVANT (NO): static assets (JS/CSS/images/fonts), analytics, tracking, CDNs, favicons.

Provide reasoning, then your answer (YES or NO)."""

    meta = {
        "level": "level1",
        "url": payload.get("url", "")[:200],
        "index": payload.get("n"),
        "estimated_input_tokens": approx_tokens(prompt),
        "timestamp": datetime.now().isoformat(),
    }
    stem = ""
    if logger:
        stem = logger.save_prompt("level1", prompt, meta)

    try:
        if USE_STRUCTURED_OUTPUT:
            msg = await client.messages.create(
                model=MODEL_STRUCTURED,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
                output_config={"format": LEVEL1_OUTPUT_FORMAT},
            )
            raw = msg.content[0].text.strip()
            obj = json.loads(raw)
            result = obj.get("answer", "NO") == "YES"
        else:
            msg = await client.messages.create(
                model=MODEL_FALLBACK,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt + '\n\nRespond with: <reasoning>...</reasoning><answer>YES</answer> or <answer>NO</answer>'}],
            )
            raw = msg.content[0].text.strip()
            result = _parse_level1_answer_xml(raw)

        if logger and stem:
            logger.save_response(stem, raw, {"relevant": result, "url": payload.get("url", "")[:200]})
        return result
    except Exception as e:
        if logger and stem:
            logger.save_response(stem, f"Error: {e}", {"relevant": False, "url": payload.get("url", "")[:200], "error": str(e)})
        raise


async def level2_analyze(client, entry: dict, index: int, logger: PromptLogger | None) -> str:
    """Deep analysis: extract full details, write structured notes."""
    req = entry.get("request", {})
    res = entry.get("response", {})
    url = req.get("url", "")
    method = req.get("method", "")
    status = res.get("status", 0)

    post_text = extract_post_data(entry)
    res_body, mime = extract_response_body(entry)

    req_body_sanitized = sanitize_body(post_text, MAX_LEVEL2_BODY)
    res_body_sanitized = sanitize_body(res_body, MAX_LEVEL2_BODY) if res_body else "(empty)"

    parsed = urlparse(url)
    path = parsed.path or url

    payload = f"""Analyze this HTTP request from a sobranie.mk HAR capture. Document everything useful for API discovery.

## Request
- URL: {url}
- Method: {method}
- Path: {path}
- Query: {parsed.query or '(none)'}

## Request body (sanitized)
```
{req_body_sanitized or '(none)'}
```

## Response
- Status: {status}
- Content-Type: {mime}

## Response body (sanitized)
```
{res_body_sanitized}
```

Fill each field: route_type, method_name, parameters, response_structure, documentation_notes, other. Be thorough."""

    level2_xml_prompt = payload + '''

Respond with:
<route_type>...</route_type>
<method_name>...</method_name>
<parameters>...</parameters>
<response_structure>...</response_structure>
<documentation_notes>...</documentation_notes>
<other>...</other>'''

    meta = {
        "level": "level2",
        "url": url[:200],
        "index": index,
        "method": method,
        "status": status,
        "req_body_len": len(req_body_sanitized or ""),
        "res_body_len": len(res_body_sanitized or ""),
        "estimated_input_tokens": approx_tokens(payload),
        "timestamp": datetime.now().isoformat(),
    }
    stem = ""
    if logger:
        stem = logger.save_prompt("level2", payload, meta)

    try:
        if USE_STRUCTURED_OUTPUT:
            msg = await client.messages.create(
                model=MODEL_STRUCTURED,
                max_tokens=2500,
                messages=[{"role": "user", "content": payload}],
                output_config={"format": LEVEL2_OUTPUT_FORMAT},
            )
            raw = msg.content[0].text.strip()
            obj = json.loads(raw)
            out = _level2_json_to_markdown(obj)
        else:
            msg = await client.messages.create(
                model=MODEL_FALLBACK,
                max_tokens=2500,
                messages=[{"role": "user", "content": level2_xml_prompt}],
            )
            raw = msg.content[0].text.strip()
            out = _level2_xml_to_markdown(raw)

        if logger and stem:
            logger.save_response(stem, raw, {"url": url[:200], "index": index})
        return out
    except Exception as e:
        if logger and stem:
            logger.save_response(stem, f"Error: {e}", {"url": url[:200], "index": index, "error": str(e)})
        raise


def load_har(path: Path) -> list[dict]:
    """Load HAR and return entries. Supports standard log.entries structure."""
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    if isinstance(data, dict):
        entries = data.get("log", {}).get("entries", data.get("entries", []))
    else:
        entries = []
    return entries if isinstance(entries, list) else []


def prefilter_skip(url: str) -> bool:
    """Return True if URL should be skipped before Level 1 (obvious static/tracking)."""
    ul = url.lower()
    return any(p in ul for p in SKIP_URL_PATTERNS)


def main():
    root = project_root()
    limit = int(os.environ.get("HAR_ANALYZE_LIMIT", "0")) or None

    dry_run = os.environ.get("HAR_DRY_RUN", "").strip() == "1"
    if not dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    paths = []
    for a in sys.argv[1:]:
        p = Path(a)
        if not p.exists():
            print(f"File not found: {p}", file=sys.stderr)
            continue
        if p.is_file() and (p.suffix == ".har" or "har" in p.name.lower()):
            paths.append(p)
        elif p.is_dir():
            paths.extend(p.glob("**/*.har"))

    if not paths:
        print("Usage: python scripts/analyze_har.py path/to/capture.har [path/to/other.har ...]", file=sys.stderr)
        print("  Or:  python scripts/analyze_har.py path/to/dir/  (processes all .har in dir)", file=sys.stderr)
        sys.exit(1)

    all_entries: list[tuple[Path, int, dict]] = []
    for p in paths:
        entries = load_har(p)
        for i, e in enumerate(entries):
            all_entries.append((p, i, e))

    total = len(all_entries)
    print(f"Loaded {total} entries from {len(paths)} HAR file(s)")

    # Pre-filter: skip obvious static/tracking (no LLM). Set HAR_SKIP_PREFILTER=1 to disable.
    skip_prefilter = os.environ.get("HAR_SKIP_PREFILTER", "").strip() == "1"
    if skip_prefilter:
        prefiltered = all_entries
    else:
        prefiltered = [(p, i, e) for p, i, e in all_entries if not prefilter_skip(e.get("request", {}).get("url", ""))]
    prefiltered_count = len(prefiltered)
    skipped_pre = total - prefiltered_count
    if skipped_pre:
        print(f"Pre-filter skipped {skipped_pre} obvious static/tracking URLs")
    all_entries = prefiltered

    if limit:
        all_entries = all_entries[:limit]
        print(f"Limited to {limit} entries")

    level1_count = len(all_entries)
    relevant: list[tuple[Path, int, dict, str]] = []

    if dry_run:
        print("\nDry run: skipping LLM calls. Would process", level1_count, "entries.")
        for i, (p, idx, e) in enumerate(all_entries[:5]):
            pl = build_level1_payload(e, i)
            print(f"  {i+1}. {pl['url'][:70]}... | {pl['method']} {pl['status']} | methodName={pl.get('req','')[:60]}")
        if level1_count > 5:
            print(f"  ... and {level1_count - 5} more")
        return

    from anthropic import AsyncAnthropic

    log_dir = root / LOG_DIR / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger = PromptLogger(log_dir)
    print(f"\nLogging prompts/responses to {log_dir}")

    async def run_async():
        client = AsyncAnthropic()
        sem = asyncio.Semaphore(CONCURRENCY)

        async def level1_with_sem(i: int, har_path: Path, idx: int, entry: dict):
            pl = build_level1_payload(entry, i)
            pl["n"] = i + 1
            async with sem:
                try:
                    is_rel = await level1_relevance(client, pl, logger)
                    return (har_path, idx, entry, pl.get("url", ""), is_rel, None)
                except Exception as e:
                    return (har_path, idx, entry, pl.get("url", ""), False, str(e))

        # --- Level 1: relevance filter (async batch) ---
        print("\nLevel 1: relevance filter (async batch) ...")
        tasks = [level1_with_sem(i, p, idx, e) for i, (p, idx, e) in enumerate(all_entries)]
        results = []
        for i in range(0, len(tasks), CONCURRENCY):
            batch = tasks[i : i + CONCURRENCY]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            for r in batch_results:
                if isinstance(r, Exception):
                    print(f"  Error: {r}")
                else:
                    results.append(r)
            done = min(i + len(batch), len(tasks))
            count = sum(1 for r in results if not isinstance(r, Exception) and r[4])
            if done % 20 == 0 or done == len(tasks):
                print(f"  Checked {done}/{len(tasks)}, relevant so far: {count}")
            if i + CONCURRENCY < len(tasks):
                await asyncio.sleep(BATCH_DELAY)

        relevant_list = [(p, idx, e, url) for p, idx, e, url, is_rel, err in results if is_rel and err is None]

        print(f"\nLevel 1 complete: {len(relevant_list)} relevant of {len(all_entries)}")

        # --- Level 2: deep analysis (async batch) ---
        print("\nLevel 2: deep analysis of relevant requests (async batch)...")
        analyses_list = []

        async def level2_with_sem(har_path: Path, idx: int, entry: dict, url: str):
            async with sem:
                try:
                    analysis = await level2_analyze(client, entry, idx, logger)
                    return {"har": str(har_path), "index": idx, "url": url, "analysis": analysis}
                except Exception as e:
                    return {"har": str(har_path), "index": idx, "url": url, "analysis": f"Error: {e}"}

        tasks2 = [level2_with_sem(p, idx, e, url) for p, idx, e, url in relevant_list]
        for i in range(0, len(tasks2), CONCURRENCY):
            batch = tasks2[i : i + CONCURRENCY]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            for j, r in enumerate(batch_results):
                if isinstance(r, Exception):
                    idx = i + j
                    if idx < len(relevant_list):
                        p, idx, e, url = relevant_list[idx]
                        analyses_list.append({"har": str(p), "index": idx, "url": url, "analysis": f"Error: {r}"})
                else:
                    analyses_list.append(r)
            print(f"  [{min(i + len(batch), len(tasks2))}/{len(tasks2)}] done")
            if i + CONCURRENCY < len(tasks2):
                await asyncio.sleep(BATCH_DELAY)

        return analyses_list

    analyses = asyncio.run(run_async())
    logger.save_index(run_summary={
        "total_entries": total,
        "prefiltered": prefiltered_count,
        "level1_count": level1_count,
        "relevant_count": len(analyses),
        "concurrency": CONCURRENCY,
        "batch_delay": BATCH_DELAY,
    })

    # --- Write output ---
    lines = [
        "# HAR Analysis Findings",
        "",
        "Two-level LLM analysis of HAR capture(s). Pre-filter skipped static/tracking; Level 1 filtered for relevance; Level 2 produced structured notes.",
        "",
        f"- **Total entries in HAR**: {total}",
        f"- **Passed to Level 1**: {level1_count}" + (f" (limited from {prefiltered_count})" if limit else ""),
        f"- **Relevant (Level 1)**: {len(relevant)}",
        f"- **Analyzed (Level 2)**: {len(analyses)}",
        "",
        "---",
        "",
    ]

    for a in analyses:
        lines.append(f"## Entry from {Path(a['har']).name} (index {a['index']})")
        lines.append("")
        lines.append(f"**URL**: `{a['url']}`")
        lines.append("")
        lines.append(a["analysis"])
        lines.append("")
        lines.append("---")
        lines.append("")

    out_path = root / OUTPUT
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
