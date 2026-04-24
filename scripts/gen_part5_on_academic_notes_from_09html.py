# -*- coding: utf-8 -*-
"""
สกัดเนื้อหา ว่าด้วยบันทึกทางวิชาการ จาก Initial_source/html5/09.html

ไฟล์ปลายทาง: docs/11-on-academic-notes/index.md
(สารบัญค้นคำอยู่ที่ docs/10-part-5-word-index/ — แยกสคริปต์ภายหลัง)

อ้างอิงแนวทางเดียวกับ gen_part4_abhidhamma_pitaka_from_08html.py:
  - อ่านช่วงบรรทัดของ 09.html (PART5_ACADEMIC_NOTES_LINE_RANGE)
  - BeautifulSoup วนทุก <p>
  - _cell_text_raw_part5: 09.html ใช้ CharOverride-2 เป็นหัว «ฉบับที่ …» ไม่ใช่เชิงอรรถ;
    CharOverride-3 = เน้นความ (**…**); CharOverride-4 = หมายเลขยก (sup)
  - normalize_quotes → polish_thai_text → convert_body_part5
  - coalesce_thai_numbered_lists, typographic_quotes_transform
  - หลังรีเจน: python scripts/ensure_ptb_heading_ids.py docs/11-on-academic-notes docs/10-part-5-word-index -r --write

ช่วง HTML: บรรทัด ๓๕–๑๓๒ ครอบคลุมเนื้อหาหลักใน _idContainer007 และเชิงอรรถ/ตารางท้าย (Paragraph-Style-3)

รัน:
  python scripts/gen_part5_on_academic_notes_from_09html.py
"""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

from ptb_coalesce_thai_numbered_lists import coalesce_thai_numbered_lists
from typographic_quotes_docs import transform as typographic_quotes_transform

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "09.html"
OUT_MD = ROOT / "docs" / "11-on-academic-notes" / "index.md"

# บรรทัด ๑ ของไฟล์ = ๑ (รวมหัวข้อซ้ำ «ว่าด้วยบันทึกทางวิชาการ» แล้วตัดด้วยสคริปต์)
PART5_ACADEMIC_NOTES_LINE_RANGE: tuple[int, int] = (35, 132)

PH_Q_OPEN = "\uf020"
PH_Q_CLOSE = "\uf021"

# ย่อหน้าที่เป็นชื่อเรื่องส่วนบน (ไม่ใช่เนื้อหาบทนี้)
SKIP_PARAGRAPH_TEXTS = frozenset(
    {
        "ภาค ๕",
        "ว่าด้วยบันทึกทางวิชาการ",
        "สารบาญค้นคำ",
        ".",
    }
)

H1_FULL = "ว่าด้วยบันทึกทางวิชาการ"
TITLE_NAV = "ว่าด้วยบันทึกทางวิชาการ"
# เติม {#…} ถาวรด้วย ensure_ptb_heading_ids.py
H1_ANCHOR_PLACEHOLDER = "p5AcNotes01"

PREV_TEXT = "เล่ม ๔๕ ปัฏฐาน ภาค ๖"
PREV_LINK = "/part-4-tipitaka-digest/abhidhamma-pitaka/vol-45"
NEXT_TEXT = "ภาค ๕ สารบัญค้นคำ"
NEXT_LINK = "/word-index/"


def normalize_quotes(t: str) -> str:
    t = t.replace("\u201d", PH_Q_OPEN)
    t = t.replace("\u201e", PH_Q_CLOSE)
    t = t.replace("\u201c", PH_Q_OPEN)
    t = t.replace("\u201a", PH_Q_CLOSE)
    return t


def finalize_quote_placeholders(t: str) -> str:
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


def polish_thai_text_before_quotes(t: str) -> str:
    t = t.replace("กัณฑ์ว่าด้วย", "กัณฑ์ ว่าด้วย")
    t = re.sub(r"([๐-๙]+)(ของ)", r"\1 \2", t)
    # อย่าแทรกช่องว่างในรูป ๑.๑ / ๒.๓ (เลขทศนิยมไทยหลังจุดเป็นตัวเลข)
    t = re.sub(
        r"^([๑-๙]+)\.([^\s])",
        lambda m: (
            m.group(0)
            if re.match(r"^[๐-๙]$", m.group(2))
            else f"{m.group(1)}. {m.group(2)}"
        ),
        t,
    )
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
    t = re.sub(r"([๐-๙]+)\.([ก-้])", r"\1. \2", t)
    return t


