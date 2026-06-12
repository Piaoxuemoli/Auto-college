"""Render experiment-screenshot placeholders in Markdown to screenshot-style SVGs.

The renderer is deterministic and uses only the Python standard library. It is
intended for experiment reports where commands, IP addresses, and configuration
steps must remain exact. It creates polished browser/terminal/configuration
screenshots without asking an image model to redraw text.

Supported placeholder formats:

    <!-- experiment-screenshot:
    title: PPPoE server setup
    style: terminal
    content:
    $ sudo pppoe-server -I eth0 -L 10.1.1.1 -R 10.1.1.100
    ✓ PPPoE service started
    -->

    ```experiment-screenshot
    title: RADIUS authentication test
    style: web
    content:
    1. User client1 starts PPPoE dial-up
    2. PPPoE server sends Access-Request to RADIUS
    3. RADIUS returns Access-Accept
    ```

Usage:
    python paper-writer/scripts/render_experiment_screenshots.py \
        --input "paper-writer/outputs/demo/04_final/final_paper.rendered.md" \
        --output-dir "paper-writer/outputs/demo/03_figures" \
        --processed-markdown "paper-writer/outputs/demo/04_final/final_paper.assets.md" \
        --manifest "paper-writer/outputs/demo/03_figures/experiment_screenshot_manifest.json"
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Match


COMMENT_BLOCK_RE = re.compile(
    r"<!--\s*experiment-screenshot\s*:\s*\n(?P<body>.*?)-->",
    re.IGNORECASE | re.DOTALL,
)
FENCE_BLOCK_RE = re.compile(
    r"```experiment-screenshot\s*\n(?P<body>.*?)(?:\n```)",
    re.IGNORECASE | re.DOTALL,
)
KEY_VALUE_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$")


@dataclass
class ScreenshotSpec:
    title: str
    style: str
    content: str
    subtitle: str = ""
    width: int = 1200


@dataclass
class ScreenshotResult:
    index: int
    title: str
    style: str
    source_path: str
    image_path: str
    markdown_image_path: str
    status: str
    error: str | None = None


def slugify(value: str, fallback: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[\s/\\:;|]+", "-", value)
    value = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff._-]+", "", value)
    value = re.sub(r"-+", "-", value).strip("-._")
    return value or fallback


def display_width(text: str) -> int:
    width = 0
    for char in text:
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def wrap_text(text: str, max_width: int) -> list[str]:
    if not text:
        return [""]

    wrapped: list[str] = []
    current: list[str] = []
    current_width = 0

    for word in re.split(r"(\s+)", text):
        if not word:
            continue
        word_width = display_width(word)
        if current and current_width + word_width > max_width:
            wrapped.append("".join(current).rstrip())
            current = []
            current_width = 0
        if word_width > max_width:
            for char in word:
                char_width = display_width(char)
                if current and current_width + char_width > max_width:
                    wrapped.append("".join(current).rstrip())
                    current = []
                    current_width = 0
                current.append(char)
                current_width += char_width
        else:
            current.append(word)
            current_width += word_width

    if current:
        wrapped.append("".join(current).rstrip())
    return wrapped or [""]


def parse_spec(body: str, index: int) -> ScreenshotSpec:
    fields: dict[str, str] = {}
    content_lines: list[str] = []
    in_content = False

    for raw_line in body.strip("\n").splitlines():
        line = raw_line.rstrip()
        if in_content:
            content_lines.append(line)
            continue

        match = KEY_VALUE_RE.match(line)
        if match:
            key = match.group(1).lower().replace("-", "_")
            value = match.group(2)
            if key in {"content", "body", "steps", "commands"}:
                in_content = True
                if value:
                    content_lines.append(value)
            else:
                fields[key] = value
        elif line.strip():
            content_lines.append(line)

    title = fields.get("title") or fields.get("name") or f"实验过程截图 {index}"
    style = (fields.get("style") or fields.get("type") or "terminal").strip().lower()
    subtitle = fields.get("subtitle", "").strip()
    content = "\n".join(content_lines).strip()
    width = parse_width(fields.get("width"), default=1200)
    return ScreenshotSpec(title=title, style=style, subtitle=subtitle, content=content, width=width)


def parse_width(value: str | None, default: int) -> int:
    if not value:
        return default
    try:
        return max(800, min(1600, int(value)))
    except ValueError:
        return default


def svg_text(x: int, y: int, text: str, *, size: int = 26, fill: str = "#111827",
             family: str = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
             weight: str = "400") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">{html.escape(text)}</text>'
    )


def svg_rect(x: int, y: int, width: int, height: int, *, fill: str, stroke: str = "none",
             radius: int = 0, stroke_width: int = 1) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" ry="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def chrome_buttons(x: int, y: int) -> str:
    return "\n".join(
        f'<circle cx="{x + i * 28}" cy="{y}" r="8" fill="{color}"/>'
        for i, color in enumerate(["#ff5f57", "#febc2e", "#28c840"])
    )


def render_terminal(spec: ScreenshotSpec) -> str:
    width = spec.width
    content_width = width - 96
    max_chars = max(48, content_width // 15)
    raw_lines = spec.content.splitlines() or ["# No experiment content provided"]
    visual_lines: list[tuple[str, str]] = []

    for raw_line in raw_lines:
        line = raw_line.rstrip()
        if line.startswith(("$", "#", ">")):
            fill = "#93c5fd"
        elif line.startswith(("✓", "✔", "PASS", "SUCCESS")):
            fill = "#86efac"
        elif line.startswith(("✗", "ERROR", "FAIL")):
            fill = "#fca5a5"
        elif line.strip().startswith("#"):
            fill = "#94a3b8"
        else:
            fill = "#e5e7eb"
        for wrapped in wrap_text(line, max_chars):
            visual_lines.append((wrapped, fill))

    height = 128 + len(visual_lines) * 34 + 48
    parts = [svg_frame(width, height, "#0f172a")]
    parts.append(svg_rect(28, 28, width - 56, 56, fill="#111827", radius=18))
    parts.append(chrome_buttons(58, 56))
    parts.append(svg_text(150, 64, spec.title, size=22, fill="#e5e7eb", weight="700"))
    if spec.subtitle:
        parts.append(svg_text(width - 410, 64, spec.subtitle, size=18, fill="#94a3b8"))
    parts.append(svg_rect(28, 84, width - 56, height - 112, fill="#020617", stroke="#334155", radius=18))

    y = 132
    mono = "'SFMono-Regular', Menlo, Consolas, 'Noto Sans Mono CJK SC', monospace"
    for line, fill in visual_lines:
        parts.append(svg_text(58, y, line, size=23, fill=fill, family=mono))
        y += 34

    parts.append("</svg>")
    return "\n".join(parts)


def render_web(spec: ScreenshotSpec) -> str:
    width = spec.width
    max_chars = max(42, (width - 180) // 18)
    content_lines = flatten_wrapped_lines(spec.content, max_chars)
    card_height = max(280, 96 + len(content_lines) * 42)
    height = card_height + 170

    parts = [svg_frame(width, height, "#eef2ff")]
    parts.append(svg_rect(28, 28, width - 56, 82, fill="#ffffff", stroke="#c7d2fe", radius=22))
    parts.append(chrome_buttons(64, 70))
    parts.append(svg_rect(164, 50, width - 240, 40, fill="#f8fafc", stroke="#e2e8f0", radius=18))
    parts.append(svg_text(192, 77, "https://lab.local/experiment/process", size=18, fill="#64748b"))
    parts.append(svg_rect(56, 140, width - 112, card_height, fill="#ffffff", stroke="#cbd5e1", radius=24))
    parts.append(svg_text(92, 190, spec.title, size=34, fill="#1e3a8a", weight="800"))
    if spec.subtitle:
        parts.append(svg_text(92, 228, spec.subtitle, size=22, fill="#64748b"))
        start_y = 280
    else:
        start_y = 250

    y = start_y
    for i, line in enumerate(content_lines, start=1):
        marker = str(i) if not re.match(r"^\d+[.)]\s+", line) else re.sub(r"^([0-9]+).*", r"\1", line)
        clean = re.sub(r"^\d+[.)]\s+", "", line)
        parts.append(svg_rect(92, y - 28, 36, 36, fill="#2563eb", radius=18))
        parts.append(svg_text(105, y - 4, marker[:2], size=18, fill="#ffffff", weight="700"))
        parts.append(svg_text(150, y - 2, clean, size=24, fill="#111827"))
        y += 42

    parts.append("</svg>")
    return "\n".join(parts)


def render_config(spec: ScreenshotSpec) -> str:
    width = spec.width
    rows = parse_rows(spec.content)
    height = 170 + max(1, len(rows)) * 54 + 48
    parts = [svg_frame(width, height, "#f8fafc")]
    parts.append(svg_rect(32, 28, width - 64, height - 56, fill="#ffffff", stroke="#cbd5e1", radius=20))
    parts.append(svg_text(70, 82, spec.title, size=32, fill="#0f172a", weight="800"))
    if spec.subtitle:
        parts.append(svg_text(70, 116, spec.subtitle, size=20, fill="#64748b"))
    table_y = 140
    parts.append(svg_rect(70, table_y, width - 140, 48, fill="#e0f2fe", stroke="#bae6fd", radius=12))
    parts.append(svg_text(96, table_y + 32, "配置项", size=22, fill="#075985", weight="700"))
    parts.append(svg_text(width // 2, table_y + 32, "参数 / 操作", size=22, fill="#075985", weight="700"))

    y = table_y + 58
    for idx, (key, value) in enumerate(rows):
        fill = "#ffffff" if idx % 2 == 0 else "#f8fafc"
        parts.append(svg_rect(70, y - 34, width - 140, 48, fill=fill, stroke="#e2e8f0", radius=8))
        parts.append(svg_text(96, y - 2, key, size=21, fill="#334155", weight="700"))
        parts.append(svg_text(width // 2, y - 2, value, size=21, fill="#111827"))
        y += 54

    parts.append("</svg>")
    return "\n".join(parts)


def render_checklist(spec: ScreenshotSpec) -> str:
    width = spec.width
    lines = [line.strip("-• 　") for line in spec.content.splitlines() if line.strip()]
    height = 150 + max(1, len(lines)) * 58 + 50
    parts = [svg_frame(width, height, "#f0fdf4")]
    parts.append(svg_text(58, 76, spec.title, size=34, fill="#14532d", weight="800"))
    if spec.subtitle:
        parts.append(svg_text(58, 112, spec.subtitle, size=21, fill="#64748b"))
    y = 150
    for line in lines:
        parts.append(svg_rect(58, y - 36, width - 116, 46, fill="#ffffff", stroke="#bbf7d0", radius=14))
        parts.append(svg_rect(82, y - 25, 24, 24, fill="#22c55e", radius=6))
        parts.append(svg_text(87, y - 6, "✓", size=18, fill="#ffffff", weight="800"))
        parts.append(svg_text(124, y - 4, line, size=23, fill="#166534"))
        y += 58
    parts.append("</svg>")
    return "\n".join(parts)


def svg_frame(width: int, height: int, background: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        f'<rect width="{width}" height="{height}" fill="{background}"/>'
    )


def flatten_wrapped_lines(content: str, max_chars: int) -> list[str]:
    output: list[str] = []
    for line in content.splitlines():
        clean = line.strip("-• 　")
        if not clean:
            continue
        output.extend(wrap_text(clean, max_chars))
    return output or ["未提供实验步骤"]


def parse_rows(content: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for raw_line in content.splitlines():
        line = raw_line.strip("-• 　")
        if not line:
            continue
        if "=" in line:
            key, value = line.split("=", 1)
        elif "：" in line:
            key, value = line.split("：", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            key, value = f"步骤 {len(rows) + 1}", line
        rows.append((key.strip(), value.strip()))
    return rows or [("步骤 1", "未提供实验配置")]


def render_svg(spec: ScreenshotSpec) -> str:
    renderers: dict[str, Callable[[ScreenshotSpec], str]] = {
        "terminal": render_terminal,
        "shell": render_terminal,
        "console": render_terminal,
        "web": render_web,
        "browser": render_web,
        "dashboard": render_web,
        "config": render_config,
        "table": render_config,
        "checklist": render_checklist,
        "steps": render_checklist,
    }
    renderer = renderers.get(spec.style, render_terminal)
    return renderer(spec)


def relpath_for_markdown(image_path: Path, markdown_path: Path) -> str:
    relative = os.path.relpath(image_path, start=markdown_path.parent)
    return Path(relative).as_posix()


def render_markdown(
    input_path: Path,
    output_dir: Path,
    processed_markdown: Path,
    manifest_path: Path,
) -> list[ScreenshotResult]:
    markdown = input_path.read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    processed_markdown.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    results: list[ScreenshotResult] = []

    def replace_match(match: Match[str]) -> str:
        index = len(results) + 1
        body = match.group("body")
        spec = parse_spec(body, index)
        slug = slugify(spec.title, f"experiment-{index:02d}")
        stem = f"experiment-{index:02d}-{slug}"
        source_path = output_dir / f"{stem}.txt"
        image_path = output_dir / f"{stem}.svg"
        source_path.write_text(body.strip() + "\n", encoding="utf-8")

        try:
            image_path.write_text(render_svg(spec), encoding="utf-8")
            markdown_image_path = relpath_for_markdown(image_path, processed_markdown)
            results.append(ScreenshotResult(
                index=index,
                title=spec.title,
                style=spec.style,
                source_path=str(source_path),
                image_path=str(image_path),
                markdown_image_path=markdown_image_path,
                status="rendered",
            ))
            return f"![{spec.title}]({markdown_image_path})"
        except OSError as exc:
            results.append(ScreenshotResult(
                index=index,
                title=spec.title,
                style=spec.style,
                source_path=str(source_path),
                image_path=str(image_path),
                markdown_image_path="",
                status="failed",
                error=str(exc),
            ))
            return match.group(0)

    processed = COMMENT_BLOCK_RE.sub(replace_match, markdown)
    processed = FENCE_BLOCK_RE.sub(replace_match, processed)
    processed_markdown.write_text(processed, encoding="utf-8")

    manifest = {
        "input": str(input_path),
        "processed_markdown": str(processed_markdown),
        "output_dir": str(output_dir),
        "renderer": "deterministic-svg",
        "screenshots": [asdict(result) for result in results],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Render experiment screenshot placeholders to SVG images")
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--output-dir", required=True, help="Directory for generated screenshot SVG files")
    parser.add_argument("--processed-markdown", required=True, help="Markdown copy with placeholders replaced by images")
    parser.add_argument("--manifest", required=True, help="JSON manifest describing rendered screenshots")
    args = parser.parse_args()

    results = render_markdown(
        input_path=Path(args.input),
        output_dir=Path(args.output_dir),
        processed_markdown=Path(args.processed_markdown),
        manifest_path=Path(args.manifest),
    )

    rendered_count = sum(1 for result in results if result.status == "rendered")
    failed_count = sum(1 for result in results if result.status == "failed")
    print(f"Experiment screenshots: {len(results)} found, {rendered_count} rendered, {failed_count} failed")
    return 1 if failed_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
