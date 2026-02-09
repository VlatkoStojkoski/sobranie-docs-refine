#!/usr/bin/env python3
"""
Bootstrap docs/API.md from docs/API_DOCS.md and docs/API_INDEX.md.

Merges: API_INDEX (intro, routing, conventions, operations table) + API_DOCS
($defs, common, per-op schemas). Injects Common request filters, Common response
keys, and Notes slots for LLM refinement. See docs/API_MD_PIPELINE.md.

Run: python scripts/bootstrap_api_md.py [--output docs/API.md]
"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
API_INDEX = DOCS / "API_INDEX.md"
API_DOCS = DOCS / "API_DOCS.md"
DEFAULT_OUTPUT = DOCS / "API.md"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output path for API.md")
    args = parser.parse_args()

    if not API_INDEX.exists():
        print("ERROR: API_INDEX.md not found")
        return 1
    if not API_DOCS.exists():
        print("ERROR: API_DOCS.md not found")
        return 1

    index_content = API_INDEX.read_text(encoding="utf-8")
    docs_content = API_DOCS.read_text(encoding="utf-8")

    # API_DOCS: skip the first "# API Schemas" intro, keep from "## $defs" to end
    docs_start = docs_content.find("## $defs")
    if docs_start < 0:
        docs_section = docs_content
    else:
        docs_section = docs_content[docs_start:]

    # Inject Common request filters, Common response keys, and Notes slot before first operation
    notes_slots = """

## Common request filters

*(Add usage notes as refinement discovers them. Deduplicate: document each filter once here if used across multiple operations.)*

- **TypeId** — *(usage)*
- **StatusId** — *(usage)*
- **CommitteeId** — *(usage)*
- **StructureId** — *(usage)*
- **Page / Rows / CurrentPage** — *(usage)*
- **DateFrom / DateTo** — *(usage)*

## Common response keys

*(Add meaning/usage notes as refinement discovers them. Deduplicate globally.)*

- **TotalItems** — *(meaning)*
- **Items** — *(meaning)*
- **d** — *(meaning; ASMX-wrapped responses)*
- **Id / Title** — *(meaning when context-specific)*

---

"""
    # Insert after "## Common patterns" block, before first "## OperationName"
    match = re.search(r"(## Common patterns[\s\S]*?)(\n## [A-Za-z])", docs_section)
    if match:
        docs_section = docs_section[: match.end(1)] + notes_slots + docs_section[match.start(2) :]
    else:
        # Fallback: prepend before first ## that looks like an operation (GetAll...)
        first_op = re.search(r"\n## (GetAll[A-Za-z]+|Get[A-Z][a-zA-Z]+)\b", docs_section)
        if first_op:
            docs_section = docs_section[: first_op.start()] + notes_slots + docs_section[first_op.start() :]

    # Add ### Notes slot under first operation
    first_op_match = re.search(r"(## (GetAllApplicationTypes|GetAll[A-Za-z]+))\n\n(### Request)", docs_section)
    if first_op_match:
        docs_section = docs_section.replace(
            first_op_match.group(0),
            first_op_match.group(1) + "\n\n### Notes\n*(Add filter usage, key meanings, operation-specific notes here.)*\n\n" + first_op_match.group(3),
            1,
        )

    # Combine: full API_INDEX + separator + API_DOCS from $defs onward
    combined = index_content.rstrip() + "\n\n---\n\n# Schemas and per-operation reference\n\n" + docs_section

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(combined, encoding="utf-8")

    print(f"Bootstrap complete: {output_path}")
    return 0


if __name__ == "__main__":
    exit(main())
