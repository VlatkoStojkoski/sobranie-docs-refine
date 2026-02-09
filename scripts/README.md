# Scripts

## Improved Flow (Phases 0–5)

```bash
# Phase 0: Preparation (dirs, HAR, migration)
python scripts/phase0_prepare.py

# Phase 1–2: One-time setup (request schemas, generator config)
source .env  # or: set -a && source .env && set +a
python scripts/phase1_request_schemas.py
python scripts/phase2_generator_config.py

# Phase 3–5: Collection and schema output
python scripts/phase3_collect.py
python scripts/phase4_response_schemas.py

# Validation
python scripts/validate_schemas.py
```

## Legacy Pipeline

1. **collect.py** — Diverse API samples  
   - Listings with randomized filters (TypeId, StatusId, MaterialTypeId, etc.)  
   - Detail requests using IDs from listings; also GetAmendmentDetails, GetVotingResultsFor* when IDs available  
   - Output: `collected/YYYY-MM-DD_HH-MM-SS/*.json`  
   - Uses `.api_cache/`; `--no-cache` to bypass  
   - Logs: `logs/collect/YYYY-MM-DD_HH-MM-SS/collect.log`, `requests_responses.jsonl`

2. **infer_schema.py** — Schema from collected data  
   - Merges multiple samples per endpoint (union of shapes)  
   - Output: `schema_inference.json`, `docs/SCHEMA_INFERENCE_REPORT.md`  
   - Run after collect.py

3. **build_docs.py** — Build API_DOCS from inference  
   - Uses `schema_inference.json` (or archive fallback)  
   - Preserves $defs and Common patterns from existing API_DOCS  
   - Output: `docs/API_DOCS.md`

4. **enrich.py** — LLM analysis  
   - Per-operation schema context (no truncation)  
   - Multiple samples, $defs, Common patterns, schema_inference in prompt  
   - Output: `docs/ENRICHMENT_REPORT.md`  
   - Logs: `logs/enrich/YYYY-MM-DD_HH-MM-SS/prompt_*.txt`, `response_*.txt`

5. **generate_openapi.py** — OpenAPI from docs  
   - Single LLM call: `docs/API_DOCS.md` → `docs/openapi.yaml`  
   - Logs: `logs/generate_openapi/YYYY-MM-DD_HH-MM-SS/prompt.txt`, `response.txt`

## One-time

- **build_docs_from_archive.py** — Legacy: build from archive only

## Cache

- **cache.py** — File-based cache (key: SHA256 of url + payload). Used by collect.py.

## Env

`ANTHROPIC_API_KEY` for enrich.py and generate_openapi.py.
