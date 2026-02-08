#!/usr/bin/env python3
"""
Verify OpenAPI spec against live API. Makes actual requests for each endpoint
and checks that response structure matches documented schemas.
"""

import json
import time
from pathlib import Path

import requests
import yaml

API_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
DELAY = 0.8


def api_post(payload: dict, retries: int = 2):
    for attempt in range(retries + 1):
        resp = requests.post(API_URL, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 500 and attempt < retries:
            time.sleep(DELAY * 2)
            continue
        resp.raise_for_status()
    return resp.json()


def check_type(val, expected: str) -> bool:
    if expected == "array":
        return isinstance(val, list)
    if expected == "object":
        return isinstance(val, dict) and not (isinstance(val, type) and val.__name__ == "dict")
    if expected == "string":
        return isinstance(val, str)
    if expected == "integer":
        return isinstance(val, int)
    if expected == "number":
        return isinstance(val, (int, float))
    if expected == "boolean":
        return isinstance(val, bool)
    if expected == "null":
        return val is None
    return True


def check_schema(data, schema: dict, path: str = "") -> list[str]:
    """Recursively validate data against JSON schema. Returns list of errors."""
    errors = []
    if schema.get("type") == "array":
        if not isinstance(data, list):
            return [f"{path}: expected array, got {type(data).__name__}"]
        items = schema.get("items", {})
        for i, item in enumerate(data[:3]):  # sample first 3
            errors.extend(check_schema(item, items, f"{path}[{i}]"))
    elif schema.get("type") == "object":
        if not isinstance(data, dict):
            return [f"{path}: expected object, got {type(data).__name__}"]
        props = schema.get("properties", {})
        required = schema.get("required", [])
        for r in required:
            if r not in data:
                errors.append(f"{path}.{r}: required field missing")
        for k, v in data.items():
            if k in props:
                errors.extend(check_schema(v, props[k], f"{path}.{k}"))
    elif schema.get("type"):
        if data is None and schema.get("nullable") is True:
            pass  # null allowed
        elif not check_type(data, schema["type"]):
            errors.append(f"{path}: expected {schema['type']}, got {type(data).__name__}")
    return errors


def main():
    root = Path(__file__).parent.parent
    spec_path = root / "openapi.yaml"
    if not spec_path.exists():
        print(f"openapi.yaml not found at {spec_path}")
        return 1

    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    schemas = spec.get("components", {}).get("schemas", {})
    examples = spec.get("paths", {}).get("/Routing/MakePostRequest", {}).get("post", {}).get("requestBody", {}).get("content", {}).get("application/json", {}).get("examples", {})

    if not examples:
        print("No request examples in spec")
        return 1

    # Fetch reference IDs
    print("Fetching reference data...")
    structures = api_post({"methodName": "GetAllStructuresForFilter", "languageId": 1})
    time.sleep(DELAY)
    committees = api_post({"methodName": "GetAllCommitteesForFilter", "languageId": 1, "structureId": STRUCTURE_ID})
    time.sleep(DELAY)
    parties = api_post({"methodName": "GetAllPoliticalParties", "languageId": 1, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    questions = api_post({"methodName": "GetAllQuestions", "LanguageId": 1, "CurrentPage": 1, "Page": 1, "Rows": 5, "SearchText": "", "RegistrationNumber": "", "StatusId": None, "From": "", "To": "", "CommitteeId": None, "DateFrom": None, "DateTo": None, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)
    sittings = api_post({"methodName": "GetAllSittings", "Page": 1, "Rows": 5, "LanguageId": 1, "TypeId": 1, "CommitteeId": None, "StatusId": 3, "DateFrom": None, "DateTo": None, "SessionId": None, "Number": None, "StructureId": STRUCTURE_ID})
    time.sleep(DELAY)

    sitting_ids = [s["Id"] for s in (sittings.get("Items") or [])[:2]]
    committee_ids = [c["Id"] for c in (committees or [])[:2]]
    party_ids = [p["Id"] for p in (parties or [])[:2]]
    question_ids = [q["Id"] for q in (questions.get("Items") or [])[:2] if q.get("Id")]

    # Resolve $ref in examples (they may have value key)
    results = []
    for name, ex in examples.items():
        payload = ex.get("value", ex) if isinstance(ex, dict) else ex
        if not isinstance(payload, dict):
            continue
        # Substitute IDs for detail endpoints
        if "SittingId" in payload or "MethodName" in payload and "GetSittingDetails" in str(payload.get("MethodName", "")):
            payload = {**payload, "MethodName": "GetSittingDetails", "SittingId": sitting_ids[0] if sitting_ids else "00000000-0000-0000-0000-000000000000", "LanguageId": 1}
        elif "GetAllSittings" in str(payload.get("methodName", "")):
            payload = {**payload, "StructureId": STRUCTURE_ID}
        elif ("committeeId" in payload or "CommitteeId" in payload) and ("GetCouncilDetails" in str(payload.get("methodName", "")) or "GetCommitteeDetails" in str(payload.get("methodName", ""))):
            payload = {**payload, "committeeId": committee_ids[0] if committee_ids else "00000000-0000-0000-0000-000000000000", "languageId": 1}
        elif "politicalPartyId" in payload and ("GetParliamentaryGroupDetails" in str(payload.get("methodName", "")) or "GetPoliticalPartyDetails" in str(payload.get("methodName", ""))):
            payload = {**payload, "politicalPartyId": party_ids[0] if party_ids else "00000000-0000-0000-0000-000000000000", "LanguageId": 1}
        elif "QuestionId" in payload:
            payload = {**payload, "QuestionId": question_ids[0] if question_ids else "00000000-0000-0000-0000-000000000000", "LanguageId": 1}
        elif "StructureId" in str(payload):
            payload = {**payload, "StructureId": STRUCTURE_ID}
        elif "structureId" in str(payload):
            payload = {**payload, "structureId": STRUCTURE_ID}

        print(f"  {name}...")
        try:
            data = api_post(payload)
            time.sleep(DELAY)
            # Get response schema for this operation
            resp_schema = schemas.get(f"{name}Response", schemas.get(f"{name.replace('Request', '')}Response", {}))
            if resp_schema:
                errs = check_schema(data, resp_schema, "response")
                if errs:
                    results.append((name, "SCHEMA_ISSUES", errs))
                else:
                    results.append((name, "OK", None))
            else:
                results.append((name, "OK", None))
        except Exception as e:
            results.append((name, "ERROR", str(e)))

    print("\n--- Results ---")
    for name, status, detail in results:
        if status == "OK":
            print(f"  {name}: OK")
        elif status == "ERROR":
            print(f"  {name}: ERROR - {detail}")
        else:
            print(f"  {name}: SCHEMA_ISSUES")
            for e in (detail or [])[:5]:
                print(f"    - {e}")

    return 0 if all(r[1] == "OK" for r in results) else 1


if __name__ == "__main__":
    exit(main())
