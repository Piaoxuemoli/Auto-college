#!/usr/bin/env python3
"""
Unified terminal screenshot renderer with three tiers, best realism first:

  Tier 1  freeze --execute "cmd"   — really runs the command and captures ANSI
          output. Physically real fonts, colors, and timing. Requires
          https://github.com/charmbracelet/freeze on PATH.
  Tier 2  termframe + ANSI text    — for forged content: build ANSI with
          ansi_builder.py and pipe it through a real terminal emulator
          (https://github.com/pambirus/termframe) so a genuine engine does
          the coloring. Its SVG is rasterized to PNG via a headless browser.
  Tier 3  HTML fallback            — existing html_to_png.py pipeline.

Usage:
    python render.py --execute "git log --oneline -5" --name git-log
    python render.py --spec session.json --name gpu-ssh-session
    python render.py --ansi session.ansi --name gpu-ssh-session
    python render.py --html page.html --name legacy-shot

Exit codes:
    0 — screenshot generated
    1 — input error
    2 — no rendering tool available; skip screenshot and continue
"""

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import time

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import ansi_builder  # noqa: E402

FREEZE_CONFIG = SKILL_DIR / "configs" / "freeze-base.json"


# ---------------------------------------------------------------------------
# Tool discovery / best-effort installation
# ---------------------------------------------------------------------------

INSTALL_HINTS = {
    "freeze": [
        ("brew", ["brew", "install", "charmbracelet/tap/freeze"]),
        ("go", ["go", "install", "github.com/charmbracelet/freeze@latest"]),
        ("scoop", ["scoop", "install", "freeze"]),
    ],
    "termframe": [
        ("brew", ["brew", "install", "termframe"]),
        ("cargo", ["cargo", "install", "--locked", "--git",
                   "https://github.com/pambirus/termframe.git"]),
        ("scoop", ["scoop", "install", "termframe"]),
    ],
}


def try_install(tool: str) -> bool:
    """Best-effort install via available package managers. Never fatal."""
    for manager, cmd in INSTALL_HINTS.get(tool, []):
        if not shutil.which(cmd[0]):
            continue
        print(f"[install] Trying: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=600, shell=False)
            if result.returncode == 0 and shutil.which(tool):
                print(f"[install] {tool} installed.")
                return True
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"[install] {manager} failed: {exc}", file=sys.stderr)
    print(f"[install] Could not auto-install {tool}; continuing with fallback tiers.")
    return False


def get_tool(tool: str, auto_install: bool = True) -> str | None:
    path = shutil.which(tool)
    if path:
        return path
    if auto_install and try_install(tool):
        return shutil.which(tool)
    return None


# ---------------------------------------------------------------------------
# Output partitioning (same layout as html_to_png.py)
# ---------------------------------------------------------------------------

def make_output_dir(name: str, output_root: str | None) -> pathlib.Path:
    slug = name or "terminal"
    root = pathlib.Path(output_root) if output_root else SKILL_DIR / "outputs"
    out_dir = root / time.strftime("%Y-%m-%d") / f"{time.strftime('%H%M%S')}-{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


# ---------------------------------------------------------------------------
# Tier 1: freeze
# ---------------------------------------------------------------------------

