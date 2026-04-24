#!/usr/bin/env python3
"""Remove 🚩 from bullets where every PtbWordIndexLink in that bullet is tier=\"secondary\"."""
from __future__ import annotations

import re
from pathlib import Path

PATH = Path("docs/10-part-5-word-index/persons/thera/index.md")

LINK_RE = re.compile(r"<PtbWordIndexLink\b[^>]*/>")


def main() -> None:
    lines = PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    i = 0
    stripped = 0
    while i < len(lines):
        line = lines[i]
        if not (line.startswith("* **") and "🚩" in line):
            i += 1
            continue
        j = i + 1
        while j < len(lines):
            l2 = lines[j]
            if l2.startswith("* **"):
                break
            if l2.strip() == "</PtbWordIndexEntry>":
                break
            j += 1
        segment = "".join(lines[i:j])
        links = LINK_RE.findall(segment)
        if not links:
            i = j
            continue
        tiers: list[str] = []
        ok = True
        for L in links:
            m = re.search(r'tier="(primary|secondary)"', L)
            if not m:
                ok = False
                break
            tiers.append(m.group(1))
        if ok and tiers and all(t == "secondary" for t in tiers):
            lines[i] = lines[i].replace("🚩", "")
            stripped += 1
        i = j

    PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Removed flag from {stripped} bullet(s) (secondary-only)")


if __name__ == "__main__":
    main()
