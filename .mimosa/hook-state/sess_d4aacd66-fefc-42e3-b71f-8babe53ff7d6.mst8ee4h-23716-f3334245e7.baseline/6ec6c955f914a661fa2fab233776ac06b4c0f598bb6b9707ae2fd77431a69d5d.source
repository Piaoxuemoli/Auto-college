"""Initialize paper-writer output directory.

Usage:
    python init_output_dir.py <paper-name> --target-words 1500 --lang English --author "张三 2021001 计算机系"
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def init_output_dir(name: str, target_words: int = 1500,
                    lang: str = "English", author: str = "") -> Path:
    """Create output directory structure for a paper."""
    base = Path("paper-writer/outputs") / name
    dirs = ["00_admin", "01_sources", "02_outline", "04_final",
            "05_exports", "06_qa"]
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)

    # write context
    context = {
        "paper_name": name,
        "target_words": target_words,
        "lang": lang,
        "author": author,
        "output_paths": {
            "admin": str(base / "00_admin"),
            "sources": str(base / "01_sources"),
            "outline": str(base / "02_outline" / "outline.md"),
            "citations": str(base / "00_admin" / "citations.json"),
            "final_paper": str(base / "04_final" / "final_paper.md"),
            "exports": str(base / "05_exports"),
            "docx": str(base / "05_exports" / "final_paper.docx"),
            "check_report": str(base / "06_qa" / "check_report.json"),
        },
    }
    (base / "00_admin" / "paper_context.json").write_text(
        json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    return base


def main():
    parser = argparse.ArgumentParser(description="Initialize paper output directory")
    parser.add_argument("name", help="Paper name")
    parser.add_argument("--target-words", type=int, default=1500,
                        help="Target word count")
    parser.add_argument("--lang", default="English",
                        help="Paper language: English / 中文 / 双语")
    parser.add_argument("--author", default="",
                        help="Author info (name, student ID, department)")
    args = parser.parse_args()

    base = init_output_dir(args.name, args.target_words, args.lang, args.author)
    print(f"Initialized: {base}")


if __name__ == "__main__":
    main()
