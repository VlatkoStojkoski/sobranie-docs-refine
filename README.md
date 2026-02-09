# Sobranie.mk API

Macedonian Parliament (Собрание) API documentation. LLM-driven refinement of `docs/global.md` and `docs/ops/<Operation>.md` from live request/response pairs.

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
2. **Gather** — Flatten manifest into `collected/pairs.json` for refinement (optional).
3. **Refine** — Clean up markdown: global + per-op docs, no notes or samples. One LLM call per operation, sequential. Writes incrementally so you can inspect results during the run. Issues flagged in `issues_for_review.md`.
4. **Build** — Regenerate `docs/API.md` from global + ops (refine does this automatically at the end).

Initial docs (`global.md`, `ops/*.md`) and `config/generators.json` are provided.

## Usage

```bash
# One-time: split monolithic API.md (if migrating)
python scripts/split_api_md.py

# 1. Collect new pairs
python scripts/collect.py
python scripts/collect.py --no-cache

# 2. Gather pairs into collected/pairs.json (optional; refine_api_md does not use pairs)
python scripts/gather_pairs.py
python scripts/gather_pairs.py --generate-more --no-cache

# 3. Refine (md-only cleanup, sequential, no notes)
python scripts/refine_api_md.py
python scripts/refine_api_md.py --limit 5 --dry-run

# Alternative: refine_ops_cleanup (same idea, temporary script)
python scripts/refine_ops_cleanup.py
python scripts/refine_ops_cleanup.py --limit 5 --dry-run

# Regenerate API.md manually (refine does this automatically at the end)
python scripts/build_api_md.py
```

**Refine options:** `--model`, `--max-tokens`, `--limit N`, `--dry-run`

**During a run:** `docs/global.md` and `docs/ops/*.md` are written after each op. `tail -f logs/refine_api_md/<run_id>/issues_for_review.md` to watch issues. `docs/API.md` is updated only at the end.

**Env:** `ANTHROPIC_API_KEY` required.

See `docs/API.md` for the full API reference. See `DECISIONS.md` for rationale and details.
