# Sobranie.mk API

North Macedonian Parliament (Собрание) API documentation. LLM-driven refinement of a single `API.md` from live request/response pairs.

## What it does

1. **Collect** — Send requests to the API using `config/generators.json`, save req/resp pairs to `collected/`.
2. **Refine** — For each pair, run two Claude prompts: extract notes, then apply them to update `docs/API.md`. Additive only (widening, anyOf, filter/key notes).

Initial `docs/API.md` and `config/generators.json` are provided. No bootstrap or schema-inference scripts.

## Usage

```bash
# 1. Collect new pairs (optional: --generate-more to run collect first)
python scripts/gather_pairs.py
python scripts/gather_pairs.py --generate-more --no-cache

# 2. Refine API.md per pair
python scripts/refine_api_md.py
python scripts/refine_api_md.py --limit 5
python scripts/refine_api_md.py --resume 10 --limit 20
```

**Env:** `ANTHROPIC_API_KEY` required.

See `DECISIONS.md` for rationale and details.
