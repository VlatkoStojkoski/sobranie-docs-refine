#!/usr/bin/env python3
"""
Refine docs using global.md + docs/ops/<Operation>.md.

Bulk flow: (1) Run notes for all pairs (5 parallel at a time); (2) Group notes by operation;
(3) Chunk ops into groups of 5; (4) Run 5 apply calls in parallel per chunk; (5) Merge
5 new_globals via concatenation; (6) Write docs, next chunk. Additive only. See DECISIONS.md.

Run: python scripts/gather_pairs.py && python scripts/refine_api_md.py
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
CONFIG = ROOT / "config"
COLLECTED = ROOT / "collected"
DOCS = ROOT / "docs"
PROMPTS = ROOT / "prompts"
LOGS = ROOT / "logs" / "refine_api_md"
PAIRS_FILE = COLLECTED / "pairs.json"
GLOBAL_MD = DOCS / "global.md"
OPS_DIR = DOCS / "ops"

CHUNK_SIZE = 5
PARALLEL_NOTES = 5

MAX_REQ_CHARS = 4000
MAX_RESP_CHARS = 12000

MODEL_MAX_TOKENS = {
    "claude-3-5-haiku-20241022": 8192,
    "claude-3-haiku-20240307": 8192,
    "claude-haiku-4-5": 32000,
}

SYSTEM_NOTES = """You refine Sobranie.mk API documentation. Widening only: add enum values, optional fields, anyOf unions; never remove or narrow. Add filter usage and key meaning notes to Common request filters / Common response keys; deduplicate globally. Per-op Notes for operation-specific details."""

SYSTEM_APPLY = """You apply notes to update global.md and the per-operation .md. Widening only: add enum values, anyOf with null, new optional properties, union types. Preserve all existing content. Include filter/key notes when the notes ask. Never drop enum values or anyOf branches."""


def truncate_json(obj, max_chars: int) -> str:
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    if len(s) <= max_chars:
        return s
    return s[: max_chars - 50] + "\n  ... (truncated)"


def _merge_globals(globals: list[str]) -> str:
    """Merge multiple global.md versions via concatenation. Split by ## sections, dedupe lines per section."""
    if len(globals) == 1:
        return globals[0]
    sections: dict[str, list[str]] = {}
    section_order: list[str] = []
    for g in globals:
        parts = re.split(r"\n(?=## )", g.strip())
        for part in parts:
            part = part.strip()
            if not part:
                continue
            lines = part.split("\n")
            header = lines[0].strip()
            content_lines = lines[1:]
            seen = set()
            unique = []
            for line in content_lines:
                key = line.strip()
                if key and key not in seen:
                    seen.add(key)
                    unique.append(line)
            if header not in sections:
                sections[header] = []
                section_order.append(header)
            sections[header].extend(unique)
    out_parts = []
    for header in section_order:
        lines = sections[header]
        seen = set()
        unique = []
        for line in lines:
            key = line.strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(line)
        out_parts.append(header + "\n" + "\n".join(unique))
    return "\n\n".join(out_parts)


def load_refine_config() -> dict:
    cfg_path = CONFIG / "refine.json"
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return {}


