#!/usr/bin/env python3
"""
Collect diverse API samples for enrichment.

1. Listings: randomized filters (TypeId, StatusId, MaterialTypeId, etc.) to get varied items
2. Detail: use IDs from listings to fetch item details
3. Output: collected/YYYY-MM-DD_HH-MM-SS/{operation}.json

Run: python scripts/collect.py
"""

import json
import random
import time
from datetime import datetime
from pathlib import Path

import requests

API = "https://www.sobranie.mk/Routing/MakePostRequest"
CALENDAR = "https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar"
LOAD_LANG = "https://www.sobranie.mk/Infrastructure/LoadLanguage"
OFFICIAL_VISITS = "https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
DELAY = 0.6
OUTPUT = "collected"


def post(url: str, payload: dict, retries: int = 2):
    for attempt in range(retries + 1):
        try:
            r = requests.post(url, json=payload, timeout=(5, 30))
            if r.status_code == 200:
                return r.json()
            if r.status_code == 500 and attempt < retries:
                time.sleep(DELAY * 2)
                continue
        except requests.RequestException:
            if attempt < retries:
                time.sleep(DELAY * 2)
                continue
        return {"_error": getattr(r, "status_code", "ERR"), "_body": getattr(r, "text", "")[:300]}
    return {"_error": "timeout"}


def truncate(obj, max_arr=10, max_str=2000):
    if isinstance(obj, dict):
        return {k: truncate(v, max_arr, max_str) for k, v in obj.items()}
    if isinstance(obj, list):
        return [truncate(x, max_arr, max_str) for x in obj[:max_arr]] + (
            [{"_truncated": len(obj) - max_arr}] if len(obj) > max_arr else []
        )
    if isinstance(obj, str) and len(obj) > max_str:
        return obj[:max_str] + "..."
    return obj


