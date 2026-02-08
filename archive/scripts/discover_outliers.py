#!/usr/bin/env python3
"""
Discover schema violations and outliers across the Sobranie API.
No Claude required. Does programmatic validation and exhaustive enum collection.

1. SCHEMA VALIDATOR: Fetches sittings + materials, validates responses against
   documented types, enums, nullability. Reports violations.

2. ENUM COLLECTOR: Collects ALL unique ID values seen (DocumentTypeId, StatusId,
   etc.) across many responses. Compares to documented enums, reports gaps.

3. OUTLIER DETECTOR: Finds statistical anomalies - unusual null rates, empty
   arrays, field lengths, duplicate IDs.
"""

import json
import os
import re
import time
from collections import defaultdict
from pathlib import Path

import requests

# Config
API_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
SITTINGS_TO_FETCH = 80
MATERIALS_TO_FETCH = 80
DELAY_BETWEEN_REQUESTS = 0.4
OUTPUT = "API_OUTLIER_FINDINGS.md"

# Documented enums from API.md $defs (kept in sync with discover_outliers findings)
DOCUMENTED_ENUMS = {
    "SittingStatusId": {1, 2, 3, 4, 5, 6},
    "AgendaItemTypeId": {1, 2},
    "DocumentTypeId": {19, 20, 40, 42, 43, 44, 51, 52, 53, 57, 59, 64, 71, 72},  # sitting docs
    "MaterialStatusId": {0, 6, 9, 10, 11, 12, 24, 64},
    "MaterialDocumentTypeId": {1, 7, 8, 9, 16, 17, 30, 45, 52, 65, 68},
    "MaterialTypeId": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37},
    "ProcedureTypeId": {1, 2, 3},
    "ProposerTypeId": {1, 2, 4},
}

UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)
ASP_DATE_PATTERN = re.compile(r"^/Date\(\d+\)/$")


def project_root() -> Path:
    return Path(__file__).parent.parent


