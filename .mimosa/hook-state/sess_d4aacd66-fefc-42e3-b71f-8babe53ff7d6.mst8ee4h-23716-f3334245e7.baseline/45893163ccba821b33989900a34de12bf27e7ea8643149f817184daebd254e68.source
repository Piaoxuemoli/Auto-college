"""
Manage local profile data for the lab-report skill.

Usage:
    python profile_config.py status
    python profile_config.py write --json '{"student_name":"...","student_id":"..."}'
    python profile_config.py write --student-name "..." --student-id "..."
    python profile_config.py --profile-path /tmp/profile.json status
    python profile_config.py path

Profile location:
    ~/.qoobee-skills/lab-report/profile.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROFILE_FIELDS = [
    "student_name",
    "student_id",
    "class",
    "course",
    "instructor",
    "institution",
]


def profile_path() -> Path:
    return Path.home() / ".qoobee-skills" / "lab-report" / "profile.json"


def empty_profile() -> dict[str, str]:
    return {field: "" for field in PROFILE_FIELDS}


def load_profile(path: Path | None = None) -> dict[str, str]:
    path = path or profile_path()
    if not path.exists():
        return empty_profile()

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid profile JSON at {path}: {exc}", file=sys.stderr)
        sys.exit(1)

    profile = empty_profile()
    for field in PROFILE_FIELDS:
        value = data.get(field, "")
        profile[field] = str(value).strip() if value is not None else ""
    return profile


def save_profile(profile: dict[str, str], path: Path | None = None) -> Path:
    path = path or profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    clean_profile = empty_profile()
    for field in PROFILE_FIELDS:
        clean_profile[field] = str(profile.get(field, "")).strip()

    with path.open("w", encoding="utf-8") as f:
        json.dump(clean_profile, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def missing_fields(profile: dict[str, str]) -> list[str]:
    return [field for field in PROFILE_FIELDS if not profile.get(field)]


def print_status(path: Path | None = None) -> None:
    path = path or profile_path()
    profile = load_profile(path)
    missing = missing_fields(profile)
    payload = {
        "path": str(path),
        "exists": path.exists(),
        "complete": not missing,
        "missing_fields": missing,
        "profile": profile,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def parse_json_update(json_text: str | None) -> dict[str, str]:
    if not json_text:
        return {}
    try:
        incoming = json.loads(json_text)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(incoming, dict):
        print("ERROR: --json must be a JSON object", file=sys.stderr)
        sys.exit(1)
    return incoming


def write_profile(updates: dict[str, str], path: Path | None = None) -> None:
    if not updates:
        print("ERROR: No profile fields provided.", file=sys.stderr)
        sys.exit(1)

    profile = load_profile(path)
    for field in PROFILE_FIELDS:
        if field in updates and updates[field] is not None:
            profile[field] = str(updates.get(field, "")).strip()

    path = save_profile(profile, path)
    print(f"Saved profile: {path}")
    print_status(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage lab-report local profile data.")
    parser.add_argument(
        "--profile-path",
        default=None,
        help="Override profile path for testing or migration."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Print profile path, completion status, and data.")
    subparsers.add_parser("path", help="Print profile path only.")

    write_parser = subparsers.add_parser("write", help="Merge and save profile fields.")
    write_parser.add_argument("--json", default=None, help="JSON object with profile fields.")
    write_parser.add_argument("--student-name", dest="student_name", default=None)
    write_parser.add_argument("--student-id", dest="student_id", default=None)
    write_parser.add_argument("--class", dest="class", default=None)
    write_parser.add_argument("--course", dest="course", default=None)
    write_parser.add_argument("--instructor", dest="instructor", default=None)
    write_parser.add_argument("--institution", dest="institution", default=None)

    args = parser.parse_args()
    custom_path = Path(args.profile_path) if args.profile_path else None

    if args.command == "status":
        print_status(custom_path)
    elif args.command == "path":
        print(custom_path or profile_path())
    elif args.command == "write":
        updates = parse_json_update(args.json)
        for field in PROFILE_FIELDS:
            value = getattr(args, field)
            if value is not None:
                updates[field] = value
        write_profile(updates, custom_path)


if __name__ == "__main__":
    main()