def polish_thai_text_after_quotes(t: str) -> str:
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


def _cell_text_raw_plain(node: Tag) -> str:
    """ดึงข้อความล้วน — ไม่แปลง CharOverride-3 เป็น ** (ใช้ลายเซ็น เชิงอรรถขอบ)."""
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            if child.name == "br":
                parts.append(" ")
            elif child.name == "a":
                continue
            else:
                parts.append(_cell_text_raw_plain(child))
        else:
            parts.append(str(child))
    return "".join(parts)


def cell_text_plain_part5(p: Tag) -> str:
    t = re.sub(r"\s+", " ", _cell_text_raw_plain(p)).strip()
    t = polish_thai_text(normalize_quotes(t))
    return _space_before_opening_bold_markdown(t)


def _cell_text_raw_part5(node: Tag) -> str:
    """09.html: ไม่แปลง CharOverride-2 เป็นเชิงอรรถ (ใช้เป็นหัวฉบับ)."""
    parts: list[str] = []
    chlist = list(node.children)
    i = 0
    while i < len(chlist):
        child = chlist[i]
        if isinstance(child, NavigableString):
            parts.append(str(child))
            i += 1
            continue
        if not isinstance(child, Tag):
            i += 1
            continue
        if child.name == "br":
            parts.append(" ")
            i += 1
            continue
        if child.name == "a":
            i += 1
            continue
        if child.name == "span":
            cls = child.get("class") or []
            if "CharOverride-3" in cls:
                bits: list[str] = [_cell_text_raw_part5(child)]
                j = i + 1
                while j < len(chlist):
                    nxt = chlist[j]
                    if isinstance(nxt, NavigableString) and not str(nxt).strip():
                        j += 1
                        continue
                    if (
                        isinstance(nxt, Tag)
                        and nxt.name == "span"
                        and "CharOverride-3" in (nxt.get("class") or [])
                    ):
                        bits.append(_cell_text_raw_part5(nxt))
                        j += 1
                        continue
                    break
                inner = re.sub(r"\s+", " ", "".join(bits)).strip()
                if inner:
                    parts.append(f"**{inner}**")
                i = j
                continue
            if "CharOverride-4" in cls:
                num = child.get_text(strip=True)
                if num:
                    parts.append(f"<sup>{num}</sup>")
                i += 1
                continue
            parts.append(_cell_text_raw_part5(child))
            i += 1
            continue
        parts.append(child.get_text())
        i += 1
    return "".join(parts)


def _space_before_opening_bold_markdown(t: str) -> str:
    """กัน 'เพราะฉะนั้น**เพื่อ' ติดกัน — ใส่ช่องว่างก่อน ** เปิดเน้น."""
    return re.sub(r"([\u0e00-\u0e7f])(\*\*[^\s*])", r"\1 \2", t)


def cell_text_part5(node: Tag) -> str:
    t = re.sub(r"\s+", " ", _cell_text_raw_part5(node))
    t = polish_thai_text(normalize_quotes(t.strip()))
    return _space_before_opening_bold_markdown(t)


def cls_set(p: Tag) -> frozenset[str]:
    return frozenset(p.get("class") or [])


def para_override_num(c: frozenset[str]) -> int | None:
    for x in c:
        m = re.fullmatch(r"ParaOverride-(\d+)", x)
        if m:
            return int(m.group(1))
    return None


_THAI_MONTH = (
    "มกราคม|กุมภาพันธ์|มีนาคม|เมษายน|พฤษภาคม|มิถุนายน|"
    "กรกฎาคม|กรกฏาคม|สิงหาคม|กันยายน|ตุลาคม|พฤศจิกายน|ธันวาคม"
)


def looks_like_standalone_date(text: str) -> bool:
    t = text.strip()
    if len(t) > 80:
        return False
    return bool(re.search(_THAI_MONTH, t)) and bool(re.search(r"[๐-๙]", t))


