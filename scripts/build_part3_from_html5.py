# -*- coding: utf-8 -*-
"""
แปลง Initial_source/html5/05.html (ภาค ๓ ใน div _idContainer003)
เป็น docs/08-part-3-tipitaka-selected-passages/*/index.md
"""
from __future__ import annotations

import html as html_module
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "Initial_source" / "html5" / "05.html"
OUT_BASE = ROOT / "docs" / "08-part-3-tipitaka-selected-passages"

THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


def abbrev_compact(s: str) -> str:
    return re.sub(r"\s+", "", s)


BOOK_ROWS: list[tuple[str, str, str]] = [
    ("วิ.", "วิ. มหาวิ.", "มหาวิภังค์"),
    ("วิ.", "วิ. ภิกฺขุนี.", "ภิกขุนีวิภังค์"),
    ("วิ.", "วิ. มหา.", "มหาวรรค"),
    ("วิ.", "วิ. จุลล.", "จุลวรรค"),
    ("วิ.", "วิ. ปริ.", "ปริวาร"),
    ("ที.", "ที. สี.", "สีลขันธวรรค"),
    ("ที.", "ที. มหา.", "มหาวรรค"),
    ("ที.", "ที. ปา.", "ปาฏิกวรรค"),
    ("ม.", "ม. มู.", "มูลปัณณาสก์"),
    ("ม.", "ม. ม.", "มัชฌิมปัณณาสก์"),
    ("ม.", "ม. อุ.", "อุปริปัณณาสก์"),
    ("สํ.", "สํ. ส.", "สคาถวรรค"),
    ("สํ.", "สํ. นิ.", "นิทานวรรค"),
    ("สํ.", "สํ. ข.", "ขันธวารวรรค"),
    ("สํ.", "สํ. สฬา.", "สฬายตนวรรค"),
    ("สํ.", "สํ. มหา.", "มหาวารวรรค"),
    ("องฺ.", "องฺ. เอก.", "เอกนิบาต"),
    ("องฺ.", "องฺ. ทุก.", "ทุกนิบาต"),
    ("องฺ.", "องฺ. ติก.", "ติกนิบาต"),
    ("องฺ.", "องฺ. จตุกฺก.", "จตุกกนิบาต"),
    ("องฺ.", "องฺ. ปญฺจก.", "ปัญจกนิบาต"),
    ("องฺ.", "องฺ. ฉกฺก.", "ฉักกนิบาต"),
    ("องฺ.", "องฺ. สตฺตก.", "สัตตกนิบาต"),
    ("องฺ.", "องฺ. อฏฺฐก.", "อัฏฐกนิบาต"),
    ("องฺ.", "องฺ. นวก.", "นวกนิบาต"),
    ("องฺ.", "องฺ. ทสก.", "ทสกนิบาต"),
    ("องฺ.", "องฺ. เอกาทสก.", "เอกาทสกนิบาต"),
    ("ขุ.", "ขุ. ขุ.", "ขุททกปาฐะ"),
    ("ขุ.", "ขุ. ธ.", "ธรรมบท"),
    ("ขุ.", "ขุ. อุ.", "อุทาน"),
    ("ขุ.", "ขุ. อิติ.", "อิติวุตตกะ"),
    ("ขุ.", "ขุ. สุ.", "สุตตนิบาต"),
    ("ขุ.", "ขุ. วิมาน.", "วิมานวัตถุ"),
    ("ขุ.", "ขุ. เปต.", "เปตวัตถุ"),
    ("ขุ.", "ขุ. เถร.", "เถรคาถา"),
    ("ขุ.", "ขุ. เถรี.", "เถรีคาถา"),
    ("ขุ.", "ขุ. ชา.", "ชาดก"),
    ("ขุ.", "ขุ. มหา.", "มหานิทเทส"),
    ("ขุ.", "ขุ. จูฬ.", "จูฬนิทเทส"),
    ("ขุ.", "ขุ. ปฏิ.", "ปฏิสัมภิทามรรค"),
    ("ขุ.", "ขุ. อป.", "อปทาน"),
    ("ขุ.", "ขุ. พุทฺธ.", "พุทธวงศ์"),
    ("ขุ.", "ขุ. จริยา.", "จริยาปิฎก"),
    ("อภิ.", "อภิ. สงฺ.", "ธรรมสังคณี"),
    ("อภิ.", "อภิ. วิ.", "วิภังค์"),
    ("อภิ.", "อภิ. ธา.", "ธาตุกถา"),
    ("อภิ.", "อภิ. ปุ.", "ปุคคลบัญญัติ"),
    ("อภิ.", "อภิ. ก.", "กถาวัตถุ"),
    ("อภิ.", "อภิ. ย.", "ยมก"),
    ("อภิ.", "อภิ. ป.", "ปัฏฐาน"),
]

