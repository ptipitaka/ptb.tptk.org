# -*- coding: utf-8 -*-
"""
PTB ภาค ๔ — สร้าง slug โรมัน (ASCII) จากชื่อกัณฑ์/คำบาลีที่เขียนด้วยไทย

หลักทั่วไป (ใช้กับทุกเล่มวินัยและเล่มอื่นในภาค ๔ ที่ใช้แบบเดียวกัน):
- ถอดเป็นอักษรโรมันที่ใกล้การอ่าน **บาลี** จากการเขียนไทย ไม่ใช้ RTGS ทั่วไปของคำไทยแท้
- ไม่ใส่สระแม่สะกดแบบ IAST (จุด/nikhahit) — ใช้ a-z และ '-' เท่านั้น
- ตัดเลขนำ `๑.` ในหัวข้อ และตัดวงเล็ดคำขยาย ` (ว่าด้วย…)` ก่อนถอด
- ประกอบ slug โดย **longest-prefix match** จาก PALI_THAI_STEMS (เรียงชิ้นยาวสุดก่อน)
  แล้วคั่นชิ้นด้วย '-'
- ถ้าต้องการ **ล็อกลิงก์** ไม่ให้เปลี่ยนเมื่อปรับอัลกอริทึม — ใส่คู่ใน EXACT_KANDA_BASE_SLUGS
- ถ้ามีช่วงข้อความที่ยังไม่มี stem — เพิ่มชิ้นใน PALI_THAI_STEMS (หรือ exact override)

ดูคำอธิบายเพิ่มใน .cursor/rules/ptb-content-guide.mdc
"""
from __future__ import annotations

import re
from typing import Final

# (ข้อความไทย, โรมัน) — เรียงความยาวข้อความไทยมากสุดก่อน (longest match)
_PALI_THAI_STEMS_RAW: Final[list[tuple[str, str]]] = [
    # ชื่อกัณฑ์เต็ม (ยาวสุดก่อน — ใช้ซ้ำได้ทุกเล่ม)
    ("ธรรมสำหรับระงับอธิกรณ์ ๗ อย่าง", "dhamma-adhikarana-samatha-7"),
    ("จตุตถปาราชิกกัณฑ์", "catuttha-parajikakanda"),
    ("ทุติยปาราชิกกัณฑ์", "dutiya-parajikakanda"),
    ("ตติยปาราชิกกัณฑ์", "tatiya-parajikakanda"),
    ("ปฐมปาราชิกกัณฑ์", "pathama-parajikakanda"),
    ("เวรัญชกัณฑ์", "veranjakanda"),
    ("ปาราชิกกัณฑ์", "parajikakanda"),
    ("นิสสัคคิยกัณฑ์", "nissaggiyakanda"),
    ("ปาจิตติยกัณฑ์", "pacittiyakanda"),
    ("ปาฏิเทสนียกัณฑ์", "patidesaniyakanda"),
    ("สัตตรสกัณฑ์", "sattarasakanda"),
    ("เสขิยกัณฑ์", "sekhiyakanda"),
    ("เตรสกัณฑ์", "terasakanda"),
    ("อนิยตกัณฑ์", "aniyatakanda"),
    # ชิ้นย่อย (ประกอบชื่อยาวหรือกัณฑ์ในอนาคต)
    ("ปาราชิก", "parajika"),
    ("เวรัญช", "veranja"),
    ("จตุตถ", "catuttha"),
    ("ปฐม", "pathama"),
    ("ทุติย", "dutiya"),
    ("ตติย", "tatiya"),
    ("เตรส", "terasa"),
    ("อนิยต", "aniyata"),
    ("นิสสัคคิย", "nissaggiya"),
    ("ปาจิตติย", "pacittiya"),
    ("ปาฏิเทสนีย", "patidesaniya"),
    ("เสขิย", "sekhiya"),
    ("สัตตรส", "sattarasa"),
    ("อธิกรณสมถะ", "adhikaranasamatha"),
    ("กัณฑ์", "kanda"),
    # ขันธกะ (มหาวัคค์ / จุลลวัคค์)
    ("วัสสูปนายิกาขันธกะ", "vassupanayika-khandhaka"),
    ("ปวารณาขันธกะ", "pavarana-khandhaka"),
    ("อุโบสถขันธกะ", "uposatha-khandhaka"),
    ("มหาขันธกะ", "maha-khandhaka"),
    ("ปาฏิโมกขฐปนขันธกะ", "patimokkhatthapana-khandhaka"),
    ("ภิกขุนีขันธกะ", "bhikkhuni-khandhaka"),
    ("ขุททกวัตถุขันธกะ", "khuddakavatthu-khandhaka"),
    ("เสนาสนขันธกะ", "senasana-khandhaka"),
    ("สังฆเภทขันธกะ", "sanghabheda-khandhaka"),
    ("สัตตสติกขันธกะ", "sattasatikhandhaka"),
    ("ปัญจสติกขันธกะ", "pancasatikhandhaka"),
    ("วัตตขันธกะ", "vatta-khandhaka"),
    ("สมถขันธกะ", "samatha-khandhaka"),
    ("สมุจจยขันธกะ", "samuccaya-khandhaka"),
    ("กัมมขันธกะ", "kamma-khandhaka"),
    ("โกสัมพิขันธกะ", "kosambi-khandhaka"),
    ("จัมเปยยขันธกะ", "campeyya-khandhaka"),
    ("จีวรขันธกะ", "civara-khandhaka"),
    ("กฐินขันธกะ", "kathina-khandhaka"),
    ("เภสัชชขันธกะ", "bhesajja-khandhaka"),
    ("จัมมขันธกะ", "camma-khandhaka"),
    ("คมิกวัตร", "kamika-vatta"),
]