def is_issue_heading(text: str, c: frozenset[str], p: Tag) -> bool:
    if para_override_num(c) != 2:
        return False
    if not re.match(r"^ฉบับที่\s+[๐-๙]", text.strip()):
        return False
    # ยืนยันว่าเป็นช่องเน้นชื่อฉบับ (CharOverride-2)
    for node in p.find_all("span"):
        cl = node.get("class") or []
        if "CharOverride-2" in cl:
            return True
    return False


def emit_paragraph(md: list[str], text: str) -> None:
    md.append(f"<PtbParagraph>{text}</PtbParagraph>")
    md.append("")


def convert_body() -> str:
    start, end = PART5_ACADEMIC_NOTES_LINE_RANGE
    lines = HTML_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    chunk = "".join(lines[start - 1 : end])
    soup = BeautifulSoup(chunk, "html.parser")
    ps = soup.find_all("p")

    md: list[str] = []
    overview_done = False

    for p in ps:
        c = cls_set(p)
        po = para_override_num(c)
        if po == 5 or "Paragraph-Style-3" in c:
            text = cell_text_plain_part5(p)
        else:
            text = cell_text_part5(p)
        if not text:
            continue
        if text in SKIP_PARAGRAPH_TEXTS or text.replace(" ", "") in {
            x.replace(" ", "") for x in SKIP_PARAGRAPH_TEXTS
        }:
            continue

        if not overview_done:
            md.append("## ภาพรวม {.ptb-h-block}")
            md.append("")
            overview_done = True

        if is_issue_heading(text, c, p):
            md.append(f"## {text.strip()} {{.ptb-h-block}}")
            md.append("")
            continue

        if po == 3 and looks_like_standalone_date(text):
            md.append(f'<p class="ptb-paragraph-left-align ptb-text-sm">{text}</p>')
            md.append("")
            continue

        if po == 5 and looks_like_standalone_date(text):
            md.append(f'<p class="ptb-paragraph-left-align ptb-text-sm">{text}</p>')
            md.append("")
            continue

        if po == 5 and not looks_like_standalone_date(text) and len(text) < 120:
            md.append(f'<p class="ptb-paragraph-right-align"><strong>{text}</strong></p>')
            md.append("")
            continue

        if "Paragraph-Style-3" in c:
            md.append(f'<p class="ptb-paragraph-left-align ptb-text-sm">{text}</p>')
            md.append("")
            continue

        emit_paragraph(md, text)

    return "\n".join(md).rstrip() + "\n"


def fix_footnote_close_quote_before_para_end(body: str) -> str:
    return re.sub(
        r"</PtbFootnote>\s+\"</PtbParagraph>",
        r'</PtbFootnote>"</PtbParagraph>',
        body,
    )


def write_markdown() -> None:
    body = fix_footnote_close_quote_before_para_end(convert_body())
    body = coalesce_thai_numbered_lists(body)
    kw_block = "\n".join(
        [
            "  - ภาค ๕",
            "  - บันทึกทางวิชาการ",
            "  - พระไตรปิฎกฉบับสำหรับประชาชน",
        ]
    )
    fm = f"""---
title: {TITLE_NAV}
lang: th
description: บันทึกทางวิชาการ — พระไตรปิฎกฉบับสำหรับประชาชน (ภาค ๕)
outline: [2, 6]
prev: {{ text: '{PREV_TEXT}', link: '{PREV_LINK}' }}
next: {{ text: '{NEXT_TEXT}', link: '{NEXT_LINK}' }}
searchKeywords:
{kw_block}
---

# {H1_FULL} {{#{H1_ANCHOR_PLACEHOLDER} .ptb-h-block}}

"""
    full = fm + body
    full, _n_typo = typographic_quotes_transform(full)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(full, encoding="utf-8")
    print(f"Wrote {OUT_MD} (typographic quotes: {_n_typo} pair(s))")


def main() -> None:
    if not HTML_PATH.is_file():
        raise SystemExit(f"Missing source HTML: {HTML_PATH}")
    write_markdown()


if __name__ == "__main__":
    main()