BOOK_ORDER_INDEX: dict[str, int] = {abbrev_compact(ab): i for i, (_p, ab, _n) in enumerate(BOOK_ROWS)}
BOOK_BY_COMPACT: dict[str, tuple[str, str, str]] = {
    abbrev_compact(ab): (pit, ab, name) for pit, ab, name in BOOK_ROWS
}

# อักษรย่อใน HTML ต่างจากตารางเล็กน้อย
BOOK_COMPACT_ALIASES: dict[str, str] = {
    "วิ.จุลฺล.": abbrev_compact("วิ. จุลล."),
}

# หัวข้อหลักของแต่ละเรื่องในเล่ม: ๑. ๒. … ๑๐๐. (เลขไทย + จุด + เว้นวรรค)
PASSAGE_TITLE_RE = re.compile(r"^[๐-๙]{1,4}\.\s")

GROUP_FOLDERS: list[tuple[str, str, str]] = [
    ("วิ.", "vinaya-pitaka", "วินัยปิฎก (วิ.)"),
    ("ที.", "digha-nikaya", "ทีฆนิกาย (ที.)"),
    ("ม.", "majjhima-nikaya", "มัชฌิมนิกาย (ม.)"),
    ("สํ.", "samyutta-nikaya", "สังยุตตนิกาย (สํ.)"),
    ("องฺ.", "anguttara-nikaya", "อังคุตตรนิกาย (องฺ.)"),
    ("ขุ.", "khuddaka-nikaya", "ขุททกนิกาย (ขุ.)"),
    ("อภิ.", "abhidhamma-pitaka", "อภิธรรมปิฎก (อภิ.)"),
]


def extract_main_div(html: str) -> str:
    start = html.find('id="_idContainer003"')
    if start == -1:
        raise SystemExit("ไม่พบ _idContainer003")
    start = html.rfind("<div", 0, start + 1)
    marker = '<div id="_idContainer006"'
    end = html.find(marker)
    if end == -1:
        raise SystemExit("ไม่พบจุดเริ่มเชิงอรรถ _idContainer006")
    chunk = html[start:end]
    if chunk.rstrip().endswith("</div>"):
        chunk = chunk[: chunk.rfind("</div>")]
    return chunk


def split_ps(chunk: str) -> list[str]:
    return re.findall(r"<p\s+[^>]*>.*?</p>", chunk, flags=re.DOTALL)


def p_class(p_html: str) -> str:
    m = re.search(r'class="([^"]*)"', p_html)
    return m.group(1) if m else ""


def inner_html(p_html: str) -> str:
    m = re.search(r">(.*)</p>\s*$", p_html, re.DOTALL)
    return m.group(1) if m else ""


def strip_tags_keep_structure(fragment: str) -> str:
    fragment = fragment.replace("\r\n", "\n").replace("\r", "\n")
    fragment = re.sub(r"<a\s[^>]*id=\"[^\"]+\"\s*></a>", "", fragment)

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
                            tag = m.group(0)
                            if "CharOverride-1" in tag:
                                note = walk(inner).strip()
                                out.append(
                                    f'<PtbFootnote label="{html_module.escape(note)}">เชิงอรรถประกอบในเล่มต้นฉบับ</PtbFootnote>'
                                )
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


def resolve_book_compact(compact_prefix: str) -> str:
    if compact_prefix in BOOK_ORDER_INDEX:
        return compact_prefix
    if compact_prefix in BOOK_COMPACT_ALIASES:
        return BOOK_COMPACT_ALIASES[compact_prefix]
    keys = sorted(BOOK_ORDER_INDEX.keys(), key=len, reverse=True)
    for k in keys:
        if compact_prefix.startswith(k):
            return k
    return compact_prefix


