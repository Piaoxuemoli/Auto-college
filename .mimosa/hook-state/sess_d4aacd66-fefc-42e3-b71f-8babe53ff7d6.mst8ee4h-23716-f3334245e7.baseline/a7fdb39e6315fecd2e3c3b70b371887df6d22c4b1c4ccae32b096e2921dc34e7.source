"""Filter extracted images: keep educational, remove decorative.

Rules:
  - Too small: width < 150 or height < 100  -> filter
  - Too light: file size < 5 KB              -> filter
  - Extreme aspect ratio: > 5:1 or 1:5       -> filter
  - Near-solid color: pixel variance very low -> filter
  - Otherwise                                 -> keep

Usage:
    python filter_images.py \
        --input-dir "outputs/course/01_extracted/" \
        --output-dir "outputs/course/01_filtered/" \
        --report "outputs/course/00_admin/filter_report.json"
"""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Error: requires Pillow and numpy.  pip install Pillow numpy",
          file=sys.stderr)
    sys.exit(1)


# --- thresholds ---
MIN_WIDTH = 150
MIN_HEIGHT = 100
MIN_FILESIZE = 5 * 1024  # 5 KB
MAX_ASPECT_RATIO = 5.0
MAX_PIXEL_VARIANCE = 50.0  # near-solid if variance below this


def _check_image(img_path: Path) -> str | None:
    """Return reason string if image should be filtered, None if keep."""
    # file size check
    fsize = img_path.stat().st_size
    if fsize < MIN_FILESIZE:
        return f"too_small_file({fsize}B)"

    try:
        with Image.open(img_path) as img:
            w, h = img.size
    except Exception:
        return "unreadable"

    # dimension check
    if w < MIN_WIDTH or h < MIN_HEIGHT:
        return f"too_small_dim({w}x{h})"

    # aspect ratio check
    ratio = max(w, h) / max(min(w, h), 1)
    if ratio > MAX_ASPECT_RATIO:
        return f"extreme_ratio({ratio:.1f})"

    # near-solid color check
    try:
        gray = img.convert("L")
        arr = np.asarray(gray, dtype=np.float32)
        variance = float(arr.var())
        if variance < MAX_PIXEL_VARIANCE:
            return f"near_solid(var={variance:.1f})"
    except Exception:
        pass  # skip variance check if numpy fails

    return None  # keep


def filter_images(input_dir: str, output_dir: str) -> Dict[str, Any]:
    """Filter images from input_dir, copy kept ones to output_dir."""
    in_root = Path(input_dir)
    out_root = Path(output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    kept: List[str] = []
    filtered: List[Dict[str, str]] = []
    total = 0

    # iterate source subdirectories
    for src_dir in sorted(in_root.iterdir()):
        if not src_dir.is_dir():
            continue
        out_src = out_root / src_dir.name
        out_src.mkdir(exist_ok=True)

        for img_file in sorted(src_dir.iterdir()):
            if img_file.suffix.lower() not in (
                ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"
            ):
                # not an image — copy text files through
                if img_file.suffix.lower() in (".txt", ".md"):
                    shutil.copy2(img_file, out_src / img_file.name)
                continue

            total += 1
            reason = _check_image(img_file)
            if reason:
                filtered.append({
                    "path": str(img_file.relative_to(in_root)),
                    "reason": reason,
                })
            else:
                shutil.copy2(img_file, out_src / img_file.name)
                kept.append(str(img_file.relative_to(in_root)))

    return {
        "total": total,
        "kept": len(kept),
        "filtered": len(filtered),
        "kept_paths": kept,
        "filtered_details": filtered,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Filter extracted images: keep educational, remove decorative")
    parser.add_argument("--input-dir", required=True,
                        help="01_extracted/ directory with images")
    parser.add_argument("--output-dir", required=True,
                        help="01_filtered/ directory for kept images")
    parser.add_argument("--report", required=True,
                        help="Path to write filter_report.json")
    args = parser.parse_args()

    result = filter_images(args.input_dir, args.output_dir)

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Filtered: {result['total']} total -> "
          f"{result['kept']} kept, {result['filtered']} removed")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
