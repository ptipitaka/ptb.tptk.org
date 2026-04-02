# -*- coding: utf-8 -*-
"""
สกัดความย่อภาค ๔ — สุตตันตปิฎก (ทีฆนิกาย, มัชฌิมนิกาย, สังยุตตนิกาย เล่ม ๑๕–๑๙, อังคุตตรนิกาย เล่ม ๒๐–๒๔, ขุททกนิกาย เล่ม ๒๕–๓๓) จาก Initial_source/html5/07.html

เล่มที่รองรับ: ๙–๑๑ (digha-nikaya), ๑๒–๑๔ (majjhima-nikaya), ๑๕–๑๙ (samyutta-nikaya), ๒๐–๒๔ (anguttara-nikaya), ๒๕–๓๓ (khuddaka-nikaya)

กระบวนการ convert (ลำดับจริงใน write_volume):
  1. อ่านช่วงบรรทัดของ 07.html ตาม PART4_DIGEST_VOLUMES (start_line–end_line)
  2. BeautifulSoup: วนทุก <p> ใน chunk
  3. cell_text_with_footnotes(p): ดึงข้อความจาก span (ข้าม <a>),
     แปลง CharOverride-2/-12 เป็น <PtbFootnote>…</PtbFootnote>,
     <br/> → ช่องว่าง, ยุบช่องว่างซ้ำเป็นช่องว่างเดียว
  4. normalize_quotes: แปลง ” (U+201D) / „ (U+201E) จาก InDesign เป็น placeholder
     เปิด/ปิด ชั่วคราว — ไม่รวมเป็นวรรคเดียวทันที (กันสับสนเปิด-ปิด)
  5. polish_thai_text: ช่องว่าง/คำย่อ/เชิงอรรถ/เครื่องหมายคำพูดหลัง finalize placeholder
  6. finalize_quote_placeholders: แปลง placeholder → " (ASCII) พร้อมจัดช่องว่างเปิด-ปิด
  7. convert_body: จัด class Paragraph-Style / ParaOverride → ## ### #### / <PtbParagraph>
     (ย่อหน้าเนื้อหาทั้งหมดใช้ PtbParagraph — ไม่ใช้ ptb-paragraph-no-indent จาก ParaOverride)
  8. fix_footnote_close_quote_before_para_end
  9. coalesce_thai_numbered_lists: รวมลำดับ ๑. ๒. … เป็น <PtbList auto>
 10. typographic_quotes_docs.transform: คู่ \"…\" ในเนื้อหา → “…” (U+201C / U+201D) ตาม ptb-content-guide
 11. เขียนไฟล์ vol-XX.md ตาม out_subdir ของแต่ละเล่ม

หมายเหตุ: หัวข้อ ##–#### ใส่เฉพาะ `{.ptb-h-block}` — ให้รัน
`python scripts/ensure_ptb_heading_ids.py docs -r --write` หลังรีเจน เพื่อได้ `{#…}` แบบอักษร/ตัวเลข ๑๐ ตัวตามกฎ
(h1 ใน frontmatter ยังใช้ anchor จาก config แต่ละเล่ม)

รัน:
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 11
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 12 --vol 13
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 15
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 16 --vol 17 --vol 18 --vol 19
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 20
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 21
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 22
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 23
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 24
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 25
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 26
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 27
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 28
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 29
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 30
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 31
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 32
  python scripts/gen_part4_sutta_pitaka_from_07html.py --vol 33
  python scripts/gen_part4_sutta_pitaka_from_07html.py --all
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
HTML_PATH = ROOT / "Initial_source" / "html5" / "07.html"
OUT_BASE = ROOT / "docs" / "09-part-4-tipitaka-digest" / "sutta-pitaka"


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
    layout: NotRequired[Literal["digha", "majjhima", "samyutta"]]
    nikaya_keyword: NotRequired[str]
    # ย่อหน้าเปิดจาก HTML ที่ไม่ตรงกับ h1_full ทั้งบรรทัด (เช่น หัวเล่มแยก ๒ บรรทัด)
    also_skip_paragraph_texts: NotRequired[list[str]]


PART4_DIGEST_VOLUMES: dict[int, VolCfg] = {
    9: {
        "start_line": 240,
        "end_line": 620,
        "h1_full": "เล่ม ๙ ทีฆนิกาย สีลขันธวัคค์",
        "title_nav": "เล่ม ๙ สีลขันธวัคค์",
        "h1_anchor": "sjoTRI4HWs",
        "prev_text": "เล่ม ๘ ปริวาร",
        "prev_link": "/part-4-tipitaka-digest/vinaya-pitaka/vol-08",
        "next_text": "เล่ม ๑๐ มหาวัคค์",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-10",
        "extra_keywords": ["สีลขันธวัคค์"],
        "out_subdir": "digha-nikaya",
    },
    10: {
        "start_line": 1155,
        "end_line": 1508,
        "h1_full": "เล่ม ๑๐ ทีฆนิกาย มหาวัคค์",
        "title_nav": "เล่ม ๑๐ มหาวัคค์",
        "h1_anchor": "38XeOApWRh",
        "prev_text": "เล่ม ๙ สีลขันธวัคค์",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-09",
        "next_text": "เล่ม ๑๑ ปาฏิกวัคค์",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-11",
        "extra_keywords": ["มหาวัคค์"],
        "out_subdir": "digha-nikaya",
    },
    11: {
        "start_line": 2083,
        "end_line": 2523,
        "h1_full": "เล่ม ๑๑ ทีฆนิกาย ปาฏิกวัคค์",
        "title_nav": "เล่ม ๑๑ ปาฏิกวัคค์",
        "h1_anchor": "Tk7Rp2MqNw",
        "prev_text": "เล่ม ๑๐ มหาวัคค์",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-10",
        "next_text": "เล่ม ๑๒ มูลปัณณาสก์",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-12",
        "extra_keywords": ["ปาฏิกวัคค์"],
        "out_subdir": "digha-nikaya",
    },
    12: {
        "start_line": 3265,
        "end_line": 3988,
        "h1_full": "เล่ม ๑๒ มัชฌิมนิกาย มูลปัณณาสก์",
        "title_nav": "เล่ม ๑๒ มูลปัณณาสก์",
        "h1_anchor": "Zx4Wn8HvLm",
        "prev_text": "เล่ม ๑๑ ปาฏิกวัคค์",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-11",
        "next_text": "เล่ม ๑๓ มัชฌิมปัณณาสก์",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13",
        "extra_keywords": ["มูลปัณณาสก์"],
        "out_subdir": "majjhima-nikaya",
        "layout": "majjhima",
    },
    13: {
        "start_line": 5060,
        "end_line": 5589,
        "h1_full": "เล่ม ๑๓ มัชฌิมนิกาย มัชฌิมปัณณาสก์",
        "title_nav": "เล่ม ๑๓ มัชฌิมปัณณาสก์",
        "h1_anchor": "Bc9Js3QyKp",
        "prev_text": "เล่ม ๑๒ มูลปัณณาสก์",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-12",
        "next_text": "เล่ม ๑๔ อุปริปัณณาสก์",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-14",
        "extra_keywords": ["มัชฌิมปัณณาสก์"],
        "out_subdir": "majjhima-nikaya",
        "layout": "majjhima",
    },
    14: {
        "start_line": 6624,
        "end_line": 7029,
        "h1_full": "เล่ม ๑๔ มัชฌิมนิกาย อุปริปัณณาสก์",
        "title_nav": "เล่ม ๑๔ อุปริปัณณาสก์",
        "h1_anchor": "Qm8Rt4VnXz",
        "prev_text": "เล่ม ๑๓ มัชฌิมปัณณาสก์",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13",
        "next_text": "เล่ม ๑๕ สคาถวรรค",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-15",
        "extra_keywords": ["อุปริปัณณาสก์"],
        "out_subdir": "majjhima-nikaya",
        "layout": "majjhima",
    },
    15: {
        "start_line": 7748,
        "end_line": 7774,
        "h1_full": "เล่ม ๑๕ สังยุตตนิกาย สคาถวรรค",
        "title_nav": "เล่ม ๑๕ สคาถวรรค",
        "h1_anchor": "Ak171aWeAw",
        "prev_text": "เล่ม ๑๔ อุปริปัณณาสก์",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-14",
        "next_text": "เล่ม ๑๖ นิทานวรรค",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-16",
        "extra_keywords": ["สคาถวรรค"],
        "out_subdir": "samyutta-nikaya",
        "layout": "samyutta",
        "nikaya_keyword": "สังยุตตนิกาย",
    },
    16: {
        "start_line": 7808,
        "end_line": 7819,
        "h1_full": "เล่ม ๑๖ สังยุตตนิกาย นิทานวรรค",
        "title_nav": "เล่ม ๑๖ นิทานวรรค",
        "h1_anchor": "OakrdssHXn",
        "prev_text": "เล่ม ๑๕ สคาถวรรค",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-15",
        "next_text": "เล่ม ๑๗ ขันธวารวรรค",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-17",
        "extra_keywords": ["นิทานวรรค"],
        "out_subdir": "samyutta-nikaya",
        "layout": "samyutta",
        "nikaya_keyword": "สังยุตตนิกาย",
    },
    17: {
        "start_line": 7822,
        "end_line": 7843,
        "h1_full": "เล่ม ๑๗ สังยุตตนิกาย ขันธวารวรรค",
        "title_nav": "เล่ม ๑๗ ขันธวารวรรค",
        "h1_anchor": "NqpmYnr14G",
        "prev_text": "เล่ม ๑๖ นิทานวรรค",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-16",
        "next_text": "เล่ม ๑๘ สฬายตนวรรค",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-18",
        "extra_keywords": ["ขันธวารวรรค"],
        "out_subdir": "samyutta-nikaya",
        "layout": "samyutta",
        "nikaya_keyword": "สังยุตตนิกาย",
    },
    18: {
        "start_line": 7867,
        "end_line": 7879,
        "h1_full": "เล่ม ๑๘ สังยุตตนิกาย สฬายตนวรรค",
        "title_nav": "เล่ม ๑๘ สฬายตนวรรค",
        "h1_anchor": "uS0Q4HOIb4",
        "prev_text": "เล่ม ๑๗ ขันธวารวรรค",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-17",
        "next_text": "เล่ม ๑๙ มหาวารวรรค",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-19",
        "extra_keywords": ["สฬายตนวรรค"],
        "out_subdir": "samyutta-nikaya",
        "layout": "samyutta",
        "nikaya_keyword": "สังยุตตนิกาย",
    },
    19: {
        "start_line": 7895,
        "end_line": 7910,
        "h1_full": "เล่ม ๑๙ สังยุตตนิกาย มหาวารวรรค",
        "title_nav": "เล่ม ๑๙ มหาวารวรรค",
        "h1_anchor": "wq9LecALRq",
        "prev_text": "เล่ม ๑๘ สฬายตนวรรค",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-18",
        "next_text": "เล่ม ๒๐ เอก - ติกนิบาต",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20",
        "extra_keywords": ["มหาวารวรรค"],
        "out_subdir": "samyutta-nikaya",
        "layout": "samyutta",
        "nikaya_keyword": "สังยุตตนิกาย",
    },
    20: {
        "start_line": 8113,
        "end_line": 8726,
        "h1_full": "เล่ม ๒๐ อังคุตตรนิกาย เอก - ทุก - ติกนิบาต",
        "title_nav": "เล่ม ๒๐ เอก - ติกนิบาต",
        "h1_anchor": "ssUj4TBRl1",
        "prev_text": "เล่ม ๑๙ มหาวารวรรค",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-19",
        "next_text": "เล่ม ๒๑ จตุกกนิบาต",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-21",
        "extra_keywords": ["เอกนิบาต", "ทุกนิบาต", "ติกนิบาต"],
        "out_subdir": "anguttara-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "อังคุตตรนิกาย",
    },
    21: {
        "start_line": 9358,
        "end_line": 9868,
        "h1_full": "เล่ม ๒๑ อังคุตตรนิกาย จตุกกนิบาต",
        "title_nav": "เล่ม ๒๑ จตุกกนิบาต",
        "h1_anchor": "xM8d7ibHB5",
        "prev_text": "เล่ม ๒๐ เอก - ติกนิบาต",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20",
        "next_text": "เล่ม ๒๒ ปัญจก - ฉักกนิบาต",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-22",
        "extra_keywords": ["จตุกกนิบาต"],
        "out_subdir": "anguttara-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "อังคุตตรนิกาย",
    },
    22: {
        "start_line": 10408,
        "end_line": 10882,
        "h1_full": "เล่ม ๒๒ อังคุตตรนิกาย ปัญจก - ฉักกนิบาต",
        "title_nav": "เล่ม ๒๒ ปัญจก - ฉักกนิบาต",
        "h1_anchor": "RfobppBc1J",
        "prev_text": "เล่ม ๒๑ จตุกกนิบาต",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-21",
        "next_text": "เล่ม ๒๓ สัตตก - นวกนิบาต",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-23",
        "extra_keywords": ["ปัญจกนิบาต", "ฉักกนิบาต"],
        "out_subdir": "anguttara-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "อังคุตตรนิกาย",
    },
    23: {
        "start_line": 11536,
        "end_line": 11962,
        "h1_full": "เล่ม ๒๓ อังคุตตรนิกาย สัตตก - อัฏฐก - นวกนิบาต",
        "title_nav": "เล่ม ๒๓ สัตตก - นวกนิบาต",
        "h1_anchor": "S613HNLlfC",
        "prev_text": "เล่ม ๒๒ ปัญจก - ฉักกนิบาต",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-22",
        "next_text": "เล่ม ๒๔ ทสก - เอกาทสกนิบาต",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-24",
        "extra_keywords": ["สัตตกนิบาต", "อัฏฐกนิบาต", "นวกนิบาต"],
        "out_subdir": "anguttara-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "อังคุตตรนิกาย",
    },
    24: {
        "start_line": 12471,
        "end_line": 12758,
        "h1_full": "เล่ม ๒๔ อังคุตตรนิกาย ทสก - เอกาทสกนิบาต",
        "title_nav": "เล่ม ๒๔ ทสก - เอกาทสกนิบาต",
        "h1_anchor": "JDfsqvN7tl",
        "prev_text": "เล่ม ๒๓ สัตตก - นวกนิบาต",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-23",
        "next_text": "เล่ม ๒๕ ขุททกปาฐะ ธัมมปทคาถา อุทาน อิติวุตตกะ สุตตนิบาต",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-25",
        "extra_keywords": ["ทสกนิบาต", "เอกาทสกนิบาต"],
        "out_subdir": "anguttara-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "อังคุตตรนิกาย",
    },
    25: {
        "start_line": 13251,
        "end_line": 13425,
        "h1_full": "เล่ม ๒๕ ขุททกปาฐะ ธัมมปทคาถา อุทาน อิติวุตตกะ สุตตนิบาต",
        "title_nav": "เล่ม ๒๕ ขุททกปาฐะ ธัมมปทคาถา อุทาน อิติวุตตกะ สุตตนิบาต",
        "h1_anchor": "RyYLpSXijO",
        "prev_text": "เล่ม ๒๔ ทสก - เอกาทสกนิบาต",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-24",
        "next_text": "เล่ม ๒๖ วิมานวัตถุ เปตวัตถุ เถรคาถา เถรีคาถา",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-26",
        "extra_keywords": [
            "ขุททกปาฐะ",
            "ธัมมปทคาถา",
            "อุทาน",
            "อิติวุตตกะ",
            "สุตตนิบาต",
        ],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๒๕ ขุททกนิกาย",
            "ขุททกปาฐะ ธัมมปทคาถา อุทาน อิติวุตตกะ สุตตนิบาต",
        ],
    },
    26: {
        "start_line": 13698,
        "end_line": 13756,
        "h1_full": "เล่ม ๒๖ วิมานวัตถุ เปตวัตถุ เถรคาถา เถรีคาถา",
        "title_nav": "เล่ม ๒๖ วิมานวัตถุ เปตวัตถุ เถรคาถา เถรีคาถา",
        "h1_anchor": "ghqXaxHDjF",
        "prev_text": "เล่ม ๒๕ ขุททกปาฐะ ธัมมปทคาถา อุทาน อิติวุตตกะ สุตตนิบาต",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-25",
        "next_text": "เล่ม ๒๗ ชาดก ภาค ๑",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-27",
        "extra_keywords": [
            "วิมานวัตถุ",
            "เปตวัตถุ",
            "เถรคาถา",
            "เถรีคาถา",
        ],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๒๖ ขุททกนิกาย",
            "วิมานวัตถุ เปตวัตถุ เถรคาถา เถรีคาถา",
        ],
    },
    27: {
        "start_line": 13808,
        "end_line": 13842,
        "h1_full": "เล่ม ๒๗ ชาดก ภาค ๑",
        "title_nav": "เล่ม ๒๗ ชาดก ภาค ๑",
        "h1_anchor": "KPhOVYVa2z",
        "prev_text": "เล่ม ๒๖ วิมานวัตถุ เปตวัตถุ เถรคาถา เถรีคาถา",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-26",
        "next_text": "เล่ม ๒๘ ชาดก ภาค ๒",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-28",
        "extra_keywords": ["ชาดก"],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๒๗ ขุททกนิกาย ชาดก ภาค ๑",
        ],
    },
    28: {
        "start_line": 13865,
        "end_line": 13889,
        "h1_full": "เล่ม ๒๘ ชาดก ภาค ๒",
        "title_nav": "เล่ม ๒๘ ชาดก ภาค ๒",
        "h1_anchor": "bxyeFNpvQV",
        "prev_text": "เล่ม ๒๗ ชาดก ภาค ๑",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-27",
        "next_text": "เล่ม ๒๙ มหานิทเทส",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-29",
        "extra_keywords": ["ชาดก"],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๒๘ ขุททกนิกาย ชาดก ภาค ๒",
        ],
    },
    29: {
        "start_line": 13931,
        "end_line": 13934,
        "h1_full": "เล่ม ๒๙ มหานิทเทส",
        "title_nav": "เล่ม ๒๙ มหานิทเทส",
        "h1_anchor": "0sdStSiwJ9",
        "prev_text": "เล่ม ๒๘ ชาดก ภาค ๒",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-28",
        "next_text": "เล่ม ๓๐ จูฬนิทเทส",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-30",
        "extra_keywords": ["มหานิทเทส"],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๒๙ ขุททกนิกาย มหานิทเทส",
        ],
    },
    30: {
        "start_line": 13937,
        "end_line": 13940,
        "h1_full": "เล่ม ๓๐ จูฬนิทเทส",
        "title_nav": "เล่ม ๓๐ จูฬนิทเทส",
        "h1_anchor": "Bx8ke7MNy1",
        "prev_text": "เล่ม ๒๙ มหานิทเทส",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-29",
        "next_text": "เล่ม ๓๑ ปฏิสัมภิทามรรค",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-31",
        "extra_keywords": ["จูฬนิทเทส"],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๓๐ ขุททกนิกาย จูฬนิทเทส",
        ],
    },
    31: {
        "start_line": 13943,
        "end_line": 14129,
        "h1_full": "เล่ม ๓๑ ปฏิสัมภิทามรรค",
        "title_nav": "เล่ม ๓๑ ปฏิสัมภิทามรรค",
        "h1_anchor": "cFaO4hJVZ5",
        "prev_text": "เล่ม ๓๐ จูฬนิทเทส",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-30",
        "next_text": "เล่ม ๓๒ อปทาน ภาค ๑",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-32",
        "extra_keywords": ["ปฏิสัมภิทามรรค"],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๓๑ ขุททกนิกาย ปฏิสัมภิทามรรค (ทางแห่งความแตกฉาน)",
        ],
    },
    32: {
        "start_line": 14259,
        "end_line": 14295,
        "h1_full": "เล่ม ๓๒ อปทาน ภาค ๑",
        "title_nav": "เล่ม ๓๒ อปทาน ภาค ๑",
        "h1_anchor": "AFdmdZ42Lf",
        "prev_text": "เล่ม ๓๑ ปฏิสัมภิทามรรค",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-31",
        "next_text": "เล่ม ๓๓ อปทาน ภาค ๒ - พุทธวังสะ จริยาปิฎก",
        "next_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-33",
        "extra_keywords": ["อปทาน"],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๓๒ ขุททกนิกาย อปทาน ภาค ๑",
        ],
    },
    33: {
        "start_line": 14357,
        "end_line": 14548,
        "h1_full": "เล่ม ๓๓ อปทาน ภาค ๒ - พุทธวังสะ จริยาปิฎก",
        "title_nav": "เล่ม ๓๓ อปทาน ภาค ๒ - พุทธวังสะ จริยาปิฎก",
        "h1_anchor": "vPBRYElMZg",
        "prev_text": "เล่ม ๓๒ อปทาน ภาค ๑",
        "prev_link": "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-32",
        "next_text": "เล่ม ๓๔ ธัมมสังคณี",
        "next_link": "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-34",
        "extra_keywords": ["อปทาน", "พุทธวังสะ", "จริยาปิฎก"],
        "out_subdir": "khuddaka-nikaya",
        "layout": "majjhima",
        "nikaya_keyword": "ขุททกนิกาย",
        "also_skip_paragraph_texts": [
            "เล่ม ๓๓ ขุททกนิกาย อปทาน ภาค ๒ พุทธวังสะ จริยาปิฎก",
        ],
    },
}


# InDesign/HTML ใน 07.html ใช้คู่ ” … „ (201D เปิด, 201E ปิด) — ต้องแยกก่อนจึงค่อยเป็น "
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
                    # CharOverride-12 มักเป็นช่องว่างหลังเลขเชิงอรรถ (CharOverride-2) ใน InDesign — ไม่สร้าง footnote ถ้าไม่มีตัวเลข
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

        if text == "สุตตันตปิฎก":
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
    cfg = PART4_DIGEST_VOLUMES[vol]
    body = fix_footnote_close_quote_before_para_end(convert_body(vol, cfg))
    body = coalesce_thai_numbered_lists(body)
    pitaka_kw = cfg.get("nikaya_keyword")
    if not pitaka_kw:
        pitaka_kw = (
            "มัชฌิมนิกาย" if cfg.get("layout") == "majjhima" else "ทีฆนิกาย"
        )
    kws = [
        "  - ภาค ๔",
        "  - ความย่อแห่งพระไตรปิฎก",
        "  - สุตตันตปิฎก",
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
    vol_choices = sorted(PART4_DIGEST_VOLUMES.keys())
    ap = argparse.ArgumentParser(
        description=f"Generate part 4 digest from 07.html (volumes {vol_choices[0]}–{vol_choices[-1]})"
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
        for v in sorted(PART4_DIGEST_VOLUMES.keys()):
            write_volume(v)
    elif args.vols:
        for v in sorted(set(args.vols)):
            write_volume(v)
    else:
        ap.print_help()
        raise SystemExit(2)


if __name__ == "__main__":
    main()
