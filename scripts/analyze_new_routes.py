#!/usr/bin/env python3
"""
Analyze new API routes (questions, councils, committees, parties, groups, MPs clubs,
voting results) against documented schema in API.md.

Follows the same pattern as analyze_sittings.py and analyze_materials_diverse.py:
- Fetches real responses with diverse filters where applicable
- Uses Claude to compare against documented schema
- Outputs [DEVIATION], [UNDOCUMENTED], [NEW_ENUM], [INTERESTING] findings

Routes covered (from API.md, added after initial exploration):
- Catalogs: GetAllQuestionStatuses, GetAllInstitutionsForFilter, GetAllApplicationTypes,
  GetAllCouncils, GetAllParliamentaryGroups, GetAllMPsClubsByStructure
- List: GetAllQuestions (diverse StatusId)
- Details: GetQuestionDetails, GetCouncilDetails, GetCommitteeDetails,
  GetPoliticalPartyDetails, GetParliamentaryGroupDetails, GetMPsClubDetails,
  GetVotingResultsForSitting
"""

import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from anthropic import Anthropic

# Config
API_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
DELAY = 0.5
TARGET_PER_LIST = 5
TARGET_PER_DETAIL = 4
MAX_ARRAY_ITEMS = 3
OUTPUT = "API_ANALYSIS_FINDINGS_NEW_ROUTES.md"


def project_root() -> Path:
    return Path(__file__).parent.parent


