#!/usr/bin/env python3
"""
Convert terminal HTML to PNG screenshot.

Auto-configures rendering tools: tries to install Playwright first (best quality),
retrying up to 3 times. Falls back to existing system tools if auto-config fails.
If nothing works, exits with code 2 so the caller can skip screenshots gracefully.

Usage:
    python html_to_png.py <input.html> [output.png] [--width W] [--output-root DIR] [--name NAME]

When output.png is omitted, files are written to:
    <skill-dir>/outputs/YYYY-MM-DD/HHMMSS-name/

Exit codes:
    0 — screenshot generated successfully
    1 — input error (HTML not found, etc.)
    2 — no tool available, skip screenshot and continue
"""

import sys
import os
import subprocess
import shutil
import tempfile
import time
import re


MAX_RETRIES = 3


def count_lines(html_path):
    """Count visible content lines inside the terminal body div only."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            text = f.read()
        import re
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        m = re.search(r'<div class="(?:body|terminal|content)"[^>]*>(.*?)</div>\s*(?:</div>\s*)?</div>\s*</body>', text, flags=re.DOTALL)
        if not m:
            m = re.search(r'<div class="body"[^>]*>(.*?)</div>', text, flags=re.DOTALL)
        if m:
            body_text = m.group(1)
        else:
            body_text = text
        body_text = re.sub(r'<[^>]+>', '', body_text)
        body_text = body_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        lines = body_text.split('\n')
        return max(len(lines), 5)
    except Exception:
        return 40


def estimate_height(line_count):
    """Estimate needed viewport height from content lines."""
    content_px = line_count * 20
    chrome_px = 116
    return int(content_px + chrome_px)


def estimate_width(html_path):
    """Estimate viewport width from CSS window widths, including page padding."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            text = f.read()

        widths = [
            int(value)
            for value in re.findall(
                r'\.(?:window|terminal|monitor)\s*\{[^}]*?width:\s*(\d+)px',
                text,
                flags=re.DOTALL
            )
        ]
        if not widths:
            widths = [int(value) for value in re.findall(r'width:\s*(\d+)px', text)]

        content_width = max(widths) if widths else 740
        # Most templates use 20-22px body padding on both sides plus a little clip margin.
        return max(800, min(content_width + 96, 1600))
    except Exception:
        return 800


def extract_visible_text(html_text):
    """Extract approximate visible text for quality checks."""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</(?:div|p|span|pre|section)>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = (
        text.replace('&lt;', '<')
        .replace('&gt;', '>')
        .replace('&amp;', '&')
        .replace('&nbsp;', ' ')
    )
    lines = [line.rstrip() for line in text.splitlines()]
    return '\n'.join(line for line in lines if line.strip())


