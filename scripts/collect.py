#!/usr/bin/env python3
"""
Pipeline-based request collection.

Reads config/generators.json (pipeline format), sends requests to the Sobranie API,
saves req/res pairs to collected/. Pipelines chain stages: each stage can extract IDs
from responses and pass them to later stages via a shared store.

Run: python scripts/collect.py [--no-cache] [--pipeline NAME]
"""

import argparse
import hashlib
import json
import logging
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from jsonpath_ng.ext import parse as jp_parse

ROOT = Path(__file__).parent.parent
CONFIG = ROOT / "config"
COLLECTED = ROOT / "collected"
ERRORS = ROOT / "errors"
LOGS = ROOT / "logs" / "collect"

DEFAULT_URL = "https://www.sobranie.mk/Routing/MakePostRequest"
DELAY = 0.6


# --- HTTP ---

def post(url: str, payload: dict, use_cache: bool, cache_get, cache_set):
    if use_cache:
        cached = cache_get(url, payload)
        if cached is not None:
            return cached
    try:
        import requests
        r = requests.post(url, json=payload, timeout=(5, 60))
        if r.status_code == 200:
            data = r.json()
            if use_cache:
                cache_set(url, payload, data)
            return data
        return {"_error": r.status_code, "_body": (r.text or "")[:300]}
    except Exception as e:
        return {"_error": type(e).__name__, "_body": str(e)[:300]}


def is_error(resp) -> bool:
    return isinstance(resp, dict) and resp.get("_error") is not None


def is_permanent_client_error(resp) -> bool:
    """4xx errors are treated as deterministic for this payload."""
    if not is_error(resp):
        return False
    code = resp.get("_error")
    return isinstance(code, int) and 400 <= code < 500


# --- Jsonpath extraction ---

def jp_extract(data, path: str) -> list:
    """Extract values from data using a jsonpath expression."""
    expr = jp_parse(path)
    return [m.value for m in expr.find(data) if m.value]


# --- Param generation ---

def _aspdate_to_year(asp: str) -> int | None:
    if not isinstance(asp, str):
        return None
    m = re.search(r"/Date\((\d+)\)/", asp)
    if not m:
        return None
    try:
        return datetime.fromtimestamp(int(m.group(1)) / 1000.0).year
    except (ValueError, OSError):
        return None


def generate_value(gen: dict, store: dict, globals_: dict, picked: dict) -> object:
    """Generate a parameter value from a generator spec or a store source.

    `picked` tracks already-chosen items for paired sources (same dict used
    across all params in one body generation so paired fields stay matched).
    """
    if "source" in gen:
        src = gen["source"]
        # Paired source: "storeName.field" — pick one dict from store[storeName],
        # reuse the same pick for all fields from the same storeName.
        if "." in src:
            store_key, field = src.split(".", 1)
            items = store.get(store_key, [])
            if not items:
                return None
            if store_key not in picked:
                picked[store_key] = random.choice(items)
            return picked[store_key].get(field)
        # Simple source: pick a random value from the list.
        vals = store.get(src, [])
        return random.choice(vals) if vals else None
    g = gen.get("generator", "constant")
    if g == "constant":
        return gen.get("value")
    if g == "range":
        return random.randint(int(gen.get("min", 0)), int(gen.get("max", 10)))
    if g == "current_structure":
        return globals_.get("current_structure")
    if g == "current_structure_year":
        years = globals_.get("current_structure_years")
        if years and len(years) == 2:
            lo, hi = years[0], min(years[1], datetime.now().year)
            return random.randint(lo, hi) if lo <= hi else datetime.now().year
        return datetime.now().year
    if g == "object":
        return {k: generate_value(v, store, globals_, picked) for k, v in (gen.get("properties") or {}).items()}
    return None


def generate_body(params: dict, store: dict, globals_: dict) -> dict:
    picked: dict = {}  # tracks paired source picks for this body
    return {k: generate_value(v, store, globals_, picked) for k, v in params.items()}


def body_hash(body: dict) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


# --- Bootstrap: get current structure ---

