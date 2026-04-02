"""One-off checks for MDX/HTML in Tipitaka passage markdown (tag balance, footnote line)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VOID = {"hr", "br", "img", "meta", "link", "input"}
TAG_PATTERN = re.compile(r"<(/?)([\w-]+)([^>]*)>", re.I)
FOOTNOTE_PATTERN = re.compile(r"<PtbFootnote>(.*)</PtbFootnote>")


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        try:
            end = text.index("---", 3) + 3
            return text[end:]
        except ValueError:
            pass
    return text


def check_stack(path: Path) -> int:
    text = _strip_frontmatter(path.read_text(encoding="utf-8"))
    stack: list[str] = []
    for m in TAG_PATTERN.finditer(text):
        closing, name, rest = m.group(1), m.group(2), m.group(3)
        name_l = name.lower()
        if closing:
            if not stack or stack[-1] != name:
                print(
                    "BAD close",
                    name,
                    "expected",
                    stack[-1] if stack else None,
                    "at pos",
                    m.start(),
                )
                return 1
            stack.pop()
        else:
            if name_l in VOID or rest.rstrip().endswith("/"):
                continue
            stack.append(name)

    print("unclosed:", stack)
    return 1 if stack else 0


def check_footnote_line(path: Path, line_1based: int) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    if line_1based < 1 or line_1based > len(lines):
        print(f"error: line {line_1based} out of range (1–{len(lines)})", file=sys.stderr)
        return 2
    s = lines[line_1based - 1]
    m = FOOTNOTE_PATTERN.search(s)
    if not m:
        print("no match")
        return 1
    fn = m.group(1)
    print("footnote len", len(fn))
    for i, ch in enumerate(fn):
        if ch in "<>":
            print("angle at", i, repr(ch))
    print("double quote count", fn.count('"'))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnostics for HTML/MDX in markdown files.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_stack = sub.add_parser("stack", help="Check simple HTML tag open/close balance")
    p_stack.add_argument("path", type=Path, help="Markdown file to scan")

    p_fn = sub.add_parser("footnote", help="Inspect <PtbFootnote> on one line")
    p_fn.add_argument("path", type=Path, help="Markdown file")
    p_fn.add_argument(
        "--line",
        type=int,
        required=True,
        metavar="N",
        help="1-based line number",
    )

    args = parser.parse_args()
    if args.cmd == "stack":
        return check_stack(args.path)
    if args.cmd == "footnote":
        return check_footnote_line(args.path, args.line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
