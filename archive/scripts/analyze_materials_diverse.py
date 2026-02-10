#!/usr/bin/env python3
"""
Analyze GetMaterialDetails across materials sampled from all filter dimensions.
Fetches materials via GetAllMaterialsForPublicPortal with diverse filters
(StatusGroupId, MaterialTypeId, ProcedureTypeId, InitiatorTypeId, ResponsibleCommitteeId),
then fetches GetMaterialDetails for each. Uses Claude to analyze against API.md.
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
PER_FILTER_COMBO = 3
PER_COMMITTEE = 2
TARGET_COUNT = 50
DELAY_BETWEEN_REQUESTS = 0.5
ANALYSIS_OUTPUT = "API_ANALYSIS_FINDINGS_MATERIALS.md"

# Filter values from API docs
STATUS_GROUP_IDS = [6, 9, 10, 11, 12, 24, 64]  # MaterialStatusId
MATERIAL_TYPE_IDS = [1, 2, 6, 8, 21, 24, 28]  # subset for diversity
PROCEDURE_TYPE_IDS = [1, 2, 3]
INITIATOR_TYPE_IDS = [1, 2, 4]  # ProposerTypeId


def project_root() -> Path:
    return Path(__file__).parent.parent


def fetch_materials(
    status_group_id: int | None = None,
    material_type_id: int | None = None,
    procedure_type_id: int | None = None,
    initiator_type_id: int | None = None,
    responsible_committee_id: str | None = None,
    page: int = 1,
    rows: int = ROWS_PER_FETCH,
) -> list[dict]:
    """Fetch materials from GetAllMaterialsForPublicPortal with given filters."""
    payload = {
        "MethodName": "GetAllMaterialsForPublicPortal",
        "LanguageId": 1,
        "ItemsPerPage": rows,
        "CurrentPage": page,
        "SearchText": "",
        "AuthorText": "",
        "ActNumber": "",
        "StatusGroupId": status_group_id,
        "MaterialTypeId": material_type_id,
        "ResponsibleCommitteeId": responsible_committee_id,
        "CoReportingCommittees": None,
        "OpinionCommittees": None,
        "RegistrationNumber": None,
        "EUCompatible": None,
        "DateFrom": None,
        "DateTo": None,
        "ProcedureTypeId": procedure_type_id,
        "InitiatorTypeId": initiator_type_id,
        "StructureId": STRUCTURE_ID,
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("Items")
        return items if items else []
    except Exception as e:
        print(f"  Error fetching materials: {e}", file=sys.stderr)
        return []


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
    """Collect materials across StatusGroupId, MaterialTypeId, ProcedureTypeId, InitiatorTypeId, ResponsibleCommitteeId."""
    seen_ids: set[str] = set()
    candidates: list[dict] = []

    # StatusGroupId combos
    for status_id in STATUS_GROUP_IDS:
        items = fetch_materials(status_group_id=status_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        for item in items[:PER_FILTER_COMBO]:
            mid = item.get("Id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                item["_filter"] = f"StatusGroupId={status_id}"
                candidates.append(item)
                if len(candidates) >= TARGET_COUNT:
                    return candidates[:TARGET_COUNT]

    # MaterialTypeId combos
    for type_id in MATERIAL_TYPE_IDS:
        items = fetch_materials(material_type_id=type_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        for item in items[:PER_FILTER_COMBO]:
            mid = item.get("Id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                item["_filter"] = f"MaterialTypeId={type_id}"
                candidates.append(item)
                if len(candidates) >= TARGET_COUNT:
                    return candidates[:TARGET_COUNT]

    # ProcedureTypeId combos
    for proc_id in PROCEDURE_TYPE_IDS:
        items = fetch_materials(procedure_type_id=proc_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        for item in items[:PER_FILTER_COMBO]:
            mid = item.get("Id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                item["_filter"] = f"ProcedureTypeId={proc_id}"
                candidates.append(item)
                if len(candidates) >= TARGET_COUNT:
                    return candidates[:TARGET_COUNT]

    # InitiatorTypeId combos
    for init_id in INITIATOR_TYPE_IDS:
        items = fetch_materials(initiator_type_id=init_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        for item in items[:PER_FILTER_COMBO]:
            mid = item.get("Id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                item["_filter"] = f"InitiatorTypeId={init_id}"
                candidates.append(item)
                if len(candidates) >= TARGET_COUNT:
                    return candidates[:TARGET_COUNT]

    # Committee filter
    committees = fetch_committees()
    time.sleep(DELAY_BETWEEN_REQUESTS)
    for committee in (committees or [])[:8]:
        cid = committee.get("Id")
        if not cid:
            continue
        items = fetch_materials(responsible_committee_id=cid)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        for item in items[:PER_COMMITTEE]:
            mid = item.get("Id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                item["_filter"] = f"ResponsibleCommitteeId={cid[:8]}..."
                candidates.append(item)
                if len(candidates) >= TARGET_COUNT:
                    return candidates[:TARGET_COUNT]

    return candidates[:TARGET_COUNT]


def fetch_material_details(material_id: str) -> dict | None:
    """Fetch GetMaterialDetails for a material."""
    payload = {
        "methodName": "GetMaterialDetails",
        "MaterialId": material_id,
        "LanguageId": 1,
        "AmendmentsPage": 1,
        "AmendmentsRows": 5,
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  Error fetching {material_id}: {e}", file=sys.stderr)
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


def analyze_material_with_claude(
    client: Anthropic,
    material_summary: dict,
    material_meta: dict,
    api_docs: str,
) -> str:
    prompt = f"""You are analyzing a GetMaterialDetails API response against our documented schema.

