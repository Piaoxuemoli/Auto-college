"""
Check and optionally install official Anthropic document-processing skills.

Usage:
    python check_official_skills.py
    python check_official_skills.py --source-files "manual.pdf|slides.pptx"
    python check_official_skills.py --install --source-files "manual.pdf|data.xlsx"

The script checks user-level Claude/Cursor skill directories for:
    pdf, docx, pptx, xlsx

When --install is passed, missing skills are installed with the OpenSkill CLI:
    npx -y skills add anthropics/skills@<skill> -g -y
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


OFFICIAL_SKILLS = {
    "pdf": {
        "extensions": [".pdf"],
        "package": "anthropics/skills@pdf",
    },
    "docx": {
        "extensions": [".docx", ".doc"],
        "package": "anthropics/skills@docx",
    },
    "pptx": {
        "extensions": [".pptx", ".ppt"],
        "package": "anthropics/skills@pptx",
    },
    "xlsx": {
        "extensions": [".xlsx", ".xlsm", ".xls", ".csv", ".tsv"],
        "package": "anthropics/skills@xlsx",
    },
}


def skill_roots() -> list[Path]:
    home = Path.home()
    return [
        home / ".claude" / "skills",
        home / ".cursor" / "skills",
    ]


def split_pipe_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split("|") if item.strip()]


def required_skills(source_files: list[str]) -> list[str]:
    if not source_files:
        return sorted(OFFICIAL_SKILLS)

    required: set[str] = set()
    for file_path in source_files:
        suffix = Path(file_path).suffix.lower()
        for skill_name, meta in OFFICIAL_SKILLS.items():
            if suffix in meta["extensions"]:
                required.add(skill_name)
    return sorted(required)


def find_installed_skill(skill_name: str) -> list[str]:
    found = []
    for root in skill_roots():
        skill_dir = root / skill_name
        if (skill_dir / "SKILL.md").exists():
            found.append(str(skill_dir))
    return found


def check(source_files: list[str]) -> dict:
    required = required_skills(source_files)
    skills = {}
    for skill_name in required:
        installed_paths = find_installed_skill(skill_name)
        skills[skill_name] = {
            "required": True,
            "installed": bool(installed_paths),
            "paths": installed_paths,
            "package": OFFICIAL_SKILLS[skill_name]["package"],
            "extensions": OFFICIAL_SKILLS[skill_name]["extensions"],
        }

    missing = [name for name, info in skills.items() if not info["installed"]]
    return {
        "skill_roots": [str(path) for path in skill_roots()],
        "source_files": source_files,
        "required_skills": required,
        "missing_skills": missing,
        "complete": not missing,
        "skills": skills,
    }


def install_missing(missing: list[str]) -> list[dict]:
    if not missing:
        return []

    if not shutil.which("npx"):
        print(
            "ERROR: npx is required to bootstrap OpenSkill and install official skills.",
            file=sys.stderr,
        )
        print("Install Node.js/npm first, then rerun with --install.", file=sys.stderr)
        sys.exit(2)

    results = []
    for skill_name in missing:
        package = OFFICIAL_SKILLS[skill_name]["package"]
        command = ["npx", "-y", "skills", "add", package, "-g", "-y"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        results.append(
            {
                "skill": skill_name,
                "package": package,
                "command": " ".join(command),
                "returncode": result.returncode,
                "stdout": result.stdout[-4000:],
                "stderr": result.stderr[-4000:],
            }
        )
        if result.returncode != 0:
            print(f"ERROR: Failed to install {skill_name} with OpenSkill.", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check/install official Anthropic skills needed by lab-report."
    )
    parser.add_argument(
        "--source-files",
        default="",
        help="Pipe-separated source file paths. If omitted, checks all supported skills.",
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install missing skills through OpenSkill: npx skills add anthropics/skills@<skill> -g -y.",
    )
    args = parser.parse_args()

    source_files = split_pipe_list(args.source_files)
    status = check(source_files)

    if args.install and status["missing_skills"]:
        status["install_results"] = install_missing(status["missing_skills"])
        status = check(source_files) | {"install_results": status["install_results"]}

    print(json.dumps(status, ensure_ascii=False, indent=2))

    if status["missing_skills"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
