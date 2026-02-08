# Scripts

## Pipeline

1. **collect.py** — Diverse API samples  
   - Listings with randomized filters (TypeId, StatusId, MaterialTypeId, etc.)  
   - Detail requests using IDs from listings  
   - Output: `collected/YYYY-MM-DD_HH-MM-SS/*.json`

2. **enrich.py** — LLM analysis  
   - For each operation: compare sample response to `docs/API_DOCS.md`  
   - Output: `docs/ENRICHMENT_REPORT.md`  
   - Use the report to prompt an assistant to update docs

3. **generate_openapi.py** — OpenAPI from docs  
   - Single LLM call: `docs/API_DOCS.md` → `docs/openapi.yaml`

## One-time

- **build_docs_from_archive.py** — Build `docs/API_DOCS.md` from `archive/schema_inference.json`

## Env

`ANTHROPIC_API_KEY` for enrich.py and generate_openapi.py.
