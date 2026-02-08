#!/usr/bin/env python3
"""
Infer JSON schema from collected API responses. Data-driven — merges multiple samples
per endpoint to capture union of all shapes seen.

Output: schema_inference.json, docs/SCHEMA_INFERENCE_REPORT.md

Run: python scripts/infer_schema.py [collected/YYYY-MM-DD_HH-MM-SS]
     (default: latest collected/ subdir)
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
COLLECTED = ROOT / "collected"

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
        item_schemas = [
            infer_type(v)
            for v in val
            if not (isinstance(v, dict) and v.get("_truncated") is not None)
        ]
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


def merge_append_only(existing: dict, new: dict) -> dict:
    """
    Merge new schema into existing. Append-only: never remove or narrow.
    Result accepts all bodies that passed existing OR new.
    """
    if not new:
        return existing
    if not existing:
        return new

    ex_t, new_t = existing.get("type"), new.get("type")
    if ex_t != new_t:
        return existing  # type mismatch: keep existing, never narrow
    if ex_t == "object":
        all_props = dict(existing.get("properties") or {})
        for k, v in (new.get("properties") or {}).items():
            if k.startswith("_"):
                continue
            if k in all_props:
                all_props[k] = merge_append_only(all_props[k], v)
            else:
                all_props[k] = v
        return {"type": "object", "properties": all_props}
    if ex_t == "array":
        ex_items = existing.get("items") or {}
        new_items = new.get("items") or {}
        return {"type": "array", "items": merge_append_only(ex_items, new_items)}
    # primitive: take wider type (add nullable if either has it)
    out = {"type": ex_t}
    if existing.get("format") or new.get("format"):
        out["format"] = new.get("format") or existing.get("format")
    if existing.get("pattern") or new.get("pattern"):
        out["pattern"] = new.get("pattern") or existing.get("pattern")
    if existing.get("nullable") or new.get("nullable"):
        out["nullable"] = True
    return out


def main():
    if not COLLECTED.exists():
        print("No collected/ found. Run collect.py first.")
        return 1

    runs = sorted(COLLECTED.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    if not runs:
        print("No runs in collected/")
        return 1
    run_dir = runs[0]
    if len(sys.argv) > 1:
        run_dir = ROOT / sys.argv[1]

    if not run_dir.exists():
        print(f"Run dir not found: {run_dir}")
        return 1

    # Load existing schema_inference for append-only merge
    existing_inference = {}
    out_json = ROOT / "schema_inference.json"
    if out_json.exists():
        try:
            existing_inference = json.loads(out_json.read_text(encoding="utf-8"))
        except Exception:
            pass

    report = {"run": str(run_dir.name), "endpoints": {}}
    prior = existing_inference.get("runs_merged") or ([existing_inference["run"]] if existing_inference.get("run") else [])
    report["runs_merged"] = sorted(set([run_dir.name] + prior))

    # Start with existing endpoints (preserve ops not in current run)
    for method, ep in (existing_inference.get("endpoints") or {}).items():
        report["endpoints"][method] = dict(ep)

    for fpath in sorted(run_dir.glob("*.json")):
        if fpath.name == "manifest.json":
            continue
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception:
            continue
        method = data.get("method", fpath.stem)
        samples = data.get("samples", [])
        if not samples:
            continue

        schema = infer_from_samples(samples)
        simple = simplify_for_docs(schema)

        # Append-only: merge with existing schema for this endpoint
        existing_schema = (existing_inference.get("endpoints") or {}).get(method, {}).get("schema")
        if existing_schema:
            simple = merge_append_only(existing_schema, simple)

        errors = [s for s in samples if isinstance(s.get("response"), dict) and s["response"].get("_error")]
        ok_count = len(samples) - len(errors)

        report["endpoints"][method] = {
            "sample_count": len(samples),
            "ok_count": ok_count,
            "schema": simple,
            "request_keys": list(set(k for s in samples for k in (s.get("request") or {}).keys())),
        }

    # Build report_md
    report_md = [f"# Schema Inference Report\n\nRun: {run_dir.name}. Append-only merge with prior schema.\n\n"]
    for method in sorted(report["endpoints"].keys()):
        ep = report["endpoints"][method]
        report_md.append(f"## {method}\n\n")
        report_md.append(f"Samples: {ep.get('sample_count', 0)}, OK: {ep.get('ok_count', 0)}\n\n")
        report_md.append("```json\n")
        report_md.append(json.dumps(ep["schema"], indent=2))
        report_md.append("\n```\n\n")

    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    report_path = ROOT / "docs" / "SCHEMA_INFERENCE_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("".join(report_md), encoding="utf-8")

    print(f"Wrote {out_json} and {report_path} ({len(report['endpoints'])} endpoints)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