def parse_citation(raw: str) -> tuple[str, str, str, list[int], list[int], list[int]]:
    raw = raw.strip()
    thai_digit = re.compile(r"[๐-๙]")
    m = thai_digit.search(raw)
    if not m:
        return ("?", "", raw, [9999], [9999], [9999])
    prefix = raw[: m.start()].strip()
    rest = raw[m.start() :].strip()
    compact_prefix = abbrev_compact(prefix)
    matched = resolve_book_compact(compact_prefix)
    pit = ""
    if matched in BOOK_BY_COMPACT:
        pit = BOOK_BY_COMPACT[matched][0]
    else:
        for pk, _, _ in GROUP_FOLDERS:
            if compact_prefix.startswith(abbrev_compact(pk)):
                pit = pk
                break
    parts = [p.strip() for p in rest.split("/")]

    def parse_nums(seg: str) -> list[int]:
        seg = seg.translate(THAI_DIGITS)
        nums = [int(x) for x in re.findall(r"\d+", seg)]
        return nums if nums else [9999]

    vols, khaos, pages = [9999], [9999], [9999]
    if len(parts) >= 1:
        vols = parse_nums(parts[0])
    if len(parts) >= 2:
        khaos = parse_nums(parts[1])
    if len(parts) >= 3:
        pages = parse_nums(parts[2])
    return (pit, matched, prefix, vols, khaos, pages)


def sort_key(passage: Passage) -> tuple:
    c = passage.cite_parse
    book_idx = BOOK_ORDER_INDEX.get(c[1], 9999)
    return (book_idx, c[3][0], c[4][0], c[5][0], passage.seq)


@dataclass
class Passage:
    seq: int
    title: str
    blocks: list[str] = field(default_factory=list)
    # หนึ่งเรื่องอาจมีหลายบรรทัดอ้างอิง (เช่น หัวข้อย่อย (๑)(๒)… แต่ละท้ายเรื่องมี cite)
    citations: list[tuple[str, tuple]] = field(default_factory=list)

    @property
    def cite_parse(self) -> tuple:
        return self.citations[0][1] if self.citations else ()

    def markdown(self) -> str:
        lines: list[str] = []
        safe_title = self.title.replace("\n", " ").strip()
        anchor = slug_anchor(safe_title, self.seq)
        lines.append(f"### {safe_title} {{#{anchor} .ptb-dh3 .ptb-h-block}}")
        lines.append("")
        for b in self.blocks:
            if b.startswith("#### ") or b.startswith("<!--"):
                lines.append(b)
            else:
                lines.append(f"<PtbParagraph>{b}</PtbParagraph>")
            lines.append("")
        for raw, _cp in self.citations:
            lines.append(
                f'<p class="ptb-quote-citation ptb-text-xs ptb-paragraph-no-indent">{html_module.escape(raw)}</p>'
            )
            lines.append("")
        # join จบด้วย "" ไม่สร้างบรรทัดว่างหลังบรรทัดสุดท้าย — ต้องมี \n เพิ่มหนึ่งตัว
        # เพื่อให้หัวข้อ ### / ## ถัดไปไม่ชิดกับ </p> หรือบรรทัดก่อนหน้า (กติกา Markdown)
        return "\n".join(lines) + "\n"


