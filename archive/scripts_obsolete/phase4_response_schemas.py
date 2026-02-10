#!/usr/bin/env python3
"""
Phase 4: Response schemas via algorithmic inference + LLM refinement.
Phase 5: Combine and write schemas/api.json.

Run: python scripts/phase4_response_schemas.py
Env: ANTHROPIC_API_KEY
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
COLLECTED = ROOT / "collected"
CONFIG = ROOT / "config"
SCHEMAS = ROOT / "schemas"
DATA = ROOT / "data"


def _validates_all(schema: dict, responses: list) -> bool:
    """Return True if all responses validate against schema."""
    try:
        import jsonschema
    except ImportError:
        return True
    try:
        validator = jsonschema.Draft202012Validator(schema)
        for resp in responses:
            validator.validate(resp)
        return True
    except (jsonschema.SchemaError, jsonschema.ValidationError):
        return False


def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-refinement", action="store_true", help="Skip LLM refinement; use algorithmic schemas only (faster)")
    parser.add_argument("--extract-defs", action="store_true", help="Extract shared object structures to $defs (experimental; can cause recursion)")
    parser.add_argument("--allow-validation-failures", action="store_true", help="Do not fail pipeline when validation gate has failures")
    args = parser.parse_args()

    sys.path.insert(0, str(ROOT / "scripts"))
    from improved.inference import infer_from_responses, load_responses_from_manifest, extract_shared_defs, infer_enum_additions
    from improved.llm import complete_json

    print("Phase 4: Response schemas")

    manifest_path = COLLECTED / "manifest.json"
    if not manifest_path.exists():
        print("ERROR: collected/manifest.json not found. Run phase3 first.")
        return 1

    request_schemas = {}
    if (CONFIG / "request_schemas.json").exists():
        data = json.loads((CONFIG / "request_schemas.json").read_text(encoding="utf-8"))
        request_schemas = data.get("schemas", data)

    print("1. Loading responses from manifest...")
    by_op = load_responses_from_manifest(COLLECTED, manifest_path)
    print(f"   {len(by_op)} operations, {sum(len(v) for v in by_op.values())} responses")

    print("2. Algorithmic inference...")
    response_schemas = {}
    for op, responses in by_op.items():
        schema, _ = infer_from_responses(responses)
        if schema:
            response_schemas[op] = schema

    if args.skip_refinement:
        print("3. Skipping LLM refinement (--skip-refinement)...")
        refined = dict(response_schemas)
    else:
        print("3. LLM refinement (descriptions only, no type changes)...")
        refined = {}
        for op in sorted(response_schemas.keys()):
            schema = response_schemas[op]
            prompt = f"""Refine this JSON Schema for API response of operation "{op}":
STRICT RULES - do NOT violate:
- ONLY add or update "description" fields. Do NOT change: type, anyOf, enum, required, properties, items, $ref
- Preserve anyOf [type, {{type:null}}] exactly - do not simplify to string or null
- Preserve all properties, structure, and nesting identically
- For integer fields (TypeId, StatusId, etc.), add "description" with possible values if evident
- Output ONLY valid JSON (the schema object) with identical structure to input"""
            schema_str = json.dumps(schema, indent=2)[:8000]
            full_prompt = f"{prompt}\n\n{schema_str}"
            try:
                out = complete_json(full_prompt)
                out = out if isinstance(out, dict) else schema
                # Validate refined schema against responses; fallback to algorithmic if invalid
                if _validates_all(out, by_op.get(op, [])):
                    refined[op] = out
                else:
                    refined[op] = schema
            except Exception:
                refined[op] = schema

    print("4. Building $defs (enums + shared structures)...")
    enum_defs_path = CONFIG / "enum_defs.json"
    if enum_defs_path.exists():
        defs = json.loads(enum_defs_path.read_text(encoding="utf-8"))
    else:
        defs = {"AspDate": {"type": "string", "pattern": r"^/Date\(\d+\)/$"}}
    defs = infer_enum_additions(by_op, defs)
    if args.extract_defs:
        try:
            shared_defs, refined = extract_shared_defs(refined)
            defs.update(shared_defs)
        except Exception as e:
            print(f"   WARN: $defs extraction failed ({e}), using inline schemas")

    print("5. Writing schemas/api.json...")
    SCHEMAS.mkdir(parents=True, exist_ok=True)
    output = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$defs": defs,
        "requests": request_schemas,
        "responses": refined
    }
    (SCHEMAS / "api.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"   Saved schemas/api.json ({len(request_schemas)} requests, {len(refined)} responses)")

    print("6. Validation gate (mandatory)...")
    manifest_path = COLLECTED / "manifest.json"
    if manifest_path.exists():
        from validate_schemas import validate_all
        req_failures, resp_failures = validate_all(output, manifest_path, COLLECTED)
        if req_failures or resp_failures:
            if req_failures:
                print(f"   FAIL: {len(req_failures)} request validation failures")
                for path, msg in req_failures[:5]:
                    print(f"      {path}: {msg[:100]}")
            if resp_failures:
                print(f"   FAIL: {len(resp_failures)} response validation failures")
                for path, msg in resp_failures[:5]:
                    print(f"      {path}: {msg[:100]}")
            if args.allow_validation_failures:
                print("   (Continuing due to --allow-validation-failures)")
            else:
                print("   Pipeline gate: validation failed. Fix schemas or re-run phases.")
                return 1
        else:
            print("   All collected bodies validate")
    else:
        print("   (No manifest; skip validation gate)")

    return 0


if __name__ == "__main__":
    exit(main())
