"""
Convert consecutive <PtbParagraph>(๑) ... </PtbParagraph> blocks to <PtbList> + marker items.
For vol-24.md style: Thai digits in parentheses only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Matches (๑) through (๑๒) at start of PtbParagraph body (after >)
MARKER_HEAD = re.compile(
    r"^(\s*)<PtbParagraph>\((๑๐|๑๑|๑๒|๙|๘|๗|๖|๕|๔|๓|๒|๑)\)"
)
# Optional extension: " - (๙) " after (๘)
# ASCII hyphen or common unicode dashes (source text may use either)
EXT_RANGE = re.compile(
    r"^\s*[-–−]\s*\((๑๐|๑๑|๑๒|๙|๘|๗|๖|๕|๔|๓|๒|๑)\)\s*"
)


def split_marker_body(line: str) -> tuple[str | None, str | None, str]:
    """
    Returns (indent, full_marker_string, body_after_marker) or (None, None, line) if no match.
    line is full line including newline if present.
    """
    m = MARKER_HEAD.match(line)
    if not m:
        return None, None, line
    indent = m.group(1)
    first = m.group(2)
    rest = line[m.end() :]
    # Strip closing tag from rest
    if not rest.endswith("</PtbParagraph>\n") and not rest.endswith("</PtbParagraph>"):
        return None, None, line
    if rest.endswith("</PtbParagraph>\n"):
        inner = rest[: -len("</PtbParagraph>\n")]
        nl = "\n"
    else:
        inner = rest[: -len("</PtbParagraph>")]
        nl = ""
    # (๘) - (๙) case
    marker = f"({first})"
    ext = EXT_RANGE.match(inner)
    if ext:
        second = ext.group(1)
        marker = f"({first}) - ({second})"
        inner = inner[ext.end() :].lstrip()
    return indent, marker, inner + nl


def flush_list(buf: list[tuple[str, str]], out: list[str]) -> None:
    if not buf:
        return
    out.append("")
    out.append("<PtbList>")
    out.append("")
    for marker, body in buf:
        # body may include trailing \n from original
        body = body.rstrip("\n")
        out.append(f'<PtbListItem marker="{marker}">{body}</PtbListItem>')
        out.append("")
    out.append("</PtbList>")
    out.append("")
    buf.clear()


def convert(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    buf: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Blank lines between list items must not flush the list
        if buf and line.strip() == "":
            i += 1
            continue
        indent, marker, body = split_marker_body(line)
        if marker is not None and body is not None:
            buf.append((marker, body.rstrip("\n")))
            i += 1
            continue
        # Not a marker line — flush list if any
        if buf:
            flush_list(buf, out)
        out.append(line)
        i += 1
    if buf:
        flush_list(buf, out)
    return "".join(out)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not path or not path.is_file():
        print("Usage: convert_paren_paragraphs_to_ptblist.py <file.md>", file=sys.stderr)
        sys.exit(1)
    text = path.read_text(encoding="utf-8")
    new_text = convert(text)
    path.write_text(new_text, encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
