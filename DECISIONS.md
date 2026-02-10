# Sobranie API documentation — decisions

All rationale and decisions from development. Single source of truth for why things work the way they do.

---

## Goal: procedural doc improvement from req/res pairs

The project procedurally improves API documentation by collecting real request/response pairs and using an LLM to refine the docs based on what the API actually returns.

**Pipeline:**

1. **Collect** — Generate requests from `config/generators.json`, send to the live API, save req/res pairs to `collected/<Operation>/`.
2. **Refine** — For each collected pair:
   - **Notes step:** LLM receives current op md + global md + the req/res pair. Returns concise notes on what the docs should add or update. Saved to `logs/refine/<run_id>/notes/`.
   - **Apply step:** Every `batch_size` notes (configurable), LLM receives current op md + global md + batched notes. Returns `newOperationMd`, `newGlobalMd`, and optionally `seriousConcerns`. Docs are overwritten immediately.
   - **Rebuild:** `docs/API.md` is regenerated from global + ops after every successful apply.
3. **Resume** — Progress tracked in `logs/refine/<run_id>/state.json`. Stop anytime; `--resume <run_id>` to continue.

**Principles:**

- No info lost from previous iterations. New docs only refine.
- Only widen, never narrow: add enum values, add anyOf with null, add optional properties, add union types. Never remove values, never make optional fields required, never drop anyOf branches.
- Docs must validate every request/response body that has previously been used to improve them.
- Improving = more accurate and precise, not necessarily longer. Simplify when possible.
- Clear separation: global has conventions, $defs, common patterns; ops have request/response schemas and op-specific notes.
- Enum values defined in global `$defs` only; op docs reference via `$ref`.

---

## Data quality and diversification

From analysis of collected data:

- **Success rate**: ~80% (345 successes vs 84 errors).
- **Low quality** (among successes): ~30 empty responses (TotalItems:0, Items:[], d:[]).
- **Duplicates**: Many pairs share identical requests (e.g. same languageId) and identical responses. Pure catalogs (GetAllGenders, GetAllApplicationTypes, LoadLanguage) yield redundant samples.
- **Macedonian only**: Use `languageId`/`LanguageId` = 1 (Macedonian) everywhere. No Albanian/Turkish variants.
- **Meaningful generators only**: Keep constant for methodName and known-good IDs; catalog and uuid_from_listing where they reliably get IDs; range for pagination. Avoid enum for language. Lower sample sizes for pure catalogs (1–2).

---

## Doc structure

- **docs/global.md**: Conventions, `$defs`, common filters/keys, common patterns. Shared across all operations.
- **docs/ops/<Operation>.md**: Per-operation doc. Template: `## OperationName`, `### Request Schema` (JSON Schema), `### Response Schema` (JSON Schema), `### Notes`.
- **docs/API.md**: Generated from global + ops by `build_api_md.py`. Full reference.

**Per-op template rules:**

- Use `const` for single fixed values, not single-element enum.
- One keyword per property: `$ref` OR `type`, not both.
- Enums only via `$ref` to global `$defs` — no inline enum definitions.
- Use `anyOf` when a field has multiple shapes.

---

## Config

- **config/generators.json**: Request generators per operation. Macedonian-only, meaningful generators.
- **config/refine.json**: `model_notes` (for notes step), `model_apply` (for apply step), `batch_size`.

---

## Scripts

- **collect.py**: Generate requests from `generators.json`, send to API, save pairs to `collected/`. Uses file-based cache (`.api_cache/`). Logs to `logs/collect/<run_id>/`.
- **refine.py**: Pair-driven refine. Notes step per pair, batched apply step, write docs, rebuild API.md. LLM calls cached in `.llm_cache/`. Resumable via state file. Logs to `logs/refine/<run_id>/`.
- **build_api_md.py**: Regenerate `docs/API.md` from global + ops. Called by refine after each apply; can also be run standalone.
- **cache.py**: File-based cache for API requests (used by collect).
- **improved/llm.py**: LLM client for Anthropic Claude. Structured output support.

---

## Prompts

- **prompts/notes_from_pair.txt**: Notes step — analyze pair against current docs, produce actionable notes.
- **prompts/apply_notes.txt**: Apply step — apply batched notes to produce updated op md + global md.

---

## Models

- **Notes step**: claude-haiku-4-5 (fast, cheap; notes are concise).
- **Apply step**: claude-haiku-4-5 (can be upgraded per `config/refine.json`).
- Claude only. Anthropic exclusively. No OpenAI.

---

## Routing

- **Standard**: `https://www.sobranie.mk/Routing/MakePostRequest` — POST with `methodName`.
- **ASMX**: `GetCustomEventsCalendar`, `GetOfficialVisitsForUser` — different URLs, wrapped model.
- **Infrastructure**: `LoadLanguage` — `Infrastructure/LoadLanguage`, empty body.

---

## File layout

- **docs/global.md**: Conventions, $defs, common filters/keys.
- **docs/ops/<Operation>.md**: Per-operation docs.
- **docs/API.md**: Regenerated by build_api_md from global + ops.
- **collected/{operation}/**: req_001.json, resp_001.json, etc.
- **collected/manifest.json**: Links req ↔ resp per run.
- **errors/{operation}/**: Failed requests.
- **logs/collect/**: Collection run logs.
- **logs/refine/**: Refine run logs (refine.log, notes/, concerns.md, state.json).
- **config/refine.json**: Model and batch settings.
- **config/generators.json**: Request generators.
- **prompts/**: LLM prompt templates.

---

## Archive

Obsolete scripts (baseline md-only refine, gather_pairs), legacy prompts, old logs, caches, and schema-inference artifacts live in `archive/`. Structure preserved.
