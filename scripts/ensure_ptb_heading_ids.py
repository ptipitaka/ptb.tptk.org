# -*- coding: utf-8 -*-
"""
จัดการ `{#id .ptb-h-block}` และ `{#id .ptb-h-sr}` สำหรับหัวข้อ Markdown ใต้ docs/

**โหมดปกติ (ไม่ใส่ --migrate)**  
เติม `{#…}` (อักษร/ตัวเลข 10 ตัว) เฉพาะบรรทัดที่มี `.ptb-h-block` หรือ `.ptb-h-sr` แต่ยังไม่มี id — **ไม่ทับ** id เดิม

**โหมด initial / --migrate**  
สำหรับทุกหัวข้อที่มี `.ptb-h-block` หรือ `.ptb-h-sr` (และระดับ ≥ --min-level): **ลบ id เดิมแล้วใส่รหัสสุ่มใหม่**  
จากนั้นแทนที่ `#idเก่า` เป็น `#idใหม่` ทั้งไฟล์ .md ใน docs/ (ลิงก์เช่น href="...#p3-1")

- รหัสใหม่: อักษร/ตัวเลข 10 ตัว (`secrets`) ไม่มี prefix
- `--min-level` ค่าเริ่ม 1 (= รวม h1); ใส่ 2 เพื่อข้ามบรรทัดที่ขึ้นต้นด้วย `# ` อย่างเดียว (เหลือ ##–######)
- dry-run เป็นค่าเริ่มต้น; ใส่ `--write` เมื่อต้องการเขียนไฟล์

รัน:
  python scripts/ensure_ptb_heading_ids.py docs -r --write --migrate
  python scripts/ensure_ptb_heading_ids.py docs/foo.md --write
"""
from __future__ import annotations

import argparse
import re
import secrets
import string
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEADING_ATTRS_LINE = re.compile(
    r"^(?P<prefix>#{1,6}\s+.+\S)\s+\{(?P<attrs>[^}]+)\}\s*$"
)
# id ใน `{#… }` จนถึงช่องว่างหรือ } (รองรับ slug ที่มีอักษรไทยตามของเดิมใน repo)
HEADING_ID_ATTR = re.compile(r"#\s*([^\s}]+)")
_ANY_BRACE_ID = re.compile(r"\{#([^\s}]+)")
_STRIP_FIRST_ID = re.compile(r"#\s*[^\s}]+\s*")

_ALPHABET = string.ascii_letters + string.digits


def iter_markdown_under_docs(docs_root: Path) -> list[Path]:
    """ทุกไฟล์ .md ใต้ docs_root ยกเว้นโฟลเดอร์ .vitepress"""
    if not docs_root.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(docs_root.rglob("*.md")):
        if ".vitepress" in p.parts:
            continue
        out.append(p)
    return out


def collect_ids_in_text(text: str) -> set[str]:
    return set(_ANY_BRACE_ID.findall(text))


def new_ptb_heading_id(reserved: set[str]) -> str:
    while True:
        tail = "".join(secrets.choice(_ALPHABET) for _ in range(10))
        nid = tail
        if nid not in reserved:
            reserved.add(nid)
            return nid


def heading_level(prefix: str) -> int:
    m = re.match(r"^(#+)\s", prefix)
    return len(m.group(1)) if m else 0


def is_ptb_heading_attrs(attrs: str) -> bool:
    return ".ptb-h-block" in attrs or ".ptb-h-sr" in attrs


def attrs_need_id(attrs: str) -> bool:
    if not is_ptb_heading_attrs(attrs):
        return False
    return HEADING_ID_ATTR.search(attrs) is None


def strip_id_tokens_from_attrs(attrs: str) -> str:
    s = attrs.strip()
    while HEADING_ID_ATTR.search(s):
        s = _STRIP_FIRST_ID.sub("", s, count=1)
    return " ".join(s.split())


def inject_id_into_attrs(attrs: str, new_id: str) -> str:
    stripped = strip_id_tokens_from_attrs(attrs).strip()
    return f"#{new_id} {stripped}".strip()


def replace_fragments_global(text: str, old_to_new: dict[str, str]) -> str:
    for old, new in sorted(old_to_new.items(), key=lambda kv: -len(kv[0])):
        text = re.sub(
            r"#" + re.escape(old) + r"(?![\w-])",
            "#" + new,
            text,
        )
    return text


def process_fill_only(
    text: str,
    min_level: int,
    reserved: set[str],
) -> tuple[str, int, dict[str, str]]:
    """เติม id เฉพาะหัวข้อที่ยังไม่มี id; คืน (new_text, num_changes, {})"""
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
        if not attrs_need_id(attrs):
            out.append(line)
            continue
        if heading_level(m.group("prefix")) < min_level:
            out.append(line)
            continue
        nid = new_ptb_heading_id(reserved)
        new_attrs = inject_id_into_attrs(attrs, nid)
        new_line = f"{m.group('prefix')} {{{new_attrs}}}{ending}"
        out.append(new_line)
        changed += 1
    return "".join(out), changed, {}


def plan_migrate_file(
    text: str,
    min_level: int,
    reserved: set[str],
    global_old_to_new: dict[str, str],
) -> tuple[str, int]:
    """
    แทนที่ทุก id ในหัวข้อ .ptb-h-block / .ptb-h-sr; อัปเดต global_old_to_new
    คืน (new_text, num_heading_changes)
    """
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
        if heading_level(m.group("prefix")) < min_level:
            out.append(line)
            continue

        m_old = HEADING_ID_ATTR.search(attrs)
        old_ids: list[str] = [m_old.group(1)] if m_old else []
        for oid in old_ids:
            reserved.discard(oid)

        new_id = new_ptb_heading_id(reserved)

        for oid in old_ids:
            if oid in global_old_to_new and global_old_to_new[oid] != new_id:
                raise ValueError(
                    f"id ซ้ำใน repo: {oid!r} ถูก map เป็น {global_old_to_new[oid]!r} แล้ว "
                    f"แต่เจออีกครั้งที่จะได้ {new_id!r}"
                )
            global_old_to_new[oid] = new_id

        new_attrs = inject_id_into_attrs(attrs, new_id)
        new_line = f"{m.group('prefix')} {{{new_attrs}}}{ending}"
        if new_line != line:
            changed += 1
        out.append(new_line)

    return "".join(out), changed


