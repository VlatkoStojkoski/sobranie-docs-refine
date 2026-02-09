#!/usr/bin/env python3
"""
One-time: Build docs/API_DOCS.md from archive/schema_inference.json.
Run: python scripts/build_docs_from_archive.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARCHIVE = ROOT / "archive"
DOCS = ROOT / "docs"


def asp_date_ref(schema: dict) -> dict:
    if schema.get("format") == "asp-date" or (schema.get("pattern") and "Date" in str(schema.get("pattern", ""))):
        return {"$ref": "#/$defs/AspDate"}
    return schema


def transform(schema: dict) -> dict:
    if not schema:
        return {}
    if schema.get("type") == "object":
        out = {"type": "object", "properties": {}}
        for k, v in schema.get("properties", {}).items():
            if k.startswith("_"):
                continue
            s = transform(v)
            if s:
                out["properties"][k] = asp_date_ref(s) if s.get("format") == "asp-date" else s
        return out
    if schema.get("type") == "array":
        return {"type": "array", "items": transform(schema.get("items", {})) or {}}
    if schema.get("type") in ("string", "integer", "number", "boolean", "null"):
        s = {k: v for k, v in schema.items() if k in ("type", "format", "pattern", "nullable")}
        return asp_date_ref(s) if s.get("format") == "asp-date" else s
    return {}


def main():
    data = json.loads((ARCHIVE / "schema_inference.json").read_text())
    req_examples = {}
    coll = ARCHIVE / "2026-02-07_22-04-35"
    if coll.exists():
        for f in coll.glob("*.json"):
            if f.name == "manifest.json":
                continue
            try:
                d = json.loads(f.read_text())
                if d.get("samples") and d["samples"][0].get("request"):
                    req_examples[d.get("method", f.stem)] = d["samples"][0]["request"]
            except Exception:
                pass

    lines = ["# API Schemas", "", "Precise request/response schemas. From collected responses.", "", "## $defs", ""]
    lines.append("```json\n" + json.dumps({"AspDate": {"type": "string", "pattern": r"^/Date\(\d+\)/$"}}, indent=2) + "\n```\n")

    for method in sorted(data["endpoints"].keys()):
        schema = transform(data["endpoints"][method].get("schema", {}))
        if not schema:
            continue
        lines.append(f"## {method}\n")
        if method in req_examples:
            lines.append("### Request\n```json\n" + json.dumps(req_examples[method], indent=2, ensure_ascii=False) + "\n```\n")
        lines.append("### Response\n```json\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n```\n")

    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "API_DOCS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {DOCS}/API_DOCS.md")


if __name__ == "__main__":
    main()
