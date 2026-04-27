# Rebuild "## พระเถระอื่น ๆ (เรียงตามอักษร)" — sort entries + ### letter headings.
# หมวดตามพยัญชนะนำ (ไม่ใช้สระนำ เ/แ/โ/ใ/ไ เป็นหมวด) และลำดับหมวดตามพยัญชนะไทย
# Usage: python scripts/_sort_thera_other_section.py --write
from __future__ import annotations

import argparse
import locale
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs/10-part-5-word-index/persons/bhikkhu/index.md"

# h2 may have ensure_ptb_heading_ids: `{#… .ptb-h-block}` or plain `{.ptb-h-block}`
SECTION_LINE_START = "## พระเถระอื่น ๆ (เรียงตามอักษร)"

ENTRY_RE = re.compile(
    r"(<PtbWordIndexEntry\b[^>]*?\s*/>|<PtbWordIndexEntry\b[^>]*>.*?</PtbWordIndexEntry>)",
    re.DOTALL,
)


def get_term(opening_block: str) -> str:
    first = opening_block.split("\n", 1)[0]
    m = re.search(r'term="([^"]*)"', first)
    return m.group(1) if m else ""


def sort_key(term: str) -> str:
    try:
        return locale.strxfrm(term)
    except Exception:
        return term


# ลำดับพยัญชนะไทย (เรียงหมวด h3)
THAI_CONSONANT_ORDER = (
    "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
)
_CONSONANT_RANK: dict[str, int] = {c: i for i, c in enumerate(THAI_CONSONANT_ORDER)}

# สระนำที่เขียนหน้าพยัญชนะ — ไม่ถือเป็นหมวดอักษร
_LEADING_VOWEL_MARKS = frozenset("เแโใไ")


def _is_thai_consonant(ch: str) -> bool:
    if len(ch) != 1:
        return False
    o = ord(ch)
    return 0x0E01 <= o <= 0x0E2E


def first_leading_consonant(term: str) -> str:
    """พยัญชนะตัวแรกของชื่อหลังคำว่า พระ (ข้ามสระนำ; รายการ ก และ ก ใช้คนแรกก่อน ' และ ')."""
    if not term.startswith("พระ"):
        return term[0] if term else "?"
    rest = term[len("พระ") :].strip()
    if " และ " in rest:
        rest = rest.split(" และ ", 1)[0].strip()
    if not rest:
        return "?"
    i = 0
    if rest[i] in _LEADING_VOWEL_MARKS:
        i += 1
    while i < len(rest):
        ch = rest[i]
        if _is_thai_consonant(ch):
            return ch
        i += 1
    return rest[0]


def consonant_section_order_key(letter: str) -> tuple[int, str]:
    if letter in _CONSONANT_RANK:
        return (_CONSONANT_RANK[letter], "")
    return (len(THAI_CONSONANT_ORDER), sort_key(letter))


def main() -> None:
    for loc in ("th_TH.UTF-8", "Thai_Thailand.utf8", "Thai_Thailand", "th_TH"):
        try:
            locale.setlocale(locale.LC_COLLATE, loc)
            break
        except OSError:
            continue

    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    text = PATH.read_text(encoding="utf-8")
    idx = text.find(SECTION_LINE_START)
    if idx < 0:
        raise SystemExit(f"missing section line starting with {SECTION_LINE_START!r}")

    line_end = text.find("\n", idx)
    if line_end < 0:
        raise SystemExit("unterminated section heading line")
    section_heading_line = text[idx:line_end]
    head = text[:idx]
    rest = text[line_end + 1 :]
    blocks = ENTRY_RE.findall(rest)
    if not blocks:
        raise SystemExit("no PtbWordIndexEntry blocks after section")

    # Pair term -> block (last wins if duplicate terms — should not happen)
    by_term: dict[str, str] = {}
    for b in blocks:
        t = get_term(b)
        if not t:
            raise SystemExit("entry without term")
        by_term[t] = b

    terms = list(by_term.keys())
    by_consonant: dict[str, list[str]] = {}
    for t in terms:
        c = first_leading_consonant(t)
        by_consonant.setdefault(c, []).append(t)
    letter_order = sorted(by_consonant.keys(), key=consonant_section_order_key)
    for c in letter_order:
        by_consonant[c].sort(key=sort_key)

    out_parts: list[str] = [head.rstrip(), "", section_heading_line, ""]
    # U+2060 word joiner so headings are >1 visible char for ensure_ptb_heading_ids regex
    wj = "\u2060"
    for letter in letter_order:
        out_parts.append(f"### {letter}{wj} {{.ptb-h-block}}")
        out_parts.append("")
        for term in by_consonant[letter]:
            block = by_term[term].rstrip()
            out_parts.append(block)
            out_parts.append("")
            out_parts.append("")

    new_text = "\n".join(out_parts).rstrip() + "\n"
    if not args.write:
        print("dry-run; would write", PATH)
        print("terms:", len(terms))
        return
    PATH.write_text(new_text, encoding="utf-8")
    print("wrote", PATH, "entries", len(terms))


if __name__ == "__main__":
    main()
