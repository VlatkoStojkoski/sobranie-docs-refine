#!/usr/bin/env python3
"""
Probe API endpoints from HAR_ANALYSIS_FINDINGS that are NOT yet in API.md.
Makes real requests and captures responses for schema documentation.
"""

import json
import time
from pathlib import Path

import requests

API_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
DELAY = 0.5
OUTPUT = "new_endpoints_responses.json"


def api_post(payload: dict):
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    root = Path(__file__).parent.parent
    results = {}

    # --- 1. Fetch reference IDs ---
    print("Fetching reference data...")
    parties = api_post({"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    committees = api_post({"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID})
    time.sleep(DELAY)
    sittings_resp = api_post({"methodName": "GetAllSittings", "Page": 1, "Rows": 5, "LanguageId": 1, "TypeId": 1,
        "CommitteeId": None, "StatusId": 3, "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None,
        "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    questions_resp = api_post({"methodName": "GetAllQuestions", "LanguageId": 1, "CurrentPage": 1, "Page": 1,
        "Rows": 10, "SearchText": "", "RegistrationNumber": "", "StatusId": None, "From": "", "To": "",
        "CommitteeId": None, "DateFrom": None, "DateTo": None, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)

    party_ids = [p["Id"] for p in (parties or [])[:2]]
    committee_ids = [c["Id"] for c in (committees or [])[:2]]
    sitting_ids = [s["Id"] for s in (sittings_resp.get("Items") or [])[:3]]
    question_ids = []
    if questions_resp and isinstance(questions_resp, dict) and questions_resp.get("Items"):
        question_ids = [q["Id"] for q in questions_resp["Items"][:2] if q.get("Id")]
    elif questions_resp and isinstance(questions_resp, list):
        question_ids = [q["Id"] for q in questions_resp[:2] if q.get("Id")]

    # Get voting IDs from a sitting with votes
    voting_def_id = None
    agenda_item_id = None
    for sid in sitting_ids:
        details = api_post({"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1})
        time.sleep(DELAY)
        agenda = (details or {}).get("Agenda") or {}
        children = agenda.get("children") or []
        for ch in children:
            vds = ch.get("VotingDefinitions") or []
            for vd in vds:
                if vd.get("Id"):
                    voting_def_id = vd["Id"]
                    agenda_item_id = ch.get("Id") or ch.get("objectId")
                    break
            if voting_def_id:
                break
        if voting_def_id:
            break

    # Get amendment IDs from materials
    amendment_id = None
    materials = api_post({"MethodName": "GetAllMaterialsForPublicPortal", "LanguageId": 1, "ItemsPerPage": 5,
        "CurrentPage": 1, "SearchText": "", "AuthorText": "", "ActNumber": "", "StatusGroupId": None,
        "MaterialTypeId": 1, "ResponsibleCommitteeId": None, "CoReportingCommittees": None, "OpinionCommittees": None,
        "RegistrationNumber": None, "EUCompatible": None, "DateFrom": None, "DateTo": None,
        "ProcedureTypeId": None, "InitiatorTypeId": None, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    for m in (materials.get("Items") or [])[:2]:
        mat_detail = api_post({"methodName": "GetMaterialDetails", "MaterialId": m["Id"], "LanguageId": 1,
            "AmendmentsPage": 1, "AmendmentsRows": 5})
        time.sleep(DELAY)
        amendments = (mat_detail or {}).get("Amendments") or {}
        items = amendments.get("Items") or []
        if items and items[0].get("Id"):
            amendment_id = items[0]["Id"]
            break

    # Get parliamentary group IDs and MPs club IDs
    groups = api_post({"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    mps_clubs = api_post({"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    councils = api_post({"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)

    group_ids = [g["Id"] for g in (groups or [])[:2]] if groups else []
    club_ids = [c["Id"] for c in (mps_clubs or [])[:2]] if mps_clubs and isinstance(mps_clubs, list) else []
    if mps_clubs and isinstance(mps_clubs, dict) and mps_clubs.get("Items"):
        club_ids = [c["Id"] for c in mps_clubs["Items"][:2] if c.get("Id")]
    council_ids = [c["Id"] for c in (councils or [])[:2]] if councils else []

    # --- 2. Probe NEW endpoints ---
    new_endpoints = [
        ("GetAllQuestionStatuses", {"methodName": "GetAllQuestionStatuses", "languageId": 1}),
        ("GetAllInstitutionsForFilter", {"methodName": "GetAllInstitutionsForFilter", "languageId": 1}),
        ("GetAllQuestions", {"methodName": "GetAllQuestions", "LanguageId": 1, "CurrentPage": 1, "Page": 1,
            "Rows": 10, "SearchText": "", "RegistrationNumber": "", "StatusId": None, "From": "", "To": "",
            "CommitteeId": None, "DateFrom": None, "DateTo": None, "StructureId": STRUCTURE_ID}),
        ("GetAllApplicationTypes", {"methodName": "GetAllApplicationTypes", "languageId": 1}),
        ("GetAllCouncils", {"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID}),
        ("GetAllParliamentaryGroups", {"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID}),
        ("GetAllMPsClubsByStructure", {"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID}),
    ]

    for name, payload in new_endpoints:
        print(f"  {name}...")
        try:
            data = api_post(payload)
            results[name] = {"request": payload, "response": data, "status": "ok"}
        except Exception as e:
            results[name] = {"request": payload, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    # Detail endpoints (need IDs)
    if question_ids:
        qid = question_ids[0]
        print("  GetQuestionDetails...")
        try:
            data = api_post({"methodName": "GetQuestionDetails", "QuestionId": qid, "LanguageId": 1})
            results["GetQuestionDetails"] = {"request": {"QuestionId": qid}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetQuestionDetails"] = {"request": {"QuestionId": qid}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    if party_ids:
        pid = party_ids[0]
        print("  GetPoliticalPartyDetails...")
        try:
            data = api_post({"methodName": "GetPoliticalPartyDetails", "politicalPartyId": pid, "LanguageId": 1})
            results["GetPoliticalPartyDetails"] = {"request": {"politicalPartyId": pid}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetPoliticalPartyDetails"] = {"request": {"politicalPartyId": pid}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    if committee_ids:
        cid = committee_ids[0]
        print("  GetCommitteeDetails...")
        try:
            data = api_post({"methodName": "GetCommitteeDetails", "committeeId": cid, "languageId": 1})
            results["GetCommitteeDetails"] = {"request": {"committeeId": cid}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetCommitteeDetails"] = {"request": {"committeeId": cid}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    if council_ids:
        cid = council_ids[0]
        print("  GetCouncilDetails...")
        try:
            data = api_post({"methodName": "GetCouncilDetails", "committeeId": cid, "languageId": 1})
            results["GetCouncilDetails"] = {"request": {"committeeId": cid}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetCouncilDetails"] = {"request": {"committeeId": cid}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    if group_ids:
        gid = group_ids[0]
        print("  GetParliamentaryGroupDetails...")
        try:
            data = api_post({"methodName": "GetParliamentaryGroupDetails", "parliamentaryGroupId": gid, "LanguageId": 1})
            results["GetParliamentaryGroupDetails"] = {"request": {"parliamentaryGroupId": gid}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetParliamentaryGroupDetails"] = {"request": {"parliamentaryGroupId": gid}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    if club_ids:
        cid = club_ids[0]
        print("  GetMPsClubDetails...")
        try:
            data = api_post({"methodName": "GetMPsClubDetails", "mpsClubId": cid, "LanguageId": 1})
            results["GetMPsClubDetails"] = {"request": {"mpsClubId": cid}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetMPsClubDetails"] = {"request": {"mpsClubId": cid}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    if amendment_id:
        print("  GetAmendmentDetails...")
        try:
            data = api_post({"methodName": "GetAmendmentDetails", "amendmentId": amendment_id, "languageId": 1})
            results["GetAmendmentDetails"] = {"request": {"amendmentId": amendment_id}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetAmendmentDetails"] = {"request": {"amendmentId": amendment_id}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    if voting_def_id and agenda_item_id and sitting_ids:
        sid = sitting_ids[0]
        print("  GetVotingResultsForAgendaItem...")
        try:
            data = api_post({"methodName": "GetVotingResultsForAgendaItem", "VotingDefinitionId": voting_def_id,
                "AgendaItemId": agenda_item_id, "LanguageId": 1})
            results["GetVotingResultsForAgendaItem"] = {"request": {"VotingDefinitionId": voting_def_id,
                "AgendaItemId": agenda_item_id}, "response": data, "status": "ok"}
        except Exception as e:
            results["GetVotingResultsForAgendaItem"] = {"request": {}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

        print("  GetVotingResultsForSitting...")
        try:
            data = api_post({"methodName": "GetVotingResultsForSitting", "votingDefinitionId": voting_def_id,
                "sittingId": sid, "languageId": 1})
            results["GetVotingResultsForSitting"] = {"request": {"votingDefinitionId": voting_def_id, "sittingId": sid},
                "response": data, "status": "ok"}
        except Exception as e:
            results["GetVotingResultsForSitting"] = {"request": {}, "error": str(e), "status": "error"}
        time.sleep(DELAY)

    # GetOfficialVisitsForUser - needs user ID, may need auth; try with placeholder
    print("  GetOfficialVisitsForUser (ASMX)...")
    try:
        resp = requests.post("https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser",
            json={"model": "914bff80-4c19-4675-ace4-cb0c7a08f688"}, headers={"Content-Type": "application/json"}, timeout=30)
        resp.raise_for_status()
        results["GetOfficialVisitsForUser"] = {"request": {"model": "user-uuid"}, "response": resp.json(), "status": "ok"}
    except Exception as e:
        results["GetOfficialVisitsForUser"] = {"request": {}, "error": str(e), "status": "error"}
    time.sleep(DELAY)

    # LoadLanguage - Infrastructure
    print("  LoadLanguage (Infrastructure)...")
    try:
        resp = requests.post("https://www.sobranie.mk/Infrastructure/LoadLanguage", json={}, timeout=30)
        resp.raise_for_status()
        body = resp.text
        results["LoadLanguage"] = {"request": {}, "response_preview": body[:200] if body else "empty", "status": resp.status_code}
    except Exception as e:
        results["LoadLanguage"] = {"request": {}, "error": str(e), "status": "error"}

    out_path = root / OUTPUT
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
