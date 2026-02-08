# Sobranie API Documentation

> API docs for the North Macedonian Parliament (Собрание на Р. Северна Македонија) at [sobranie.mk](https://www.sobranie.mk).

## What this is

This repo documents the **unofficial, undocumented** backend API used by the sobranie.mk website. The API is an RPC-style gateway: most endpoints route through a single POST handler (`/Routing/MakePostRequest`) with a `methodName` parameter that selects the actual operation.

The docs are reverse-engineered from:
- HAR (HTTP Archive) captures of live website traffic
- Direct API probing with diverse parameters
- LLM-assisted schema analysis against our documentation

## Key artifacts

| File | Description |
|------|-------------|
| **`openapi.yaml`** | OpenAPI 3.0 spec — standardized docs for Swagger UI, codegen, tooling. Synced from collected responses |
| **`API.md`** | Main reference — request/response schemas for 35+ endpoints, reusable `$defs`, common patterns |
| **`API_DOC_FROM_DATA.md`** | Machine-generated from `schema_inference.json`; use to keep API.md consistent |
| **`schema_inference.json`** | Data-driven schema inference from `collected_responses/` |
| **`HAR_ANALYSIS_FINDINGS.md`** | 42 unique endpoints discovered from HAR capture (deduplicated). Structured notes per endpoint |
| **`API_ANALYSIS_FINDINGS_NEW_ROUTES.md`** | Schema validation of new routes (questions, councils, committees, parties, groups, MPs clubs, voting). [DEVIATION], [UNDOCUMENTED], [NEW_ENUM] findings |
| **`API_EXPLORATION_FINDINGS.md`** | Open-ended LLM exploration across sittings, materials, calendar, MPs |
| **`new_endpoints_responses.json`** | Raw responses from initial probe of newly discovered endpoints |

## API overview

- **Base URL (standard):** `https://www.sobranie.mk/Routing/MakePostRequest`
- **Method:** POST
- **Body:** JSON with `methodName`, `languageId`, and endpoint-specific params
- **Date format:** Microsoft JSON `/Date(timestamp)/` (milliseconds since epoch)
- **Languages:** 1 = Macedonian, 2 = Albanian, 3 = Turkish

### OpenAPI / Swagger

Use `openapi.yaml` for:
- **Swagger UI:** `npx swagger-ui-watcher openapi.yaml` or paste into [editor.swagger.io](https://editor.swagger.io)
- **Codegen:** OpenAPI Generator, Postman import, etc.
- **Verification:** `python scripts/verify_openapi.py` — hits live API, validates all 36 endpoints and schemas

### Coverage

**Core:** Sittings, materials, agendas, committees, structures, political parties, MPs, voting results  
**Parliamentary questions:** GetAllQuestions, GetQuestionDetails, GetAllQuestionStatuses  
**Councils & groups:** GetAllCouncils, GetCouncilDetails, GetAllParliamentaryGroups, GetAllMPsClubsByStructure  
**Non-standard:** `GetCustomEventsCalendar` (ASMX), `LoadLanguage` (Infrastructure), `GetOfficialVisitsForUser` (ASMX)

## Workflow

**Data-driven pipeline (recommended for doc accuracy):**
```
collect_all_responses.py  →  collected_responses/  (raw API calls)
       ↓
infer_schema.py          →  schema_inference.json, SCHEMA_INFERENCE_REPORT.md
       ↓
sync_docs.py             →  openapi.yaml, API_DOC_FROM_DATA.md
       ↓
verify_openapi.py        →  validates against live API
```

**Legacy / exploratory:**
```
HAR capture (browser)  →  analyze_har.py  →  HAR_ANALYSIS_FINDINGS.md
probe_new_endpoints.py  →  new_endpoints_responses.json
analyze_new_routes.py  →  API_ANALYSIS_FINDINGS_NEW_ROUTES.md  →  API.md (enrichment)
```

1. **Discovery:** Capture traffic from sobranie.mk in browser DevTools → export HAR
2. **HAR analysis:** `analyze_har.py` runs two-level LLM filtering, produces structured endpoint notes
3. **Probing:** `probe_new_endpoints.py` hits new endpoints with real params, saves responses
4. **Documentation:** Responses inform `API.md` schemas
5. **Enrichment:** `analyze_new_routes.py` compares live responses to docs, flags gaps

## Results summary

- **HAR:** 821 entries → 633 passed pre-filter → 42 unique endpoints after deduplication
- **API.md:** 35+ endpoints with request examples, response schemas, notes
- **Schema validation:** 22 new-route analyses; multiple [UNDOCUMENTED] fields (e.g. GetPoliticalPartyDetails.Members, GetParliamentaryGroupDetails amendments/questions) and [NEW_ENUM] values (RoleId, StatusId, etc.)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...  # for LLM-based scripts
```

## Scripts

| Script | Purpose |
|--------|---------|
| **`collect_all_responses.py`** | Call all endpoints with diverse params → `collected_responses/` |
| **`infer_schema.py`** | Infer JSON schema from collected data → `schema_inference.json` |
| **`sync_docs.py`** | Sync `openapi.yaml` and generate `API_DOC_FROM_DATA.md` from inference |
| **`verify_openapi.py`** | Validate `openapi.yaml` against live API |
| `analyze_har.py` | Parse HAR file(s), two-level LLM analysis → `HAR_ANALYSIS_FINDINGS.md` |
| `probe_new_endpoints.py` | Call newly discovered endpoints, save responses → `new_endpoints_responses.json` |
| `analyze_new_routes.py` | Validate new routes against API.md → `API_ANALYSIS_FINDINGS_NEW_ROUTES.md` |
| `analyze_sittings.py` | GetSittingDetails schema analysis → `API_ANALYSIS_FINDINGS.md` |
| `analyze_materials_diverse.py` | GetMaterialDetails across filters → `API_ANALYSIS_FINDINGS_MATERIALS.md` |
| `explore_api.py` | Broad exploration across all endpoints → `API_EXPLORATION_FINDINGS.md` |
| `discover_outliers.py` | Programmatic validation (no LLM) → `API_OUTLIER_FINDINGS.md` |
| `deduplicate_har_findings.py` | Remove duplicate entries from `HAR_ANALYSIS_FINDINGS.md` |

See `scripts/README.md` for detailed usage and env vars.

## License

Documentation only. The sobranie.mk API and data belong to the Assembly of the Republic of North Macedonia.
