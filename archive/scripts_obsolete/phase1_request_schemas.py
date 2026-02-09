#!/usr/bin/env python3
"""
Phase 1: Request schemas from HAR + enrichment + LLM.

1. Build enrichment.json (LLM-assisted from docs, archive, collected, schema_inference)
2. Extract requests from HAR
3. LLM: produce JSON Schema per operation
4. Validate all known requests against schemas
5. Persist config/request_schemas.json

Run: python scripts/phase1_request_schemas.py
Env: ANTHROPIC_API_KEY
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
CONFIG = ROOT / "config"
COLLECTED = ROOT / "collected"
DOCS = ROOT / "docs"
ARCHIVE = ROOT / "archive"

MAX_EXCERPT = 2000


def _extract_op_section(text: str, op: str) -> str:
    """Extract ## OperationName section from markdown."""
    pat = rf"^## {re.escape(op)}\s*$"
    m = re.search(pat, text, re.MULTILINE)
    if not m:
        return ""
    start = m.end()
    next_m = re.search(r"\n## ", text[start:])
    end = start + (next_m.start() if next_m else len(text))
    return text[start:end].strip()[:MAX_EXCERPT]


def build_enrichment_raw() -> dict:
    """Aggregate raw data from docs, archive, collected, schema_inference."""
    raw: dict = {"sources": [], "by_operation": {}}
    ops = set()

    if (DOCS / "API_DOCS.md").exists():
        txt = (DOCS / "API_DOCS.md").read_text(encoding="utf-8")
        raw["sources"].append("docs/API_DOCS.md")
        for m in re.finditer(r"^## ([A-Z][a-zA-Z0-9]+)\s*$", txt, re.MULTILINE):
            op = m.group(1)
            if op in ("$defs", "Common patterns"):
                continue
            ops.add(op)
            if op not in raw["by_operation"]:
                raw["by_operation"][op] = {"excerpts": [], "request_notes": "", "response_notes": ""}
            raw["by_operation"][op]["excerpts"].append(f"[API_DOCS] {_extract_op_section(txt, op)}")

    if (DOCS / "API_INDEX.md").exists():
        raw["sources"].append("docs/API_INDEX.md")
        idx_txt = (DOCS / "API_INDEX.md").read_text(encoding="utf-8")[:MAX_EXCERPT * 2]
        for op in ops:
            if op not in raw["by_operation"]:
                raw["by_operation"][op] = {"excerpts": [], "request_notes": "", "response_notes": ""}
            raw["by_operation"][op]["excerpts"].append(f"[API_INDEX] {idx_txt[:MAX_EXCERPT]}")

    if (ROOT / "schema_inference.json").exists():
        raw["sources"].append("schema_inference.json")
        inf = json.loads((ROOT / "schema_inference.json").read_text(encoding="utf-8"))
        for op, ep in (inf.get("endpoints") or {}).items():
            ops.add(op)
            if op not in raw["by_operation"]:
                raw["by_operation"][op] = {"excerpts": [], "request_notes": "", "response_notes": ""}
            keys = ep.get("request_keys", [])
            raw["by_operation"][op]["excerpts"].append(f"[schema_inference] request_keys: {keys}")

    if (ARCHIVE / "API_DOC_FROM_DATA.md").exists():
        raw["sources"].append("archive/API_DOC_FROM_DATA.md")
        txt = (ARCHIVE / "API_DOC_FROM_DATA.md").read_text(encoding="utf-8")[:MAX_EXCERPT * 5]
        for op in list(ops):
            if op not in raw["by_operation"]:
                raw["by_operation"][op] = {"excerpts": [], "request_notes": "", "response_notes": ""}
            raw["by_operation"][op]["excerpts"].append(f"[API_DOC_FROM_DATA] {txt[:MAX_EXCERPT]}")

    manifest_path = COLLECTED / "manifest.json"
    if manifest_path.exists():
        raw["sources"].append("collected/manifest")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for run in manifest.get("runs", []):
            for pair in run.get("pairs", []):
                req_path = COLLECTED / pair["req"]
                if req_path.exists():
                    try:
                        req = json.loads(req_path.read_text(encoding="utf-8"))
                        op = req_path.parent.name
                        ops.add(op)
                        if op not in raw["by_operation"]:
                            raw["by_operation"][op] = {"excerpts": [], "request_notes": "", "response_notes": ""}
                        raw["by_operation"][op]["excerpts"].append(f"[collected request] {json.dumps(req)[:500]}")
                    except (json.JSONDecodeError, OSError):
                        pass

    return raw


def load_collected_requests() -> dict[str, list[dict]]:
    """Load all successful request bodies from manifest."""
    by_op: dict[str, list[dict]] = {}
    manifest_path = COLLECTED / "manifest.json"
    if not manifest_path.exists():
        return by_op
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for run in manifest.get("runs", []):
        for pair in run.get("pairs", []):
            req_path = COLLECTED / pair["req"]
            if req_path.exists():
                try:
                    req = json.loads(req_path.read_text(encoding="utf-8"))
                    op = req_path.parent.name
                    by_op.setdefault(op, []).append(req)
                except (json.JSONDecodeError, OSError):
                    pass
    return by_op


