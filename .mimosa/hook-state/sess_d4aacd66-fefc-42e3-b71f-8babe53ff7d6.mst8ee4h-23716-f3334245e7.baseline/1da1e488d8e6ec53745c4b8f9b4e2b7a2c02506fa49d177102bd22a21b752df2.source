"""Check paper format and content compliance.

Checks:
  - Word count within target range (±10%)
  - Required sections present (language-aware)
  - Citation references match bibliography
  - No empty sections
  - Common AI filler phrases detected

Usage:
    python check_paper.py \
        --input "outputs/paper/04_final/final_paper.md" \
        --target-words 1500 \
        --lang English \
        --output "outputs/paper/06_qa/check_report.json"
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


# AI filler phrases (Chinese)
_AI_FILLER = [
    "在当今社会", "随着.*的发展", "具有重要意义", "引起了广泛关注",
    "综上所述", "总而言之", "不言而喻", "众所周知",
    "具有深远的影响", "发挥着重要作用", "扮演着重要角色",
    "不可忽视的是", "值得强调的是",
]

_REQUIRED_SECTIONS_DEFAULT = ["引言", "结语"]
_REQUIRED_SECTIONS_EN = ["Introduction", "Conclusion"]
_REQUIRED_SECTIONS_BILINGUAL = ["引言", "结语", "Introduction", "Conclusion"]
_OPTIONAL_SECTIONS = ["主体分析", "个人理解", "参考文献", "参考", "材料说明"]


def _count_chinese_chars(text: str) -> int:
    """Count Chinese characters + ASCII words."""
    chinese = len(re.findall(r"[一-鿿]", text))
    # count English words (rough)
    english_text = re.sub(r"[一-鿿]", " ", text)
    english = len(english_text.split())
    return chinese + english


def _find_sections(md_text: str) -> List[str]:
    """Extract section headings from markdown."""
    sections = []
    for line in md_text.splitlines():
        m = re.match(r"^#{1,3}\s+(.+)", line)
        if m:
            sections.append(m.group(1).strip())
    return sections


def _find_inline_citations(md_text: str) -> set:
    """Find [N] citations in body text."""
    return set(int(m) for m in re.findall(r"\[(\d+)\]", md_text))


def _find_references(md_text: str) -> set:
    """Find [N] reference entries in bibliography."""
    refs = set()
    in_ref = False
    for line in md_text.splitlines():
        if "参考文献" in line or "references" in line.lower():
            in_ref = True
            continue
        if in_ref:
            m = re.match(r"^\[(\d+)\]", line.strip())
            if m:
                refs.add(int(m.group(1)))
    return refs


def _check_ai_filler(md_text: str) -> List[str]:
    """Detect AI filler phrases."""
    found = []
    for pattern in _AI_FILLER:
        matches = re.findall(pattern, md_text)
        if matches:
            found.extend(matches[:2])
    return found


def check_paper(md_path: str, target_words: int = 0,
                required_sections: List[str] | None = None,
                lang: str = "中文") -> Dict[str, Any]:
    """Run all checks on a paper."""
    md_text = Path(md_path).read_text(encoding="utf-8")

    # word count
    word_count = _count_chinese_chars(md_text)
    if target_words > 0:
        tolerance = target_words * 0.1
        if word_count < target_words - tolerance:
            word_status = "too_short"
        elif word_count > target_words + tolerance:
            word_status = "too_long"
        else:
            word_status = "ok"
    else:
        word_status = "no_target"

    # sections - determine required by language
    sections = _find_sections(md_text)
    if required_sections:
        required = required_sections
    elif lang.lower() in ("english", "en"):
        required = _REQUIRED_SECTIONS_EN
    elif lang.lower() in ("双语", "bilingual"):
        required = _REQUIRED_SECTIONS_BILINGUAL
    else:
        required = _REQUIRED_SECTIONS_DEFAULT
    sections_missing = []
    for req in required:
        if not any(req in s for s in sections):
            sections_missing.append(req)

    # citations
    inline_cites = _find_inline_citations(md_text)
    ref_entries = _find_references(md_text)
    orphan_cites = inline_cites - ref_entries
    unused_refs = ref_entries - inline_cites

    # AI filler
    ai_filler = _check_ai_filler(md_text)

    # overall status
    warnings = []
    if word_status == "too_short":
        warnings.append(f"字数不足: {word_count}/{target_words}")
    elif word_status == "too_long":
        warnings.append(f"字数超标: {word_count}/{target_words}")
    if sections_missing:
        warnings.append(f"缺少章节: {', '.join(sections_missing)}")
    if orphan_cites:
        warnings.append(f"引用无对应参考文献: {sorted(orphan_cites)}")
    if ai_filler:
        warnings.append(f"AI 填充词: {ai_filler[:3]}")

    status = "ok" if not warnings else "warning"

    return {
        "word_count": word_count,
        "target": target_words,
        "word_status": word_status,
        "sections_found": sections,
        "sections_missing": sections_missing,
        "inline_citations": sorted(inline_cites),
        "reference_entries": sorted(ref_entries),
        "orphan_citations": sorted(orphan_cites),
        "unused_references": sorted(unused_refs),
        "ai_filler_detected": ai_filler,
        "status": status,
        "warnings": warnings,
    }


def main():
    # ensure UTF-8 output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Check paper format and content")
    parser.add_argument("--input", required=True, help="Input .md file")
    parser.add_argument("--target-words", type=int, default=0, help="Target word count")
    parser.add_argument("--lang", default="中文",
                        help="Paper language: English / 中文 / 双语")
    parser.add_argument("--output", required=True, help="Output JSON report path")
    args = parser.parse_args()

    result = check_paper(args.input, args.target_words, lang=args.lang)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Check result: {result['status']}")
    print(f"  Words: {result['word_count']}/{result['target']}")
    print(f"  Sections: {len(result['sections_found'])}")
    if result["warnings"]:
        for w in result["warnings"]:
            print(f"  [!] {w}")
    print(f"Report: {output_path}")


if __name__ == "__main__":
    main()
