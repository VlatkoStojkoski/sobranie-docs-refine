# Improved API Documentation Flow

> Machine-readable request and response schemas via HAR + enrichment, config-driven collection, and algorithmic inference with LLM refinement.

## Overview

This flow replaces the current collect → infer_schema → build_docs → enrich pipeline. It is designed for **precision** (schemas validate all collected bodies), **maintainability** (config-driven, not hardcoded), and **one-time setup** (Phases 1–2 are run once; normal runs start from Phase 3).

**Phases:**
- **Phase 0:** Preparation — aggregate existing data, locate HAR
- **Phase 1:** Request schemas — HAR + enrichment + LLM → validated request schemas
- **Phase 2:** Generator config — LLM produces config from schemas + taxonomy
- **Phase 3:** Collection — send requests, save req/resp, errors, listing cache
- **Phase 4:** Response schemas — algorithmic inference + LLM refinement → final schemas
- **Phase 5:** Output — one combined schema file

**Typical usage:** Run Phase 1–2 once. Thereafter, run Phase 3 → 4 → 5 (or 3 → 4 only if output format unchanged).

---

## Decision Log

| # | Decision | Choice |
|---|----------|--------|
| 1 | Schema format | JSON Schema (OpenAPI 3.1 compatible); supports anyOf, $ref, merging |
| 2 | Output layout | One combined file; separate `requests` and `responses` top-level keys |
| 3 | Human docs | None; machine-readable schemas only |
| 4 | Exact schemas | Narrowest schema validating every collected body; LLM for enum/descriptions |
| 5 | Type conflicts | Use anyOf/union |
| 6 | Empty arrays | Use schema from non-empty samples (same field path, across samples); merge all non-empty |
| 7 | Shared types | Infer $defs from structurally identical shapes; LLM for enum vs string |
| 8 | Required | Infer from "field present in all samples" |
| 9 | File layout | Per-operation: `{operation}/req_001.json`, `resp_001.json` |
| 10 | Req–resp pairing | Explicit manifest with linkage |
| 11 | Error responses | Save in `errors/`, link to req, exclude from schema |
| 12 | Truncation | None; full bodies for inference |
| 13 | Run behavior | Append into same directory with versioning |
| 14 | Config format | JSON validated by JSON Schema meta-schema; minimal custom generator vocab |
| 15 | Operation taxonomy | listing | detail | other (in config) |
| 16 | Type taxonomy | OpenAPI-compatible types; enums via LLM |
| 17 | ID sourcing | Always from listing responses; persist listing cache (index + per-file) |
| 18 | Non-listing-detail | mini-schema + generators; first-class in config |
| 19 | Sample size | Global default + per-operation overrides |
| 20 | HAR | Assumed at `data/session.har`; single session |
| 21 | Enrichment | JSON; LLM helps create initial request config from archives |
| 22 | Validation | Algorithmic (existing validator) |
| 23 | Ops not in HAR | Use docs + archive as alternative source |
| 24 | Scope | All known operations |
| 25 | Migration | Reuse collected/, schema_inference, docs, archive |
| 26 | Phasing | Single monolithic doc; focus on simplicity |
| 27 | Tools | Python; Anthropic Claude |
| 28 | Non-standard endpoints | First-class; own config (GetCustomEventsCalendar, LoadLanguage, GetOfficialVisitsForUser) |
| 29 | Routing | MakePostRequest + methodName; three non-standard URLs |
| 30 | languageId, StructureId | Enums from catalogs (fetched at runtime) |

---

## Phase 5: Output

### Result
One file: `schemas/api.json` (or configurable path).

### Structure
```json
{
  "$defs": {
    "AspDate": { "type": "string", "pattern": "^/Date\\(\\d+\\)/$" },
    "Author": { "type": "object", "properties": { "Id": {...}, "FirstName": {...}, "LastName": {...} } }
  },
  "requests": {
    "GetAllSittings": { "$ref": "#/$defs/GetAllSittingsRequest", "description": "..." },
    "GetMaterialDetails": { ... }
  },
  "responses": {
    "GetAllSittings": { "type": "object", "properties": { "TotalItems": {...}, "Items": {...} } },
    ...
  }
}
```

### Format
- JSON Schema draft 2020-12 / OpenAPI 3.1 compatible
- Shared types in `$defs`; requests/responses use `$ref` where applicable
- No markdown, no human-oriented docs

### Dependencies
- Phase 4 complete (request schemas + response schemas ready)

---

## Phase 4: Response Schemas (Algorithmic + LLM)

