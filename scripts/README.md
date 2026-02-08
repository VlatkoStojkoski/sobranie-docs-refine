# Scripts

## Pipeline

1. **collect.py** — Diverse API samples  
   - Listings with randomized filters (TypeId, StatusId, MaterialTypeId, etc.)  
   - Detail requests using IDs from listings  
   - Output: `collected/YYYY-MM-DD_HH-MM-SS/*.json`  
   - Uses `.api_cache/` for request/response caching; use `--no-cache` to bypass  
   - Logs: `logs/collect/YYYY-MM-DD_HH-MM-SS/collect.log`, `requests_responses.jsonl`

2. **enrich.py** — LLM analysis  
   - For each operation: compare sample response to `docs/API_DOCS.md`  
   - Output: `docs/ENRICHMENT_REPORT.md`  
   - Logs: `logs/enrich/YYYY-MM-DD_HH-MM-SS/prompt_*.txt`, `response_*.txt`  
   - Use the report to prompt an assistant to update docs

3. **generate_openapi.py** — OpenAPI from docs  
   - Single LLM call: `docs/API_DOCS.md` → `docs/openapi.yaml`  
   - Logs: `logs/generate_openapi/YYYY-MM-DD_HH-MM-SS/prompt.txt`, `response.txt`

## One-time

- **build_docs_from_archive.py** — Build `docs/API_DOCS.md` from `archive/schema_inference.json`

## Cache

- **cache.py** — File-based cache for API requests (key: SHA256 of url + payload).  
- Used by `collect.py`; responses stored in `.api_cache/*.json`.

## Env

`ANTHROPIC_API_KEY` for enrich.py and generate_openapi.py.