def validate_html_quality(html_path):
    """Return non-fatal warnings for common terminal screenshot realism issues."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as exc:
        return [f"could not read HTML for quality checks: {exc}"]

    warnings = []
    visible = extract_visible_text(html)
    visible_lines = [line for line in visible.splitlines() if line.strip()]
    line_count = len(visible_lines)
    has_titlebar = 'class="titlebar"' in html or "class='titlebar'" in html
    has_startup_context = any(
        marker in visible
        for marker in [
            "PowerShell 7 Ready",
            "Type 'help-commands'",
            "Last login:",
            "Welcome to Ubuntu",
            "Microsoft Windows",
        ]
    )
    has_ssh_transition = bool(re.search(r'\bssh\s+\S+@\S+', visible))
    looks_linux_prompt = bool(re.search(r'[\w.-]+@[\w.-]+:[~/\w./-]*[$#]', visible))
    looks_powershell = "PS " in visible and ">" in visible
    looks_macos_zsh = bool(re.search(r'\b\w+@[\w.-]+\s+\S+\s+%', visible))

    if re.search(r'\.tabs\s*\{[^}]*align-items:\s*flex-end', html, re.DOTALL):
        warnings.append(
            "Windows Terminal tab strip uses align-items:flex-end; + and dropdown controls may sag."
        )

    has_tab_action = 'class="tab-action new-tab"' in html or "class='tab-action new-tab'" in html
    if has_tab_action and re.search(r'\.tab-action\s*\{(?![^}]*height:\s*\d+px)', html, re.DOTALL):
        warnings.append(
            "Windows Terminal tab-action controls have no explicit height; vertical alignment may drift."
        )

    if not has_tab_action and re.search(r'\.(?:new-tab|chevron)\s*\{(?![^}]*height:\s*\d+px)', html, re.DOTALL):
        warnings.append(
            "Windows Terminal + or dropdown controls have no explicit height; vertical alignment may drift."
        )

    if re.search(r'class=["\'][^"\']*new-tab[^"\']*["\'][^>]*>\s*\+', html):
        warnings.append(
            "Windows Terminal new-tab control uses a text '+' glyph. Use CSS-drawn strokes for stable size and baseline."
        )

    if re.search(r'class=["\'][^"\']*chevron[^"\']*["\'][^>]*>\s*[⌄∨vV]', html):
        warnings.append(
            "Windows Terminal dropdown uses a text chevron glyph. Use a CSS-drawn chevron for stable size and baseline."
        )

    if re.search(r'class=["\'][^"\']*caption-btn[^"\']*["\'][^>]*>\s*[─□×-]', html):
        warnings.append(
            "Windows caption buttons use text glyphs. Use CSS-drawn minimize/maximize/close icons for stable size and alignment."
        )

    if has_titlebar and line_count <= 6 and not has_startup_context and not has_ssh_transition:
        warnings.append(
            "Short command evidence has a titlebar. Prefer a borderless snippet unless the user asked for a full terminal."
        )

    if has_titlebar and looks_linux_prompt and line_count <= 12 and not has_ssh_transition:
        warnings.append(
            "Short Linux/server output has fake window chrome. Prefer a clean SSH/Linux snippet unless showing a full SSH session."
        )

    if looks_powershell and re.search(r'(^|\n)\s*[$#]\s+\w+', visible):
        warnings.append("PowerShell-looking content also contains Unix prompts; check prompt grammar.")

    if looks_macos_zsh and "PS " in visible:
        warnings.append("macOS zsh-looking content also contains PowerShell prompt text; check session profile.")

    return warnings


def slugify(value):
    """Return a filesystem-safe lowercase slug."""
    value = os.path.splitext(os.path.basename(value))[0] if value else "terminal"
    value = re.sub(r'[^A-Za-z0-9._-]+', '-', value).strip('-._').lower()
    return value or "terminal"


def default_output_root(html_path):
    """Use the skill's outputs directory next to scripts/ when possible."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    if os.path.basename(script_dir) == "scripts" and os.path.isdir(skill_dir):
        return os.path.join(skill_dir, "outputs")
    return os.path.join(os.path.dirname(os.path.abspath(html_path)), "outputs")


def build_partitioned_output_paths(html_path, output_root=None, name=None):
    """Create a dated output partition and return (html_copy, png_path, output_dir)."""
    slug = slugify(name or html_path)
    date_part = time.strftime("%Y-%m-%d")
    time_part = time.strftime("%H%M%S")
    root = output_root or default_output_root(html_path)
    output_dir = os.path.join(root, date_part, f"{time_part}-{slug}")
    os.makedirs(output_dir, exist_ok=True)

    html_copy = os.path.join(output_dir, f"{slug}.html")
    png_path = os.path.join(output_dir, f"{slug}.png")
    shutil.copy2(html_path, html_copy)
    return html_copy, png_path, output_dir


