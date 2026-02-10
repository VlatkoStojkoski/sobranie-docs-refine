#!/usr/bin/env python3
"""
Phase 3: Config-driven collection. Generate request bodies, send, save. No truncation.

Run: python scripts/phase3_collect.py [--no-cache]
"""

import argparse
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONFIG = ROOT / "config"
COLLECTED = ROOT / "collected"
ERRORS = ROOT / "errors"
LISTING_CACHE = ROOT / "listing_cache"

API = "https://www.sobranie.mk/Routing/MakePostRequest"
CALENDAR = "https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar"
LOAD_LANG = "https://www.sobranie.mk/Infrastructure/LoadLanguage"
OFFICIAL_VISITS = "https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser"
DELAY = 0.6


def post(url: str, payload: dict, use_cache: bool, cache_get, cache_set):
    if use_cache:
        cached = cache_get(url, payload)
        if cached is not None:
            return cached
    try:
        import requests
        r = requests.post(url, json=payload, timeout=(5, 30))
        if r.status_code == 200:
            data = r.json()
            if use_cache:
                cache_set(url, payload, data)
            return data
        return {"_error": r.status_code, "_body": (r.text or "")[:300]}
    except Exception as e:
        return {"_error": "timeout", "_body": str(e)[:300]}


def is_error(resp) -> bool:
    return isinstance(resp, dict) and resp.get("_error") is not None


def extract_ids(resp, field: str) -> list:
    ids = []
    if not isinstance(resp, dict):
        return ids
    for key in ["Items", "d", "MembersOfParliament"]:
        items = resp.get(key)
        if isinstance(items, list):
            for x in items:
                if isinstance(x, dict) and field in x and x[field]:
                    ids.append(x[field])
    return ids


def get_url(op: str, op_cfg: dict) -> str:
    url = op_cfg.get("url") or API
    if "LoadLanguage" in op:
        return LOAD_LANG
    if "GetCustomEventsCalendar" in op:
        return CALENDAR
    if "GetOfficialVisitsForUser" in op:
        return OFFICIAL_VISITS
    return url if url.startswith("http") else API


def _generate_value(gen: dict, catalog: dict, listing_ids: dict, op_cfg: dict) -> object:
    """Generate a single value from a generator spec."""
    g = gen.get("generator", "constant")
    if g == "constant":
        return gen.get("value")
    if g == "enum":
        vals = gen.get("values", [])
        return random.choice(vals) if vals else None
    if g == "range":
        lo, hi = int(gen.get("min", 0)), int(gen.get("max", 10))
        return random.randint(lo, hi)
    if g == "catalog":
        src = gen.get("source", "")
        fld = gen.get("field", "Id")
        vals = catalog.get(src, {}).get(fld, catalog.get(src, {}).get("Id", []))
        return random.choice(vals) if vals else None
    if g == "uuid_from_listing":
        id_src = op_cfg.get("id_source", {})
        src_op = id_src.get("operation", "")
        vals = listing_ids.get(src_op, [])
        return random.choice(vals) if vals else None
    if g == "object":
        out = {}
        for pk, pgen in (gen.get("properties") or {}).items():
            out[pk] = _generate_value(pgen, catalog, listing_ids, op_cfg)
        return out
    return None


