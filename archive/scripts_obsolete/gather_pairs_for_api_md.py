#!/usr/bin/env python3
"""
Gather request/response pairs for API.md refinement.

Reads collected/manifest.json, flattens all pairs, optionally runs phase3
with simplified config to generate more, then outputs a combined pair list.

Run:
  python scripts/gather_pairs_for_api_md.py
  python scripts/gather_pairs_for_api_md.py --generate-more
  python scripts/gather_pairs_for_api_md.py --generate-more --no-cache

Output: collected/pairs_for_api_md.json (list of {operation, req, resp})
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
COLLECTED = ROOT / "collected"
CONFIG = ROOT / "config"
PAIRS_OUTPUT = COLLECTED / "pairs_for_api_md.json"


def flatten_pairs_from_manifest(manifest_path: Path) -> list[dict]:
    """Flatten all pairs from manifest, ordered by run_id then pairs. Filter to existing files."""
    if not manifest_path.exists():
        return []

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pairs = []
    seen = set()

    for run in manifest.get("runs", []):
        run_id = run.get("run_id", "")
        for p in run.get("pairs", []):
            req_rel = p.get("req", "")
            resp_rel = p.get("resp", "")
            if not req_rel or not resp_rel:
                continue

            req_path = COLLECTED / req_rel
            resp_path = COLLECTED / resp_rel
            if not req_path.exists() or not resp_path.exists():
                continue

            operation = req_rel.split("/")[0] if "/" in req_rel else ""

            key = (operation, req_rel, resp_rel)
            if key in seen:
                continue
            seen.add(key)

            pairs.append({
                "operation": operation,
                "req": req_rel,
                "resp": resp_rel,
                "run_id": run_id,
            })

    return pairs


def main():
    parser = argparse.ArgumentParser(description="Gather req/resp pairs for API.md refinement")
    parser.add_argument(
        "--generate-more",
        action="store_true",
        help="Run phase3 with config/generators_api_md.json before gathering",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Pass --no-cache to phase3 when generating more",
    )
    parser.add_argument(
        "--output",
        default=str(PAIRS_OUTPUT),
        help=f"Output path for pair list (default: {PAIRS_OUTPUT})",
    )
    args = parser.parse_args()

    if args.generate_more:
        cfg = CONFIG / "generators_api_md.json"
        if not cfg.exists():
            print("ERROR: config/generators_api_md.json not found. Run with --generate-more only if simplified config exists.")
            return 1

        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "phase3_collect.py"),
            "--config",
            str(cfg),
        ]
        if args.no_cache:
            cmd.append("--no-cache")

        print("Running phase3 with simplified config to generate more pairs...")
        result = subprocess.run(cmd, cwd=str(ROOT))
        if result.returncode != 0:
            print("ERROR: phase3_collect failed")
            return result.returncode

    pairs = flatten_pairs_from_manifest(COLLECTED / "manifest.json")
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(pairs, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Gathered {len(pairs)} pairs -> {output_path}")
    return 0


if __name__ == "__main__":
    exit(main())
