# -*- coding: utf-8 -*-
"""
กำหนด anchor `{#… .ptb-h-block}` ใน vol-01.md ตามกฎภาค ๔
กัณฑ์ (`### ๑. …`) ใช้ id แบบ `v1-{slug-โรมัน}` แทน `v1-kan{n}`; หัวข้อย่อยต่อท้าย `-anu`, `-vini`, `-sik{n}` ฯลฯ

ดูรายละเอียดใน .cursor/rules/ptb-content-guide.mdc

รัน: python scripts/reanchor_vinaya_vol01.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ptb_pali_thai_slug import (  # noqa: E402
    kanda_base_from_numbered_h3_title,
    slug_from_thai_pali_kanda_base,
)

VOL01 = ROOT / "docs" / "09-part-4-tipitaka-digest" / "vinaya-pitaka" / "vol-01.md"

_THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")

# attrs ข้างใน { … } อาจมี id เดิมที่มีจุด (.) — ห้ามใช้ [\w-]+ จำกัดเกินไป
HEADING_RE = re.compile(r"^(?P<pre>(?P<hs>#{2,6})\s+)(?P<title>.+?)\s*\{(?P<attrs>[^}]+)\}\s*$")


def thai_digits_to_int(s: str) -> int:
    return int(s.translate(_THAI_DIGITS))


def ascii_slug(s: str, max_len: int = 32) -> str:
    t = re.sub(r"[^\u0e00-\u0e7fa-zA-Z0-9]+", "-", s.strip().lower())
    t = re.sub(r"-+", "-", t).strip("-")[:max_len]
    return t or "x"


def reanchor_line(
    level: int,
    title: str,
    kbase: str | None,
    sik: int | None,
) -> tuple[str, str | None, int | None]:
    """คืน (new_id, kbase, sik)"""
    t = title.strip()

    if level == 2:
        sik = None
        if t.startswith("ภาพรวม") or t.startswith("เกริ่นนำ"):
            return "v1-overview", None, sik
        if t.startswith("ขยายความ"):
            return "v1-elaboration", None, sik
        return f"v1-h2-{ascii_slug(t, 40)}", kbase, sik

    if level == 3:
        sik = None
        km = re.match(r"^([๐-๙]+)\.\s", t)
        if km:
            base = kanda_base_from_numbered_h3_title(t)
            slug = slug_from_thai_pali_kanda_base(base)
            return f"v1-{slug}", slug, sik
        return f"v1-h3-{ascii_slug(t, 40)}", kbase, sik

    if kbase is None:
        raise ValueError(f"หัวข้อระดับ {level} ก่อนกำหนดกัณฑ์: {t[:60]!r}")

    if level == 4:
        if t.startswith("อนุบัญญัติ"):
            if sik is not None:
                return f"v1-{kbase}-sik{sik}-anu", kbase, sik
            return f"v1-{kbase}-anu", kbase, sik
        if t.startswith("วินีตวัตถุ"):
            if sik is not None:
                return f"v1-{kbase}-sik{sik}-vini", kbase, sik
            return f"v1-{kbase}-vini", kbase, sik
        if t.startswith("สิกขาบทที่"):
            sm = re.search(r"สิกขาบทที่\s+([๐-๙]+)", t)
            if not sm:
                raise ValueError(f"ไม่พบเลขสิกขาบทใน: {t[:80]!r}")
            new_sik = thai_digits_to_int(sm.group(1))
            return f"v1-{kbase}-sik{new_sik}", kbase, new_sik
        if t.startswith("มหาโจร"):
            return f"v1-{kbase}-mahachor", kbase, sik
        return f"v1-{kbase}-h4-{ascii_slug(t, 28)}", kbase, sik

    if level == 5:
        if sik is None:
            raise ValueError(f"h5 ต้องอยู่หลัง #### สิกขาบท: {t[:60]!r}")
        if t.startswith("อนุบัญญัติ"):
            return f"v1-{kbase}-sik{sik}-anu", kbase, sik
        if t.startswith("วินีตวัตถุ"):
            return f"v1-{kbase}-sik{sik}-vini", kbase, sik
        return f"v1-{kbase}-sik{sik}-h5-{ascii_slug(t, 24)}", kbase, sik

    if level == 6:
        return f"v1-{kbase}-sik{sik}-h6-{ascii_slug(t, 20)}", kbase, sik

    raise ValueError(f"ระดับหัวข้อไม่รองรับ: {level}")


def process(text: str) -> str:
    kbase: str | None = None
    sik: int | None = None
    out_lines: list[str] = []
    for raw_line in text.splitlines(keepends=True):
        core = raw_line.rstrip("\r\n")
        line_ending = raw_line[len(core) :] or "\n"
        m = HEADING_RE.match(core)
        if not m or ".ptb-h-block" not in m.group("attrs"):
            out_lines.append(raw_line)
            continue
        hs = m.group("hs")
        title = m.group("title")
        level = len(hs)
        new_id, kbase, sik = reanchor_line(level, title, kbase, sik)
        new_core = f"{m.group('pre')}{title} {{#{new_id} .ptb-h-block}}"
        out_lines.append(new_core + line_ending)
    return "".join(out_lines)


def main() -> None:
    raw = VOL01.read_text(encoding="utf-8")
    new = process(raw)
    VOL01.write_text(new, encoding="utf-8")
    print("Updated", VOL01)


if __name__ == "__main__":
    main()
