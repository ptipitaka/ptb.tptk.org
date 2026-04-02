"""Merge consecutive <PtbList>...</PtbList> blocks that each contain a single PtbListItem into one list."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Join: </PtbList> + optional whitespace/newlines + <PtbList> + optional whitespace/newlines
# into single list (drop closing/opening between)
# Adjacent lists: </PtbList> then newline then <PtbList> (optional space before items)
PATTERN = re.compile(r"</PtbList>(\s*\n\s*)<PtbList>\s*", re.MULTILINE)


def merge(text: str) -> str:
    prev = None
    while prev != text:
        prev = text
        text = PATTERN.sub(r"\1", text)
    return text


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not path or not path.is_file():
        print("Usage: merge_adjacent_ptblists.py <file.md>", file=sys.stderr)
        sys.exit(1)
    text = path.read_text(encoding="utf-8")
    new_text = merge(text)
    path.write_text(new_text, encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