def run_migrate(
    docs_root: Path,
    write: bool,
    min_level: int,
) -> tuple[int, int, dict[str, str]]:
    """
    migrate ทุกไฟล์ .md ใต้ docs_root; คืน (files_touched, headings_changed, global_map)
    """
    files = iter_markdown_under_docs(docs_root)
    reserved: set[str] = set()
    for p in files:
        reserved |= collect_ids_in_text(p.read_text(encoding="utf-8"))

    global_old_to_new: dict[str, str] = {}
    new_contents: dict[Path, str] = {}
    total_headings = 0

    for p in files:
        raw = p.read_text(encoding="utf-8")
        new_text, nchg = plan_migrate_file(raw, min_level, reserved, global_old_to_new)
        new_contents[p] = new_text
        total_headings += nchg

    final = {
        p: replace_fragments_global(t, global_old_to_new) for p, t in new_contents.items()
    }

    files_touched = 0
    for p in files:
        old_t = p.read_text(encoding="utf-8")
        if final[p] != old_t:
            files_touched += 1
            if write:
                p.write_text(final[p], encoding="utf-8")

    return files_touched, total_headings, global_old_to_new


def run_fill(
    paths: list[Path],
    write: bool,
    min_level: int,
) -> tuple[int, int]:
    """ประมวลผลเฉพาะ paths ที่ส่งมา (ไฟล์หรือโฟลเดอร์เดียว)"""
    all_files: list[Path] = []
    for target in paths:
        if target.is_file():
            if target.suffix.lower() == ".md" and ".vitepress" not in target.parts:
                all_files.append(target)
        elif target.is_dir():
            all_files.extend(iter_markdown_under_docs(target))
        else:
            raise SystemExit(f"ไม่พบ path: {target}")
    all_files = sorted(set(all_files))

    reserved: set[str] = set()
    for p in all_files:
        reserved |= collect_ids_in_text(p.read_text(encoding="utf-8"))

    total_files = 0
    total_h = 0
    for p in all_files:
        raw = p.read_text(encoding="utf-8")
        new_text, n, _ = process_fill_only(raw, min_level, reserved)
        if n:
            total_files += 1
            total_h += n
            try:
                rel = p.relative_to(ROOT)
            except ValueError:
                rel = p
            print(f"{'WROTE' if write else 'WOULD UPDATE'} {n} heading(s): {rel}")
            if write:
                p.write_text(new_text, encoding="utf-8")
    return total_files, total_h


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "path",
        nargs="+",
        type=Path,
        help="ไฟล์ .md และ/หรือโฟลเดอร์ (ใช้ -r กับโฟลเดอร์)",
    )
    ap.add_argument("--write", action="store_true", help="เขียนไฟล์")
    ap.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="ถ้ามีโฟลเดอร์ใน args ให้รวมทุก .md ใต้โฟลเดอร์นั้น (เฉพาะโหมด fill)",
    )
    ap.add_argument(
        "--migrate",
        action="store_true",
        help="แทนที่ id เดิมทุกหัวข้อ .ptb-h-block + อัปเดต #fragment ทั้ง docs/ (ใช้กับ path=docs)",
    )
    ap.add_argument(
        "--min-level",
        type=int,
        default=1,
        metavar="N",
        help="ระดับหัวข้อขั้นต่ำ (1=รวม h1, 2=เริ่มจาก ##)",
    )
    args = ap.parse_args()

    if args.min_level < 1 or args.min_level > 6:
        raise SystemExit("--min-level ต้องอยู่ระหว่าง 1 ถึง 6")

    if args.migrate:
        if len(args.path) != 1:
            raise SystemExit("โหมด --migrate ใช้ path เดียว (แนะนำ docs)")
        target = args.path[0]
        if not target.is_absolute():
            target = (ROOT / target).resolve()
        if target.name != "docs" or target.parent != ROOT:
            # อนุญาตเฉพาะ root docs เพื่อให้ replace fragment ครบทั้งไซต์
            raise SystemExit(
                "โหมด --migrate ต้องระบุโฟลเดอร์ docs ของโปรเจกต์เท่านั้น "
                f"(ได้รับ {target})"
            )
        ft, th, _ = run_migrate(target, write=args.write, min_level=args.min_level)
        msg = (
            f"Migrate: {th} heading(s), {ft} file(s) with changes."
            if args.write
            else f"Migrate (dry-run): ~{th} headings, ~{ft} files."
        )
        print(msg, file=sys.stderr)
        return

    # --- fill-only ---
    resolved: list[Path] = []
    for raw_p in args.path:
        p = raw_p if raw_p.is_absolute() else (ROOT / raw_p).resolve()
        if p.is_dir() and args.recursive:
            resolved.append(p)
        elif p.is_dir() and not args.recursive:
            resolved.extend(sorted(p.glob("*.md")))
        else:
            resolved.append(p)

    tf, th = run_fill(resolved, write=args.write, min_level=args.min_level)
    if not args.write:
        print(
            f"Done (dry-run). {th} heading(s) in {tf} file(s). Use --write to apply.",
            file=sys.stderr,
        )
    else:
        print(f"Done. {th} heading(s) in {tf} file(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
