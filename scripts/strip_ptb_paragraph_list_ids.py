# -*- coding: utf-8 -*-
"""
ลบแอตทริบิวต์ id ออกจากแท็กเปิด <PtbParagraph> และ <PtbList> ใต้ docs/ ยกเว้น .vitepress

นโยบาย: ใช้ id สำหรับลิงก์ fragment เฉพาะหัวข้อ Markdown {#…} เท่านั้น — ไม่กำหนด id บนย่อหน้า/รายการ

รัน:
  python scripts/strip_ptb_paragraph_list_ids.py --write
  python scripts/strip_ptb_paragraph_list_ids.py   # dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

_ID_ATTR = re.compile(r"\s+id\s*=\s*(?:\"[^\"]*\"|'[^']*')")


def iter_markdown_docs() -> list[Path]:
    out: list[Path] = []
    for p in sorted(DOCS.rglob("*.md")):
        if ".vitepress" in p.parts:
            continue
        out.append(p)
    return out


def strip_tag_ids(text: str, tag: str) -> tuple[str, int]:
    n = 0
    pattern = re.compile(rf"<{tag}(\s[^>]*)?>")

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        attrs = m.group(1) or ""
        if not _ID_ATTR.search(attrs):
            return m.group(0)
        n += 1
        new_attrs = _ID_ATTR.sub("", attrs)
        if new_attrs.strip():
            return f"<{tag}{new_attrs}>"
        return f"<{tag}>"

    return pattern.sub(repl, text), n


def process_file(path: Path) -> tuple[str, int, int]:
    raw = path.read_text(encoding="utf-8")
    text, np = strip_tag_ids(raw, "PtbParagraph")
    text, nl = strip_tag_ids(text, "PtbList")
    return text, np, nl


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="เขียนไฟล์")
    args = ap.parse_args()

    files = iter_markdown_docs()
    total_p = total_l = files_touched = 0
    for p in files:
        new_text, np, nl = process_file(p)
        if np or nl:
            total_p += np
            total_l += nl
            rel = p.relative_to(ROOT)
            print(f"{'WROTE' if args.write else 'WOULD UPDATE'} -{np} PtbParagraph id, -{nl} PtbList id: {rel}")
            if args.write:
                p.write_text(new_text, encoding="utf-8")
            files_touched += 1

    msg = (
        f"Done: removed {total_p} PtbParagraph + {total_l} PtbList id(s) in {files_touched} file(s)."
        if args.write
        else f"Dry-run: would remove {total_p} PtbParagraph + {total_l} PtbList id(s) in {files_touched} file(s). Use --write to apply."
    )
    print(msg, file=sys.stderr)


if __name__ == "__main__":
    main()