def extract_api_section(api_docs: str, endpoint: str) -> str:
    """Extract the ### `Endpoint` section from API.md until the next ###."""
    escaped = re.escape(endpoint)
    pattern = rf"### `{escaped}`[^\n]*\n(.*?)(?=### `|\Z)"
    match = re.search(pattern, api_docs, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def api_post(payload: dict) -> dict | list:
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def truncate_for_analysis(data, max_items: int = MAX_ARRAY_ITEMS):
    """Truncate large arrays so Claude sees structure without huge payloads."""
    if isinstance(data, dict):
        return {k: truncate_for_analysis(v, max_items) for k, v in data.items()}
    if isinstance(data, list):
        if len(data) > max_items:
            return [truncate_for_analysis(x, max_items) for x in data[:max_items]] + [
                {"_truncated": len(data) - max_items}
            ]
        return [truncate_for_analysis(x, max_items) for x in data]
    return data


def analyze_with_claude(
    client: Anthropic,
    endpoint: str,
    meta: str,
    response_data,
    api_docs: str,
    response_type: str = "detail",
) -> str:
    """Ask Claude to analyze response against documented schema."""
    type_hint = {
        "catalog": "This is a catalog/reference endpoint (array of Id/Title or similar).",
        "list": "This is a list endpoint (TotalItems + Items or array).",
        "detail": "This is a detail/entity endpoint with nested structure.",
    }.get(response_type, "")

    payload_str = json.dumps(response_data, ensure_ascii=False, indent=2)
    if len(payload_str) > 14000:
        payload_str = payload_str[:14000] + "\n... (truncated for length)"

    prompt = f"""You are analyzing an API response against our documented schema.

## Endpoint: {endpoint}
{type_hint}

## Documented schema (from API.md)
{api_docs}

## Request context
{meta}

## Actual response (arrays truncated, _truncated=N means N more items)
```json
{payload_str}
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


def run_task(client, endpoint, fetch_fn, meta_fn, api_docs, response_type) -> dict | None:
    """Fetch, analyze, return result or None on error."""
    try:
        data = fetch_fn()
        time.sleep(DELAY)
        meta = meta_fn(data) if meta_fn else ""
        truncated = truncate_for_analysis(data)
        findings = analyze_with_claude(client, endpoint, meta, truncated, api_docs, response_type)
        return {"endpoint": endpoint, "meta": meta, "findings": findings, "status": "ok"}
    except Exception as e:
        return {"endpoint": endpoint, "meta": "", "findings": f"Error: {e}", "status": "error"}


def main():
    root = project_root()
    api_md_path = root / "API.md"
    if not api_md_path.exists():
        print(f"API.md not found at {api_md_path}", file=sys.stderr)
        sys.exit(1)

    api_docs_full = api_md_path.read_text(encoding="utf-8")
    limit = int(os.environ.get("ANALYZE_LIMIT", "0")) or None

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY to run Claude analysis", file=sys.stderr)
        sys.exit(1)

    client = Anthropic()

    # --- Fetch reference data ---
    print("Fetching reference data...")
    questions_resp = api_post({
        "methodName": "GetAllQuestions",
        "LanguageId": 1, "CurrentPage": 1, "Page": 1, "Rows": 15,
        "SearchText": "", "RegistrationNumber": "", "StatusId": None,
        "From": "", "To": "", "CommitteeId": None, "DateFrom": None, "DateTo": None,
        "StructureId": STRUCTURE_ID,
    })
    time.sleep(DELAY)

    councils = api_post({"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    committees = api_post({"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID})
    time.sleep(DELAY)
    parties = api_post({"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    groups = api_post({"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    mps_clubs = api_post({"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)

    question_ids = [q["Id"] for q in (questions_resp.get("Items") or [])[:TARGET_PER_DETAIL] if q.get("Id")]
    council_ids = [c["Id"] for c in (councils or [])[:3]]
    committee_ids = [c["Id"] for c in (committees or [])[:3]]
    party_ids = [p["Id"] for p in (parties or [])[:3]]
    group_ids = [g["Id"] for g in (groups or [])[:3]]
    club_ids = [c["Id"] for c in (mps_clubs or [])[:3]] if isinstance(mps_clubs, list) else []

    # Voting IDs from sitting
    sitting_ids = [s["Id"] for s in (api_post({
        "methodName": "GetAllSittings", "Page": 1, "Rows": 5, "LanguageId": 1,
        "TypeId": 1, "CommitteeId": None, "StatusId": 3,
        "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None,
        "StructureId": STRUCTURE_ID,
    }) or {}).get("Items") or []]
    time.sleep(DELAY)

    voting_def_id = None
    for sid in sitting_ids:
        details = api_post({"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1})
        time.sleep(DELAY)
        for ch in (details.get("Agenda") or {}).get("children") or []:
            for vd in ch.get("VotingDefinitions") or []:
                if vd.get("Id"):
                    voting_def_id = vd["Id"]
                    break
            if voting_def_id:
                break
        if voting_def_id:
            break

    # --- Build tasks ---
    tasks = []

    # Catalogs (fetch once)
    for endpoint, payload in [
        ("GetAllQuestionStatuses", {"methodName": "GetAllQuestionStatuses", "languageId": 1}),
        ("GetAllInstitutionsForFilter", {"methodName": "GetAllInstitutionsForFilter", "languageId": 1}),
        ("GetAllApplicationTypes", {"methodName": "GetAllApplicationTypes", "languageId": 1}),
        ("GetAllCouncils", {"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID}),
        ("GetAllParliamentaryGroups", {"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID}),
        ("GetAllMPsClubsByStructure", {"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID}),
    ]:
        tasks.append((
            endpoint,
            lambda p=payload: api_post(p),
            lambda d: f"items={len(d) if isinstance(d, list) else len(d.get('Items', []))}",
            "catalog",
        ))

    # List: GetAllQuestions with diverse StatusId
    for status_id in [None, 17, 19]:
        payload = {
            "methodName": "GetAllQuestions",
            "LanguageId": 1, "CurrentPage": 1, "Page": 1, "Rows": 8,
            "SearchText": "", "RegistrationNumber": "", "StatusId": status_id,
            "From": "", "To": "", "CommitteeId": None, "DateFrom": None, "DateTo": None,
            "StructureId": STRUCTURE_ID,
        }
        tasks.append((
            "GetAllQuestions",
            lambda p=payload: api_post(p),
            lambda d, s=status_id: f"StatusId={s} | TotalItems={d.get('TotalItems', 'N/A')}",
            "list",
        ))

    # Detail endpoints
    for qid in question_ids[:2]:
        tasks.append((
            "GetQuestionDetails",
            lambda q=qid: api_post({"methodName": "GetQuestionDetails", "QuestionId": q, "LanguageId": 1}),
            lambda d, q=qid: f"QuestionId={q[:8]}...",
            "detail",
        ))

    for cid in council_ids[:2]:
        tasks.append((
            "GetCouncilDetails",
            lambda c=cid: api_post({"methodName": "GetCouncilDetails", "committeeId": c, "languageId": 1}),
            lambda d, c=cid: f"committeeId={c[:8]}...",
            "detail",
        ))

    for cid in committee_ids[:2]:
        tasks.append((
            "GetCommitteeDetails",
            lambda c=cid: api_post({"methodName": "GetCommitteeDetails", "committeeId": c, "languageId": 1}),
            lambda d, c=cid: f"committeeId={c[:8]}...",
            "detail",
        ))

    for pid in party_ids[:2]:
        tasks.append((
            "GetPoliticalPartyDetails",
            lambda p=pid: api_post({"methodName": "GetPoliticalPartyDetails", "politicalPartyId": p, "LanguageId": 1}),
            lambda d, p=pid: f"politicalPartyId={p[:8]}...",
            "detail",
        ))

    for gid in group_ids[:2]:
        tasks.append((
            "GetParliamentaryGroupDetails",
            lambda g=gid: api_post({"methodName": "GetParliamentaryGroupDetails", "parliamentaryGroupId": g, "LanguageId": 1}),
            lambda d, g=gid: f"parliamentaryGroupId={g[:8]}...",
            "detail",
        ))

    for cid in club_ids[:2]:
        tasks.append((
            "GetMPsClubDetails",
            lambda c=cid: api_post({"methodName": "GetMPsClubDetails", "mpsClubId": c, "LanguageId": 1}),
            lambda d, c=cid: f"mpsClubId={c[:8]}...",
            "detail",
        ))

    if voting_def_id and sitting_ids:
        sid = sitting_ids[0]
        tasks.append((
            "GetVotingResultsForSitting",
            lambda: api_post({
                "methodName": "GetVotingResultsForSitting",
                "votingDefinitionId": voting_def_id,
                "sittingId": sid,
                "languageId": 1,
            }),
            lambda d: f"votingDefinitionId={voting_def_id[:8]}... sittingId={sid[:8]}...",
            "detail",
        ))

    if limit:
        tasks = tasks[:limit]
        print(f"Limited to {limit} tasks (ANALYZE_LIMIT)")

    # --- Run tasks ---
    results = []
    for i, (endpoint, fetch_fn, meta_fn, response_type) in enumerate(tasks):
        print(f"[{i+1}/{len(tasks)}] {endpoint}...")
        api_section = extract_api_section(api_docs_full, endpoint)
        if not api_section:
            print(f"  Warning: no API.md section for {endpoint}", file=sys.stderr)
        result = run_task(client, endpoint, fetch_fn, meta_fn, api_section or "(no docs)", response_type)
        if result:
            results.append(result)
            first_line = result["findings"].split("\n")[0][:70] if result["findings"] else "n/a"
            print(f"  -> {first_line}")

    # --- Write output ---
    lines = [
        "# New Routes Schema Analysis",
        "",
        f"Analyzed {len(results)} responses across new API routes (questions, councils, committees, parties, groups, MPs clubs, voting).",
        "",
        "---",
        "",
    ]
    for r in results:
        lines.append(f"## {r['endpoint']}")
        if r.get("meta"):
            lines.append(r["meta"])
            lines.append("")
        lines.append(r["findings"])
        lines.append("")
        lines.append("---")
        lines.append("")

    out_path = root / OUTPUT
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
