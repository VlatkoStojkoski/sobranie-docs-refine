#!/usr/bin/env python3
"""
Collect diverse API samples for enrichment.

1. Listings: randomized filters (TypeId, StatusId, MaterialTypeId, etc.)
2. Detail: use IDs from listings to fetch item details
3. Output: collected/YYYY-MM-DD_HH-MM-SS/{operation}.json

Uses .api_cache/ for request caching. Use --no-cache to bypass.

Run: python scripts/collect.py [--no-cache]
"""

import argparse
import json
import logging
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

from cache import get as cache_get
from cache import set_ as cache_set

API = "https://www.sobranie.mk/Routing/MakePostRequest"
CALENDAR = "https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar"
LOAD_LANG = "https://www.sobranie.mk/Infrastructure/LoadLanguage"
OFFICIAL_VISITS = "https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
DELAY = 0.6
OUTPUT = "collected"
LOG_DIR = "logs"


def setup_logging(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "collect.log"
    fmt = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)
    logger = logging.getLogger("collect")
    if logger.handlers:
        logger.handlers.clear()
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter(fmt))
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    return logger


def post(url: str, payload: dict, retries: int = 2, use_cache: bool = True, log=None):
    if use_cache:
        cached = cache_get(url, payload)
        if cached is not None:
            if log:
                log.info("cache HIT %s", payload.get("methodName") or payload.get("MethodName") or payload.get("model") or "?")
            return cached
        if log:
            log.info("cache MISS %s", payload.get("methodName") or payload.get("MethodName") or payload.get("model") or "?")

    r = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(url, json=payload, timeout=(5, 30))
            if r.status_code == 200:
                data = r.json()
                if use_cache:
                    cache_set(url, payload, data)
                return data
            if r.status_code == 500 and attempt < retries:
                time.sleep(DELAY * 2)
                continue
        except requests.RequestException as e:
            if attempt < retries:
                time.sleep(DELAY * 2)
                continue
            return {"_error": "timeout", "_body": str(e)[:300]}

    out = {"_error": getattr(r, "status_code", "ERR"), "_body": getattr(r, "text", "")[:300]}
    if use_cache:
        cache_set(url, payload, out)
    return out


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache, hit live API")
    args = parser.parse_args()
    use_cache = not args.no_cache

    root = Path(__file__).parent.parent
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out = root / OUTPUT / ts
    out.mkdir(parents=True, exist_ok=True)
    log_dir = root / LOG_DIR / "collect" / ts
    log = setup_logging(log_dir)
    log.info("collect start use_cache=%s out=%s", use_cache, out)
    requests_log = log_dir / "requests_responses.jsonl"

    def save(name: str, samples: list):
        (out / f"{name}.json").write_text(
            json.dumps({"method": name, "samples": samples}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        log.info("saved %s (%d samples)", name, len(samples))

    def call(payload: dict, url=API):
        data = post(url, payload, use_cache=use_cache, log=log)
        status = "ok" if not (isinstance(data, dict) and data.get("_error")) else "error"
        log.info("call %s -> %s", payload.get("methodName") or payload.get("MethodName") or payload.get("model") or "?", status)
        with open(requests_log, "a", encoding="utf-8") as f:
            f.write(json.dumps({"url": url, "request": payload, "response": truncate(data), "status": status}, ensure_ascii=False) + "\n")
        time.sleep(DELAY)
        return data

    # --- Reference data ---
    log.info("Fetching reference data...")
    committees = call({"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID})
    parties = call({"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID})
    councils = call({"methodName": "GetAllCouncils", "languageId": 1, "StructureId": STRUCTURE_ID})
    groups = call({"methodName": "GetAllParliamentaryGroups", "languageId": 1, "StructureId": STRUCTURE_ID})
    clubs = call({"MethodName": "GetAllMPsClubsByStructure", "LanguageId": 1, "StructureId": STRUCTURE_ID})

    committee_ids = [c["Id"] for c in (committees or [])[:8]] if isinstance(committees, list) else []
    party_ids = [p["Id"] for p in (parties or [])[:5]] if isinstance(parties, list) else []
    council_ids = [c["Id"] for c in (councils or [])[:3]] if isinstance(councils, list) else []
    group_ids = [g["Id"] for g in (groups or [])[:5]] if isinstance(groups, list) else []
    club_ids = [c["Id"] for c in (clubs or [])[:3]] if isinstance(clubs, list) else []
    log.info("refs: committees=%d parties=%d councils=%d groups=%d clubs=%d", len(committee_ids), len(party_ids), len(council_ids), len(group_ids), len(club_ids))

    # --- Diverse listings ---
    sitting_samples = []
    for i in range(5):
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
        sitting_samples.append({"request": payload, "response": truncate(call(payload))})
    save("GetAllSittings", sitting_samples)

    sitting_ids = []
    for s in sitting_samples:
        items = s["response"].get("Items", []) if isinstance(s["response"], dict) else []
        sitting_ids.extend(x["Id"] for x in (items or [])[:3] if isinstance(x, dict) and x.get("Id"))

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
        question_samples.append({"request": payload, "response": truncate(call(payload))})
    save("GetAllQuestions", question_samples)

    question_ids = []
    for s in question_samples:
        items = s["response"].get("Items", []) if isinstance(s["response"], dict) else []
        question_ids.extend(x["Id"] for x in (items or [])[:2] if isinstance(x, dict) and x.get("Id"))

    material_samples = []
    for status_grp, mat_type in [(None, 1), (6, None), (None, 28), (10, None), (11, None), (12, None)]:
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
        material_samples.append({"request": payload, "response": truncate(call(payload))})
    save("GetAllMaterialsForPublicPortal", material_samples)

    material_ids = []
    for s in material_samples:
        items = s["response"].get("Items", []) if isinstance(s["response"], dict) else []
        material_ids.extend(x["Id"] for x in (items or [])[:3] if isinstance(x, dict) and x.get("Id"))

    # --- Catalogs ---
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
        save(name, [{"request": payload, "response": truncate(call(payload))}])

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
        mp_samples.append({"request": payload, "response": truncate(call(payload))})
    save("GetParliamentMPsNoImage", mp_samples)

    mp_user_ids = []
    for s in mp_samples:
        mems = s["response"].get("MembersOfParliament", []) if isinstance(s["response"], dict) else []
        mp_user_ids.extend(m.get("UserId") for m in (mems or [])[:2] if isinstance(m, dict) and m.get("UserId"))

    agenda_samples = []
    for month, year in [(1, 2026), (6, 2025)]:
        payload = {"methodName": "GetMonthlyAgenda", "LanguageId": 1, "Month": month, "Year": year}
        agenda_samples.append({"request": payload, "response": truncate(call(payload))})
    save("GetMonthlyAgenda", agenda_samples)

    # --- Detail endpoints ---
    def detail_samples(op: str, requests: list, return_samples: bool = False):
        samples = []
        for req in requests:
            samples.append({"request": req, "response": truncate(call(req))})
        if samples:
            save(op, samples)
        return samples if return_samples else None

    sitting_detail_samples = detail_samples("GetSittingDetails", [{"MethodName": "GetSittingDetails", "SittingId": sid, "LanguageId": 1} for sid in sitting_ids[:5]], return_samples=True)
    material_detail_samples = detail_samples("GetMaterialDetails", [{"methodName": "GetMaterialDetails", "MaterialId": mid, "LanguageId": 1, "AmendmentsPage": 1, "AmendmentsRows": 5} for mid in material_ids[:3]], return_samples=True)

    # Extract IDs for dependent endpoints
    voting_def_id, agenda_item_id = None, None
    for s in (sitting_detail_samples or []):
        det = s.get("response")
        if not isinstance(det, dict) or det.get("_error"):
            continue
        for ch in (det.get("Agenda") or {}).get("children") or []:
            for vd in (ch.get("VotingDefinitions") or []):
                if isinstance(vd, dict) and vd.get("Id"):
                    voting_def_id, agenda_item_id = vd["Id"], ch.get("Id") or ch.get("objectId")
                    break
            if voting_def_id:
                break
        if voting_def_id:
            break

    amendment_id = None
    for s in (material_detail_samples or []):
        mat = s.get("response")
        if not isinstance(mat, dict) or mat.get("_error"):
            continue
        items = (mat.get("Amendments") or {}).get("Items") or (mat.get("FirstReadingAmendments") or []) or (mat.get("SecondReadingAmendments") or [])
        if isinstance(items, list) and items and isinstance(items[0], dict) and items[0].get("Id"):
            amendment_id = items[0]["Id"]
            break

    if amendment_id:
        detail_samples("GetAmendmentDetails", [{"methodName": "GetAmendmentDetails", "amendmentId": amendment_id, "languageId": 1}])
    if voting_def_id and sitting_ids:
        detail_samples("GetVotingResultsForSitting", [{"methodName": "GetVotingResultsForSitting", "votingDefinitionId": voting_def_id, "sittingId": sitting_ids[0], "languageId": 1}])
    if voting_def_id and agenda_item_id:
        detail_samples("GetVotingResultsForAgendaItem", [{"methodName": "GetVotingResultsForAgendaItem", "VotingDefinitionId": voting_def_id, "AgendaItemId": agenda_item_id, "LanguageId": 1}])
        detail_samples("GetVotingResultsForAgendaItemReportDocument", [{"methodName": "GetVotingResultsForAgendaItemReportDocument", "VotingDefinitionId": voting_def_id, "AgendaItemId": agenda_item_id, "LanguageId": 1}])
    detail_samples("GetQuestionDetails", [{"methodName": "GetQuestionDetails", "QuestionId": qid, "LanguageId": 1} for qid in question_ids[:3]])
    detail_samples("GetCommitteeDetails", [{"methodName": "GetCommitteeDetails", "committeeId": cid, "languageId": 1} for cid in committee_ids[:3]])
    detail_samples("GetCouncilDetails", [{"methodName": "GetCouncilDetails", "committeeId": cid, "languageId": 1} for cid in (council_ids or committee_ids[:2])])
    detail_samples("GetPoliticalPartyDetails", [{"methodName": "GetPoliticalPartyDetails", "politicalPartyId": pid, "LanguageId": 1} for pid in party_ids[:3]])
    detail_samples("GetParliamentaryGroupDetails", [{"methodName": "GetParliamentaryGroupDetails", "parliamentaryGroupId": gid, "LanguageId": 1} for gid in group_ids[:3]])
    detail_samples("GetMPsClubDetails", [{"methodName": "GetMPsClubDetails", "mpsClubId": cid, "LanguageId": 1} for cid in club_ids[:2]])
    detail_samples("GetUserDetailsByStructure", [{"methodName": "GetUserDetailsByStructure", "userId": uid, "structureId": STRUCTURE_ID, "languageId": 1} for uid in mp_user_ids[:2]])

    # --- Non-standard ---
    cal_payload = {"model": {"Language": 1, "Month": 1, "Year": 2026}}
    save("GetCustomEventsCalendar", [{"request": cal_payload, "response": truncate(call(cal_payload, CALENDAR))}])
    save("LoadLanguage", [{"request": {}, "response": truncate(call({}, LOAD_LANG))}])
    visits_payload = {"model": "914bff80-4c19-4675-ace4-cb0c7a08f688"}
    save("GetOfficialVisitsForUser", [{"request": visits_payload, "response": truncate(call(visits_payload, OFFICIAL_VISITS))}])

    log.info("done %s", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
