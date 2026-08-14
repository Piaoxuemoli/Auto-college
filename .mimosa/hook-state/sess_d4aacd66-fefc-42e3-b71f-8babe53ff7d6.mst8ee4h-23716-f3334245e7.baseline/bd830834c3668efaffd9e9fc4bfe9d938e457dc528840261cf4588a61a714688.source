"""Parse final_slides.md slide cards into PresentationBuilder specs.

Reads the structured slide card format produced by slide-writer.md and converts
it into a list of dicts that PresentationBuilder.add_specs() can consume.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

_SLIDE_RE = re.compile(r"^#\s+Slide\s+\d+:\s*(.*)", re.MULTILINE)
_META_RE = re.compile(r"<!--\s*slide:\s*(.*?)\s*-->")
_FIELD_RE = re.compile(r"(\w+)=([^\s]+)")


def _parse_metadata_comment(text: str) -> Dict[str, str]:
    m = _META_RE.search(text)
    if not m:
        return {}
    return dict(_FIELD_RE.findall(m.group(1)))


def _extract_section(text: str, header: str) -> Optional[str]:
    """Extract text under a header like 'Key message:' until the next section.

    Handles both inline content (Key message: text) and multi-line content
    (Key message:\ntext\ntext).
    """
    escaped = re.escape(header)
    # Match header followed by optional whitespace, then content until next
    # section header (line starting with uppercase word + colon) or end
    pattern = re.compile(
        rf"^{escaped}\s*(.*?)(?=^[A-Z]\w+.*?:|\Z)",
        re.MULTILINE | re.DOTALL)
    m = pattern.search(text)
    if m:
        content = m.group(1).strip()
        return content if content else None
    return None


def _extract_bullets(text: str) -> List[str]:
    """Extract bullet points from visible content section."""
    bullets = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())
        elif line.startswith("* "):
            bullets.append(line[2:].strip())
    return bullets


def _split_slides(raw: str) -> List[str]:
    """Split the markdown into individual slide blocks.

    Each block starts with the metadata comment (<!-- slide: ... -->) if present,
    followed by the heading and content. Falls back to splitting on headings if
    no metadata comments are found.
    """
    meta_positions = [m.start() for m in _META_RE.finditer(raw)]
    if meta_positions:
        slides = []
        for i, start in enumerate(meta_positions):
            end = meta_positions[i + 1] if i + 1 < len(meta_positions) else len(raw)
            slides.append(raw[start:end])
        return slides
    # Fallback: split on headings
    positions = [m.start() for m in _SLIDE_RE.finditer(raw)]
    if not positions:
        return []
    slides = []
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(raw)
        slides.append(raw[start:end])
    return slides


def _slide_to_spec(block: str, slide_title: str) -> Dict[str, Any]:
    """Convert a single slide block into a spec dict."""
    meta = _parse_metadata_comment(block)
    layout = meta.get("layout", "")
    role = meta.get("role", "")

    key_message = _extract_section(block, "Key message:")
    visible_text = _extract_section(block, "Visible content:")
    speaker_notes = _extract_section(block, "Speaker notes:")
    bullets = _extract_bullets(visible_text) if visible_text else []

    spec: Dict[str, Any] = {}

    # Map role/layout to template type
    if role == "cover" or layout in ("title-hero", "title-with-subtitle"):
        spec["type"] = "cover"
        spec["title"] = slide_title
        if key_message:
            spec["subtitle"] = key_message
    elif role == "hook" or layout in ("question", "contrast", "problem-card"):
        spec["type"] = "question"
        spec["question"] = key_message or slide_title
    elif role == "transition" or layout in ("section-divider", "big-number"):
        if layout == "big-number" and key_message:
            spec["type"] = "stat_hero"
            spec["stat"] = key_message
            spec["stat_label"] = slide_title
        else:
            spec["type"] = "section_divider"
            section_num = meta.get("section", "1")
            spec["section_number"] = section_num
            spec["section_title"] = slide_title
    elif role == "takeaway" or layout in ("three-takeaways", "closing-statement"):
        if layout == "closing-statement":
            spec["type"] = "closing"
            spec["title"] = slide_title
        else:
            spec["type"] = "three_takeaways"
            spec["title"] = slide_title
            spec["takeaways"] = bullets[:4] if bullets else [key_message or ""]
    elif layout == "two-column":
        spec["type"] = "two_column"
        spec["title"] = slide_title
        # Try to split bullets into two halves
        mid = len(bullets) // 2
        spec["left_title"] = "Part 1"
        spec["left_bullets"] = bullets[:mid] if mid > 0 else bullets
        spec["right_title"] = "Part 2"
        spec["right_bullets"] = bullets[mid:] if mid > 0 else bullets
    elif layout == "process-flow":
        spec["type"] = "process_flow"
        spec["title"] = slide_title
        spec["steps"] = bullets if bullets else [key_message or ""]
    elif layout == "before-after":
        spec["type"] = "before_after"
        spec["title"] = slide_title
        mid = len(bullets) // 2
        spec["left_items"] = bullets[:mid] if mid > 0 else bullets
        spec["right_items"] = bullets[mid:] if mid > 0 else bullets
    elif layout == "quote-plus-analysis":
        spec["type"] = "quote"
        spec["quote"] = key_message or slide_title
        spec["author"] = ""
    elif layout == "diagram":
        spec["type"] = "diagram"
        spec["title"] = slide_title
        spec["items"] = bullets if bullets else [key_message or ""]
    elif layout == "icon-grid":
        spec["type"] = "icon_grid"
        spec["title"] = slide_title
        # Parse bullets with **bold title**：description format
        items = []
        for b in bullets:
            if "**" in b and "：" in b:
                # Extract bold title and description
                import re
                m = re.match(r"\*\*(.+?)\*\*[：:]\s*(.*)", b)
                if m:
                    items.append({"title": m.group(1), "desc": m.group(2)})
                else:
                    items.append({"title": b, "desc": ""})
            elif "**" in b:
                # Bold title without description
                import re
                title = re.sub(r"\*\*(.+?)\*\*", r"\1", b)
                items.append({"title": title, "desc": ""})
            else:
                items.append({"title": b, "desc": ""})
        spec["items"] = items if items else [{"title": key_message or slide_title, "desc": ""}]
    else:
        # Default: bullet list
        spec["type"] = "bullet_list"
        spec["title"] = slide_title
        spec["bullets"] = bullets if bullets else [key_message or ""]
        if key_message:
            spec["key_message"] = key_message

    if speaker_notes:
        spec["_speaker_notes"] = speaker_notes

    return spec


def parse_slides_md(path: str) -> List[Dict[str, Any]]:
    """Parse final_slides.md and return a list of spec dicts for PresentationBuilder."""
    raw = Path(path).read_text(encoding="utf-8")
    blocks = _split_slides(raw)
    specs = []
    for block in blocks:
        title_match = _SLIDE_RE.search(block)
        title = title_match.group(1).strip() if title_match else "Untitled"
        spec = _slide_to_spec(block, title)
        specs.append(spec)
    return specs
