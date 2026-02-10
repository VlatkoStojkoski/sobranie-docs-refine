"""
File-based cache for API requests. Keys by (url, payload JSON).
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE_DIR = ROOT / ".api_cache"


def _key(url: str, payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True)
    h = hashlib.sha256(f"{url}\n{body}".encode()).hexdigest()
    return h[:32]  # Use 32 chars (128 bits) to avoid collision risk


def get(url: str, payload: dict) -> dict | None:
    """Return cached response or None."""
    k = _key(url, payload)
    path = CACHE_DIR / f"{k}.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("response")
    except (json.JSONDecodeError, OSError):
        return None


def set_(url: str, payload: dict, response) -> None:
    """Cache a response."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    k = _key(url, payload)
    path = CACHE_DIR / f"{k}.json"
    path.write_text(
        json.dumps({"url": url, "payload": payload, "response": response}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
