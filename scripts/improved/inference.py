"""
Algorithmic response schema inference. Extends infer_schema logic with:
- anyOf for type conflicts
- required inference
- $defs extraction for identical structures
"""

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ASP_DATE_PATTERN = re.compile(r"^/Date\(\d+\)/$")

# Response fields commonly nullable (Email, Phone, Image, etc.)
NULLABLE_RESPONSE_FIELDS = {
    "Email", "Phone", "Image", "ImageUrl", "Photo", "Address", "Description",
    "Title", "Link", "Url", "Date", "Value", "Text", "Note", "Remark",
}

def infer_type(val) -> dict:
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
            return {"type": "string", "format": "asp-date", "pattern": r"^/Date\(\d+\)/$"}
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
        props = {k: infer_type(v) for k, v in val.items() if not k.startswith("_")}
        return {"type": "object", "properties": props}
    return {}


def _extract_constituent_schemas(schema: dict) -> list[dict]:
    """Expand schema into constituent type schemas (handles anyOf)."""
    if not schema:
        return []
    if "anyOf" in schema:
        out = []
        for sub in schema["anyOf"]:
            out.extend(_extract_constituent_schemas(sub))
        return out
    t = schema.get("type")
    if t:
        return [dict(schema)]
    return []


def _merge_primitive_schemas(schemas: list) -> dict:
    """Merge primitive/anyOf schemas; never produce null-only."""
    expanded = []
    for s in schemas:
        expanded.extend(_extract_constituent_schemas(s))
    if not expanded:
        return {}
    types = set()
    fmt = None
    pat = None
    for s in expanded:
        t = s.get("type")
        if t:
            types.add(t)
        if s.get("format"):
            fmt = s.get("format")
        if s.get("pattern"):
            pat = s.get("pattern")
    if not types:
        return {"type": "string"}
    if types == {"null"}:
        return {"anyOf": [{"type": "string", **({"format": fmt} if fmt else {})}, {"type": "null"}]}
    if len(types) == 1 and "null" not in types:
        out = {"type": list(types)[0]}
        if fmt:
            out["format"] = fmt
        if pat:
            out["pattern"] = pat
        return out
    if "null" in types:
        types.discard("null")
    branches = [{"type": t} for t in types]
    if fmt and "string" in types:
        for b in branches:
            if b.get("type") == "string":
                b["format"] = fmt
                break
    if pat and "string" in types:
        for b in branches:
            if b.get("type") == "string":
                b["pattern"] = pat
                break
    branches.append({"type": "null"})
    return {"anyOf": branches}


def merge_schemas(schemas: list) -> dict:
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
    return _merge_primitive_schemas(schemas)


def infer_required(responses: list, path: str = "", prefix: str = "") -> set:
    """Return keys present in all responses at path."""
    if not responses:
        return set()
    if path:
        parts = path.split(".")
        acc = []
        for r in responses:
            v = r
            for p in parts:
                v = v.get(p) if isinstance(v, dict) else None
            acc.append(v)
        responses = acc
    if not responses:
        return set()
    first = responses[0]
    if not isinstance(first, dict):
        return set()
    required = set()
    for k in first.keys():
        if k.startswith("_"):
            continue
        if all(isinstance(r, dict) and k in r for r in responses):
            required.add(k)
    return required


def _ensure_nullable(prop: dict) -> dict:
    """Ensure property accepts null (anyOf [type, null])."""
    if not prop or prop.get("type") == "null":
        return prop
    if "anyOf" in prop or (isinstance(prop.get("type"), list) and "null" in prop.get("type", [])):
        return prop
    return {"anyOf": [dict(prop), {"type": "null"}]}


def _is_null_only(schema: dict) -> bool:
    """True if schema only accepts null."""
    if not schema:
        return False
    if schema.get("type") == "null":
        return True
    if "anyOf" in schema:
        return all(s.get("type") == "null" for s in schema["anyOf"])
    return False