def _setup_logging(log_dir: Path, run_id: str) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "refine.log"
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))

    log = logging.getLogger("refine_api_md")
    log.setLevel(logging.DEBUG)
    log.handlers.clear()
    log.addHandler(fh)
    log.addHandler(ch)

    llm_log = logging.getLogger("llm")
    llm_log.setLevel(logging.DEBUG)
    llm_log.handlers.clear()
    llm_log.addHandler(fh)
    llm_log.addHandler(ch)

    return log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", default=str(PAIRS_FILE), help="Path to pairs JSON")
    parser.add_argument(
        "--model-notes",
        default=os.environ.get("API_MD_MODEL_NOTES"),
        help="Model for notes step",
    )
    parser.add_argument(
        "--model-apply",
        default=os.environ.get("API_MD_MODEL_APPLY"),
        help="Model for apply step",
    )
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--resume", type=int, default=None, help="Resume from pair index (0-based)")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help=f"Apply ops per chunk in parallel (default {CHUNK_SIZE})",
    )
    parser.add_argument(
        "--parallel-notes",
        type=int,
        default=PARALLEL_NOTES,
        help=f"Notes in parallel (default {PARALLEL_NOTES})",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cfg = load_refine_config()
    model_notes = args.model_notes or cfg.get("model_notes") or "claude-sonnet-4-5"
    model_apply = args.model_apply or cfg.get("model_apply") or "claude-haiku-4-5"

    pairs_path = Path(args.pairs)
    if not pairs_path.is_absolute():
        pairs_path = ROOT / pairs_path

    if not pairs_path.exists():
        print("ERROR: Pairs file not found. Run: python scripts/gather_pairs.py")
        return 1

    if not GLOBAL_MD.exists() or not OPS_DIR.exists():
        print("ERROR: docs/global.md or docs/ops/ not found. Run: python scripts/split_api_md.py")
        return 1

    pairs = json.loads(pairs_path.read_text(encoding="utf-8"))
    if not pairs:
        print("No pairs to process.")
        return 0

    start_idx = args.resume or 0
    end_idx = len(pairs) if args.limit is None else min(start_idx + args.limit, len(pairs))
    subset = pairs[start_idx:end_idx]

    notes_template = (PROMPTS / "notes_from_pair.txt").read_text(encoding="utf-8")
    apply_template = (PROMPTS / "apply_notes_to_api_md.txt").read_text(encoding="utf-8")

    if not args.dry_run:
        from improved.llm import complete, complete_structured, APPLY_OUTPUT_SCHEMA
    else:
        complete = complete_structured = APPLY_OUTPUT_SCHEMA = None

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = LOGS / run_id
    log = _setup_logging(log_dir, run_id)

    log.info(f"Run {run_id} | Log dir: {log_dir}")
    log.info(f"Pairs: {start_idx}..{end_idx - 1} ({len(subset)} total)")
    log.info(f"Models: notes={model_notes}, apply={model_apply}")
    log.info(f"Chunk size: {args.chunk_size}, parallel notes: {args.parallel_notes}")
    log.debug(f"Args: {vars(args)}")

    global_content = GLOBAL_MD.read_text(encoding="utf-8")

    # --- Phase 1: Notes for all pairs (5 parallel at a time) ---
    op_content_cache: dict[str, str] = {}

    def run_notes(job: tuple[int, dict]) -> tuple[int, str, str | None]:
        i, p = job
        op = p.get("operation", "?")
        req_rel = p.get("req", "")
        resp_rel = p.get("resp", "")
        req_path = COLLECTED / req_rel
        resp_path = COLLECTED / resp_rel
        if not req_path.exists() or not resp_path.exists():
            return (i, op, None)
        op_path = OPS_DIR / f"{op}.md"
        op_content = op_content_cache.get(op) or (op_path.read_text(encoding="utf-8") if op_path.exists() else "")
        if op not in op_content_cache:
            op_content_cache[op] = op_content
        req_json = json.loads(req_path.read_text(encoding="utf-8"))
        resp_json = json.loads(resp_path.read_text(encoding="utf-8"))
        req_str = truncate_json(req_json, MAX_REQ_CHARS)
        resp_str = truncate_json(resp_json, MAX_RESP_CHARS)
        prompt = notes_template.format(
            global_md=global_content,
            op_md=op_content,
            operation=op,
            request_json=req_str,
            response_json=resp_str,
        )
        if args.dry_run:
            (log_dir / f"{i:04d}_{op}_prompt_notes.txt").write_text(prompt, encoding="utf-8")
            return (i, op, "No changes needed.")
        try:
            notes = complete(
                prompt,
                system=SYSTEM_NOTES,
                model=model_notes,
                max_tokens=MODEL_MAX_TOKENS.get(model_notes),
            )
            (log_dir / f"{i:04d}_{op}_notes.txt").write_text(notes, encoding="utf-8")
            return (i, op, notes)
        except Exception as e:
            (log_dir / f"{i:04d}_{op}_error.txt").write_text(str(e), encoding="utf-8")
            return (i, op, None)

    log.info("Phase 1: Notes (starting)")
    phase1_start = time.perf_counter()
    jobs = [(start_idx + i, p) for i, p in enumerate(subset)]
    notes_results: list[tuple[int, str, str | None]] = []
    with ThreadPoolExecutor(max_workers=args.parallel_notes) as ex:
        futures = {ex.submit(run_notes, j): j for j in jobs}
        done = 0
        for fut in as_completed(futures):
            r = fut.result()
            notes_results.append(r)
            done += 1
            if r[2] is not None:
                log.info(f"  Notes OK [{r[0]}] {r[1]} ({done}/{len(jobs)})")
                log.debug(f"Notes [{r[0]}] {r[1]} -> {len(r[2])} chars")
            else:
                log.warning(f"  Notes SKIP/ERR [{r[0]}] {r[1]} ({done}/{len(jobs)})")
                log.debug(f"Notes [{r[0]}] {r[1]} -> skipped or error")

    notes_results.sort(key=lambda x: x[0])
    phase1_elapsed = time.perf_counter() - phase1_start
    ok_count = sum(1 for r in notes_results if r[2] is not None)
    log.info(f"Phase 1: Notes done in {phase1_elapsed:.1f}s ({ok_count}/{len(jobs)} ok)")

    # --- Group notes by operation ---
    notes_by_op: dict[str, list[str]] = {}
    for _, op, notes in notes_results:
        if notes is None:
            continue
        notes_by_op.setdefault(op, []).append(notes)

    if not notes_by_op:
        log.warning("No notes collected.")
        return 0

    ops_with_notes = sorted(notes_by_op.keys())
    log.info(f"Grouped notes: {len(ops_with_notes)} ops, {sum(len(v) for v in notes_by_op.values())} notes total")
    op_chunks = [
        ops_with_notes[i : i + args.chunk_size]
        for i in range(0, len(ops_with_notes), args.chunk_size)
    ]
    log.info(f"Phase 2: {len(op_chunks)} chunks of up to {args.chunk_size} ops each")

    # --- Phase 2: Apply per chunk (5 parallel), merge globals, write ---
    max_tokens_apply = args.max_tokens or MODEL_MAX_TOKENS.get(model_apply)

    def run_apply(op: str) -> tuple[str, str, str]:
        op_path = OPS_DIR / f"{op}.md"
        op_content = op_content_cache.get(op) or (op_path.read_text(encoding="utf-8") if op_path.exists() else "")
        all_notes = "\n\n---\n\n## Next pair\n\n".join(notes_by_op[op])
        prompt = apply_template.format(
            global_md=global_content,
            op_md=op_content,
            operation=op,
            notes=all_notes,
        )
        result = complete_structured(
            prompt,
            schema=APPLY_OUTPUT_SCHEMA,
            system=SYSTEM_APPLY,
            model=model_apply,
            max_tokens=max_tokens_apply,
        )
        return (op, result.get("new_global", global_content), result.get("new_op", op_content))

    phase2_start = time.perf_counter()
    phase2_elapsed = 0.0
    for chunk_idx, ops_chunk in enumerate(op_chunks):
        if args.dry_run:
            log.info(f"  Chunk {chunk_idx + 1}/{len(op_chunks)}: DRY-RUN {ops_chunk}")
            continue

        log.info(f"  Chunk {chunk_idx + 1}/{len(op_chunks)}: Apply {ops_chunk}")
        chunk_start = time.perf_counter()
        results: list[tuple[str, str, str]] = []
        with ThreadPoolExecutor(max_workers=len(ops_chunk)) as ex:
            futures = [ex.submit(run_apply, op) for op in ops_chunk]
            for fut in as_completed(futures):
                try:
                    r = fut.result()
                    results.append(r)
                    log.info(f"    Apply OK {r[0]}")
                    log.debug(f"Apply {r[0]} -> new_global {len(r[1])} chars, new_op {len(r[2])} chars")
                except Exception as e:
                    log.error(f"    Apply ERROR: {e}")
                    log.debug(f"Apply exception: {e}", exc_info=True)

        new_globals = [r[1] for r in results]
        merged_global = _merge_globals(new_globals)
        log.debug(f"Merged {len(new_globals)} globals -> {len(merged_global)} chars")
        global_content = merged_global
        GLOBAL_MD.write_text(merged_global, encoding="utf-8")
        log.debug(f"Wrote global.md ({len(merged_global)} chars)")

        for op, _, new_op in results:
            (OPS_DIR / f"{op}.md").write_text(new_op, encoding="utf-8")
            op_content_cache[op] = new_op
        log.debug(f"Wrote {len(results)} op files")

        chunk_elapsed = time.perf_counter() - chunk_start
        log.info(f"  Chunk {chunk_idx + 1}/{len(op_chunks)} done in {chunk_elapsed:.1f}s")

    phase2_elapsed = time.perf_counter() - phase2_start
    if not args.dry_run and notes_by_op:
        log.info("Regenerating docs/API.md")
        from build_api_md import build
        build()
        log.debug("build_api_md done")

    log.info(f"Done. Phase 1: {phase1_elapsed:.1f}s, Phase 2: {phase2_elapsed:.1f}s, Total: ~{phase1_elapsed + phase2_elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    exit(main())
