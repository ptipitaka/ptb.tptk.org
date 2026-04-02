# -*- coding: utf-8 -*-
"""Generate docs/07-part-2-historical-documents/*.md from Initial_source/html5/04.html."""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "04.html"
OUT_DIR = ROOT / "docs" / "07-part-2-historical-documents"
IMG_BASE = "/images/07-part-2-historical-documents/section-1"


def norm_text(s: str) -> str:
    s = s.replace("\u00a0", " ").replace("\t", " ")
    s = re.sub(r"[ \n\r]+", " ", s)
    return s.strip()


def p_plain(p: Tag) -> str:
    parts = []
    for span in p.find_all("span", recursive=False):
        parts.append(span.get_text())
    if not parts:
        return norm_text(p.get_text())
    return norm_text("".join(parts))


def p_ledger_raw(p: Tag) -> str:
    """Preserve spacing for account-style lines (tabs → spaces)."""
    t = p.get_text()
    t = t.replace("\u00a0", " ").replace("\t", "    ")
    t = re.sub(r"\s+\n\s*", "\n", t)
    return t.strip()


def is_title_p(p: Tag) -> bool:
    return "Paragraph-Style-2" in " ".join(p.get("class") or [])


def collect_ps(div: Tag | None) -> list[str]:
    if div is None:
        return []
    return [p_plain(p) for p in div.find_all("p", recursive=True)]


def gather_imgs_after(body: Tag, start_id: str, stop_id: str) -> list[str]:
    imgs: list[str] = []
    collecting = False
    for el in body.descendants:
        if not isinstance(el, Tag):
            continue
        if el.name == "div" and el.get("id") == start_id:
            collecting = True
            continue
        if el.name == "div" and el.get("id") == stop_id:
            break
        if collecting and el.name == "img":
            src = el.get("src", "")
            if "/image/" in src:
                imgs.append(src.split("/")[-1])
    return imgs


def collapse_section1_merged_pairs(imgs: list[str]) -> list[str]:
    """รวมคู่ภาพที่เป็นหน้าเดียวกัน: A4-02-002+A4-02-0021, A4-04+A4-041."""
    out: list[str] = []
    i = 0
    while i < len(imgs):
        if (
            i + 1 < len(imgs)
            and imgs[i] == "A4-02-002.jpg"
            and imgs[i + 1] == "A4-02-0021.jpg"
        ):
            out.append("A4-02-002-0021.jpg")
            i += 2
        elif (
            i + 1 < len(imgs)
            and imgs[i] == "A4-04.jpg"
            and imgs[i + 1] == "A4-041.jpg"
        ):
            out.append("A4-04-041.jpg")
            i += 2
        else:
            out.append(imgs[i])
            i += 1
    return out


