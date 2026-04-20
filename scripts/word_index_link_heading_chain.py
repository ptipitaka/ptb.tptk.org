#!/usr/bin/env python3
"""
Build PtbWordIndexLink labels from heading chains in digest/source .md files.

Label format: ภาค {part} เล่ม {vol} — {h2} — {h3} — … (actual heading titles from file,
excluding ภาพรวม / ขยายความ from the chain).

Usage (dry-run):
  python scripts/word_index_link_heading_chain.py path/to/word-index.md

  python scripts/word_index_link_heading_chain.py path/to/word-index.md --write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"

# Markdown heading with optional attrs: # Title {#id …} or ## … {#id …}
HEADING_RE = re.compile(
    r"^(#{1,6})\s+(.+?)\s*\{#([A-Za-z0-9]+)(?:\s+[^}]*)?\}\s*$"
)

SKIP_TITLES = frozenset({"ภาพรวม", "ขยายความ"})


def strip_heading_title(raw: str) -> str:
    """Remove trailing footnote markup from heading line for display title."""
    t = raw.strip()
    # Drop <PtbFootnote>...</PtbFootnote> if entire title is wrapped (rare)
    if "<PtbFootnote>" in t:
        t = re.sub(r"<PtbFootnote>.*?</PtbFootnote>", "", t, flags=re.DOTALL)
    return t.strip()


def parse_headings(md_text: str) -> list[tuple[int, str, str]]:
    """Return list of (level 1-6, title, anchor_id)."""
    out: list[tuple[int, str, str]] = []
    for line in md_text.splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        level = len(m.group(1))
        title = strip_heading_title(m.group(2))
        hid = m.group(3)
        out.append((level, title, hid))
    return out


def chain_for_anchor(headings: list[tuple[int, str, str]], target_id: str) -> list[str] | None:
    """Return heading titles from outermost ancestor (under h1) down to target_id."""
    idx = None
    for i, (_lv, _t, hid) in enumerate(headings):
        if hid == target_id:
            idx = i
            break
    if idx is None:
        return None

    path: list[str] = []
    j = idx
    cur_lv = headings[idx][0] + 1  # ensure first heading is always taken
    while j >= 0:
        lv, title, _hid = headings[j]
        if title in SKIP_TITLES:
            j -= 1
            continue
        if j == idx:
            path.insert(0, title)
            cur_lv = lv
            j -= 1
            continue
        if lv < cur_lv:
            path.insert(0, title)
            cur_lv = lv
        j -= 1
    return path


def part_and_vol_from_href(href: str) -> tuple[str | None, str | None]:
    """Extract part number (1,3,4) and Thai vol digits from href."""
    m = re.search(r"/part-(\d+)-", href)
    part = m.group(1) if m else None
    m2 = re.search(r"/vol-(\d+)", href)
    vol = None
    if m2:
        n = int(m2.group(1))
        thai_digits = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")
        vol = str(n).translate(thai_digits)
    return part, vol


def trim_volume_h1_duplicate(chain: list[str], vol: str | None) -> list[str]:
    """Remove redundant 'เล่ม {vol}' from the first segment; keep the rest of the h1 title."""
    if not vol or not chain:
        return chain
    first = chain[0]
    vol_prefix = f"เล่ม {vol}"
    if first == vol_prefix:
        return chain[1:]
    if first.startswith(f"{vol_prefix} "):
        rest = first[len(f"{vol_prefix} ") :].strip()
        if rest:
            return [rest, *chain[1:]]
        return chain[1:]
    return chain


def part4_pitaka_or_nikaya_prefix(href: str) -> str | None:
    """First breadcrumb under 'ภาค ๔ เล่ม …' from URL path (not in single-volume .md headings)."""
    if "/part-4-tipitaka-digest/" not in href:
        return None
    if "/vinaya-pitaka/" in href:
        return "วินัยปิฎก (วิ.)"
    if "/sutta-pitaka/digha-nikaya/" in href:
        return "ทีฆนิกาย (ที.)"
    if "/sutta-pitaka/majjhima-nikaya/" in href:
        return "มัชฌิมนิกาย (ม.)"
    if "/sutta-pitaka/samyutta-nikaya/" in href:
        return "สังยุตตนิกาย (สํ.)"
    if "/sutta-pitaka/anguttara-nikaya/" in href:
        return "อังคุตตรนิกาย (องฺ.)"
    if "/sutta-pitaka/khuddaka-nikaya/" in href:
        return "ขุททกนิกาย (ขุ.)"
    if "/abhidhamma-pitaka/" in href:
        return "อภิธรรมปิฎก (อภิ.)"
    return None


def _prepend_if_missing(prefix: str, chain: list[str]) -> list[str]:
    if not chain or not prefix:
        return chain
    first = chain[0]
    if first == prefix:
        return chain
    key = prefix.split(" (", 1)[0].strip()
    if key and key in first:
        return chain
    return [prefix, *chain]


def label_for_href(href: str, chain: list[str] | None) -> str | None:
    if not chain:
        return None
    part, vol = part_and_vol_from_href(href)
    if not part:
        return None
    chain = list(chain)
    chain = trim_volume_h1_duplicate(chain, vol)
    if not chain:
        return None
    if part == "4":
        pfx = part4_pitaka_or_nikaya_prefix(href)
        if pfx:
            chain = _prepend_if_missing(pfx, chain)
    thai = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")
    part_th = part.translate(thai)
    if vol:
        prefix = f"ภาค {part_th} เล่ม {vol}"
    else:
        prefix = f"ภาค {part_th}"
    rest = " — ".join(chain)
    return f"{prefix} — {rest}"


def resolve_md_path(href: str) -> Path | None:
    """Map site href to docs markdown path."""
    if not href.startswith("/"):
        return None
    path = href.lstrip("/").split("#", 1)[0]
    if path.endswith("/"):
        path += "index"
    p = DOCS / "09-part-4-tipitaka-digest"
    # part-1, part-3 use different folder names
    if path.startswith("part-1-knowledge-of-the-tipitaka/"):
        p = DOCS / "06-part-1-knowledge-of-the-tipitaka" / path.replace(
            "part-1-knowledge-of-the-tipitaka/", ""
        )
        if p.suffix != ".md":
            p = p.with_suffix(".md")
        return p if p.is_file() else None
    if path.startswith("part-3-tipitaka-selected-passages/"):
        p = DOCS / "08-part-3-tipitaka-selected-passages" / path.replace(
            "part-3-tipitaka-selected-passages/", ""
        )
        if p.suffix != ".md":
            p = p.with_suffix(".md")
        return p if p.is_file() else None
    if path.startswith("part-4-tipitaka-digest/"):
        rel = path.replace("part-4-tipitaka-digest/", "")
        p = DOCS / "09-part-4-tipitaka-digest" / rel
        if p.suffix != ".md":
            p = p.with_suffix(".md")
        return p if p.is_file() else None
    return None


# Optional tier="primary"|"secondary" (word-index บุคคล); เก็บไว้เมื่อสร้าง label ใหม่
LINK_RE = re.compile(
    r'<PtbWordIndexLink\s+href="([^"]+)"\s+label="([^"]*)"(?:\s+tier="(primary|secondary)")?\s*/>'
)


def process_file(word_index_md: Path, write: bool) -> int:
    text = word_index_md.read_text(encoding="utf-8")
    cache: dict[tuple[str, str], list[str] | None] = {}

    def get_chain(href_full: str) -> list[str] | None:
        if "#" not in href_full:
            return None
        path_part, frag = href_full.split("#", 1)
        key = (path_part, frag)
        if key in cache:
            return cache[key]
        md_path = resolve_md_path("/" + path_part.lstrip("/") + "#" + frag)
        if not md_path or not md_path.is_file():
            cache[key] = None
            return None
        headings = parse_headings(md_path.read_text(encoding="utf-8"))
        ch = chain_for_anchor(headings, frag)
        cache[key] = ch
        return ch

    def repl(m: re.match) -> str:
        href, old_label, tier = m.group(1), m.group(2), m.group(3)
        chain = get_chain(href)
        new_label = label_for_href(href, chain)
        if new_label is None:
            return m.group(0)
        if new_label == old_label:
            return m.group(0)
        tier_attr = f' tier="{tier}"' if tier else ""
        return f'<PtbWordIndexLink href="{href}" label="{new_label}"{tier_attr} />'

    new_text, n = LINK_RE.subn(repl, text)
    changed = new_text != text
    if write and changed:
        word_index_md.write_text(new_text, encoding="utf-8")

    unresolved = []
    for m in LINK_RE.finditer(text):
        href = m.group(1)
        if "#" not in href:
            continue
        _, frag = href.split("#", 1)
        if get_chain(href) is None:
            unresolved.append((href, frag))

    print(f"{word_index_md}: PtbWordIndexLink count: {n}" + (f", file updated" if write and changed else ""))
    if unresolved:
        print("  unresolved (chain None):", len(unresolved))
        for h, f in unresolved[:20]:
            print(f"    {h}")
        if len(unresolved) > 20:
            print("    ...")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("word_index_md", type=Path)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    return process_file(args.word_index_md.resolve(), args.write)


if __name__ == "__main__":
    sys.exit(main())
