import re
from pathlib import Path

t = Path("docs/10-part-5-word-index/persons/bhikkhu/index.md").read_text(
    encoding="utf-8"
)
allm = list(
    re.finditer(
        r'<PtbWordIndexLink\s+href="([^"]+)"\s+label="([^"]*)"(?:\s+tier="(primary|secondary)")?\s*/>',
        t,
    )
)
print("matches", len(allm))
print("with tier", sum(1 for m in allm if m.group(3)))
print("without", sum(1 for m in allm if not m.group(3)))
