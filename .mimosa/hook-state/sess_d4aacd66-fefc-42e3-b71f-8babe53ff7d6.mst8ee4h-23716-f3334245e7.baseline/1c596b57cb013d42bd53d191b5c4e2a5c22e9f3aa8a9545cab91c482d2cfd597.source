"""PPTX export and optional preview rendering."""
from __future__ import annotations
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional


def export_pptx(prs, output_path: str) -> str:
    """Save a Presentation object to disk."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)
    return output_path


def render_preview(pptx_path: str, output_dir: str,
                   dpi: int = 150) -> List[str]:
    """Render PPTX to PNG previews using soffice + pdftoppm.

    Requires LibreOffice (soffice) and poppler (pdftoppm) installed.
    Returns list of PNG file paths. Returns empty list if tools are missing.
    """
    if not shutil.which("soffice") or not shutil.which("pdftoppm"):
        return []

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Step 1: PPTX -> PDF
    pdf_dir = out / "pdf"
    pdf_dir.mkdir(exist_ok=True)
    try:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf",
             "--outdir", str(pdf_dir), pptx_path],
            check=True, capture_output=True, timeout=30)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return []

    # Step 2: PDF -> PNG
    pptx_stem = Path(pptx_path).stem
    pdf_file = pdf_dir / f"{pptx_stem}.pdf"
    if not pdf_file.exists():
        return []

    png_dir = out / "slides"
    png_dir.mkdir(exist_ok=True)
    try:
        subprocess.run(
            ["pdftoppm", "-png", f"-r{dpi}", str(pdf_file),
             str(png_dir / "slide")],
            check=True, capture_output=True, timeout=30)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return []

    return sorted(str(p) for p in png_dir.glob("*.png"))
