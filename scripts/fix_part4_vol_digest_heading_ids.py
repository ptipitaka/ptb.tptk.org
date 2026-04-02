# -*- coding: utf-8 -*-
"""
แก้ `{#id .ptb-h-block}` / `{#id .ptb-h-sr}` ใน vol-01..vol-38 ใต้ docs/09-part-4-tipitaka-digest
ให้ตรงกับกฎ: id = อักษร/ตัวเลข ๑๐ ตัว (เช่น ensure_ptb_heading_ids.py)

- เติม id ถ้ายังไม่มี
- แทนที่ id ที่ไม่ใช่ 10 ตัว หรือมีอักขระนอก [A-Za-z0-9]
- อัปเดต #fragment ที่อ้าง id เก่าในทุกไฟล์ .md ใต้ docs/ (ยกเว้น .vitepress)

ค่าเริ่มต้น dry-run; ใส่ --write เพื่อเขียนไฟล์
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIGEST = ROOT / "docs" / "09-part-4-tipitaka-digest"

HEADING_ATTRS_LINE = re.compile(
    r"^(?P<prefix>#{1,6}\s+.+\S)\s+\{(?P<attrs>[^}]+)\}\s*$"
)
HEADING_ID_ATTR = re.compile(r"#\s*([^\s}]+)")

from ensure_ptb_heading_ids import (  # noqa: E402
    collect_ids_in_text,
    inject_id_into_attrs,
    iter_markdown_under_docs,
    new_ptb_heading_id,
    replace_fragments_global,
    strip_id_tokens_from_attrs,
)

VALID_ID = re.compile(r"^[A-Za-z0-9]{10}$")


def is_ptb_heading_attrs(attrs: str) -> bool:
    return ".ptb-h-block" in attrs or ".ptb-h-sr" in attrs


def vol_digest_files() -> list[Path]:
    out: list[Path] = []
    for n in range(1, 39):
        name = f"vol-{n:02d}.md"
        for p in DIGEST.rglob(name):
            out.append(p)
    return sorted(set(out))


def plan_file(
    text: str,
    reserved: set[str],
    id_map: dict[str, str],
) -> tuple[str, int]:
    """คืน (new_text, จำนวนหัวข้อที่แก้) — อัปเดต id_map สำหรับ oid -> nid"""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    changed = 0

    for line in lines:
        core = line.rstrip("\r\n")
        ending = line[len(core) :]
        m = HEADING_ATTRS_LINE.match(core)
        if not m:
            out.append(line)
            continue
        attrs = m.group("attrs")
        if not is_ptb_heading_attrs(attrs):
            out.append(line)
            continue

        m_id = HEADING_ID_ATTR.search(attrs)
        oid = m_id.group(1) if m_id else None
        need_new = oid is None or not VALID_ID.match(oid)

        if not need_new:
            out.append(line)
            continue

        if oid is not None and oid in id_map:
            nid = id_map[oid]
        else:
            if oid is not None:
                reserved.discard(oid)
            nid = new_ptb_heading_id(reserved)
            if oid is not None:
                id_map[oid] = nid

        stripped = strip_id_tokens_from_attrs(attrs)
        new_attrs = inject_id_into_attrs(stripped, nid)
        new_line = f"{m.group('prefix')} {{{new_attrs}}}{ending}"
        out.append(new_line)
        changed += 1

    return "".join(out), changed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="เขียนไฟล์")
    args = ap.parse_args()

    targets = vol_digest_files()
    if not targets:
        print("ไม่พบไฟล์ vol-01..vol-38", file=sys.stderr)
        sys.exit(1)

    docs_root = ROOT / "docs"
    all_md = iter_markdown_under_docs(docs_root)
    reserved: set[str] = set()
    for p in all_md:
        reserved |= collect_ids_in_text(p.read_text(encoding="utf-8"))

    per_file: dict[Path, tuple[str, int]] = {}
    global_map: dict[str, str] = {}

    for p in targets:
        raw = p.read_text(encoding="utf-8")
        new_text, nchg = plan_file(raw, reserved, global_map)
        per_file[p] = (new_text, nchg)

    total_headings = sum(t[1] for t in per_file.values())
    files_with_changes = sum(1 for t in per_file.values() if t[1] > 0)

    if not args.write:
        print(
            f"Dry-run: จะแก้ {total_headings} หัวข้อ ใน {files_with_changes} ไฟล์ "
            f"(vol-01..vol-38 ใต้ 09-part-4-tipitaka-digest)",
            file=sys.stderr,
        )
        for p, (_, n) in sorted(per_file.items()):
            if n:
                print(f"  {n:3d}  {p.relative_to(ROOT)}", file=sys.stderr)
        print("ใส่ --write เพื่อใช้งาน", file=sys.stderr)
        return

    # เขียนไฟล์เป้าหมายก่อน แล้วค่อยแทนที่ fragment ทั้ง docs
    for p, (new_text, n) in per_file.items():
        if n:
            p.write_text(new_text, encoding="utf-8")

    if global_map:
        updated = 0
        for p in all_md:
            raw = p.read_text(encoding="utf-8")
            new_raw = replace_fragments_global(raw, global_map)
            if new_raw != raw:
                p.write_text(new_raw, encoding="utf-8")
                updated += 1

    print(
        f"Done: แก้ {total_headings} หัวข้อ ใน {files_with_changes} ไฟล์ vol; "
        f"อัปเดตลิงก์ fragment ใน {updated} ไฟล์ .md ทั้ง docs",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
