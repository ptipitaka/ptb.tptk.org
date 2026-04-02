# -*- coding: utf-8 -*-
"""
สกัดความย่อวินัยปิฎก เล่ม ๓–๘ จาก Initial_source/html5/06.html
→ docs/09-part-4-tipitaka-digest/vinaya-pitaka/vol-0N.md

อิงรูปแบบจาก gen_vol02_from_06html.py แต่ครอบคลุม ParaOverride หลายแบบในเล่ม ๔–๘
และใช้เฉพาะ .ptb-h-block (ไม่ใส่ .ptb-dh*) ตาม ptb-content-guide
"""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "06.html"
OUT_DIR = ROOT / "docs" / "09-part-4-tipitaka-digest" / "vinaya-pitaka"

# (vol, start_line, end_line) — end รวมบรรทัดสุดท้ายของเนื้อหา (ก่อนบรรทัด "จบความย่อ...")
VOLUME_RANGES: list[tuple[int, int, int]] = [
    (3, 1563, 2356),
    (4, 2371, 2742),
    (5, 3140, 3366),
    (6, 3671, 3871),
    (7, 4071, 4454),
    (8, 4894, 4944),
]

VOL_META: dict[int, dict[str, str]] = {
    3: {
        "h1": "เล่ม ๓ ภิกขุนีวิภังค์",
        "title": "เล่ม ๓ ภิกขุนีวิภังค์",
        "desc": "ความย่อแห่งพระไตรปิฎก — เล่ม ๓ ภิกขุนีวิภังค์",
    },
    4: {
        "h1": "เล่ม ๔ มหาวัคค์ ภาค ๑",
        "title": "เล่ม ๔ มหาวัคค์ ภาค ๑",
        "desc": "ความย่อแห่งพระไตรปิฎก — เล่ม ๔ มหาวัคค์ ภาค ๑",
    },
    5: {
        "h1": "เล่ม ๕ มหาวัคค์ ภาค ๒",
        "title": "เล่ม ๕ มหาวัคค์ ภาค ๒",
        "desc": "ความย่อแห่งพระไตรปิฎก — เล่ม ๕ มหาวัคค์ ภาค ๒",
    },
    6: {
        "h1": "เล่ม ๖ จุลลวัคค์ ภาค ๑",
        "title": "เล่ม ๖ จุลลวัคค์ ภาค ๑",
        "desc": "ความย่อแห่งพระไตรปิฎก — เล่ม ๖ จุลลวัคค์ ภาค ๑",
    },
    7: {
        "h1": "เล่ม ๗ จุลลวัคค์ ภาค ๒",
        "title": "เล่ม ๗ จุลลวัคค์ ภาค ๒",
        "desc": "ความย่อแห่งพระไตรปิฎก — เล่ม ๗ จุลลวัคค์ ภาค ๒",
    },
    8: {
        "h1": "เล่ม ๘ ปริวาร",
        "title": "เล่ม ๘ ปริวาร",
        "desc": "ความย่อแห่งพระไตรปิฎก — เล่ม ๘ ปริวาร",
    },
}


def thai_slug(s: str, max_len: int = 48) -> str:
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"[^\u0e00-\u0e7fa-zA-Z0-9\-๑-๙]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or "sec"


def normalize_quotes(t: str) -> str:
    return t.replace("„", '"').replace("\u201c", '"').replace("\u201d", '"')


def split_trailing_paren_subtitle(text: str) -> tuple[str, str | None]:
    m = re.search(r"\s+(\([^)]{2,500}\))\s*$", text)
    if not m:
        return text, None
    return text[: m.start()].strip(), m.group(1).strip()


