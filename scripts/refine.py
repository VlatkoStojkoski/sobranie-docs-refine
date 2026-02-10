#!/usr/bin/env python3
"""
Refine docs from collected req/res pairs.

Pipeline:
  1. Load pairs from collected/manifest.json
  2. For each pair: LLM notes step (what should change)
  3. Every batch_size notes: LLM apply step (produce new docs)
  4. Write updated docs, rebuild API.md

Resumable via logs/refine/<run_id>/state.json.
LLM calls cached in .llm_cache/ (skip with --no-llm-cache).

Usage:
  python scripts/refine.py
  python scripts/refine.py --batch-size 5 --op GetAllSittings
  python scripts/refine.py --resume 2026-02-09_18-00-00
  python scripts/refine.py --dry-run
"""

import argparse
import hashlib
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

DOCS = ROOT / "docs"
GLOBAL_MD = DOCS / "global.md"
OPS_DIR = DOCS / "ops"
COLLECTED = ROOT / "collected"
LOGS = ROOT / "logs" / "refine"
PROMPTS = ROOT / "prompts"
CONFIG = ROOT / "config"
LLM_CACHE_DIR = ROOT / ".llm_cache"

# --- Schemas ---

NOTES_SCHEMA = {
    "type": "object",
    "properties": {
        "notes": {
            "type": "string",
            "description": "Concise notes on what to add/update, or 'No changes needed.' if the pair adds nothing new.",
        },
    },
    "required": ["notes"],
    "additionalProperties": False,
}

APPLY_SCHEMA = {
    "type": "object",
    "properties": {
        "newOperationMd": {
            "type": "string",
            "description": "Full updated per-operation .md content.",
        },
        "newGlobalMd": {
            "type": "string",
            "description": "Full updated global.md content.",
        },
        "seriousConcerns": {
            "type": "string",
            "description": "Breaking changes or serious issues to flag. Empty string if none.",
        },
    },
    "required": ["newOperationMd", "newGlobalMd", "seriousConcerns"],
    "additionalProperties": False,
}

SYSTEM_NOTES = (
    "You analyze real API request/response pairs to refine documentation "
    "for the Sobranie.mk parliament API. Be precise and concise."
)

SYSTEM_APPLY = (
    "You produce updated Sobranie.mk API documentation by applying analyst notes. "
    "Preserve all existing information; only refine and improve accuracy."
)

# Notes step input budget (tokens). Response gets the remainder after template + global + op + request.
NOTES_INPUT_BUDGET = 15_000
# Value truncation: max chars per string (and similar limits) before budget-based array capping.
MAX_STR_LENGTH = 200
# Max tokens for request body so huge requests don't blow total prompt size.
REQUEST_MAX_TOKENS = 2000

# --- Helpers ---


