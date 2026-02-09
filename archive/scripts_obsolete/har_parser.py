"""
HAR parser: extract API request bodies from HAR file, grouped by operation.
"""

import json
from pathlib import Path
from collections import defaultdict

SOBRANIE_URLS = (
    "sobranie.mk/Routing/MakePostRequest",
    "sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar",
    "sobranie.mk/Infrastructure/LoadLanguage",
    "sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser",
)


def _is_sobranie_request(url: str) -> bool:
    return any(part in url for part in SOBRANIE_URLS)


def _operation_from_body(body: dict, url: str) -> str | None:
    """Derive operation name from request body or URL."""
    if body:
        name = body.get("methodName") or body.get("MethodName")
        if name:
            return name.lstrip("/")
    if "GetCustomEventsCalendar" in url:
        return "GetCustomEventsCalendar"
    if "LoadLanguage" in url:
        return "LoadLanguage"
    if "GetOfficialVisitsForUser" in url:
        return "GetOfficialVisitsForUser"
    return None


def extract_requests(har_path: Path) -> dict[str, list[dict]]:
    """
    Extract request bodies from HAR, grouped by operation.

    Returns: { "GetAllSittings": [req1, req2, ...], ... }
    """
    data = json.loads(har_path.read_text(encoding="utf-8"))
    entries = data.get("log", {}).get("entries", [])

    by_op: dict[str, list[dict]] = defaultdict(list)

    for entry in entries:
        req = entry.get("request", {})
        url = req.get("url", "")
        if not _is_sobranie_request(url):
            continue
        if req.get("method") != "POST":
            continue

        post_data = req.get("postData") or {}
        text = post_data.get("text") or ""
        body: dict = {}
        if text.strip():
            try:
                body = json.loads(text)
            except json.JSONDecodeError:
                continue

        op = _operation_from_body(body, url)
        if op:
            by_op[op].append(body)

    return dict(by_op)