def slug_anchor(title: str, seq: int) -> str:
    t = re.sub(r"[^\u0e00-\u0e7fa-zA-Z0-9]+", "-", title.lower())
    t = re.sub(r"-+", "-", t).strip("-")
    if not t:
        t = f"p{seq}"
    return f"ptb-p3-{seq}-{t[:48]}"


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    chunk = extract_main_div(html)
    ps = split_ps(chunk)

    passages: list[Passage] = []
    current: Passage | None = None
    post_cite: Passage | None = None
    seq = 0

    def target() -> Passage | None:
        if current is not None:
            return current
        return post_cite

    for p_html in ps:
        cls = p_class(p_html)
        inner = inner_html(p_html)

        if "Paragraph-Style-4" in cls and "Character-Style-4" in inner:
            text = strip_tags_keep_structure(inner)
            if not text or text == ".":
                continue
            if not PASSAGE_TITLE_RE.match(text):
                dest = current if current is not None else post_cite
                if dest is not None:
                    dest.blocks.append(text)
                continue
            post_cite = None
            seq += 1
            current = Passage(seq, text, [])
            passages.append(current)
            continue

        if "CharOverride-3" in inner:
            cite = strip_tags_keep_structure(inner)
            cp = parse_citation(cite)
            dest = current if current is not None else post_cite
            if dest is not None:
                dest.citations.append((cite, cp))
                post_cite = dest
            current = None
            continue

        if "Paragraph-Style-2" in cls and "CharOverride-4" in inner:
            st = strip_tags_keep_structure(inner)
            dest = post_cite or current
            if dest is not None:
                dest.blocks.append(f"#### {st} {{#summary-{dest.seq} .ptb-dh4 .ptb-h-block}}")
            continue

        if "Paragraph-Style-1" in cls or "Paragraph-Style-2" in cls:
            st = strip_tags_keep_structure(inner)
            if not st:
                continue
            dest = target()
            if dest is not None:
                dest.blocks.append(st)
            continue

    by_pit: dict[str, list[Passage]] = {pk: [] for pk, _, _ in GROUP_FOLDERS}
    orphans: list[Passage] = []
    for p in passages:
        if not p.citations or not p.cite_parse or p.cite_parse[0] == "?":
            orphans.append(p)
            continue
        pit = p.cite_parse[0]
        if pit not in by_pit:
            orphans.append(p)
            continue
        by_pit[pit].append(p)

    for pit in by_pit:
        by_pit[pit].sort(key=sort_key)

    OUT_BASE.mkdir(parents=True, exist_ok=True)

    parent_fm = """---
title: ภาค ๓ ข้อความน่ารู้จากพระไตรปิฎก
lang: th
description: คัดข้อความจากพระไตรปิฎกตามอักษรย่อชื่อคัมภีร์ — วินัย สุตตันตะ อภิธรรม
outline: [2, 3]
pageClass: ptb-page-part3-index
prev: { text: 'ส่วนที่ ๓ เอกสารในรัชกาลที่ ๗', link: '/part-2-historical-documents/section-3/' }

searchKeywords:
  - ภาค ๓
  - ข้อความน่ารู้
  - พระไตรปิฎก
  - วินัยปิฎก
  - สุตตันตปิฎก
  - อภิธรรมปิฎก
---

# ภาค ๓ {#part-3-open .ptb-dh1 .ptb-h-block}

<div class="ptb-title-stack">
  <p class="ptb-text-2xl">ภาค ๓</p>
  <p>ข้อความน่ารู้จากพระไตรปิฎก</p>
</div>

<PtbParagraph>เนื้อหาในภาคนี้จัดตามกลุ่มคัมภีร์จากอักษรย่อท้ายแต่ละเรื่อง เรียงลำดับตามตารางอักษรย่อชื่อคัมภีร์ในเล่ม แล้วตามเล่ม ข้อ และหน้าในคัมภีร์อ้างอิง</PtbParagraph>

<PtbList class="ptb-part-open__list" markerWidth="14ch">
"""

    items = []
    for _pit, slug, title in GROUP_FOLDERS:
        link = f"/part-3-tipitaka-selected-passages/{slug}/"
        items.append(f'<PtbListItem marker="{title}"><a href="{link}">เปิดอ่าน</a></PtbListItem>')
    (OUT_BASE / "index.md").write_text(
        parent_fm + "\n".join(items) + "\n</PtbList>\n", encoding="utf-8"
    )

    for pit, slug, group_title in GROUP_FOLDERS:
        plist = by_pit[pit]
        folder = OUT_BASE / slug
        folder.mkdir(parents=True, exist_ok=True)

        sections: list[tuple[str, str, list[Passage]]] = []
        cur_key: str | None = None
        cur_name = ""
        bucket: list[Passage] = []
        for p in plist:
            c = p.cite_parse
            key = c[1]
            if key in BOOK_BY_COMPACT:
                _pp, _abbrev_spaced, fullname = BOOK_BY_COMPACT[key]
            else:
                fullname = c[2] or key
            if key != cur_key:
                if bucket:
                    sections.append((cur_key or "", cur_name, bucket))
                cur_key = key
                cur_name = fullname
                bucket = []
            bucket.append(p)
        if bucket:
            sections.append((cur_key or "", cur_name, bucket))

        desc = f"{group_title} — ข้อความน่ารู้จากพระไตรปิฎก"
        fm = f"""---
title: {group_title}
lang: th
description: {desc}
outline: [2, 3, 4]
pageClass: ptb-page-part3-pitaka
prev: {{ text: 'ภาค ๓ เกริ่นนำ', link: '/part-3-tipitaka-selected-passages/' }}

searchKeywords:
  - {group_title}
  - ข้อความน่ารู้
  - พระไตรปิฎก
---

# {group_title} {{#pitaka-{slug} .ptb-dh1 .ptb-h-block}}

"""
        parts_out: list[str] = [fm]
        for key, fullname, bucket in sections:
            abbrev_spaced = BOOK_BY_COMPACT.get(key, ("", key, fullname))[1]
            sec_anchor = f"book-{BOOK_ORDER_INDEX.get(key, 999):03d}"
            parts_out.append(
                f"## {fullname} ({abbrev_spaced}) {{#{sec_anchor} .ptb-dh2 .ptb-h-block}}\n\n"
            )
            for p in bucket:
                parts_out.append(p.markdown())

        (folder / "index.md").write_text("".join(parts_out), encoding="utf-8")

    if orphans:
        print("WARNING orphans (no pitaka match):", len(orphans))


if __name__ == "__main__":
    main()
