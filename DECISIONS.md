# Sobranie API documentation — decisions

All rationale and decisions from development. Single source of truth for why things work the way they do.

---

## Approach: LLM-driven API.md

- **Single artifact**: One `docs/API.md` containing schemas, notes, conventions, and per-operation docs. Not machine-only schema files.
- **Refinement loop**: For each request/response pair, two sequential LLM steps: (1) extract notes, (2) apply notes → updated API.md. Additive only.
- **No bootstrap/generation of initial files**: API.md and config/generators.json are provided by us. No scripts to create them from scratch.
- **Claude only**: Anthropic Claude exclusively. No OpenAI.

---

## Data quality and diversification

From analysis of collected data:

- **Success rate**: ~80% (345 successes vs 84 errors).
- **Low quality** (among successes): ~30 empty responses (TotalItems:0, Items:[], d:[]).
- **Duplicates**: Many pairs share identical requests (e.g. same languageId) and identical responses. Pure catalogs (GetAllGenders, GetAllApplicationTypes, LoadLanguage) yield redundant samples.
- **Macedonian only**: Use `languageId`/`LanguageId` = 1 (Macedonian) everywhere. No Albanian/Turkish variants.
- **Meaningful generators only**: Keep constant for methodName and known-good IDs; catalog and uuid_from_listing where they reliably get IDs; range for pagination. Avoid enum for language. Lower sample sizes for pure catalogs (1–2).

---

## API.md structure

- **Top**: Intro, calling conventions, operations table.
- **$defs**: Shared types (AspDate, UUID, LanguageId, etc.).
- **Common patterns**: Domain conventions.
- **Common request filters**: Usage notes for TypeId, StatusId, CommitteeId, StructureId, Page/Rows, etc. Deduplicate globally.
- **Common response keys**: Meaning/usage for TotalItems, Items, d, etc. Deduplicate globally.
- **Per-operation**: Notes, Request, Response. Add `### Notes` when filter/key notes are discovered.

---

## Widening and anyOf

LLM must only widen, never narrow:

- **Widening** = expand schemas to accept more values: add enum values, make fields optional (anyOf with null), add optional properties, use anyOf/union when a field has multiple types.
- **anyOf/union** = required when a field can have multiple shapes. Docs must validate every previously seen body.
- **Never** remove enum values, make optional fields required, or drop anyOf branches.

---

## Filter usage and key meanings

- Request filters: explain what each does, how it affects results, when to use/omit.
- Response keys: explain meaning and typical usage. Add to Common sections; deduplicate globally.

---

## Config

- **config/generators.json**: The one generator config. Macedonian-only, meaningful generators, smaller sample sizes for catalogs.

---

## Scripts (simplified)

- **collect.py**: Send requests using generators, save to collected/. Uses cache.
- **gather_pairs.py**: Flatten manifest pairs; optionally run collect first (`--generate-more`).
- **refine_api_md.py**: Per-pair refinement loop. Two LLM steps per pair. `--limit`, `--resume`, `--dry-run`.

---

## Prompts

- **notes_from_pair.txt**: Extract notes from pair vs current API.md. Widening only, filter/key notes when useful.
- **apply_notes_to_api_md.txt**: Apply notes → complete updated API.md.

---

## Models and limits

- Claude Sonnet for both steps (notes + apply). Haiku has 8192 max output; API.md can exceed that.
- Script passes max_tokens for known models (e.g. 8192 for Haiku) to avoid 400 errors.

---

## Routing

- **Standard**: `https://www.sobranie.mk/Routing/MakePostRequest` — POST, body includes methodName.
- **ASMX**: `GetCustomEventsCalendar`, `GetOfficialVisitsForUser` — different URLs, wrapped model.
- **Infrastructure**: `LoadLanguage` — `Infrastructure/LoadLanguage`, empty body.

---

## File layout

- **collected/{operation}/**: req_001.json, resp_001.json, etc.
- **collected/manifest.json**: Links req ↔ resp per run.
- **errors/{operation}/**: Failed requests.
- **prompts/**: LLM prompt templates.

---

## Archive

Obsolete scripts, logs, caches, legacy docs, and schema-inference artifacts live in `archive/`. Structure preserved; new obsolete items are added, not reorganized.
