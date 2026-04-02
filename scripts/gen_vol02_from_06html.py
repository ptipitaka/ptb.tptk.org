# -*- coding: utf-8 -*-
"""Extract เล่ม ๒ มหาวิภังค์ ภาค ๒ from Initial_source/html5/06.html → vol-02.md."""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "06.html"
OUT_PATH = ROOT / "docs" / "09-part-4-tipitaka-digest" / "vinaya-pitaka" / "vol-02.md"

START_LINE = 676
END_LINE = 1055


def thai_slug(s: str, max_len: int = 48) -> str:
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"[^\u0e00-\u0e7fa-zA-Z0-9\-๑-๙]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or "sec"


def normalize_quotes(t: str) -> str:
    return t.replace("„", '"').replace('"', '"')


def split_trailing_paren_subtitle(text: str) -> tuple[str, str | None]:
    m = re.search(r"\s+(\([^)]{2,400}\))\s*$", text)
    if not m:
        return text, None
    return text[: m.start()].strip(), m.group(1).strip()


def polish_thai_text(t: str) -> str:
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
    # หลังวงเล็บปิดต่อทันทีด้วยพยัญชนะไทย (เช่น …สังฆาฏิ)ภิกษุ)
    t = re.sub(r"(?<=[\u0e00-\u0e7f])\)([ก-ฮ])", r") \1", t)
    t = re.sub(
        r"<PtbFootnote>([^<]+)</PtbFootnote>\s*\(",
        r"<PtbFootnote>\1</PtbFootnote> (",
        t,
    )
    t = re.sub(
        r"</PtbFootnote>([ก-ฮ])",
        r"</PtbFootnote> \1",
        t,
    )
    # เลขนำหน้าหัวข้อ ๑–๙ ต่อทันทีด้วยพยัญชนะ (แท็บหายระหว่าง span ใน HTML)
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
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n+", " ", t)
    return polish_thai_text(normalize_quotes(t.strip()))


def cls_set(p: Tag) -> frozenset[str]:
    return frozenset(p.get("class") or [])