### Input
- `collected/{operation}/req_*.json`, `resp_*.json` (successful pairs only)
- Manifest linking req ↔ resp
- Errors excluded

### Steps

1. **Load all successful response bodies** from manifest.
2. **Algorithmic inference**
   - For each operation, merge all response bodies into one schema:
     - Infer types from values (string, integer, number, boolean, null, object, array)
     - Detect asp-date (pattern), uuid (format)
     - Same field, different types → `anyOf: [typeA, typeB]` or `anyOf: [type, {"type":"null"}]`
     - Empty arrays: if any sample has non-empty array for that path, use schema from non-empty samples; merge across all non-empty
     - Required: field present in all samples → add to `required`
     - No truncation; use full bodies
   - Structurally identical object shapes → extract to `$defs`, replace with `$ref`
     - "Identical" = same keys, same value types (recursive)
   - Append-only merge when re-running (never narrow)
3. **LLM refinement**
   - Input: inferred schema per operation
   - Tasks: enum vs string/int discernment; add descriptions for schema values
   - Output: refined schema (structured output, JSON)
   - Model: Anthropic Claude
4. **Combine** request schemas (from Phase 1) + refined response schemas + $defs → Phase 5 output.

### Output
- Feeds Phase 5

### Notes
- Response schemas are algorithmically inferred; LLM only refines (enum, descriptions).
- Reuse existing inference logic from `infer_schema.py` where possible; extend for anyOf, required, $defs extraction.

---

## Phase 3: Collection

### Input
- Generator config (Phase 2)
- Listing cache (if exists; for optional skip/reuse)

### Steps

1. **Resolve catalog enums**
   - Run catalog operations first (GetAllCommitteesForFilter, GetAllStructuresForFilter, GetAllPoliticalParties, etc.)
   - Extract IDs and store in listing cache
   - Use for `languageId`, `StructureId`, `CommitteeId`, etc. in generators
2. **Generate request bodies** per operation from config:
   - Use sample size (global default + per-operation override)
   - For listing ops: randomize filters, use catalog IDs where configured
   - For detail ops: use IDs from listing responses (or listing cache)
   - For other ops: use mini-schema + generators
3. **Send requests**
   - MakePostRequest for standard ops; dedicated URLs for GetCustomEventsCalendar, LoadLanguage, GetOfficialVisitsForUser
   - No truncation; save full response
4. **Save**
   - Success: `collected/{operation}/req_001.json`, `collected/{operation}/resp_001.json`
   - Error: `errors/{operation}/err_001.json`; link req → error in manifest
5. **Listing cache**
   - Index file: `listing_cache/index.json` — maps operation + run → path to cache file
   - Per-file: `listing_cache/{run_id}_{operation}.json` — request, response, extracted_ids, item_count
   - Separate from req/resp storage; used for logging and optional skip of listing phase
6. **Manifest**
   - `collected/manifest.json`: run_id, pairs (req path, resp path), version
   - `collected/errors_manifest.json`: req path → error path (separate from success linkage)

### File Layout
```
collected/
  manifest.json
  errors_manifest.json
  GetAllSittings/
    req_001.json
    resp_001.json
  GetMaterialDetails/
    req_001.json
    resp_001.json
errors/
  GetAllSittings/
    err_001.json
listing_cache/
  index.json
  2026-02-08_12-00-00_GetAllCommitteesForFilter.json
  2026-02-08_12-00-00_GetAllSittings.json
```

### Versioning
- Append new req/resp with monotonic IDs
- Each run has run_id (timestamp)
- Manifest records which pairs belong to which run

### Dependencies
- Phase 2 config
- Live API (or cache for idempotency)

---

## Phase 2: Generator Config

### Input
- Request schemas (Phase 1)
- Operation taxonomy (listing | detail | other)
- Enrichment / archive data (for context)

### Steps
1. **LLM step**
   - Input: request schemas, taxonomy, list of all operations, enrichment/archive excerpts
   - Output: generator config (JSON)
   - Config includes: operation type, sample size overrides, field generators per operation
2. **Validate** config against meta-schema
3. **Persist** config to `config/generators.json`

### Config Schema (Meta-schema)
- JSON Schema validates structure
- Top-level: `sample_size_default`, `operations`
- Per-operation: `type` (listing | detail | other), `sample_size`?, `fields` (or `request_schema` ref for complex)
- Field generators: minimal custom vocab, e.g.:
  - `{"generator": "range", "min": 1, "max": 10}` for integers
  - `{"generator": "enum", "values": [1, 2]}` or `{"generator": "catalog", "source": "GetAllCommitteesForFilter", "field": "Id"}`
  - `{"generator": "constant", "value": "..."}` 
  - `{"generator": "uuid"}` for IDs from listing
