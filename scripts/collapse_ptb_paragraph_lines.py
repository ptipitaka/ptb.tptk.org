#!/usr/bin/env python3
"""
Collapse multiline <PtbParagraph>...</PtbParagraph> blocks to a single line per block.

Whitespace at line breaks is normalized to a single space (per PTB content guide).
Default: dry-run. Use --write to modify files.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PTB_PARA = re.compile(r"<PtbParagraph\b[^>]*>.*?</PtbParagraph>", re.DOTALL)


def collapse_body(body: str) -> str:
    # Join soft-wrapped lines: newline + surrounding whitespace -> one space
    s = re.sub(r"\s*\r?\n\s*", " ", body)
    # Trim runs of spaces introduced at former line joins (keep single spaces)
    s = re.sub(r" {2,}", " ", s)
    return s


def collapse_one_block(full: str) -> str:
    if "\n" not in full and "\r" not in full:
        return full
    m = re.match(r"^(<PtbParagraph\b[^>]*>)(.*?)(</PtbParagraph>)$", full, re.DOTALL)
    if not m:
        return full
    open_tag, body, close_tag = m.groups()
    return open_tag + collapse_body(body) + close_tag


def process_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        orig = m.group(0)
        new = collapse_one_block(orig)
        if new != orig:
            count += 1
        return new

    return PTB_PARA.sub(repl, text), count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "paths",
        nargs="*",
        default=["docs"],
        help="Files or directories (default: docs)",
    )
    ap.add_argument(
        "--write",
        action="store_true",
        help="Write changes (default dry-run)",
    )
    args = ap.parse_args()
    roots = [Path(p) for p in args.paths]
    md_files: list[Path] = []
    for r in roots:
        if r.is_file() and r.suffix == ".md":
            md_files.append(r)
        elif r.is_dir():
            for p in r.rglob("*.md"):
                if ".vitepress" in p.parts:
                    continue
                md_files.append(p)
    total_blocks = 0
    changed_files = 0
    for path in sorted(set(md_files)):
        raw = path.read_text(encoding="utf-8")
        new, n = process_text(raw)
        total_blocks += n
        if new != raw:
            changed_files += 1
            if args.write:
                path.write_text(new, encoding="utf-8", newline="\n")
            print(f"{path}: collapsed {n} block(s)")
    if not args.write:
        print(f"Dry-run: would change {changed_files} file(s), {total_blocks} block(s). Use --write to apply.")
    else:
        print(f"Done: {changed_files} file(s), {total_blocks} block(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