def _fix_narrow_id_title(schema: dict, key: str = "") -> dict:
    """For *Id and *Title: never allow null-only; ensure string/uuid + null."""
    if not schema or not isinstance(schema, dict):
        return schema
    if schema.get("type") == "object":
        props = schema.get("properties") or {}
        required = set(schema.get("required") or [])
        out = {}
        for k, v in props.items():
            v = _fix_narrow_id_title(v, k)
            if (k.endswith("Id") or k.endswith("Title")) and _is_null_only(v):
                if k.endswith("Id"):
                    v = {"anyOf": [{"type": "string", "format": "uuid"}, {"type": "null"}]}
                else:
                    v = {"anyOf": [{"type": "string"}, {"type": "null"}]}
            out[k] = v
        return {"type": "object", "properties": out, **{x: schema[x] for x in schema if x not in ("type", "properties")}}
    if schema.get("type") == "array" and "items" in schema:
        return {"type": "array", "items": _fix_narrow_id_title(schema["items"], ""), **{x: schema[x] for x in schema if x not in ("type", "items")}}
    if "anyOf" in schema:
        return {"anyOf": [_fix_narrow_id_title(s, key) for s in schema["anyOf"]], **{x: schema[x] for x in schema if x != "anyOf"}}
    return schema


def _widen_nullable_fields(schema: dict, in_required: set = None) -> dict:
    """Recursively widen response fields to accept null where common."""
    if not schema or not isinstance(schema, dict):
        return schema
    in_required = in_required or set()
    if schema.get("type") == "object":
        props = schema.get("properties") or {}
        required = set(schema.get("required") or [])
        out_props = {}
        for k, v in props.items():
            v = _widen_nullable_fields(v, required)
            # Widen: *Id/*Title, known nullable fields, or string/number not in required
            is_id_or_title = k.endswith("Id") or k.endswith("Title")
            should_null = (
                is_id_or_title
                or k in NULLABLE_RESPONSE_FIELDS
                or (v.get("type") in ("string", "number") and k not in required)
            )
            if should_null and v.get("type") not in ("null",) and "anyOf" not in v:
                v = _ensure_nullable(v)
            out_props[k] = v
        return {"type": "object", "properties": out_props, **{x: schema[x] for x in schema if x not in ("type", "properties")}}
    if schema.get("type") == "array" and "items" in schema:
        return {"type": "array", "items": _widen_nullable_fields(schema["items"], set()), **{x: schema[x] for x in schema if x not in ("type", "items")}}
    if "anyOf" in schema:
        return {"anyOf": [_widen_nullable_fields(s, set()) for s in schema["anyOf"]], **{x: schema[x] for x in schema if x != "anyOf"}}
    return schema


def infer_from_responses(responses: list) -> tuple[dict, set]:
    """Infer schema and required fields from response list."""
    valid = [r for r in responses if r is not None and not (isinstance(r, dict) and r.get("_error"))]
    if not valid:
        return {}, set()
    schemas = [infer_type(r) for r in valid]
    schema = merge_schemas(schemas)
    required = infer_required(valid)
    if schema.get("type") == "object" and required:
        schema["required"] = sorted(required)
    schema = _widen_nullable_fields(schema)
    schema = _fix_narrow_id_title(schema)
    return schema, required


KNOWN_ENUM_FIELDS = (
    "LanguageId", "GenderId", "SittingStatusId", "AgendaItemTypeId", "QuestionStatusId",
    "MaterialStatusId", "ProposerTypeId", "ProcedureTypeId", "StatusId", "TypeId",
    "MaterialTypeId", "DocumentTypeId", "RoleId", "ObjectStatusId", "StatusGroupId",
)


def _collect_enum_values(obj, path: str, acc: dict) -> None:
    """Recursively collect integer values for known enum fields."""
    if obj is None:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("_"):
                continue
            p = f"{path}.{k}" if path else k
            if k in KNOWN_ENUM_FIELDS and isinstance(v, int):
                acc.setdefault(k, set()).add(v)
            _collect_enum_values(v, p, acc)
    elif isinstance(obj, list):
        for v in obj:
            _collect_enum_values(v, path, acc)


def infer_enum_additions(responses_by_op: dict[str, list], base_defs: dict) -> dict:
    """Merge observed enum values from responses into base_defs; return updated defs."""
    observed: dict[str, set] = {}
    for op, responses in responses_by_op.items():
        for r in responses:
            _collect_enum_values(r, "", observed)
    defs = dict(base_defs)
    for field, vals in observed.items():
        if field not in defs or "enum" not in defs[field]:
            continue
        base_enum = set(defs[field]["enum"])
        merged = sorted(base_enum | vals)
        if merged != defs[field]["enum"]:
            defs[field] = {**defs[field], "enum": merged}
    return defs


