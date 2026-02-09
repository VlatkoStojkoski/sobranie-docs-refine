#!/usr/bin/env python3
"""
Build docs/API_DOCS.md from schema inference and collected data.

1. Uses schema_inference.json (run infer_schema.py first from collected/)
2. Falls back to archive/schema_inference.json if local not found
3. Request examples from collected/ or archive/

Run: python scripts/build_docs.py
     Or: python scripts/infer_schema.py && python scripts/build_docs.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
ARCHIVE = ROOT / "archive"
COLLECTED = ROOT / "collected"


def asp_date_ref(schema: dict) -> dict:
    if schema.get("format") == "asp-date" or (
        schema.get("pattern") and "Date" in str(schema.get("pattern", ""))
    ):
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


def parse_existing_operations(doc_path: Path) -> dict:
    """Parse existing API_DOCS.md for operation sections. Returns {method: block_text}."""
    if not doc_path.exists():
        return {}
    txt = doc_path.read_text(encoding="utf-8")
    # Match ## MethodName ... until next ## MethodName or end
    pattern = r"^(## [A-Z][a-zA-Z0-9]+)\n(.*?)(?=^## [A-Z][a-zA-Z0-9]+\n|\Z)"
    matches = re.findall(pattern, txt, re.MULTILINE | re.DOTALL)
    result = {}
    for header, body in matches:
        method = header.replace("## ", "").strip()
        if method in ("$defs", "Common patterns"):
            continue
        if method and body.strip():
            result[method] = body.strip()
    return result


def get_request_examples() -> dict:
    """Get canonical request per method from collected/ or archive."""
    for base in [COLLECTED, ARCHIVE]:
        if not base.exists():
            continue
        runs = sorted(base.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
        for run_dir in runs[:1]:
            if not run_dir.is_dir():
                continue
            examples = {}
            for f in run_dir.glob("*.json"):
                if f.name == "manifest.json":
                    continue
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    samples = d.get("samples", [])
                    for s in samples:
                        req = s.get("request")
                        resp = s.get("response")
                        if req and (not isinstance(resp, dict) or not resp.get("_error")):
                            method = d.get("method", f.stem)
                            if method not in examples:
                                examples[method] = req
                            break
                except Exception:
                    pass
            if examples:
                return examples
    return {}


def main():
    # Prefer local schema_inference, fallback to archive
    inference_path = ROOT / "schema_inference.json"
    if not inference_path.exists():
        inference_path = ARCHIVE / "schema_inference.json"
    if not inference_path.exists():
        print("Run infer_schema.py first, or ensure archive/schema_inference.json exists.")
        return 1

    data = json.loads(inference_path.read_text(encoding="utf-8"))
    req_examples = get_request_examples()

    # Preserve $defs and Common patterns from existing API_DOCS (never overwrite)
    defs_path = DOCS / "API_DOCS.md"
    prefix_lines = [
        "# API Schemas",
        "",
        "Precise request and response schemas. From collected responses + schema inference.",
        "",
    ]
    use_fallback = True
    if defs_path.exists():
        txt = defs_path.read_text(encoding="utf-8")
        m = re.search(r"^(.*?)(?=\n## GetAll|\n## Get[A-Z][a-z])", txt, re.DOTALL)
        if m:
            kept = m.group(1).strip()
            if "## $defs" in kept and "## Common patterns" in kept:
                prefix_lines = [kept, ""]
                use_fallback = False
    if use_fallback:
        # Fallback: minimal $defs
        defs_json = json.dumps(
            {"AspDate": {"type": "string", "pattern": r"^/Date\(\d+\)/$"}},
            indent=2,
        )
        prefix_lines = [
            "# API Schemas",
            "",
            "Precise request and response schemas. From collected responses + schema inference.",
            "",
            "## $defs",
            "",
            f"```json\n{defs_json}\n```",
            "",
            "## Common patterns",
            "",
            "- **Institutional authors**: `Authors[].Id` = `\"00000000-0000-0000-0000-000000000000\"` with full name in `FirstName`, empty `LastName`.",
            "- **Plenary vs committee**: `CommitteeId`/`CommitteeTitle` null for plenary (TypeId 1); populated for committee (2).",
            "",
        ]

    lines = list(prefix_lines)

    # All methods: from schema_inference + any extras from existing API_DOCS (append-only)
    inference_methods = set(data.get("endpoints", {}).keys())
    existing_ops = parse_existing_operations(defs_path)
    existing_only = set(existing_ops.keys()) - inference_methods
    all_methods = sorted(inference_methods | existing_only)

    for method in all_methods:
        if method in inference_methods:
            ep = data["endpoints"][method]
            schema = transform(ep.get("schema", {}))
            if not schema:
                continue
            lines.append(f"## {method}\n")
            if method in req_examples:
                lines.append("### Request\n```json\n" + json.dumps(req_examples[method], indent=2, ensure_ascii=False) + "\n```\n")
            lines.append("### Response\n```json\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n```\n")
        else:
            # Preserve operation from existing API_DOCS (not in schema_inference)
            lines.append(f"## {method}\n")
            lines.append(existing_ops[method] + "\n")

    num_ops = len(all_methods)
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "API_DOCS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {DOCS}/API_DOCS.md ({num_ops} operations)")
    return 0


if __name__ == "__main__":
    exit(main())
