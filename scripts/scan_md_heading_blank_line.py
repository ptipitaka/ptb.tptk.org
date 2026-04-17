#!/usr/bin/env python3
"""Report markdown headings not preceded by a blank line (docs/ only)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEADING = re.compile(r"^\s{0,3}#{1,6}\s")


def main() -> None:
    root = Path(__file__).resolve().parent.parent / "docs"
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])

    no_blank: list[tuple[Path, int, str, str]] = []
    for path in sorted(root.rglob("*.md")):
        if ".vitepress" in path.parts:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if i == 0:
                continue
            if not HEADING.match(line):
                continue
            prev = lines[i - 1]
            if not prev.strip():
                continue
            if prev.strip() == "---":
                continue
            no_blank.append((path, i + 1, prev.strip(), line.strip()))

    lines_out = [f"Total: {len(no_blank)}"]
    for path, ln, prev, cur in no_blank:
        rel = path.relative_to(root.parent)
        lines_out.append("")
        lines_out.append(f"{rel}:{ln}")
        lines_out.append(f"  prev: {prev}")
        lines_out.append(f"  cur:  {cur}")
    text = "\n".join(lines_out) + "\n"
    print(text, end="")
    if "--write-report" in sys.argv:
        report_path = Path(__file__).resolve().parent / "heading_survey_output.txt"
        report_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
