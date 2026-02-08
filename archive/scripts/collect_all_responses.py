#!/usr/bin/env python3
"""
Collect raw responses from ALL API endpoints with diverse parameters.
Data-driven: no guessing. Output used by infer_schema.py for schema inference.

Output: collected_responses/YYYY-MM-DD_HH-MM-SS/
  - manifest.json (index of all calls)
  - {method_name}.json (per-method: request variants and response samples)

Run: python scripts/collect_all_responses.py
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests

API_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
CALENDAR_URL = "https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar"
LOAD_LANG_URL = "https://www.sobranie.mk/Infrastructure/LoadLanguage"
OFFICIAL_VISITS_URL = "https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
DELAY = 0.6
OUTPUT_DIR = "collected_responses"


def api_post(url: str, payload: dict, retries: int = 2):
    for attempt in range(retries + 1):
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            try:
                return resp.json()
            except Exception:
                return {"_raw": resp.text[:5000]}
        if resp.status_code == 500 and attempt < retries:
            time.sleep(DELAY * 2)
            continue
        return {"_error": f"HTTP {resp.status_code}", "_body": resp.text[:500]}


def truncate_for_storage(obj, max_array: int = 10, max_str: int = 2000):
    """Truncate large values to keep storage manageable while preserving structure."""
    if isinstance(obj, dict):
        return {k: truncate_for_storage(v, max_array, max_str) for k, v in obj.items()}
    if isinstance(obj, list):
        if len(obj) > max_array:
            kept = [truncate_for_storage(x, max_array, max_str) for x in obj[:max_array]]
            return kept + [{"_truncated": len(obj) - max_array}]
        return [truncate_for_storage(x, max_array, max_str) for x in obj]
    if isinstance(obj, str) and len(obj) > max_str:
        return obj[:max_str] + "...[truncated]"
    return obj


def main():
    root = Path(__file__).parent.parent
    out_dir = root / OUTPUT_DIR / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"timestamp": datetime.now().isoformat(), "calls": []}

    # --- 1. Fetch reference IDs ---
    print("Fetching reference data...")
    refs = {}

    def fetch(name: str, payload: dict, url=API_URL):
        data = api_post(url, payload)
        time.sleep(DELAY)
        refs[name] = data
        return data

    structures = fetch("structures", {"methodName": "GetAllStructuresForFilter", "languageId": 1})
    committees = fetch("committees", {"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID})
    parties = fetch("parties", {"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID})
    sittings = fetch("sittings", {"methodName": "GetAllSittings", "Page": 1, "Rows": 20, "LanguageId": 1, "TypeId": 1,
        "CommitteeId": None, "StatusId": 3, "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None,
        "StructureId": STRUCTURE_ID})
    questions = fetch("questions", {"methodName": "GetAllQuestions", "LanguageId": 1, "CurrentPage": 1, "Page": 1,
        "Rows": 15, "SearchText": "", "RegistrationNumber": "", "StatusId": None, "From": "", "To": "",
        "CommitteeId": None, "DateFrom": None, "DateTo": None, "StructureId": STRUCTURE_ID})
    materials = fetch("materials", {"MethodName": "GetAllMaterialsForPublicPortal", "LanguageId": 1, "ItemsPerPage": 10,
        "CurrentPage": 1, "SearchText": "", "AuthorText": "", "ActNumber": "", "StatusGroupId": None,
        "MaterialTypeId": 1, "ResponsibleCommitteeId": None, "CoReportingCommittees": None, "OpinionCommittees": None,
        "RegistrationNumber": None, "EUCompatible": None, "DateFrom": None, "DateTo": None,
        "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID})
    groups = fetch("groups", {"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID})
    mps_clubs = fetch("mps_clubs", {"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID})
    councils = fetch("councils", {"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID})
    mps = fetch("mps", {"methodName": "GetParliamentMPsNoImage", "languageId": 1, "genderId": None, "ageFrom": None,
        "ageTo": None, "politicalPartyId": None, "searchText": None, "page": 1, "rows": 5,
        "StructureId": STRUCTURE_ID, "coalition": "", "constituency": ""})

    sitting_ids = [s["Id"] for s in (sittings.get("Items") or [])[:10]] if isinstance(sittings, dict) else []
    committee_ids = [c["Id"] for c in (committees or [])[:5]] if isinstance(committees, list) else []
    party_ids = [p["Id"] for p in (parties or [])[:3]] if isinstance(parties, list) else []
    question_ids = [q["Id"] for q in (questions.get("Items") or [])[:5] if q.get("Id")] if isinstance(questions, dict) else []
    material_ids = [m["Id"] for m in (materials.get("Items") or [])[:5]] if isinstance(materials, dict) else []
    group_ids = [g["Id"] for g in (groups or [])[:3]] if isinstance(groups, list) else []
    club_ids = [c["Id"] for c in (mps_clubs or [])[:3]] if isinstance(mps_clubs, list) else []
    council_ids = [c["Id"] for c in (councils or [])[:2]] if isinstance(councils, list) else []
    mp_user_ids = [m.get("UserId") for m in (mps.get("MembersOfParliament") or [])[:2] if m.get("UserId")] if isinstance(mps, dict) else []

    voting_def_id, agenda_item_id = None, None
    for sid in sitting_ids[:5]:
        det = api_post(API_URL, {"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1})
        if isinstance(det, dict) and "_error" not in det:
            for ch in (det.get("Agenda") or {}).get("children") or []:
                for vd in ch.get("VotingDefinitions") or []:
                    if vd.get("Id"):
                        voting_def_id, agenda_item_id = vd["Id"], ch.get("Id") or ch.get("objectId")
                        break
            if voting_def_id:
                break
        time.sleep(DELAY)

    amendment_id = None
    for mid in material_ids[:3]:
        mat = api_post(API_URL, {"methodName": "GetMaterialDetails", "MaterialId": mid, "LanguageId": 1, "AmendmentsPage": 1, "AmendmentsRows": 5})
        if isinstance(mat, dict) and "_error" not in mat:
            items = (mat.get("Amendments") or {}).get("Items") or (mat.get("FirstReadingAmendments") or [])
            if items and items[0].get("Id"):
                amendment_id = items[0]["Id"]
                break
        time.sleep(DELAY)

    # --- 2. Define all endpoints with variants ---
    ENDPOINTS = [
        # Catalogs (single request each)
        ("GetAllGenders", [{"methodName": "GetAllGenders", "languageId": 1}]),
        ("GetAllStructuresForFilter", [{"methodName": "GetAllStructuresForFilter", "languageId": 1}]),
        ("GetAllCommitteesForFilter", [{"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID}]),
        ("GetAllMaterialStatusesForFilter", [{"methodName": "GetAllMaterialStatusesForFilter", "languageId": 1}]),
        ("GetAllMaterialTypesForFilter", [{"methodName": "GetAllMaterialTypesForFilter", "languageId": 1}]),
        ("GetAllSittingStatuses", [{"methodName": "GetAllSittingStatuses", "LanguageId": 1}]),
        ("GetAllQuestionStatuses", [{"methodName": "GetAllQuestionStatuses", "languageId": 1}]),
        ("GetAllInstitutionsForFilter", [{"methodName": "GetAllInstitutionsForFilter", "languageId": 1}]),
        ("GetAllProcedureTypes", [{"methodName": "GetAllProcedureTypes", "languageId": 1}]),
        ("GetProposerTypes", [{"methodName": "GetProposerTypes", "languageId": 1}]),
        ("GetAllApplicationTypes", [{"methodName": "GetAllApplicationTypes", "languageId": 1}]),
        # List endpoints with diversity
        ("GetAllPoliticalParties", [{"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID}]),
        ("GetAllCouncils", [{"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID}]),
        ("GetAllParliamentaryGroups", [{"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID}]),
        ("GetAllMPsClubsByStructure", [{"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID}]),
        ("GetAllSittings", [
            {"methodName": "GetAllSittings", "Page": 1, "Rows": 5, "LanguageId": 1, "TypeId": 1, "CommitteeId": None, "StatusId": 3, "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None, "StructureId": STRUCTURE_ID},
            {"methodName": "GetAllSittings", "Page": 1, "Rows": 5, "LanguageId": 1, "TypeId": 2, "CommitteeId": committee_ids[0] if committee_ids else None, "StatusId": 1, "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None, "StructureId": STRUCTURE_ID},
        ]),
        ("GetAllQuestions", [
            {"methodName": "GetAllQuestions", "LanguageId": 1, "CurrentPage": 1, "Page": 1, "Rows": 5, "SearchText": "", "RegistrationNumber": "", "StatusId": None, "From": "", "To": "", "CommitteeId": None, "DateFrom": None, "DateTo": None, "StructureId": STRUCTURE_ID},
            {"methodName": "GetAllQuestions", "LanguageId": 1, "CurrentPage": 1, "Page": 1, "Rows": 5, "SearchText": "", "RegistrationNumber": "", "StatusId": 17, "From": "", "To": "", "CommitteeId": None, "DateFrom": None, "DateTo": None, "StructureId": STRUCTURE_ID},
        ]),
        ("GetAllMaterialsForPublicPortal", [
            {"MethodName": "GetAllMaterialsForPublicPortal", "LanguageId": 1, "ItemsPerPage": 5, "CurrentPage": 1, "SearchText": "", "AuthorText": "", "ActNumber": "", "StatusGroupId": None, "MaterialTypeId": 1, "ResponsibleCommitteeId": None, "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None, "EUCompatible": None, "DateFrom": None, "DateTo": None, "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID},
            {"MethodName": "GetAllMaterialsForPublicPortal", "LanguageId": 1, "ItemsPerPage": 5, "CurrentPage": 1, "SearchText": "", "AuthorText": "", "ActNumber": "", "StatusGroupId": 6, "MaterialTypeId": None, "ResponsibleCommitteeId": None, "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None, "EUCompatible": None, "DateFrom": None, "DateTo": None, "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID},
            {"MethodName": "GetAllMaterialsForPublicPortal", "LanguageId": 1, "ItemsPerPage": 5, "CurrentPage": 1, "SearchText": "", "AuthorText": "", "ActNumber": "", "StatusGroupId": None, "MaterialTypeId": 28, "ResponsibleCommitteeId": None, "CoReportingCommittees": None, "OpinionCommittees": None, "RegistrationNumber": None, "EUCompatible": None, "DateFrom": None, "DateTo": None, "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID},
        ]),
        ("GetParliamentMPsNoImage", [
            {"methodName": "GetParliamentMPsNoImage", "languageId": 1, "genderId": None, "ageFrom": None, "ageTo": None, "politicalPartyId": None, "searchText": None, "page": 1, "rows": 5, "StructureId": STRUCTURE_ID, "coalition": "", "constituency": ""},
            {"methodName": "GetParliamentMPsNoImage", "languageId": 1, "genderId": 1, "ageFrom": None, "ageTo": None, "politicalPartyId": None, "searchText": None, "page": 1, "rows": 5, "StructureId": STRUCTURE_ID, "coalition": "", "constituency": ""},
            {"methodName": "GetParliamentMPsNoImage", "languageId": 1, "genderId": None, "ageFrom": None, "ageTo": None, "politicalPartyId": party_ids[0] if party_ids else None, "searchText": None, "page": 1, "rows": 5, "StructureId": STRUCTURE_ID, "coalition": "", "constituency": ""},
        ]),
        ("GetMonthlyAgenda", [
            {"methodName": "GetMonthlyAgenda", "LanguageId": 1, "Month": 1, "Year": 2026},
            {"methodName": "GetMonthlyAgenda", "LanguageId": 1, "Month": 6, "Year": 2025},
        ]),
    ]

    # Detail endpoints (built from resolved IDs)
    detail_endpoints = [
        ("GetSittingDetails", [{"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1} for sid in sitting_ids[:5]]),
        ("GetMaterialDetails", [{"methodName": "GetMaterialDetails", "MaterialId": mid, "LanguageId": 1, "AmendmentsPage": 1, "AmendmentsRows": 5} for mid in material_ids[:3]]),
        ("GetQuestionDetails", [{"methodName": "GetQuestionDetails", "QuestionId": qid, "LanguageId": 1} for qid in question_ids[:3]]),
        ("GetCommitteeDetails", [{"methodName": "GetCommitteeDetails", "committeeId": cid, "languageId": 1} for cid in committee_ids[:3]]),
        ("GetCouncilDetails", [{"methodName": "GetCouncilDetails", "committeeId": cid, "languageId": 1} for cid in (council_ids or committee_ids[:2])]),
        ("GetPoliticalPartyDetails", [{"methodName": "GetPoliticalPartyDetails", "politicalPartyId": pid, "LanguageId": 1} for pid in party_ids[:3]]),
        ("GetParliamentaryGroupDetails", [{"methodName": "GetParliamentaryGroupDetails", "parliamentaryGroupId": gid, "LanguageId": 1} for gid in group_ids[:3]]),
        ("GetMPsClubDetails", [{"methodName": "GetMPsClubDetails", "mpsClubId": cid, "LanguageId": 1} for cid in club_ids[:2]]),
        ("GetUserDetailsByStructure", [{"methodName": "GetUserDetailsByStructure", "userId": uid, "structureId": STRUCTURE_ID, "languageId": 1} for uid in mp_user_ids[:2]]),
        ("GetAmendmentDetails", [{"methodName": "GetAmendmentDetails", "amendmentId": amendment_id, "languageId": 1}] if amendment_id else []),
        ("GetVotingResultsForSitting", [{"methodName": "GetVotingResultsForSitting", "votingDefinitionId": voting_def_id, "sittingId": sitting_ids[0], "languageId": 1}] if voting_def_id and sitting_ids else []),
        ("GetVotingResultsForAgendaItem", [{"methodName": "GetVotingResultsForAgendaItem", "VotingDefinitionId": voting_def_id, "AgendaItemId": agenda_item_id, "LanguageId": 1}] if voting_def_id and agenda_item_id else []),
        ("GetVotingResultsForAgendaItemReportDocument", [{"methodName": "GetVotingResultsForAgendaItemReportDocument", "VotingDefinitionId": voting_def_id, "AgendaItemId": agenda_item_id, "LanguageId": 1}] if voting_def_id and agenda_item_id else []),
    ]

    flat_endpoints = list(ENDPOINTS)
    for name, variants in detail_endpoints:
        if variants:
            flat_endpoints.append((name, variants))

    # --- 3. Execute and save ---
    for name, variants in flat_endpoints:
        if not variants:
            continue
        safe_name = re.sub(r"[^\w\-]", "_", name)
        samples = []
        for i, payload in enumerate(variants):
            print(f"  {name} (variant {i+1}/{len(variants)})...")
            data = api_post(API_URL, payload)
            samples.append({"request": payload, "response": truncate_for_storage(data)})
            manifest["calls"].append({"method": name, "variant": i})
            time.sleep(DELAY)
        with open(out_dir / f"{safe_name}.json", "w", encoding="utf-8") as f:
            json.dump({"method": name, "samples": samples}, f, ensure_ascii=False, indent=2)

    # Non-standard endpoints
    for name, url, payload in [
        ("GetCustomEventsCalendar", CALENDAR_URL, {"model": {"Language": 1, "Month": 1, "Year": 2026}}),
        ("GetCustomEventsCalendar", CALENDAR_URL, {"model": {"Language": 1, "Month": 6, "Year": 2025}}),
        ("LoadLanguage", LOAD_LANG_URL, {}),
        ("GetOfficialVisitsForUser", OFFICIAL_VISITS_URL, {"model": "914bff80-4c19-4675-ace4-cb0c7a08f688"}),
    ]:
        print(f"  {name}...")
        data = api_post(url, payload)
        safe = re.sub(r"[^\w\-]", "_", name)
        fpath = out_dir / f"{safe}.json"
        existing = json.loads(fpath.read_text()) if fpath.exists() else {"method": name, "samples": []}
        existing["samples"].append({"request": payload, "response": truncate_for_storage(data)})
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        manifest["calls"].append({"method": name})
        time.sleep(DELAY)

    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nCollected to {out_dir}")
    return 0


if __name__ == "__main__":
    exit(main())
