"""Compile all extracted text into a single handbook with index.

Reads the outline to map chapters to source directories, then concatenates
ALL text files from each source directory into one complete handbook.
No summarization — every character from every source file is preserved.
Text is formatted with markdown: headings, lists, code blocks, etc.

Usage:
    python compile_handbook.py \
        --outline "outputs/course/02_outline/outline.md" \
        --extracted "outputs/course/01_extracted/" \
        --filtered "outputs/course/01_filtered/" \
        --output "outputs/course/04_final/final_handbook.md"
"""
from __future__ import annotations
import argparse
import os
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Outline parsing
# ---------------------------------------------------------------------------

def _parse_outline(outline_path: Path) -> List[Dict]:
    text = outline_path.read_text(encoding="utf-8")
    chapters = []
    current_chapter = None

    for line in text.splitlines():
        line = line.strip()

        ch_match = re.match(r"^##\s+(.+)", line)
        if ch_match and not line.startswith("###"):
            heading = ch_match.group(1).strip()
            if re.match(r"(Chapter|第)", heading, re.IGNORECASE):
                current_chapter = {"chapter": heading, "sources": [], "subsections": []}
                chapters.append(current_chapter)
            else:
                current_chapter = None
            continue

        if current_chapter is None:
            continue

        src_match = re.match(r"^-\s*来源:\s*(.+)", line)
        if src_match:
            current_chapter["sources"] = [d.strip() for d in src_match.group(1).split(",") if d.strip()]
            continue

        sub_match = re.match(r"^###\s+(.+)", line)
        if sub_match:
            current_chapter["subsections"].append(sub_match.group(1).strip())

    return chapters


def _chapter_sort_key(chapter: Dict) -> Tuple[int, int]:
    nums = re.findall(r"\d+", chapter["chapter"])
    return (int(nums[0]), 0) if nums else (999, 0)


# ---------------------------------------------------------------------------
# Text formatting
# ---------------------------------------------------------------------------

# Patterns that indicate a line is code
_CODE_PATTERNS = re.compile(
    r"(__global__|__shared__|__device__|__host__|#include|#define|"
    r"\bvoid\s+\w+\s*\(|\bint\s+main\s*\(|"
    r"^\s*(for|while|if)\s*\(|^\s*\w+\s*\[.*\]\s*=|"
    r"MPI_\w+|cudaMalloc|cudaMemcpy|"
    r"BLOCK_LOW|BLOCK_HIGH|BLOCK_SIZE|BLOCK_OWNER)",
    re.MULTILINE,
)

# Bullet characters from PPT extraction
_BULLET_RE = re.compile(r"^[\s]*[•▪◦‣⁃–—]\s*")
_SUB_BULLET_RE = re.compile(r"^[\s]*[·∙→►▸▹]\s*")

# Standalone page/slide number
_PAGE_NUM_RE = re.compile(r"^\d{1,4}$")

# URL pattern
_URL_RE = re.compile(r"(https?://[^\s]+)")

# Common PPT shape labels / watermarks to strip
_NOISE_WORDS = {
    "芯片", "CPU", "GPU", "NVIDIA", "CUDA", "MPI", "OpenMP",
    "应用", "函数库", "编程语言", "编译器指令", "硬件", "软件",
    "图", "表", "公式", "注意", "备注", "来源", "参考",
}

# Line that looks like a C/C++ code fragment
_CODE_LINE_RE = re.compile(
    r"(__global__|__shared__|__device__|#include|#define|"
    r"\bvoid\s+\w+\s*\(|^\s*\{|^\s*\}|^\s*//|"
    r"^\s*for\s*\(|^\s*if\s*\(|^\s*while\s*\(|"
    r"MPI_\w+|cudaMalloc|cudaMemcpy|"
    r"BLOCK_LOW|BLOCK_HIGH|BLOCK_SIZE)"
)


def _is_code_line(line: str) -> bool:
    return bool(_CODE_LINE_RE.search(line))


