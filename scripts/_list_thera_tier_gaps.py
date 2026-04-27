#!/usr/bin/env python3
import re
from pathlib import Path

p = Path("docs/10-part-5-word-index/persons/bhikkhu/index.md")
t = p.read_text(encoding="utf-8")
LINK_RE = re.compile(
    r'<PtbWordIndexLink\s+href="([^"]+)"\s+label="([^"]*)"(?:\s+tier="(primary|secondary)")?\s*/>'
)
n = 0
for m in LINK_RE.finditer(t):
    if m.group(3):
        continue
    n += 1
    href = m.group(1)
    frag = href.split("#", 1)[1] if "#" in href else ""
    print(frag, "\t", href[:90])
print("TOTAL_MISSING", n)
