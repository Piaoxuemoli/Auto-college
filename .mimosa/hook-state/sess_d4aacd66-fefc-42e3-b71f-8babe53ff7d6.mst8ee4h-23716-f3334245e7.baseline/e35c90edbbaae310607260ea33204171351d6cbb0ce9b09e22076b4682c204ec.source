"""
Initialize output directory structure for a lab-report experiment.

Usage:
    python init_output_dir.py <experiment-name> [--base-dir <path>]

Creates:
    outputs/<name>/
    outputs/<name>/screenshots/
    outputs/<name>/raw_outputs/
    outputs/<name>/experiment_info.json
    outputs/<name>/report_context.json
    optional paths for source_manifest.json, evidence_map.md, and delivery outputs are
    recorded for downstream agents

Validates experiment name: lowercase letters, digits, hyphens, max 64 chars.
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path


def validate_name(name: str) -> bool:
    """Validate experiment name: a-z, 0-9, hyphens, 1-64 chars."""
    if not name or len(name) > 64:
        return False
    return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))


PROFILE_FIELDS = [
    "student_name",
    "student_id",
    "class",
    "course",
    "instructor",
    "institution",
]

REPORT_TYPES = {"standard-executable", "data-provided", "paper-only"}
RUN_MODES = {"manual", "auto"}
SCREENSHOT_PREFERENCES = {"key", "all", "none"}
FAILURE_POLICIES = {"auto-skip", "manual-pause"}
DELIVERY_FORMATS = {"md", "docx", "pdf"}


def load_profile(profile_path: str | None = None) -> tuple[dict[str, str], Path]:
    """Load local profile data if available."""
    path = Path(profile_path) if profile_path else Path.home() / ".qoobee-skills" / "lab-report" / "profile.json"
    if not path.exists():
        return {}, path

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {}, path

    return {key: str(value).strip() for key, value in data.items() if value is not None}, path


def split_pipe_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split("|") if item.strip()]


def normalize_delivery_formats(value: str | None) -> list[str]:
    formats = [item.lower() for item in split_pipe_list(value or "md")]
    formats = formats or ["md"]
    invalid = [item for item in formats if item not in DELIVERY_FORMATS]
    if invalid:
        print(
            f"ERROR: Invalid delivery format(s): {', '.join(invalid)}. "
            f"Expected one of: {', '.join(sorted(DELIVERY_FORMATS))}"
        )
        sys.exit(1)
    return list(dict.fromkeys(formats))


def profile_complete(profile: dict[str, str]) -> bool:
    return all(profile.get(field, "") for field in PROFILE_FIELDS)


def init_output_dir(
    experiment_name: str,
    base_dir: str | None = None,
    profile_path: str | None = None,
    report_type: str = "standard-executable",
    run_mode: str = "manual",
    source_files: list[str] | None = None,
    language: str = "",
    screenshot_preference: str = "key",
    delivery_formats: list[str] | None = None,
    course_template_id: str = "",
    failure_policy: str | None = None,
    source_manifest_path: str = "",
    notes: str = "",
) -> str:
    """Create output directory structure. Returns the experiment directory path."""
    if not validate_name(experiment_name):
        print(f"ERROR: Invalid experiment name '{experiment_name}'.")
        print("       Must be lowercase letters, digits, and hyphens (1-64 chars).")
        print("       Examples: cuda-vector-add, chem-titration-lab3, ml-mnist-exp1")
        sys.exit(1)

    if report_type not in REPORT_TYPES:
        print(f"ERROR: Invalid report type '{report_type}'. Expected one of: {', '.join(sorted(REPORT_TYPES))}")
        sys.exit(1)

    if run_mode not in RUN_MODES:
        print(f"ERROR: Invalid run mode '{run_mode}'. Expected one of: {', '.join(sorted(RUN_MODES))}")
        sys.exit(1)

    if screenshot_preference not in SCREENSHOT_PREFERENCES:
        print(
            f"ERROR: Invalid screenshot preference '{screenshot_preference}'. "
            f"Expected one of: {', '.join(sorted(SCREENSHOT_PREFERENCES))}"
        )
        sys.exit(1)

    failure_policy = failure_policy or ("auto-skip" if run_mode == "auto" else "manual-pause")
    if failure_policy not in FAILURE_POLICIES:
        print(f"ERROR: Invalid failure policy '{failure_policy}'. Expected one of: {', '.join(sorted(FAILURE_POLICIES))}")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = base_dir or os.path.dirname(script_dir)
    exp_dir = os.path.join(skill_root, "outputs", experiment_name)

    if os.path.exists(exp_dir):
        print(f"ERROR: Experiment directory already exists: {exp_dir}")
        print("       Choose a different name or remove the existing directory.")
        sys.exit(1)

    screenshots_dir = os.path.join(exp_dir, "screenshots")
    raw_outputs_dir = os.path.join(exp_dir, "raw_outputs")

    os.makedirs(screenshots_dir)
    os.makedirs(raw_outputs_dir)

    profile, resolved_profile_path = load_profile(profile_path)

    # Create skeleton experiment_info.json
    info = {
        "experiment_name": experiment_name,
        "title": "",
        "course": profile.get("course", ""),
        "student_name": profile.get("student_name", ""),
        "student_id": profile.get("student_id", ""),
        "class": profile.get("class", ""),
        "date": date.today().isoformat(),
        "instructor": profile.get("instructor", ""),
        "institution": profile.get("institution", "")
    }
    info_path = os.path.join(exp_dir, "experiment_info.json")
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
        f.write("\n")

    context = {
        "experiment_name": experiment_name,
        "report_type": report_type,
        "run_mode": run_mode,
        "created_at": datetime.now().replace(microsecond=0).isoformat(),
        "profile_path": str(resolved_profile_path),
        "profile_complete": profile_complete(profile),
        "source_files": source_files or [],
        "source_manifest_path": source_manifest_path,
        "language": language,
        "screenshot_preference": screenshot_preference,
        "delivery_formats": delivery_formats or ["md"],
        "course_template_id": course_template_id,
        "failure_policy": failure_policy,
        "notes": notes,
    }
    context_path = os.path.join(exp_dir, "report_context.json")
    with open(context_path, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Created experiment directory:")
    print(f"  {exp_dir}/")
    print(f"    experiment_info.json")
    print(f"    report_context.json")
    print(f"    screenshots/")
    print(f"    raw_outputs/")
    return exp_dir


def main():
    parser = argparse.ArgumentParser(
        description="Initialize output directory for a lab-report experiment."
    )
    parser.add_argument(
        "experiment_name",
        help="Experiment name slug (a-z, 0-9, hyphens). e.g., cuda-vector-add"
    )
    parser.add_argument(
        "--base-dir",
        default=None,
        help="Base skill directory (default: parent of scripts/)."
    )
    parser.add_argument(
        "--profile-path",
        default=None,
        help="Optional profile JSON path (default: ~/.qoobee-skills/lab-report/profile.json)."
    )
    parser.add_argument(
        "--report-type",
        default="standard-executable",
        choices=sorted(REPORT_TYPES),
        help="Report path type."
    )
    parser.add_argument(
        "--run-mode",
        default="manual",
        choices=sorted(RUN_MODES),
        help="Confirmation mode."
    )
    parser.add_argument(
        "--source-files",
        default="",
        help="Pipe-separated source file paths, e.g. 'a.pdf|b.docx'."
    )
    parser.add_argument(
        "--language",
        default="",
        help="Report language hint, usually zh or en."
    )
    parser.add_argument(
        "--screenshot-preference",
        default="key",
        choices=sorted(SCREENSHOT_PREFERENCES),
        help="Screenshot capture preference."
    )
    parser.add_argument(
        "--delivery-formats",
        default="md",
        help="Pipe-separated output formats, e.g. 'md|docx|pdf'."
    )
    parser.add_argument(
        "--course-template-id",
        default="",
        help="Optional saved course template id."
    )
    parser.add_argument(
        "--failure-policy",
        default=None,
        choices=sorted(FAILURE_POLICIES),
        help="Failure handling policy. Defaults to auto-skip in auto mode and manual-pause in manual mode."
    )
    parser.add_argument(
        "--source-manifest-path",
        default="",
        help="Optional path to source_manifest.json generated by index_source_files.py."
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional run context notes."
    )
    args = parser.parse_args()
    init_output_dir(
        args.experiment_name,
        args.base_dir,
        args.profile_path,
        args.report_type,
        args.run_mode,
        split_pipe_list(args.source_files),
        args.language,
        args.screenshot_preference,
        normalize_delivery_formats(args.delivery_formats),
        args.course_template_id,
        args.failure_policy,
        args.source_manifest_path,
        args.notes,
    )


if __name__ == "__main__":
    main()