def main():
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    from improved.har_parser import extract_requests
    from improved.llm import complete_json, complete

    print("Phase 1: Request schemas")

    DATA.mkdir(parents=True, exist_ok=True)
    CONFIG.mkdir(parents=True, exist_ok=True)

    har_path = DATA / "session.har"
    if not har_path.exists():
        har_path = ARCHIVE / "logs.har"
    if not har_path.exists():
        print("ERROR: No HAR at data/session.har or archive/logs.har")
        return 1

    print("1. Building enrichment (raw aggregation)...")
    raw = build_enrichment_raw()
    raw_str = json.dumps(raw, ensure_ascii=False, indent=2)[:50000]
    print(f"   Aggregated {len(raw['by_operation'])} operations")

    print("2. LLM: structuring enrichment...")
    enrich_prompt = f"""Organize this API documentation aggregation into structured JSON.

Input (raw aggregation from docs, archive, collected, schema_inference):
{raw_str}

Output JSON with this shape (no other text):
{{
  "by_operation": {{
    "OperationName": {{
      "request_notes": "concise notes on request params",
      "response_notes": "concise notes on response",
      "excerpts": ["key excerpt 1", "key excerpt 2"]
    }}
  }}
}}

Include all operations from the input. Be concise. Output ONLY valid JSON."""
    enrichment = complete_json(enrich_prompt)
    (DATA / "enrichment.json").write_text(json.dumps(enrichment, ensure_ascii=False, indent=2), encoding="utf-8")
    print("   Saved data/enrichment.json")

    print("3. Extracting requests from HAR...")
    har_requests = extract_requests(har_path)
    collected_requests = load_collected_requests()
    all_ops = set(har_requests) | set(collected_requests) | set(enrichment.get("by_operation", {}))
    print(f"   HAR: {sum(len(v) for v in har_requests.values())} requests, {len(har_requests)} ops")
    print(f"   Collected: {sum(len(v) for v in collected_requests.values())} requests")

    print("4. LLM: producing request schemas...")
    by_op_data = enrichment.get("by_operation", {})
    schema_prompt_parts = [
        "Produce JSON Schema (draft 2020-12) for each operation's REQUEST body.",
        "RULES:",
        "- Optional filter params (TypeId, StatusId, CommitteeId, DateFrom, DateTo, etc.) MUST use anyOf: [type, {type:null}]",
        "- StatusId, TypeId are integers or null (e.g. StatusId 17, 19 for question statuses)",
        "- methodName: use enum with BOTH variants when API accepts both (e.g. GetQuestionDetails AND /GetQuestionDetails)",
        "- required: only params that are always present; optional filters must NOT be in required",
        "Common params: methodName/MethodName (string), languageId/LanguageId (integer 1-3), structureId/StructureId (uuid).",
        "",
        "Output JSON:",
        '{ "schemas": { "OperationName": { "type": "object", "properties": {...}, "required": [...] }, ... } }',
        "",
        "Operations and example requests (HAR + collected):",
    ]
    for op in sorted(all_ops):
        examples = (har_requests.get(op) or [])[:3] + (collected_requests.get(op) or [])[:2]
        notes = (by_op_data.get(op) or {}).get("request_notes", "")
        schema_prompt_parts.append(f"\n### {op}")
        if notes:
            schema_prompt_parts.append(f"Notes: {notes}")
        for i, ex in enumerate(examples[:3]):
            schema_prompt_parts.append(f"Example {i+1}: {json.dumps(ex, ensure_ascii=False)[:800]}")

    schema_prompt = "\n".join(schema_prompt_parts)
    if len(schema_prompt) > 90000:
        schema_prompt = schema_prompt[:90000] + "\n\n... (truncated)"
    out = complete_json(schema_prompt)
    schemas = out.get("schemas", out)

    try:
        import jsonschema
        from improved.schema_widener import widen_for_validation_failure, widen_optional_filters
    except ImportError:
        jsonschema = None

    # Proactive: widen optional filters before validation (cover all bodies)
    if jsonschema:
        schemas = widen_optional_filters(schemas)

    print("5. Validating schemas against known requests...")
    if jsonschema:
        validator_cls = jsonschema.Draft202012Validator
        max_rounds = 3
        for round in range(max_rounds):
            failed = []
            for op, schema in schemas.items():
                try:
                    validator = validator_cls(schema)
                except jsonschema.SchemaError:
                    continue
                requests_to_check = (har_requests.get(op) or []) + (collected_requests.get(op) or [])
                for req in requests_to_check:
                    try:
                        validator.validate(req)
                    except jsonschema.ValidationError as e:
                        failed.append((op, req, str(e)))
                        break
            if not failed:
                print("   All known requests validate")
                break
            print(f"   Round {round+1}: {len(failed)} failures, widening schemas...")
            schemas = widen_for_validation_failure(schemas, failed, har_requests, collected_requests)
            if round == max_rounds - 2:
                schemas = widen_optional_filters(schemas)
    else:
        print("   WARN: pip install jsonschema. Skipping validation.")

    print("6. Persisting config/request_schemas.json...")
    (CONFIG / "request_schemas.json").write_text(
        json.dumps({"schemas": schemas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"   Saved {len(schemas)} operation schemas")
    return 0


if __name__ == "__main__":
    exit(main())
