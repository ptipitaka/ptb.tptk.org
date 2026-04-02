"""
Convert ASCII paired "..." to “...” in docs/**/*.md body only.

Skips:
- YAML frontmatter (first --- ... ---)
- Fenced code blocks (```)
- HTML comments <!-- -->
- <style>...</style>
- Inside HTML tags and double-quoted attribute values
- Quoted spans immediately after = (e.g. {style="display:none"})
- Text may cross <PtbFootnote>...</PtbFootnote> inside a quoted span (footnote skipped when pairing)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

O = "\u201c"
C = "\u201d"


def _end_of_ptb_footnote(content: str, j: int) -> int | None:
    """If j starts <PtbFootnote>...</PtbFootnote>, return index after the closing tag; else None."""
    if content.startswith("<PtbFootnote>", j):
        end = content.find("</PtbFootnote>", j)
        if end == -1:
            return None
        return end + len("</PtbFootnote>")
    return None


def transform(content: str) -> tuple[str, int]:
    """Returns (new_content, number_of_pairs_replaced)."""
    n = len(content)
    out: list[str] = []
    i = 0
    replaced = 0

    def append(s: str) -> None:
        out.append(s)

    # --- Frontmatter ---
    if content.startswith("---"):
        m = re.match(r"^---\n.*?\n---\n", content, flags=re.DOTALL)
        if m:
            append(m.group(0))
            i = m.end()

    line_start = i
    fence = False  # ``` markdown fence

    state = "text"  # text | tag | attr_dq | comment | style

    def is_line_start(pos: int) -> bool:
        return pos == 0 or content[pos - 1] == "\n"

    while i < n:
        c = content[i]

        if state == "text":
            if fence:
                # end fence: line starts with ```
                if is_line_start(i) and content.startswith("```", i):
                    fence = False
                    nl = content.find("\n", i)
                    if nl == -1:
                        append(content[i:])
                        break
                    append(content[i : nl + 1])
                    i = nl + 1
                    line_start = i
                    continue
                nl = content.find("\n", i)
                if nl == -1:
                    append(content[i:])
                    break
                append(content[i : nl + 1])
                i = nl + 1
                line_start = i
                continue

            if is_line_start(i) and content.startswith("```", i):
                fence = True
                nl = content.find("\n", i)
                if nl == -1:
                    append(content[i:])
                    break
                append(content[i : nl + 1])
                i = nl + 1
                line_start = i
                continue

            if content.startswith("<!--", i):
                state = "comment"
                append("<!--")
                i += 4
                continue

            if content[i : i + 7].lower() == "<style":
                # enter style block
                state = "style"
                append(c)
                i += 1
                continue

            if c == "<":
                state = "tag"
                append(c)
                i += 1
                continue

            if c == '"':
                # Skip attribute-like "... after =
                j = i - 1
                while j >= line_start and content[j] in " \t":
                    j -= 1
                if j >= line_start and content[j] == "=":
                    # copy quoted attr value verbatim
                    append('"')
                    i += 1
                    while i < n and content[i] != '"':
                        append(content[i])
                        i += 1
                    if i < n:
                        append('"')
                        i += 1
                    continue

                # Pair quotes until next ASCII " — skip <PtbFootnote>...</PtbFootnote> (not other '<')
                j = i + 1
                while j < n:
                    if content[j] == "<":
                        foot_end = _end_of_ptb_footnote(content, j)
                        if foot_end is not None:
                            j = foot_end
                            continue
                        append(content[i])
                        i += 1
                        break
                    if content[j] == '"':
                        inner = content[i + 1 : j]
                        append(O + inner + C)
                        replaced += 1
                        i = j + 1
                        break
                    j += 1
                else:
                    append(content[i])
                    i += 1
                continue

            if c == "\n":
                line_start = i + 1
            append(c)
            i += 1
            continue

        if state == "comment":
            if content.startswith("-->", i):
                append("-->")
                i += 3
                state = "text"
                continue
            append(c)
            i += 1
            continue

        if state == "style":
            low = content[i : i + 8].lower()
            if low == "</style>":
                append(content[i : i + 8])
                i += 8
                state = "text"
                continue
            append(c)
            i += 1
            continue

        if state == "tag":
            if c == '"':
                state = "attr_dq"
                append(c)
                i += 1
                continue
            append(c)
            if c == ">":
                state = "text"
            i += 1
            continue

        if state == "attr_dq":
            append(c)
            if c == '"':
                state = "tag"
            i += 1
            continue

    return "".join(out), replaced


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    report_lines: list[str] = []
    total = 0
    changed_files: list[str] = []

    for path in sorted(docs.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        new, count = transform(raw)
        rel = path.relative_to(root)
        if count:
            report_lines.append(f"- {rel}: แปลง {count} คู่เครื่องหมาย")
            total += count
        if new != raw:
            path.write_text(new, encoding="utf-8")
            changed_files.append(str(rel))

    report_path = root / "scripts" / "typographic-quotes-last-run.md"
    body = [
        "---",
        "title: สแกนเครื่องหมายคำพูด (typographic quotes)",
        "outline: false",
        "---",
        "",
        "ไฟล์นี้สร้างอัตโนมัติจาก `scripts/typographic_quotes_docs.py`",
        "",
        f"**สรุป:** แปลงรวม **{total}** คู่ใน **{len(changed_files)}** ไฟล์",
        "",
    ]
    if report_lines:
        body.append("## รายการแก้")
        body.extend(report_lines)
    else:
        body.append("## ผลสแกน")
        body.append(
            "- ไม่พบคู่ `\"` แบบ ASCII ในเนื้อความที่ต้องแปลง "
            "(ส่วนที่เหลือเป็นแอตทริบิวต์ HTML / `{style=\"...\"}` / frontmatter ฯลฯ)"
        )
    body.append("")
    body.append("ข้อห้าม: ไม่แก้เครื่องหมายภายในค่าแอตทริบิวต์ HTML (`alt=\"\"` `marker=\"\"` ฯลฯ)")
    report_path.write_text("\n".join(body), encoding="utf-8")

    print(f"Pairs replaced: {total}, files changed: {len(changed_files)}")
    for f in changed_files:
        print(f"  {f}")
    print(f"Report: {report_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
