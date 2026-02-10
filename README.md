# Sobranie.mk API

Macedonian Parliament (Собрание) API documentation, procedurally improved by analyzing real request/response pairs with an LLM.

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

1. **Collect** — Generate requests from `config/generators.json`, send to the live API, save req/res pairs to `collected/`.
2. **Refine** — For each pair: LLM produces notes on what the docs should update. Every N notes: LLM applies them to produce updated docs. `docs/API.md` rebuilt after each batch.

## Usage

```bash
# 1. Collect req/res pairs
python scripts/collect.py
python scripts/collect.py --no-cache

# 2. Refine docs from pairs
python scripts/refine.py
python scripts/refine.py --batch-size 5 --op GetAllSittings
python scripts/refine.py --resume <run_id>
python scripts/refine.py --dry-run

# Rebuild API.md manually (refine does this automatically)
python scripts/build_api_md.py
```

**Env:** `ANTHROPIC_API_KEY` required for refine (not for collect).

**Resumable:** Refine tracks progress in `logs/refine/<run_id>/state.json`. Stop anytime; `--resume <run_id>` to continue.

**Monitor:** `tail -f logs/refine/<run_id>/refine.log` for live progress. Check `notes/` for individual pair analysis and `concerns.md` for flagged issues.

See **`CONTRIBUTING.md`** for step-by-step. See `docs/API.md` for the full API reference. See `DECISIONS.md` for rationale.
