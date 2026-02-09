#!/usr/bin/env python3
"""
Refine docs/API.md sequentially per request/response pair.

For each pair: (1) LLM extracts notes; (2) LLM applies notes → updated API.md.
Additive only. See DECISIONS.md.

Run: python scripts/gather_pairs.py && python scripts/refine_api_md.py
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
COLLECTED = ROOT / "collected"
DOCS = ROOT / "docs"
PROMPTS = ROOT / "prompts"
LOGS = ROOT / "logs" / "refine_api_md"
PAIRS_FILE = COLLECTED / "pairs.json"
DEFAULT_API_MD = DOCS / "API.md"

# Max chars for request/response in prompt (avoid context overflow)
MAX_REQ_CHARS = 4000
MAX_RESP_CHARS = 12000

# Models with output limits < 16000 (Haiku: 8192)
MODEL_MAX_TOKENS = {
    "claude-3-5-haiku-20241022": 8192,
    "claude-3-haiku-20240307": 8192,
}

SYSTEM_NOTES = """You refine Sobranie.mk API documentation. Widening only: add enum values, optional fields, anyOf unions; never remove or narrow. Add filter usage and key meaning notes to Common request filters / Common response keys; deduplicate globally. Per-op Notes for operation-specific details."""

SYSTEM_APPLY = """You apply notes to update API.md. Widening only: add enum values, anyOf with null, new optional properties, union types. Preserve all existing content. Include filter/key notes when the notes ask. Never drop enum values or anyOf branches."""


def truncate_json(obj, max_chars: int) -> str:
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    if len(s) <= max_chars:
        return s
    return s[: max_chars - 50] + "\n  ... (truncated)"


def load_llm():
    from improved.llm import complete
    return complete


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-md",
        default=os.environ.get("API_MD_PATH", str(DEFAULT_API_MD)),
        help="Path to API.md (env: API_MD_PATH)",
    )
    parser.add_argument("--pairs", default=str(PAIRS_FILE), help="Path to pairs JSON")
    parser.add_argument(
        "--model-notes",
        default=os.environ.get("API_MD_MODEL_NOTES"),
        help="Model for notes step (default: claude-sonnet-4-20250514)",
    )
    parser.add_argument(
        "--model-apply",
        default=os.environ.get("API_MD_MODEL_APPLY"),
        help="Model for apply step (default: claude-sonnet-4-20250514; use Haiku only if API.md is small)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Override max_tokens for apply step (e.g. 8192 for Haiku); auto-set for known models",
    )
    parser.add_argument("--resume", type=int, default=None, help="Resume from pair index (0-based)")
    parser.add_argument("--limit", type=int, default=None, help="Max pairs to process")
    parser.add_argument("--dry-run", action="store_true", help="Log prompts only, do not call LLM")
    args = parser.parse_args()

    api_md_path = Path(args.api_md)
    if not api_md_path.is_absolute():
        api_md_path = ROOT / api_md_path

    pairs_path = Path(args.pairs)
    if not pairs_path.is_absolute():
        pairs_path = ROOT / pairs_path

    if not pairs_path.exists():
        print("ERROR: Pairs file not found. Run: python scripts/gather_pairs.py")
        return 1

    if not api_md_path.exists():
        print("ERROR: docs/API.md not found")
        return 1

    pairs = json.loads(pairs_path.read_text(encoding="utf-8"))
    if not pairs:
        print("No pairs to process.")
        return 0

    start_idx = args.resume or 0
    if start_idx >= len(pairs):
        print("Resume index >= pair count. Nothing to do.")
        return 0

    end_idx = len(pairs)
    if args.limit is not None:
        end_idx = min(start_idx + args.limit, len(pairs))

    subset = pairs[start_idx:end_idx]
    print(f"Processing pairs {start_idx}..{end_idx - 1} ({len(subset)} pairs)")

    notes_template = (PROMPTS / "notes_from_pair.txt").read_text(encoding="utf-8")
    apply_template = (PROMPTS / "apply_notes_to_api_md.txt").read_text(encoding="utf-8")

    complete = load_llm() if not args.dry_run else None

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = LOGS / run_id
    log_dir.mkdir(parents=True, exist_ok=True)

    api_md_content = api_md_path.read_text(encoding="utf-8")

    for i, p in enumerate(subset):
        global_idx = start_idx + i
        op = p.get("operation", "?")
        req_rel = p.get("req", "")
        resp_rel = p.get("resp", "")

        req_path = COLLECTED / req_rel
        resp_path = COLLECTED / resp_rel
        if not req_path.exists() or not resp_path.exists():
            print(f"  [{global_idx}] SKIP {op}: missing files")
            continue

        req_json = json.loads(req_path.read_text(encoding="utf-8"))
        resp_json = json.loads(resp_path.read_text(encoding="utf-8"))

        req_str = truncate_json(req_json, MAX_REQ_CHARS)
        resp_str = truncate_json(resp_json, MAX_RESP_CHARS)

        prompt_notes = notes_template.format(
            api_md=api_md_content,
            operation=op,
            request_json=req_str,
            response_json=resp_str,
        )

        if args.dry_run:
            (log_dir / f"{global_idx:04d}_{op}_prompt_notes.txt").write_text(prompt_notes, encoding="utf-8")
            print(f"  [{global_idx}] DRY-RUN {op}")
            continue

        model_notes = args.model_notes or "claude-sonnet-4-20250514"
        max_tokens_notes = MODEL_MAX_TOKENS.get(model_notes)
        try:
            notes = complete(
                prompt_notes,
                system=SYSTEM_NOTES,
                model=model_notes,
                max_tokens=max_tokens_notes,
            )
        except Exception as e:
            print(f"  [{global_idx}] ERROR {op}: {e}")
            (log_dir / f"{global_idx:04d}_{op}_error.txt").write_text(str(e), encoding="utf-8")
            continue

        (log_dir / f"{global_idx:04d}_{op}_notes.txt").write_text(notes, encoding="utf-8")

        prompt_apply = apply_template.format(api_md=api_md_content, notes=notes)

        model_apply = args.model_apply or "claude-sonnet-4-20250514"
        max_tokens_apply = args.max_tokens or MODEL_MAX_TOKENS.get(model_apply)
        try:
            new_api_md = complete(
                prompt_apply,
                system=SYSTEM_APPLY,
                model=model_apply,
                max_tokens=max_tokens_apply,
            )
        except Exception as e:
            print(f"  [{global_idx}] ERROR {op} (apply): {e}")
            (log_dir / f"{global_idx:04d}_{op}_apply_error.txt").write_text(str(e), encoding="utf-8")
            continue

        # Strip markdown fences if present
        new_api_md = new_api_md.strip()
        if new_api_md.startswith("```"):
            lines = new_api_md.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            new_api_md = "\n".join(lines)

        api_md_content = new_api_md
        api_md_path.write_text(api_md_content, encoding="utf-8")

        hash_after = hashlib.sha256(api_md_content.encode()).hexdigest()[:8]
        print(f"  [{global_idx}] OK {op} (hash={hash_after})")

    print("Done.")
    return 0


if __name__ == "__main__":
    exit(main())