def parse_args(argv):
    """Parse positional args plus optional flags without requiring argparse."""
    if len(argv) < 2:
        print(__doc__)
        sys.exit(1)

    html_path = argv[1]
    png_path = None
    width = None
    output_root = None
    output_name = None

    i = 2
    while i < len(argv):
        arg = argv[i]
        if arg == "--width":
            if i + 1 >= len(argv):
                print("ERROR: --width requires a value", file=sys.stderr)
                sys.exit(1)
            try:
                width = int(argv[i + 1])
            except ValueError:
                print(f"ERROR: invalid --width value: {argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2
        elif arg.startswith("--width="):
            try:
                width = int(arg.split("=", 1)[1])
            except ValueError:
                print(f"ERROR: invalid --width value: {arg}", file=sys.stderr)
                sys.exit(1)
            i += 1
        elif arg == "--output-root":
            if i + 1 >= len(argv):
                print("ERROR: --output-root requires a value", file=sys.stderr)
                sys.exit(1)
            output_root = argv[i + 1]
            i += 2
        elif arg.startswith("--output-root="):
            output_root = arg.split("=", 1)[1]
            i += 1
        elif arg == "--name":
            if i + 1 >= len(argv):
                print("ERROR: --name requires a value", file=sys.stderr)
                sys.exit(1)
            output_name = argv[i + 1]
            i += 2
        elif arg.startswith("--name="):
            output_name = arg.split("=", 1)[1]
            i += 1
        elif png_path is None:
            png_path = arg
            i += 1
        else:
            print(f"ERROR: unexpected argument: {arg}", file=sys.stderr)
            sys.exit(1)

    return html_path, png_path, width, output_root, output_name


# ---------------------------------------------------------------------------
# Auto-configuration: install Playwright
# ---------------------------------------------------------------------------

def _try_pip_install():
    """Try pip install playwright. Returns True on success."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "playwright"],
        capture_output=True, text=True, timeout=120
    )
    return result.returncode == 0


def _try_playwright_install_chromium():
    """Try playwright install chromium. Returns True on success."""
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True, text=True, timeout=300
    )
    return result.returncode == 0


def auto_configure_playwright():
    """
    Attempt to install Playwright + Chromium, retrying up to MAX_RETRIES times.
    Returns True if Playwright is usable after configuration.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"[auto-config] Attempt {attempt}/{MAX_RETRIES}: installing playwright...")

        if not _try_pip_install():
            print(f"[auto-config] pip install failed (attempt {attempt})", file=sys.stderr)
            if attempt < MAX_RETRIES:
                print("[auto-config] Retrying in 2 seconds...")
                time.sleep(2)
            continue

        if not _try_playwright_install_chromium():
            print(f"[auto-config] playwright install chromium failed (attempt {attempt})", file=sys.stderr)
            if attempt < MAX_RETRIES:
                print("[auto-config] Retrying in 2 seconds...")
                time.sleep(2)
            continue

        # Both installs succeeded — verify import works
        try:
            from playwright.sync_api import sync_playwright
            print("[auto-config] Playwright installed and ready.")
            return True
        except ImportError:
            print(f"[auto-config] Import failed after install (attempt {attempt})", file=sys.stderr)
            if attempt < MAX_RETRIES:
                time.sleep(2)

    return False


# ---------------------------------------------------------------------------
# Fallback: detect existing system tools
# ---------------------------------------------------------------------------

