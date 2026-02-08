#!/usr/bin/env python3
"""
Deduplicate HAR_ANALYSIS_FINDINGS.md by (URL, Method Name).
Keeps first occurrence of each unique endpoint.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FINDINGS_FILE = REPO_ROOT / "HAR_ANALYSIS_FINDINGS.md"


def parse_entries(content: str) -> tuple[str, list[tuple[tuple[str, str], str, str]]]:
    """Parse markdown into (header, [(dedup_key, index, block), ...])"""
    entries = []
    # Split on double newline before entry header
    blocks = re.split(r'\n\n(?=## Entry from logs\.har \(index \d+\))', content)

    # First block is the header (before first entry)
    header = blocks[0]
    blocks = blocks[1:]

    for block in blocks:
        if not block.strip():
            continue
        # Extract index from "## Entry from logs.har (index N)"
        idx_match = re.search(r'## Entry from logs\.har \(index (\d+)\)', block)
        index = idx_match.group(1) if idx_match else "?"

        # Extract URL
        url_match = re.search(r'\*\*URL\*\*:\s*`([^`]+)`', block)
        url = url_match.group(1).strip() if url_match else ""

        # Extract Method Name (next line after **Method Name**)
        method_match = re.search(r'\*\*Method Name\*\*\s*\n([^\n*]+)', block)
        method = method_match.group(1).strip() if method_match else ""
        # Normalize: strip leading slash for consistency (GetAllQuestions vs /GetAllQuestions)
        method_normalized = method.lstrip("/")

        dedup_key = (url, method_normalized)
        entries.append((dedup_key, index, block))

    return header, entries


def main():
    content = FINDINGS_FILE.read_text(encoding="utf-8")
    header, entries = parse_entries(content)

    seen: dict[tuple[str, str], tuple[str, str]] = {}  # key -> (index, block)
    for (url, method), index, block in entries:
        key = (url, method)
        if key not in seen:
            seen[key] = (index, block)

    unique_entries = list(seen.values())  # insertion order = first occurrence

    # Rebuild document
    new_content = header.rstrip()
    if not new_content.endswith("---"):
        new_content += "\n\n---\n\n"
    else:
        new_content += "\n\n"

    for i, (index, block) in enumerate(unique_entries, start=1):
        # Update the header to show it's a unique entry (optional: renumber)
        block_clean = block.strip()
        new_content += block_clean
        if i < len(unique_entries):
            new_content += "\n\n---\n\n"

    # Update header stats - match full line (including any prior dedup suffix)
    original_count = len(entries)
    unique_count = len(unique_entries)
    new_content = re.sub(
        r"(- \*\*Analyzed \(Level 2\)\*\*: )[^\n]+",
        rf"\g<1>{unique_count} (deduplicated from {original_count})",
        new_content,
        count=1,
    )

    FINDINGS_FILE.write_text(new_content, encoding="utf-8")
    print(f"Deduplicated: {original_count} -> {unique_count} unique entries")
    print(f"Removed {original_count - unique_count} duplicates")


if __name__ == "__main__":
    main()