def generate_body(op: str, op_cfg: dict, catalog: dict, listing_ids: dict) -> dict:
    body = {}
    for k, gen in (op_cfg.get("fields") or {}).items():
        body[k] = _generate_value(gen, catalog, listing_ids, op_cfg)
    return body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument(
        "--config",
        default=None,
        help="Path to generators config (default: config/generators.json)",
    )
    args = parser.parse_args()
    use_cache = not args.no_cache

    sys.path.insert(0, str(ROOT / "scripts"))
    from cache import get as cache_get, set_ as cache_set

    cfg_path = Path(args.config) if args.config else CONFIG / "generators.json"
    if not cfg_path.is_absolute():
        cfg_path = ROOT / cfg_path
    if not cfg_path.exists():
        print("ERROR: Config not found:", cfg_path)
        return 1

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    ops = cfg.get("operations", {})
    default_n = cfg.get("sample_size_default", 5)
    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    LISTING_CACHE.mkdir(parents=True, exist_ok=True)
    cache_index = []
    if (LISTING_CACHE / "index.json").exists():
        try:
            cache_index = json.loads((LISTING_CACHE / "index.json").read_text(encoding="utf-8"))
        except Exception:
            pass
    if not isinstance(cache_index, list):
        cache_index = []

    catalog: dict[str, dict[str, list]] = {}
    listing_ids: dict[str, list] = {}

    non_detail = [o for o, c in ops.items() if c.get("type") != "detail"]
    detail = [o for o, c in ops.items() if c.get("type") == "detail"]
    order = non_detail + detail

    manifest = {"runs": []}
    if (COLLECTED / "manifest.json").exists():
        manifest = json.loads((COLLECTED / "manifest.json").read_text(encoding="utf-8"))
    errors_manifest = {"errors": []}
    if (COLLECTED / "errors_manifest.json").exists():
        errors_manifest = json.loads((COLLECTED / "errors_manifest.json").read_text(encoding="utf-8"))

    run_pairs = []
    op_counters: dict[str, int] = {}
    for op_dir in [COLLECTED / o for o in ops]:
        if op_dir.exists():
            for f in op_dir.glob("req_*.json"):
                try:
                    n = int(f.stem.split("_")[1])
                    op_counters[op_dir.name] = max(op_counters.get(op_dir.name, 0), n)
                except (ValueError, IndexError):
                    pass

    for op in order:
        op_cfg = ops.get(op, {})
        n = op_cfg.get("sample_size") or default_n
        url = get_url(op, op_cfg)
        op_dir = COLLECTED / op
        op_dir.mkdir(parents=True, exist_ok=True)
        (ERRORS / op).mkdir(parents=True, exist_ok=True)

        for _ in range(n):
            op_counters[op] = op_counters.get(op, 0) + 1
            nnn = f"{op_counters[op]:03d}"
            body = generate_body(op, op_cfg, catalog, listing_ids)
            resp = post(url, body, use_cache, cache_get, cache_set)
            time.sleep(DELAY)

            (op_dir / f"req_{nnn}.json").write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")

            if is_error(resp):
                (ERRORS / op / f"err_{nnn}.json").write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")
                errors_manifest["errors"].append({"req": f"{op}/req_{nnn}.json", "error": f"{op}/err_{nnn}.json"})
            else:
                (op_dir / f"resp_{nnn}.json").write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")
                run_pairs.append({"req": f"{op}/req_{nnn}.json", "resp": f"{op}/resp_{nnn}.json"})

            for fld in ["Id", "UserId", "CommitteeId", "SittingId", "MaterialId", "QuestionId", "parliamentaryGroupId", "politicalPartyId", "mpsClubId"]:
                ids = extract_ids(resp, fld)
                listing_ids.setdefault(op, []).extend(ids)
                catalog.setdefault(op, {}).setdefault(fld, []).extend(ids)
            catalog.setdefault(op, {}).setdefault("Id", []).extend(extract_ids(resp, "Id"))

            path = LISTING_CACHE / f"{run_id}_{op}_{nnn}.json"
            path.write_text(json.dumps({"request": body, "response": resp, "extracted_ids": list(set(listing_ids.get(op, []))), "item_count": len(resp.get("Items") or []) if isinstance(resp, dict) else 0}, ensure_ascii=False, indent=2), encoding="utf-8")
            cache_index.append({"run_id": run_id, "operation": op, "path": str(path.relative_to(ROOT))})

    manifest["runs"].append({"run_id": run_id, "pairs": run_pairs})
    (COLLECTED / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (COLLECTED / "errors_manifest.json").write_text(json.dumps(errors_manifest, indent=2), encoding="utf-8")
    (LISTING_CACHE / "index.json").write_text(json.dumps(cache_index, indent=2), encoding="utf-8")

    print(f"Phase 3 done. Run {run_id}. {len(run_pairs)} pairs saved.")
    return 0


if __name__ == "__main__":
    exit(main())
