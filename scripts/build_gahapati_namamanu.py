# -*- coding: utf-8 -*-
"""Build docs/10-part-5-word-index/persons/gahapati/index.md (ดัชนีเศรษฐี คฤหบดี / นามานุกรม)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULER_JSON = ROOT / "scripts" / "_rulers_legacy_links.json"
BHI_JSON = ROOT / "scripts" / "_bhikkhu_links_extract.json"
OUT_PATH = (
    ROOT
    / "docs"
    / "10-part-5-word-index"
    / "persons"
    / "gahapati"
    / "index.md"
)


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


# รายการที่อ้างอิงเอง (ไม่อยู่ใน merge ตาม r:/b: เดียว)
MANUAL: dict[str, list[dict]] = {
    "จุลลกเศรษฐี": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/vol-27#70i3unC6N8",
            "ภาค ๔ เล่ม ๒๗ — ขุททกนิกาย (ขุ.) — เอกนิบาต ชาดก — ๓. จุลลกเสฏฐิชาดก",
        ),
    ],
    "ชาณุสโสณิพราหมณ์": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-12#xixuVaQUXY",
            "ภาค ๔ เล่ม ๑๒ — มัชฌิมนิกาย มูลปัณณาสก์ — โอปัมมวรรค — ๔. ภยเภรวสูตร",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-12#8rrn9q5h9U",
            "ภาค ๔ เล่ม ๑๒ — มัชฌิมนิกาย มูลปัณณาสก์ — ๒๗. จูฬหัตถิปโทปมสูตร",
            _sort=1,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13#HeqjKWqnGU",
            "ภาค ๔ เล่ม ๑๓ — มัชฌิมนิกาย มัชฌิมปัณณาสก์ — ๔๙. สุภสูตร (สุภมาณพบุตรโตเทยยพราหมณ์)",
            _sort=2,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#mnE3911aXJ",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย ติกนิบาต — วรรคที่ ๑ ชื่อพราหมณวรรค — ชาณุสโสณิ / ปัจโจโรหณี / นิพพานที่เห็นได้ด้วยตนเอง (สรุป)",
            _sort=3,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-24#5uxIoYBN3A",
            "ภาค ๔ เล่ม ๒๔ — อังคุตตรนิกาย ทสก - เอกาทสกนิบาต — วรรคที่ ๒ ชื่อชาณุสโสณิวรรค — ปัจโจโรหณี",
            _sort=4,
        ),
    ],
    "ตารุกขพราหมณ์": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-09#gRfIW10FmM",
            "ภาค ๔ เล่ม ๙ — ทีฆนิกาย สีลขันดวรรค — ๑๓. เตวิชชสูตร — พราหมณมหาศาลที่มนสากตะ (รวมตารุกขพราหมณ์)",
        ),
    ],
    "วังกีสพราหมณ์": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/vol-09#gRfIW10FmM",
            "ภาค ๔ เล่ม ๙ — ทีฆนิกาย สีลขันดวรรค — ๑๓. เตวิชชสูตร — พราหมณมหาศาลที่มนสากตะ (รวมวังกีสพราหมณ์)",
        ),
    ],
    "โตเทยยพราหมณ์": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13#HeqjKWqnGU",
            "ภาค ๔ เล่ม ๑๓ — มัชฌิมนิกาย — ๔๙. สุภสูตร (สุภมาณพบุตรโตเทยยพราหมณ์)",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13#jryTrSSZMR",
            "ภาค ๔ เล่ม ๑๓ — มัชฌิมนิกาย — ๕๐. สคารวสูตร — ป่ามะม่วงของโตเทยยพราหมณ์ ณ ปัจจลกัปปะ",
            _sort=1,
        ),
    ],
    "ทสมะ, คฤหบดี (ชาวเมืองอัฏฐกะ)": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13#YAjVG1umTK",
            "ภาค ๔ เล่ม ๑๓ — มัชฌิมนิกาย — ๒. อัฏฐกนาครสูตร (ทสมะ คฤหบดีชาวอัฏฐกะ)",
        ),
    ],
    "ธนัญชานิพราหมณ์": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-13#Wonha2bv3O",
            "ภาค ๔ เล่ม ๑๓ — มัชฌิมนิกาย — ๔๗. ธนัญชานิสูตร",
        ),
    ],
    "เปขุณิยเศรษฐี (หรือ เขณิยเศรษฐี)": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#KOAXAGZb4Z",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย ติกนิบาต — มหาวรรค — พระนันทกะ สาฬหะ โรหนะ เปขุณิยเศรษฐี (สรุป)",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-14#TfITAXHwzT",
            "ภาค ๔ เล่ม ๑๔ — มัชฌิมนิกาย — ๔๖. นันทโกวาทสูตร",
            _sort=1,
        ),
    ],
    "มิคารเศรษฐี": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#TKcSgfdRaR",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย — เอตทัคคปาลิ — นางวิสาขา มิคารมาตา (อ้างถึงมิคารเศรษฐี)",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#KOAXAGZb4Z",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย ติกนิบาต — มหาวรรค — สาฬหะ หลานมิคารเศรษฐี (สรุป)",
            _sort=1,
        ),
    ],
    "เมณฑกเศรษฐี (หรือ เมณฑกคฤหบดี)": [
        L(
            "/part-4-tipitaka-digest/vinaya-pitaka/vol-05#QFY2hsBTLg",
            "ภาค ๔ เล่ม ๕ — วินัยปิฎก — มหาขันธกะ — ทรงแสดงธรรมโปรดเมณฑกคฤหบดี",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/vinaya-pitaka/vol-05#VNVHhxlmKP",
            "ภาค ๔ เล่ม ๕ — วินัยปิฎก — มหาขันธกะ — ทรงอนุญาตตามที่เมณฑกคฤหบดีขอร้อง (ปัญจโครส)",
            _sort=1,
        ),
    ],
    "ราชคหเศรษฐี": [
        L(
            "/part-4-tipitaka-digest/vinaya-pitaka/vol-07#E92bWjDSKH",
            "ภาค ๔ เล่ม ๗ — วินัยปิฎก — มหาขันธกะ — ทรงอนุญาตที่อยู่ ๕ ชนิด — เศรษฐีกรุงราชคฤห์ถวายวิหาร / อนาถปิณฑิก ทราบข่าวพุทธอุบัติ",
        ),
    ],
    "นางวิสาขา": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#TKcSgfdRaR",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย — เอตทัคคะฝ่ายอุบาสิกา — นางวิสาขา มิคารมาตา (ถวายทาน)",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-12#sXIUUADUvH",
            "ภาค ๔ เล่ม ๑๒ — มัชฌิมนิกาย — ๓๗. จูฬตัณหาสังขยสูตร — ปราสาทของนางวิสาขา บุพพาราม",
            _sort=1,
        ),
        L(
            "/part-4-tipitaka-digest/vinaya-pitaka/vol-05#9MOv9lqmWx",
            "ภาค ๔ เล่ม ๕ — วินัยปิฎก — มหาขันธกะ — นางวิสาขาขอพร ๘ ประการ",
            _sort=2,
        ),
        L(
            "/part-4-tipitaka-digest/vinaya-pitaka/vol-07#Gulp2eOZ9q",
            "ภาค ๔ เล่ม ๗ — วินัยปิฎก — ปาฏิโมกขฐปนขันธกะ — ปราสาทที่นางวิสาขา (อุโบสถ ปาฏิโมกข์)",
            _sort=3,
        ),
    ],
    "หัตถกะ อาฬวกะ": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#ZhZSpEXwan",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย — เอตทัคคะฝ่ายอุบาสก — หัตถกะ อาฬวกะ (สงเคราะห์บริษัทด้วยสังคหวัตถุ ๔)",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#VwbP5h8hGG",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย ติกนิบาต — เทวทูตวรรค — ตอบหัตถกะ อาฬวกะ เรื่องการบรรทมเป็นสุข / อริยทรัพย์ ๗",
            _sort=1,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-23#LSryFSSaMg",
            "ภาค ๔ เล่ม ๒๓ — อังคุตตรนิกาย — อัฏฐกนิบาต — สรรเสริญหัตถกะ สงเคราะห์บริษัท ๔ / อัศจรรย์ ๘",
            _sort=2,
        ),
    ],
    "อนาถปิณฑิกเศรษฐี / อนาถปิณฑิกคฤหบดี (สุทัตตะ)": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/vol-14#iqGJgmkET8",
            "ภาค ๔ เล่ม ๑๔ — มัชฌิมนิกาย — ๔๓. อนาถปิณฑิโกวาทสูตร",
            _sort=0,
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#ZhZSpEXwan",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย — เอตทัคคะฝ่ายอุบาสก — อนาถปิณฑิกะ (สุทัตตะ) ถวายทาน",
            _sort=1,
        ),
        L(
            "/part-4-tipitaka-digest/vinaya-pitaka/vol-07#snwJPPqq1j",
            "ภาค ๔ เล่ม ๗ — วินัยปิฎก — อนาถปิณฑิกคฤหบดี — เลื่อมใส สร้างเชตวนาราม",
            _sort=2,
        ),
        L(
            "/part-4-tipitaka-digest/vinaya-pitaka/vol-07#aYHewvBlaI",
            "ภาค ๔ เล่ม ๗ — วินัยปิฎก — การถวายเชตวนาราม",
            _sort=3,
        ),
    ],
    "อุคคคฤหบดี (ชาวกรุงเวสาลี)": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#ZhZSpEXwan",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย — เอตทัคคะฝ่ายอุบาสก — อุคคะ คฤหบดี ชาวกรุงเวสาลี (ถวายของที่ชอบใจ)",
        ),
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-23#LSryFSSaMg",
            "ภาค ๔ เล่ม ๒๓ — อังคุตตรนิกาย — อัฏฐกนิบาต — อุคคคฤหบดีชาวเวสาลี — ความอัศจรรย์ ๘ ประการ",
        ),
    ],
    "อุคคคฤหบดี (ชาวหัตถิคาม)": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-23#LSryFSSaMg",
            "ภาค ๔ เล่ม ๒๓ — อังคุตตรนิกาย — อัฏฐกนิบาต — อุคคคฤหบดีชาวหัตถิคาม (ทำนองเช่นเวสาลี)",
        ),
    ],
    "อุคคตะคฤหบดี": [
        L(
            "/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-20#ZhZSpEXwan",
            "ภาค ๔ เล่ม ๒๐ — อังคุตตรนิกาย — เอตทัคคะฝ่ายอุบาสก — อุคคตะ คฤหบดี (อุปัฏฐากพระสงฆ์)",
        ),
    ],
}

# (หมวด, ชื่อรายการ, คำอธิบาย, การอ้างลิงก์: "r:คีย์" / "b:คีย์" / None แล้วใช้ MANUAL[term])
SECTIONS: list[tuple[str, str, str, str | None]] = [
    (
        "ก",
        "กูฏทันตพราหมณ์",
        "พราหมณ์ผู้มั่งคั่งที่ครอบครองหมู่บ้านพราหมณ์ชื่อขานุมัตตะ ซึ่งได้รับพระราชทานจากพระเจ้าพิมพิสาร ท่านเป็นผู้เตรียมโภคทรัพย์และสัตว์จำนวนมากเพื่อประกอบมหายัญ แต่เมื่อได้ฟังธรรมจากพระพุทธเจ้า จึงเลื่อมใสและเปลี่ยนวิธีการบูชายัญเป็นการให้ทานและรักษาศีลแทน",
        "r:กูฏทันตพราหมณ์",
    ),
    (
        "จ",
        "จังกีพราหมณ์",
        "พราหมณมหาศาล (พราหมณ์ผู้มั่งคั่งมีทรัพย์มาก) ที่มีชื่อเสียง เป็นผู้ครอบครองหมู่บ้านพราหมณ์ชื่อโอปาสาทะ ซึ่งได้รับพระราชทานจากพระเจ้าปเสนทิโกศล และเคยอาศัยอยู่ในหมู่บ้านชื่ออิจฉานังคละ",
        "r:จังกีพราหมณ์",
    ),
    (
        "จ",
        "จุลลกเศรษฐี",
        "(บุคคลในอดีตชาติ/ชาดก) เศรษฐีผู้มีปัญญาพิจารณาเหตุผล ย่อมสามารถตั้งตนได้ด้วยทรัพย์อันเป็นต้นทุนแม้น้อย เหมือนคนก่อไฟกองน้อยให้เป็นกองใหญ่",
        None,
    ),
    (
        "ช",
        "ชาณุสโสณิพราหมณ์",
        "พราหมณมหาศาลผู้มีชื่อเสียง พักอาศัยอยู่ในตำบลบ้านมนสากตะ และกรุงสาวัตถี เป็นผู้มั่งคั่งที่เคยนั่งรถเทียมด้วยม้าขาวไปเฝ้าพระพุทธเจ้า และได้เข้าเฝ้าเพื่อสนทนาธรรมหลายครั้ง เช่น เรื่องปัจโจโรหณี (การก้าวลงจากบาป) และเรื่องนิพพานที่เห็นได้ด้วยตนเอง",
        None,
    ),
    (
        "ต",
        "ตารุกขพราหมณ์",
        "พราหมณมหาศาลผู้มีชื่อเสียง พักอาศัยอยู่ในตำบลบ้านพราหมณ์ชื่อมนสากตะ",
        None,
    ),
    (
        "ต",
        "โตเทยยพราหมณ์",
        "พราหมณมหาศาลผู้มีชื่อเสียง พักอาศัยอยู่ในตำบลบ้านมนสากตะ ท่านมีป่ามะม่วงเป็นของตนอันเป็นที่ซึ่งพระผู้มีพระภาคเคยเสด็จแวะประทับ และเป็นบิดาของสุภมาณพ",
        None,
    ),
    (
        "ท",
        "ทสมะ, คฤหบดี (ชาวเมืองอัฏฐกะ)",
        "คฤหบดีผู้มั่งคั่ง ผู้เดินทางไปหาพระอานนท์เพื่อถามถึงธรรมที่ทำให้สิ้นอาสวะ เมื่อได้ฟังธรรมแล้วเกิดความชื่นชม จึงได้สร้างวิหาร ๕๐๐ แห่งถวายแด่พระอานนท์ และได้นิมนต์ภิกษุชาวกรุงปาตลิบุตรและชาวเวสาลีประชุมกันเพื่อถวายทานอย่างมโหฬาร",
        None,
    ),
    (
        "ธ",
        "ธนัญชานิพราหมณ์",
        "พราหมณ์ผู้มีทรัพย์แต่ประมาท อาศัยพระราชาปล้นพราหมณ์คฤหบดี และอาศัยพราหมณ์คฤหบดีปล้นพระราชาเพื่อแสวงหาทรัพย์ ภายหลังป่วยหนักได้ฟังธรรมจากพระสาริบุตร และเมื่อสิ้นชีวิตได้ไปเกิดในพรหมโลก",
        None,
    ),
    (
        "ป",
        "เปขุณิยเศรษฐี (หรือ เขณิยเศรษฐี)",
        "เศรษฐีผู้เป็นปู่หรือตาของโรหนะ ผู้ซึ่งพระนันทกะได้ปรารภเทศนาสอนมิให้เชื่อถือสิ่งใดเพียงเพราะฟังตามๆ กันมา",
        None,
    ),
    (
        "ป",
        "โปกขรสาติพราหมณ์",
        "พราหมณมหาศาลผู้มีชื่อเสียง พักอาศัยอยู่ในตำบลบ้านมนสากตะ เป็นผู้มั่งคั่งที่ได้รับพระราชทานจากพระเจ้าปเสนทิโกศลให้ครอบครองหมู่บ้านอิจฉานังคละ (เมืองอุกกัฏฐา) ภายหลังได้เข้าเฝ้าและฟังธรรมจนได้ดวงตาเห็นธรรม จึงประกาศตนพร้อมครอบครัวและบริวารเป็นอุบาสก",
        "r:โปกขรสาติพราหมณ์",
    ),
    (
        "ม",
        "มิคารเศรษฐี",
        "เศรษฐีผู้เป็นบิดาสามีของนางวิสาขา (อันเป็นที่มาของชื่อ \"มิคารมาตา\" ของนางวิสาขา) ท่านมีหลานชายชื่อสาฬหะ",
        None,
    ),
    (
        "ม",
        "เมณฑกเศรษฐี (หรือ เมณฑกคฤหบดี)",
        "เศรษฐีชาวภัททิยนคร ผู้มีความมั่งคั่งและมีหลานชายชื่ออุคคหะ ท่านเป็นผู้กราบทูลขอและได้รับพระพุทธานุญาตให้ภิกษุรับเสบียงเดินทางและของ ๕ อย่างที่เกิดจากโค (ปัญจโครส) ได้",
        None,
    ),
    (
        "ร",
        "ราชคหเศรษฐี",
        "เศรษฐีแห่งเมืองราชคฤห์ ผู้เป็นพี่ภริยา (พี่เขย) ของอนาถปิณฑิกเศรษฐี ท่านเป็นผู้มั่งคั่งที่จัดเตรียมภัตตาหารอย่างมโหฬารถวายแด่พระพุทธเจ้า อันเป็นต้นเหตุให้อนาถปิณฑิกเศรษฐีได้ทราบข่าวการอุบัติขึ้นของพระพุทธเจ้า",
        None,
    ),
    (
        "ว",
        "วังกีสพราหมณ์",
        "พราหมณมหาศาลผู้มีชื่อเสียง พักอาศัยอยู่ในตำบลบ้านพราหมณ์ชื่อมนสากตะ",
        None,
    ),
    (
        "ว",
        "นางวิสาขา",
        "มหาอุบาสิกาผู้มีความมั่งคั่ง ได้สร้างปราสาทถวายในบุพพาราม นางได้รับยกย่องจากพระพุทธเจ้าให้เป็นเอตทัคคะฝ่ายอุบาสิกาในทางถวายทาน",
        None,
    ),
    (
        "ส",
        "โสณทัณฑพราหมณ์",
        "พราหมณ์ผู้มั่งคั่งที่ได้รับพระราชทานจากพระเจ้าพิมพิสารให้ครองกรุงจัมปา ท่านเป็นผู้มีทรัพย์มากและมีอิทธิพลจนมีผู้มาเรียนมนต์ด้วยเป็นจำนวนมาก ท่านได้สนทนาธรรมกับพระพุทธเจ้าและยอมรับว่าคุณสมบัติที่แท้จริงของพราหมณ์คือศีลและปัญญา",
        "r:โสณทัณฑพราหมณ์",
    ),
    (
        "ห",
        "หัตถกะ อาฬวกะ",
        "คฤหบดีผู้มั่งคั่งแห่งเมืองอาฬวี ผู้ได้รับยกย่องให้เป็นเอตทัคคะฝ่ายอุบาสกในทางสงเคราะห์บริษัทด้วยสังคหวัตถุ ๔ พระพุทธเจ้าตรัสสรรเสริญว่าท่านประกอบด้วยอริยทรัพย์ ๗ ประการและมีความปรารถนาน้อย",
        None,
    ),
    (
        "อ",
        "อนาถปิณฑิกเศรษฐี / อนาถปิณฑิกคฤหบดี (สุทัตตะ)",
        "เศรษฐีชาวกรุงสาวัตถี ผู้มีทรัพย์มั่งคั่ง ท่านได้สละทรัพย์ซื้อสวนของราชกุมารเชตสร้าง \"เชตวนาราม\" ถวายไว้ในพระพุทธศาสนา ท่านได้รับยกย่องให้เป็นเอตทัคคะฝ่ายอุบาสกในทางถวายทาน",
        None,
    ),
    (
        "อ",
        "อุคคคฤหบดี (ชาวกรุงเวสาลี)",
        "คฤหบดีผู้มั่งคั่ง ผู้ได้รับยกย่องให้เป็นเอตทัคคะฝ่ายอุบาสกในทางถวายของที่ชอบใจ ท่านมีภรรยาสาวถึง ๔ คน และได้สละทรัพย์สินรวมถึงยอมยกภรรยาให้บุรุษอื่นโดยไม่มีจิตผิดปกติ ถือว่าโภคทรัพย์ในตระกูลตนเป็นของสาธารณะสำหรับผู้มีศีล",
        None,
    ),
    (
        "อ",
        "อุคคคฤหบดี (ชาวหัตถิคาม)",
        "คฤหบดีผู้มั่งคั่งและประกอบด้วยความอัศจรรย์ ๘ ประการ ทำนองเดียวกับอุคคคฤหบดีชาวกรุงเวสาลี",
        None,
    ),
    (
        "อ",
        "อุคคตะคฤหบดี",
        "คฤหบดีผู้มีกำลังทรัพย์รับใช้พระพุทธศาสนา ได้รับยกย่องให้เป็นเอตทัคคะฝ่ายอุบาสกในทางอุปัฏฐาก (รับใช้) พระสงฆ์",
        None,
    ),
]

SECTION_IDS = {
    "ก": "p5gah-G",
    "จ": "p5gah-J",
    "ช": "p5gah-CH",
    "ต": "p5gah-DTA",
    "ท": "p5gah-DTH",
    "ธ": "p5gah-DT2",
    "ป": "p5gah-P",
    "ม": "p5gah-M",
    "ร": "p5gah-R",
    "ว": "p5gah-W",
    "ส": "p5gah-S",
    "ห": "p5gah-H",
    "อ": "p5gah-A",
}


def resolve_links(
    ruler: dict,
    bhikkhu: dict,
    term: str,
    link_ref: str | None,
) -> list[dict]:
    if link_ref is None:
        if term not in MANUAL:
            raise SystemExit(f"Missing MANUAL for {term!r}")
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
            sid = SECTION_IDS.get(sec, f"p5gah-{sec}")
            body.append(f"#### หมวด {sec} {{#{sid} .ptb-h-block}}")
            body.append("")
            current = sec
        links = resolve_links(ruler, bhikkhu, term, link_ref)
        if not links:
            raise SystemExit(f"No links for {term}")
        body.append(render_entry(links, term, desc))
    fm = """---
title: เศรษฐี คฤหบดี
lang: th
description: ดัชนีชื่อบุคคล — เศรษฐี คฤหบดี — ภาค ๕ สารบัญค้นคำ พระไตรปิฎกฉบับสำหรับประชาชน
outline: [2, 6]
prev: { text: 'มหาอำมาตย์', link: '/word-index/persons/maha-amatya/' }
next: { text: 'อุบาสก', link: '/word-index/persons/upasaka/' }
searchKeywords:
  - ชื่อบุคคล
  - เศรษฐี
  - คฤหบดี
  - เศรษฐี คฤหบดี
  - ภาค ๕ สารบัญค้นคำ
---

## เศรษฐี คฤหบดี {#p5gah-h1 .ptb-h-block}

"""
    out = fm + "\n".join(body)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(out, encoding="utf-8", newline="\n")
    print("Wrote", OUT_PATH, "lines", out.count(chr(10)) + 1)


if __name__ == "__main__":
    main()
