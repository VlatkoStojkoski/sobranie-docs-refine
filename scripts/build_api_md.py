#!/usr/bin/env python3
"""
Regenerate docs/API.md from docs/global.md + docs/ops/*.md.

Ops are concatenated in alphabetical order. Run after refine_api_md updates.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
GLOBAL_MD = DOCS / "global.md"
OPS_DIR = DOCS / "ops"
API_MD = DOCS / "API.md"


def build():
    global_content = GLOBAL_MD.read_text(encoding="utf-8")
    op_files = sorted(OPS_DIR.glob("*.md"))
    op_contents = []
    for p in op_files:
        op_contents.append(p.read_text(encoding="utf-8"))
    combined = global_content.rstrip()
    if op_contents:
        combined += "\n\n---\n\n" + "\n\n---\n\n".join(op_contents)
    API_MD.write_text(combined, encoding="utf-8")
    print(f"Built {API_MD} ({len(combined)} chars)")
    return 0


if __name__ == "__main__":
    exit(build())
