# Contributing

## Prerequisites

- Python 3.10+
- `pip install requests` (for collect)
- `ANTHROPIC_API_KEY` in `.env` (for refine). Copy `.env.example` → `.env` and add your key.

---

## 1. Collect req/res pairs

Generate requests from `config/generators.json`, send to the live API, save pairs:

```bash
python scripts/collect.py            # with cache (default)
python scripts/collect.py --no-cache  # fresh requests
```

- Pairs saved to `collected/<Operation>/req_NNN.json` and `resp_NNN.json`.
- Errors saved to `errors/<Operation>/err_NNN.json`.
- Request config: `config/generators.json` (one entry per operation with parameter generators).

## 2. Refine docs from pairs

Analyze pairs with an LLM to improve `docs/global.md` and `docs/ops/<Op>.md`:

```bash
python scripts/refine.py                          # process all pending pairs
python scripts/refine.py --batch-size 5            # notes per apply call
python scripts/refine.py --op GetAllSittings       # one operation only
python scripts/refine.py --limit 20                # at most 20 pairs
python scripts/refine.py --resume 2026-02-09_18-00 # resume a stopped run
python scripts/refine.py --dry-run                 # show what would be processed
```

Each batch: **notes step** (one LLM call per pair) → **apply step** (one LLM call per batch) → write `docs/ops/<Op>.md` + `docs/global.md` → rebuild `docs/API.md`.

Stop anytime. Resume with `--resume <run_id>`.

## 3. Monitor progress

```bash
tail -f logs/refine/<run_id>/refine.log   # live progress
ls logs/refine/<run_id>/notes/             # individual pair notes
cat logs/refine/<run_id>/concerns.md       # serious issues flagged by LLM
cat logs/refine/<run_id>/state.json        # resume state (processed pairs)
```

---

## Where things live

| Item | Purpose |
|------|---------|
| `docs/global.md` | Conventions, $defs, common patterns. Updated by refine. |
| `docs/ops/*.md` | Per-operation docs (request/response schema, notes). Updated by refine. |
| `docs/API.md` | Generated from global + ops. Rebuilt after each apply. |
| `config/generators.json` | How collect generates requests per operation. |
| `config/refine.json` | Models (`model_notes`, `model_apply`) and `batch_size`. |
| `prompts/notes_from_pair.txt` | Prompt for notes step (analyze pair against docs). |
| `prompts/apply_notes.txt` | Prompt for apply step (produce updated docs from notes). |

For rationale and design choices, see `DECISIONS.md`.
