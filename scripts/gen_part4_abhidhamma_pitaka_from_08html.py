# -*- coding: utf-8 -*-
"""
สกัดความย่อภาค ๔ — อภิธัมมปิฎก จาก Initial_source/html5/08.html

อ้างอิงฉบับพิมพ์: Initial_source/ptb_fullbook.pdf หน้า 1134–1302 (และเล่มถัดไปเมื่อเพิ่มคอนฟิก)

เล่มที่รองรับ: ๓๔–๓๗ … (เพิ่มใน PART4_ABHIDHAMMA_VOLUMES)

กระบวนการ convert (ลำดับจริงใน write_volume):
  1. อ่านช่วงบรรทัดของ 08.html ตาม PART4_ABHIDHAMMA_VOLUMES (start_line–end_line)
  2. BeautifulSoup: วนทุก <p> ใน chunk
  3. cell_text_with_footnotes(p): ดึงข้อความจาก span (ข้าม <a>),
     แปลง CharOverride-2/-12 เป็น <PtbFootnote>…</PtbFootnote>,
     <br/> → ช่องว่าง, ยุบช่องว่างซ้ำเป็นช่องว่างเดียว
  4. normalize_quotes: แปลง ” (U+201D) / „ (U+201E) จาก InDesign เป็น placeholder
     เปิด/ปิด ชั่วคราว — ไม่รวมเป็นวรรคเดียวทันที (กันสับสนเปิด-ปิด)
  5. polish_thai_text: ช่องว่าง/คำย่อ/เชิงอรรถ/เครื่องหมายคำพูดหลัง finalize placeholder
  6. finalize_quote_placeholders: แปลง placeholder → " (ASCII) พร้อมจัดช่องว่างเปิด-ปิด
  7. convert_body: layout abhidhamma จัด class head-2-* / ข้อ-1--- / Paragraph-Style → ## ### / <PtbParagraph>
  8. fix_footnote_close_quote_before_para_end
  9. coalesce_thai_numbered_lists: รวมลำดับ ๑. ๒. … เป็น <PtbList auto>
 10. typographic_quotes_docs.transform: คู่ \"…\" ในเนื้อหา → “…” (U+201C / U+201D) ตาม ptb-content-guide
 11. เขียนไฟล์ vol-XX.md ตาม out_subdir ของแต่ละเล่ม

หมายเหตุ: หัวข้อ ##–#### ใส่เฉพาะ `{.ptb-h-block}` — ให้รัน
`python scripts/ensure_ptb_heading_ids.py docs -r --write` หลังรีเจน เพื่อได้ `{#…}` แบบอักษร/ตัวเลข ๑๐ ตัวตามกฎ
(h1 ใน frontmatter ยังใช้ anchor จาก config แต่ละเล่ม)

รัน:
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 34
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 35
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 36
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 37
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 38
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 39
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 40
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 41
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 42
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 43
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 44
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --vol 45
  python scripts/gen_part4_abhidhamma_pitaka_from_08html.py --all
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from bs4 import BeautifulSoup, NavigableString, Tag

from ptb_coalesce_thai_numbered_lists import coalesce_thai_numbered_lists
from typographic_quotes_docs import transform as typographic_quotes_transform

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "08.html"
OUT_BASE = ROOT / "docs" / "09-part-4-tipitaka-digest" / "abhidhamma-pitaka"


class VolCfg(TypedDict):
    start_line: int
    end_line: int
    h1_full: str
    title_nav: str
    h1_anchor: str
    prev_text: str
    prev_link: str
    next_text: str
    next_link: str
    extra_keywords: list[str]
    out_subdir: str
    layout: NotRequired[Literal["digha", "majjhima", "samyutta", "abhidhamma"]]
    nikaya_keyword: NotRequired[str]
    # ย่อหน้าเปิดจาก HTML ที่ไม่ตรงกับ h1_full ทั้งบรรทัด (เช่น หัวเล่มแยก ๒ บรรทัด)
    also_skip_paragraph_texts: NotRequired[list[str]]


PART4_ABHIDHAMMA_VOLUMES: dict[int, VolCfg] = {
    34: {
        "start_line": 241,
        "end_line": 610,
        "h1_full": "เล่ม ๓๔ ธัมมสังคณี (รวมกลุ่มธรรมะ)",
        "title_nav": "เล่ม ๓๔ ธัมมสังคณี",
        "h1_anchor": "GCiHPazmF8",
        "prev_text": "เล่ม ๓๓ อปทาน ภาค ๒ - พุทธวังสะ จริยาปิฎก",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-33",
        "next_text": "เล่ม ๓๕ วิภังค์",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-35",
        "extra_keywords": ["มาติกา"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ธัมมสังคณี",
    },
    35: {
        "start_line": 1247,
        "end_line": 1390,
        "h1_full": "เล่ม ๓๕ วิภังค์ (แยกกลุ่มธรรมะ)",
        "title_nav": "เล่ม ๓๕ วิภังค์",
        "h1_anchor": "tac8HL1FuD",
        "prev_text": "เล่ม ๓๔ ธัมมสังคณี",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-34",
        "next_text": "เล่ม ๓๖ ธาตุกถา และ ปุคคลปัญญัตติ",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-36",
        "extra_keywords": [],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "วิภังค์",
    },
    36: {
        "start_line": 1552,
        "end_line": 1675,
        "h1_full": "เล่ม ๓๖ ธาตุกถา และ ปุคคลปัญญัตติ",
        "title_nav": "เล่ม ๓๖ ธาตุกถา และ ปุคคลปัญญัตติ",
        "h1_anchor": "I7gBmTVHX1",
        "prev_text": "เล่ม ๓๕ วิภังค์",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-35",
        "next_text": "เล่ม ๓๗ กถาวัตถุ",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-37",
        "extra_keywords": ["ปุคคลปัญญัตติ"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ธาตุกถา",
    },
    37: {
        "start_line": 1805,
        "end_line": 3316,
        "h1_full": "เล่ม ๓๗ กถาวัตถุ",
        "title_nav": "เล่ม ๓๗ กถาวัตถุ",
        "h1_anchor": "VI5D3Jb9dI",
        "prev_text": "เล่ม ๓๖ ธาตุกถา และ ปุคคลปัญญัตติ",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-36",
        "next_text": "เล่ม ๓๘ ยมก ภาค ๑",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-38",
        "extra_keywords": [],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "กถาวัตถุ",
    },
    38: {
        "start_line": 4195,
        "end_line": 4402,
        "h1_full": "เล่ม ๓๘ ยมก ภาค ๑",
        "title_nav": "เล่ม ๓๘ ยมก ภาค ๑",
        "h1_anchor": "DRgTXovJVD",
        "prev_text": "เล่ม ๓๗ กถาวัตถุ",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-37",
        "next_text": "เล่ม ๓๙ ยมก ภาค ๒",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-39",
        "extra_keywords": ["ภาค ๑"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ยมก",
    },
    39: {
        "start_line": 4513,
        "end_line": 4591,
        "h1_full": "เล่ม ๓๙ ยมก ภาค ๒",
        "title_nav": "เล่ม ๓๙ ยมก ภาค ๒",
        "h1_anchor": "JdsX3c40og",
        "prev_text": "เล่ม ๓๘ ยมก ภาค ๑",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-38",
        "next_text": "เล่ม ๔๐ ปัฏฐาน ภาค ๑",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-40",
        "extra_keywords": ["ภาค ๒"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ยมก",
    },
    40: {
        "start_line": 4662,
        "end_line": 4798,
        "h1_full": "เล่ม ๔๐ ปัฏฐาน ภาค ๑",
        "title_nav": "เล่ม ๔๐ ปัฏฐาน ภาค ๑",
        "h1_anchor": "QgbBm0bQrE",
        "prev_text": "เล่ม ๓๙ ยมก ภาค ๒",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-39",
        "next_text": "เล่ม ๔๑ ปัฏฐาน ภาค ๒",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-41",
        "extra_keywords": ["ภาค ๑"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ปัฏฐาน",
    },
    41: {
        "start_line": 4950,
        "end_line": 4953,
        "h1_full": "เล่ม ๔๑ ปัฏฐาน ภาค ๒",
        "title_nav": "เล่ม ๔๑ ปัฏฐาน ภาค ๒",
        "h1_anchor": "l9HtDhkNNe",
        "prev_text": "เล่ม ๔๐ ปัฏฐาน ภาค ๑",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-40",
        "next_text": "เล่ม ๔๒ ปัฏฐาน ภาค ๓",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-42",
        "extra_keywords": ["ภาค ๒"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ปัฏฐาน",
    },
    42: {
        "start_line": 4956,
        "end_line": 5095,
        "h1_full": "เล่ม ๔๒ ปัฏฐาน ภาค ๓",
        "title_nav": "เล่ม ๔๒ ปัฏฐาน ภาค ๓",
        "h1_anchor": "Uv8f3o405D",
        "prev_text": "เล่ม ๔๑ ปัฏฐาน ภาค ๒",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-41",
        "next_text": "เล่ม ๔๓ ปัฏฐาน ภาค ๔",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-43",
        "extra_keywords": ["ภาค ๓"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ปัฏฐาน",
    },
    43: {
        "start_line": 5176,
        "end_line": 5303,
        "h1_full": "เล่ม ๔๓ ปัฏฐาน ภาค ๔",
        "title_nav": "เล่ม ๔๓ ปัฏฐาน ภาค ๔",
        "h1_anchor": "jC662540vx",
        "prev_text": "เล่ม ๔๒ ปัฏฐาน ภาค ๓",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-42",
        "next_text": "เล่ม ๔๔ ปัฏฐาน ภาค ๕",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-44",
        "extra_keywords": [],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ปัฏฐาน",
    },
    44: {
        "start_line": 5355,
        "end_line": 5369,
        "h1_full": "เล่ม ๔๔ ปัฏฐาน ภาค ๕",
        "title_nav": "เล่ม ๔๔ ปัฏฐาน ภาค ๕",
        "h1_anchor": "k8miVxzbFK",
        "prev_text": "เล่ม ๔๓ ปัฏฐาน ภาค ๔",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-43",
        "next_text": "เล่ม ๔๕ ปัฏฐาน ภาค ๖",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-45",
        "extra_keywords": ["ภาค ๕"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ปัฏฐาน",
    },
    45: {
        "start_line": 5382,
        "end_line": 5393,
        "h1_full": "เล่ม ๔๕ ปัฏฐาน ภาค ๖",
        "title_nav": "เล่ม ๔๕ ปัฏฐาน ภาค ๖",
        "h1_anchor": "2zNXqvieWJ",
        "prev_text": "เล่ม ๔๔ ปัฏฐาน ภาค ๕",
        "prev_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-44",
        "next_text": "ว่าด้วยบันทึกทางวิชาการ",
        "next_link": "/on-academic-notes/",
        "extra_keywords": ["ภาค ๖"],
        "out_subdir": "",
        "layout": "abhidhamma",
        "nikaya_keyword": "ปัฏฐาน",
    },
}


# InDesign/HTML ใน 08.html ใช้คู่ ” … „ (201D เปิด, 201E ปิด) — ต้องแยกก่อนจึงค่อยเป็น "
PH_Q_OPEN = "\uf020"
PH_Q_CLOSE = "\uf021"


def normalize_quotes(t: str) -> str:
    """แปลงเครื่องหมายคำพูดจาก InDesign เป็น placeholder เปิด/ปิด (ยังไม่ใช่ ")."""
    t = t.replace("\u201d", PH_Q_OPEN)
    t = t.replace("\u201e", PH_Q_CLOSE)
    t = t.replace("\u201c", PH_Q_OPEN)
    t = t.replace("\u201a", PH_Q_CLOSE)
    return t


def finalize_quote_placeholders(t: str) -> str:
    """จัดช่องว่างรอบ placeholder แล้วแปลงเป็น \" (ASCII)."""
    t = re.sub(rf"{re.escape(PH_Q_OPEN)}\s+", PH_Q_OPEN, t)
    t = re.sub(rf"\s+{re.escape(PH_Q_CLOSE)}", PH_Q_CLOSE, t)
    t = re.sub(
        rf"([\u0e00-\u0e7f]){re.escape(PH_Q_OPEN)}",
        rf"\1 {PH_Q_OPEN}",
        t,
    )
    t = re.sub(rf"{re.escape(PH_Q_OPEN)}\s+", PH_Q_OPEN, t)
    t = re.sub(rf"\s+{re.escape(PH_Q_CLOSE)}", PH_Q_CLOSE, t)
    t = t.replace(PH_Q_OPEN, '"').replace(PH_Q_CLOSE, '"')
    t = re.sub(r" {2,}", " ", t)
    return t


def split_trailing_paren_subtitle(text: str) -> tuple[str, str | None]:
    m = re.search(r"\s+(\([^)]{2,500}\))\s*$", text)
    if not m:
        return text, None
    return text[: m.start()].strip(), m.group(1).strip()


def split_first_line_subtitle(text: str) -> tuple[str, str | None]:
    if "\n" not in text:
        return text, None
    a, b = text.split("\n", 1)
    a, b = a.strip(), b.strip()
    if b.startswith("("):
        return a, b
    return text, None


def polish_thai_text_before_quotes(t: str) -> str:
    """ช่องว่าง/เชิงอรรถ/ตัวเลข — ยังไม่แตะเครื่องหมาย \" (ใช้กับข้อความที่มี PH_Q_OPEN/CLOSE)."""
    t = t.replace("กัณฑ์ว่าด้วย", "กัณฑ์ ว่าด้วย")
    t = re.sub(r"([๐-๙]+)(ของ)", r"\1 \2", t)
    t = re.sub(r"^([๑-๙]+)\.([^\s])", r"\1. \2", t)
    t = re.sub(r"(\([๑-๔]\))([ก-๙])", r"\1 \2", t)
    t = re.sub(r" ณ([ก-๙])", r" ณ \1", t)
    t = re.sub(r"ประทับ ณ([ก-๙])", r"ประทับ ณ \1", t)
    t = re.sub(r"ประทับณ\s", "ประทับ ณ ", t)
    t = re.sub(r"(?<=[\u0e00-\u0e7f])\)([ก-ฮ])", r") \1", t)
    t = re.sub(
        r"<PtbFootnote>([^<]+)</PtbFootnote>\s*\(",
        r"<PtbFootnote>\1</PtbFootnote> (",
        t,
    )
    t = re.sub(r"</PtbFootnote>([ก-ฮ])", r"</PtbFootnote> \1", t)
    t = re.sub(r"</PtbFootnote>([^\s<])", r"</PtbFootnote> \1", t)
    t = re.sub(r"นาฬันทามี", "นาฬันทา มี", t)
    t = re.sub(r"มหาปทานสูตรจึง", "มหาปทานสูตร จึง", t)
    t = re.sub(r"เดือน ๑๒พระ", "เดือน ๑๒ พระ", t)
    t = re.sub(r"ปาฏิกสูตรจึง", "ปาฏิกสูตร จึง", t)
    t = re.sub(r"สูตรว่าด้วย", "สูตร ว่าด้วย", t)
    t = re.sub(r"([๐-๙]+)\.([ก-้])", r"\1. \2", t)
    return t


def polish_thai_text_after_quotes(t: str) -> str:
    """หลังได้ \" แล้ว — ไม่ใช้กฎ \"\\s*([ก-๙])\" (เคยทำให้เกิด \\\" ใน… ผิด)."""
    # ห้ามจับคู่ท้าย "กว่า" (เช่น ยิ่งกว่า") — ใช้ (?<!ก) ว่า"
    t = re.sub(r"(?<!ก)ว่า\"", 'ว่า "', t)
    t = re.sub(r"ว่าด้วย\"", 'ว่าด้วย "', t)
    t = re.sub(r"และว่าด้วย\"", 'และว่าด้วย "', t)
    t = re.sub(r"ตรัสว่า\"", 'ตรัสว่า "', t)
    _th_consonant = r"[\u0e01-\u0e2e]"
    t = re.sub(
        rf"({_th_consonant})\"({_th_consonant})",
        r'\1" \2',
        t,
    )
    t = re.sub(
        rf"({_th_consonant})\" ({_th_consonant})",
        r'\1 "\2',
        t,
    )
    t = re.sub(r'"([^"]*?)\s+"(\s+[\u0e01-\u0e2e])', r'"\1"\2', t)
    t = re.sub(
        r'"([^"]*?)\s+"([\u0e01-\u0e2e])',
        r'"\1"\2',
        t,
    )
    t = re.sub(
        r'"([^"]+)"([\u0e01-\u0e2e])',
        r'"\1" \2',
        t,
    )
    t = re.sub(r'ว่า "\s+', 'ว่า "', t)
    t = re.sub(r'และว่าด้วย "\s+', 'และว่าด้วย "', t)
    t = re.sub(r'ว่าด้วย "\s+', 'ว่าด้วย "', t)
    t = re.sub(r'ตรัสว่า "\s+', 'ตรัสว่า "', t)
    t = re.sub(r'แปลว่า" ([\u0e01-\u0e2e])', r'แปลว่า "\1', t)
    t = re.sub(r'และว่าด้วย" ([\u0e01-\u0e2e])', r'และว่าด้วย "\1', t)
    t = re.sub(r'เป็น" ([\u0e01-\u0e2e])', r'เป็น "\1', t)
    return t


def polish_thai_text(t: str) -> str:
    t = polish_thai_text_before_quotes(t)
    t = finalize_quote_placeholders(t)
    t = polish_thai_text_after_quotes(t)
    return t


def _cell_text_raw(node: Tag) -> str:
    """ดึงข้อความจากโหนด <p>/<span> แบบเรียงลูก — ห้ามเรียก polish ซ้ำใน span ย่อย
    (ถ้า polish ทุกชั้น เครื่องหมาย ” จะกลายเป็น \" ก่อนรวมย่อหน้า แล้ว regex ชั้นนอกจะทำลายช่องว่าง)."""
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            if child.name == "br":
                parts.append(" ")
            elif child.name == "a":
                continue
            elif child.name == "span":
                cls = child.get("class") or []
                if "CharOverride-2" in cls or "CharOverride-12" in cls:
                    num = child.get_text(strip=True)
                    if num:
                        parts.append(f"<PtbFootnote>เชิงอรรถ {num} ม.พ.ป.</PtbFootnote>")
                else:
                    parts.append(_cell_text_raw(child))
            else:
                parts.append(child.get_text())
    return "".join(parts)


def cell_text_with_footnotes(node: Tag) -> str:
    t = re.sub(r"\s+", " ", _cell_text_raw(node))
    return polish_thai_text(normalize_quotes(t.strip()))


def cls_set(p: Tag) -> frozenset[str]:
    return frozenset(p.get("class") or [])


def para_override_num(c: frozenset[str]) -> int | None:
    for x in c:
        m = re.fullmatch(r"ParaOverride-(\d+)", x)
        if m:
            return int(m.group(1))
    return None


def first_char_override_in_paragraph(p: Tag, want: frozenset[int]) -> int | None:
    """คืนเลขแรกของ CharOverride-N ที่พบใน <p> (เฉพาะ N ใน want) — ลำดับ DOM."""
    for node in p.find_all("span"):
        for cls in node.get("class") or []:
            m = re.fullmatch(r"CharOverride-(\d+)", cls)
            if m:
                n = int(m.group(1))
                if n in want:
                    return n
    return None


def paragraph_has_charoverride8(p: Tag) -> bool:
    return first_char_override_in_paragraph(p, frozenset({8})) is not None


def is_abhidhamma_heading_paragraph(p: Tag) -> bool:
    """ย่อหน้า p ที่ class ขึ้นต้น head-2- ใน 08.html มักเป็นหัวระดับย่อย; ParaOverride-15 เป็นย่อหน้าเนื้อหาต่อเนื่อง (ตัวเอียง)."""
    c = cls_set(p)
    if para_override_num(c) == 15:
        return False
    return any(cls.startswith("head-2-") for cls in c)


def emit_heading_block(md: list[str], level: str, text: str) -> None:
    md.append(f"{level} {text} {{.ptb-h-block}}")
    md.append("")


def emit_subtitle_heading(md: list[str], text: str) -> None:
    title, sub = split_first_line_subtitle(text)
    if sub is None:
        title, sub = split_trailing_paren_subtitle(title)
    if sub:
        md.append(f"### {title} {{.ptb-h-block}}")
        md.append("")
        md.append(f'<p class="ptb-subtitle">{sub}</p>')
    else:
        md.append(f"### {title} {{.ptb-h-block}}")
    md.append("")


def convert_body(vol: int, cfg: VolCfg) -> str:
    lines = HTML_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    s, e = cfg["start_line"], cfg["end_line"]
    chunk = "".join(lines[s - 1 : e])
    soup = BeautifulSoup(chunk, "html.parser")
    ps = soup.find_all("p")

    md: list[str] = []
    h1_full = cfg["h1_full"]
    overview_done = False
    layout = cfg.get("layout", "digha")

    for p in ps:
        c = cls_set(p)
        po = para_override_num(c)
        text = cell_text_with_footnotes(p)
        if not text:
            continue

        if text == "อภิธัมมปิฎก":
            continue
        skip_title_para = text == h1_full or text.replace(" ", "") == h1_full.replace(
            " ", ""
        )
        if not skip_title_para:
            for sk in cfg.get("also_skip_paragraph_texts") or []:
                if text == sk or text.replace(" ", "") == sk.replace(" ", ""):
                    skip_title_para = True
                    break
        if skip_title_para:
            continue

        if not overview_done:
            md.append("## ภาพรวม {.ptb-h-block}")
            md.append("")
            overview_done = True

        if "จบความย่อแห่งพระไตรปิฎก" in text or "จบความย่อแห่งพระไตรปิฏก" in text:
            text = text.replace("ปิฏก", "ปิฎก")
            text = text.replace("เล่มม ๒๘", "เล่ม ๒๘")
            md.append(f"<PtbParagraph>{text}</PtbParagraph>")
            md.append("")
            continue

        if layout == "abhidhamma":
            # เล่ม ๓๖ ใช้ Paragraph-Style-2 ParaOverride-6 สำหรับ «ขยายความ» (ไม่ใช่ head-2-17p-bold)
            if "Paragraph-Style-2" in c and po == 6 and text.strip() == "ขยายความ":
                emit_heading_block(md, "##", "ขยายความ")
                continue
            if "head-2-17p-bold" in c and text.strip() == "ขยายความ":
                emit_heading_block(md, "##", "ขยายความ")
                continue
            if is_abhidhamma_heading_paragraph(p):
                emit_heading_block(md, "###", text)
                continue
            md.append(f"<PtbParagraph>{text}</PtbParagraph>")
            md.append("")
            continue

        if layout == "majjhima":
            if "Paragraph-Style-2" in c and po == 16 and text.strip() == "ขยายความ":
                emit_heading_block(md, "##", "ขยายความ")
                continue
            if (
                "Paragraph-Style-1" in c
                and po in (2, 24)
                and "วรรค" in text
                and "คือ" in text
            ):
                emit_heading_block(md, "##", text)
                continue

            if "Paragraph-Style-4" in c and po in (6, 16):
                if text.strip() == "ขยายความ":
                    emit_heading_block(md, "##", "ขยายความ")
                else:
                    emit_heading_block(md, "##", text)
                continue

            # หัววรรค (PS4 + PO ๗/๒๕ ไม่มีเลขสูตร CharOverride-8)
            if (
                "Paragraph-Style-4" in c
                and po in (7, 25)
                and "วรรค" in text
                and "คือ" in text
                and not paragraph_has_charoverride8(p)
            ):
                emit_heading_block(md, "##", text)
                continue

            if "Paragraph-Style-4" in c and po in (7, 11, 22):
                emit_subtitle_heading(md, text)
                continue

            if "Paragraph-Style-4" in c and po == 17:
                ch = first_char_override_in_paragraph(p, frozenset({7, 11}))
                if ch == 7:
                    emit_heading_block(md, "##", text)
                else:
                    emit_heading_block(md, "####", text)
                continue

            if "Paragraph-Style-4" in c and po == 8:
                emit_heading_block(md, "####", text)
                continue

            if "Paragraph-Style-4" in c and po is None:
                if paragraph_has_charoverride8(p):
                    emit_subtitle_heading(md, text)
                else:
                    emit_heading_block(md, "####", text)
                continue

            md.append(f"<PtbParagraph>{text}</PtbParagraph>")
            md.append("")
            continue

        # --- layout samyutta (สังยุตตนิกาย เล่ม ๑๕ สคาถวรรค ฯลฯ) ---
        if layout == "samyutta":
            if "Paragraph-Style-1" in c and po == 12:
                emit_heading_block(md, "##", text)
                continue
            if "Paragraph-Style-1" in c and po == 33:
                emit_heading_block(md, "###", text)
                continue
            if "Paragraph-Style-1" in c and po == 13:
                emit_heading_block(md, "##", text)
                continue

            md.append(f"<PtbParagraph>{text}</PtbParagraph>")
            md.append("")
            continue

        # --- layout digha (ทีฆนิกาย เล่ม ๙–๑๑) ---
        if "Paragraph-Style-4" in c and po in (6, 16):
            if text.strip() == "ขยายความ":
                md.append("## ขยายความ {.ptb-h-block}")
            else:
                md.append(f"## {text} {{.ptb-h-block}}")
            md.append("")
            continue

        if "Paragraph-Style-4" in c and po == 7:
            title, sub = split_first_line_subtitle(text)
            if sub is None:
                title, sub = split_trailing_paren_subtitle(title)
            if sub:
                md.append(f"### {title} {{.ptb-h-block}}")
                md.append("")
                md.append(f'<p class="ptb-subtitle">{sub}</p>')
            else:
                md.append(f"### {title} {{.ptb-h-block}}")
            md.append("")
            continue

        if "Paragraph-Style-4" in c and po == 11:
            title, sub = split_first_line_subtitle(text)
            if sub is None:
                title, sub = split_trailing_paren_subtitle(title)
            if sub:
                md.append(f"### {title} {{.ptb-h-block}}")
                md.append("")
                md.append(f'<p class="ptb-subtitle">{sub}</p>')
            else:
                md.append(f"### {title} {{.ptb-h-block}}")
            md.append("")
            continue

        if "Paragraph-Style-4" in c and po in (8, 17):
            md.append(f"#### {text} {{.ptb-h-block}}")
            md.append("")
            continue

        if "Paragraph-Style-4" in c and po is None:
            md.append(f"#### {text} {{.ptb-h-block}}")
            md.append("")
            continue

        md.append(f"<PtbParagraph>{text}</PtbParagraph>")
        md.append("")

    return "\n".join(md).rstrip() + "\n"


def fix_footnote_close_quote_before_para_end(body: str) -> str:
    return re.sub(
        r"</PtbFootnote>\s+\"</PtbParagraph>",
        r'</PtbFootnote>"</PtbParagraph>',
        body,
    )


def write_volume(vol: int) -> None:
    cfg = PART4_ABHIDHAMMA_VOLUMES[vol]
    body = fix_footnote_close_quote_before_para_end(convert_body(vol, cfg))
    body = coalesce_thai_numbered_lists(body)
    pitaka_kw = cfg.get("nikaya_keyword") or "อภิธัมมปิฎก"
    kws = [
        "  - ภาค ๔",
        "  - ความย่อแห่งพระไตรปิฎก",
        "  - อภิธัมมปิฎก",
        f"  - {pitaka_kw}",
    ]
    for x in cfg["extra_keywords"]:
        kws.append(f"  - {x}")
    kw_block = "\n".join(kws)
    fm = f"""---
title: {cfg["title_nav"]}
lang: th
description: ความย่อแห่งพระไตรปิฎก — {cfg["h1_full"]}
outline: [2, 6]
prev: {{ text: '{cfg["prev_text"]}', link: '{cfg["prev_link"]}' }}
next: {{ text: '{cfg["next_text"]}', link: '{cfg["next_link"]}' }}
searchKeywords:
{kw_block}
---

# {cfg["h1_full"]} {{#{cfg["h1_anchor"]} .ptb-h-block}}

"""
    full = fm + body
    full, _n_typo = typographic_quotes_transform(full)
    out = OUT_BASE / cfg["out_subdir"] / f"vol-{vol:02d}.md"
    out.write_text(full, encoding="utf-8")
    print(f"Wrote {out} (typographic quotes: {_n_typo} pair(s))")


def main() -> None:
    vol_choices = sorted(PART4_ABHIDHAMMA_VOLUMES.keys())
    ap = argparse.ArgumentParser(
        description=f"Generate part 4 digest from 08.html (volumes {vol_choices[0]}–{vol_choices[-1]})"
    )
    ap.add_argument(
        "--vol",
        type=int,
        action="append",
        dest="vols",
        choices=vol_choices,
        metavar="N",
        help="Volume number (repeatable)",
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help=f"Generate all configured volumes ({vol_choices[0]}–{vol_choices[-1]})",
    )
    args = ap.parse_args()
    if args.all:
        for v in sorted(PART4_ABHIDHAMMA_VOLUMES.keys()):
            write_volume(v)
    elif args.vols:
        for v in sorted(set(args.vols)):
            write_volume(v)
    else:
        ap.print_help()
        raise SystemExit(2)


if __name__ == "__main__":
    main()