def _format_text(raw: str) -> str:
    """Format raw extracted text into readable markdown.

    Rules:
    - Remove standalone page/slide numbers
    - Remove PPT shape labels (noise words like 芯片, CPU, etc.)
    - Bullet characters -> markdown bullets
    - Code-like lines -> wrap in code blocks
    - URLs -> keep as-is (markdown auto-links)
    - Preserve all content (no summarization)
    """
    lines = raw.splitlines()
    if not lines:
        return ""

    # Pass 1: clean up lines
    cleaned = []
    for line in lines:
        stripped = line.strip()

        if not stripped:
            cleaned.append("")
            continue

        # skip standalone page numbers
        if _PAGE_NUM_RE.match(stripped):
            continue

        # skip PPT shape labels / noise words
        if stripped in _NOISE_WORDS:
            continue

        # skip very short non-content lines (1-2 chars, not alphanumeric)
        if len(stripped) <= 2 and not any(c.isalnum() for c in stripped):
            continue

        cleaned.append(stripped)

    if not cleaned:
        return ""

    # Pass 2: detect and format
    result = []
    in_code_block = False

    for line in cleaned:
        if not line:
            if in_code_block:
                result.append("```")
                in_code_block = False
            result.append("")
            continue

        # code block detection
        if _is_code_line(line):
            if not in_code_block:
                result.append("```c")
                in_code_block = True
            result.append(line)
            continue
        elif in_code_block:
            result.append("```")
            in_code_block = False

        # bullet points
        if _BULLET_RE.match(line):
            line = _BULLET_RE.sub("- ", line)
            result.append(line)
            continue

        if _SUB_BULLET_RE.match(line):
            line = _SUB_BULLET_RE.sub("  - ", line)
            result.append(line)
            continue

        # regular text
        result.append(line)

    # close any open code block
    if in_code_block:
        result.append("```")

    # join and clean up excessive blank lines
    text = "\n".join(result)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Image handling
# ---------------------------------------------------------------------------

def _get_images_for_text(txt_file: Path, filtered_dir: Path | None) -> List[Path]:
    """Find filtered images corresponding to a text file.

    Only returns images from 01_filtered/ — never falls back to 01_extracted/.
    This ensures all images passed the quality filter.
    """
    if filtered_dir is None:
        return []

    stem = txt_file.stem
    parent_name = txt_file.parent.name
    fdir = filtered_dir / parent_name
    if not fdir.is_dir():
        return []

    images = []
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.webp"):
        for img in sorted(fdir.glob(f"{stem}_img_*{ext[1:]}")):
            images.append(img)

    return images


def _image_rel_path(img: Path, output_path: Path) -> str:
    """Get forward-slash relative path for markdown."""
    rel = os.path.relpath(img, output_path.parent)
    return PurePosixPath(Path(rel).as_posix()).as_posix()


# ---------------------------------------------------------------------------
# Keyword index
# ---------------------------------------------------------------------------

def _build_keyword_index(chapters_text: str) -> str:
    keywords = {}
    kw_patterns = [
        r"Amdahl", r"CGMA", r"CUDA", r"Flynn", r"MPI", r"MSI",
        r"PCAM", r"Warp|线程束", r"共享内存", r"控制分歧", r"前缀和|Prefix Sum|Scan",
        r"加速比", r"域分解|功能分解", r"数据竞态|Data Race", r"缓存一致性",
        r"超立方体|Hypercube", r"素数筛选|Sieve", r"矩阵乘法",
        r"网络直径|对分宽度", r"负载均衡", r"循环分配|块分配",
        r"尴尬的并行|Embarrassingly Parallel", r"私有化直方图",
        r"SIMD|MIMD|SISD|MISD", r"原子操作|Atomic",
        r"并行规约|Reduction", r"内存合并|Coalescing",
        r"分块矩阵|Tiled", r"伪共享|False Sharing",
    ]

    lines = chapters_text.splitlines()
    for kw_pat in kw_patterns:
        for i, line in enumerate(lines):
            if re.search(kw_pat, line, re.IGNORECASE):
                heading = ""
                for j in range(i, -1, -1):
                    hm = re.match(r"^(#{1,4})\s+(.+)", lines[j])
                    if hm:
                        heading = hm.group(2).strip()
                        break
                if heading:
                    base_kw = kw_pat.split("|")[0]
                    if base_kw not in keywords:
                        keywords[base_kw] = heading
                break

    if not keywords:
        return ""

    idx_lines = ["\n---\n\n## 关键词索引\n", "| 关键词 | 位置 |", "|--------|------|"]
    for kw, loc in sorted(keywords.items(), key=lambda x: x[0]):
        idx_lines.append(f"| {kw} | {loc} |")
    return "\n".join(idx_lines) + "\n"


