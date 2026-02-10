# LLM-driven API.md pipeline

Single `docs/API.md` refined sequentially per request/response pair. Two LLM steps per pair; changes are additive only.

## Overview

1. **Gather** pairs from `collected/manifest.json` (optionally run phase3 with `config/generators_api_md.json` to generate more).
2. **Bootstrap** initial `docs/API.md` from `API_INDEX.md` + `API_DOCS.md`.
3. **Refine** per pair: (1) notes extraction, (2) apply notes → updated API.md. Sequential; each pair builds on the previous.

## API.md structure

- **Top**: API_INDEX content (intro, calling conventions, operations table).
- **$defs**: Shared types (AspDate, UUID, LanguageId, etc.).
- **Common patterns**: Domain conventions (institutional authors, plenary vs committee, etc.).
- **Common request filters**: Usage notes for TypeId, StatusId, CommitteeId, StructureId, Page/Rows, DateFrom/DateTo. Deduplicate globally.
- **Common response keys**: Meaning/usage notes for TotalItems, Items, d, Id/Title. Deduplicate globally.
- **Per-operation**: Each operation may have a `### Notes` section for filter usage and key meanings; Request and Response schemas.

## Prompts

Refine script passes system prompts reinforcing widening, filter/key notes, and deduplication. It also passes `max_tokens` for models with lower limits (e.g. 8192 for Haiku) to avoid 400 errors.

- **`prompts/notes_from_pair.txt`** (Step 1): Given current API.md and one req/resp pair, produce notes on what to add/update.
  - Widening only (add enum values, optional fields, anyOf/unions).
  - Filter usage and key meanings when useful.
  - Output "No changes needed" if the pair adds nothing.
- **`prompts/apply_notes_to_api_md.txt`** (Step 2): Given current API.md and notes, produce complete updated API.md.
  - Apply only the changes; preserve everything else.
  - Widening only; include filter/key notes when asked.

## Widening and anyOf

The LLM must only widen, never narrow:

- **Widening** = expand schemas to accept more valid values: add enum values, make fields optional (anyOf with null), add optional properties, use anyOf/union when a field has multiple types across samples.
- **anyOf/union** = use when a field can have multiple shapes, e.g. `anyOf: [string, null]` for nullable strings; `anyOf: [integer, array]` when the API returns different types. The docs must validate every previously seen body.
- **Never** remove enum values, make optional fields required, or drop anyOf branches.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/gather_pairs_for_api_md.py` | Flatten manifest pairs; optionally `--generate-more` with simplified config |
| `scripts/bootstrap_api_md.py` | Create initial API.md from API_INDEX + API_DOCS |
| `scripts/refine_api_md.py` | Per-pair refinement loop; `--limit`, `--resume`, `--dry-run` |
| `scripts/phase3_collect.py --config config/generators_api_md.json` | Collect with Macedonian-only, meaningful generators |

## Config

- **`config/generators_api_md.json`**: Simplified generators (languageId=1, smaller sample sizes for catalogs).
- **Env**: `ANTHROPIC_API_KEY` required; optional `API_MD_PATH`, `API_MD_MODEL_NOTES`, `API_MD_MODEL_APPLY`.

## Logs

`logs/refine_api_md/YYYY-MM-DD_HH-MM-SS/` — per-pair notes, prompts, errors.
