"""Export slide specs to a Slidev project directory.

Converts the internal spec format (from slide_card_parser or PresentationBuilder)
into Slidev-compatible Markdown with YAML frontmatter, speaker notes, and
appropriate layout mappings.

Reference: references/slidev/skills/slidev/SKILL.md (MIT License)
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional


# --- Layout mapping: our spec type -> Slidev layout ---
_LAYOUT_MAP = {
    "cover": "cover",
    "question": "center",
    "bullet_list": "default",
    "two_column": "two-cols",
    "section_divider": "section",
    "stat_hero": "fact",
    "pros_cons": "two-cols",
    "before_after": "two-cols",
    "three_takeaways": "default",
    "quote": "quote",
    "closing": "end",
    "icon_grid": "default",
    "diagram": "default",
    "process_flow": "default",
    "phases": "default",
    "table": "default",
}


def _escape_yaml(s: str) -> str:
    """Escape a string for YAML frontmatter value."""
    if not s:
        return '""'
    # If it contains special chars, quote it
    for ch in [":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`"]:
        if ch in s:
            return f'"{s.replace(chr(34), chr(92) + chr(34))}"'
    return s


def _spec_to_slidev_body(spec: Dict[str, Any], index: int) -> str:
    """Convert a single spec to Slidev Markdown body (no frontmatter)."""
    slide_type = spec.get("type", "bullet_list")
    speaker_notes = spec.get("_speaker_notes", "")
    lines = []
    _append_slide_content(lines, slide_type, spec)
    if speaker_notes:
        lines.append("<!--")
        lines.append(speaker_notes)
        lines.append("-->")
        lines.append("")
    return "\n".join(lines)


def _spec_to_slidev(spec: Dict[str, Any], index: int) -> str:
    """Convert a single spec dict to Slidev Markdown with frontmatter."""
    slide_type = spec.get("type", "bullet_list")
    layout = _LAYOUT_MAP.get(slide_type, "default")
    speaker_notes = spec.get("_speaker_notes", "")

    lines = []

    # Frontmatter
    lines.append("---")
    lines.append(f"layout: {layout}")
    lines.append("---")
    lines.append("")

    _append_slide_content(lines, slide_type, spec)

    # Speaker notes
    if speaker_notes:
        lines.append("<!--")
        lines.append(speaker_notes)
        lines.append("-->")
        lines.append("")

    return "\n".join(lines)


def _append_slide_content(lines: list, slide_type: str, spec: dict) -> None:
    """Append slide body content to lines list."""
    # Content based on type
    if slide_type == "cover":
        title = spec.get("title", "")
        subtitle = spec.get("subtitle", "")
        course = spec.get("course", "")
        student = spec.get("student", "")
        date = spec.get("date", "")
        if title:
            lines.append(f"# {title}")
            lines.append("")
        if subtitle:
            lines.append(f"## {subtitle}")
            lines.append("")
        meta = " / ".join(filter(None, [course, student, date]))
        if meta:
            lines.append(f"*{meta}*")
            lines.append("")

    elif slide_type == "question":
        question = spec.get("question", spec.get("title", ""))
        subtitle = spec.get("subtitle", "")
        lines.append(f"# {question}")
        lines.append("")
        if subtitle:
            lines.append(f"> {subtitle}")
            lines.append("")

    elif slide_type == "bullet_list":
        title = spec.get("title", "")
        key_message = spec.get("key_message", "")
        bullets = spec.get("bullets", [])
        if title:
            lines.append(f"# {title}")
            lines.append("")
        if key_message:
            lines.append(f"**{key_message}**")
            lines.append("")
        if bullets:
            lines.append("<v-clicks>")
            lines.append("")
            for b in bullets:
                lines.append(f"- {b}")
            lines.append("")
            lines.append("</v-clicks>")
            lines.append("")

    elif slide_type == "two_column":
        title = spec.get("title", "")
        left_title = spec.get("left_title", "")
        left_bullets = spec.get("left_bullets", [])
        right_title = spec.get("right_title", "")
        right_bullets = spec.get("right_bullets", [])
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append("::left::")
        lines.append("")
        if left_title:
            lines.append(f"### {left_title}")
            lines.append("")
        for b in left_bullets:
            lines.append(f"- {b}")
        lines.append("")
        lines.append("::right::")
        lines.append("")
        if right_title:
            lines.append(f"### {right_title}")
            lines.append("")
        for b in right_bullets:
            lines.append(f"- {b}")
        lines.append("")

    elif slide_type == "section_divider":
        num = spec.get("section_number", "")
        s_title = spec.get("section_title", spec.get("title", ""))
        lines.append(f"# {num}. {s_title}" if num else f"# {s_title}")
        lines.append("")

    elif slide_type == "stat_hero":
        stat = spec.get("stat", "")
        stat_label = spec.get("stat_label", "")
        context = spec.get("context", "")
        title = spec.get("title", "")
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append(f"# {stat}")
        lines.append("")
        if stat_label:
            lines.append(f"**{stat_label}**")
            lines.append("")
        if context:
            lines.append(context)
            lines.append("")

    elif slide_type == "pros_cons":
        title = spec.get("title", "")
        pros = spec.get("pros", [])
        cons = spec.get("cons", [])
        pros_label = spec.get("pros_label", "Pros / 优点")
        cons_label = spec.get("cons_label", "Cons / 缺点")
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append("::left::")
        lines.append("")
        lines.append(f"### {pros_label}")
        lines.append("")
        for p in pros:
            lines.append(f"- {p}")
        lines.append("")
        lines.append("::right::")
        lines.append("")
        lines.append(f"### {cons_label}")
        lines.append("")
        for c in cons:
            lines.append(f"- {c}")
        lines.append("")

    elif slide_type == "before_after":
        title = spec.get("title", "")
        left_label = spec.get("left_label", "Before")
        right_label = spec.get("right_label", "After")
        left_items = spec.get("left_items", [])
        right_items = spec.get("right_items", [])
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append("::left::")
        lines.append("")
        lines.append(f"### {left_label}")
        lines.append("")
        for item in left_items:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("::right::")
        lines.append("")
        lines.append(f"### {right_label}")
        lines.append("")
        for item in right_items:
            lines.append(f"- {item}")
        lines.append("")

    elif slide_type == "three_takeaways":
        title = spec.get("title", "Summary")
        takeaways = spec.get("takeaways", [])
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append("<v-clicks>")
        lines.append("")
        for i, tk in enumerate(takeaways):
            lines.append(f"{i + 1}. {tk}")
        lines.append("")
        lines.append("</v-clicks>")
        lines.append("")

    elif slide_type == "quote":
        quote = spec.get("quote", "")
        author = spec.get("author", "")
        title = spec.get("title", "")
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append(f"> {quote}")
        if author:
            lines.append(f"> — {author}")
        lines.append("")

    elif slide_type == "closing":
        title = spec.get("title", "Thank You")
        message = spec.get("message", "")
        lines.append(f"# {title}")
        lines.append("")
        if message:
            lines.append(message)
            lines.append("")

    elif slide_type == "icon_grid":
        title = spec.get("title", "")
        items = spec.get("items", [])
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append("<v-clicks>")
        lines.append("")
        for i, item in enumerate(items):
            if isinstance(item, dict):
                item_title = item.get("title", "")
                item_desc = item.get("desc", "")
                lines.append(f"**{i + 1}. {item_title}**")
                if item_desc:
                    lines.append(f"  {item_desc}")
            else:
                lines.append(f"**{i + 1}. {item}**")
            lines.append("")
        lines.append("</v-clicks>")
        lines.append("")

    elif slide_type == "diagram":
        title = spec.get("title", "")
        items = spec.get("items", [])
        key_message = spec.get("key_message", "")
        if title:
            lines.append(f"# {title}")
            lines.append("")
        if key_message:
            lines.append(f"**{key_message}**")
            lines.append("")
        for i, item in enumerate(items):
            lines.append(f"{i + 1}. {item}")
        lines.append("")

    elif slide_type == "process_flow":
        title = spec.get("title", "")
        steps = spec.get("steps", [])
        if title:
            lines.append(f"# {title}")
            lines.append("")
        lines.append("<v-clicks>")
        lines.append("")
        for i, step in enumerate(steps):
            lines.append(f"{i + 1}. {step}")
        lines.append("")
        lines.append("</v-clicks>")
        lines.append("")

    else:
        # Fallback: generic content
        title = spec.get("title", "")
        if title:
            lines.append(f"# {title}")
            lines.append("")
        for key in ["bullets", "items", "steps"]:
            if key in spec:
                for item in spec[key]:
                    if isinstance(item, dict):
                        lines.append(f"- {item.get('title', str(item))}")
                    else:
                        lines.append(f"- {item}")
                lines.append("")
                break


def specs_to_slidev_md(specs: List[Dict[str, Any]], *,
                       title: str = "Presentation",
                       theme: str = "default") -> str:
    """Convert a list of slide specs to a complete Slidev Markdown file."""
    parts = []

    # Headmatter: merge deck config with first slide's layout
    first_layout = "cover"
    if specs:
        slide_type = specs[0].get("type", "bullet_list")
        first_layout = _LAYOUT_MAP.get(slide_type, "default")

    headmatter = [
        "---",
        f"theme: {theme}",
        f"title: {_escape_yaml(title)}",
        "transition: slide-left",
        f"layout: {first_layout}",
        "---",
        "",
    ]
    parts.extend(headmatter)

    # First slide: skip frontmatter (already in headmatter)
    if specs:
        parts.append(_spec_to_slidev_body(specs[0], 0))

    # Remaining slides
    for i, spec in enumerate(specs[1:], start=1):
        parts.append("---")
        parts.append("")
        parts.append(_spec_to_slidev(spec, i))

    return "\n".join(parts)


PACKAGE_JSON_TEMPLATE = """\
{{
  "name": "{name}",
  "private": true,
  "scripts": {{
    "dev": "slidev",
    "build": "slidev build",
    "export": "slidev export",
    "export-pptx": "slidev export --format pptx"
  }},
  "dependencies": {{
    "@slidev/cli": "latest",
    "@slidev/theme-default": "latest"
  }}
}}
"""


def export_slidev(specs: List[Dict[str, Any]], output_dir: str, *,
                  title: str = "Presentation",
                  theme: str = "default") -> str:
    """Export slide specs to a Slidev project directory.

    Creates:
    - slides.md (Slidev-compatible Markdown)
    - package.json (with @slidev/cli dependency)

    Returns the output directory path.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Generate slides.md
    md_content = specs_to_slidev_md(specs, title=title, theme=theme)
    (out / "slides.md").write_text(md_content, encoding="utf-8")

    # Generate package.json
    safe_name = title.lower().replace(" ", "-").replace("/", "-")[:50]
    pkg = PACKAGE_JSON_TEMPLATE.format(name=safe_name)
    (out / "package.json").write_text(pkg, encoding="utf-8")

    return str(out)


def export_slidev_from_md(slides_md_path: str, output_dir: str, *,
                          title: str = "Presentation",
                          theme: str = "default") -> str:
    """Convenience: parse slide card markdown and export to Slidev project."""
    from .slide_card_parser import parse_slides_md
    specs = parse_slides_md(slides_md_path)
    return export_slidev(specs, output_dir, title=title, theme=theme)
