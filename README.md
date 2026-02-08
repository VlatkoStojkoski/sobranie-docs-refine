# Sobranie.mk API

> North Macedonian Parliament (Собрание) API documentation.

## Docs

| File | Purpose |
|------|---------|
| `docs/API_INDEX.md` | Operation index, calling conventions, route descriptions |
| `docs/API_DOCS.md` | Precise request/response schemas for all operations |
| `docs/openapi.yaml` | OpenAPI 3.0 spec (generated from API_DOCS) |

## Scripts

```bash
# 1. Collect diverse samples (listings + detail requests)
python scripts/collect.py

# 2. LLM enrichment: compare samples to docs → docs/ENRICHMENT_REPORT.md
python scripts/enrich.py

# 3. Generate openapi.yaml from API_DOCS.md
python scripts/generate_openapi.py
```

**Env:** `ANTHROPIC_API_KEY` for enrich.py and generate_openapi.py.

Use `ENRICHMENT_REPORT.md` to prompt an assistant to update API_INDEX.md and API_DOCS.md.

## One-time: build docs from archive

```bash
python scripts/build_docs_from_archive.py  # Populates API_DOCS from archive
```
