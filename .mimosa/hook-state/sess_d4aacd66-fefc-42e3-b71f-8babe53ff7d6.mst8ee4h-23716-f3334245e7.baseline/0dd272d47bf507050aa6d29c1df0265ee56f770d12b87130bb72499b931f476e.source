"""
Index lab-report source files from files or directories.

Usage:
    python index_source_files.py --inputs "manual.pdf|materials/" --output source_manifest.json

The manifest lets the orchestrator pass a whole material folder to downstream agents without
asking the user to classify every file.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys


CATEGORY_EXTENSIONS = {
    "manual": {".pdf", ".doc", ".docx", ".md", ".txt"},
    "slides": {".ppt", ".pptx"},
    "data": {".csv", ".tsv", ".xls", ".xlsx", ".xlsm", ".json"},
    "image": {".png", ".jpg", ".jpeg", ".webp", ".gif"},
    "log": {".log", ".out", ".err"},
    "code": {
        ".py",
        ".ipynb",
        ".js",
        ".ts",
        ".java",
        ".c",
        ".cc",
        ".cpp",
        ".h",
        ".hpp",
        ".cs",
        ".go",
        ".rs",
        ".m",
        ".sh",
        ".ps1",
        ".bat",
        ".sql",
    },
}

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "outputs",
}


def split_pipe_list(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if suffix in extensions:
            return category
    return "other"


def iter_files(input_paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for input_path in input_paths:
        if not input_path.exists():
            print(f"WARNING: Source path does not exist: {input_path}", file=sys.stderr)
            continue
        if input_path.is_file():
            files.append(input_path)
            continue

        for child in input_path.rglob("*"):
            if any(part in IGNORED_DIRS for part in child.parts):
                continue
            if child.is_file():
                files.append(child)

    return sorted(set(files), key=lambda path: str(path).lower())


def build_manifest(input_paths: list[str]) -> dict:
    resolved_inputs = [Path(item).expanduser().resolve() for item in input_paths]
    files = iter_files(resolved_inputs)
    entries = []
    for file_path in files:
        try:
            size_bytes = file_path.stat().st_size
        except OSError:
            size_bytes = 0
        entries.append(
            {
                "path": str(file_path),
                "name": file_path.name,
                "extension": file_path.suffix.lower(),
                "category": category_for(file_path),
                "size_bytes": size_bytes,
            }
        )

    return {
        "created_at": datetime.now().replace(microsecond=0).isoformat(),
        "input_paths": [str(path) for path in resolved_inputs],
        "files": entries,
        "counts": {
            category: sum(1 for entry in entries if entry["category"] == category)
            for category in sorted({entry["category"] for entry in entries} | set(CATEGORY_EXTENSIONS) | {"other"})
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create source_manifest.json for lab-report.")
    parser.add_argument(
        "--inputs",
        required=True,
        help="Pipe-separated files or directories, e.g. 'manual.pdf|materials/'."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to write source_manifest.json."
    )
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
