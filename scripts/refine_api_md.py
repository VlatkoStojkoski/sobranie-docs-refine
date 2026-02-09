#!/usr/bin/env python3
"""
Refine docs using global.md + docs/ops/<Operation>.md.

Phase 2 only: Cleanup of markdown (no notes). For each op, sends global + op doc to LLM;
outputs new_global, new_op, raisePossibleIssueToHuman. Writes incrementally so you can
inspect results during the run. See DECISIONS.md.

Run: python scripts/refine_api_md.py
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
CONFIG = ROOT / "config"
DOCS = ROOT / "docs"
PROMPTS = ROOT / "prompts"
LOGS = ROOT / "logs" / "refine_api_md"
GLOBAL_MD = DOCS / "global.md"
OPS_DIR = DOCS / "ops"

MODEL_MAX_TOKENS = {
    "claude-3-5-haiku-20241022": 8192,
    "claude-3-haiku-20240307": 8192,
    "claude-haiku-4-5": 32000,
}

SYSTEM_CLEANUP = """You clean up Sobranie.mk API documentation. Use only the existing markdown (global + per-op doc); no notes or samples. Global must be minimal: only enums (with descriptions), general API notes, and common patterns that apply to many ops. Do not put operation-specific notes in global—they go in the per-op doc; your new_global is merged with other ops' so op-specific bullets would accumulate. Per-op: schemas from existing docs only, op-specific notes; reference global $defs for enums. Flag anything suspicious in raisePossibleIssueToHuman."""

PHASE2_CLEANUP_SCHEMA = {
    "type": "object",
    "properties": {
        "new_global": {"type": "string", "description": "Minimal shared global.md: conventions, $defs, common patterns only; no operation-specific content (put that in new_op). This is merged with other ops' new_global so do not add op-specific bullets."},
        "new_op": {"type": "string", "description": "Full updated per-operation .md content"},
        "raisePossibleIssueToHuman": {"type": "string", "description": "Anything worth human review; empty if nothing"},
    },
    "required": ["new_global", "new_op", "raisePossibleIssueToHuman"],
    "additionalProperties": False,
}


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
    parser.add_argument(
        "--model",
        default=os.environ.get("API_MD_MODEL_APPLY"),
        help="Model for cleanup step",
    )
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None, help="Process only first N operations")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cfg = load_refine_config()
    model = args.model or cfg.get("model_apply") or "claude-haiku-4-5"

    if not GLOBAL_MD.exists() or not OPS_DIR.exists():
        print("ERROR: docs/global.md or docs/ops/ not found. Run: python scripts/split_api_md.py")
        return 1

    op_files = sorted(f.stem for f in OPS_DIR.glob("*.md"))
    if not op_files:
        print("No operation markdown files in docs/ops/.")
        return 0

    if args.limit:
        op_files = op_files[: args.limit]

    cleanup_template_path = PROMPTS / "apply_cleanup_md.txt"
    if not cleanup_template_path.exists():
        print(f"ERROR: Prompt not found: {cleanup_template_path}")
        return 1
    cleanup_template = cleanup_template_path.read_text(encoding="utf-8")

    if not args.dry_run:
        from improved.llm import complete_structured
    else:
        complete_structured = None

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = LOGS / run_id
    log = _setup_logging(log_dir, run_id)

    log.info(f"Run {run_id} | Log dir: {log_dir}")
    log.info(f"Ops: {len(op_files)}, model: {model} (sequential, md-only, no notes)")
    log.debug(f"Args: {vars(args)}")

    global_content = GLOBAL_MD.read_text(encoding="utf-8")
    max_tokens = args.max_tokens or MODEL_MAX_TOKENS.get(model)

    issues_path = log_dir / "issues_for_review.md"
    if not args.dry_run:
        issues_path.write_text(
            f"# Issues for human review (refine_api_md Phase 2)\n\nRun: {run_id}\n\n",
            encoding="utf-8",
        )

    results: list[tuple[str, str, str, str]] = []
    all_issues: list[tuple[str, str]] = []

    def run_cleanup(op: str) -> tuple[str, str, str, str]:
        op_path = OPS_DIR / f"{op}.md"
        op_content = op_path.read_text(encoding="utf-8") if op_path.exists() else ""
        prompt = cleanup_template.format(
            global_md=global_content,
            op_md=op_content,
            operation=op,
        )
        result = complete_structured(
            prompt,
            schema=PHASE2_CLEANUP_SCHEMA,
            system=SYSTEM_CLEANUP,
            model=model,
            max_tokens=max_tokens,
        )
        return (
            op,
            result.get("new_global", global_content),
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
            op_name, ng, no, issue = r
            if issue and issue.strip():
                all_issues.append((op_name, issue.strip()))
                log.info(f"    issues flagged ({len(issue)} chars)")
            else:
                log.info(f"    OK")

            # Write intermediate results so you can inspect during the run
            (OPS_DIR / f"{op_name}.md").write_text(no, encoding="utf-8")
            new_globals_so_far = [x[1] for x in results]
            merged = _merge_globals(new_globals_so_far)
            GLOBAL_MD.write_text(merged, encoding="utf-8")
            if issue and issue.strip():
                with open(issues_path, "a", encoding="utf-8") as f:
                    f.write(f"## {op_name}\n\n{issue.strip()}\n\n")
        except Exception as e:
            log.error(f"  Cleanup ERROR: {e}")
            log.debug(f"Exception: {e}", exc_info=True)

    elapsed = time.perf_counter() - start_time
    if not args.dry_run and not all_issues:
        with open(issues_path, "a", encoding="utf-8") as f:
            f.write("No issues flagged.\n")
    log.info(f"Issues: {len(all_issues)} ops -> {issues_path}")

    if not args.dry_run and results:
        log.info("Regenerating docs/API.md")
        try:
            from build_api_md import build
            build()
        except Exception as e:
            log.warning(f"Could not regenerate API.md: {e}")

    log.info(f"Done in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    exit(main())
