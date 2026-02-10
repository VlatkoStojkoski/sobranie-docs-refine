#!/usr/bin/env python3
"""
Phase 0: Preparation for improved flow.

1. Create dirs: data/, collected/, errors/, listing_cache/, config/, schemas/
2. Copy HAR from archive/logs.har to data/session.har if missing
3. Migrate collected/YYYY-MM-DD_HH-MM-SS/*.json to new layout:
   collected/{operation}/req_NNN.json, resp_NNN.json
   manifest.json, errors_manifest.json

Keeps old collected dirs; does not delete.

Run: python scripts/phase0_prepare.py
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARCHIVE_HAR = ROOT / "archive" / "logs.har"
DATA_HAR = ROOT / "data" / "session.har"
COLLECTED = ROOT / "collected"
ERRORS = ROOT / "errors"
LISTING_CACHE = ROOT / "listing_cache"
CONFIG = ROOT / "config"
SCHEMAS = ROOT / "schemas"

DIRS = [ROOT / "data", COLLECTED, ERRORS, LISTING_CACHE, CONFIG, SCHEMAS]


def ensure_dirs():
    """Create required directories."""
    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  {d.relative_to(ROOT)}")


def ensure_har():
    """Copy HAR from archive to data/session.har if missing."""
    if DATA_HAR.exists():
        print(f"  {DATA_HAR.relative_to(ROOT)} exists")
        return
    if not ARCHIVE_HAR.exists():
        print(f"  WARN: {ARCHIVE_HAR.relative_to(ROOT)} not found; skipping HAR copy")
        return
    DATA_HAR.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ARCHIVE_HAR, DATA_HAR)
    print(f"  Copied {ARCHIVE_HAR.name} -> {DATA_HAR.relative_to(ROOT)}")


def _is_error_response(resp) -> bool:
    if resp is None:
        return True
    if isinstance(resp, dict) and resp.get("_error") is not None:
        return True
    return False


def _operation_name_from_path(p: Path) -> str:
    return p.stem


def _strip_truncated(obj):
    """Remove _truncated markers from response for clean schema inference."""
    if isinstance(obj, dict):
        if obj.get("_truncated") is not None:
            return None
        return {k: _strip_truncated(v) for k, v in obj.items()}
    if isinstance(obj, list):
        out = []
        for x in obj:
            stripped = _strip_truncated(x)
            if stripped is not None and not (isinstance(x, dict) and x.get("_truncated") is not None):
                out.append(stripped)
        return out
    return obj


def _max_existing_id(op_dir: Path, prefix: str) -> int:
    """Return max N from req_NNN.json / resp_NNN.json in op_dir."""
    max_n = 0
    for f in op_dir.glob(f"{prefix}_*.json"):
        try:
            n = int(f.stem.split("_")[1])
            max_n = max(max_n, n)
        except (ValueError, IndexError):
            pass
    return max_n


def migrate_collected():
    """Migrate old collected format to new layout."""
    old_runs = sorted(
        d for d in COLLECTED.iterdir()
        if d.is_dir() and d.name[0].isdigit() and "_" in d.name
    )
    if not old_runs:
        print("  No old collected runs found")
        return

    manifest_path = COLLECTED / "manifest.json"
    err_manifest_path = COLLECTED / "errors_manifest.json"
    existing = {"runs": [], "migrated_run_ids": set()}
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            existing["runs"] = data.get("runs", [])
            existing["migrated_run_ids"] = {r["run_id"] for r in existing["runs"]}
        except (json.JSONDecodeError, OSError):
            pass

    errors_manifest = []
    if err_manifest_path.exists():
        try:
            data = json.loads(err_manifest_path.read_text(encoding="utf-8"))
            errors_manifest = data.get("errors", [])
        except (json.JSONDecodeError, OSError):
            pass

    op_counters: dict[str, int] = {}

    def next_id(op: str) -> int:
        if op not in op_counters:
            op_dir = COLLECTED / op
            op_counters[op] = _max_existing_id(op_dir, "req")
        op_counters[op] += 1
        return op_counters[op]

    new_runs = []
    for run_dir in old_runs:
        if run_dir.name in existing["migrated_run_ids"]:
            continue
        run_id = run_dir.name
        run_pairs = []

        for f in sorted(run_dir.glob("*.json")):
            if f.name == "manifest.json":
                continue
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue

            method = data.get("method") or _operation_name_from_path(f)
            samples = data.get("samples", [])

            for s in samples:
                req = s.get("request")
                resp = s.get("response")
                if req is None:
                    continue

                n = next_id(method)
                nnn = f"{n:03d}"

                op_dir = COLLECTED / method
                op_dir.mkdir(parents=True, exist_ok=True)
                req_path = op_dir / f"req_{nnn}.json"
                resp_path = op_dir / f"resp_{nnn}.json"

                req_path.write_text(json.dumps(req, ensure_ascii=False, indent=2), encoding="utf-8")

                if _is_error_response(resp):
                    err_path = ERRORS / method / f"err_{nnn}.json"
                    err_path.parent.mkdir(parents=True, exist_ok=True)
                    err_path.write_text(
                        json.dumps(resp if resp else {}, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    errors_manifest.append({
                        "req": f"{method}/req_{nnn}.json",
                        "error": f"{method}/err_{nnn}.json",
                    })
                else:
                    clean_resp = _strip_truncated(resp)
                    resp_path.write_text(
                        json.dumps(clean_resp, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    run_pairs.append({
                        "req": f"{method}/req_{nnn}.json",
                        "resp": f"{method}/resp_{nnn}.json",
                    })

        if run_pairs:
            new_runs.append({"run_id": run_id, "pairs": run_pairs})

    if new_runs:
        all_runs = existing["runs"] + new_runs
        manifest_path.write_text(
            json.dumps({"runs": all_runs}, indent=2),
            encoding="utf-8",
        )
        total_pairs = sum(len(r["pairs"]) for r in new_runs)
        print(f"  Migrated {total_pairs} pairs from {len(new_runs)} runs")

    if errors_manifest:
        err_manifest_path.write_text(
            json.dumps({"errors": errors_manifest}, indent=2),
            encoding="utf-8",
        )
        print(f"  Recorded {len(errors_manifest)} error(s)")


def normalize_existing_responses():
    """Strip _truncated from all existing collected responses."""
    count = 0
    for op_dir in COLLECTED.iterdir():
        if not op_dir.is_dir():
            continue
        for resp_f in op_dir.glob("resp_*.json"):
            try:
                resp = json.loads(resp_f.read_text(encoding="utf-8"))
                clean = _strip_truncated(resp)
                resp_f.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
                count += 1
            except (json.JSONDecodeError, OSError):
                pass
    if count:
        print(f"  Normalized {count} response file(s)")
    return count


def main():
    print("Phase 0: Preparation")
    print("1. Creating dirs...")
    ensure_dirs()
    print("2. Ensuring HAR at data/session.har...")
    ensure_har()
    print("3. Normalizing existing responses (strip _truncated)...")
    normalize_existing_responses()
    print("4. Migrating collected...")
    migrate_collected()
    print("Done.")
    return 0


if __name__ == "__main__":
    exit(main())
