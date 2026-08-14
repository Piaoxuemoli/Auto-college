"""Initialize the output directory structure for study-index.

Usage:
    python init_output_dir.py <course-name> \
        --source-files "file1.pptx|file2.pdf" \
        --delivery-formats "md|pdf"
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
_OUTPUTS_ROOT = _SKILL_ROOT / "outputs"

_DIRS = [
    "00_admin",
    "01_extracted",
    "02_outline",
    "03_drafts",
    "04_final",
    "05_exports",
    "06_qa",
    "assets",
]

_FILES = {
    "00_admin/study_context.json": None,
    "00_admin/extract_manifest.json": None,
    "02_outline/outline.md": "",
    "03_drafts/draft_handbook.md": "",
    "04_final/final_handbook.md": "",
    "05_exports/": None,
    "06_qa/qa_report.md": "",
}


def _validate_name(name: str) -> str:
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        print(f"Error: name must be lowercase-with-hyphens, got: {name}",
              file=sys.stderr)
        sys.exit(1)
    if len(name) > 64:
        print(f"Error: name too long (max 64 chars), got: {len(name)}",
              file=sys.stderr)
        sys.exit(1)
    return name


def _parse_formats(fmt_str: str) -> List[str]:
    valid = {"md", "pdf", "docx", "pptx"}
    formats = [f.strip().lower() for f in fmt_str.split("|") if f.strip()]
    for f in formats:
        if f not in valid:
            print(f"Warning: unknown format '{f}', ignoring", file=sys.stderr)
    return [f for f in formats if f in valid]


def main():
    parser = argparse.ArgumentParser(
        description="Initialize study-index output directory")
    parser.add_argument("name", help="Course name (lowercase-with-hyphens)")
    parser.add_argument("--source-files", default="",
                        help="Pipe-separated list of source files")
    parser.add_argument("--delivery-formats", default="md|pdf",
                        help="Pipe-separated output formats (default: md|pdf)")
    args = parser.parse_args()

    name = _validate_name(args.name)
    formats = _parse_formats(args.delivery_formats)
    source_files = [s.strip() for s in args.source_files.split("|")
                    if s.strip()]

    out_dir = _OUTPUTS_ROOT / name
    if out_dir.exists():
        print(f"Warning: {out_dir} already exists, adding missing files only",
              file=sys.stderr)

    # Create directories
    for d in _DIRS:
        (out_dir / d).mkdir(parents=True, exist_ok=True)

    # Create placeholder files
    for fpath, content in _FILES.items():
        full = out_dir / fpath
        if fpath.endswith("/"):
            full.mkdir(parents=True, exist_ok=True)
        elif not full.exists():
            if content is not None:
                full.write_text(content, encoding="utf-8")
            else:
                full.parent.mkdir(parents=True, exist_ok=True)
                full.write_text("{}", encoding="utf-8")

    # Build output_paths map
    output_paths = {}
    for d in _DIRS:
        output_paths[d] = str((out_dir / d).resolve())
    output_paths["study_context"] = str(
        (out_dir / "00_admin" / "study_context.json").resolve())
    output_paths["extract_manifest"] = str(
        (out_dir / "00_admin" / "extract_manifest.json").resolve())
    output_paths["outline"] = str(
        (out_dir / "02_outline" / "outline.md").resolve())
    output_paths["draft_handbook"] = str(
        (out_dir / "03_drafts" / "draft_handbook.md").resolve())
    output_paths["final_handbook"] = str(
        (out_dir / "04_final" / "final_handbook.md").resolve())
    output_paths["qa_report"] = str(
        (out_dir / "06_qa" / "qa_report.md").resolve())

    # Write study_context.json
    context = {
        "course_name": name,
        "created_at": datetime.now().isoformat(),
        "source_files": source_files,
        "delivery_formats": formats,
        "output_paths": output_paths,
    }
    ctx_path = out_dir / "00_admin" / "study_context.json"
    ctx_path.write_text(json.dumps(context, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    # Print summary
    print(json.dumps({
        "output_dir": str(out_dir),
        "course_name": name,
        "source_count": len(source_files),
        "delivery_formats": formats,
        "output_paths": output_paths,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
