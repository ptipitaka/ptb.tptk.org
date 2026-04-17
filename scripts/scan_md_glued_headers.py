#!/usr/bin/env python3
"""Find markdown lines where ATX # heading is not at line start (glued to prior text on same line)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Strip markdown-it attrs {#id .class} for analysis
ATTR = re.compile(r"\s*\{#[^}\s]+\s*[^}]*\}")


def strip_attrs(s: str) -> str:
    return ATTR.sub("", s)


def line_has_glued_heading(line: str) -> bool:
    raw = line.rstrip("\r\n")
    if not raw.strip():
        return False
    if raw.strip() == "---":
        return False

    deattr = strip_attrs(raw)
    if not deattr.strip():
        return False

    # Valid ATX heading line: 0-3 spaces then #… then space or end
    if re.match(r"^\s{0,3}#{1,6}(\s+|$)", deattr):
        return False

    # Markdown link targets [](url#frag) — ignore # in URL
    deattr = re.sub(r"\]\([^)]*#([^)]*)\)", "]( )", deattr)

    # Remaining: if still #{1,6}\s+ appears, heading syntax is glued to prior text
    if re.search(r"#{1,6}\s+\S", deattr):
        return True

    return False


def main() -> None:
    root = Path(__file__).resolve().parent.parent / "docs"
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])

    hits: list[tuple[str, int, str]] = []
    for path in sorted(root.rglob("*.md")):
        if ".vitepress" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            if i == 1:
                continue
            if line_has_glued_heading(line):
                hits.append((str(path.relative_to(root)), i, line[:200]))

    print(f"Total: {len(hits)}")
    for p, ln, preview in hits:
        print(f"{p}:{ln}:{preview}")


if __name__ == "__main__":
    main()