def load_responses_from_manifest(collected_dir: Path, manifest_path: Path) -> dict[str, list]:
    """Load response bodies per operation from manifest."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_op: dict[str, list] = defaultdict(list)
    for run in manifest.get("runs", []):
        for pair in run.get("pairs", []):
            resp_path = collected_dir / pair["resp"]
            if resp_path.exists():
                try:
                    resp = json.loads(resp_path.read_text(encoding="utf-8"))
                    op = resp_path.parent.name
                    by_op[op].append(resp)
                except (json.JSONDecodeError, OSError):
                    pass
    return dict(by_op)


def _normalize_for_fingerprint(schema: dict) -> dict:
    """Strip descriptions and produce canonical structure for comparison."""
    if not schema or not isinstance(schema, dict):
        return schema
    out = {}
    for k, v in schema.items():
        if k == "description":
            continue
        if isinstance(v, dict):
            out[k] = _normalize_for_fingerprint(v)
        elif isinstance(v, list):
            out[k] = [_normalize_for_fingerprint(x) if isinstance(x, dict) else x for x in v]
        else:
            out[k] = v
    return out


def _fingerprint(schema: dict) -> str:
    """Canonical hash for structural equality."""
    norm = _normalize_for_fingerprint(schema)
    js = json.dumps(norm, sort_keys=True)
    return hashlib.sha256(js.encode()).hexdigest()[:12]


def _extract_defs_visit(schema: dict, defs: dict, fp_to_defname: dict, seen: set) -> None:
    """Recursively replace shared object schemas with $ref; populate defs."""
    if not schema or not isinstance(schema, dict):
        return
    if schema.get("type") == "object" and "properties" in schema:
        fp = _fingerprint(schema)
        if fp in fp_to_defname:
            # Already have a def; caller will replace this node
            return
        if fp in seen:
            # Second occurrence: create def from first, then replace
            defname = f"SharedObj_{fp}"
            fp_to_defname[fp] = defname
            if defname not in defs:
                defs[defname] = json.loads(json.dumps(schema))
            return
        seen.add(fp)
        for k, v in (schema.get("properties") or {}).items():
            _extract_defs_visit(v, defs, fp_to_defname, seen)
        return
    if schema.get("type") == "array" and "items" in schema:
        _extract_defs_visit(schema["items"], defs, fp_to_defname, seen)
        return
    if "anyOf" in schema:
        for sub in schema["anyOf"]:
            _extract_defs_visit(sub, defs, fp_to_defname, seen)
        return
    for k in ("properties", "items", "additionalProperties"):
        if k in schema and isinstance(schema[k], dict):
            _extract_defs_visit(schema[k], defs, fp_to_defname, seen)


def _replace_with_refs(schema: dict, defs: dict, fp_to_defname: dict, seen: set) -> dict:
    """Replace shared object schemas with $ref; return modified schema."""
    if not schema or not isinstance(schema, dict):
        return schema
    if schema.get("type") == "object" and "properties" in schema:
        fp = _fingerprint(schema)
        if fp in fp_to_defname:
            return {"$ref": f"#/$defs/{fp_to_defname[fp]}"}
        out = {"type": "object", "properties": {}}
        if "required" in schema:
            out["required"] = schema["required"]
        for k, v in (schema.get("properties") or {}).items():
            out["properties"][k] = _replace_with_refs(v, defs, fp_to_defname, seen)
        return out
    if schema.get("type") == "array" and "items" in schema:
        return {"type": "array", "items": _replace_with_refs(schema["items"], defs, fp_to_defname, seen)}
    if "anyOf" in schema:
        out = dict(schema)
        out["anyOf"] = [_replace_with_refs(s, defs, fp_to_defname, seen) for s in schema["anyOf"]]
        return out
    return dict(schema)


def extract_shared_defs(schemas: dict[str, dict]) -> tuple[dict, dict[str, dict]]:
    """
    Extract structurally identical object schemas to $defs.
    Returns (defs_dict, schemas_with_refs).
    Only extracts shapes that appear 2+ times.
    """
    defs: dict = {}
    fp_to_defname: dict = {}
    seen: set = set()
    # First pass: identify shared structures
    for op, schema in schemas.items():
        _extract_defs_visit(schema, defs, fp_to_defname, seen)
    # Recursively process defs themselves
    for defname, def_schema in list(defs.items()):
        _extract_defs_visit(def_schema, defs, fp_to_defname, seen)
    # Second pass: replace with $ref
    result = {}
    for op, schema in schemas.items():
        result[op] = _replace_with_refs(schema, defs, fp_to_defname, set())
    # Recursively replace refs inside defs
    for defname, def_schema in defs.items():
        defs[defname] = _replace_with_refs(def_schema, defs, fp_to_defname, set())
    return defs, result