def main() -> None:
    lines = HTML_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    chunk = "".join(lines[START_LINE - 1 : END_LINE])
    soup = BeautifulSoup(chunk, "html.parser")
    ps = soup.find_all("p")

    md: list[str] = []
    h2c = h3c = h4c = 0
    i = 0

    while i < len(ps):
        p = ps[i]
        c = cls_set(p)
        text = cell_text_with_footnotes(p)
        if not text or text == "เล่ม ๒ มหาวิภังค์ ภาค ๒":
            i += 1
            continue

        # Merge ๓./๔. กัณฑ์ title + subtitle on next line
        if (
            "Paragraph-Style-4" in c
            and "ParaOverride-5" in c
            and re.match(r"^[๓๔]\.\s*\S+กัณฑ์$", text)
            and i + 1 < len(ps)
        ):
            nxt = ps[i + 1]
            t2 = cell_text_with_footnotes(nxt)
            if t2.startswith("("):
                h3c += 1
                aid = f"ptb-v2-h3-{h3c}-{thai_slug(text, 36)}"
                md.append(f"### {text} {{#{aid} .ptb-dh3 .ptb-h-block}}")
                md.append("")
                md.append(f'<p class="ptb-subtitle">{t2}</p>')
                md.append("")
                i += 2
                continue

        if "Paragraph-Style-4" in c and "ParaOverride-13" in c:
            h2c += 1
            ts = text.strip()
            if ts == "ขยายความ":
                aid = "v2-elaboration"
            elif ts == "ภาพรวม":
                aid = "v2-overview"
            else:
                aid = f"ptb-v2-h2-{h2c}-{thai_slug(text, 40)}"
            md.append(f"## {text} {{#{aid} .ptb-dh2 .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        # เสขิยหมวดย่อย (๑)สารูป (๒)โภชน์ …
        if "Paragraph-Style-4" in c and "ParaOverride-18" in c:
            h3c += 1
            aid = f"ptb-v2-h3-{h3c}-{thai_slug(text, 44)}"
            md.append(f"### {text} {{#{aid} .ptb-dh3 .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if (
            "Paragraph-Style-4" in c
            and "ParaOverride-6" in c
            and p_has_span_class(p, "CharOverride-3")
        ):
            h3c += 1
            aid = f"ptb-v2-h3-{h3c}-{thai_slug(text, 44)}"
            md.append(f"### {text} {{#{aid} .ptb-dh3 .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        # ๑. นิสสัคคิยกัณฑ์ / ๒. ปาจิตติยกัณฑ์ / ๕. ธรรม… (ParaOverride-6, ไม่ใช่หมวดเสขิย)
        if "Paragraph-Style-4" in c and "ParaOverride-6" in c:
            h3c += 1
            title, sub = split_trailing_paren_subtitle(text)
            aid = f"ptb-v2-h3-{h3c}-{thai_slug(title, 44)}"
            if sub:
                md.append(f"### {title} {{#{aid} .ptb-dh3 .ptb-h-block}}")
                md.append("")
                md.append(f'<p class="ptb-subtitle">{sub}</p>')
            else:
                md.append(f"### {title} {{#{aid} .ptb-dh3 .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and "ParaOverride-7" in c:
            h4c += 1
            aid = f"ptb-v2-h4-{h4c}-{thai_slug(text, 44)}"
            md.append(f"#### {text} {{#{aid} .ptb-dh4 .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and "ParaOverride-5" in c:
            h4c += 1
            aid = f"ptb-v2-h4-{h4c}-{thai_slug(text, 44)}"
            md.append(f"#### {text} {{#{aid} .ptb-dh4 .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-4" in c and "ParaOverride-15" in c and p_has_span_class(
            p, "CharOverride-3"
        ):
            md.append(
                f"#### {text} {{#ptb-v2-end-{thai_slug(text, 28)} .ptb-dh4 .ptb-h-block}}"
            )
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-1" in c and (
            "ParaOverride-14" in c
            or "ParaOverride-9" in c
            or "ParaOverride-16" in c
        ):
            h4c += 1
            aid = f"ptb-v2-h4-{h4c}-{thai_slug(text, 44)}"
            md.append(f"#### {text} {{#{aid} .ptb-dh4 .ptb-h-block}}")
            md.append("")
            i += 1
            continue

        if "Paragraph-Style-1" in c and (
            "ParaOverride-10" in c
            or "ParaOverride-19" in c
            or "ParaOverride-20" in c
        ):
            md.append(f'<p class="ptb-paragraph-no-indent">{text}</p>')
            md.append("")
            i += 1
            continue

        md.append(f"<PtbParagraph>{text}</PtbParagraph>")
        md.append("")
        i += 1

    body = "\n".join(md).rstrip() + "\n"

    frontmatter = """---
title: เล่ม ๒ มหาวิภังค์ ภาค ๒
lang: th
description: ความย่อแห่งพระไตรปิฎก — เล่ม ๒ มหาวิภังค์ ภาค ๒
outline: [2, 6]
prev: { text: 'เล่ม ๑ มหาวิภังค์ ภาค ๑', link: '/part-4-tipitaka-digest/vinaya-pitaka/vol-01' }
next: { text: 'เล่ม ๓ ภิกขุนีวิภังค์', link: '/part-4-tipitaka-digest/vinaya-pitaka/vol-03' }
searchKeywords:
  - ภาค ๔
  - ความย่อแห่งพระไตรปิฎก
---

# เล่ม ๒ มหาวิภังค์ ภาค ๒ {.ptb-dh1 .ptb-h-block}

"""
    OUT_PATH.write_text(frontmatter + body, encoding="utf-8")
    print(f"Wrote {OUT_PATH}, paragraphs out: {len(md)//2}")


if __name__ == "__main__":
    main()
