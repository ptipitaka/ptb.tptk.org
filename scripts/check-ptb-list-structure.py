from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"


def scan_file(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    list_depth = 0

    for line_number, line in enumerate(lines, start=1):
        open_count = len(re.findall(r"<PtbList\b", line))
        close_count = line.count("</PtbList>")

        if "<PtbListItem" in line and list_depth <= 0:
            errors.append(f"{path}:{line_number} PtbListItem must be wrapped by PtbList")

        list_depth += open_count
        list_depth -= close_count

        if list_depth < 0:
            errors.append(f"{path}:{line_number} unexpected </PtbList> without matching <PtbList>")
            list_depth = 0

    if list_depth != 0:
        errors.append(f"{path}:EOF unbalanced <PtbList> ... </PtbList> tags")

    return errors


def main() -> int:
    markdown_files = sorted(DOCS_DIR.rglob("*.md"))
    all_errors: list[str] = []

    for md_file in markdown_files:
        all_errors.extend(scan_file(md_file))

    if all_errors:
        print("Ptb list structure check failed:")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print("Ptb list structure check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