- Non-standard endpoints: `url`, `request_structure` with generators

### Dependencies
- Phase 1 complete

---

## Phase 1: Request Schemas

### Input
- `data/session.har`
- Enrichment data (aggregated from docs, archive, collected)
- Existing collected request bodies (for validation)

### Steps
1. **Build enrichment file** (LLM-assisted)
   - Scan: `docs/`, `archive/`, `collected/`, `schema_inference.json`
   - Aggregate into structured JSON (by source, by operation)
   - LLM helps structure and create initial request config based on archives
   - Output: `data/enrichment.json`
2. **Extract requests from HAR**
   - Parse HAR, filter for Sobranie API URLs
   - Extract request bodies (POST payloads)
   - Group by operation (methodName or URL)
3. **LLM: request schemas**
   - Input: HAR requests + enrichment.json + existing collected requests
   - Task: produce JSON Schema for each operation’s request body
   - Output: validated JSON Schema (structured output)
   - Combine HAR + messy data; use LLM for synthesis
4. **Validate**
   - Use existing JSON Schema validator (e.g. `jsonschema` lib)
   - Ensure every known good request body (from collected + HAR) validates
   - If none exist yet: validate against HAR-extracted requests only
5. **Persist** request schemas for Phase 2 and Phase 5

### Enrichment File Structure (data/enrichment.json)
```json
{
  "sources": ["docs/API_DOCS.md", "archive/API.md", "collected/..."],
  "by_operation": {
    "GetAllSittings": {
      "request_notes": "...",
      "response_notes": "...",
      "excerpts": ["..."]
    }
  }
}
```
(Exact shape can be refined; this is the logical structure.)

### Dependencies
- HAR at `data/session.har`
- Docs, archive, collected (for enrichment)
- LLM (Anthropic Claude)

---

## Phase 0: Preparation

### Steps
1. **Ensure HAR exists** at `data/session.har`
2. **Ensure directories exist**: `data/`, `collected/`, `errors/`, `listing_cache/`, `config/`, `schemas/`
3. **Scan docs and archive** for all documentation files
   - `docs/*.md`, `archive/**/*.md`, etc.
   - Used for enrichment and ops-not-in-HAR fallback
4. **Migrate / reuse**
   - Reuse `collected/`, `schema_inference.json`, docs, archive
   - Convert existing collected format if needed (single-file-per-method → per-operation req/resp split)
   - Script: one-time migration from `collected/YYYY-MM-DD/*.json` to `collected/{operation}/req_*.json` + manifest

### Migration Script (One-time)
- Read existing `collected/**/*.json` (method + samples)
- For each sample: write `req_N.json`, `resp_N.json` under `collected/{operation}/`
- Build manifest with req ↔ resp linkage
- Preserve run metadata

---

## File Reference

| Path | Purpose |
|------|---------|
| `data/session.har` | HAR capture (single session) |
| `data/enrichment.json` | Aggregated findings; LLM input for request config |
| `config/generators.json` | Generator config (Phase 2 output) |
| `collected/manifest.json` | Req ↔ resp linkage, run versioning |
| `collected/errors_manifest.json` | Req → error linkage |
| `collected/{operation}/req_*.json` | Request bodies |
| `collected/{operation}/resp_*.json` | Response bodies (success) |
| `errors/{operation}/err_*.json` | Error responses |
| `listing_cache/index.json` | Index of listing cache files |
| `listing_cache/{run}_{operation}.json` | Listing request, response, extracted_ids, item_count |
| `schemas/api.json` | Final output: $defs, requests, responses |

---

## Execution Order

**One-time:**
```
Phase 0 → Phase 1 → Phase 2
```

**Normal run:**
```
Phase 3 → Phase 4 → Phase 5
```

**Full run (e.g. config changed):**
```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
```

---

## Implementation Notes

1. **Simplicity first** — Prefer small, focused scripts over monolithic ones.
2. **Reuse** — Adapt `infer_schema.py`, `collect.py`, `cache.py` where it reduces effort.
3. **No truncation** — Remove truncation from collection; store full bodies.
4. **LLM structured output** — Use Claude structured output for deterministic schema/config output.
5. **Validation** — Use `jsonschema` (Python) for schema validation.
6. **Catalog fetch** — Run catalog ops at start of Phase 3; persist to listing cache for optional reuse.
7. **Non-standard endpoints** — Explicit entries in generator config with URL and request structure.