def bootstrap_structure(use_cache, cache_get, cache_set, log) -> dict:
    """Call GetAllStructuresForFilter to get current structure ID and year range."""
    globals_ = {}
    body = {"methodName": "GetAllStructuresForFilter", "languageId": 1}
    resp = post(DEFAULT_URL, body, use_cache, cache_get, cache_set)
    if is_error(resp) or not isinstance(resp, list):
        log.warning("Bootstrap: GetAllStructuresForFilter failed or unexpected format")
        return globals_
    for item in resp:
        if isinstance(item, dict) and item.get("IsCurrent") and item.get("Id"):
            globals_["current_structure"] = item["Id"]
            y_from = _aspdate_to_year(item.get("DateFrom") or "")
            y_to = _aspdate_to_year(item.get("DateTo") or "")
            if y_from is not None:
                y_to = y_to if y_to is not None else datetime.now().year
                globals_["current_structure_years"] = [y_from, min(y_to, datetime.now().year)]
            break
    if "current_structure" not in globals_ and resp:
        first = resp[0]
        if isinstance(first, dict) and first.get("Id"):
            globals_["current_structure"] = first["Id"]
    log.info(f"Bootstrap: structure={globals_.get('current_structure', '?')}")
    return globals_


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Pipeline-based request collection.")
    parser.add_argument("--no-cache", action="store_true", help="Skip API response cache")
    parser.add_argument("--pipeline", type=str, default=None, help="Run only this pipeline (by name)")
    args = parser.parse_args()
    use_cache = not args.no_cache

    sys.path.insert(0, str(ROOT / "scripts"))
    from cache import get as cache_get, set_ as cache_set

    cfg_path = CONFIG / "generators.json"
    if not cfg_path.exists():
        print("ERROR: config/generators.json not found")
        return 1

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    pipelines = cfg.get("pipelines", [])
    if not pipelines:
        print("ERROR: no pipelines in config")
        return 1

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = LOGS / run_id
    log_dir.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger("collect")
    log.setLevel(logging.DEBUG)
    log.handlers.clear()
    fh = logging.FileHandler(log_dir / "collect.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(ch)

    log.info(f"Collect run {run_id} | cache={'on' if use_cache else 'off'}")

    # Bootstrap: get current structure
    globals_ = bootstrap_structure(use_cache, cache_get, cache_set, log)

    # Ensure first-run directories exist before reading/iterating.
    COLLECTED.mkdir(parents=True, exist_ok=True)
    ERRORS.mkdir(parents=True, exist_ok=True)

    # Load existing manifest and counters
    manifest = {"runs": []}
    if (COLLECTED / "manifest.json").exists():
        manifest = json.loads((COLLECTED / "manifest.json").read_text(encoding="utf-8"))
    errors_manifest = {"errors": []}
    if (COLLECTED / "errors_manifest.json").exists():
        errors_manifest = json.loads((COLLECTED / "errors_manifest.json").read_text(encoding="utf-8"))

    op_counters: dict[str, int] = {}
    for op_dir in COLLECTED.iterdir():
        if op_dir.is_dir():
            for f in op_dir.glob("req_*.json"):
                try:
                    n = int(f.stem.split("_")[1])
                    op_counters[op_dir.name] = max(op_counters.get(op_dir.name, 0), n)
                except (ValueError, IndexError):
                    pass

    # Global dedup of finalized outcomes:
    # - successful requests
    # - deterministic client errors (4xx)
    # Transient failures are intentionally NOT finalized so retries can re-send.
    finalized: set[str] = set()

    run_pairs = []
    start_time = time.perf_counter()
    req_count = 0
    err_count = 0

    # Filter pipelines
    if args.pipeline:
        pipelines = [p for p in pipelines if p.get("name") == args.pipeline]
        if not pipelines:
            log.error(f"Pipeline '{args.pipeline}' not found")
            return 1

    total_calls = sum(
        s.get("calls", 1) for p in pipelines for s in p.get("stages", [])
    )
    log.info(f"Pipelines: {len(pipelines)}, total planned calls: {total_calls}")

    def run_stage(stage, store):
        """Execute a single pipeline stage. Returns (requests_made, errors_made)."""
        nonlocal req_count, err_count, globals_

        op = stage["operation"]
        calls = stage.get("calls", 1)
        params = stage.get("params", {})
        extract = stage.get("extract", {})
        url = stage.get("url", DEFAULT_URL)

        op_dir = COLLECTED / op
        op_dir.mkdir(parents=True, exist_ok=True)
        (ERRORS / op).mkdir(parents=True, exist_ok=True)

        # Cap calls to available source IDs
        source_fields = [v["source"] for v in params.values() if isinstance(v, dict) and "source" in v]
        if source_fields:
            store_keys = set(sf.split(".")[0] for sf in source_fields)
            available = min(len(store.get(sk, [])) for sk in store_keys)
            actual_calls = min(calls, available)
            if actual_calls == 0:
                log.warning(f"  {op}: no IDs available, skipping")
                return 0, 0
            if actual_calls < calls:
                log.info(f"  {op}: capped {calls} -> {actual_calls} (available IDs)")
        else:
            actual_calls = calls

        log.info(f"  {op} (n={actual_calls})")
        stage_reqs = 0
        stage_errs = 0

        for _ in range(actual_calls):
            body = generate_body(params, store, globals_)

            dedup_key = f"{op}:{body_hash(body)}"
            if dedup_key in finalized:
                log.debug(f"    {op} skipped (duplicate)")
                continue

            op_counters[op] = op_counters.get(op, 0) + 1
            nnn = f"{op_counters[op]:03d}"

            resp = post(url, body, use_cache, cache_get, cache_set)
            time.sleep(DELAY)

            (op_dir / f"req_{nnn}.json").write_text(
                json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8",
            )

            req_count += 1
            stage_reqs += 1
            if is_error(resp):
                err_count += 1
                stage_errs += 1
                log.warning(f"    {op} req_{nnn} -> ERR {resp.get('_error', '?')}")
                log.debug(f"    {op} req_{nnn} error: {resp.get('_body', '')[:200]}")
                if is_permanent_client_error(resp):
                    finalized.add(dedup_key)
                (ERRORS / op / f"err_{nnn}.json").write_text(
                    json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8",
                )
                errors_manifest["errors"].append({
                    "req": f"{op}/req_{nnn}.json", "error": f"{op}/err_{nnn}.json",
                })
            else:
                finalized.add(dedup_key)
                log.debug(f"    {op} req_{nnn} -> OK")
                (op_dir / f"resp_{nnn}.json").write_text(
                    json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8",
                )
                run_pairs.append({
                    "req": f"{op}/req_{nnn}.json", "resp": f"{op}/resp_{nnn}.json",
                })

                # Extract IDs into store for later stages
                for store_key, extractor in extract.items():
                    if isinstance(extractor, str):
                        ids = jp_extract(resp, extractor)
                        store.setdefault(store_key, []).extend(ids)
                    elif isinstance(extractor, dict) and "from" in extractor:
                        parent_expr = jp_parse(extractor["from"])
                        pick = extractor.get("pick", {})
                        for match in parent_expr.find(resp):
                            obj = match.value
                            row = {}
                            for field_key, sub_path in pick.items():
                                sub_expr = jp_parse(sub_path)
                                sub_matches = sub_expr.find(obj)
                                if sub_matches and sub_matches[0].value:
                                    row[field_key] = sub_matches[0].value
                            if len(row) == len(pick):
                                store.setdefault(store_key, []).append(row)

                if op == "GetAllStructuresForFilter" and "current_structure" not in globals_:
                    globals_ = bootstrap_structure(use_cache, cache_get, cache_set, log)

        log.info(f"    Progress: {req_count} sent, {err_count} err")
        return stage_reqs, stage_errs

    def _needs_from_store(stage) -> set[str]:
        """Return store keys that a stage's downstream stages need."""
        return set(
            sf.split(".")[0]
            for v in stage.get("params", {}).values()
            if isinstance(v, dict) and "source" in v
            for sf in [v["source"]]
        )

    def _produces_store_keys(stage) -> set[str]:
        """Return store keys that a stage's extract populates."""
        return set(stage.get("extract", {}).keys())

    for pipeline in pipelines:
        name = pipeline.get("name", "unnamed")
        stages = pipeline.get("stages", [])
        store: dict[str, list] = {}

        log.info(f"Pipeline: {name} ({len(stages)} stages)")

        for i, stage in enumerate(stages):
            run_stage(stage, store)

            # Check if any later stage needs store keys that this stage produces
            # but got nothing. If so, retry this stage and its feeder (x2, x2, x2).
            produced = _produces_store_keys(stage)
            if not produced:
                continue

            empty_keys = [k for k in produced if not store.get(k)]
            if not empty_keys:
                continue

            # Find which downstream stages need these empty keys
            downstream_needs = set()
            for later in stages[i + 1:]:
                downstream_needs |= _needs_from_store(later)
            if not (downstream_needs & produced):
                continue

            # Retry: re-run this stage's feeder chain (stages 0..i) with x2 calls
            # up to 3 retries
            for retry in range(1, 4):
                multiplier = 2 ** retry
                log.info(f"  Retry {retry}/3: store keys {empty_keys} empty, re-running stages 0..{i} (x{multiplier})")
                for j in range(i + 1):
                    retry_stage = dict(stages[j])
                    retry_stage["calls"] = stages[j].get("calls", 1) * multiplier
                    run_stage(retry_stage, store)
                empty_keys = [k for k in produced if not store.get(k)]
                if not empty_keys:
                    log.info(f"  Retry {retry}/3: success, store keys populated")
                    break
            else:
                if empty_keys:
                    log.warning(f"  After 3 retries, store keys still empty: {empty_keys}")

    elapsed = time.perf_counter() - start_time
    log.info(f"Done: {len(run_pairs)} pairs saved, {err_count} errors, {elapsed:.1f}s")

    manifest["runs"].append({"run_id": run_id, "pairs": run_pairs})
    (COLLECTED / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (COLLECTED / "errors_manifest.json").write_text(json.dumps(errors_manifest, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    exit(main())