def detect_fallback_tools():
    """
    Detect available screenshot tools from the local system.
    Returns (tool_name, details) or (None, {}).
    Checks in order: Playwright (already installed), Edge headless, Chrome headless, wkhtmltoimage.
    """
    # 1. Playwright Python (may have been manually installed)
    try:
        from playwright.sync_api import sync_playwright
        return "playwright-python", {"sync_playwright": sync_playwright}
    except ImportError:
        pass

    # 2. Playwright via npx
    if shutil.which("npx"):
        try:
            result = subprocess.run(
                ["npx", "playwright", "--version"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return "playwright-npx", {}
        except Exception:
            pass

    # 3. Puppeteer
    if shutil.which("node"):
        try:
            result = subprocess.run(
                ["node", "-e", "require('puppeteer')"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return "puppeteer", {}
        except Exception:
            pass

    # 4. Edge headless (Windows)
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for edge_path in edge_paths:
        if os.path.exists(edge_path):
            return "edge-headless", {"path": edge_path}

    # 5. Chrome/Chromium headless
    for chrome_name in ["google-chrome", "chromium", "chromium-browser", "chrome"]:
        chrome_path = shutil.which(chrome_name)
        if chrome_path:
            return "chrome-headless", {"path": chrome_path}

    # 6. wkhtmltoimage
    wk_path = shutil.which("wkhtmltoimage")
    if wk_path:
        return "wkhtmltoimage", {"path": wk_path}

    return None, {}


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def render_playwright_python(html_path, png_path, width):
    """Render using Playwright Python API — clips to exact content height."""
    from playwright.sync_api import sync_playwright

    abs_html = "file:///" + os.path.abspath(html_path).replace("\\", "/")

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="msedge", headless=True)
        except Exception:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception:
                browser = p.chromium.launch(channel="chrome", headless=True)

        page = browser.new_page(viewport={"width": width, "height": 4800})
        page.goto(abs_html, wait_until="networkidle")
        page.wait_for_timeout(300)

        body = page.query_selector("body")
        if body:
            box = body.bounding_box()
            if box:
                clip = {
                    "x": max(0, box["x"] - 4),
                    "y": max(0, box["y"] - 4),
                    "width": box["width"] + 8,
                    "height": box["height"] + 8,
                }
                page.screenshot(path=png_path, clip=clip)
            else:
                page.screenshot(path=png_path, full_page=True)
        else:
            page.screenshot(path=png_path, full_page=True)

        browser.close()
    return True


def render_edge_headless(html_path, png_path, width, edge_path):
    """Render using Edge headless — no npm/python deps needed."""
    abs_html = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    abs_png = os.path.abspath(png_path)

    line_count = count_lines(html_path)
    height = int(estimate_height(line_count))

    result = subprocess.run(
        [
            edge_path, "--headless", "--disable-gpu",
            "--no-pdf-header-footer",
            f"--screenshot={abs_png}",
            f"--window-size={width},{height}",
            abs_html
        ],
        capture_output=True, text=True, timeout=60
    )

    if os.path.exists(abs_png):
        return True

    alt_name = os.path.basename(abs_png)
    if os.path.exists(alt_name):
        shutil.move(alt_name, abs_png)
        return True

    print(f"Edge stderr: {result.stderr}", file=sys.stderr)
    return False


def render_chrome_headless(html_path, png_path, width, chrome_path):
    """Render using Chrome/Chromium headless."""
    abs_html = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    abs_png = os.path.abspath(png_path)

    line_count = count_lines(html_path)
    height = int(estimate_height(line_count))

    subprocess.run(
        [
            chrome_path, "--headless", "--disable-gpu",
            f"--screenshot={abs_png}",
            f"--window-size={width},{height}",
            abs_html
        ],
        capture_output=True, text=True, timeout=60
    )
    return os.path.exists(abs_png)


def render_wkhtmltoimage(html_path, png_path, width):
    """Render using wkhtmltoimage."""
    abs_html = os.path.abspath(html_path)
    abs_png = os.path.abspath(png_path)

    subprocess.run(
        [
            "wkhtmltoimage",
            "--width", str(width),
            "--quality", "100",
            "--encoding", "UTF-8",
            abs_html, abs_png
        ],
        capture_output=True, text=True, timeout=60
    )
    return os.path.exists(abs_png)


def render_playwright_npx(html_path, png_path, width):
    """Render using npx playwright (Node.js)."""
    abs_html = os.path.abspath(html_path).replace("\\", "/")
    abs_png = os.path.abspath(png_path).replace("\\", "/")

    script = f"""
    const {{ chromium }} = require('playwright');
    (async () => {{
        const browser = await chromium.launch({{ headless: true }});
        const page = await browser.newPage({{ viewport: {{ width: {width}, height: 4800 }} }});
        await page.goto('file:///{abs_html}');
        await page.waitForTimeout(500);
        const body = await page.$('body');
        if (body) {{
            const box = await body.boundingBox();
            await page.screenshot({{
                path: '{abs_png}',
                clip: {{ x: Math.max(0, box.x - 4), y: Math.max(0, box.y - 4),
                         width: box.width + 8, height: box.height + 8 }}
            }});
        }} else {{
            await page.screenshot({{ path: '{abs_png}', fullPage: true }});
        }}
        await browser.close();
    }})();
    """

    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(script)
        script_path = f.name

    try:
        result = subprocess.run(
            ["node", script_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"Node stderr: {result.stderr}", file=sys.stderr)
        return os.path.exists(abs_png)
    finally:
        os.unlink(script_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    html_path, png_path, width_override, output_root, output_name = parse_args(sys.argv)

    if not os.path.exists(html_path):
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    if png_path is None:
        html_path, png_path, output_dir = build_partitioned_output_paths(
            html_path,
            output_root=output_root,
            name=output_name,
        )
        print(f"[output] Directory: {output_dir}")
        print(f"[output] HTML: {html_path}")
        print(f"[output] PNG: {png_path}")
    else:
        output_parent = os.path.dirname(os.path.abspath(png_path))
        if output_parent:
            os.makedirs(output_parent, exist_ok=True)

    width = width_override or estimate_width(html_path)
    print(f"[render] Viewport width: {width}px")

    quality_warnings = validate_html_quality(html_path)
    if quality_warnings:
        for warning in quality_warnings:
            print(f"[quality-check] WARNING: {warning}", file=sys.stderr)
    else:
        print("[quality-check] OK")

    # ---- Phase 1: Auto-configure Playwright (best quality) ----
    print("[auto-config] Attempting to install Playwright (best quality tool)...")
    configured = auto_configure_playwright()

    if configured:
        # Use the freshly installed Playwright
        try:
            from playwright.sync_api import sync_playwright
            success = render_playwright_python(html_path, png_path, width)
        except Exception as e:
            print(f"ERROR with auto-configured Playwright: {e}", file=sys.stderr)
            success = False

        if success and os.path.exists(png_path):
            size_kb = os.path.getsize(png_path) / 1024
            print(f"OK: {png_path} ({size_kb:.0f} KB)")
            sys.exit(0)
        else:
            print("[auto-config] Playwright install succeeded but render failed."
                  " Trying fallback...", file=sys.stderr)

    # ---- Phase 2: Fallback to existing system tools ----
    print("[fallback] Detecting existing system tools...")
    tool, details = detect_fallback_tools()

    if tool is None:
        # ---- Phase 3: Nothing works — skip screenshot ----
        print(
            "SKIP: No screenshot tool available.\n"
            "Auto-configuration (playwright install) failed after 3 attempts.\n"
            "No existing system tools (Edge, Chrome, wkhtmltoimage) found.\n"
            "Continuing without screenshot — no user action required.",
            file=sys.stderr
        )
        sys.exit(2)

    print(f"[fallback] Using existing tool: {tool}")

    success = False
    try:
        if tool == "playwright-python":
            success = render_playwright_python(html_path, png_path, width)
        elif tool == "playwright-npx":
            success = render_playwright_npx(html_path, png_path, width)
        elif tool == "puppeteer":
            success = render_playwright_npx(html_path, png_path, width)
        elif tool == "edge-headless":
            success = render_edge_headless(html_path, png_path, width, details["path"])
        elif tool == "chrome-headless":
            success = render_chrome_headless(html_path, png_path, width, details["path"])
        elif tool == "wkhtmltoimage":
            success = render_wkhtmltoimage(html_path, png_path, width)
    except Exception as e:
        print(f"ERROR with {tool}: {e}", file=sys.stderr)

    if success and os.path.exists(png_path):
        size_kb = os.path.getsize(png_path) / 1024
        print(f"OK: {png_path} ({size_kb:.0f} KB)")
        sys.exit(0)
    else:
        # Fallback render also failed — skip
        print(
            "SKIP: All tools failed to render screenshot.\n"
            "Continuing without screenshot — no user action required.",
            file=sys.stderr
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
