# Sobranie.mk API

Macedonian Parliament (Собрание) API documentation. LLM-driven refinement of `docs/global.md` and `docs/ops/<Operation>.md`. Collect fetches live request/response pairs; refine uses only existing markdown.

## The API

[Sobranie.mk](https://www.sobranie.mk) is the official website of the Macedonian Parliament. Its backend exposes a POST/JSON API that returns data in Macedonian, Albanian, and Turkish (`LanguageId`: 1, 2, 3).

### What data it gives access to

- **Catalogs** — Genders, parliamentary terms (StructureId), committees, material types/statuses, sitting/question statuses, institutions, procedure types, proposer types, application types.
- **Listings** — Sittings (plenary and committee), parliamentary questions, materials (laws, amendments, reports, etc.), MPs, monthly agenda, political parties, councils, parliamentary groups, MPs clubs.
- **Detail** — Full details for a sitting, material, question, committee, council, party, parliamentary group, MPs club, or MP (by structure). Voting results for sittings and agenda items. Amendments.
- **Other** — Calendar events (ASMX), official visits (ASMX), localization strings (LoadLanguage).

### Endpoints

- **Standard:** `https://www.sobranie.mk/Routing/MakePostRequest` — POST with `methodName` + params.
- **ASMX:** `https://www.sobranie.mk/Moldova/services/` — Calendar, official visits.
- **Infrastructure:** `https://www.sobranie.mk/Infrastructure/` — LoadLanguage.

Dates use AspDate format (`/Date(ms)/`). Pagination via `Page`/`Rows` or `CurrentPage`/`ItemsPerPage` depending on the operation. Full reference: `docs/API.md`.

---

## What this repo does

1. **Collect** — Send requests using `config/generators.json`, save pairs to `collected/`.
2. **Gather** — Flatten manifest into `collected/pairs.json` (optional; refine does not use pairs).
3. **Refine** — One LLM call per op: produce global_modification_notes + new_op. After all ops, apply notes in one batch to get final global.md. Writes each op doc as it goes; writes global once at the end. Issues to `issues_for_review.md`.
4. **Build** — Regenerate `docs/API.md` from global + ops (refine runs this automatically at the end).

Initial docs (`global.md`, `ops/*.md`) and `config/generators.json` are provided.

## Usage

```bash
# 1. Collect new pairs
python scripts/collect.py
python scripts/collect.py --no-cache

# 2. Gather pairs into collected/pairs.json (optional)
python scripts/gather_pairs.py
python scripts/gather_pairs.py --generate-more --no-cache

# 3. Refine global + per-op docs (per-op notes, then batch global apply)
python scripts/refine_ops_cleanup.py
python scripts/refine_ops_cleanup.py --limit 5 --dry-run

# Regenerate API.md manually (refine does this automatically at the end)
python scripts/build_api_md.py
```

**Refine options:** `--model`, `--limit N`, `--dry-run`

**During a run:** Each `docs/ops/<Op>.md` is written after its op; `docs/global.md` is written once at the end (batch apply). `tail -f logs/refine_ops_cleanup/<run_id>/issues_for_review.md` to watch issues. `docs/API.md` is regenerated at the end.

**Env:** `ANTHROPIC_API_KEY` required for refine (not for collect).

See **`CONTRIBUTING.md`** for step-by-step: refining docs vs generating new pairs. See `docs/API.md` for the full API reference. See `DECISIONS.md` for rationale and details.
