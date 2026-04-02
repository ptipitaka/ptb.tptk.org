# -*- coding: utf-8 -*-
"""
สกัดความย่อ เล่ม ๙ ทีฆนิกาย สีลขันธวัคค์ จาก Initial_source/html5/07.html
บรรทัด 240–620 (จนถึงบรรทัด "จบความย่อแห่งพระไตรปิฎก เล่ม ๙" — ไม่รวมเชิงอรรถท้ายเล่มที่แทรกระหว่างหน้า PDF)

รัน: python scripts/gen_part4_digha_vol09_from_07html.py
(แนะนำใช้ scripts/gen_part4_sutta_pitaka_from_07html.py --vol 9 แทน — สคริปต์นี้คงไว้เพื่ออ้างอิง)

หลังรัน: python scripts/ensure_ptb_heading_ids.py docs -r --write
"""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "07.html"
OUT_PATH = ROOT / "docs" / "09-part-4-tipitaka-digest" / "sutta-pitaka" / "digha-nikaya" / "vol-09.md"

# บรรทัด 1-based ใน 07.html
START_LINE = 240
END_LINE = 620

H1_FULL = "เล่ม ๙ ทีฆนิกาย สีลขันธวัคค์"
TITLE_NAV = "เล่ม ๙ สีลขันธวัคค์"
H1_ANCHOR = "sjoTRI4HWs"


def normalize_quotes(t: str) -> str:
    return t.replace("„", '"').replace("\u201c", '"').replace("\u201d", '"')


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


def polish_thai_text(t: str) -> str:
    t = t.replace("กัณฑ์ว่าด้วย", "กัณฑ์ ว่าด้วย")
    t = re.sub(r"([๐-๙]+)(ของ)", r"\1 \2", t)
    t = re.sub(r'ว่า"', 'ว่า "', t)
    t = re.sub(r'"\s*([ก-๙])', r'" \1', t)
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
    t = re.sub(r"ว่าด้วย\"", 'ว่าด้วย "', t)
    t = re.sub(r"และว่าด้วย\"", 'และว่าด้วย "', t)
    t = re.sub(r"ตรัสว่า\"", 'ตรัสว่า "', t)
    t = re.sub(r"([ก-๙])\"([ก-้])", r'\1" \2', t)
    t = re.sub(r'ว่า "\s+', 'ว่า "', t)
    t = re.sub(r'และว่าด้วย "\s+', 'และว่าด้วย "', t)
    t = re.sub(r'ว่าด้วย "\s+', 'ว่าด้วย "', t)
    t = re.sub(r'ตรัสว่า "\s+', 'ตรัสว่า "', t)
    t = re.sub(r"นาฬันทามี", "นาฬันทา มี", t)
    t = re.sub(r"มหาปทานสูตรจึง", "มหาปทานสูตร จึง", t)
    t = re.sub(r"เดือน ๑๒พระ", "เดือน ๑๒ พระ", t)
    t = re.sub(r"ปาฏิกสูตรจึง", "ปาฏิกสูตร จึง", t)
    return t


def cell_text_with_footnotes(node: Tag) -> str:
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
                    parts.append(cell_text_with_footnotes(child))
            else:
                parts.append(child.get_text())
    t = "".join(parts)
    t = re.sub(r"\s+", " ", t)
    return polish_thai_text(normalize_quotes(t.strip()))


def cls_set(p: Tag) -> frozenset[str]:
    return frozenset(p.get("class") or [])


def para_override_num(c: frozenset[str]) -> int | None:
    for x in c:
        m = re.fullmatch(r"ParaOverride-(\d+)", x)
        if m:
            return int(m.group(1))
    return None


def convert_body() -> str:
    lines = HTML_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    chunk = "".join(lines[START_LINE - 1 : END_LINE])
    soup = BeautifulSoup(chunk, "html.parser")
    ps = soup.find_all("p")

    md: list[str] = []
    overview_done = False
    i = 0

    while i < len(ps):
        p = ps[i]
        c = cls_set(p)
        po = para_override_num(c)
        text = cell_text_with_footnotes(p)
        if not text:
            i += 1
            continue

        if text == "สุตตันตปิฎก":
            i += 1
            continue
        if text == H1_FULL or text.replace(" ", "") == H1_FULL.replace(" ", ""):
            i += 1
            continue

        if not overview_done:
            md.append("## ภาพรวม {.ptb-h-block}")
            md.append("")
            overview_done = True

        if "Paragraph-Style-4" in c and po == 6:
            if text.strip() == "ขยายความ":
                md.append("## ขยายความ {.ptb-h-block}")
            else:
                md.append(f"## {text} {{.ptb-h-block}}")
            md.append("")
            i += 1
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
            i += 1
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
            i += 1
            continue

        if "Paragraph-Style-4" in c and po == 8:
            md.append(f"#### {text} {{.ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and po is None:
            md.append(f"#### {text} {{.ptb-h-block}}")
            md.append("")
            i += 1
            continue

        md.append(f"<PtbParagraph>{text}</PtbParagraph>")
        md.append("")
        i += 1

    return "\n".join(md).rstrip() + "\n"


def fix_footnote_close_quote_before_para_end(body: str) -> str:
    return re.sub(
        r"</PtbFootnote>\s+\"</PtbParagraph>",
        r'</PtbFootnote>"</PtbParagraph>',
        body,
    )


def main() -> None:
    body = fix_footnote_close_quote_before_para_end(convert_body())
    fm = f"""---
title: {TITLE_NAV}
lang: th
description: ความย่อแห่งพระไตรปิฎก — {H1_FULL}
outline: [2, 6]
prev: {{ text: 'เล่ม ๘ ปริวาร', link: '/part-4-tipitaka-digest/vinaya-pitaka/vol-08' }}
next: {{ text: 'เล่ม ๑๐ มหาวัคค์', link: '/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-10' }}
searchKeywords:
  - ภาค ๔
  - ความย่อแห่งพระไตรปิฎก
  - สุตตันตปิฎก
  - ทีฆนิกาย
  - สีลขันธวัคค์
---

# {H1_FULL} {{#{H1_ANCHOR} .ptb-h-block}}

"""
    OUT_PATH.write_text(fm + body, encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