## Documented schema (from API.md)
{api_docs}

## Material metadata (from GetAllMaterialsForPublicPortal)
- Id: {material_meta.get('Id')}
- Title: {material_meta.get('Title', '')[:80]}...
- TypeTitle: {material_meta.get('TypeTitle')}
- StatusGroupTitle: {material_meta.get('StatusGroupTitle')}
- ProposerTypeTitle: {material_meta.get('ProposerTypeTitle')}

## Actual response (truncated for large arrays)
```json
{json.dumps(material_summary, ensure_ascii=False, indent=2)}
```

Analyze this response. For each finding, output exactly one line in this format:
- [DEVIATION] <description> — if something violates or differs from the documented schema
- [UNDOCUMENTED] <field/path> — if you see a field we haven't documented
- [NEW_ENUM] <ID type> = <value> (<label if present>) — if you see an enum/ID value we don't have (e.g. DocumentTypeId for material docs)
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
    start = api_docs.find("### `GetMaterialDetails`")
    end = api_docs.find("### `GetMonthlyAgenda`")
    material_docs = api_docs[start:end] if start != -1 and end != -1 else api_docs

    limit = int(os.environ.get("ANALYZE_LIMIT", "0")) or None

    print("Fetching materials across StatusGroupId, MaterialTypeId, ProcedureTypeId, InitiatorTypeId, ResponsibleCommitteeId...")
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
    per_material = []

    for i, cand in enumerate(candidates):
        mid = cand.get("Id")
        filter_info = cand.pop("_filter", "unknown")
        print(f"[{i+1}/{len(candidates)}] {mid} ({filter_info})...")
        details = fetch_material_details(mid)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if not details:
            continue

        truncated = truncate_for_analysis(details, max_array_items=2)
        findings = analyze_material_with_claude(client, truncated, cand, material_docs)
        per_material.append({
            "material_id": mid,
            "title": cand.get("Title", "")[:60],
            "type_title": cand.get("TypeTitle"),
            "status_group_title": cand.get("StatusGroupTitle"),
            "proposer_type_title": cand.get("ProposerTypeTitle"),
            "filter": filter_info,
            "findings": findings,
        })
        first_line = findings.split("\n")[0][:80] if findings else "n/a"
        print(f"  -> {first_line}")

    lines = [
        "# GetMaterialDetails Schema Analysis (Diverse Filters)",
        "",
        f"Analyzed {len(per_material)} materials sampled across StatusGroupId, MaterialTypeId, ProcedureTypeId, InitiatorTypeId, ResponsibleCommitteeId.",
        "",
        "---",
        "",
    ]
    for f in per_material:
        ctx = f"Type: {f['type_title']} | Status: {f['status_group_title']} | Proposer: {f['proposer_type_title']} | Filter: {f['filter']}"
        lines.append(f"## Material {f['material_id']}")
        lines.append(f"Title: {f['title']}...")
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
