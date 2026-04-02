# -*- coding: utf-8 -*-
"""
Build ordered passage list for docs/08-part-3-tipitaka-selected-passages/index.md
from Initial_source/html5/05.html; sync ### headings in pitaka index.md files.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/08-part-3-tipitaka-selected-passages"
HTML = ROOT / "Initial_source/html5/05.html"

THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
INT_TO_THAI = "๐๑๒๓๔๕๖๗๘๙"


def int_to_thai(n: int) -> str:
    return "".join(INT_TO_THAI[int(c)] for c in str(n))


def thai_to_int(s: str) -> int:
    return int(s.translate(THAI_DIGITS))


FOLDER_SLUGS: dict[str, str] = {
    "vinaya-pitaka": "วินัยปิฎก (วิ.)",
    "digha-nikaya": "ทีฆนิกาย (ที.)",
    "majjhima-nikaya": "มัชฌิมนิกาย (ม.)",
    "samyutta-nikaya": "สังยุตตนิกาย (สํ.)",
    "anguttara-nikaya": "อังคุตตรนิกาย (องฺ.)",
    "khuddaka-nikaya": "ขุททกนิกาย (ขุ.)",
    "abhidhamma-pitaka": "อภิธรรมปิฎก (อภิ.)",
}

FOLDER_ORDER = list(FOLDER_SLUGS.keys())


def passage_chunks() -> list[tuple[int, int]]:
    """ช่วงลำดับข้อ ๑–๒๒๖: ๒๐ ข้อ × ๑๑ ช่วง + ช่วงสุดท้าย ๖ ข้อ."""
    chunks: list[tuple[int, int]] = []
    for i in range(11):
        lo = i * 20 + 1
        hi = lo + 19
        chunks.append((lo, hi))
    chunks.append((221, 226))
    return chunks


def extract_titles_from_html(html: str) -> list[tuple[int, str]]:
    pat = re.compile(
        r'<p class="Paragraph-Style-4(?: ParaOverride-\d+)?">(.*?)</p>',
        re.DOTALL,
    )
    items: dict[int, str] = {}
    for m in pat.finditer(html):
        block = m.group(1)
        # Superscript footnote digits (InDesign CharOverride-1), not part of title text
        block = re.sub(
            r'<span class="Character-Style-4 CharOverride-1">[๑-๙]</span>',
            "",
            block,
        )
        text = re.sub(r"<[^>]+>", "", block)
        text = text.replace("&#9;", " ").replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        text = text.replace("„", '"').replace("“", '"').replace("”", '"')
        mo = re.match(r"^([๐-๙]+)\.\s*(.*)$", text)
        if not mo:
            continue
        title = mo.group(2).strip()
        n = thai_to_int(mo.group(1))
        if n in items and items[n] != title:
            raise ValueError(f"Duplicate conflicting title for #{n}")
        items[n] = title
    return [(k, items[k]) for k in sorted(items)]


_HEADING_THAI_NUM = re.compile(r"^###\s*([๐-๙]+)\.\s")


def passage_n_from_heading_line(line: str) -> int | None:
    """เลขข้อต่อเนื่อง ๑–๒๒๖ จาก ### ๓๒. ชื่อ… (ไม่พึ่ง {#id})"""
    if ".ptb-h-block" not in line or not line.lstrip().startswith("###"):
        return None
    m = _HEADING_THAI_NUM.match(line.lstrip())
    if not m:
        return None
    return thai_to_int(m.group(1))


def anchor_from_heading_line(line: str) -> str | None:
    m = re.search(r"\{#([A-Za-z_][A-Za-z0-9_-]*)\s", line)
    return m.group(1) if m else None


def build_p3_to_folder() -> dict[int, str]:
    m: dict[int, str] = {}
    for folder in FOLDER_ORDER:
        p = DOCS / folder / "index.md"
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            n = passage_n_from_heading_line(line)
            if n is None:
                continue
            if n in m and m[n] != folder:
                raise ValueError(f"ข้อ {n} ซ้ำใน {m[n]} กับ {folder}")
            m[n] = folder
    return m


def sync_heading_line(line: str, n: int, new_title: str) -> str:
    """Replace title in ### heading line ที่มีเลขข้อ n (เลขไทยนำหน้า) — คง {#id …} เดิม"""
    if ".ptb-h-block" not in line or not line.lstrip().startswith("###"):
        return line
    m = _HEADING_THAI_NUM.match(line.lstrip())
    if not m or thai_to_int(m.group(1)) != n:
        return line
    th = int_to_thai(n)
    if "<PtbFootnote" in line:
        m2 = re.match(
            r"^(###\s*)([๐-๙]+)(\.\s*)(.*?)(<PtbFootnote\b[^>]*>.*?</PtbFootnote>)(\s*)(\{#[^}]+\}[^\n]*)$",
            line.rstrip("\n"),
            re.DOTALL,
        )
        if not m2:
            return line
        return f"{m2.group(1)}{th}{m2.group(3)}{new_title}{m2.group(5)}{m2.group(6)}{m2.group(7)}\n"
    m2 = re.match(
        r"^(###\s*)([๐-๙]+)(\.\s*)(.*?)(\s*(?:\{#[^}]+\}\s*[^\n]*))$",
        line.rstrip("\n"),
        re.DOTALL,
    )
    if not m2:
        return line
    return f"{m2.group(1)}{th}{m2.group(3)}{new_title}{m2.group(5)}\n"


