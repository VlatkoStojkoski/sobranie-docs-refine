#!/usr/bin/env python3
"""
Split docs/API.md into docs/global.md and docs/ops/<Operation>.md.

Run once to migrate to split-docs structure. After that, refine_api_md uses
global + per-op files; build_api_md regenerates API.md.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
API_MD = DOCS / "API.md"
GLOBAL_MD = DOCS / "global.md"
OPS_DIR = DOCS / "ops"


def _find_op_headers(lines: list[str]) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(lines):
        m = re.match(r"^## (GetAll[A-Za-z]+|Get[A-Z][a-zA-Z]+|Load[A-Za-z]+)$", line.strip())
        if m:
            out.append((i, m.group(1)))
    return out


def split():
    content = API_MD.read_text(encoding="utf-8")
    lines = content.split("\n")
    op_headers = _find_op_headers(lines)
    if not op_headers:
        print("No operation headers found in API.md")
        return 1

    # Global: lines 0 .. first op header (exclusive)
    global_end = op_headers[0][0]
    global_content = "\n".join(lines[:global_end])
    GLOBAL_MD.parent.mkdir(parents=True, exist_ok=True)
    GLOBAL_MD.write_text(global_content, encoding="utf-8")
    print(f"Wrote {GLOBAL_MD} ({len(lines[:global_end])} lines)")

    OPS_DIR.mkdir(parents=True, exist_ok=True)
    for idx, (start, op_name) in enumerate(op_headers):
        end = op_headers[idx + 1][0] if idx + 1 < len(op_headers) else len(lines)
        op_content = "\n".join(lines[start:end])
        op_path = OPS_DIR / f"{op_name}.md"
        op_path.write_text(op_content, encoding="utf-8")
        print(f"  {op_name}.md ({end - start} lines)")
    print(f"Wrote {len(op_headers)} op files to {OPS_DIR}")
    return 0


if __name__ == "__main__":
    exit(split())
