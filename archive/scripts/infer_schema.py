#!/usr/bin/env python3
"""
Infer JSON schema from collected API responses. Data-driven only — no guessing.
Merges multiple samples per endpoint to capture union of all shapes seen.

Output: SCHEMA_INFERENCE_REPORT.md + schema_inference.json

Run: python scripts/infer_schema.py [collected_responses/YYYY-MM-DD_HH-MM-SS]
     (default: latest collected_responses/ subdir)
"""

import json
import re
from pathlib import Path
from collections import defaultdict

ASP_DATE_PATTERN = re.compile(r"^/Date\(\d+\)/$")


def infer_type(val):
    """Infer JSON schema type from a single value."""
    if val is None:
        return {"type": "null"}
    if isinstance(val, bool):
        return {"type": "boolean"}
    if isinstance(val, int):
        return {"type": "integer"}
    if isinstance(val, float):
        return {"type": "number"}
    if isinstance(val, str):
        if ASP_DATE_PATTERN.match(val):
            return {"type": "string", "format": "asp-date", "pattern": "^/Date\\(\\d+\\)/$"}
        if len(val) == 36 and val.count("-") == 4:
            try:
                int(val.replace("-", "")[:8], 16)
                return {"type": "string", "format": "uuid"}
            except ValueError:
                pass
        return {"type": "string"}
    if isinstance(val, list):
        if not val:
            return {"type": "array", "items": {}}
        item_schemas = [infer_type(v) for v in val if not (isinstance(v, dict) and v.get("_truncated") is not None)]
        merged = merge_schemas(item_schemas) if item_schemas else {}
        return {"type": "array", "items": merged}
    if isinstance(val, dict):
        if val.get("_truncated") is not None:
            return {"type": "array", "items": {}}
        if val.get("_error"):
            return {"type": "object", "properties": {"_error": {"type": "string"}}}
        props = {k: infer_type(v) for k, v in val.items()}
        return {"type": "object", "properties": props}
    return {}


def merge_schemas(schemas: list) -> dict:
    """Merge multiple inferred schemas into one (union of types, properties)."""
    schemas = [s for s in schemas if s]
    if not schemas:
        return {}
    first = schemas[0]
    if first.get("type") == "object":
        all_props = defaultdict(list)
        for s in schemas:
            for k, v in (s.get("properties") or {}).items():
                all_props[k].append(v)
        merged_props = {}
        for k, vlist in all_props.items():
            merged = merge_schemas(vlist) if len(vlist) > 1 else (vlist[0] if vlist else {})
            if merged:
                merged_props[k] = merged
        return {"type": "object", "properties": merged_props}
    if first.get("type") == "array":
        item_schemas = [s.get("items", {}) for s in schemas if s.get("items")]
        merged_items = merge_schemas(item_schemas) if item_schemas else {}
        return {"type": "array", "items": merged_items}
    types = set()
    for s in schemas:
        t = s.get("type")
        if t:
            types.add(t)
    if len(types) == 1:
        out = {"type": list(types)[0]}
        if first.get("format"):
            out["format"] = first["format"]
        if first.get("pattern"):
            out["pattern"] = first["pattern"]
        return out
    if "null" in types:
        types.discard("null")
        out = {"type": list(types)[0]} if len(types) == 1 else {}
        out["nullable"] = True
        return out
    return first


def infer_from_samples(samples: list) -> dict:
    """Infer schema from multiple response samples."""
    responses = [s.get("response") for s in samples if s.get("response") is not None]
    if not responses:
        return {}
    schemas = [infer_type(r) for r in responses]
    return merge_schemas(schemas)


def simplify_for_docs(schema: dict, path: str = "") -> dict:
    """Simplify schema for documentation: collapse trivial, add nullable where seen."""
    if not schema:
        return {}
    if schema.get("type") == "object":
        props = schema.get("properties", {})
        simplified = {}
        for k, v in props.items():
            if k.startswith("_"):
                continue
            s = simplify_for_docs(v, f"{path}.{k}")
            if s:
                simplified[k] = s
        return {"type": "object", "properties": simplified} if simplified else {"type": "object"}
    if schema.get("type") == "array":
        items = simplify_for_docs(schema.get("items", {}), f"{path}[]")
        return {"type": "array", "items": items if items else {}}
    out = {"type": schema.get("type", "string")}
    if schema.get("format"):
        out["format"] = schema["format"]
    if schema.get("pattern"):
        out["pattern"] = schema["pattern"]
    if schema.get("nullable"):
        out["nullable"] = True
    return out


def collect_unique_values(samples: list, path: str, results: dict):
    """Recursively collect unique values for enum inference."""
    for s in samples:
        data = s.get("response")
        if data is None:
            continue
        if path == "":
            obj = data
        else:
            obj = data
            for p in path.split("."):
                if p.endswith("[]"):
                    obj = obj.get(p[:-2], [])
                    if isinstance(obj, list) and obj:
                        obj = obj[0]
                else:
                    obj = obj.get(p) if isinstance(obj, dict) else None
                if obj is None:
                    break
        if obj is not None and not isinstance(obj, (dict, list)):
            results[path].add(obj)


def main():
    root = Path(__file__).parent.parent
    collected = root / "collected_responses"
    if not collected.exists():
        print("No collected_responses/ found. Run collect_all_responses.py first.")
        return 1

    # Use latest run
    runs = sorted(collected.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    if not runs:
        print("No runs in collected_responses/")
        return 1
    run_dir = runs[0]
    if len(__import__("sys").argv) > 1:
        run_dir = root / __import__("sys").argv[1]

    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"No manifest in {run_dir}")
        return 1

    report = {"run": str(run_dir.name), "endpoints": {}}
    report_md = [f"# Schema Inference Report\n\nRun: {run_dir.name}\n\n"]

    for fpath in sorted(run_dir.glob("*.json")):
        if fpath.name == "manifest.json":
            continue
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
        method = data.get("method", fpath.stem)
        samples = data.get("samples", [])
        if not samples:
            continue

        schema = infer_from_samples(samples)
        simple = simplify_for_docs(schema)

        # Check for errors in samples
        errors = [s for s in samples if isinstance(s.get("response"), dict) and s["response"].get("_error")]
        ok_count = len(samples) - len(errors)

        report["endpoints"][method] = {
            "sample_count": len(samples),
            "ok_count": ok_count,
            "schema": simple,
            "request_keys": list(set(k for s in samples for k in (s.get("request") or {}).keys())),
        }

        report_md.append(f"## {method}\n\n")
        report_md.append(f"Samples: {len(samples)}, OK: {ok_count}\n\n")
        report_md.append("```json\n")
        report_md.append(json.dumps(simple, indent=2))
        report_md.append("\n```\n\n")

    with open(root / "schema_inference.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    with open(root / "SCHEMA_INFERENCE_REPORT.md", "w", encoding="utf-8") as f:
        f.write("".join(report_md))

    print(f"Wrote schema_inference.json and SCHEMA_INFERENCE_REPORT.md ({len(report['endpoints'])} endpoints)")
    return 0


if __name__ == "__main__":
    exit(main())