def api_post(payload: dict) -> dict | list:
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def collect_sitting_ids() -> list[str]:
    """Collect diverse sitting IDs."""
    ids = []
    payload = {
        "methodName": "GetAllSittings",
        "Page": 1,
        "Rows": 50,
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
    for page in range(1, 4):
        payload["Page"] = page
        data = api_post(payload)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        items = data.get("Items") or []
        for it in items:
            if it.get("Id"):
                ids.append(it["Id"])
    return ids[:SITTINGS_TO_FETCH]


def collect_material_ids() -> list[str]:
    """Collect diverse material IDs."""
    ids = []
    payload = {
        "MethodName": "GetAllMaterialsForPublicPortal",
        "LanguageId": 1,
        "ItemsPerPage": 20,
        "CurrentPage": 1,
        "SearchText": "",
        "AuthorText": "",
        "ActNumber": "",
        "StatusGroupId": None,
        "MaterialTypeId": None,
        "ResponsibleCommitteeId": None,
        "CoReportingCommittees": None,
        "OpinionCommittees": None,
        "RegistrationNumber": None,
        "EUCompatible": None,
        "DateFrom": None,
        "DateTo": None,
        "ProcedureTypeId": None,
        "InitiatorTypeId": None,
        "StructureId": STRUCTURE_ID,
    }
    for page in range(1, 6):
        payload["CurrentPage"] = page
        data = api_post(payload)
        time.sleep(DELAY_BETWEEN_REQUESTS)
        items = data.get("Items") or []
        for it in items:
            if it.get("Id"):
                ids.append(it["Id"])
    return ids[:MATERIALS_TO_FETCH]


def extract_enums_and_validate(
    obj,
    path: str,
    violations: list[dict],
    enums_seen: dict[str, set],
    null_counts: dict[str, int],
    total_counts: dict[str, int],
) -> None:
    """Recursively traverse response, collect enum values, validate types."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            extract_enums_and_validate(v, p, violations, enums_seen, null_counts, total_counts)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            extract_enums_and_validate(item, f"{path}[{i}]", violations, enums_seen, null_counts, total_counts)
    else:
        # Leaf value
        if path.endswith("Id") or "TypeId" in path or "StatusId" in path:
            key = path.split(".")[-1].rstrip("]")
            if "[" in key:
                key = key.split("[")[0]
            enum_name = None
            if key == "DocumentTypeId":
                enum_name = "MaterialDocumentTypeId" if "GetMaterialDetails" in path else "DocumentTypeId"
            elif key == "SittingTypeId":
                enum_name = "AgendaItemTypeId"
            elif key in ("StatusGroupId", "ObjectStatusId"):
                enum_name = "MaterialStatusId"
            elif key in DOCUMENTED_ENUMS:
                enum_name = key
            elif any(key.endswith(k) for k in DOCUMENTED_ENUMS):
                enum_name = next((k for k in DOCUMENTED_ENUMS if key.endswith(k)), None)
            if enum_name and isinstance(obj, (int, float)):
                val = int(obj)
                enums_seen.setdefault(enum_name, set()).add(val)
                doc_set = DOCUMENTED_ENUMS.get(enum_name)
                if doc_set and val not in doc_set:
                    violations.append({"path": path, "type": "ENUM_UNDOCUMENTED", "value": val, "expected": sorted(doc_set)})
        if obj is None:
            null_counts[path] = null_counts.get(path, 0) + 1
        total_counts[path] = total_counts.get(path, 0) + 1


def validate_uuid(val, path: str, violations: list[dict]) -> None:
    if val is None:
        return
    if isinstance(val, str) and not UUID_PATTERN.match(val) and val != "00000000-0000-0000-0000-000000000000":
        violations.append({"path": path, "type": "UUID_INVALID", "value": val[:50]})


def validate_sitting(d: dict, violations: list[dict], enums_seen: dict, null_counts: dict, total_counts: dict) -> None:
    extract_enums_and_validate(d, "GetSittingDetails", violations, enums_seen, null_counts, total_counts)
    for doc in d.get("Documents") or []:
        validate_uuid(doc.get("Id"), "Documents[].Id", violations)
    for item in d.get("Agenda", {}).get("Items") or []:
        validate_uuid(item.get("Id"), "Agenda.Items[].Id", violations)


def validate_material(d: dict, violations: list[dict], enums_seen: dict, null_counts: dict, total_counts: dict) -> None:
    extract_enums_and_validate(d, "GetMaterialDetails", violations, enums_seen, null_counts, total_counts)
    for arr_name in ["Documents", "Committees", "Sittings", "FirstReadingSittings", "SecondReadingSittings", "ThirdReadingSittings"]:
        for i, item in enumerate(d.get(arr_name) or []):
            if isinstance(item, dict) and item.get("Id"):
                validate_uuid(item["Id"], f"{arr_name}[].Id", violations)
    for auth in d.get("Authors") or []:
        validate_uuid(auth.get("Id"), "Authors[].Id", violations)


def find_empty_arrays(d: dict, path: str, empties: list[tuple[str, str]]) -> None:
    if isinstance(d, dict):
        for k, v in d.items():
            p = f"{path}.{k}" if path else k
            if isinstance(v, list):
                if len(v) == 0:
                    empties.append((p, "empty"))
                else:
                    find_empty_arrays(v, p, empties)
            elif isinstance(v, dict):
                find_empty_arrays(v, p, empties)
    elif isinstance(d, list):
        for i, item in enumerate(d):
            find_empty_arrays(item, f"{path}[{i}]", empties)


def find_duplicate_ids(d: dict, path: str, id_path: str, seen: set, duplicates: list[str]) -> None:
    if isinstance(d, dict):
        ids = d.get("Id") if "Id" in d else None
        if ids is not None and id_path in path:
            if ids in seen:
                duplicates.append(f"{path}: duplicate Id={ids}")
            seen.add(ids)
        for k, v in d.items():
            find_duplicate_ids(v, f"{path}.{k}", id_path, set(), duplicates)
    elif isinstance(d, list):
        local_seen = set()
        for i, item in enumerate(d):
            if isinstance(item, dict) and "Id" in item:
                vid = item["Id"]
                if vid in local_seen:
                    duplicates.append(f"{path}[{i}] Id={vid}")
                local_seen.add(vid)
            find_duplicate_ids(item, f"{path}[{i}]", id_path, set(), duplicates)


def main():
    root = project_root()
    limit_s = os.environ.get("OUTLIER_SITTINGS_LIMIT", "0")
    limit_m = os.environ.get("OUTLIER_MATERIALS_LIMIT", "0")
    max_sittings = int(limit_s) or SITTINGS_TO_FETCH
    max_materials = int(limit_m) or MATERIALS_TO_FETCH

    violations: list[dict] = []
    enums_seen: dict[str, set] = defaultdict(set)
    null_counts: dict[str, int] = defaultdict(int)
    total_counts: dict[str, int] = defaultdict(int)
    empty_array_paths: dict[str, int] = defaultdict(int)
    all_proposer_types: set[str] = set()
    all_termination_statuses: set[str] = set()

    # Filter coverage: which filter values return 0 results?
    print("Checking filter coverage (GetAllMaterialsForPublicPortal)...")
    filter_coverage: list[tuple[str, int, int]] = []
    for status_id in DOCUMENTED_ENUMS["MaterialStatusId"]:
        data = api_post({
            "MethodName": "GetAllMaterialsForPublicPortal",
            "LanguageId": 1, "ItemsPerPage": 5, "CurrentPage": 1,
            "SearchText": "", "AuthorText": "", "ActNumber": "",
            "StatusGroupId": status_id, "MaterialTypeId": None, "ResponsibleCommitteeId": None,
            "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None,
            "EUCompatible": None, "DateFrom": None, "DateTo": None,
            "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID,
        })
        time.sleep(DELAY_BETWEEN_REQUESTS)
        total = data.get("TotalItems", 0)
        filter_coverage.append((f"StatusGroupId={status_id}", total, 5))
    for type_id in [1, 2, 6, 8, 24, 28]:  # subset
        data = api_post({
            "MethodName": "GetAllMaterialsForPublicPortal",
            "LanguageId": 1, "ItemsPerPage": 5, "CurrentPage": 1,
            "SearchText": "", "AuthorText": "", "ActNumber": "",
            "StatusGroupId": None, "MaterialTypeId": type_id, "ResponsibleCommitteeId": None,
            "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None,
            "EUCompatible": None, "DateFrom": None, "DateTo": None,
            "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID,
        })
        time.sleep(DELAY_BETWEEN_REQUESTS)
        total = data.get("TotalItems", 0)
        filter_coverage.append((f"MaterialTypeId={type_id}", total, 5))

    print("Collecting sitting IDs...")
    sitting_ids = collect_sitting_ids()
    print(f"  Got {len(sitting_ids)} sitting IDs")

    print("Collecting material IDs...")
    material_ids = collect_material_ids()
    print(f"  Got {len(material_ids)} material IDs")

    print("Fetching GetSittingDetails...")
    for i, sid in enumerate(sitting_ids[:max_sittings]):
        try:
            data = api_post({"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1})
            time.sleep(DELAY_BETWEEN_REQUESTS)
            validate_sitting(data, violations, enums_seen, null_counts, total_counts)
        except Exception as e:
            print(f"  Error {sid}: {e}")
        if (i + 1) % 20 == 0:
            print(f"  ... {i+1}/{max_sittings}")

    print("Fetching GetMaterialDetails...")
    for i, mid in enumerate(material_ids[:max_materials]):
        try:
            data = api_post({
                "methodName": "GetMaterialDetails",
                "MaterialId": mid,
                "LanguageId": 1,
                "AmendmentsPage": 1,
                "AmendmentsRows": 5,
            })
            time.sleep(DELAY_BETWEEN_REQUESTS)
            validate_material(data, violations, enums_seen, null_counts, total_counts)
            if data.get("ProposerTypeTitle"):
                all_proposer_types.add(data["ProposerTypeTitle"])
            if data.get("TerminationStatusTitle"):
                all_termination_statuses.add(data["TerminationStatusTitle"])
            empties = []
            find_empty_arrays(data, "GetMaterialDetails", empties)
            for p, _ in empties:
                empty_array_paths[p] += 1
        except Exception as e:
            print(f"  Error {mid}: {e}")
        if (i + 1) % 20 == 0:
            print(f"  ... {i+1}/{max_materials}")

    # Deduplicate violations by path+value
    seen_v = set()
    unique_violations = []
    for v in violations:
        key = (v["path"], v.get("value"))
        if key not in seen_v:
            seen_v.add(key)
            unique_violations.append(v)

    # Build report
    lines = [
        "# API Outlier & Schema Violation Report",
        "",
        f"Analyzed {min(len(sitting_ids), max_sittings)} sittings and {min(len(material_ids), max_materials)} materials.",
        "No Claude used — programmatic validation only.",
        "",
        "---",
        "",
        "## 1. Undocumented Enum Values",
        "",
    ]

    for enum_name, doc_set in DOCUMENTED_ENUMS.items():
        seen = enums_seen.get(enum_name, set())
        missing_in_docs = seen - doc_set
        if missing_in_docs:
            lines.append(f"### {enum_name}")
            lines.append(f"- **Seen in API:** {sorted(seen)}")
            lines.append(f"- **Documented:** {sorted(doc_set)}")
            lines.append(f"- **Gap (seen but not documented):** {sorted(missing_in_docs)}")
            lines.append("")

    lines.append("## 2. Schema Violations")
    lines.append("")
    if unique_violations:
        for v in unique_violations[:50]:
            lines.append(f"- `{v['path']}`: {v['type']} — value={v.get('value')}")
        if len(unique_violations) > 50:
            lines.append(f"- ... and {len(unique_violations) - 50} more")
    else:
        lines.append("No violations found.")
    lines.append("")

    lines.append("## 3. ProposerTypeTitle Values (from GetMaterialDetails)")
    lines.append("")
    lines.append("Documented GetProposerTypes: Пратеник, Влада..., Група избирачи.")
    lines.append("")
    for pt in sorted(all_proposer_types):
        lines.append(f"- `{pt}`")
    lines.append("")

    lines.append("## 4. TerminationStatusTitle Values (closed materials)")
    lines.append("")
    for ts in sorted(all_termination_statuses):
        lines.append(f"- `{ts}`")
    lines.append("")

    lines.append("## 5. Frequently Empty Arrays")
    lines.append("")
    sorted_empties = sorted(empty_array_paths.items(), key=lambda x: -x[1])[:15]
    for path, count in sorted_empties:
        lines.append(f"- `{path}`: empty in {count} materials")
    lines.append("")

    lines.append("## 6. Filter Coverage (materials with filter)")
    lines.append("")
    for fname, total, _ in filter_coverage:
        status = "✓" if total > 0 else "✗ 0 results"
        lines.append(f"- `{fname}`: {total} items — {status}")
    lines.append("")

    lines.append("## 7. Null Rates (high-null fields)")
    lines.append("")
    null_rates = []
    for path, n in null_counts.items():
        t = total_counts.get(path, 0)
        if t > 10 and n > 0:
            null_rates.append((path, n, t, round(100 * n / t, 1)))
    null_rates.sort(key=lambda x: -x[3])
    for path, n, t, pct in null_rates[:20]:
        lines.append(f"- `{path}`: {n}/{t} ({pct}%) null")
    lines.append("")

    out_path = root / OUTPUT
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