def split_first_line_subtitle(text: str) -> tuple[str, str | None]:
    """แยกบรรทัดแรก / บรรทัดหลัง เช่น ๑. กัณฑ์ ... \\n (ว่าด้วย...)"""
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
    t = re.sub(r"ว่า\"", "ว่า \"", t)
    t = re.sub(r'"\s*([ก-๙])', r'" \1', t)
    t = re.sub(r"^([๑-๙]+)\.([^\s])", r"\1. \2", t)
    t = re.sub(r"(\([๑-๔]\))([ก-๙])", r"\1 \2", t)
    t = re.sub(r"สิกขาบทที่ (๑๐|[๑-๙])(ห้าม|ให้)", r"สิกขาบทที่ \1 \2", t)
    t = re.sub(r"สิกขาบทที่ (๑๐|[๑-๙])(ภิกษุ)", r"สิกขาบทที่ \1 \2", t)
    t = re.sub(r" ณ([ก-๙])", r" ณ \1", t)
    t = re.sub(r"ประทับ ณ([ก-๙])", r"ประทับ ณ \1", t)
    t = re.sub(r"ประทับณ\s", "ประทับ ณ ", t)
    t = re.sub(r"เชตวนารามสมัย", "เชตวนาราม สมัย", t)
    t = re.sub(r"เชตวนาราม([ก-ฮ])", r"เชตวนาราม \1", t)
    t = re.sub(r"อดีตภริยา", "อดีต ภริยา", t)
    t = re.sub(r"(?<=[\u0e00-\u0e7f])\)([ก-ฮ])", r") \1", t)
    t = re.sub(
        r"<PtbFootnote>([^<]+)</PtbFootnote>\s*\(",
        r"<PtbFootnote>\1</PtbFootnote> (",
        t,
    )
    t = re.sub(r"</PtbFootnote>([ก-ฮ])", r"</PtbFootnote> \1", t)
    m = re.match(r"^([๑-๙])(.+)$", t)
    if m:
        d, rest = m.group(1), m.group(2)
        if rest and rest[0] not in "๐๑๒๓๔๕๖๗๘๙. ":
            if "\u0e00" <= rest[0] <= "\u0e7f":
                t = f"{d} {rest}"
    return t


def p_has_span_class(p: Tag, class_name: str) -> bool:
    for sp in p.find_all("span"):
        if class_name in (sp.get("class") or []):
            return True
    return False


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


def is_volume_title_text(vol: int, text: str) -> bool:
    h1 = VOL_META[vol]["h1"].replace(" ", "")
    t = re.sub(r"\s+", "", text)
    return t == h1 or VOL_META[vol]["h1"] in text and len(text) < 80


def nav_prev_next(vol: int) -> tuple[dict[str, str], dict[str, str]]:
    base = "/part-4-tipitaka-digest/vinaya-pitaka"
    chain = [
        ("เล่ม ๒ มหาวิภังค์ ภาค ๒", f"{base}/vol-02"),
        ("เล่ม ๓ ภิกขุนีวิภังค์", f"{base}/vol-03"),
        ("เล่ม ๔ มหาวัคค์ ภาค ๑", f"{base}/vol-04"),
        ("เล่ม ๕ มหาวัคค์ ภาค ๒", f"{base}/vol-05"),
        ("เล่ม ๖ จุลลวัคค์ ภาค ๑", f"{base}/vol-06"),
        ("เล่ม ๗ จุลลวัคค์ ภาค ๒", f"{base}/vol-07"),
        ("เล่ม ๘ ปริวาร", f"{base}/vol-08"),
    ]
    i = vol - 2  # vol 3 → index 1
    prev = {"text": chain[i - 1][0], "link": chain[i - 1][1]}
    if vol == 8:
        nxt = {
            "text": "เล่ม ๙ ทีฆนิกาย ภาค ๑",
            "link": "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-09",
        }
    else:
        nxt = {"text": chain[i + 1][0], "link": chain[i + 1][1]}
    return prev, nxt