def main() -> None:
    soup = BeautifulSoup(HTML_PATH.read_text(encoding="utf-8"), "html.parser")
    body = soup.body
    assert body

    c001 = soup.find("div", id="_idContainer001")
    c003 = soup.find("div", id="_idContainer003")
    c004 = soup.find("div", id="_idContainer004")
    c006 = soup.find("div", id="_idContainer006")
    c008 = soup.find("div", id="_idContainer008")
    c011 = soup.find("div", id="_idContainer011")
    c012 = soup.find("div", id="_idContainer012")
    c036 = soup.find("div", id="_idContainer036")
    c039 = soup.find("div", id="_idContainer039")
    c041 = soup.find("div", id="_idContainer041")
    c043 = soup.find("div", id="_idContainer043")
    c054 = soup.find("div", id="_idContainer054")
    c056 = soup.find("div", id="_idContainer056")

    title_ps = collect_ps(c001)
    intro_ps = collect_ps(c003) + collect_ps(c004)
    footnote_ps = collect_ps(c006)
    imgs = collapse_section1_merged_pairs(
        gather_imgs_after(body, "_idContainer008", "_idContainer036")
    )

    # --- Part 2 index ---
    index_md: list[str] = [
        "---\n",
        "title: ภาค ๒ ว่าด้วยเอกสารทางประวัติศาสตร์\n",
        "lang: th\n",
        "description: ภาค ๒ ว่าด้วยเอกสารทางประวัติศาสตร์ เกี่ยวกับการชำระ การจารึก และการพิมพ์พระไตรปิฎกในประเทศไทย\n",
        "outline: [2, 3]\n",
        "pageClass: ptb-page-part-2\n",
        "prev: { text: 'การจัดหมวดหมู่ของแต่ละปิฎก', link: '/part-1-knowledge-of-the-tipitaka/structure-of-each-pitaka/' }\n",
        "next: { text: 'ส่วนที่ ๑ รัชกาลที่ ๑', link: '/part-2-historical-documents/section-1/' }\n",
        "\n",
        "searchKeywords:\n",
        "  - ภาค ๒\n",
        "  - เอกสารประวัติศาสตร์\n",
        "  - พระไตรปิฎก\n",
        "  - การชำระ\n",
        "  - การจารึก\n",
        "  - การพิมพ์\n",
        "  - รัชกาลที่ ๑\n",
        "  - รัชกาลที่ ๕\n",
        "  - รัชกาลที่ ๗\n",
        "---\n\n",
        "# ภาค ๒ ว่าด้วยเอกสารทางประวัติศาสตร์ {#part-2-intro}\n\n",
        '<div class="ptb-part2-title-block">\n',
    ]
    for tp in title_ps:
        index_md.append(f'  <p class="ptb-part2-title-line">{tp}</p>\n')
    index_md.append("</div>\n\n")

    for line in intro_ps:
        index_md.append(f"<PtbParagraph>{line}</PtbParagraph>\n\n")

    if footnote_ps:
        index_md.append("### เชิงอรรถแหล่งที่มา\n\n")
        for fp in footnote_ps:
            index_md.append(f'<p class="ptb-paragraph-no-indent ptb-text-xs">{fp}</p>\n\n')

    index_md.extend(
        [
            "## เนื้อหาในภาคนี้\n\n",
            "<PtbList auto>\n",
            '<PtbListItem><a href="/part-2-historical-documents/section-1/">ส่วนที่ ๑ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๑</a></PtbListItem>\n',
            '<PtbListItem><a href="/part-2-historical-documents/section-2/">ส่วนที่ ๒ เอกสารที่เกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๕</a></PtbListItem>\n',
            '<PtbListItem><a href="/part-2-historical-documents/section-3/">ส่วนที่ ๓ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๗</a></PtbListItem>\n',
            "</PtbList>\n",
        ]
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.md").write_text("".join(index_md), encoding="utf-8")

    # --- Section 1 ---
    s1: list[str] = [
        "---\n",
        "title: ส่วนที่ ๑ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๑\n",
        "lang: th\n",
        "description: เอกสารจากพงศาวดารฉบับพระราชหัตถเลขา และพระสมุดคำประกาศเทวดา สังคายนา พ.ศ. ๒๓๓๑\n",
        "outline: [2, 3]\n",
        "pageClass: ptb-page-part-2\n",
        "prev: { text: 'ภาค ๒ — บทนำ', link: '/part-2-historical-documents/' }\n",
        "next: { text: 'ส่วนที่ ๒ รัชกาลที่ ๕', link: '/part-2-historical-documents/section-2/' }\n",
        "\n",
        "searchKeywords:\n",
        "  - รัชกาลที่ ๑\n",
        "  - พระพุทธยอดฟ้าจุฬาโลก\n",
        "  - สังคายนา\n",
        "  - พ.ศ. ๒๓๓๑\n",
        "  - พระสมุดคำประกาศเทวดา\n",
        "  - พงศาวดาร\n",
        "---\n\n",
        "# ส่วนที่ ๑ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๑ {#section-1}\n\n",
        "<PtbParagraph><strong>เอกสารเกี่ยวกับการชำระ และการจารึก พระไตรปิฎก ในรัชกาลที่ ๑</strong></PtbParagraph>\n\n",
    ]
    if c008:
        skip_h = 3
        for p in c008.find_all("p", recursive=False):
            t = p_plain(p)
            if not t:
                continue
            if is_title_p(p) and skip_h > 0:
                skip_h -= 1
                continue
            if is_title_p(p):
                s1.append(f"## {t}\n\n")
            else:
                s1.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")

    if c011:
        for p in c011.find_all("p", recursive=False):
            t = p_plain(p)
            if not t:
                continue
            if is_title_p(p):
                s1.append(f"## {t}\n\n")
            else:
                s1.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")

    if c012:
        for p in c012.find_all("p", recursive=False):
            t = p_plain(p)
            if not t:
                continue
            if is_title_p(p):
                s1.append(f"### {t}\n\n")
            else:
                s1.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")

    thai_digits = "๐๑๒๓๔๕๖๗๘๙"

    def to_thai_num(n: int) -> str:
        return "".join(thai_digits[int(c)] for c in str(n))

    for i, name in enumerate(imgs, 1):
        webp = f"{i:02d}.webp"
        stem = Path(name).stem
        if stem == "A4-04-041":
            alt_extra = " พระสมุดคำประกาศเทวดา (ต่อจากภาพก่อนหน้า)"
        elif stem == "A4-02-002-0021":
            alt_extra = " พระสมุดคำประกาศเทวดา (รวมสองแผ่นต่อแนวตั้ง)"
        else:
            alt_extra = ""
        alt = f"ภาพประกอบส่วนที่ ๑ — ภาพที่ {to_thai_num(i)}{alt_extra}"
        s1.append(f'<ImageLightbox\n  src="{IMG_BASE}/{webp}"\n  alt="{alt}"\n/>\n\n')

    (OUT_DIR / "section-1").mkdir(exist_ok=True)
    (OUT_DIR / "section-1" / "index.md").write_text("".join(s1), encoding="utf-8")

    # --- Section 2 ---
    s2: list[str] = [
        "---\n",
        "title: ส่วนที่ ๒ เอกสารที่เกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๕\n",
        "lang: th\n",
        "description: จากหนังสือกฎหมายรัชกาลที่ ๕ — การสาสนูปถัมภกคือการพิมพ์พระไตรปิฎก\n",
        "outline: [2, 3]\n",
        "pageClass: ptb-page-part-2\n",
        "prev: { text: 'ส่วนที่ ๑ รัชกาลที่ ๑', link: '/part-2-historical-documents/section-1/' }\n",
        "next: { text: 'ส่วนที่ ๓ รัชกาลที่ ๗', link: '/part-2-historical-documents/section-3/' }\n",
        "\n",
        "searchKeywords:\n",
        "  - รัชกาลที่ ๕\n",
        "  - พระจุลจอมเกล้า\n",
        "  - พิมพ์พระไตรปิฎก\n",
        "  - ประกาศสังคายนา\n",
        "---\n\n",
        "# ส่วนที่ ๒ เอกสารที่เกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๕ {#section-2}\n\n",
        "<PtbParagraph><strong>เอกสารที่เกี่ยวกับการชำระ และการพิมพ์พระไตรปิฎก ในรัชกาลที่ ๕</strong></PtbParagraph>\n\n",
    ]
    for container in (c036, c039, c041):
        if not container:
            continue
        skip_title_n = 3 if container is c036 else 0
        for p in container.find_all("p", recursive=False):
            t = p_plain(p)
            if not t:
                continue
            classes = " ".join(p.get("class") or [])
            if "Paragraph-Style-2" in classes and skip_title_n > 0:
                skip_title_n -= 1
                continue
            if is_title_p(p):
                level = "###" if "ParaOverride-6" in classes else "##"
                s2.append(f"{level} {t}\n\n")
            else:
                s2.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")

    (OUT_DIR / "section-2").mkdir(exist_ok=True)
    (OUT_DIR / "section-2" / "index.md").write_text("".join(s2), encoding="utf-8")

    # --- Section 3 ---
    s3: list[str] = [
        "---\n",
        "title: ส่วนที่ ๓ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๗\n",
        "lang: th\n",
        "description: รายงานการสร้างพระไตรปิฎกฉบับสยามรัฐ — จากราชกิจจานุเบกษา และเอกสารที่เกี่ยวเนื่อง\n",
        "outline: [2, 3]\n",
        "pageClass: ptb-page-part-2 ptb-page-part-2-section-3\n",
        "prev: { text: 'ส่วนที่ ๒ รัชกาลที่ ๕', link: '/part-2-historical-documents/section-2/' }\n",
        "\n",
        "searchKeywords:\n",
        "  - รัชกาลที่ ๗\n",
        "  - พระมงกุฎเกล้าเจ้าอยู่หัว\n",
        "  - พระไตรปิฎกสยามรัฐ\n",
        "  - ราชกิจจานุเบกษา\n",
        "  - กิติยากร\n",
        "---\n\n",
        "# ส่วนที่ ๓ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๗ {#section-3}\n\n",
        "<PtbParagraph><strong>เอกสารเกี่ยวกับการชำระและการพิมพ์พระไตรปิฎก ในรัชกาลที่ ๗</strong></PtbParagraph>\n\n",
    ]

    if c043:
        sub = []
        seen_part = False
        for p in c043.find_all("p", recursive=False):
            cls = p.get("class") or []
            if "Paragraph-Style-2" not in cls:
                break
            t = p_plain(p)
            if "ส่วนที่ ๓" in t:
                seen_part = True
                continue
            if seen_part:
                sub.append(t)
        skip_sub = {
            "เอกสารเกี่ยวกับการชำระและการพิมพ์พระไตรปิฎก",
            "ในรัชกาลที่ ๗",
        }
        for t in sub:
            if t in skip_sub:
                continue
            s3.append(f"### {t}\n\n")

    s3.append('<div class="ptb-document-block">\n')

    LEDGER_MARKERS = (
        "ค่าพิมพ์หนังสือ ๔๕ เล่ม",
        "ค่ากระดาษสำหรับพิมพ์",
        "ค่าพิมพ์พระบรมรูป",
        "ค่าใช้จ่ายในการทำที่เก็บ",
        "กับค่าพิมพ์ใบเสร็จ",
        "ค่าจัดส่งพระไตรปิฎก",
        "ค่าเครื่องสักการผู้ชำระ",
        "ค่าใช้จ่ายอื่น ๆ ในการฉลอง",
    )

    def is_ledger_p(t: str) -> bool:
        if any(m in t for m in LEDGER_MARKERS):
            return True
        if re.search(r"เงิน\s*[\d๐-๙,]+\.[\d๐-๙]{2}\s*$", t):
            return True
        if re.search(r"รวม\s+[\d๐-๙,]+\.[\d๐-๙]{2}\s*$", t):
            return True
        return False

    if c043:
        for p in c043.find_all("p", recursive=False):
            t = p_plain(p)
            if not t:
                continue
            classes = " ".join(p.get("class") or [])
            if "Paragraph-Style-2" in classes:
                continue
            if "ParaOverride-8" in classes:
                s3.append(
                    f'<p class="ptb-paragraph-left-align ptb-text-sm">{t}</p>\n\n'
                )
            elif "ParaOverride-9" in classes:
                s3.append(
                    f'<p class="ptb-paragraph-right-align ptb-text-sm">{t}</p>\n\n'
                )
            elif "ParaOverride-12" in classes:
                s3.append(f'<p class="ptb-paragraph-right-align">{t}</p>\n\n')
            elif "ParaOverride-7" in classes:
                s3.append(
                    f'<p class="ptb-paragraph-right-align ptb-text-sm">{t}</p>\n\n'
                )
            elif is_ledger_p(t) or (
                "&#9;" in str(p) and "ก." in t and "เงิน" in t
            ):
                raw = p_ledger_raw(p)
                raw_esc = raw.replace("&", "&amp;").replace("<", "&lt;")
                s3.append(f'<pre class="ptb-ledger-pre">{raw_esc}</pre>\n\n')
            elif "ParaOverride-11" in classes:
                s3.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")
            else:
                s3.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")

    s3.append("</div>\n\n")

    if c054:
        s3.append("## พระราชหัตถเลขา\n\n")
        for p in c054.find_all("p", recursive=False):
            t = p_plain(p)
            if not t:
                continue
            classes = " ".join(p.get("class") or [])
            if is_title_p(p):
                s3.append(f"### {t}\n\n")
            elif "ParaOverride-8" in classes:
                s3.append(
                    f'<p class="ptb-paragraph-left-align ptb-text-sm">{t}</p>\n\n'
                )
            elif "ParaOverride-9" in classes:
                s3.append(
                    f'<p class="ptb-paragraph-right-align ptb-text-sm">{t}</p>\n\n'
                )
            else:
                s3.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")

    if c056:
        s3.append("## คำแปล อารัมภกถา พระไตรปิฎก\n\n")
        for p in c056.find_all("p", recursive=False):
            t = p_plain(p)
            if not t or t == ".":
                continue
            if is_title_p(p):
                s3.append(f"### {t}\n\n")
            else:
                s3.append(f"<PtbParagraph>{t}</PtbParagraph>\n\n")

    for fid, label in (
        ("_idContainer046", "เชิงอรรถ ๑"),
        ("_idContainer049", "เชิงอรรถ ๒"),
        ("_idContainer052", "เชิงอรรถ ๓"),
    ):
        fn = soup.find("div", id=fid)
        if fn:
            ps = collect_ps(fn)
            if ps:
                s3.append(f"### {label}\n\n")
                for fp in ps:
                    s3.append(
                        f'<p class="ptb-paragraph-no-indent ptb-text-xs">{fp}</p>\n\n'
                    )

    (OUT_DIR / "section-3").mkdir(exist_ok=True)
    (OUT_DIR / "section-3" / "index.md").write_text("".join(s3), encoding="utf-8")

    print("OK:", OUT_DIR / "index.md")
    print("OK:", OUT_DIR / "section-1" / "index.md", len(imgs), "images")
    print("OK:", OUT_DIR / "section-2" / "index.md")
    print("OK:", OUT_DIR / "section-3" / "index.md")


if __name__ == "__main__":
    main()
