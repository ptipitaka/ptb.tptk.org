# -*- coding: utf-8 -*-
"""
รวมลำดับบล็อก <PtbParagraph> / <p class="ptb-paragraph-no-indent"> ที่ขึ้นต้นด้วย
เลขไทย + จุด + ช่องว่าง (หรือจุดชิดข้อความ เช่น ๑๐.ค) และเลขต่อเนื่องกัน
ให้เป็น <PtbList auto> + <PtbListItem> (ตัดเลขนำออก) ตาม ptb-content-guide

รันมือ:
  python scripts/ptb_coalesce_thai_numbered_lists.py --write \\
    docs/09-part-4-tipitaka-digest/vinaya-pitaka/vol-08.md \\
    docs/09-part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-09.md \\
    docs/09-part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-10.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

THAI_DIGITS = "๐๑๒๓๔๕๖๗๘๙"

# เลขไทยที่จุด แล้วตามด้วยช่องว่างหรือตัวอักษรไทยทันที (กรณี ๑๐.คาถา)
_RE_LEADING_THAI_NUM = re.compile(
    r"^([๐-๙]+)\.(?:\s+|(?=[\u0e00-\u0e7f]))",
)

_RE_PTB_PARA = re.compile(
    r"^<PtbParagraph(\s[^>]*)?>([\s\S]*?)</PtbParagraph>\s*$",
)
_RE_P_NO_INDENT = re.compile(
    r'^<p class="ptb-paragraph-no-indent"(\s[^>]*)?>([\s\S]*?)</p>\s*$',
)


def thai_to_int(s: str) -> int:
    return int("".join(str(THAI_DIGITS.index(c)) for c in s))


def try_parse_numbered_block(block: str) -> tuple[int, str] | None:
    """คืน (เลขลำดับ, เนื้อหาภายในหลังตัดเลขนำ) หรือ None"""
    block = block.strip()
    m = _RE_PTB_PARA.match(block) or _RE_P_NO_INDENT.match(block)
    if not m:
        return None
    inner = m.group(2).strip()
    lm = _RE_LEADING_THAI_NUM.match(inner)
    if not lm:
        return None
    n = thai_to_int(lm.group(1))
    rest = inner[lm.end() :].lstrip()
    return (n, rest)


def coalesce_thai_numbered_lists(text: str, min_run: int = 2) -> str:
    parts = re.split(r"\n{2,}", text)
    out: list[str] = []
    i = 0
    while i < len(parts):
        part = parts[i]
        parsed = try_parse_numbered_block(part)
        if parsed is None:
            out.append(part)
            i += 1
            continue
        n0, _ = parsed
        j = i
        expected = n0
        collected: list[str] = []
        while j < len(parts):
            pj = try_parse_numbered_block(parts[j])
            if pj is None or pj[0] != expected:
                break
            collected.append(pj[1])
            expected += 1
            j += 1
        run_len = j - i
        if run_len >= min_run:
            start_attr = "" if n0 == 1 else f' :start="{n0}"'
            lines = [f"<PtbList auto{start_attr}>", ""]
            for body in collected:
                lines.append(f"<PtbListItem>{body}</PtbListItem>")
                lines.append("")
            lines.append("</PtbList>")
            out.append("\n".join(lines).rstrip())
            i = j
        else:
            out.append(part)
            i += 1
    return "\n\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", type=Path, help="ไฟล์ .md")
    ap.add_argument("--write", action="store_true")
    ap.add_argument(
        "--min-run",
        type=int,
        default=2,
        help="อย่างน้อยกี่บล็อกติดกันจึงรวมเป็น PtbList (ค่าเริ่ม ๒)",
    )
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    any_change = False
    for rel in args.paths:
        path = rel if rel.is_absolute() else root / rel
        raw = path.read_text(encoding="utf-8")
        new = coalesce_thai_numbered_lists(raw, min_run=args.min_run)
        if new != raw:
            any_change = True
            print(f"{'WROTE' if args.write else 'WOULD UPDATE'}: {path.relative_to(root)}")
            if args.write:
                path.write_text(new, encoding="utf-8")
    if not any_change:
        print("No changes.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
