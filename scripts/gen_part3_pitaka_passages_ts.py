"""Generate docs/.vitepress/theme/part3PitakaPassages.ts from pitaka index.md files."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/08-part-3-tipitaka-selected-passages"
OUT = ROOT / "docs/.vitepress/theme/part3PitakaPassages.ts"

THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
_HEADING_THAI_NUM = re.compile(r"^###\s*([๐-๙]+)\.\s")


def thai_to_int(s: str) -> int:
    return int(s.translate(THAI_DIGITS))


FOLDERS = [
    "vinaya-pitaka",
    "digha-nikaya",
    "majjhima-nikaya",
    "samyutta-nikaya",
    "anguttara-nikaya",
    "khuddaka-nikaya",
    "abhidhamma-pitaka",
]


def parse_title(line: str) -> tuple[int, str, str] | None:
    """คืน (เลขข้อต่อเนื่อง, ชื่อเรื่อง, anchor id ใน {#…})"""
    if ".ptb-h-block" not in line or not line.lstrip().startswith("###"):
        return None
    m = _HEADING_THAI_NUM.match(line.lstrip())
    if not m:
        return None
    pid = thai_to_int(m.group(1))
    am = re.search(r"\{#([A-Za-z0-9_-]+)\s", line)
    anchor = am.group(1) if am else ""
    s = re.sub(r"^###\s*[๐-๙]+\.\s*", "", line)
    s = re.sub(r"<PtbFootnote[^>]*>.*?</PtbFootnote>", "", s, flags=re.DOTALL)
    s = re.sub(r"\s*\{#[^}]+\}.*$", "", s).strip()
    return pid, s, anchor


def main() -> None:
    lines: list[str] = []
    lines.append("/**")
    lines.append(" * ข้อ p3 และชื่อเรื่องต่อคัมภีร์ (ภาค ๓) — สอดคล้องกับ index ในแต่ละโฟลเดอร์")
    lines.append(" * สร้างด้วย: python scripts/gen_part3_pitaka_passages_ts.py")
    lines.append(" */")
    lines.append("export const PART3_PITAKA_PASSAGES = {")

    for folder in FOLDERS:
        text = (DOCS / folder / "index.md").read_text(encoding="utf-8")
        items: list[tuple[int, str, str]] = []
        for line in text.splitlines():
            r = parse_title(line)
            if r:
                items.append(r)
        items.sort(key=lambda x: x[0])
        block_lines = [
            f"    {{ id: {pid}, title: {json.dumps(title, ensure_ascii=False)}, anchor: {json.dumps(anchor, ensure_ascii=False)} }},"
            for pid, title, anchor in items
        ]
        inner = "\n".join(block_lines)
        lines.append(f"  '{folder}': [\n{inner}\n  ] as const,")

    lines.append("} as const")
    lines.append("")
    lines.append("export type Part3PitakaKey = keyof typeof PART3_PITAKA_PASSAGES")
    lines.append("")
    lines.append(
        "export type Part3PassageEntry = (typeof PART3_PITAKA_PASSAGES)[Part3PitakaKey][number]"
    )
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
