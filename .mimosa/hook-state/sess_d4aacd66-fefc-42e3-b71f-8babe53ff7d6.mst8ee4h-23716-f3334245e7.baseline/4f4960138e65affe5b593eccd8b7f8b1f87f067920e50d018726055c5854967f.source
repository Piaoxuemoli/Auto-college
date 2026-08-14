"""Export Markdown handbook to PDF with embedded images.

Usage:
    python export_pdf.py \
        --input "outputs/course/04_final/final_handbook.md" \
        --output "outputs/course/05_exports/final_handbook.pdf" \
        --resource-dirs "outputs/course/01_filtered"
"""
from __future__ import annotations
import argparse
import base64
import mimetypes
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Error: requires markdown. pip install markdown", file=sys.stderr)
    sys.exit(1)

try:
    from weasyprint import HTML as _WeasyHTML
    _PDF_ENGINE = "weasyprint"
except Exception:
    _PDF_ENGINE = None

try:
    from xhtml2pdf import pisa
    if _PDF_ENGINE is None:
        _PDF_ENGINE = "xhtml2pdf"
except ImportError:
    pass

if _PDF_ENGINE is None:
    print("Error: requires weasyprint or xhtml2pdf. "
          "pip install weasyprint  OR  pip install xhtml2pdf", file=sys.stderr)
    sys.exit(1)


def _embed_images(md_text: str, resource_dirs: list[Path]) -> str:
    """Replace relative image paths with base64 data URIs."""
    def _replace(match):
        alt = match.group(1)
        src = match.group(2)

        # skip already-embedded or absolute URLs
        if src.startswith(("data:", "http://", "https://")):
            return match.group(0)

        # resolve relative to resource dirs
        for rdir in resource_dirs:
            img_path = rdir / src
            if not img_path.exists():
                # try going up one level (from 04_final/ to parent)
                img_path = rdir.parent / src
            if img_path.exists():
                mime = mimetypes.guess_type(str(img_path))[0] or "image/png"
                data = img_path.read_bytes()
                b64 = base64.b64encode(data).decode()
                return f"![{alt}](data:{mime};base64,{b64})"

        # not found — leave as-is (broken link)
        return match.group(0)

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _replace, md_text)


def _md_to_html(md_text: str) -> str:
    """Convert markdown to a full HTML document."""
    extensions = ["tables", "fenced_code", "codehilite", "toc"]
    body = markdown.markdown(md_text, extensions=extensions)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: "Microsoft YaHei", "SimSun", sans-serif; font-size: 11pt; line-height: 1.6; margin: 2cm; }}
h1 {{ font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 4pt; }}
h2 {{ font-size: 15pt; border-bottom: 1px solid #999; padding-bottom: 2pt; margin-top: 1.5em; }}
h3 {{ font-size: 13pt; margin-top: 1.2em; }}
table {{ border-collapse: collapse; width: 100%; margin: 0.5em 0; }}
th, td {{ border: 1px solid #999; padding: 4pt 8pt; text-align: left; font-size: 10pt; }}
th {{ background: #f0f0f0; }}
code {{ background: #f5f5f5; padding: 1pt 3pt; font-size: 10pt; }}
pre {{ background: #f5f5f5; padding: 8pt; overflow-x: auto; font-size: 9pt; }}
pre code {{ background: none; padding: 0; }}
blockquote {{ border-left: 3pt solid #ccc; margin-left: 0; padding-left: 12pt; color: #555; }}
img {{ max-width: 100%; height: auto; margin: 0.5em 0; }}
hr {{ border: none; border-top: 1px solid #ccc; margin: 1em 0; }}
@page {{ size: A4; margin: 1.5cm; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def md_to_pdf(md_path: str, pdf_path: str, resource_dirs: list[str]) -> None:
    """Convert Markdown file to PDF with embedded images."""
    md_file = Path(md_path)
    pdf_file = Path(pdf_path)
    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    md_text = md_file.read_text(encoding="utf-8")
    rdirs = [Path(d) for d in resource_dirs]

    # embed images as base64
    md_text = _embed_images(md_text, rdirs)

    # convert to HTML
    html_text = _md_to_html(md_text)

    # render to PDF
    if _PDF_ENGINE == "weasyprint":
        _WeasyHTML(string=html_text).write_pdf(str(pdf_file))
    else:
        with open(pdf_file, "wb") as f:
            pisa.CreatePDF(html_text, dest=f, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Export Markdown handbook to PDF")
    parser.add_argument("--input", required=True, help="Input .md file")
    parser.add_argument("--output", required=True, help="Output .pdf file")
    parser.add_argument("--resource-dirs", required=True,
                        help="Colon-separated list of directories to search for images")
    args = parser.parse_args()

    dirs = [d.strip() for d in args.resource_dirs.split(":") if d.strip()]
    md_to_pdf(args.input, args.output, dirs)
    print(f"PDF exported: {args.output}")


if __name__ == "__main__":
    main()
