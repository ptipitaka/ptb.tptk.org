"""One-off: extract PtbWordIndexLink lists from bhikkhu index (dry run)."""
import re
from pathlib import Path

text = Path("docs/10-part-5-word-index/persons/bhikkhu/index.md").read_text(encoding="utf-8")
pattern = re.compile(
    r'<PtbWordIndexEntry term="([^"]+)"[^>]*>(.*?)</PtbWordIndexEntry>',
    re.DOTALL,
)
link_re = re.compile(
    r'<PtbWordIndexLink\s+href="([^"]+)"\s+label="([^"]+)"(?:\s+tier="(primary|secondary)")?\s*/>'
)
out = []
for m in pattern.finditer(text):
    term = m.group(1)
    block = m.group(2)
    links = link_re.findall(block)
    if links:
        out.append((term, links))
Path("scripts/_bhikkhu_links_extract.json").write_text(
    __import__("json").dumps(
        {t: [{"href": a, "label": b, "tier": c or None} for a, b, c in ls] for t, ls in out},
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)
print("wrote", len(out), "entries")
