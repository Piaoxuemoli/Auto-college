"""Render Mermaid code blocks in Markdown to image files via mermaid.ink.

This script intentionally uses only the Python standard library. It extracts
```mermaid fenced blocks from a Markdown file, saves each source block as .mmd,
renders it through the public mermaid.ink API, and writes a processed Markdown
copy where each rendered block is replaced by a Markdown image reference.

Usage:
    python paper-writer/scripts/render_mermaid.py \
        --input "paper-writer/outputs/demo/04_final/final_paper.md" \
        --output-dir "paper-writer/outputs/demo/03_figures" \
        --processed-markdown "paper-writer/outputs/demo/04_final/final_paper.rendered.md" \
        --manifest "paper-writer/outputs/demo/03_figures/mermaid_manifest.json"
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Match


MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(?P<code>.*?)(?:\n```)", re.IGNORECASE | re.DOTALL)
ACC_TITLE_RE = re.compile(r"^\s*accTitle\s*:\s*(?P<title>.+?)\s*$", re.IGNORECASE | re.MULTILINE)
TITLE_RE = re.compile(r"^\s*title\s+(?P<title>.+?)\s*$", re.IGNORECASE | re.MULTILINE)


@dataclass
class DiagramResult:
    index: int
    title: str
    source_path: str
    image_path: str | None
    markdown_image_path: str | None
    status: str
    error: str | None = None


def slugify(value: str, fallback: str) -> str:
    """Create a filesystem-safe slug while preserving readable CJK text."""
    value = value.strip().lower()
    value = re.sub(r"[\s/\\:;|]+", "-", value)
    value = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff._-]+", "", value)
    value = re.sub(r"-+", "-", value).strip("-._")
    return value or fallback


def extract_title(code: str, index: int) -> str:
    """Prefer Mermaid accessibility title, then Mermaid title, then Figure N."""
    for pattern in (ACC_TITLE_RE, TITLE_RE):
        match = pattern.search(code)
        if match:
            return match.group("title").strip().strip('"')
    return f"Figure {index}"


def encode_for_mermaid_ink(code: str) -> str:
    """mermaid.ink accepts URL-safe base64 without padding."""
    encoded = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
    return encoded.rstrip("=")


def render_mermaid_ink(code: str, output_path: Path, *, timeout: int, background: str) -> None:
    encoded = encode_for_mermaid_ink(code)
    query = urllib.parse.urlencode({"type": "png", "bgColor": background})
    url = f"https://mermaid.ink/img/{encoded}?{query}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "paper-writer-mermaid-renderer/1.0",
            "Accept": "image/png,*/*;q=0.8",
        },
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        data = response.read()

    if not data:
        raise RuntimeError("mermaid.ink returned an empty response")
    if "image" not in content_type.lower():
        sample = data[:200].decode("utf-8", errors="replace")
        raise RuntimeError(f"mermaid.ink returned non-image content: {content_type}; {sample}")

    output_path.write_bytes(data)


def relpath_for_markdown(image_path: Path, markdown_path: Path) -> str:
    relative = os.path.relpath(image_path, start=markdown_path.parent)
    return Path(relative).as_posix()


def render_markdown(
    input_path: Path,
    output_dir: Path,
    processed_markdown: Path,
    manifest_path: Path,
    *,
    timeout: int,
    background: str,
    allow_failures: bool,
) -> tuple[list[DiagramResult], str]:
    markdown = input_path.read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    processed_markdown.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    results: list[DiagramResult] = []

    def replace_block(match: Match[str]) -> str:
        code = match.group("code").strip()
        index = len(results) + 1
        title = extract_title(code, index)
        slug = slugify(title, f"diagram-{index:02d}")
        stem = f"{index:02d}-{slug}"
        source_path = output_dir / f"{stem}.mmd"
        image_path = output_dir / f"{stem}.png"
        source_path.write_text(code + "\n", encoding="utf-8")

        try:
            render_mermaid_ink(code, image_path, timeout=timeout, background=background)
            markdown_image_path = relpath_for_markdown(image_path, processed_markdown)
            result = DiagramResult(
                index=index,
                title=title,
                source_path=str(source_path),
                image_path=str(image_path),
                markdown_image_path=markdown_image_path,
                status="rendered",
            )
            results.append(result)
            return f"![{title}]({markdown_image_path})"
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
            result = DiagramResult(
                index=index,
                title=title,
                source_path=str(source_path),
                image_path=None,
                markdown_image_path=None,
                status="failed",
                error=str(exc),
            )
            results.append(result)
            return match.group(0)

    processed = MERMAID_BLOCK_RE.sub(replace_block, markdown)
    processed_markdown.write_text(processed, encoding="utf-8")

    manifest = {
        "input": str(input_path),
        "processed_markdown": str(processed_markdown),
        "output_dir": str(output_dir),
        "renderer": "mermaid.ink",
        "diagrams": [asdict(result) for result in results],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    failed = [result for result in results if result.status != "rendered"]
    if failed and not allow_failures:
        return results, f"Failed to render {len(failed)} Mermaid diagram(s); see {manifest_path}"
    return results, ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Markdown Mermaid blocks to PNG via mermaid.ink")
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--output-dir", required=True, help="Directory for generated .mmd and .png files")
    parser.add_argument("--processed-markdown", required=True, help="Markdown copy with Mermaid blocks replaced by images")
    parser.add_argument("--manifest", required=True, help="JSON manifest describing rendered diagrams")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument("--background", default="white", help="Mermaid image background color")
    parser.add_argument("--allow-failures", action="store_true", help="Exit 0 even if some diagrams fail")
    args = parser.parse_args()

    results, error = render_markdown(
        input_path=Path(args.input),
        output_dir=Path(args.output_dir),
        processed_markdown=Path(args.processed_markdown),
        manifest_path=Path(args.manifest),
        timeout=args.timeout,
        background=args.background,
        allow_failures=args.allow_failures,
    )

    rendered_count = sum(1 for result in results if result.status == "rendered")
    failed_count = sum(1 for result in results if result.status == "failed")
    print(f"Mermaid diagrams: {len(results)} found, {rendered_count} rendered, {failed_count} failed")

    if error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
