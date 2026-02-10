# Scripts

Utility scripts for API discovery and analysis.

## Requirements

```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=...
```

## Scripts

### `analyze_sittings.py`

Fetches 50 sittings from `GetAllSittings` (mixed TypeId, date diversity), fetches `GetSittingDetails` for each, and uses Claude to analyze responses against the documented schema in `API.md`. Outputs findings to `API_ANALYSIS_FINDINGS.md` in the project root.

**Usage:**
```bash
python scripts/analyze_sittings.py
```

**Env:**
- `ANTHROPIC_API_KEY` (required)
- `ANALYZE_LIMIT` (optional) — e.g. `5` to analyze only 5 sittings for testing

---

### `analyze_sittings_diverse.py`

Same as `analyze_sittings.py` but samples sittings across all filter dimensions: equal amounts of TypeId 1 (plenary) and TypeId 2 (committee), spread across StatusId 1–6, and across different committees. Intended to surface edge cases and format variations that may only appear with specific filter combinations.

**Usage:**
```bash
python scripts/analyze_sittings_diverse.py
```

**Output:** `API_ANALYSIS_FINDINGS_DIVERSE.md` in the project root.

**Env:**
- `ANTHROPIC_API_KEY` (required)
- `ANALYZE_LIMIT` (optional) — cap total sittings analyzed for testing

---

### `analyze_materials_diverse.py`

Fetches materials from `GetAllMaterialsForPublicPortal` across diverse filters (StatusGroupId, MaterialTypeId, ProcedureTypeId, InitiatorTypeId, ResponsibleCommitteeId), fetches `GetMaterialDetails` for each, and uses Claude to analyze responses against the documented schema. Outputs findings to `API_ANALYSIS_FINDINGS_MATERIALS.md` in the project root.

**Usage:**
```bash
python scripts/analyze_materials_diverse.py
```

**Output:** `API_ANALYSIS_FINDINGS_MATERIALS.md` in the project root.

**Env:**
- `ANTHROPIC_API_KEY` (required)
- `ANALYZE_LIMIT` (optional) — cap total materials analyzed for testing

---

### `explore_api.py`

Systematic LLM exploration across **all documentable endpoints**. Covers:

- **Detail:** GetSittingDetails, GetMaterialDetails (diverse TypeId, StatusId, CommitteeId, material filters)
- **List:** GetAllSittings, GetAllMaterialsForPublicPortal (filter combos), GetMonthlyAgenda (different months), GetParliamentMPsNoImage (pagination, filters, different StructureId)
- **Calendar:** GetCustomEventsCalendar (different URL, different months)
- **Catalogs:** Single batch of all reference endpoints (GetAllGenders, GetAllStructuresForFilter, etc.)

Each response is sent to Claude with an open-ended prompt. Endpoint-type hints (detail vs list vs catalog) help the LLM focus. Output is collected for manual analysis and doc enrichment.

**Usage:**
```bash
python scripts/explore_api.py
```

**Output:** `API_EXPLORATION_FINDINGS.md` in the project root.

**Env:**
- `ANTHROPIC_API_KEY` (required)
- `EXPLORE_LIMIT` (optional) — cap total tasks (e.g. `10` for quick test)

---

### `analyze_new_routes.py`

Analyzes new API routes (questions, councils, committees, parties, groups, MPs clubs, voting) against the documented schema in `API.md`. Follows the same pattern as `analyze_sittings.py` and `analyze_materials_diverse.py`:

- **Catalogs**: GetAllQuestionStatuses, GetAllInstitutionsForFilter, GetAllApplicationTypes, GetAllCouncils, GetAllParliamentaryGroups, GetAllMPsClubsByStructure
- **List**: GetAllQuestions (diverse StatusId)
- **Details**: GetQuestionDetails, GetCouncilDetails, GetCommitteeDetails, GetPoliticalPartyDetails, GetParliamentaryGroupDetails, GetMPsClubDetails, GetVotingResultsForSitting

Uses Claude to compare responses against `API.md` and outputs [DEVIATION], [UNDOCUMENTED], [NEW_ENUM], [INTERESTING] findings.

**Usage:**
```bash
python scripts/analyze_new_routes.py
```

**Output:** `API_ANALYSIS_FINDINGS_NEW_ROUTES.md` in the project root.

**Env:**
- `ANTHROPIC_API_KEY` (required)
- `ANALYZE_LIMIT` (optional) — cap total tasks for testing (e.g. `5`)

---

### Data collection and schema inference pipeline

