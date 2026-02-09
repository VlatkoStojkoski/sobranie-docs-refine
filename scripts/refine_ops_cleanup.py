#!/usr/bin/env python3
"""
Refine docs/global.md and docs/ops/<Op>.md.

Per operation: produce global_modification_notes (what to change in global for this op) and new_op (template-following doc; specifics in op not global). After all ops, apply notes in one batch to produce final global.md. Issues go to issues_for_review.md.

Run: python scripts/refine_ops_cleanup.py [--dry-run] [--limit N]
Output: docs/global.md (once at end), docs/ops/*.md, logs/refine_ops_cleanup/<run_id>/refine.log + issues_for_review.md
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
CONFIG = ROOT / "config"
DOCS = ROOT / "docs"
PROMPTS = ROOT / "prompts"
LOGS = ROOT / "logs" / "refine_ops_cleanup"
GLOBAL_MD = DOCS / "global.md"
OPS_DIR = DOCS / "ops"


def load_refine_config() -> dict:
    cfg_path = CONFIG / "refine.json"
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return {}


def _setup_logging(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "refine.log"
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    log = logging.getLogger("refine_ops_cleanup")
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


# Structured output per op: global_modification_notes, new_op, raisePossibleIssueToHuman
CLEANUP_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "global_modification_notes": {
            "type": "string",
            "description": "Instructions to update global.md for this operation's context only: e.g. add enum X to $defs, add a common pattern if it applies to many ops, or 'move Y to op doc'. Be concise; these notes will be batched with other ops and applied once. Empty string if no changes needed for global.",
        },
        "new_op": {"type": "string", "description": "Full per-operation .md content following the template (### Request Schema, ### Response Schema, ### Notes) with all field-level details preserved; operation-specific content stays here, not in global."},
        "raisePossibleIssueToHuman": {
            "type": "string",
            "description": "Anything suspicious or worth human review; empty string if nothing to flag",
        },
    },
    "required": ["global_modification_notes", "new_op", "raisePossibleIssueToHuman"],
    "additionalProperties": False,
}

SYSTEM_CLEANUP = """You refine Sobranie.mk API documentation. Use only the existing markdown (global + per-op doc); do not use request/response samples.

Global: Output only global_modification_notes—concise instructions for what should change in global.md for this op's context (e.g. ensure enum X is in $defs; add a convention only if it applies to many ops; or "move this to op doc"). Do not output full global; notes will be batched and applied later. Put operation-specific details in new_op, not in global notes.

Per-op doc (new_op): Must follow the exact template: ## OperationName, then ### Request Schema (JSON Schema), ### Response Schema (JSON Schema), ### Notes. Preserve every field and behavior from the current doc; do not drop field details. Use $ref to global $defs for enums. Move any operation-specific notes from global into ### Notes. Flag issues in raisePossibleIssueToHuman."""


# Batch: apply all per-op modification notes to produce final global.md
BATCH_GLOBAL_SCHEMA = {
    "type": "object",
    "properties": {
        "global_md": {"type": "string", "description": "The final global.md content after applying all modification notes. Minimal: conventions, $defs, common patterns only; no op-specific content."},
    },
    "required": ["global_md"],
    "additionalProperties": False,
}

BATCH_GLOBAL_SYSTEM = """You produce the final global.md for Sobranie.mk API docs. You are given the current global.md and modification notes from each operation. Apply the notes: add or update $defs and sections as requested, move op-specific content out (it belongs in per-op docs). Keep global minimal and deduplicated. Output only the final global_md content."""


