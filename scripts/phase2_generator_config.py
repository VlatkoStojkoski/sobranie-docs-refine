#!/usr/bin/env python3
"""
Phase 2: Generator config from request schemas + taxonomy via LLM.

Run: python scripts/phase2_generator_config.py
Env: ANTHROPIC_API_KEY or OPENAI_API_KEY
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONFIG = ROOT / "config"
DOCS = ROOT / "docs"
DATA = ROOT / "data"


def main():
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    from improved.llm import complete_json

    print("Phase 2: Generator config")

    schemas_path = CONFIG / "request_schemas.json"
    if not schemas_path.exists():
        print("ERROR: Run phase1 first. config/request_schemas.json not found.")
        return 1

    meta_path = CONFIG / "generator_meta_schema.json"
    if not meta_path.exists():
        print("ERROR: config/generator_meta_schema.json not found.")
        return 1

    schemas_data = json.loads(schemas_path.read_text(encoding="utf-8"))
    schemas = schemas_data.get("schemas", schemas_data)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    api_index = (DOCS / "API_INDEX.md").read_text(encoding="utf-8") if (DOCS / "API_INDEX.md").exists() else ""
    enrichment = {}
    if (DATA / "enrichment.json").exists():
        enrichment = json.loads((DATA / "enrichment.json").read_text(encoding="utf-8"))

    prompt = f"""Produce a generator config for API request body generation.

## Meta-schema (output must validate against this):
{json.dumps(meta, indent=2)}

## Request schemas (per operation):
{json.dumps(schemas, indent=2)[:30000]}

## API_INDEX taxonomy (catalogs, listings, details, non-standard):
{api_index[:4000]}

## Task
For each operation in request_schemas, define:
- type: "listing" | "detail" | "other"
  - listing: paginated/filterable, can provide IDs for detail ops
  - detail: needs IDs from listing ops; set id_source: {{ "operation": "GetAllSittings", "field": "Id" }}
  - other: catalogs, LoadLanguage, GetCustomEventsCalendar, etc.
- sample_size: optional override (default 5)
- url: for non-standard only (GetCustomEventsCalendar, LoadLanguage, GetOfficialVisitsForUser)
- fields: map param name -> {{ generator, ... }}
  - generator "constant": use "value"
  - generator "enum": use "values" [1,2,3] or "source": "catalog" operation
  - generator "range": use "min", "max" for integers
  - generator "uuid_from_listing": for detail ops, ID comes from id_source
  - generator "catalog": "source": "GetAllStructuresForFilter", "field": "Id"
  - generator "constant_or_null": "value" or null

StructureId: use catalog GetAllStructuresForFilter, field Id. languageId: enum [1,2,3].

Output JSON (no other text):
{{ "sample_size_default": 5, "operations": {{ "OpName": {{ "type": "...", "fields": {{}} }}, ... }} }}"""

    print("1. LLM: producing generator config...")
    out = complete_json(prompt)

    print("2. Validating against meta-schema...")
    try:
        import jsonschema
        jsonschema.validate(out, meta)
    except ImportError:
        pass
    except jsonschema.ValidationError as e:
        print(f"   WARN: Validation error: {e.message}")

    (CONFIG / "generators.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   Saved config/generators.json ({len(out.get('operations', {}))} operations)")
    return 0


if __name__ == "__main__":
    exit(main())