| Script | Purpose |
|--------|---------|
| **`collect_all_responses.py`** | Call ALL endpoints with diverse parameters; save raw responses to `collected_responses/YYYY-MM-DD_HH-MM-SS/` |
| **`infer_schema.py`** | Infer JSON schema from collected responses (data-driven, no guessing). Outputs `schema_inference.json` and `SCHEMA_INFERENCE_REPORT.md` |
| **`sync_docs.py`** | Sync `openapi.yaml` and generate `API_DOC_FROM_DATA.md` from schema inference + collected samples |
| **`enrich_api_md_from_data.py`** | Optional: LLM compares API_DOC_FROM_DATA vs API.md, outputs `API_ENRICHMENT_REPORT.md` with suggested updates |

**Pipeline:**
```bash
python scripts/collect_all_responses.py   # ~2 min, hits live API
python scripts/infer_schema.py           # Infers schema from collected data
python scripts/sync_docs.py              # Updates openapi.yaml, generates API_DOC_FROM_DATA.md
python scripts/verify_openapi.py         # Validates spec against live API
```

Use `API_DOC_FROM_DATA.md` to update `API.md`; keep both consistent with `openapi.yaml`.

---

### `discover_outliers.py`

Programmatic schema validation and outlier detection — **no Claude required**. Fetches many sittings and materials, validates responses against documented types and enums, collects all unique ID values seen, and reports:

1. **Undocumented enum values** — IDs seen in API but not in our $defs
2. **Schema violations** — type mismatches, invalid UUIDs
3. **ProposerTypeTitle values** — all values seen (may exceed GetProposerTypes)
4. **TerminationStatusTitle values** — for closed materials
5. **Frequently empty arrays** — which paths are often empty
6. **Filter coverage** — which StatusGroupId/MaterialTypeId filters return 0 results
7. **Null rates** — which fields are often null

**Usage:**
```bash
python scripts/discover_outliers.py
```

**Output:** `API_OUTLIER_FINDINGS.md` in the project root.

**Env:**
- `OUTLIER_SITTINGS_LIMIT` (optional) — cap sittings fetched (default 80)
- `OUTLIER_MATERIALS_LIMIT` (optional) — cap materials fetched (default 80)

---

### `analyze_har.py`

Two-level LLM analysis of HAR (HTTP Archive) captures for API discovery:

1. **Pre-filter** (no LLM): Skips obvious static/tracking URLs (.js, .css, images, analytics).
2. **Level 1** (minimal tokens): Per-request relevance check — URL, method, status, tiny req/res snippets. Filters out remaining noise.
3. **Level 2** (detailed): Full sanitized req/res analysis for each relevant request. Outputs structured notes: route type, method name, params, response structure, documentation suggestions.

Surfaces new methods, non-standard routes (e.g. .asmx), document/media URLs, and enrichable patterns.

**Usage:**
```bash
# Single HAR file
python scripts/analyze_har.py path/to/capture.har

# Multiple files or directory
python scripts/analyze_har.py path/to/*.har
python scripts/analyze_har.py path/to/dir/
```

**Output:** `HAR_ANALYSIS_FINDINGS.md` in the project root.

**Env:**
- `ANTHROPIC_API_KEY` (required)
- `HAR_ANALYZE_LIMIT` (optional) — cap entries analyzed (e.g. `50` for testing)
- `HAR_SKIP_PREFILTER` (optional) — set to `1` to skip pre-filter and run all through Level 1
- `HAR_DRY_RUN` (optional) — set to `1` to load HAR and print sample entries without LLM calls (no API key needed)
- `HAR_USE_STRUCTURED_OUTPUT` (optional) — set to `0` to disable structured output; uses XML-style prompts (default 1)
- `HAR_MODEL` (optional) — model for structured output (default `claude-sonnet-4-5`). Must support structured output per [Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs).
- `HAR_MODEL_FALLBACK` (optional) — model when structured output disabled (default `claude-sonnet-4-20250514`)
- `HAR_CONCURRENCY` (optional) — parallel requests per batch (default 5)
- `HAR_BATCH_DELAY` (optional) — seconds between batches (default 0.5)

**Logs:** Each run creates `har_analysis_logs/YYYY-MM-DD_HH-MM-SS/` with:
- `level1_NNNN_prompt.txt`, `level1_NNNN_meta.json`, `level1_NNNN_response.txt`
- `level2_NNNN_prompt.txt`, `level2_NNNN_meta.json`, `level2_NNNN_response.txt`
- `index.json`, `run_summary.json`
