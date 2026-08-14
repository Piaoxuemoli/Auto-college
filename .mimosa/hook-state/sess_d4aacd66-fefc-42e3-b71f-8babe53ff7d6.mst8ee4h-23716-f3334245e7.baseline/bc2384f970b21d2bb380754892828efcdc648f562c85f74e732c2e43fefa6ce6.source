"""
Index coursework source materials.

Usage:
    python index_source_files.py --inputs "task.docx|readings/" --output source_manifest.json
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys


CATEGORY_EXTENSIONS = {
    "requirement": {".doc", ".docx", ".pdf", ".md", ".txt"},
    "reading": {".pdf", ".epub", ".doc", ".docx"},
    "slides": {".ppt", ".pptx"},
    "data": {".csv", ".tsv", ".xls", ".xlsx", ".xlsm", ".json"},
    "image": {".png", ".jpg", ".jpeg", ".webp", ".gif"},
    "notes": {".md", ".txt", ".rtf"},
}

REQUIREMENT_HINTS = {"要求", "任务", "rubric", "requirement", "作业", "说明"}
IGNORED_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "outputs"}


def split_pipe_list(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    name = path.stem.lower()
    if any(hint in name for hint in REQUIREMENT_HINTS):
        return "requirement"
    if suffix in {".ppt", ".pptx"}:
        return "slides"
    if suffix in {".csv", ".tsv", ".xls", ".xlsx", ".xlsm", ".json"}:
        return "data"
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return "image"
    if suffix in {".md", ".txt", ".rtf"}:
        return "notes"
    if suffix in {".pdf", ".doc", ".docx", ".epub"}:
        return "reading"
    return "other"


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            print(f"WARNING: Source path does not exist: {path}", file=sys.stderr)
            continue
        if path.is_file():
            files.append(path)
            continue
        for child in path.rglob("*"):
            if any(part in IGNORED_DIRS for part in child.parts):
                continue
            if child.is_file():
                files.append(child)
    return sorted(set(files), key=lambda item: str(item).lower())


def build_manifest(inputs: list[str]) -> dict:
    input_paths = [Path(item).expanduser().resolve() for item in inputs]
    entries = []
    for path in iter_files(input_paths):
        try:
            size_bytes = path.stat().st_size
        except OSError:
            size_bytes = 0
        entries.append(
            {
                "path": str(path),
                "name": path.name,
                "extension": path.suffix.lower(),
                "category": category_for(path),
                "size_bytes": size_bytes,
            }
        )
    categories = {"requirement", "reading", "slides", "data", "image", "notes", "other"}
    return {
        "created_at": datetime.now().replace(microsecond=0).isoformat(),
        "input_paths": [str(path) for path in input_paths],
        "files": entries,
        "counts": {
            category: sum(1 for entry in entries if entry["category"] == category)
            for category in sorted(categories)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Index coursework-helper source materials.")
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    manifest = build_manifest(split_pipe_list(args.inputs))
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
