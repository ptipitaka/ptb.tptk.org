"""สร้างไฟล์ vol-XX.md สำหรับภาค ๔ จาก docs/.vitepress/part4-volume-titles.json

สุตตันตปิฎก: วางไฟล์ภายใต้ sutta-pitaka/<nikaya>/ ตาม ๕ นิกาย
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLES_PATH = ROOT / "docs" / ".vitepress" / "part4-volume-titles.json"
BASE = ROOT / "docs" / "09-part-4-tipitaka-digest"


def pitaka_for_volume(v: int) -> str:
    if 1 <= v <= 8:
        return "vinaya-pitaka"
    if 9 <= v <= 33:
        return "sutta-pitaka"
    if 34 <= v <= 45:
        return "abhidhamma-pitaka"
    raise ValueError(v)


def sutta_nikaya_for_volume(v: int) -> str:
    if 9 <= v <= 11:
        return "digha-nikaya"
    if 12 <= v <= 14:
        return "majjhima-nikaya"
    if 15 <= v <= 19:
        return "samyutta-nikaya"
    if 20 <= v <= 24:
        return "anguttara-nikaya"
    if 25 <= v <= 33:
        return "khuddaka-nikaya"
    raise ValueError(v)


def dir_for_volume(v: int) -> Path:
    p = pitaka_for_volume(v)
    if p == "sutta-pitaka":
        return BASE / p / sutta_nikaya_for_volume(v)
    return BASE / p


def main() -> None:
    titles: list[str] = json.loads(TITLES_PATH.read_text(encoding="utf-8"))
    assert len(titles) == 45, len(titles)

    for i, title in enumerate(titles, start=1):
        num = f"{i:02d}"
        dir_path = dir_for_volume(i)
        dir_path.mkdir(parents=True, exist_ok=True)
        body = f"""---
title: {title}
lang: th
description: ความย่อแห่งพระไตรปิฎก — {title}
outline: [2, 3]
searchKeywords:
  - ภาค ๔
  - ความย่อแห่งพระไตรปิฎก
---

# {title} {{.ptb-dh1 .ptb-h-block}}

<PtbParagraph>หน้านี้รอใส่เนื้อหาความย่อตามฉบับพิมพ์</PtbParagraph>
"""
        path = dir_path / f"vol-{num}.md"
        path.write_text(body, encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
