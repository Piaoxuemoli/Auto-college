"""
Manage reusable course report templates for lab-report.

Usage:
    python course_templates.py list
    python course_templates.py save --course "计算机网络" --template-path template.md
    python course_templates.py get --course "计算机网络"
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys


def templates_path(path: str | None = None) -> Path:
    return Path(path).expanduser() if path else Path.home() / ".qoobee-skills" / "lab-report" / "course_templates.json"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip()).strip("-").lower()
    return slug or "course-template"


def load_templates(path: Path) -> dict:
    if not path.exists():
        return {"templates": []}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid course templates JSON at {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        return {"templates": []}
    data.setdefault("templates", [])
    return data


def save_templates(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find_template(data: dict, course: str) -> dict | None:
    course_norm = course.strip().lower()
    for template in data.get("templates", []):
        names = [str(template.get("course", "")).lower()]
        names.extend(str(alias).lower() for alias in template.get("aliases", []))
        if course_norm in names:
            return template
    return None


def command_list(path: Path) -> None:
    print(json.dumps(load_templates(path), ensure_ascii=False, indent=2))


def command_get(path: Path, course: str) -> None:
    data = load_templates(path)
    template = find_template(data, course)
    payload = {
        "path": str(path),
        "course": course,
        "found": template is not None,
        "template": template,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if template is None:
        sys.exit(2)


def command_save(path: Path, course: str, template_path: str, aliases: list[str]) -> None:
    source = Path(template_path).expanduser().resolve()
    if not source.exists() or not source.is_file():
        print(f"ERROR: Template file does not exist: {source}", file=sys.stderr)
        sys.exit(1)

    data = load_templates(path)
    template_id = slugify(course)
    entry = {
        "id": template_id,
        "course": course,
        "aliases": aliases,
        "template_path": str(source),
        "updated_at": datetime.now().replace(microsecond=0).isoformat(),
    }

    templates = [item for item in data.get("templates", []) if item.get("id") != template_id]
    templates.append(entry)
    data["templates"] = sorted(templates, key=lambda item: item.get("course", ""))
    save_templates(data, path)
    print(json.dumps({"path": str(path), "saved": entry}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage lab-report course templates.")
    parser.add_argument("--templates-path", default=None, help="Override course_templates.json path.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List saved course templates.")

    get_parser = subparsers.add_parser("get", help="Find a template by course name or alias.")
    get_parser.add_argument("--course", required=True)

    save_parser = subparsers.add_parser("save", help="Save or update a course template.")
    save_parser.add_argument("--course", required=True)
    save_parser.add_argument("--template-path", required=True)
    save_parser.add_argument("--aliases", default="", help="Pipe-separated aliases.")

    args = parser.parse_args()
    path = templates_path(args.templates_path)

    if args.command == "list":
        command_list(path)
    elif args.command == "get":
        command_get(path, args.course)
    elif args.command == "save":
        aliases = [item.strip() for item in args.aliases.split("|") if item.strip()]
        command_save(path, args.course, args.template_path, aliases)


if __name__ == "__main__":
    main()
