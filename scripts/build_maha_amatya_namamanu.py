# -*- coding: utf-8 -*-
"""Build docs/10-part-5-word-index/persons/maha-amatya/index.md (ดัชนีมหาอำมาตย์)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULER_JSON = ROOT / "scripts" / "_rulers_legacy_links.json"
BHI_JSON = ROOT / "scripts" / "_bhikkhu_links_extract.json"
OUT_PATH = ROOT / "docs" / "10-part-5-word-index" / "persons" / "maha-amatya" / "index.md"


def L(
    href: str,
    label: str,
    tier: str = "primary",
    _sort: int = 0,
) -> dict:
    return {"href": href, "label": label, "tier": tier, "_sort": _sort}


def load_ruler() -> dict:
    with open(RULER_JSON, encoding="utf-8") as f:
        return json.load(f)


def load_bhikkhu() -> dict:
    with open(BHI_JSON, encoding="utf-8") as f:
        return json.load(f)


def sort_key(link: dict) -> tuple:
    import re

    h = link["href"]
    sk = link.get("_sort", 0)
    if "/part-1-" in h:
        return (0, sk, h)
    if "/part-2-" in h:
        return (1, sk, h)
    if "/part-3-" in h:
        return (2, sk, h)
    m = re.search(r"vol-(\d+)", h)
    vol = int(m.group(1)) if m else 999
    if "/part-4-" in h:
        return (3, vol, sk, h)
    return (4, vol, sk, h)


def merge_links(
    j: dict,
    key: str | None,
    extra: list[dict] | None = None,
) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    if key and key in j:
        for Ld in j[key]:
            h = Ld["href"]
            if h in seen:
                continue
            seen.add(h)
            out.append(dict(Ld))
    if extra:
        for Ld in extra:
            h = Ld["href"]
            if h in seen:
                continue
            seen.add(h)
            out.append(dict(Ld))
    out.sort(key=sort_key)
    for o in out:
        o.pop("_sort", None)
    return out


# ลิงก์เฉพาะราย (ไม่อยู่ใน ruler/bhikkhunder key ที่ใช้ merge)
MANUAL: dict[str, list[dict]] = {
    "กัปปินะ (อดีตชาติของพระมหากัปปินเถระ)": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-33#7gheJpiJVs",
            "ภาค ๔ เล่ม ๓๓ — ขุททกนิกาย (ขุ.) — อปทาน ภาค ๒ — ๒. มหากัปปินเถราปทาน (อดีตชาติ — อำมาตย์ ณ หังสนคร)",
        ),
    ],
    "หมอชีวก โกมารภัจจ์": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13#M8tkkO1jy3",
            "ภาค ๔ เล่ม ๑๓ — มัชฌิมนิกาย มูลปัณณาสก์ — ๕. ชีวกสูตร ว่าด้วยหมอชีวก โกมารภัจจ์",
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#ZhZSpEXwan",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย เอก - ทุก - ติกนิบาต — เอตทัคคะฝ่ายอุบาสก — ชีวก โกมารภัจจ์ เป็นผู้เลิศในทางเลื่อมใสในบุคคล",
        ),
    ],
    "ทีฆการายน (ทีฆการายนอำมาตย์)": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13#BuUnwB6UJK",
            "ภาค ๔ เล่ม ๑๓ — มัชฌิมนิกาย มัชฌิมปัณณาสก์ — ๓๙. ธัมมเจติยสูตร — ทรงมอบพระขรรค์แก่ทีฆการายนอำมาตย์",
        ),
    ],
    "ขัตตะ": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-09#4wIneVxGHj",
            "ภาค ๔ เล่ม ๙ — ทีฆนิกาย สีลขันดวรรค — ๔. โสณทัณฑสูตร — มหาอำมาตย์ สนองโอฐ (ขัตตะ)",
        ),
    ],
}

# (หมวด, ชื่อรายการ, คำอธิบาย, การอ้างลิงก์)
# ใช้ r:ชื่อเดิมใน _rulers_legacy_links.json หรือ b:ชื่อเดิมใน _bhikkhu_links_extract.json
SECTIONS: list[tuple[str, str, str, str | None]] = [
    (
        "ก",
        "กัณฑหาลพราหมณ์",
        "(บุคคลในอดีตชาติ/ชาดก) ราชปุโรหิตาจารย์ของพระเจ้าเอกราช ผู้รับสินบนตัดสินคดีไม่เป็นธรรม และเป็นผู้ทูลแนะให้พระราชาตัดพระเศียรพระราชโอรสธิดาเพื่อบูชายัญ",
        "r:กัณฑหาลพราหมณ์",
    ),
    (
        "ก",
        "กัปปินะ (อดีตชาติของพระมหากัปปินเถระ)",
        "(บุคคลในอดีตชาติ) เคยเป็นอำมาตย์ผู้วินิจฉัยอรรถคดีในหังสนคร สมัยพระปทุมุตตรพุทธเจ้า",
        None,
    ),
    (
        "ก",
        "กูฏทันตพราหมณ์",
        "พราหมณ์มหาศาลผู้ครอบครองหมู่บ้านขานุมัตตะ ซึ่งได้รับพระราชทานจากพระเจ้าพิมพิสาร",
        "r:กูฏทันตพราหมณ์",
    ),
    (
        "ข",
        "ขัตตะ",
        "มหาอำมาตย์ผู้ทำหน้าที่สนองโอษฐ์ของโสณทัณฑพราหมณ์แห่งกรุงจัมปา",
        None,
    ),
    (
        "ค",
        "โควินทพราหมณ์",
        "(บุคคลในอดีตชาติ) ปุโรหิตของพระเจ้าทิสัมปติ และเป็นบิดาของโชติปาลมาณพ (มหาโควินทพราหมณ์)",
        "r:มหาโควินทพราหมณ์",
    ),
    (
        "ช",
        "หมอชีวก โกมารภัจจ์",
        "แพทย์ประจำราชสำนักของพระเจ้าพิมพิสาร และเป็นแพทย์ประจำพระองค์พระพุทธเจ้าพร้อมทั้งภิกษุสงฆ์ ได้รับยกย่องให้เป็นเอตทัคคะในทางเลื่อมใสในบุคคล",
        None,
    ),
    (
        "ท",
        "ทีฆการายน (ทีฆการายนอำมาตย์)",
        "มหาอำมาตย์ของพระเจ้าปเสนทิโกศล เป็นผู้ที่พระเจ้าปเสนทิโกศลทรงมอบพระขรรค์และพระอุณหิส (เครื่องราชกกุธภัณฑ์) ให้รักษาไว้ในขณะที่พระองค์เสด็จเข้าไปเฝ้าพระพุทธเจ้าในวิหาร",
        None,
    ),
    (
        "ป",
        "โปกขรสาติพราหมณ์",
        "พราหมณ์มหาศาลผู้ได้รับมอบหมายจากพระเจ้าปเสนทิโกศลให้เป็นผู้ครอบครองเมืองอุกกัฏฐา",
        "r:โปกขรสาติพราหมณ์",
    ),
    (
        "ม",
        "มหาโควินทพราหมณ์ (โชติปาลมาณพ)",
        "(บุคคลในอดีตชาติ) ปุโรหิตของพระเจ้าเรณุ ผู้ถวายอนุสาสน์แด่พระมหากษัตริย์ทั้ง ๗ แคว้น และเป็นผู้จัดการแบ่งราชสมบัติให้กษัตริย์สหาย ๖ พระองค์ ภายหลังได้สละราชสมบัติออกบวช",
        "r:มหาโควินทพราหมณ์",
    ),
    (
        "ม",
        "มโหสธบัณฑิต",
        "(บุคคลในอดีตชาติ/ชาดก) ที่ปรึกษาหนุ่มของพระเจ้าวิเทหะแห่งกรุงมิถิลา เป็นผู้มีความฉลาดรอบคอบ ทรงบำเพ็ญปัญญาบารมี",
        "r:มโหสธบัณฑิต",
    ),
    (
        "ว",
        "วัสสการพราหมณ์",
        "มหาอำมาตย์ผู้ใหญ่แห่งแคว้นมคธ เป็นผู้ที่พระเจ้าอชาตศัตรูส่งไปกราบทูลถามพระพุทธเจ้าเรื่องการปราบแคว้นวัชชี และเป็นผู้ร่วมกับสุนิธพราหมณ์สร้างเมืองยุทธศาสตร์ที่ปาฏลิคามเพื่อป้องกันชาววัชชี",
        "r:วัสสการพราหมณ์",
    ),
    (
        "ว",
        "วิฑูฑภเสนาบดี (วิฏฏุภะ)",
        "พระราชโอรสของพระเจ้าปเสนทิโกศลที่เกิดกับนางวาสภขัตติยา ทรงเคยดำรงตำแหน่งเสนาบดีแห่งแคว้นโกศล",
        "r:วิฑูฑภเสนาบดี",
    ),
    (
        "ว",
        "วิธุรบัณฑิต",
        "(บุคคลในอดีตชาติ/ชาดก) ผู้ถวายคำแนะนำและเป็นที่ปรึกษาประจำราชสำนักของพระเจ้าธนัญชัยโกรัพยะ ทรงบำเพ็ญสัจจบารมี",
        "r:วิธุรบัณฑิต",
    ),
    (
        "ส",
        "สุนิธพราหมณ์",
        "มหาอำมาตย์ชาวมคธ ผู้ร่วมกับวัสสการพราหมณ์สร้างเมืองยุทธศาสตร์ที่ปาฏลิคาม",
        "r:สุนิธพราหมณ์",
    ),
    (
        "ส",
        "สีหเสนาบดี",
        "เสนาบดีแห่งแคว้นวัชชี (กรุงเวสาลี) อดีตเคยเป็นสาวกของนิครนถ์ แต่ภายหลังได้ไปกราบทูลถามปัญหาและฟังธรรมจากพระพุทธเจ้าจนได้ดวงตาเห็นธรรม จึงเปลี่ยนมาเลื่อมใสในพระพุทธศาสนา",
        "r:สีหเสนาบดี",
    ),
    (
        "ส",
        "โสณทัณฑพราหมณ์",
        "พราหมณ์ผู้ได้รับพระราชทานจากพระเจ้าพิมพิสารให้ครอบครองกรุงจัมปา",
        "r:โสณทัณฑพราหมณ์",
    ),
    (
        "อ",
        "อุปนนทเสนาบดี",
        "เสนาบดีที่วัสสการพราหมณ์เข้าไปสอบถามเพื่อยืนยันว่า พระอานนท์เป็นผู้เคารพบูชาภิกษุผู้สมควรและมีคุณธรรมจริงหรือไม่",
        "r:อุปนนทเสนาบดี",
    ),
]

SECTION_IDS = {
    "ก": "p5mamt-G",
    "ข": "p5mamt-KH",
    "ค": "p5mamt-KO",
    "ช": "p5mamt-CH",
    "ท": "p5mamt-T",
    "ป": "p5mamt-P",
    "ม": "p5mamt-M",
    "ว": "p5mamt-W",
    "ส": "p5mamt-S",
    "อ": "p5mamt-A",
}


def resolve_links(
    ruler: dict,
    bhikkhu: dict,
    term: str,
    link_ref: str | None,
) -> list[dict]:
    if link_ref is None:
        if term not in MANUAL:
            raise SystemExit(f"Missing MANUAL for {term}")
        return [dict(x) for x in MANUAL[term]]
    if link_ref.startswith("r:"):
        k = link_ref[2:]
        return merge_links(ruler, k, None)
    if link_ref.startswith("b:"):
        k = link_ref[2:]
        return merge_links(bhikkhu, k, None)
    raise SystemExit(f"Bad link_ref {link_ref!r} for {term}")


def render_entry(links: list[dict], term: str, desc: str) -> str:
    term_esc = term.replace("&", "&amp;").replace('"', "&quot;")
    desc_esc = desc.replace("&", "&amp;").replace('"', "&quot;")
    lines = [f'<PtbWordIndexEntry term="{term_esc}" desc="{desc_esc}">', ""]
    for Ld in links:
        tier = Ld.get("tier", "primary")
        label_esc = Ld["label"].replace("&", "&amp;").replace('"', "&quot;")
        href_esc = Ld["href"].replace("&", "&amp;")
        lines.append("<PtbWordIndexRefs>")
        lines.append(
            f'  <PtbWordIndexLink href="{href_esc}" label="{label_esc}" tier="{tier}" />'
        )
        lines.append("</PtbWordIndexRefs>")
    lines.append("</PtbWordIndexEntry>")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ruler = load_ruler()
    bhikkhu = load_bhikkhu()
    body: list[str] = []
    current: str | None = None
    for sec, term, desc, link_ref in SECTIONS:
        if sec != current:
            if current is not None:
                body.append("")
            sid = SECTION_IDS.get(sec, f"p5mamt-{sec}")
            body.append(f"#### หมวด {sec} {{#{sid} .ptb-h-block}}")
            body.append("")
            current = sec
        links = resolve_links(ruler, bhikkhu, term, link_ref)
        if not links:
            raise SystemExit(f"No links for {term}")
        body.append(render_entry(links, term, desc))
    fm = """---
title: มหาอำมาตย์
lang: th
description: ดัชนีชื่อบุคคล — มหาอำมาตย์ — ภาค ๕ สารบัญค้นคำ พระไตรปิฎกฉบับสำหรับประชาชน
outline: [2, 6]
prev: { text: 'พระราชา', link: '/word-index/persons/rulers/' }
next: { text: 'คฤหบดี เศรษฐี', link: '/word-index/persons/gahapati/' }
searchKeywords:
  - ชื่อบุคคล
  - มหาอำมาตย์
  - เสนาบดี
  - ภาค ๕ สารบัญค้นคำ
---

## มหาอำมาตย์ {#p5mamt-h1 .ptb-h-block}

"""
    out = fm + "\n".join(body)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(out, encoding="utf-8", newline="\n")
    print("Wrote", OUT_PATH, "lines", out.count(chr(10)) + 1)


if __name__ == "__main__":
    main()
