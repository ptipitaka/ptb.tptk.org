# -*- coding: utf-8 -*-
"""
แปลง Initial_source/html5/06.html ช่วงความย่อ เล่ม ๑ มหาวิภังค์ ภาค ๑
→ docs/09-part-4-tipitaka-digest/vinaya-pitaka/vol-01.md

หมายเหตุ: ไฟล์จริงใน repo มักมีโครง h4/h5 จากขั้นตอนอื่น — หลังแก้เนื้อหาให้รัน
`python scripts/reanchor_vinaya_vol01.py` เพื่อให้ `{#id}` ตรงกฎภาค ๔ (ดู ptb-content-guide.mdc)
"""
from __future__ import annotations

import html as html_module
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "06.html"
OUT_PATH = ROOT / "docs" / "09-part-4-tipitaka-digest" / "vinaya-pitaka" / "vol-01.md"

START_MARKER = (
    '<p class="Paragraph-Style-2 ParaOverride-2">'
    '<span class="Character-Style-2">เล่ม ๑ มหาวิภังค์ ภาค ๑</span></p>'
)
END_MARKER = "จบความย่อแห่งพระไตรปิฎก เล่ม ๑"


def inner_html(p_html: str) -> str:
    m = re.search(r">(.*)</p>\s*$", p_html, re.DOTALL)
    return m.group(1) if m else ""


def p_class(p_html: str) -> str:
    m = re.search(r'class="([^"]*)"', p_html)
    return m.group(1) if m else ""


def split_ps(chunk: str) -> list[str]:
    return re.findall(r"<p\s+[^>]*>.*?</p>", chunk, flags=re.DOTALL)


def strip_vol01(fragment: str) -> str:
    fragment = fragment.replace("\r\n", "\n").replace("\r", "\n")
    fragment = re.sub(r'<a\s[^>]*id="[^"]+"\s*></a>', "", fragment)

    def walk(s: str) -> str:
        out: list[str] = []
        pos = 0
        while pos < len(s):
            if s.startswith("<br", pos):
                gt = s.find(">", pos)
                out.append(" ")
                pos = gt + 1 if gt != -1 else len(s)
                continue
            if s.startswith("<span", pos):
                m = re.match(r"<span\s+[^>]*>", s[pos:])
                if not m:
                    pos += 1
                    continue
                open_end = pos + len(m.group(0))
                tag = m.group(0)
                depth = 1
                scan = open_end
                while depth and scan < len(s):
                    nxt_open = s.find("<span", scan)
                    nxt_close = s.find("</span>", scan)
                    if nxt_close == -1:
                        break
                    if nxt_open != -1 and nxt_open < nxt_close:
                        depth += 1
                        scan = nxt_open + 5
                    else:
                        depth -= 1
                        if depth == 0:
                            inner = s[open_end:nxt_close]
                            if "CharOverride-2" in tag:
                                note = walk(inner).strip()
                                if note:
                                    out.append(f"<PtbFootnote>เชิงอรรถ {note} ม.พ.ป.</PtbFootnote>")
                            elif "CharOverride-4" in tag and "CharOverride-1" in tag:
                                out.append("**" + walk(inner) + "**")
                            else:
                                out.append(walk(inner))
                            pos = nxt_close + len("</span>")
                            break
                        scan = nxt_close + 7
                continue
            if s.startswith("<a ", pos):
                close = s.find("</a>", pos)
                if close == -1:
                    pos += 1
                    continue
                gt = s.find(">", pos)
                inner_a = s[gt + 1 : close] if gt != -1 else ""
                out.append(walk(inner_a))
                pos = close + 4
                continue
            nxt = s.find("<", pos)
            raw = s[pos : len(s) if nxt == -1 else nxt]
            out.append(html_module.unescape(raw))
            pos = len(s) if nxt == -1 else nxt
        return "".join(out)

    text = walk(fragment)
    text = text.replace("\t", " ")
    text = re.sub(r" +", " ", text)
    text = text.replace("„", '"').replace("”", '"')
    return text.strip()


