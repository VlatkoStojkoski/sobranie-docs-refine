#!/usr/bin/env python3
"""
Analyze GetSittingDetails across sittings sampled from all filter dimensions.
Fetches equal amounts of TypeId 1 (plenary) and TypeId 2 (committee), spread across
StatusId 1-6, and across different committees. Uses Claude to analyze against API.md.
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
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
ROWS_PER_FETCH = 15
PER_FILTER_COMBO = 4  # sittings to take per (TypeId, StatusId) combo
PER_COMMITTEE = 2  # sittings to take per committee (TypeId 2 only)
TARGET_COUNT = 50
DELAY_BETWEEN_REQUESTS = 0.5
ANALYSIS_OUTPUT = "API_ANALYSIS_FINDINGS_DIVERSE.md"


def project_root() -> Path:
    return Path(__file__).parent.parent


def fetch_sittings(
    type_id: int | None,
    status_id: int | None,
    committee_id: str | None,
    page: int = 1,
    rows: int = ROWS_PER_FETCH,
) -> list[dict]:
    """Fetch sittings with given filters."""
    payload = {
        "methodName": "GetAllSittings",
        "Page": page,
        "Rows": rows,
        "LanguageId": 1,
        "TypeId": type_id,
        "CommitteeId": committee_id,
        "StatusId": status_id,
        "DateFrom": None,
        "DateTo": None,
        "SessionId": None,
        "Number": None,
        "StructureId": STRUCTURE_ID,
    }
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json().get("Items") or []


def fetch_committees() -> list[dict]:
    """Fetch committees from GetAllCommitteesForFilter."""
    payload = {
        "methodName": "GetAllCommitteesForFilter",
        "languageId": 1,
        "structureId": STRUCTURE_ID,
    }
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def collect_diverse_candidates() -> list[dict]:
    """Collect sittings across TypeId, StatusId, and CommitteeId filters."""
    seen_ids: set[str] = set()
    candidates: list[dict] = []

    # (TypeId, StatusId) combos: 2 type ids × 6 status ids = 12 combos
    for type_id in [1, 2]:
        for status_id in [1, 2, 3, 4, 5, 6]:
            items = fetch_sittings(type_id=type_id, status_id=status_id, committee_id=None)
            time.sleep(DELAY_BETWEEN_REQUESTS)
            items = items or []
            for item in items[:PER_FILTER_COMBO]:
                sid = item.get("Id")
                if sid and sid not in seen_ids:
                    seen_ids.add(sid)
                    candidates.append(item)
                    if len(candidates) >= TARGET_COUNT:
                        return candidates[:TARGET_COUNT]

    # Committee filter: TypeId 2 + CommitteeId
    committees = fetch_committees()
    time.sleep(DELAY_BETWEEN_REQUESTS)
    for committee in (committees or [])[:8]:  # up to 8 committees
        cid = committee.get("Id")
        if not cid:
            continue
        items = fetch_sittings(type_id=2, status_id=None, committee_id=cid)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        items = items or []
        for item in items[:PER_COMMITTEE]:
            sid = item.get("Id")
            if sid and sid not in seen_ids:
                seen_ids.add(sid)
                candidates.append(item)
                if len(candidates) >= TARGET_COUNT:
                    return candidates[:TARGET_COUNT]

    return candidates[:TARGET_COUNT]


def fetch_sitting_details(sitting_id: str) -> dict | None:
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
    prompt = f"""You are analyzing a GetSittingDetails API response against our documented schema.

## Documented schema (from API.md)
{api_docs}

## Sitting metadata (from GetAllSittings)
- Id: {sitting_meta.get('Id')}
- Number: {sitting_meta.get('Number')}
- TypeId: {sitting_meta.get('TypeId')} ({sitting_meta.get('TypeTitle', '')})
- StatusId: {sitting_meta.get('StatusId')} ({sitting_meta.get('StatusTitle', '')})
- CommitteeTitle: {sitting_meta.get('CommitteeTitle')}

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
    return msg.content[0].text.strip()


def main():
    root = project_root()
    api_md_path = root / "API.md"

    if not api_md_path.exists():
        print(f"API.md not found at {api_md_path}", file=sys.stderr)
        sys.exit(1)

    api_docs = api_md_path.read_text(encoding="utf-8")
    start = api_docs.find("### `GetSittingDetails`")
    end = api_docs.find("### `GetAllStructuresForFilter`")
    sitting_docs = api_docs[start:end] if start != -1 and end != -1 else api_docs

    limit = int(os.environ.get("ANALYZE_LIMIT", "0")) or None

    print("Fetching sittings across TypeId, StatusId, CommitteeId...")
    candidates = collect_diverse_candidates()
    print(f"  Collected {len(candidates)} candidates")

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
        print(f"[{i+1}/{len(candidates)}] {sid} (TypeId={cand.get('TypeId')}, StatusId={cand.get('StatusId')})...")
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
            "committee_title": cand.get("CommitteeTitle"),
            "findings": findings,
        })
        first_line = findings.split("\n")[0][:80] if findings else "n/a"
        print(f"  -> {first_line}")

    lines = [
        "# GetSittingDetails Schema Analysis (Diverse Filters)",
        "",
        f"Analyzed {len(per_sitting)} sittings sampled across TypeId, StatusId, CommitteeId.",
        "",
        "---",
        "",
    ]
    for f in per_sitting:
        ctx = f"Number: {f['number']} | TypeId: {f['type_id']} | StatusId: {f['status_id']}"
        if f.get("committee_title"):
            ctx += f" | Committee: {f['committee_title']}"
        lines.append(f"## Sitting {f['sitting_id']}")
        lines.append(ctx)
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
