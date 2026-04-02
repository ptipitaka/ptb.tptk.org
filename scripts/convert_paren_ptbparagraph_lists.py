"""
Convert runs of <PtbParagraph>(๑)…(๒)… in sequence to <PtbList> + <PtbListItem marker="(๑)">…
Skips blank lines between items. Requires list to start at (๑) and have at least 2 items.
"""
from __future__ import annotations

import pathlib
import re
import sys

THAI_DIGITS = {"๐": 0, "๑": 1, "๒": 2, "๓": 3, "๔": 4, "๕": 5, "๖": 6, "๗": 7, "๘": 8, "๙": 9}


def thai_to_int(s: str) -> int:
    n = 0
    for c in s:
        n = n * 10 + THAI_DIGITS[c]
    return n


# Full line: optional (๑) marker at start of inner content, rest until closing tag
ITEM_RE = re.compile(
    r"^<PtbParagraph>\(([๑๒๓๔๕๖๗๘๙๐]+)\)\s*(.*)</PtbParagraph>\s*$"
)


def parse_item(line: str):
    m = ITEM_RE.match(line.rstrip("\r\n"))
    if not m:
        return None
    mark = m.group(1)
    return thai_to_int(mark), mark, m.group(2)


def convert_file(path: pathlib.Path) -> str:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        parsed = parse_item(line) if line.strip() else None
        if parsed and parsed[0] == 1:
            items: list[tuple[str, str]] = [(parsed[1], parsed[2])]
            j = i + 1
            expected = 2
            while j < len(lines):
                lj = lines[j]
                if not lj.strip():
                    j += 1
                    continue
                p = parse_item(lj)
                if p and p[0] == expected:
                    items.append((p[1], p[2]))
                    expected += 1
                    j += 1
                else:
                    break
            if len(items) >= 2:
                out.append("<PtbList>\n\n")
                for mark, content in items:
                    out.append(f'<PtbListItem marker="({mark})">{content}</PtbListItem>\n\n')
                out.append("</PtbList>\n\n")
                if j < len(lines) and lines[j].strip() == "":
                    j += 1  # skip one blank; we already emitted \n\n after </PtbList>
                i = j
                continue
        out.append(line)
        i += 1
    return "".join(out)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: convert_paren_ptbparagraph_lists.py <file.md> [--write]", file=sys.stderr)
        sys.exit(1)
    path = pathlib.Path(sys.argv[1])
    text = convert_file(path)
    if "--write" in sys.argv:
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path}")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
