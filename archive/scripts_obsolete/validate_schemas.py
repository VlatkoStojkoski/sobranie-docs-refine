#!/usr/bin/env python3
"""
Validate that all collected requests/responses validate against schemas/api.json.
Run: python scripts/validate_schemas.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
COLLECTED = ROOT / "collected"
SCHEMAS = ROOT / "schemas"


def validate_all(data: dict, manifest_path: Path, collected_dir: Path) -> tuple[list, list]:
    """Validate all manifest pairs against schemas. Returns (req_failures, resp_failures)."""
    try:
        import jsonschema
    except ImportError:
        return ([("?", "jsonschema not installed")], [])

    requests_schemas = data.get("requests", {})
    responses_schemas = data.get("responses", {})
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator
    req_failures = []
    resp_failures = []

    for run in manifest.get("runs", []):
        for pair in run.get("pairs", []):
            op = pair["req"].split("/")[0]
            req_path = collected_dir / pair["req"]
            resp_path = collected_dir / pair["resp"]
            if not req_path.exists() or not resp_path.exists():
                continue
            req = json.loads(req_path.read_text(encoding="utf-8"))
            resp = json.loads(resp_path.read_text(encoding="utf-8"))

            if op in requests_schemas:
                schema = {"$defs": data.get("$defs", {}), **requests_schemas[op]}
                try:
                    validator(schema).validate(req)
                except jsonschema.ValidationError as e:
                    req_failures.append((pair["req"], str(e)))
            if op in responses_schemas:
                schema = {"$defs": data.get("$defs", {}), **responses_schemas[op]}
                try:
                    validator(schema).validate(resp)
                except jsonschema.ValidationError as e:
                    resp_failures.append((pair["resp"], str(e)))

    return req_failures, resp_failures


def main():
    try:
        import jsonschema
    except ImportError:
        print("pip install jsonschema")
        return 1

    api_path = SCHEMAS / "api.json"
    if not api_path.exists():
        print("schemas/api.json not found. Run phase4 first.")
        return 1

    data = json.loads(api_path.read_text(encoding="utf-8"))

    manifest_path = COLLECTED / "manifest.json"
    if not manifest_path.exists():
        print("collected/manifest.json not found.")
        return 1

    req_failures, resp_failures = validate_all(data, manifest_path, COLLECTED)

    if req_failures:
        print(f"Request validation failures: {len(req_failures)}")
        for path, msg in req_failures[:10]:
            print(f"  {path}: {msg[:80]}...")
    else:
        print("All requests validate")

    if resp_failures:
        print(f"Response validation failures: {len(resp_failures)}")
        for path, msg in resp_failures[:10]:
            print(f"  {path}: {msg[:80]}...")
    else:
        print("All responses validate")

    return 0 if not (req_failures or resp_failures) else 1


if __name__ == "__main__":
    exit(main())
