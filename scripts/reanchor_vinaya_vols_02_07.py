# -*- coding: utf-8 -*-
"""
กำหนด anchor `{#… .ptb-h-block}` ใน vol-02.md – vol-07.md ตามกฎภาค ๔

- เล่ม ๒–๓: โครงปาฏิโมกข์ (กัณฑ์ + วรรค + สิกขาบท)
- เล่ม ๔–๗: โครงขันธกะ (หมวดหลัก / หัวข้อวงเล็บ / หัวข้อย่อย ####)

รัน: python scripts/reanchor_vinaya_vols_02_07.py
     python scripts/reanchor_vinaya_vols_02_07.py --vol 3
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ptb_pali_thai_slug import (  # noqa: E402
    kanda_base_from_numbered_h3_title,
    slug_from_thai_pali_kanda_base,
)

ROOT = Path(__file__).resolve().parents[1]
VINAYA = ROOT / "docs" / "09-part-4-tipitaka-digest" / "vinaya-pitaka"

_THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
HEADING_RE = re.compile(r"^(?P<pre>(?P<hs>#{2,6})\s+)(?P<title>.+?)\s*\{(?P<attrs>[^}]+)\}\s*$")

# หัวข้อ ### (…) ใน vol-04 — ข้อความภายในวงเล็บ → slug
KHANDHAKA_PAREN_INNER_SLUGS: dict[str, str] = {
    "ธัมมจักกัปปวัตตนสูตร มัชฌิมาปฏิปทา": "dhammacakka-majjhima-patipada",
    "ภิกษุปัญจวัคคีย์ ได้เป็นพระอรหันต์": "pancavaggi-arahant",
    "อนุปุพพิกถา อุบาสก อุบาสิกา ชุดแรก": "anupubbikatha-upasaka-upasika",
    "อุรุเวลากัสสปนทีกัสสปและคยากัสสป": "uruvela-kassapa-nadi-kassapa-naya-kassapa",
    "ประทานพระพุทธานุญาตให้มีวัด": "buddhanumata-vatthu",
}


def plain_heading_title(t: str) -> str:
    return re.sub(r"<PtbFootnote>.*?</PtbFootnote>", "", t, flags=re.DOTALL).strip()


def thai_digits_to_int(s: str) -> int:
    return int(s.translate(_THAI_DIGITS))


def ascii_slug(s: str, max_len: int = 32) -> str:
    t = re.sub(r"[^\u0e00-\u0e7fa-zA-Z0-9]+", "-", s.strip().lower())
    t = re.sub(r"-+", "-", t).strip("-")[:max_len]
    return t or "x"


def unique_anchor_id(used: set[str], base_id: str) -> str:
    """คง base_id ถ้ายังไม่ซ้ำ มิฉะนั้นเติม -u2, -u3, … จนไม่ชนกัน"""
    if base_id not in used:
        used.add(base_id)
        return base_id
    n = 2
    while True:
        cand = f"{base_id}-u{n}"
        if cand not in used:
            used.add(cand)
            return cand
        n += 1


def slug_for_paren_inner(inner: str) -> str:
    inner = inner.strip()
    if inner in KHANDHAKA_PAREN_INNER_SLUGS:
        return KHANDHAKA_PAREN_INNER_SLUGS[inner]
    return ascii_slug(inner, 40)


def reanchor_patimokkha(vol: int, text: str) -> str:
    prefix = f"v{vol}"
    kbase: str | None = None
    vagga = 0
    sik: int | None = None
    used_ids: set[str] = set()
    out: list[str] = []

    for raw_line in text.splitlines(keepends=True):
        core = raw_line.rstrip("\r\n")
        line_ending = raw_line[len(core) :] or "\n"
        m = HEADING_RE.match(core)
        if not m or ".ptb-h-block" not in m.group("attrs"):
            out.append(raw_line)
            continue

        hs = m.group("hs")
        title_raw = m.group("title")
        level = len(hs)
        plain = plain_heading_title(title_raw)
        t = plain.strip()

        if level == 2:
            sik = None
            if t.startswith("ภาพรวม") or t.startswith("เกริ่นนำ"):
                new_id = f"{prefix}-overview"
                kbase = None
                vagga = 0
            elif t.startswith("ขยายความ"):
                new_id = f"{prefix}-elaboration"
                kbase = None
                vagga = 0
            else:
                new_id = f"{prefix}-h2-{ascii_slug(t, 40)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if level == 3:
            sik = None
            if re.match(r"^[๐-๙]+\.\s", t):
                base = kanda_base_from_numbered_h3_title(t)
                if base.startswith("("):
                    raise ValueError(f"H3 ผิดรูปแบบหลังตัดเลข: {t!r}")
                kbase = slug_from_thai_pali_kanda_base(base)
                vagga = 0
                new_id = f"{prefix}-{kbase}"
            else:
                vm = re.match(r"^\(([๐-๙]+)\)\s*", t)
                if vm and kbase is not None:
                    vagga = thai_digits_to_int(vm.group(1))
                    new_id = f"{prefix}-{kbase}-vg{vagga}"
                else:
                    new_id = f"{prefix}-h3-{ascii_slug(t, 40)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if kbase is None:
            raise ValueError(f"หัวข้อระดับ {level} ก่อนกำหนดกัณฑ์: {t[:70]!r}")

        if level == 4:
            vm = re.match(r"^\(([๐-๙]+)\)\s*", t)
            if vm:
                vagga = thai_digits_to_int(vm.group(1))
                new_id = f"{prefix}-{kbase}-vg{vagga}"
            elif t.startswith("สิกขาบทที่"):
                sm = re.search(r"สิกขาบทที่\s+([๐-๙]+)", t)
                if not sm:
                    raise ValueError(f"ไม่พบเลขสิกขาบท: {t[:80]!r}")
                new_sik = thai_digits_to_int(sm.group(1))
                sik = new_sik
                if vagga:
                    new_id = f"{prefix}-{kbase}-vg{vagga}-sik{new_sik}"
                else:
                    new_id = f"{prefix}-{kbase}-sik{new_sik}"
            elif t.startswith("อนุบัญญัติ"):
                if sik is not None and vagga:
                    new_id = f"{prefix}-{kbase}-vg{vagga}-sik{sik}-anu"
                elif sik is not None:
                    new_id = f"{prefix}-{kbase}-sik{sik}-anu"
                else:
                    new_id = f"{prefix}-{kbase}-anu"
            elif t.startswith("วินีตวัตถุ"):
                if sik is not None and vagga:
                    new_id = f"{prefix}-{kbase}-vg{vagga}-sik{sik}-vini"
                elif sik is not None:
                    new_id = f"{prefix}-{kbase}-sik{sik}-vini"
                else:
                    new_id = f"{prefix}-{kbase}-vini"
            elif t.startswith("มหาโจร"):
                new_id = f"{prefix}-{kbase}-mahachor"
            else:
                new_id = f"{prefix}-{kbase}-h4-{ascii_slug(t, 28)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if level == 5:
            if t.startswith("อนุบัญญัติ"):
                if sik is None:
                    raise ValueError(f"h5 อนุบัญญัติ ไม่มีสิกขาบทก่อนหน้า: {t[:60]!r}")
                if vagga:
                    new_id = f"{prefix}-{kbase}-vg{vagga}-sik{sik}-anu"
                else:
                    new_id = f"{prefix}-{kbase}-sik{sik}-anu"
            elif t.startswith("วินีตวัตถุ"):
                if sik is None:
                    raise ValueError(f"h5 วินีตวัตถุ ไม่มีสิกขาบทก่อนหน้า: {t[:60]!r}")
                if vagga:
                    new_id = f"{prefix}-{kbase}-vg{vagga}-sik{sik}-vini"
                else:
                    new_id = f"{prefix}-{kbase}-sik{sik}-vini"
            elif t.startswith("สิกขาบทที่"):
                sm = re.search(r"สิกขาบทที่\s+([๐-๙]+)", t)
                if not sm:
                    raise ValueError(f"ไม่พบเลขสิกขาบทใน h5: {t[:80]!r}")
                new_sik = thai_digits_to_int(sm.group(1))
                sik = new_sik
                if vagga:
                    new_id = f"{prefix}-{kbase}-vg{vagga}-sik{new_sik}"
                else:
                    new_id = f"{prefix}-{kbase}-sik{new_sik}"
            else:
                if sik is None:
                    new_id = f"{prefix}-{kbase}-h5-{ascii_slug(t, 24)}"
                elif vagga:
                    new_id = f"{prefix}-{kbase}-vg{vagga}-sik{sik}-h5-{ascii_slug(t, 20)}"
                else:
                    new_id = f"{prefix}-{kbase}-sik{sik}-h5-{ascii_slug(t, 20)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if level == 6:
            new_id = f"{prefix}-{kbase}-sik{sik}-h6-{ascii_slug(t, 20)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        raise ValueError(f"ระดับหัวข้อไม่รองรับ: {level} ใน {t[:50]!r}")

    return "".join(out)


def reanchor_khandhaka(vol: int, text: str) -> str:
    prefix = f"v{vol}"
    ch3: str | None = None
    sub3: str | None = None
    used_ids: set[str] = set()
    out: list[str] = []

    for raw_line in text.splitlines(keepends=True):
        core = raw_line.rstrip("\r\n")
        line_ending = raw_line[len(core) :] or "\n"
        m = HEADING_RE.match(core)
        if not m or ".ptb-h-block" not in m.group("attrs"):
            out.append(raw_line)
            continue

        hs = m.group("hs")
        title_raw = m.group("title")
        level = len(hs)
        plain = plain_heading_title(title_raw)
        t = plain.strip()

        if level == 2:
            if t.startswith("ภาพรวม") or t.startswith("เกริ่นนำ"):
                new_id = f"{prefix}-overview"
            elif t.startswith("ขยายความ"):
                new_id = f"{prefix}-elaboration"
            else:
                new_id = f"{prefix}-h2-{ascii_slug(t, 40)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if level == 3:
            sub3 = None
            if re.match(r"^[๐-๙]+\.\s", t):
                base = kanda_base_from_numbered_h3_title(t)
                ch3 = slug_from_thai_pali_kanda_base(base)
                new_id = f"{prefix}-{ch3}"
            elif t.startswith("(") and ")" in t:
                inner = t[1 : t.index(")")].strip()
                sub3 = slug_for_paren_inner(inner)
                if ch3 is None:
                    raise ValueError(f"หัวข้อ ### (…) ก่อนกำหนดหมวดหลัก: {t[:60]!r}")
                new_id = f"{prefix}-{ch3}-{sub3}"
            else:
                ch3 = slug_from_thai_pali_kanda_base(t)
                new_id = f"{prefix}-{ch3}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if level == 4:
            if ch3 is None:
                new_id = f"{prefix}-h4-{ascii_slug(t, 28)}"
            else:
                mid = f"-{sub3}" if sub3 else ""
                new_id = f"{prefix}-{ch3}{mid}-h4-{ascii_slug(t, 28)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if level == 5:
            mid = f"-{sub3}" if sub3 else ""
            if ch3 is None:
                new_id = f"{prefix}-h5-{ascii_slug(t, 24)}"
            else:
                new_id = f"{prefix}-{ch3}{mid}-h5-{ascii_slug(t, 24)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        if level == 6:
            mid = f"-{sub3}" if sub3 else ""
            new_id = f"{prefix}-{ch3}{mid}-h6-{ascii_slug(t, 20)}" if ch3 else f"{prefix}-h6-{ascii_slug(t, 20)}"
            new_id = unique_anchor_id(used_ids, new_id)
            out.append(f"{m.group('pre')}{title_raw} {{#{new_id} .ptb-h-block}}" + line_ending)
            continue

        raise ValueError(f"khandhaka: ระดับ {level} ไม่รองรับ")

    return "".join(out)


def process_volume(vol: int) -> None:
    path = VINAYA / f"vol-{vol:02d}.md"
    raw = path.read_text(encoding="utf-8")
    if vol in (2, 3):
        new = reanchor_patimokkha(vol, raw)
    elif vol in (4, 5, 6, 7):
        new = reanchor_khandhaka(vol, raw)
    else:
        raise SystemExit(f"ยังไม่รองรับเล่ม {vol}")
    path.write_text(new, encoding="utf-8")
    print("Updated", path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", type=int, help="เฉพาะเล่มเดียว (2–7)")
    args = ap.parse_args()
    vols = [args.vol] if args.vol is not None else [2, 3, 4, 5, 6, 7]
    for v in vols:
        if v < 2 or v > 7:
            raise SystemExit("ใช้ --vol ตั้งแต่ 2 ถึง 7")
        process_volume(v)


if __name__ == "__main__":
    main()