def convert_volume(vol: int, start_line: int, end_line: int) -> str:
    lines = HTML_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    chunk = "".join(lines[start_line - 1 : end_line])
    soup = BeautifulSoup(chunk, "html.parser")
    ps = soup.find_all("p")

    md: list[str] = []
    h2c = h3c = h4c = h5c = 0
    prefix = f"ptb-v{vol}"
    skip_title = VOL_META[vol]["h1"]
    i = 0

    while i < len(ps):
        p = ps[i]
        c = cls_set(p)
        po = para_override_num(c)
        text = cell_text_with_footnotes(p)
        if not text:
            i += 1
            continue
        if is_volume_title_text(vol, text) or text == skip_title:
            i += 1
            continue

        # --- หัวข้อ ---
        if "Paragraph-Style-4" in c and po == 13:
            h2c += 1
            ts = text.strip()
            if ts == "ขยายความ":
                aid = f"v{vol}-elaboration"
            elif ts == "ภาพรวม":
                aid = f"v{vol}-overview"
            else:
                aid = f"{prefix}-h2-{h2c}-{thai_slug(text, 40)}"
            md.append(f"## {text} {{#{aid} .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and po == 6:
            h3c += 1
            title, sub = split_first_line_subtitle(text)
            if sub is None:
                title, sub = split_trailing_paren_subtitle(title)
            aid = f"{prefix}-h3-{h3c}-{thai_slug(title, 44)}"
            if sub:
                md.append(f"### {title} {{#{aid} .ptb-h-block}}")
                md.append("")
                md.append(f'<p class="ptb-subtitle">{sub}</p>')
            else:
                md.append(f"### {title} {{#{aid} .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and po == 5:
            h3c += 1
            title, sub = split_first_line_subtitle(text)
            if sub is None:
                title, sub = split_trailing_paren_subtitle(title)
            aid = f"{prefix}-h3-{h3c}-{thai_slug(title, 44)}"
            if sub:
                md.append(f"### {title} {{#{aid} .ptb-h-block}}")
                md.append("")
                md.append(f'<p class="ptb-subtitle">{sub}</p>')
            else:
                md.append(f"### {title} {{#{aid} .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and po == 22:
            h4c += 1
            aid = f"{prefix}-h4-{h4c}-{thai_slug(text, 44)}"
            md.append(f"#### {text} {{#{aid} .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and po == 7:
            if "สิกขาบทที่" in text:
                h5c += 1
                aid = f"{prefix}-h5-{h5c}-{thai_slug(text, 44)}"
                md.append(f"##### {text} {{#{aid} .ptb-h-block}}")
            else:
                h4c += 1
                aid = f"{prefix}-h4-{h4c}-{thai_slug(text, 44)}"
                md.append(f"#### {text} {{#{aid} .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and po == 18:
            md.append(f"<PtbParagraph>{text}</PtbParagraph>")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and po == 15 and p_has_span_class(p, "CharOverride-3"):
            md.append(f"#### {text} {{#{prefix}-end-{thai_slug(text, 28)} .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-1" in c and po in (14, 9, 16, 11):
            h4c += 1
            aid = f"{prefix}-h4-{h4c}-{thai_slug(text, 44)}"
            md.append(f"#### {text} {{#{aid} .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-1" in c and po in (10, 19, 20, 25, 27, 31):
            md.append(f'<p class="ptb-paragraph-no-indent">{text}</p>')
            md.append("")
            i += 1
            continue

        md.append(f"<PtbParagraph>{text}</PtbParagraph>")
        md.append("")
        i += 1

    return "\n".join(md).rstrip() + "\n"


def write_volume(vol: int, start_line: int, end_line: int) -> None:
    meta = VOL_META[vol]
    prev, nxt = nav_prev_next(vol)
    body = convert_volume(vol, start_line, end_line)
    fm = f"""---
title: {meta["title"]}
lang: th
description: {meta["desc"]}
outline: [2, 6]
prev: {{ text: '{prev["text"]}', link: '{prev["link"]}' }}
next: {{ text: '{nxt["text"]}', link: '{nxt["link"]}' }}
searchKeywords:
  - ภาค ๔
  - ความย่อแห่งพระไตรปิฎก
  - วินัยปิฎก
---

# {meta["h1"]} {{.ptb-h-block}}

"""
    out = OUT_DIR / f"vol-{vol:02d}.md"
    out.write_text(fm + body, encoding="utf-8")
    print(f"Wrote {out}")


def main() -> None:
    for vol, s, e in VOLUME_RANGES:
        write_volume(vol, s, e)


if __name__ == "__main__":
    main()
