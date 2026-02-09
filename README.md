# Sobranie.mk API

North Macedonian Parliament (Собрание) API documentation. LLM-driven refinement of `docs/global.md` and `docs/ops/<Operation>.md` from live request/response pairs.

## What it does

1. **Collect** — Send requests using `config/generators.json`, save pairs to `collected/`.
2. **Refine** — Phase 1: notes for all pairs (5 parallel). Phase 2: group notes by operation, chunk ops into 5, run 5 apply calls in parallel per chunk; merge 5 new_globals via concatenation; write docs; next chunk. Additive only. Bulk apply reduces cost (~31 apply calls vs 345).

Initial docs (`global.md`, `ops/*.md`) and `config/generators.json` are provided.

## Usage

```bash
# One-time: split monolithic API.md (if migrating)
python scripts/split_api_md.py

# 1. Collect new pairs (optional: --generate-more to run collect first)
python scripts/gather_pairs.py
python scripts/gather_pairs.py --generate-more --no-cache

# 2. Refine (bulk: notes 5 parallel, apply 5 ops per chunk)
python scripts/refine_api_md.py
python scripts/refine_api_md.py --limit 20
python scripts/refine_api_md.py --resume 0 --limit 50

# Regenerate combined API.md (refine does this automatically; run manually if needed)
python scripts/build_api_md.py
```

**Refine options:** `--chunk-size 5`, `--parallel-notes 5`, `--resume`, `--limit`, `--dry-run`

**Env:** `ANTHROPIC_API_KEY` required.

See `DECISIONS.md` for rationale and details.
