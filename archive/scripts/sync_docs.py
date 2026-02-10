#!/usr/bin/env python3
"""
Sync API.md and openapi.yaml from collected data and schema inference.
Single source of truth: schema_inference.json + collected_responses.

1. Updates openapi.yaml schemas and examples from real data
2. Generates API_DOC_FROM_DATA.md (machine-generated, can replace API.md sections)

Run: python scripts/sync_docs.py
"""

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
COLLECTED = ROOT / "collected_responses"
STRUCTURE_ID = "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"


def to_openapi_schema(schema: dict) -> dict:
    """Convert inferred schema to OpenAPI 3.0 format."""
    if not schema:
        return {}
    t = schema.get("type")
    if t == "object":
        props = schema.get("properties", {})
        out = {"type": "object", "properties": {}}
        for k, v in props.items():
            if k.startswith("_"):
                continue
            s = to_openapi_schema(v)
            if s:
                if schema.get("format") == "asp-date" or (v.get("format") == "asp-date"):
                    s = {"$ref": "#/components/schemas/AspDate"}
                elif v.get("format") == "asp-date":
                    s = {"$ref": "#/components/schemas/AspDate"}
                out["properties"][k] = s
        return out
    if t == "array":
        items = to_openapi_schema(schema.get("items", {}))
        return {"type": "array", "items": items if items else {}}
    if t in ("string", "integer", "number", "boolean"):
        out = {"type": t}
        if schema.get("format") == "uuid":
            out["format"] = "uuid"
        elif schema.get("format") == "asp-date" or schema.get("pattern"):
            return {"$ref": "#/components/schemas/AspDate"}
        if schema.get("nullable"):
            out["nullable"] = True
        return out
    if t == "null":
        return {"type": "string", "nullable": True}
    return {}


def sanitize_for_openapi(obj):
    """Replace collected IDs with placeholders for portable examples."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("SittingId", "MaterialId", "QuestionId", "committeeId", "politicalPartyId",
                     "parliamentaryGroupId", "mpsClubId", "userId", "amendmentId",
                     "VotingDefinitionId", "AgendaItemId", "votingDefinitionId", "sittingId"):
                if isinstance(v, str) and len(v) == 36:
                    out[k] = "00000000-0000-0000-0000-000000000000"
                else:
                    out[k] = v
            elif k in ("StructureId", "structureId"):
                out[k] = STRUCTURE_ID
            else:
                out[k] = sanitize_for_openapi(v)
        return out
    if isinstance(obj, list):
        return [sanitize_for_openapi(x) for x in obj]
    return obj


def get_canonical_request(method: str, samples: list) -> dict:
    """Get first successful request as canonical example."""
    for s in samples:
        req = s.get("request")
        resp = s.get("response")
        if req and (not isinstance(resp, dict) or not resp.get("_error")):
            return sanitize_for_openapi(req)
    return {}


def main():
    inference_path = ROOT / "schema_inference.json"
    if not inference_path.exists():
        print("Run infer_schema.py first.")
        return 1

    with open(inference_path) as f:
        inference = json.load(f)

    # Find latest collected run
    if not COLLECTED.exists():
        print("No collected_responses/ found.")
        return 1
    runs = sorted(COLLECTED.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    run_dir = runs[0]

    # Load OpenAPI spec
    openapi_path = ROOT / "openapi.yaml"
    with open(openapi_path) as f:
        spec = yaml.safe_load(f)

    schemas = spec.setdefault("components", {}).setdefault("schemas", {})
    examples = spec["paths"]["/Routing/MakePostRequest"]["post"]["requestBody"]["content"]["application/json"]["examples"]

    # Update schemas and examples from inference
    for method, data in inference["endpoints"].items():
        schema = data.get("schema", {})
        if not schema:
            continue

        # Skip non-MakePostRequest methods for main path
        if method in ("GetCustomEventsCalendar", "LoadLanguage", "GetOfficialVisitsForUser"):
            continue

        oa_schema = to_openapi_schema(schema)
        if oa_schema:
            schemas[f"{method}Response"] = oa_schema

        # Ensure we have request example
        if method not in examples:
            fpath = run_dir / f"{re.sub(r'[^\\w-]', '_', method)}.json"
            if fpath.exists():
                with open(fpath) as f:
                    coll = json.load(f)
                req = get_canonical_request(method, coll.get("samples", []))
                if req:
                    examples[method] = {"summary": method, "value": req}

    # Schema overrides (from API.md notes - fields that can be null)
    em = schemas.get("GetParliamentMPsNoImageResponse", {}).get("properties", {}).get("ExpiredMandateMembers", {})
    if em.get("items", {}).get("properties", {}).get("PoliticalPartyId"):
        em["items"]["properties"]["PoliticalPartyId"]["nullable"] = True

    # Ensure array items
    for name, s in list(schemas.items()):
        if not isinstance(s, dict):
            continue
        if s.get("type") == "array" and "items" not in s:
            s["items"] = {}
        props = s.get("properties", {})
        for k, v in props.items():
            if isinstance(v, dict) and v.get("type") == "array" and "items" not in v:
                v["items"] = {}

    with open(openapi_path, "w") as f:
        yaml.dump(spec, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Generate API_DOC_FROM_DATA.md
    doc_lines = [
        "# API Reference (from collected data)",
        "",
        "Machine-generated from schema_inference.json + collected_responses. Use to sync API.md.",
        "",
    ]

    for method in sorted(inference["endpoints"].keys()):
        data = inference["endpoints"][method]
        schema = data.get("schema", {})
        if not schema:
            continue

        doc_lines.append(f"## {method}\n")

        fpath = run_dir / f"{re.sub(r'[^\\w\\-]', '_', method)}.json"
        req = {}
        if fpath.exists():
            with open(fpath) as f:
                coll = json.load(f)
            req = get_canonical_request(method, coll.get("samples", []))

        if req:
            doc_lines.append("Request:")
            doc_lines.append("```json")
            doc_lines.append(json.dumps(req, indent=2, ensure_ascii=False))
            doc_lines.append("```\n")

        doc_lines.append("Response schema:")
        doc_lines.append("```json")
        doc_lines.append(json.dumps(schema, indent=2))
        doc_lines.append("```\n")

    with open(ROOT / "API_DOC_FROM_DATA.md", "w") as f:
        f.write("\n".join(doc_lines))

    print(f"Updated {openapi_path}")
    print(f"Generated API_DOC_FROM_DATA.md")
    return 0


if __name__ == "__main__":
    exit(main())
