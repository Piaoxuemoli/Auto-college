"""
Check organization quality for coursework-helper final_slides.md.

Usage:
    python check_slides_md.py outputs/<assignment>/final_slides.md
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys


SLIDE_RE = re.compile(r"^# Slide\s+\d+:", re.MULTILINE)
META_RE = re.compile(r"<!--\s*slide:\s*(.*?)\s*-->")
FIELD_RE = re.compile(r"(role|section|layout)=([^\s]+)")


def parse_metadata(text: str) -> list[dict[str, str]]:
    metadata = []
    for match in META_RE.finditer(text):
        fields = dict(FIELD_RE.findall(match.group(1)))
        metadata.append(fields)
    return metadata


def longest_same_run(values: list[str]) -> int:
    longest = 0
    current = 0
    previous = None
    for value in values:
        if value == previous:
            current += 1
        else:
            current = 1
            previous = value
        longest = max(longest, current)
    return longest


def validate(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    slide_count = len(SLIDE_RE.findall(text))
    metadata = parse_metadata(text)
    warnings: list[str] = []
    errors: list[str] = []

    if slide_count == 0:
        errors.append("No '# Slide N:' headings found.")
        return errors, warnings

    if len(metadata) < slide_count:
        errors.append("Each slide should have a metadata comment: <!-- slide: role=... section=... layout=... -->.")

    missing_key_messages = max(0, slide_count - len(re.findall(r"^Key message:", text, re.MULTILINE)))
    if missing_key_messages:
        errors.append(f"{missing_key_messages} slide(s) are missing 'Key message:'.")

    missing_visible_blocks = max(0, slide_count - len(re.findall(r"^Visible content:", text, re.MULTILINE)))
    if missing_visible_blocks:
        warnings.append(f"{missing_visible_blocks} slide(s) are missing 'Visible content:'.")

    missing_notes = max(0, slide_count - len(re.findall(r"^Speaker notes:", text, re.MULTILINE)))
    if missing_notes:
        warnings.append(f"{missing_notes} slide(s) are missing speaker notes.")

    sections = [item.get("section", "") for item in metadata if item.get("section")]
    layouts = [item.get("layout", "") for item in metadata if item.get("layout")]

    if slide_count > 8 and len(set(sections)) < 3:
        errors.append("Decks longer than 8 slides should have at least 3 sections.")

    if slide_count > 6 and len(set(layouts)) < 3:
        warnings.append("Use at least 3 distinct layouts for non-trivial decks.")

    if longest_same_run(layouts) > 3:
        errors.append("More than 3 consecutive slides use the same layout.")

    role_counts = Counter(item.get("role", "") for item in metadata)
    if slide_count > 8 and not role_counts.get("transition"):
        warnings.append("Long decks benefit from at least one transition/section-divider slide.")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Check final_slides.md organization.")
    parser.add_argument("slides_path")
    args = parser.parse_args()

    path = Path(args.slides_path)
    if not path.exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    errors, warnings = validate(path)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        sys.exit(2)
    print("Slide organization check passed.")


if __name__ == "__main__":
    main()
