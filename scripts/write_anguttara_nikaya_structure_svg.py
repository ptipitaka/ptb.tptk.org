# Writes UTF-8 SVG for Anguttara Nikaya digest chart (11 nipatas).
# Layout: title → trunk line → horizontal bar on top; stems drop down; dot at stem end;
# odd nipatas = shorter stem + upper text row; even = longer stem + lower text row.
# Each label: 3 lines — name / ชุมนุมธรรมะ / ที่มี N ข้อ
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/public/images/09-part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya-structure.svg"

# (ชื่อนิบาต, เลขไทย, เล่ม, แถวสั้น=True แถวยาว=False)
NIPATAS = [
    ("เอกนิบาต", "๑", 20, True),
    ("ทุกนิบาต", "๒", 20, False),
    ("ติกนิบาต", "๓", 20, True),
    ("จตุกกนิบาต", "๔", 21, False),
    ("ปัญจกนิบาต", "๕", 22, True),
    ("ฉักกนิบาต", "๖", 22, False),
    ("สัตตกนิบาต", "๗", 23, True),
    ("อัฏฐกนิบาต", "๘", 23, False),
    ("นวกนิบาต", "๙", 23, True),
    ("ทสกนิบาต", "๑๐", 24, False),
    ("เอกาทสกนิบาต", "๑๑", 24, True),
]

GAP = 96
CX0 = 78
CX_LAST = CX0 + 10 * GAP
ROOT_X = (CX0 + CX_LAST) // 2

# แถบแนวนอน (ลำต้น) — อยู่ใต้หัวเรื่อง
TITLE_Y = 32
STEM_TITLE = 48
TRUNK_Y = 76
# แท่งสั้น (แถวบน ๑ ๓ ๕ …) / แท่งยาว (แถวล่าง ๒ ๔ ๖ …)
SHORT_STEM_LEN = 28
LONG_STEM_LEN = 104
# ระยะจากจุดถึงบรรทัดแรกของข้อความ
TEXT_AFTER_DOT = 18
LINE_GAP = 19


def build_svg() -> str:
    lines: list[str] = []
    vb_w = 1155
    vb_h = 258
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="12 4 {vb_w} {vb_h}" preserveAspectRatio="xMinYMid meet" '
        f'role="img" aria-labelledby="title desc">'
    )
    lines.append('  <title id="title">แผนภูมิอังคุตตรนิกาย</title>')
    lines.append(
        '  <desc id="desc">อังคุตตรนิกาย สิบเอ็ดนิบาต '
        'ตามลำดับฉบับพระไตรปิฎกฉบับประชาชน</desc>'
    )
    lines.append("  <style>")
    lines.append("    text {")
    lines.append('      fill: #1f2937;')
    lines.append('      font-family: "Sarabun", "TH Sarabun New", "Tahoma", sans-serif;')
    lines.append("      text-anchor: middle;")
    lines.append("    }")
    lines.append("    .root { font-size: 28px; font-weight: 700; }")
    lines.append("    .head { font-size: 24px; font-weight: 700; }")
    lines.append(
        "    .detail { font-size: 23px; font-weight: 400; fill: #6b7280; "
        "text-anchor: middle; }"
    )
    lines.append(
        "    .line { stroke: #6b7280; stroke-width: 1.35; "
        "stroke-linecap: round; fill: none; }"
    )
    lines.append("    a { text-decoration: none; }")
    lines.append("    a:hover text { fill: #1d4ed8; text-decoration: underline; }")
    lines.append("    a:hover text.detail { fill: #1d4ed8; }")
    lines.append("  </style>")
    lines.append("")
    lines.append('  <a href="/tipitaka-structure/#suttanta" target="_top">')
    lines.append(f'    <text x="{ROOT_X}" y="{TITLE_Y}" class="root">อังคุตตรนิกาย</text>')
    lines.append("  </a>")
    lines.append(
        f'  <line x1="{ROOT_X}" y1="{STEM_TITLE}" x2="{ROOT_X}" y2="{TRUNK_Y}" class="line" />'
    )
    lines.append(
        f'  <line x1="{CX0}" y1="{TRUNK_Y}" x2="{CX_LAST}" y2="{TRUNK_Y}" class="line" />'
    )

    for i, (name, digit, vol, short_row) in enumerate(NIPATAS):
        cx = CX0 + i * GAP
        href = f"/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/vol-{vol:02d}/"
        stem_len = SHORT_STEM_LEN if short_row else LONG_STEM_LEN
        y_dot = TRUNK_Y + stem_len
        y_head = y_dot + TEXT_AFTER_DOT
        y_mid = y_head + LINE_GAP
        y_bot = y_mid + LINE_GAP
        lines.append(
            f'  <line x1="{cx}" y1="{TRUNK_Y}" x2="{cx}" y2="{y_dot}" class="line" />'
        )
        lines.append(f'  <circle cx="{cx}" cy="{y_dot}" r="1.8" fill="#6b7280" />')
        lines.append(f'  <a href="{href}" target="_top">')
        lines.append(f'    <text x="{cx}" y="{y_head}" class="head">{name}</text>')
        lines.append(f'    <text x="{cx}" y="{y_mid}" class="detail">ชุมนุมธรรมะ</text>')
        lines.append(f'    <text x="{cx}" y="{y_bot}" class="detail">ที่มี {digit} ข้อ</text>')
        lines.append("  </a>")

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_svg(), encoding="utf-8", newline="\n")
    print("Wrote", OUT)