def _estimate_tokens(s: str) -> int:
    """Rough token count for prompt text (Claude/GPT ~4 chars per token)."""
    return max(1, len(s) // 4)


def _truncate_values(data, max_str: int = MAX_STR_LENGTH):
    """Truncate string (and other value) lengths only; do not cap array sizes."""
    if isinstance(data, list):
        return [_truncate_values(item, max_str) for item in data]
    if isinstance(data, dict):
        return {k: _truncate_values(v, max_str) for k, v in data.items()}
    if isinstance(data, str) and len(data) > max_str:
        return data[:max_str] + f"... ({len(data)} chars)"
    return data


def _find_largest_lists(data, path=()):
    """Return list of (path_tuple, length) for every list in the tree."""
    out = []
    if isinstance(data, list):
        out.append((path, len(data)))
        for i, item in enumerate(data):
            out.extend(_find_largest_lists(item, path + (i,)))
    elif isinstance(data, dict):
        for k, v in data.items():
            out.extend(_find_largest_lists(v, path + (k,)))
    return out


def _get_at_path(data, path):
    for key in path:
        data = data[key]
    return data


def _replace_at_path(data, path, value):
    if len(path) == 1:
        if isinstance(data, list):
            copy = list(data)
            copy[path[0]] = value
            return copy
        copy = dict(data)
        copy[path[0]] = value
        return copy
    if isinstance(data, list):
        copy = list(data)
        copy[path[0]] = _replace_at_path(copy[path[0]], path[1:], value)
        return copy
    copy = dict(data)
    copy[path[0]] = _replace_at_path(copy[path[0]], path[1:], value)
    return copy


def _shrink_largest_array(data):
    """Shrink the largest array (by item count) by half; add _truncated for the rest. Return new data."""
    candidates = _find_largest_lists(data)
    if not candidates:
        return data
    path, length = max(candidates, key=lambda x: x[1])
    if length <= 1:
        return data
    lst = _get_at_path(data, path)
    n = (length + 1) // 2
    new_list = list(lst[:n]) + [{"_truncated": length - n}]
    return _replace_at_path(data, path, new_list)


def _fit_response_to_budget(data, budget_tokens: int) -> object:
    """Cap arrays so that json.dumps(data) fits in budget_tokens (value truncation already applied)."""
    while True:
        current_tokens = _estimate_tokens(json.dumps(data, ensure_ascii=False))
        if current_tokens <= budget_tokens:
            break
        new_data = _shrink_largest_array(data)
        if _estimate_tokens(json.dumps(new_data, ensure_ascii=False)) >= current_tokens:
            break  # no progress (e.g. all arrays length <= 1)
        data = new_data
    return data


def _substitute(template: str, **kwargs) -> str:
    """Replace <<<key>>> placeholders; safe when values contain { or } (e.g. JSON)."""
    out = template
    for k, v in kwargs.items():
        out = out.replace("<<<" + k + ">>>", str(v))
    return out


def _cap_request_json(req_json: str) -> str:
    """Cap request JSON length so prefix stays manageable (soft target)."""
    budget_chars = REQUEST_MAX_TOKENS * 4
    if len(req_json) <= budget_chars:
        return req_json
    return req_json[:budget_chars] + "\n  ... (request truncated for prompt size)"


def _setup_logging(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger("refine")
    log.setLevel(logging.DEBUG)
    log.handlers.clear()
    fh = logging.FileHandler(log_dir / "refine.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(ch)
    llm_log = logging.getLogger("llm")
    llm_log.setLevel(logging.DEBUG)
    llm_log.handlers.clear()
    llm_log.addHandler(fh)
    llm_log.addHandler(ch)
    return log


def _llm_cache_key(prompt: str, schema: dict, system: str) -> str:
    payload = json.dumps({"s": system, "p": prompt, "sc": schema}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:20]


def llm_call(prompt, schema, system, model, max_tokens, *, use_cache=True, log=None):
    """Call LLM with optional file-based caching."""
    from improved.llm import complete_structured

    key = _llm_cache_key(prompt, schema, system)
    cache_file = LLM_CACHE_DIR / f"{key}.json"

    if use_cache and cache_file.exists():
        try:
            result = json.loads(cache_file.read_text(encoding="utf-8"))
            if log:
                log.debug(f"  LLM cache hit: {key}")
            return result
        except (json.JSONDecodeError, OSError):
            pass

    result = complete_structured(
        prompt, schema=schema, system=system, model=model, max_tokens=max_tokens,
    )

    LLM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"processed": []}


def save_state(path: Path, state: dict):
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def load_pairs_from_manifest(run_id: str | None = None) -> list[dict]:
    """Load successful pairs from manifest. If run_id given, only that run."""
    manifest_path = COLLECTED / "manifest.json"
    if not manifest_path.exists():
        return []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    runs = manifest.get("runs", [])
    if run_id == "latest" and runs:
        runs = [runs[-1]]
    elif run_id:
        runs = [r for r in runs if r.get("run_id") == run_id]
    pairs = []
    seen = set()
    for run in runs:
        for p in run.get("pairs", []):
            req_rel = p.get("req", "")
            resp_rel = p.get("resp", "")
            if not req_rel or not resp_rel or req_rel in seen:
                continue
            seen.add(req_rel)
            op = req_rel.split("/")[0] if "/" in req_rel else ""
            if (COLLECTED / req_rel).exists() and (COLLECTED / resp_rel).exists():
                pairs.append({"operation": op, "req": req_rel, "resp": resp_rel})
    return pairs


def rebuild_api_md(log):
    try:
        from build_api_md import build
        build()
        log.debug("  API.md rebuilt")
    except Exception as e:
        log.warning(f"  API.md rebuild failed: {e}")


# --- Main ---


def main() -> int:
    parser = argparse.ArgumentParser(description="Refine docs from collected req/res pairs.")
    parser.add_argument("--batch-size", type=int, default=None, help="Notes per apply call (default from config or 5)")
    parser.add_argument("--resume", type=str, default=None, metavar="RUN_ID", help="Resume a previous run")
    parser.add_argument("--model", default=None, help="Model override (both notes and apply)")
    parser.add_argument("--op", default=None, help="Process only this operation")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N pairs total")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    parser.add_argument("--no-llm-cache", action="store_true", help="Skip LLM response cache")
    parser.add_argument("--save-prompts", action="store_true",
                        help="Write prompt and full LLM response per pair to logs/refine/<run_id>/notes/")
    parser.add_argument("--collect-run", type=str, default="latest", metavar="RUN_ID",
                        help="Which collect run to use: 'latest' (default), 'all', or a specific run ID")
    args = parser.parse_args()

    # Config
    cfg = {}
    cfg_path = CONFIG / "refine.json"
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    model_notes = args.model or cfg.get("model_notes") or cfg.get("model_apply") or "claude-haiku-4-5"
    model_apply = args.model or cfg.get("model_apply") or "claude-haiku-4-5"
    batch_size = args.batch_size or cfg.get("batch_size") or 5
    use_llm_cache = not args.no_llm_cache

    # Run ID and logging
    run_id = args.resume or datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = LOGS / run_id
    notes_dir = log_dir / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    log = _setup_logging(log_dir)

    state_path = log_dir / "state.json"
    state = load_state(state_path)
    processed = set(state.get("processed", []))
    concerns_path = log_dir / "concerns.md"

    # Load prompts
    notes_prompt_path = PROMPTS / "notes_from_pair.txt"
    apply_prompt_path = PROMPTS / "apply_notes.txt"
    if not notes_prompt_path.exists() or not apply_prompt_path.exists():
        log.error("Missing prompt files in prompts/")
        return 1
    notes_template = notes_prompt_path.read_text(encoding="utf-8")
    apply_template = apply_prompt_path.read_text(encoding="utf-8")

    # Load and filter pairs
    collect_run = None if args.collect_run == "all" else args.collect_run
    all_pairs = load_pairs_from_manifest(collect_run)
    if not all_pairs:
        log.error("No pairs found. Run collect.py first.")
        return 1

    ops_pairs: dict[str, list[dict]] = {}
    for p in all_pairs:
        if args.op and p["operation"] != args.op:
            continue
        if p["req"] not in processed:
            ops_pairs.setdefault(p["operation"], []).append(p)

    # Apply --limit
    if args.limit:
        remaining = args.limit
        trimmed: dict[str, list[dict]] = {}
        for op in sorted(ops_pairs):
            take = min(len(ops_pairs[op]), remaining)
            if take > 0:
                trimmed[op] = ops_pairs[op][:take]
                remaining -= take
            if remaining <= 0:
                break
        ops_pairs = trimmed

    total_pending = sum(len(v) for v in ops_pairs.values())
    log.info(f"Run {run_id} | models: {model_notes}/{model_apply} | batch: {batch_size}")
    log.info(f"Pairs: {len(all_pairs)} total, {total_pending} pending, {len(processed)} done")

    if args.dry_run:
        for op, pairs in sorted(ops_pairs.items()):
            log.info(f"  {op}: {len(pairs)} pairs")
        return 0

    if not GLOBAL_MD.exists():
        log.error("docs/global.md not found")
        return 1

    start_time = time.perf_counter()
    pairs_done = 0
    applies_done = 0

    for op, pairs in sorted(ops_pairs.items()):
        op_path = OPS_DIR / f"{op}.md"
        if not op_path.exists():
            log.warning(f"Skip {op}: no docs/ops/{op}.md")
            continue

        log.info(f"--- {op} ({len(pairs)} pairs) ---")

        notes_batch: list[str] = []
        batch_keys: list[str] = []

        for i, pair in enumerate(pairs):
            # Read current docs (re-read each time; previous apply may have updated them)
            global_md = GLOBAL_MD.read_text(encoding="utf-8")
            op_md = op_path.read_text(encoding="utf-8")

            # Load pair; truncate request and response for notes step budget
            req_data = json.loads((COLLECTED / pair["req"]).read_text(encoding="utf-8"))
            resp_data = json.loads((COLLECTED / pair["resp"]).read_text(encoding="utf-8"))
            req_truncated = _truncate_values(req_data, max_str=MAX_STR_LENGTH)
            req_json = _cap_request_json(json.dumps(req_truncated, ensure_ascii=False, indent=2))
            prefix = _substitute(
                notes_template,
                global_md=global_md, op_md=op_md, operation=op,
                request_json=req_json, response_json="",
            )
            response_budget = max(500, NOTES_INPUT_BUDGET - _estimate_tokens(prefix))
            value_truncated = _truncate_values(resp_data, max_str=MAX_STR_LENGTH)
            resp_truncated = _fit_response_to_budget(value_truncated, response_budget)
            resp_json = json.dumps(resp_truncated, ensure_ascii=False, indent=2)

            # --- Notes step ---
            log.info(f"  [{i+1}/{len(pairs)}] Notes: {pair['req']}")
            prompt = _substitute(
                notes_template,
                global_md=global_md, op_md=op_md, operation=op,
                request_json=req_json, response_json=resp_json,
            )
            try:
                result = llm_call(
                    prompt, NOTES_SCHEMA, SYSTEM_NOTES, model_notes, 4096,
                    use_cache=use_llm_cache, log=log,
                )
                notes = result.get("notes", "No changes needed.")
            except Exception as e:
                log.error(f"  Notes failed: {e}")
                continue

            # Save notes to log
            safe_name = pair["req"].replace("/", "_").replace(".json", "")
            (notes_dir / f"{safe_name}.txt").write_text(notes, encoding="utf-8")
            if getattr(args, "save_prompts", False):
                (notes_dir / f"{safe_name}_prompt.txt").write_text(prompt, encoding="utf-8")
                (notes_dir / f"{safe_name}_response.json").write_text(
                    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
                )

            is_last = (i == len(pairs) - 1)
            no_changes = notes.strip().lower() in ("no changes needed.", "no changes needed")

            if no_changes:
                log.info(f"    -> No changes")
                processed.add(pair["req"])
                pairs_done += 1
            else:
                log.info(f"    -> {len(notes)} chars of notes")
                notes_batch.append(notes)
                batch_keys.append(pair["req"])
                pairs_done += 1

            # --- Apply step (when batch full or last pair for this op) ---
            should_apply = notes_batch and (len(notes_batch) >= batch_size or is_last)
            if should_apply:
                global_md = GLOBAL_MD.read_text(encoding="utf-8")
                op_md = op_path.read_text(encoding="utf-8")
                notes_text = "\n\n".join(
                    f"### Note {j+1}\n{n}" for j, n in enumerate(notes_batch)
                )

                log.info(f"  Apply: {len(notes_batch)} notes")
                prompt = _substitute(
                    apply_template,
                    global_md=global_md, op_md=op_md,
                    operation=op, notes=notes_text,
                )
                try:
                    result = llm_call(
                        prompt, APPLY_SCHEMA, SYSTEM_APPLY, model_apply, 32000,
                        use_cache=use_llm_cache, log=log,
                    )
                except Exception as e:
                    log.error(f"  Apply failed: {e}")
                    notes_batch.clear()
                    batch_keys.clear()
                    continue

                # Write updated docs
                new_op = result.get("newOperationMd", op_md)
                new_global = result.get("newGlobalMd", global_md)
                concerns = result.get("seriousConcerns", "")

                op_path.write_text(new_op, encoding="utf-8")
                GLOBAL_MD.write_text(new_global, encoding="utf-8")
                log.info(f"  Wrote {op}.md + global.md")

                rebuild_api_md(log)
                applies_done += 1

                # Log concerns
                if concerns and concerns.strip():
                    log.warning(f"  CONCERNS: {concerns[:200]}")
                    with open(concerns_path, "a", encoding="utf-8") as f:
                        f.write(f"## {op} (apply {applies_done})\n\n{concerns.strip()}\n\n")

                # Mark batch pairs as processed
                for k in batch_keys:
                    processed.add(k)
                notes_batch.clear()
                batch_keys.clear()

            # Save state after every pair
            state["processed"] = sorted(processed)
            save_state(state_path, state)

    elapsed = time.perf_counter() - start_time
    log.info(f"Done: {pairs_done} pairs, {applies_done} applies, {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