def main():
    root = Path(__file__).parent.parent
    out = root / OUTPUT / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out.mkdir(parents=True, exist_ok=True)

    def save(name: str, samples: list):
        (out / f"{name}.json").write_text(
            json.dumps({"method": name, "samples": samples}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def call(name: str, payload: dict, url=API):
        data = post(url, payload)
        time.sleep(DELAY)
        return data

    # --- Reference data ---
    print("Fetching reference data...")
    committees = call("committees", {"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID})
    parties = call("parties", {"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID})
    councils = call("councils", {"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID})
    groups = call("groups", {"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID})
    clubs = call("clubs", {"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID})

    committee_ids = [c["Id"] for c in (committees or [])[:8]] if isinstance(committees, list) else []
    party_ids = [p["Id"] for p in (parties or [])[:5]] if isinstance(parties, list) else []
    council_ids = [c["Id"] for c in (councils or [])[:3]] if isinstance(councils, list) else []
    group_ids = [g["Id"] for g in (groups or [])[:5]] if isinstance(groups, list) else []
    club_ids = [c["Id"] for c in (clubs or [])[:3]] if isinstance(clubs, list) else []

    # --- Diverse listings ---
    sitting_samples = []
    for _ in range(5):
        payload = {
            "methodName": "GetAllSittings",
            "Page": random.randint(1, 3),
            "Rows": random.randint(5, 15),
            "LanguageId": random.choice([1, 1, 1, 2]),
            "TypeId": random.choice([1, 2, None]),
            "CommitteeId": random.choice([None] + committee_ids[:2]) if committee_ids else None,
            "StatusId": random.choice([1, 2, 3, 4, 5, 6, None]),
            "DateFrom": None,
            "DateTo": None,
            "SessionId": None,
            "Number": None,
            "StructureId": STRUCTURE_ID,
        }
        sitting_samples.append({"request": payload, "response": truncate(call("sittings", payload))})
        time.sleep(DELAY)
    save("GetAllSittings", sitting_samples)

    sitting_ids = []
    for s in sitting_samples:
        items = s["response"].get("Items", []) if isinstance(s["response"], dict) else []
        sitting_ids.extend(x["Id"] for x in items[:3] if x.get("Id"))

    question_samples = []
    for status in [None, 17, 19]:
        payload = {
            "methodName": "GetAllQuestions",
            "LanguageId": 1,
            "CurrentPage": 1,
            "Page": 1,
            "Rows": random.randint(5, 12),
            "SearchText": "",
            "RegistrationNumber": "",
            "StatusId": status,
            "From": "",
            "To": "",
            "CommitteeId": None,
            "DateFrom": None,
            "DateTo": None,
            "StructureId": STRUCTURE_ID,
        }
        question_samples.append({"request": payload, "response": truncate(call("questions", payload))})
        time.sleep(DELAY)
    save("GetAllQuestions", question_samples)

    question_ids = []
    for s in question_samples:
        items = s["response"].get("Items", []) if isinstance(s["response"], dict) else []
        question_ids.extend(x["Id"] for x in items[:2] if x.get("Id"))

    material_samples = []
    for status_grp, mat_type in [(None, 1), (6, None), (None, 28)]:
        payload = {
            "MethodName": "GetAllMaterialsForPublicPortal",
            "LanguageId": 1,
            "ItemsPerPage": random.randint(5, 10),
            "CurrentPage": 1,
            "SearchText": "",
            "AuthorText": "",
            "ActNumber": "",
            "StatusGroupId": status_grp,
            "MaterialTypeId": mat_type,
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
        material_samples.append({"request": payload, "response": truncate(call("materials", payload))})
        time.sleep(DELAY)
    save("GetAllMaterialsForPublicPortal", material_samples)

    material_ids = []
    for s in material_samples:
        items = s["response"].get("Items", []) if isinstance(s["response"], dict) else []
        material_ids.extend(x["Id"] for x in items[:3] if x.get("Id"))

    # --- Catalogs (single sample each) ---
    for name, payload in [
        ("GetAllGenders", {"methodName": "GetAllGenders", "languageId": 1}),
        ("GetAllStructuresForFilter", {"methodName": "GetAllStructuresForFilter", "languageId": 1}),
        ("GetAllCommitteesForFilter", {"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID}),
        ("GetAllMaterialStatusesForFilter", {"methodName": "GetAllMaterialStatusesForFilter", "languageId": 1}),
        ("GetAllMaterialTypesForFilter", {"methodName": "GetAllMaterialTypesForFilter", "languageId": 1}),
        ("GetAllSittingStatuses", {"methodName": "GetAllSittingStatuses", "LanguageId": 1}),
        ("GetAllQuestionStatuses", {"methodName": "GetAllQuestionStatuses", "languageId": 1}),
        ("GetAllInstitutionsForFilter", {"methodName": "GetAllInstitutionsForFilter", "languageId": 1}),
        ("GetAllProcedureTypes", {"methodName": "GetAllProcedureTypes", "languageId": 1}),
        ("GetProposerTypes", {"methodName": "GetProposerTypes", "languageId": 1}),
        ("GetAllApplicationTypes", {"methodName": "GetAllApplicationTypes", "languageId": 1}),
        ("GetAllPoliticalParties", {"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID}),
        ("GetAllCouncils", {"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID}),
        ("GetAllParliamentaryGroups", {"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID}),
        ("GetAllMPsClubsByStructure", {"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID}),
    ]:
        save(name, [{"request": payload, "response": truncate(call(name, payload))}])

    # --- Listings: MPs, Agenda ---
    mp_samples = []
    for gender, party in [(None, None), (1, None), (None, party_ids[0] if party_ids else None)]:
        payload = {
            "methodName": "GetParliamentMPsNoImage",
            "languageId": 1,
            "genderId": gender,
            "ageFrom": None,
            "ageTo": None,
            "politicalPartyId": party,
            "searchText": None,
            "page": 1,
            "rows": 8,
            "StructureId": STRUCTURE_ID,
            "coalition": "",
            "constituency": "",
        }
        mp_samples.append({"request": payload, "response": truncate(call("mps", payload))})
        time.sleep(DELAY)
    save("GetParliamentMPsNoImage", mp_samples)

    mp_user_ids = []
    for s in mp_samples:
        mems = s["response"].get("MembersOfParliament", []) if isinstance(s["response"], dict) else []
        mp_user_ids.extend(m.get("UserId") for m in mems[:2] if m.get("UserId"))

    agenda_samples = []
    for month, year in [(1, 2026), (6, 2025)]:
        payload = {"methodName": "GetMonthlyAgenda", "LanguageId": 1, "Month": month, "Year": year}
        agenda_samples.append({"request": payload, "response": truncate(call("agenda", payload))})
        time.sleep(DELAY)
    save("GetMonthlyAgenda", agenda_samples)

    # --- Detail endpoints ---
    def detail_samples(op: str, requests: list):
        samples = []
        for req in requests:
            samples.append({"request": req, "response": truncate(call(op, req))})
            time.sleep(DELAY)
        if samples:
            save(op, samples)

    detail_samples("GetSittingDetails", [{"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1} for sid in sitting_ids[:5]])
    detail_samples("GetMaterialDetails", [{"methodName": "GetMaterialDetails", "MaterialId": mid, "LanguageId": 1, "AmendmentsPage": 1, "AmendmentsRows": 5} for mid in material_ids[:3]])
    detail_samples("GetQuestionDetails", [{"methodName": "GetQuestionDetails", "QuestionId": qid, "LanguageId": 1} for qid in question_ids[:3]])
    detail_samples("GetCommitteeDetails", [{"methodName": "GetCommitteeDetails", "committeeId": cid, "languageId": 1} for cid in committee_ids[:3]])
    detail_samples("GetCouncilDetails", [{"methodName": "GetCouncilDetails", "committeeId": cid, "languageId": 1} for cid in (council_ids or committee_ids[:2])])
    detail_samples("GetPoliticalPartyDetails", [{"methodName": "GetPoliticalPartyDetails", "politicalPartyId": pid, "LanguageId": 1} for pid in party_ids[:3]])
    detail_samples("GetParliamentaryGroupDetails", [{"methodName": "GetParliamentaryGroupDetails", "parliamentaryGroupId": gid, "LanguageId": 1} for gid in group_ids[:3]])
    detail_samples("GetMPsClubDetails", [{"methodName": "GetMPsClubDetails", "mpsClubId": cid, "LanguageId": 1} for cid in club_ids[:2]])
    detail_samples("GetUserDetailsByStructure", [{"methodName": "GetUserDetailsByStructure", "userId": uid, "structureId": STRUCTURE_ID, "languageId": 1} for uid in mp_user_ids[:2]])

    # --- Non-standard ---
    save("GetCustomEventsCalendar", [{"request": {"model": {"Language": 1, "Month": 1, "Year": 2026}}, "response": truncate(call("calendar", {"model": {"Language": 1, "Month": 1, "Year": 2026}}, CALENDAR))])
    save("LoadLanguage", [{"request": {}, "response": truncate(call("lang", {}, LOAD_LANG))])
    save("GetOfficialVisitsForUser", [{"request": {"model": "914bff80-4c19-4675-ace4-cb0c7a08f688"}, "response": truncate(call("visits", {"model": "914bff80-4c19-4675-ace4-cb0c7a08f688"}, OFFICIAL_VISITS))])

    print(f"Collected to {out}")


if __name__ == "__main__":
    main()