# ลบรายการซ้ำ แล้วเรียงความยาวมากสุดก่อน
_seen: set[str] = set()
_tmp: list[tuple[str, str]] = []
for th, ro in sorted(_PALI_THAI_STEMS_RAW, key=lambda x: len(x[0]), reverse=True):
    if th not in _seen:
        _seen.add(th)
        _tmp.append((th, ro))
PALI_THAI_STEMS: Final[tuple[tuple[str, str], ...]] = tuple(_tmp)

# ชื่อกัณฑ์หลักเต็มสตริง → slug คงที่ (เสถียรภาพลิงก์ / กรณีพิเศษ)
EXACT_KANDA_BASE_SLUGS: dict[str, str] = {}

MAX_SLUG_LEN: Final[int] = 56


def kanda_base_from_numbered_h3_title(title: str) -> str:
    """ตัด `๑.` นำหน้า และคำในวงเล็บขยายออกจากหัวข้อ ### (ไม่แตะหัวข้อที่ขึ้นต้นด้วย `(`)."""
    t = title.strip()
    t = re.sub(r"^[๐-๙]+\.\s*", "", t)
    ts = t.strip()
    if ts.startswith("("):
        return ts
    if " (" in t:
        t = t.split(" (", 1)[0].strip()
    elif "(" in t:
        t = t.split("(", 1)[0].strip()
    return t.strip()


def slug_from_thai_pali_kanda_base(base: str, *, exact: dict[str, str] | None = None) -> str:
    """
    คืน slug โรมันสำหรับชื่อกัณฑ์หลัก (ไม่มี prefix เลขนำ).
    `exact` รวมกับ EXACT_KANDA_BASE_SLUGS สำหรับรันสคริปต์รายเล่มที่ต้องการ override ชั่วคราว
    """
    b = base.strip()
    ex = {**EXACT_KANDA_BASE_SLUGS, **(exact or {})}
    if b in ex:
        s = ex[b]
    else:
        parts: list[str] = []
        i = 0
        n = len(b)
        while i < n:
            if b[i].isspace():
                i += 1
                continue
            matched = False
            for stem_th, stem_ro in PALI_THAI_STEMS:
                if b.startswith(stem_th, i):
                    parts.append(stem_ro)
                    i += len(stem_th)
                    matched = True
                    break
            if not matched:
                raise ValueError(
                    f"ไม่มี stem สำหรับช่วงที่เหลือของ {b!r} ที่ตำแหน่ง {i} "
                    f"({b[i : i + 24]!r}) — เพิ่มคู่ใน PALI_THAI_STEMS หรือ EXACT_KANDA_BASE_SLUGS "
                    f"ใน scripts/ptb_pali_thai_slug.py"
                )
        s = "-".join(parts)
    s = s.lower()
    if len(s) > MAX_SLUG_LEN:
        s = s[:MAX_SLUG_LEN].rstrip("-")
    return s
