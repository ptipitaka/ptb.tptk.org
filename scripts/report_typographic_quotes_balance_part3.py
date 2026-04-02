"""
Scan docs/08-part-3-tipitaka-selected-passages/**/*.md **per ### section**:
- After stripping <PtbFootnote> and fenced code, count “ and ” — must match within that section.
- Flag lines with stray ASCII " in prose (excluding common HTML attr patterns).

Writes a minimal report: one list sorted by เลขข้อ (Thai numeral in heading).

Writes: docs/08-part-3-tipitaka-selected-passages/typographic-quotes-balance-report.md
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

OPEN = "\u201c"
CLOSE = "\u201d"
ASCII_DQ = '"'

ROOT = Path(__file__).resolve().parents[1]
PART3 = ROOT / "docs" / "08-part-3-tipitaka-selected-passages"
OUT = PART3 / "typographic-quotes-balance-report.md"

_THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


def strip_frontmatter(raw: str) -> str:
    if not raw.startswith("---"):
        return raw
    m = re.match(r"^---\n.*?\n---\n", raw, flags=re.DOTALL)
    return raw[m.end() :] if m else raw


def strip_ptb_footnotes(body: str) -> str:
    return re.sub(
        r"<PtbFootnote>.*?</PtbFootnote>",
        "",
        body,
        flags=re.DOTALL,
    )


def strip_fenced_code(body: str) -> str:
    out: list[str] = []
    i = 0
    n = len(body)
    fence = False
    while i < n:
        line_end = body.find("\n", i)
        segment = body[i:] if line_end == -1 else body[i : line_end + 1]
        line = segment.rstrip("\n")
        if line.startswith("```"):
            fence = not fence
        if not fence:
            out.append(segment)
        i = len(body) if line_end == -1 else line_end + 1
    return "".join(out)


def parse_heading(line: str) -> tuple[str, str] | None:
    m = re.match(r"^(#{2,4})\s+(.+)$", line)
    if not m:
        return None
    rest = m.group(2)
    br = re.search(r"\{#([^}]+)\}", rest)
    if br:
        anchor = br.group(1).strip().split()[0] if br.group(1).strip() else ""
        title = rest[: br.start()].strip()
        return (title, anchor)
    return (rest.strip(), "")


def parse_thai_leading_number(title: str) -> int | None:
    t = title.strip()
    m = re.match(r"^([๐-๙]+)\s*\.?", t)
    if not m:
        return None
    return int(m.group(1).translate(_THAI_DIGITS))


def section_has_ascii_dq_in_prose(seg_body_lines: list[str]) -> bool:
    for line in seg_body_lines:
        stripped = re.sub(r'[\w\-:.@]+\s*=\s*"[^"]*"', "", line)
        if ASCII_DQ in stripped:
            return True
    return False


@dataclass(frozen=True, order=True)
class SectionHit:
    sort_num: int
    title: str
    anchor: str
    file_rel: str


def split_markdown_sections(body: str) -> list[str]:
    lines = body.splitlines()
    segs: list[str] = []
    cur: list[str] = []
    for line in lines:
        if line.startswith("### ") and cur:
            segs.append("\n".join(cur))
            cur = [line]
        else:
            cur.append(line)
    if cur:
        segs.append("\n".join(cur))
    return segs


def analyze_file(path: Path) -> list[SectionHit]:
    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    body = strip_fenced_code(body)
    file_rel = str(path.relative_to(PART3)).replace("\\", "/")

    hits: list[SectionHit] = []
    for seg in split_markdown_sections(body):
        if not seg.strip():
            continue
        seg_lines = seg.splitlines()
        first = seg_lines[0]
        if not first.startswith("###"):
            continue
        ph = parse_heading(first)
        if not ph:
            continue
        title, anchor = ph
        rest_lines = seg_lines[1:]
        nf = strip_ptb_footnotes(seg)
        o = nf.count(OPEN)
        c = nf.count(CLOSE)
        bad_bal = o != c
        bad_ascii = section_has_ascii_dq_in_prose(rest_lines)
        if not bad_bal and not bad_ascii:
            continue
        sn = parse_thai_leading_number(title)
        sort_num = sn if sn is not None else 10**9
        hits.append(SectionHit(sort_num, title, anchor, file_rel))
    return hits


def main() -> int:
    files = sorted(PART3.rglob("*.md"))
    files = [p for p in files if p.name != "typographic-quotes-balance-report.md"]

    all_h: list[SectionHit] = []
    for p in files:
        all_h.extend(analyze_file(p))

    merged = sorted(all_h, key=lambda h: (h.sort_num, h.title, h.file_rel))

    lines_out: list[str] = [
        "---",
        "title: รายงานเครื่องหมายคำพูด — เลขข้อที่ควรตรวจ (ภาค ๓)",
        "outline: false",
        "---",
        "",
        "สร้างอัตโนมัติจาก `scripts/report_typographic_quotes_balance_part3.py`",
        "",
        "รายการ **เลขข้อ** (หัวข้อ `### … {#…}`) ที่ในบทนั้นมีเครื่องหมายคำพูดไม่สมดุล (`“` / `”` หลังตัด `<PtbFootnote>`) **หรือ** พบ `\"` แบบ ASCII ในเนื้อหา — รวมหนึ่งรายการ เรียงตามเลขข้อ",
        "",
    ]

    if not merged:
        lines_out.append("*ไม่พบข้อที่ตรงเกณฑ์ข้างต้นในขณะสแกนล่าสุด*")
    else:
        for h in merged:
            lines_out.append(
                f"- **{h.title}** (`#{h.anchor}`) — `{h.file_rel}`"
            )

    OUT.write_text("\n".join(lines_out), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(merged)} section(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