def slug_heading(text: str, prefix: str, seq: list[int]) -> str:
    seq[0] += 1
    base = re.sub(r"[^\u0e00-\u0e7fa-zA-Z0-9]+", "-", text.lower())
    base = re.sub(r"-+", "-", base).strip("-")[:56] or f"h{seq[0]}"
    return f"{prefix}-{seq[0]}-{base}"


def convert() -> str:
    html = HTML_PATH.read_text(encoding="utf-8")
    start = html.find(START_MARKER)
    if start == -1:
        raise SystemExit("ไม่พบจุดเริ่มเล่ม ๑ มหาวิภังค์ ภาค ๑")
    start += len(START_MARKER)
    end = html.find(END_MARKER, start)
    if end == -1:
        raise SystemExit("ไม่พบจุดจบความย่อเล่ม ๑")
    chunk = html[start:end]
    ps = split_ps(chunk)

    lines: list[str] = []
    anchor_seq = [0]

    for p_html in ps:
        cls = p_class(p_html)
        inner = inner_html(p_html)
        if not inner.strip():
            continue

        if "Paragraph-Style-2" in cls and "Character-Style-2" in inner:
            text = strip_vol01(inner)
            if not text or text == ".":
                continue
            aid = slug_heading(text, "ptb-v1", anchor_seq)
            lines.append(f"## {text} {{#{aid} .ptb-dh2 .ptb-h-block}}")
            lines.append("")
            continue

        if "Paragraph-Style-4" in cls:
            text = strip_vol01(inner)
            if not text:
                continue
            if "ParaOverride-6" in cls:
                lines.append(f'<p class="ptb-subtitle">{text}</p>')
                lines.append("")
                continue
            aid = slug_heading(text, "ptb-v1", anchor_seq)
            lines.append(f"### {text} {{#{aid} .ptb-dh3 .ptb-h-block}}")
            lines.append("")
            continue

        if "Paragraph-Style-1" in cls:
            text = strip_vol01(inner)
            if not text:
                continue
            lines.append(f"<PtbParagraph>{text}</PtbParagraph>")
            lines.append("")
            continue

        text = strip_vol01(inner)
        if text:
            lines.append(f"<PtbParagraph>{text}</PtbParagraph>")
            lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


FRONT = """---
title: เล่ม ๑ มหาวิภังค์ ภาค ๑
lang: th
description: ความย่อแห่งพระไตรปิฎก — เล่ม ๑ มหาวิภังค์ ภาค ๑
outline: [2, 6]
prev: { text: 'แผนภูมิวินัยปิฎก', link: '/part-4-tipitaka-digest/vinaya-pitaka/vinaya-structure' }
next: { text: 'เล่ม ๒ มหาวิภังค์ ภาค ๒', link: '/part-4-tipitaka-digest/vinaya-pitaka/vol-02' }
searchKeywords:
  - ภาค ๔
  - ความย่อแห่งพระไตรปิฎก
  - เล่ม ๑
  - วินัยปิฎก
  - มหาวิภังค์
  - ภิกขุวิภังค์
  - เวรัญชกัณฑ์
  - ปาราชิก
  - ปฐมปาราชิกกัณฑ์
  - ทุติยปาราชิกกัณฑ์
  - ตติยปาราชิกกัณฑ์
  - จตุตถปาราชิกกัณฑ์
  - เตรสกัณฑ์
  - สังฆาทิเสส
  - อนิยตกัณฑ์
  - อนิยต
  - พระสาริบุตร
  - พระเทวทัต
  - สุทินนะ
  - ปาฏิโมกข์
  - สิกขาบท
---

# เล่ม ๑ มหาวิภังค์ ภาค ๑ {.ptb-dh1 .ptb-h-block}

"""


def main() -> None:
    body = convert()
    OUT_PATH.write_text(FRONT + body, encoding="utf-8")
    print("Wrote", OUT_PATH, "chars", len(FRONT + body))


if __name__ == "__main__":
    main()