def main() -> int:
    parser = argparse.ArgumentParser(description="Refine global + per-op docs; output issues for review.")
    parser.add_argument("--dry-run", action="store_true", help="Do not call LLM or write files")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N operations")
    parser.add_argument("--model", default=None, help="Model (default from config)")
    args = parser.parse_args()

    cfg = load_refine_config()
    model = args.model or cfg.get("model_apply") or "claude-haiku-4-5"

    if not GLOBAL_MD.exists() or not OPS_DIR.exists():
        print("ERROR: docs/global.md or docs/ops/ not found.")
        return 1

    op_files = sorted(f.stem for f in OPS_DIR.glob("*.md"))
    if not op_files:
        print("No operation markdown files in docs/ops/.")
        return 0

    if args.limit:
        op_files = op_files[: args.limit]

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = LOGS / run_id
    log = _setup_logging(log_dir)

    log.info(f"Run {run_id} | Log dir: {log_dir}")
    log.info(f"Ops: {len(op_files)}, model: {model} (sequential)")

    template_path = PROMPTS / "refine_ops_cleanup.txt"
    if not template_path.exists():
        log.error(f"Prompt not found: {template_path}")
        return 1
    template = template_path.read_text(encoding="utf-8")

    global_content = GLOBAL_MD.read_text(encoding="utf-8")

    all_issues: list[tuple[str, str]] = []  # (op, issue_text)
    results: list[tuple[str, str, str, str]] = []
    issues_path = log_dir / "issues_for_review.md"
    if not args.dry_run:
        issues_path.write_text(
            f"# Issues for human review (refine_ops_cleanup)\n\nRun: {run_id}\n\n",
            encoding="utf-8",
        )

    def run_cleanup(op: str) -> tuple[str, str, str, str]:
        op_path = OPS_DIR / f"{op}.md"
        op_content = op_path.read_text(encoding="utf-8") if op_path.exists() else ""
        prompt = template.format(
            global_md=global_content,
            op_md=op_content,
            operation=op,
        )
        from improved.llm import complete_structured
        result = complete_structured(
            prompt,
            schema=CLEANUP_OUTPUT_SCHEMA,
            system=SYSTEM_CLEANUP,
            model=model,
            max_tokens=32000,
        )
        return (
            op,
            result.get("global_modification_notes", "").strip(),
            result.get("new_op", op_content),
            result.get("raisePossibleIssueToHuman", ""),
        )

    start_time = time.perf_counter()
    for idx, op in enumerate(op_files):
        if args.dry_run:
            log.info(f"  [{idx + 1}/{len(op_files)}] DRY-RUN {op}")
            continue
        log.info(f"  [{idx + 1}/{len(op_files)}] {op}")
        try:
            r = run_cleanup(op)
            results.append(r)
            op_name, notes, new_op, issue = r
            if issue and issue.strip():
                all_issues.append((op_name, issue.strip()))
                log.info(f"    issues flagged ({len(issue)} chars)")
            else:
                log.info(f"    OK")
            if notes:
                log.debug(f"    global notes: {len(notes)} chars")

            if not args.dry_run:
                (OPS_DIR / f"{op_name}.md").write_text(new_op, encoding="utf-8")
                if issue and issue.strip():
                    with open(issues_path, "a", encoding="utf-8") as f:
                        f.write(f"## {op_name}\n\n{issue.strip()}\n\n")
        except Exception as e:
            log.error(f"  Cleanup ERROR: {e}")
            log.debug(f"Exception: {e}", exc_info=True)

    # Batch-apply all global modification notes to produce final global.md
    notes_list: list[tuple[str, str]] = [(op_name, n) for op_name, n, _, _ in results if n] if results else []
    if not args.dry_run and results:
        if notes_list:
            log.info(f"Applying {len(notes_list)} global modification note(s) in one batch")
            batch_prompt = f"""## Current global.md

{global_content}

---

## Modification notes from operations (apply these to produce final global.md)

"""
            for op_name, n in notes_list:
                batch_prompt += f"### {op_name}\n{n.strip()}\n\n"
            batch_prompt += "---\n\nProduce global_md: the final global.md after applying all notes. Keep global minimal; only conventions, $defs, common patterns; no op-specific content. Deduplicate."
            try:
                from improved.llm import complete_structured
                batch_result = complete_structured(
                    batch_prompt,
                    schema=BATCH_GLOBAL_SCHEMA,
                    system=BATCH_GLOBAL_SYSTEM,
                    model=model,
                    max_tokens=32000,
                )
                final_global = batch_result.get("global_md", global_content)
                GLOBAL_MD.write_text(final_global, encoding="utf-8")
                log.debug("Wrote docs/global.md from batch apply")
            except Exception as e:
                log.warning(f"Batch global apply failed: {e}. Leaving global.md unchanged.")
        else:
            log.info("No global modification notes; global.md unchanged")

    if results and not args.dry_run:
        log.debug(f"Wrote {len(results)} op files" + (" + global.md (batch)" if notes_list else ""))

    elapsed = time.perf_counter() - start_time

    if not args.dry_run and not all_issues:
        with open(issues_path, "a", encoding="utf-8") as f:
            f.write("No issues flagged.\n")
    log.info(f"Issues: {len(all_issues)} ops -> {issues_path}")

    # Regenerate docs/API.md from cleaned global + ops
    if not args.dry_run and results:
        log.info("Regenerating docs/API.md")
        try:
            from build_api_md import build
            build()
            log.debug("build_api_md done")
        except Exception as e:
            log.warning(f"Could not regenerate API.md: {e}")

    log.info(f"Done in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
