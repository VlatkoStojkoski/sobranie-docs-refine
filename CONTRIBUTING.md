# Contributing

How to contribute by **refining the docs** or **generating new request/response pairs**.

---

## Prerequisites

- **Python 3** (tested on 3.10+)
- **Dependencies**: `requests` for collection (install if needed: `pip install requests`)
- **Refine only**: Set `ANTHROPIC_API_KEY` (e.g. in `.env` in repo root). Copy `.env.example` to `.env` and add your key. Refine uses Claude to update markdown.

---

## Path A: Refining the docs

You improve `docs/global.md` and `docs/ops/<Operation>.md` so they stay consistent, minimal, and template-following. No request/response samples are sent to the LLM—only existing markdown.

1. **Ensure docs exist**  
   You need `docs/global.md` and `docs/ops/*.md` (they are in the repo).

2. **Set API key**  
   Create `.env` in the repo root with:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **Run refine (dry-run first)**  
   ```bash
   python scripts/refine_ops_cleanup.py --limit 3 --dry-run
   ```
   Dry-run lists which ops would be processed without calling the LLM or writing files.

4. **Run refine for real**  
   ```bash
   python scripts/refine_ops_cleanup.py
   ```
   - Processes every op in `docs/ops/*.md` except OPERATION_TEMPLATE.md (alphabetically).
   - For each op: one LLM call → `global_modification_notes` + updated op doc. Each `docs/ops/<Op>.md` is written right after its op.
   - After all ops: one batch LLM call applies all modification notes → writes `docs/global.md` once.
   - Then runs `build_api_md` to regenerate `docs/API.md`.
   - Logs and issues: `logs/refine_ops_cleanup/<run_id>/refine.log` and `issues_for_review.md`.

5. **Review issues**  
   Open `logs/refine_ops_cleanup/<run_id>/issues_for_review.md`. Fix any real inconsistencies in the docs (or in `config/generators.json` if relevant), then re-run refine if needed.

6. **Commit**  
   Commit changes to `docs/global.md`, `docs/ops/*.md`, and `docs/API.md` (and any config/prompt changes you made).

**Useful options:** `--limit N` (process only first N ops), `--dry-run`, `--model <name>` (override model from `config/refine.json`).

---

## Path B: Generating new pairs

You add or extend request/response pairs under `collected/` so the project has fresh data (e.g. for manual inspection or future tooling). Refine does **not** read these pairs; it only reads markdown.

1. **Understand the config**  
   Requests are driven by `config/generators.json`: one entry per operation, with parameter generators (constants, ranges, IDs from listing responses, etc.). See existing entries for patterns.

2. **Run collection**  
   ```bash
   python scripts/collect.py
   ```
   - Sends requests to the live API according to `generators.json`.
   - Saves pairs under `collected/<Operation>/` (e.g. `req_001.json`, `resp_001.json`).
   - Uses a cache by default (same request → skip). Use `--no-cache` to force fresh requests.
   - Failures are written to `errors/<Operation>/`.

3. **Optional: gather pairs**  
   ```bash
   python scripts/gather_pairs.py
   ```
   Flattens the manifest into `collected/pairs.json`. Optional; refine does not use this file.

4. **Use the data**  
   Inspect `collected/` and `errors/` to add new operations to `generators.json`, fix parameter ranges, or document new response shapes in the docs by hand (or run refine after you’ve updated the markdown yourself).

**No API key needed** for collection; it only does HTTP POSTs to the Sobranie API.

---

## Doing both

1. **Collect** to refresh or extend pairs.
2. **Edit** `docs/global.md` or `docs/ops/<Op>.md` manually if you discovered new fields or behaviors from the new pairs.
3. **Refine** to re-normalize and clean the docs (template, const vs enum, $ref-only, etc.) and regenerate `docs/API.md`.

---

## Where things live

| Item | Purpose |
|------|--------|
| `docs/global.md` | Conventions, $defs, common patterns. Refine updates this once at the end (batch). |
| `docs/ops/*.md` | One file per operation (Request Schema, Response Schema, Notes). Refine updates each as it runs. |
| `docs/API.md` | Generated from global + ops; built at the end of refine or via `python scripts/build_api_md.py`. |
| `docs/ops/OPERATION_TEMPLATE.md` | Template for op docs; refine and build exclude it. |
| `config/generators.json` | Defines how collect generates requests per operation. |
| `config/refine.json` | Model for refine (e.g. `model_apply`). |
| `prompts/refine_ops_cleanup.txt` | Prompt used by refine. |

For rationale and design choices, see `DECISIONS.md`.