def render_freeze(command: str, out_dir: pathlib.Path, name: str,
                  auto_install: bool = True) -> pathlib.Path | None:
    freeze = get_tool("freeze", auto_install)
    if not freeze:
        return None
    png_path = out_dir / f"{name}.png"
    config_args = ["--config", str(FREEZE_CONFIG)] if FREEZE_CONFIG.exists() else []
    print("[tier1] freeze --execute (real command, real ANSI capture)")
    try:
        result = subprocess.run(
            [
                freeze,
                "--execute", command,
                "--output", str(png_path),
                "--window",
                "--padding", "24,32,32,32",
                "--margin", "56,56,56,56",
                "--border.radius", "10",
                "--shadow.blur", "48",
                "--shadow.x", "0",
                "--shadow.y", "16",
                *config_args,
            ],
            capture_output=True, text=True, timeout=120, shell=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"[tier1] freeze failed: {exc}", file=sys.stderr)
        return None
    if result.returncode != 0 or not png_path.exists():
        print(f"[tier1] freeze failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    return png_path


# ---------------------------------------------------------------------------
# Tier 2: termframe + ANSI
# ---------------------------------------------------------------------------

def render_termframe(ansi_text: str, out_dir: pathlib.Path, name: str,
                     auto_install: bool = True) -> pathlib.Path | None:
    termframe = get_tool("termframe", auto_install)
    if not termframe:
        return None
    svg_path = out_dir / f"{name}.svg"
    print("[tier2] termframe rendering ANSI through a real terminal engine")
    try:
        result = subprocess.run(
            [termframe, "-o", str(svg_path)],
            input=ansi_text.encode("utf-8"),
            capture_output=True, timeout=120, shell=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"[tier2] termframe failed: {exc}", file=sys.stderr)
        return None
    if result.returncode != 0 or not svg_path.exists():
        print(f"[tier2] termframe failed: {result.stderr.decode(errors='replace').strip()}",
              file=sys.stderr)
        return None
    return svg_path


def svg_to_png(svg_path: pathlib.Path, out_dir: pathlib.Path, name: str) -> pathlib.Path:
    """Rasterize termframe's SVG by wrapping it in HTML and using the existing
    browser-rendering fallback chain from html_to_png.py."""
    png_path = out_dir / f"{name}.png"
    svg_data = svg_path.read_text(encoding="utf-8")
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
        "html,body{margin:0;padding:16px;background:transparent;overflow:hidden}"
        "svg{display:block}"
        "</style></head><body>" + svg_data + "</body></html>"
    )
    html_path = out_dir / f"{name}.svg.html"
    html_path.write_text(html, encoding="utf-8")

    import html_to_png
    width = html_to_png.estimate_width(str(html_path))
    tool, details = html_to_png.detect_fallback_tools()
    rendered = False
    try:
        if tool == "playwright-python":
            rendered = html_to_png.render_playwright_python(str(html_path), str(png_path), width)
        elif tool in ("playwright-npx", "puppeteer"):
            rendered = html_to_png.render_playwright_npx(str(html_path), str(png_path), width)
        elif tool == "edge-headless":
            rendered = html_to_png.render_edge_headless(str(html_path), str(png_path), width,
                                                        details["path"])
        elif tool == "chrome-headless":
            rendered = html_to_png.render_chrome_headless(str(html_path), str(png_path), width,
                                                          details["path"])
        elif tool == "wkhtmltoimage":
            rendered = html_to_png.render_wkhtmltoimage(str(html_path), str(png_path), width)
    except Exception as exc:  # noqa: BLE001 — any renderer failure means SVG-only delivery
        print(f"[tier2] SVG rasterization failed: {exc}", file=sys.stderr)
    if not rendered:
        print(f"[tier2] PNG rasterization unavailable; delivering SVG only: {svg_path}")
        return svg_path
    return png_path


# ---------------------------------------------------------------------------
# Tier 3: HTML fallback
# ---------------------------------------------------------------------------

def run_html_fallback() -> int:
    print("[tier3] falling back to HTML -> browser screenshot pipeline")
    import html_to_png
    return html_to_png.main()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--execute", help="Tier 1: command to really execute via freeze")
    mode.add_argument("--spec", help="Tier 2: session spec JSON (see ansi_builder.py)")
    mode.add_argument("--ansi", help="Tier 2: pre-built ANSI text file")
    mode.add_argument("--html", help="Tier 3: HTML file for the legacy pipeline")
    parser.add_argument("--name", default="terminal", help="Short slug for output names")
    parser.add_argument("--output-root", default=None, help="Override outputs root directory")
    parser.add_argument("--no-install", action="store_true",
                        help="Do not attempt to auto-install freeze/termframe")
    args = parser.parse_args()

    if args.html:
        # Legacy pipeline keeps its own partitioning and quality checks.
        sys.argv = ["html_to_png.py", args.html, "--name", args.name]
        if args.output_root:
            sys.argv += ["--output-root", args.output_root]
        return run_html_fallback()

    out_dir = make_output_dir(args.name, args.output_root)
    print(f"[output] Directory: {out_dir}")

    if args.execute:
        png = render_freeze(args.execute, out_dir, args.name, auto_install=not args.no_install)
        if png:
            print(f"OK: {png} ({png.stat().st_size / 1024:.0f} KB)")
            return 0
        print("[tier1] freeze unavailable. Real execution needs freeze installed "
              "(brew/go/scoop); forged content should use --spec/--ansi instead.",
              file=sys.stderr)
        return 2

    # Tier 2: build or load ANSI text
    if args.spec:
        try:
            spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"ERROR: cannot read spec: {exc}", file=sys.stderr)
            return 1
        ansi_text = ansi_builder.render_session(spec)
        (out_dir / f"{args.name}.ansi").write_text(ansi_text, encoding="utf-8")
    else:
        try:
            ansi_text = pathlib.Path(args.ansi).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot read ANSI file: {exc}", file=sys.stderr)
            return 1

    svg = render_termframe(ansi_text, out_dir, args.name, auto_install=not args.no_install)
    if svg:
        final = svg_to_png(svg, out_dir, args.name)
        print(f"OK: {final}")
        return 0

    print("[tier2] termframe unavailable; build HTML from references/html-templates.md "
          "and re-run with --html for the legacy pipeline.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