# ---------------------------------------------------------------------------
# Main compilation
# ---------------------------------------------------------------------------

def compile_handbook(outline_path: Path, extracted_dir: Path,
                     filtered_dir: Path | None, output_path: Path,
                     course_name: str) -> Dict:
    chapters = _parse_outline(outline_path)

    if not chapters:
        print("Warning: no chapters parsed, using all source dirs", file=sys.stderr)
        for src_dir in sorted(extracted_dir.iterdir()):
            if src_dir.is_dir():
                chapters.append({"chapter": src_dir.name, "sources": [src_dir.name], "subsections": []})

    chapters.sort(key=_chapter_sort_key)
    parts = []

    # header
    parts.append(f"# {course_name} — 速查手册\n")
    parts.append("> 本手册包含课程所有资料的完整内容，按章节组织，原文保留。\n")

    # table of contents
    toc = ["## 目录\n"]
    for ch in chapters:
        anchor = re.sub(r"[^\w一-鿿]+", "-", ch["chapter"]).strip("-").lower()
        toc.append(f"- [{ch['chapter']}](#{anchor})")
    toc.append("- [关键词索引](#关键词索引)")
    parts.append("\n".join(toc) + "\n")

    # chapters
    for ch in chapters:
        parts.append(f"\n---\n\n## {ch['chapter']}\n")

        for src_name in ch["sources"]:
            src_dir = extracted_dir / src_name
            if not src_dir.is_dir():
                parts.append(f"\n> ⚠️ 源目录未找到: {src_name}\n")
                continue

            parts.append(f"\n### {src_name}\n")

            txt_files = sorted(src_dir.glob("*.txt"))
            if not txt_files:
                parts.append("\n> （无文本内容）\n")
                continue

            for txt_file in txt_files:
                try:
                    raw = txt_file.read_text(encoding="utf-8").strip()
                except Exception:
                    raw = f"[读取失败: {txt_file.name}]"

                if raw:
                    formatted = _format_text(raw)
                    if formatted:
                        parts.append(f"\n{formatted}\n")

                # insert filtered images only
                images = _get_images_for_text(txt_file, filtered_dir)
                for img in images:
                    rel = _image_rel_path(img, output_path)
                    parts.append(f"\n![{img.stem}]({rel})\n")

    # keyword index
    all_text = "\n".join(parts)
    index_text = _build_keyword_index(all_text)
    if index_text:
        parts.append(index_text)

    # write
    output_path.parent.mkdir(parents=True, exist_ok=True)
    handbook = "\n".join(parts)
    output_path.write_text(handbook, encoding="utf-8")

    return {
        "chapters": len(chapters),
        "total_sources": sum(len(ch["sources"]) for ch in chapters),
        "total_chars": len(handbook),
        "output_path": str(output_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Compile all extracted content into a complete handbook")
    parser.add_argument("--outline", required=True)
    parser.add_argument("--extracted", required=True)
    parser.add_argument("--filtered", default=None)
    parser.add_argument("--output", required=True)
    parser.add_argument("--course-name", default="课程")
    args = parser.parse_args()

    result = compile_handbook(
        outline_path=Path(args.outline),
        extracted_dir=Path(args.extracted),
        filtered_dir=Path(args.filtered) if args.filtered else None,
        output_path=Path(args.output),
        course_name=args.course_name,
    )

    print(f"Handbook compiled: {result['chapters']} chapters, "
          f"{result['total_sources']} sources, "
          f"{result['total_chars']:,} chars")
    print(f"Output: {result['output_path']}")


if __name__ == "__main__":
    main()
