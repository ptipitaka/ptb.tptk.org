#!/usr/bin/env python3
"""Add tier=\"primary\" to PtbWordIndexLink in thera/index.md when tier is absent."""
from __future__ import annotations

import re
from pathlib import Path

PATH = Path("docs/10-part-5-word-index/persons/thera/index.md")

LINK_RE = re.compile(
    r'(<PtbWordIndexLink\s+href="[^"]+"\s+label="[^"]*")(\s+tier="(?:primary|secondary)")?(\s*/>)'
)


added = 0


def repl(m: re.Match[str]) -> str:
    global added
    if m.group(2):
        return m.group(0)
    added += 1
    return m.group(1) + ' tier="primary"' + m.group(3)


def main() -> None:
    global added
    added = 0
    text = PATH.read_text(encoding="utf-8")
    new_text = LINK_RE.sub(repl, text)
    if added == 0:
        raise SystemExit("No links needed tier")
    PATH.write_text(new_text, encoding="utf-8")
    print(f"Added tier=primary to {added} link(s)")


if __name__ == "__main__":
    main()
