#!/usr/bin/env python3
"""
Exploratory API analysis: systematically covers all documentable endpoints with
diverse parameters. Sends responses to Claude for open-ended exploration.
Designed to enrich every part of our API documentation.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from anthropic import Anthropic

# Config
API_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
CALENDAR_URL = "https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
DELAY = 0.5
TRUNCATE_ARRAYS = 4
OUTPUT = "API_EXPLORATION_FINDINGS.md"


def project_root() -> Path:
    return Path(__file__).parent.parent


def truncate(obj, max_items: int = TRUNCATE_ARRAYS):
    """Truncate arrays; shorten long strings (e.g. base64)."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k == "UserImg" and isinstance(v, str) and len(v) > 80:
                out[k] = v[:80] + f"... (truncated, total {len(v)} chars)"
            else:
                out[k] = truncate(v, max_items)
        return out
    if isinstance(obj, list):
        if len(obj) > max_items:
            return [truncate(x, max_items) for x in obj[:max_items]] + [{"_truncated": len(obj) - max_items}]
        return [truncate(x, max_items) for x in obj]
    return obj


def api_post(payload: dict):
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def calendar_post(month: int, year: int):
    resp = requests.post(
        CALENDAR_URL,
        json={"model": {"Language": 1, "Month": month, "Year": year}},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def explore(client: Anthropic, endpoint: str, meta: str, response, response_type: str = "detail") -> str:
    """Open-ended exploration with context about endpoint type."""
    type_hint = {
        "detail": "This is a detail/entity endpoint with nested structure.",
        "list": "This is a list endpoint (TotalItems + Items or array). Watch for pagination, empty results, structure consistency.",
        "catalog": "This is a catalog/reference endpoint. Watch for ID completeness, title consistency, structure.",
    }.get(response_type, "")

    payload = json.dumps(response, ensure_ascii=False, indent=2)
    if len(payload) > 12000:
        payload = payload[:12000] + "\n... (response truncated for length)"

    prompt = f"""You are exploring a real API response from the North Macedonian Parliament (sobranie.mk).

## Endpoint: {endpoint}
{type_hint}

## Request context / params:
{meta}

## Response (arrays truncated, _truncated=N means N more items):
```json
{payload}
```

Explore freely. Surface anything that would improve our API documentation: undocumented fields, new enum values, null vs empty patterns, edge cases, inconsistencies. Be specific (field paths, example values). Use bullet points. If nothing noteworthy, say so briefly."""

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def run_tasks(client: Anthropic, tasks: list[tuple], limit: int | None) -> list[dict]:
    """Execute exploration tasks and collect findings."""
    results = []
    for i, (endpoint, fetch_fn, meta_fn, response_type) in enumerate(tasks):
        if limit and i >= limit:
            break
        label = f"{endpoint} ({i+1}/{len(tasks)})"
        print(f"  {label}...")
        try:
            data = fetch_fn()
            time.sleep(DELAY)
            meta = meta_fn(data) if meta_fn else ""
            truncated = truncate(data)
            findings = explore(client, endpoint, meta, truncated, response_type)
            results.append({"endpoint": endpoint, "meta": meta, "findings": findings})
        except Exception as e:
            print(f"    Error: {e}")
            results.append({"endpoint": endpoint, "meta": str(e), "findings": f"Error: {e}"})
    return results


def main():
    root = project_root()
    limit = int(os.environ.get("EXPLORE_LIMIT", "0")) or None

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = Anthropic()
    tasks = []

    # --- Fetch reference data for parameterized tasks ---
    print("Fetching reference data...")
    structures = api_post({"methodName": "GetAllStructuresForFilter", "languageId": 1})
    time.sleep(DELAY)
    committees = api_post({"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID})
    time.sleep(DELAY)
    parties = api_post({"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)

    structure_ids = [s["Id"] for s in (structures or [])[:3]]
    committee_ids = [c["Id"] for c in (committees or [])[:3]]
    party_ids = [p["Id"] for p in (parties or [])[:2]]

    # --- 1. Detail: GetSittingDetails (diverse TypeId, StatusId, CommitteeId) ---
    sitting_ids = []
    for type_id in [1, 2]:
        for status_id in [1, 2, 3, 5]:
            data = api_post({
                "methodName": "GetAllSittings",
                "Page": 1, "Rows": 8, "LanguageId": 1,
                "TypeId": type_id, "CommitteeId": None, "StatusId": status_id,
                "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None,
                "StructureId": STRUCTURE_ID,
            })
            time.sleep(DELAY)
            for it in (data.get("Items") or [])[:2]:
                if it.get("Id"):
                    sitting_ids.append(it)
                    if len(sitting_ids) >= 10:
                        break
            if len(sitting_ids) >= 10:
                break
        if len(sitting_ids) >= 10:
            break
    for cid in committee_ids[:2]:
        if len(sitting_ids) >= 12:
            break
        data = api_post({
            "methodName": "GetAllSittings",
            "Page": 1, "Rows": 5, "LanguageId": 1,
            "TypeId": 2, "CommitteeId": cid, "StatusId": None,
            "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None,
            "StructureId": STRUCTURE_ID,
        })
        time.sleep(DELAY)
        for it in (data.get("Items") or [])[:1]:
            if it.get("Id") and it["Id"] not in {s["Id"] for s in sitting_ids}:
                sitting_ids.append(it)

    for s in sitting_ids:
        sid = s["Id"]
        tasks.append((
            "GetSittingDetails",
            lambda sid=sid: api_post({"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1}),
            lambda d, s=s: f"Number={s.get('Number')} TypeId={s.get('TypeId')} StatusId={s.get('StatusId')} CommitteeTitle={s.get('CommitteeTitle')}",
            "detail",
        ))

    # --- 2. Detail: GetMaterialDetails (diverse status, type, proposer) ---
    material_ids = []
    for status_id in [6, 9, 10, 12]:
        data = api_post({
            "MethodName": "GetAllMaterialsForPublicPortal",
            "LanguageId": 1, "ItemsPerPage": 10, "CurrentPage": 1,
            "SearchText": "", "AuthorText": "", "ActNumber": "",
            "StatusGroupId": status_id, "MaterialTypeId": None, "ResponsibleCommitteeId": None,
            "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None,
            "EUCompatible": None, "DateFrom": None, "DateTo": None,
            "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID,
        })
        time.sleep(DELAY)
        for it in (data.get("Items") or [])[:3]:
            if it.get("Id"):
                material_ids.append(it)
                if len(material_ids) >= 10:
                    break
        if len(material_ids) >= 10:
            break
    for type_id in [1, 2, 8, 28]:
        if len(material_ids) >= 12:
            break
        data = api_post({
            "MethodName": "GetAllMaterialsForPublicPortal",
            "LanguageId": 1, "ItemsPerPage": 10, "CurrentPage": 1,
            "SearchText": "", "AuthorText": "", "ActNumber": "",
            "StatusGroupId": None, "MaterialTypeId": type_id, "ResponsibleCommitteeId": None,
            "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None,
            "EUCompatible": None, "DateFrom": None, "DateTo": None,
            "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID,
        })
        time.sleep(DELAY)
        for it in (data.get("Items") or [])[:2]:
            if it.get("Id") and it["Id"] not in {m["Id"] for m in material_ids}:
                material_ids.append(it)

    for m in material_ids:
        mid = m["Id"]
        meta_str = f"TypeTitle={m.get('TypeTitle')} StatusGroupTitle={m.get('StatusGroupTitle')} ProposerTypeTitle={m.get('ProposerTypeTitle')}"
        tasks.append((
            "GetMaterialDetails",
            lambda mid=mid: api_post({"methodName": "GetMaterialDetails", "MaterialId": mid, "LanguageId": 1, "AmendmentsPage": 1, "AmendmentsRows": 5}),
            lambda d, ms=meta_str: ms,
            "detail",
        ))

    # --- 3. List: GetAllSittings (filter combos, pagination edge) ---
    for type_id, status_id, label in [(1, None, "plenary only"), (2, None, "committee only"), (2, 3, "committee completed"), (None, 1, "all scheduled")]:
        tasks.append((
            "GetAllSittings",
            lambda t=type_id, s=status_id: api_post({
                "methodName": "GetAllSittings", "Page": 1, "Rows": 15, "LanguageId": 1,
                "TypeId": t, "CommitteeId": None, "StatusId": s,
                "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None,
                "StructureId": STRUCTURE_ID,
            }),
            lambda d, l=label: f"Params: {l}",
            "list",
        ))

    # --- 4. List: GetAllMaterialsForPublicPortal ---
    for status_id, type_id, label in [(6, None, "StatusGroupId=6"), (12, None, "StatusGroupId=12 closed"), (None, 1, "MaterialTypeId=1 laws"), (None, 28, "MaterialTypeId=28 reports")]:
        tasks.append((
            "GetAllMaterialsForPublicPortal",
            lambda s=status_id, t=type_id: api_post({
                "MethodName": "GetAllMaterialsForPublicPortal",
                "LanguageId": 1, "ItemsPerPage": 12, "CurrentPage": 1,
                "SearchText": "", "AuthorText": "", "ActNumber": "",
                "StatusGroupId": s, "MaterialTypeId": t, "ResponsibleCommitteeId": None,
                "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None,
                "EUCompatible": None, "DateFrom": None, "DateTo": None,
                "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID,
            }),
            lambda d, l=label: f"Params: {l}",
            "list",
        ))

    # --- 5. GetMonthlyAgenda (different months) ---
    now = datetime.now()
    for month, year, label in [(now.month, now.year, "current month"), (now.month - 1 or 12, now.year if now.month > 1 else now.year - 1, "previous month")]:
        tasks.append((
            "GetMonthlyAgenda",
            lambda m=month, y=year: api_post({"methodName": "GetMonthlyAgenda", "LanguageId": 1, "Month": m, "Year": y}),
            lambda d, l=label: f"Params: {l}",
            "list",
        ))

    # --- 6. GetParliamentMPsNoImage (pagination, filters, StructureId) ---
    for (page, rows, pid, gid, search), label in [
        ((1, 20, None, None, ""), "page 1, rows=20"),
        ((2, 20, None, None, ""), "page 2"),
        ((1, 5, party_ids[0] if party_ids else None, None, ""), "politicalPartyId filter"),
        ((1, 20, None, 1, ""), "genderId=1"),
        ((1, 20, None, None, "а"), "searchText='а'"),
    ]:
        tasks.append((
            "GetParliamentMPsNoImage",
            lambda p=page, r=rows, pid=pid, gid=gid, s=search: api_post({
                "methodName": "GetParliamentMPsNoImage",
                "languageId": 1, "genderId": gid, "ageFrom": None, "ageTo": None,
                "politicalPartyId": pid, "searchText": s or None, "page": p, "rows": r,
                "StructureId": STRUCTURE_ID, "coalition": "", "constituency": "",
            }),
            lambda d, l=label: f"Params: {l}",
            "list",
        ))

    # Different StructureId (older assembly) — only if we have a distinct one
    alt_structure = next((sid for sid in structure_ids if sid != STRUCTURE_ID), None)
    if alt_structure:
        tasks.append((
            "GetParliamentMPsNoImage",
            lambda aid=alt_structure: api_post({
                "methodName": "GetParliamentMPsNoImage",
                "languageId": 1, "genderId": None, "ageFrom": None, "ageTo": None,
                "politicalPartyId": None, "searchText": None, "page": 1, "rows": 10,
                "StructureId": aid, "coalition": "", "constituency": "",
            }),
            lambda d, aid=alt_structure: f"Params: StructureId={aid[:8]}... (different assembly)",
            "list",
        ))

    # --- 7. GetCustomEventsCalendar (different URL) ---
    for month, year in [(now.month, now.year), (now.month - 2 or 10, now.year if now.month > 2 else now.year - 1)]:
        tasks.append((
            "GetCustomEventsCalendar",
            lambda m=month, y=year: calendar_post(m, y),
            lambda d, m=month, y=year: f"Params: Month={m} Year={y}",
            "list",
        ))

    # --- 8. Catalog batch (all reference endpoints in one) ---
    def fetch_catalogs():
        out = {}
        for name, payload in [
            ("GetAllGenders", {"methodName": "GetAllGenders", "languageId": 1}),
            ("GetAllStructuresForFilter", {"methodName": "GetAllStructuresForFilter", "languageId": 1}),
            ("GetAllCommitteesForFilter", {"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID}),
            ("GetAllMaterialStatusesForFilter", {"methodName": "GetAllMaterialStatusesForFilter", "languageId": 1}),
            ("GetAllMaterialTypesForFilter", {"methodName": "GetAllMaterialTypesForFilter", "languageId": 1}),
            ("GetAllSittingStatuses", {"methodName": "GetAllSittingStatuses", "LanguageId": 1}),
            ("GetAllPoliticalParties", {"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID}),
            ("GetAllProcedureTypes", {"methodName": "GetAllProcedureTypes", "languageId": 1}),
            ("GetProposerTypes", {"methodName": "GetProposerTypes", "languageId": 1}),
        ]:
            out[name] = api_post(payload)
            time.sleep(DELAY)
        return out

    tasks.append((
        "Catalogs (batch)",
        fetch_catalogs,
        lambda d: "All reference/catalog endpoints combined",
        "catalog",
    ))

    # --- Execute ---
    total = len(tasks)
    print(f"\nRunning {total} exploration tasks (limit={limit or 'none'})...")

    if limit:
        tasks = tasks[:limit]

    results = run_tasks(client, tasks, None)

    # --- Write output ---
    lines = [
        "# API Exploration Findings",
        "",
        "Open-ended LLM exploration across all documentable endpoints.",
        f"Completed {len(results)} tasks.",
        "",
        "---",
        "",
    ]

    for r in results:
        lines.append(f"## {r['endpoint']}")
        lines.append("")
        lines.append(f"*{r['meta']}*")
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
