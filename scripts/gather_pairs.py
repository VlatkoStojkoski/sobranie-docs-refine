#!/usr/bin/env python3
"""
Gather req/resp pairs from manifest for refinement. Optionally run collect first.

Run: python scripts/gather_pairs.py [--generate-more] [--no-cache]
Output: collected/pairs.json
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
COLLECTED = ROOT / "collected"
PAIRS_OUTPUT = COLLECTED / "pairs.json"


def flatten_pairs_from_manifest(manifest_path: Path) -> list[dict]:
    if not manifest_path.exists():
        return []

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pairs = []
    seen = set()

    for run in manifest.get("runs", []):
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

            pairs.append({"operation": operation, "req": req_rel, "resp": resp_rel})

    return pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-more", action="store_true", help="Run collect.py before gathering")
    parser.add_argument("--no-cache", action="store_true", help="Pass --no-cache to collect")
    parser.add_argument("--output", default=str(PAIRS_OUTPUT), help="Output path")
    args = parser.parse_args()

    if args.generate_more:
        cmd = [sys.executable, str(ROOT / "scripts" / "collect.py")]
        if args.no_cache:
            cmd.append("--no-cache")
        result = subprocess.run(cmd, cwd=str(ROOT))
        if result.returncode != 0:
            print("ERROR: collect failed")
            return result.returncode

    pairs = flatten_pairs_from_manifest(COLLECTED / "manifest.json")
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(pairs, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Gathered {len(pairs)} pairs -> {output_path}")
    return 0


if __name__ == "__main__":
    exit(main())
