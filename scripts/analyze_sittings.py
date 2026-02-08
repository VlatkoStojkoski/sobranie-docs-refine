#!/usr/bin/env python3
"""
Analyze GetSittingDetails responses across 50+ sittings using Claude.
Fetches sittings from various dates, analyzes each against documented schema,
and produces an aggregate findings document.
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from anthropic import Anthropic

# Config
API_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"  # current assembly
SITTINGS_PER_PAGE = 20
NUM_PAGES = 6  # 6 * 20 = 120 candidates, we pick 50 for date diversity
TARGET_COUNT = 50
DELAY_BETWEEN_REQUESTS = 0.5  # seconds
ANALYSIS_OUTPUT = "API_ANALYSIS_FINDINGS.md"


def project_root() -> Path:
    return Path(__file__).parent.parent


def fetch_sittings(pages: int) -> list[dict]:
    """Fetch sittings from multiple pages for date/type diversity."""
    all_items = []
    for page in range(1, pages + 1):
        payload = {
            "methodName": "GetAllSittings",
            "Page": page,
            "Rows": SITTINGS_PER_PAGE,
            "LanguageId": 1,
            "TypeId": None,
            "CommitteeId": None,
            "StatusId": None,
            "DateFrom": None,
            "DateTo": None,
            "SessionId": None,
            "Number": None,
            "StructureId": STRUCTURE_ID,
        }
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("Items", [])
        all_items.extend(items)
        time.sleep(DELAY_BETWEEN_REQUESTS)
    return all_items


def select_candidates(items: list[dict], count: int) -> list[dict]:
    """Select diverse candidates: spread across dates, mix of plenary/committee, different statuses."""
    if len(items) <= count:
        return items
    # Sort by SittingDate (desc = newest first) then interleave
    sorted_items = sorted(items, key=lambda x: x.get("SittingDate", ""), reverse=True)
    step = max(1, len(sorted_items) // count)
    selected = []
    seen_ids = set()
    for i in range(0, len(sorted_items), step):
        if len(selected) >= count:
            break
        for j in range(i, min(i + step, len(sorted_items))):
            item = sorted_items[j]
            sid = item.get("Id")
            if sid and sid not in seen_ids:
                seen_ids.add(sid)
                selected.append(item)
                if len(selected) >= count:
                    break
    return selected[:count]


def fetch_sitting_details(sitting_id: str) -> dict | None:
    """Fetch GetSittingDetails for a sitting."""
    payload = {
        "MethodName": "GetSittingDetails",
        "SittingId": sitting_id,
        "LanguageId": 1,
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  Error fetching {sitting_id}: {e}", file=sys.stderr)
        return None


def truncate_for_analysis(data: dict, max_array_items: int = 3) -> dict:
    """Truncate large arrays so Claude sees structure without huge payloads."""
    if not isinstance(data, dict):
        return data
    out = {}
    for k, v in data.items():
        if isinstance(v, list):
            if len(v) > max_array_items:
                remainder = len(v) - max_array_items
                out[k] = [
                    truncate_for_analysis(item, max_array_items) if isinstance(item, dict) else item
                    for item in v[:max_array_items]
                ] + [{"_truncated": remainder}]
            else:
                out[k] = [
                    truncate_for_analysis(item, max_array_items) if isinstance(item, dict) else item
                    for item in v
                ]
        elif isinstance(v, dict):
            out[k] = truncate_for_analysis(v, max_array_items)
        else:
            out[k] = v
    return out


def analyze_sitting_with_claude(
    client: Anthropic,
    sitting_summary: dict,
    sitting_meta: dict,
    api_docs: str,
) -> str:
    """Ask Claude to analyze a single sitting response against the documented schema."""
    prompt = f"""You are analyzing a GetSittingDetails API response against our documented schema.

## Documented schema (from API.md)
{api_docs}

## Sitting metadata (from GetAllSittings)
- Id: {sitting_meta.get('Id')}
- Number: {sitting_meta.get('Number')}
- TypeId: {sitting_meta.get('TypeId')} ({sitting_meta.get('TypeTitle', '')})
- StatusId: {sitting_meta.get('StatusId')} ({sitting_meta.get('StatusTitle', '')})

## Actual response (truncated for large arrays)
```json
{json.dumps(sitting_summary, ensure_ascii=False, indent=2)}
```

Analyze this response. For each finding, output exactly one line in this format:
- [DEVIATION] <description> — if something violates or differs from the documented schema
- [UNDOCUMENTED] <field/path> — if you see a field we haven't documented
- [NEW_ENUM] <ID type> = <value> (<label if present>) — if you see an enum/ID value we don't have
- [INTERESTING] <observation> — something noteworthy (pattern, edge case, cool detail)

If nothing notable, output: [OK] No issues found.

Be concise. One line per finding. Output only the findings, no preamble."""

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text
    return text.strip()


def main():
    root = project_root()
    api_md_path = root / "API.md"

    if not api_md_path.exists():
        print(f"API.md not found at {api_md_path}", file=sys.stderr)
        sys.exit(1)

    api_docs = api_md_path.read_text(encoding="utf-8")

    # Extract just GetSittingDetails section for context
    start = api_docs.find("### `GetSittingDetails`")
    end = api_docs.find("### `GetAllStructuresForFilter`")
    if start == -1 or end == -1:
        sitting_docs = api_docs
    else:
        sitting_docs = api_docs[start:end]

    limit = int(os.environ.get("ANALYZE_LIMIT", "0")) or None  # e.g. ANALYZE_LIMIT=5 for testing

    print("Fetching sittings...")
    items = fetch_sittings(NUM_PAGES)
    print(f"  Got {len(items)} sittings")

    candidates = select_candidates(items, TARGET_COUNT)
    print(f"  Selected {len(candidates)} candidates")

    if limit:
        candidates = candidates[:limit]
        print(f"  Limited to {limit} (ANALYZE_LIMIT)")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set ANTHROPIC_API_KEY to run Claude analysis", file=sys.stderr)
        sys.exit(1)

    client = Anthropic()

    per_sitting = []
    for i, cand in enumerate(candidates):
        sid = cand.get("Id")
        print(f"[{i+1}/{len(candidates)}] Fetching sitting {sid}...")
        details = fetch_sitting_details(sid)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if not details:
            continue

        truncated = truncate_for_analysis(details, max_array_items=2)
        findings = analyze_sitting_with_claude(client, truncated, cand, sitting_docs)
        per_sitting.append({
            "sitting_id": sid,
            "number": cand.get("Number"),
            "type_id": cand.get("TypeId"),
            "status_id": cand.get("StatusId"),
            "findings": findings,
        })
        first_line = findings.split("\n")[0][:80] if findings else "n/a"
        print(f"  -> {first_line}")

    # Build output by appending individual results
    lines = [
        "# GetSittingDetails Schema Analysis",
        "",
        f"Analyzed {len(per_sitting)} sittings. Individual findings below.",
        "",
        "---",
        "",
    ]
    for f in per_sitting:
        lines.append(f"## Sitting {f['sitting_id']}")
        lines.append(f"Number: {f['number']} | TypeId: {f['type_id']} | StatusId: {f['status_id']}")
        lines.append("")
        lines.append(f["findings"])
        lines.append("")
        lines.append("---")
        lines.append("")

    out_path = root / ANALYSIS_OUTPUT
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
