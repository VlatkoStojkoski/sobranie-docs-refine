"""
Widen request schemas to accept all known valid requests.
Used when validation fails: apply algorithmic fixes so schemas pass.
"""

import re
from typing import Any


OPTIONAL_FILTER_PARAMS = {
    "TypeId", "StatusId", "CommitteeId", "StatusGroupId", "MaterialTypeId",
    "DateFrom", "DateTo", "SessionId", "Number", "SearchText", "RegistrationNumber",
    "From", "To", "ResponsibleCommitteeId", "CoReportingCommittees", "OpinionCommittees",
    "ProcedureTypeId", "InitiatorTypeId", "EUCompatible", "genderId", "ageFrom", "ageTo",
    "politicalPartyId", "page", "rows", "coalition", "constituency",
    "StructureId", "structureId",
}

METHODNAME_VARIANTS = {
    "GetQuestionDetails": ["GetQuestionDetails", "/GetQuestionDetails"],
    "GetAllQuestions": ["GetAllQuestions", "/GetAllQuestions"],
    "GetAllQuestionStatuses": ["GetAllQuestionStatuses", "/GetAllQuestionStatuses"],
}


def _ensure_nullable(prop_schema: dict) -> dict:
    """Ensure property accepts null (anyOf [type, null])."""
    if "anyOf" in prop_schema:
        return prop_schema
    t = prop_schema.get("type")
    if isinstance(t, list) and "null" in t:
        return prop_schema
    if t == "null":
        return prop_schema
    return {"anyOf": [dict(prop_schema), {"type": "null"}]}


def _ensure_enum_includes(prop_schema: dict, value: Any) -> dict:
    """Ensure enum or const includes value."""
    if "const" in prop_schema:
        const = prop_schema["const"]
        if const == value:
            return prop_schema
        return {"type": "string", "enum": [const, value]}
    if "enum" in prop_schema:
        enum = list(prop_schema["enum"])
        if value not in enum:
            enum.append(value)
        return {**prop_schema, "enum": enum}
    return prop_schema


def _ensure_type_includes(prop_schema: dict, value_type: str) -> dict:
    """Ensure schema accepts value_type (e.g. integer when we have string)."""
    if value_type == "null":
        return _ensure_nullable(prop_schema)
    if "anyOf" in prop_schema:
        return prop_schema
    t = prop_schema.get("type")
    if isinstance(t, list):
        if value_type not in t:
            return {"anyOf": [prop_schema, {"type": value_type}]}
        return prop_schema
    if t == value_type:
        return prop_schema
    return {"anyOf": [dict(prop_schema), {"type": value_type}]}


def widen_for_validation_failure(
    schemas: dict[str, dict],
    failed: list[tuple[str, dict, str]],
    har_requests: dict[str, list],
    collected_requests: dict[str, list],
) -> dict[str, dict]:
    """
    Widen schemas based on validation failures.
    failed: [(op, req, error_message), ...]
    """
    import copy
    schemas = copy.deepcopy(schemas)

    for op, req, msg in failed:
        if op not in schemas:
            continue
        schema = schemas[op]
        props = schema.get("properties", {})

        if "is not of type" in msg or "is not valid under any of the given schemas" in msg:
            if "methodName" in msg or "was expected" in msg:
                method_val = req.get("methodName") or req.get("MethodName")
                if method_val and "methodName" in props:
                    props["methodName"] = _ensure_enum_includes(props["methodName"], method_val)
                if method_val and "MethodName" in props:
                    props["MethodName"] = _ensure_enum_includes(props["MethodName"], method_val)
            else:
                for key, val in req.items():
                    if key not in props:
                        continue
                    if val is None and key in OPTIONAL_FILTER_PARAMS:
                        props[key] = _ensure_nullable(props[key])
                    elif val is not None:
                        if key in ("StatusId", "TypeId", "MaterialTypeId", "StatusGroupId") and isinstance(val, int):
                            props[key] = {"anyOf": [{"type": "integer"}, {"type": "null"}]}
                        elif key in OPTIONAL_FILTER_PARAMS:
                            props[key] = _ensure_nullable(props[key])

        if "is not of type 'string'" in msg and "null" in msg:
            for key in OPTIONAL_FILTER_PARAMS:
                if key in props and key in req and req[key] is None:
                    props[key] = _ensure_nullable(props[key])
        if "is not of type 'integer'" in msg:
            for key in ("TypeId", "StatusId", "Page", "Rows", "CurrentPage"):
                if key in req and req[key] is None and key in props:
                    props[key] = _ensure_nullable(props[key])

    for op, variants in METHODNAME_VARIANTS.items():
        if op in schemas and "properties" in schemas[op]:
            for key in ("methodName", "MethodName"):
                if key in schemas[op]["properties"]:
                    s = schemas[op]["properties"][key]
                    for v in variants:
                        s = _ensure_enum_includes(s, v)
                    schemas[op]["properties"][key] = s

    return schemas


def widen_optional_filters(schemas: dict[str, dict]) -> dict[str, dict]:
    """Pre-emptively widen known optional filter params to accept null and remove from required."""
    import copy
    schemas = copy.deepcopy(schemas)
    for op, schema in schemas.items():
        props = schema.get("properties", {})
        required = schema.get("required")
        if required is not None:
            schema["required"] = [r for r in required if r not in OPTIONAL_FILTER_PARAMS]
        for key in OPTIONAL_FILTER_PARAMS:
            if key in props:
                props[key] = _ensure_nullable(props[key])
    return schemas
