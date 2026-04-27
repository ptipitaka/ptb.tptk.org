# -*- coding: utf-8 -*-
"""One-off: extract PtbWordIndexLink lists from legacy rulers/index.md into JSON."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/10-part-5-word-index/persons/rulers/index.md"
OUT = ROOT / "scripts/_rulers_legacy_links.json"

def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    parts = re.split(r"(?=<PtbWordIndexEntry)", text)
    out: dict[str, list[dict]] = {}
    for block in parts:
        m = re.search(r'term="([^"]+)"', block)
        if not m:
            continue
        term = m.group(1)
        links: list[dict] = []
        for hm, labm in re.findall(
            r'<PtbWordIndexLink href="([^"]+)" label="([^"]+)"', block
        ):
            links.append({"href": hm, "label": labm, "tier": "primary"})
        if links:
            out[term] = links
    OUT.write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    print("Wrote", OUT, "keys", len(out))


if __name__ == "__main__":
    main()