def sync_all_headings(title_map: dict[int, str]) -> list[str]:
    logs: list[str] = []
    for folder in FOLDER_ORDER:
        path = DOCS / folder / "index.md"
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        new_lines: list[str] = []
        changed = False
        for line in lines:
            n = passage_n_from_heading_line(line)
            if n is not None:
                if n in title_map:
                    nl = sync_heading_line(line, n, title_map[n])
                    if nl != line:
                        changed = True
                        logs.append(f"{path.name} p3-{n}")
                    line = nl
            new_lines.append(line)
        if changed:
            path.write_text("".join(new_lines), encoding="utf-8")
    return logs


def passage_anchor_by_folder(folder: str) -> dict[int, str]:
    """แมปเลขข้อ → id จริงในหน้า index ของคัมภีร์"""
    p = DOCS / folder / "index.md"
    if not p.exists():
        return {}
    out: dict[int, str] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        n = passage_n_from_heading_line(line)
        if n is None:
            continue
        aid = anchor_from_heading_line(line)
        if aid:
            out[n] = aid
    return out


def render_index_md(
    titles: list[tuple[int, str]],
    p3_folder: dict[int, str],
) -> str:
    by_n = dict(titles)
    folder_anchors = {f: passage_anchor_by_folder(f) for f in FOLDER_ORDER}
    blocks: list[str] = []
    blocks.append(
        "## ลำดับตามข้อ {.ptb-dh2 .ptb-h-block}\n\n"
        "<PtbParagraph>รายการต่อไปนี้เรียงตามลำดับข้อในฉบับพิมพ์ "
        "(<code>05.html</code>) เลขนำหน้าแต่ละรายการต่อเนื่อง ๑–๒๒๖ "
        "คลิกชื่อเรื่องเพื่อเปิดไปยังตำแหน่งเดียวกันในแฟ้มคัมภีร์</PtbParagraph>\n"
    )

    for lo, hi in passage_chunks():
        label_lo = int_to_thai(lo)
        label_hi = int_to_thai(hi)
        blocks.append(
            f"\n\n### ข้อ {label_lo} - {label_hi} {{.ptb-dh3 .ptb-h-block}}\n\n"
            f'<PtbList auto :start="{lo}" class="ptb-part-open__list">\n'
        )
        for n in range(lo, hi + 1):
            title = by_n[n]
            folder = p3_folder.get(n)
            if folder:
                frag = folder_anchors.get(folder, {}).get(n, f"p3-{n}")
                href = f"/part-3-tipitaka-selected-passages/{folder}/#{frag}"
                inner = f'<a href="{href}">{title}</a>'
            else:
                inner = title
            blocks.append(f"<PtbListItem>{inner}</PtbListItem>\n")
        blocks.append("</PtbList>\n")

    return "".join(blocks)


def main() -> int:
    html = HTML.read_text(encoding="utf-8")
    titles = extract_titles_from_html(html)
    nums = {t[0] for t in titles}
    missing = [i for i in range(1, 227) if i not in nums]
    if missing:
        print("Missing indices:", missing, file=sys.stderr)
        return 1
    if len(titles) != 226:
        print("Expected 226 titles, got", len(titles), file=sys.stderr)
        return 1

    p3_folder = build_p3_to_folder()
    missing_links = [n for n, _ in titles if n not in p3_folder]
    if missing_links:
        print("WARN: no markdown anchor for:", missing_links, file=sys.stderr)

    title_map = dict(titles)
    logs = sync_all_headings(title_map)
    print("Synced headings:", len(logs))
    new_section = render_index_md(titles, p3_folder)

    index_path = DOCS / "index.md"
    base = index_path.read_text(encoding="utf-8")
    lines = base.splitlines(keepends=True)
    head_lines: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("## ลำดับตามข้อ"):
            head_lines = lines[:i]
            break
    else:
        end_first = base.find("</PtbList>")
        if end_first == -1:
            print("No </PtbList> in index.md", file=sys.stderr)
            return 1
        head_lines = [base[: end_first + len("</PtbList>")]]
    head = "".join(head_lines).rstrip()

    index_path.write_text(head + "\n\n" + new_section, encoding="utf-8")
    print("Wrote", index_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
