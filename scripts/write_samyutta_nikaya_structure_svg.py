# One-off emitter: writes UTF-8 SVG (avoids toolchain mangling Thai in .svg writes).
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/public/images/09-part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya-structure.svg"

SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="112 0 1228 718" preserveAspectRatio="xMinYMid meet" role="img" aria-labelledby="title desc">
  <title id="title">แผนภูมิสังยุตตนิกาย</title>
  <desc id="desc">สังยุตตนิกาย ห้าวรรค ห้าสิบหกสังยุตต์ ตามลำดับฉบับพระไตรปิฎกฉบับประชาชน</desc>
  <style>
    text {
      fill: #1f2937;
      font-family: "Sarabun", "TH Sarabun New", "Tahoma", sans-serif;
      text-anchor: middle;
    }
    .root { font-size: 24px; font-weight: 700; }
    .head { font-size: 17px; font-weight: 700; }
    .detail { font-size: 17px; font-weight: 400; fill: #6b7280; text-anchor: start; }
    .line { stroke: #6b7280; stroke-width: 1.35; stroke-linecap: round; fill: none; }
    a { text-decoration: none; }
    a:hover text { fill: #1d4ed8; text-decoration: underline; }
  </style>

  <a href="/tipitaka-structure/#suttanta" target="_top">
    <text x="660" y="34" class="root">สังยุตตนิกาย</text>
  </a>

  <line x1="660" y1="42" x2="660" y2="86" class="line" />
  <line x1="220" y1="86" x2="1100" y2="86" class="line" />

  <line x1="220" y1="86" x2="220" y2="114" class="line" />
  <circle cx="220" cy="114" r="1.7" fill="#6b7280" />
  <line x1="440" y1="86" x2="440" y2="114" class="line" />
  <circle cx="440" cy="114" r="1.7" fill="#6b7280" />
  <line x1="660" y1="86" x2="660" y2="114" class="line" />
  <circle cx="660" cy="114" r="1.7" fill="#6b7280" />
  <line x1="880" y1="86" x2="880" y2="114" class="line" />
  <circle cx="880" cy="114" r="1.7" fill="#6b7280" />
  <line x1="1100" y1="86" x2="1100" y2="114" class="line" />
  <circle cx="1100" cy="114" r="1.7" fill="#6b7280" />

  <a href="/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-15/" target="_top">
    <text x="220" y="142" class="head">สคาถวรรค</text>
  </a>
  <text x="118" y="182" class="detail">&#8226; เทวตาสังยุตต์</text>
  <text x="118" y="222" class="detail">&#8226; เทวปุตตสังยุตต์</text>
  <text x="118" y="262" class="detail">&#8226; โกสลสังยุตต์</text>
  <text x="118" y="302" class="detail">&#8226; มารสังยุตต์</text>
  <text x="118" y="342" class="detail">&#8226; ภิกขุนีสังยุตต์</text>
  <text x="118" y="382" class="detail">&#8226; พรหมสังยุตต์</text>
  <text x="118" y="422" class="detail">&#8226; พราหมณสังยุตต์</text>
  <text x="118" y="462" class="detail">&#8226; วังคีสสังยุตต์</text>
  <text x="118" y="502" class="detail">&#8226; วนสังยุตต์</text>
  <text x="118" y="542" class="detail">&#8226; ยักขสังยุตต์</text>
  <text x="118" y="582" class="detail">&#8226; สักกสังยุตต์</text>

  <a href="/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-16/" target="_top">
    <text x="440" y="142" class="head">นิทานวรรค</text>
  </a>
  <text x="338" y="182" class="detail">&#8226; อภิสมยสังยุตต์</text>
  <text x="338" y="222" class="detail">&#8226; ธาตุสังยุตต์</text>
  <text x="338" y="262" class="detail">&#8226; อนมตัคคสังยุตต์</text>
  <text x="338" y="302" class="detail">&#8226; กัสสปสังยุตต์</text>
  <text x="338" y="342" class="detail">&#8226; ลาภสักการสังยุตต์</text>
  <text x="338" y="382" class="detail">&#8226; ราหุลสังยุตต์</text>
  <text x="338" y="422" class="detail">&#8226; ลักขณสังยุตต์</text>
  <text x="338" y="462" class="detail">&#8226; โอปัมมสังยุตต์</text>
  <text x="338" y="502" class="detail">&#8226; ภิกขุสังยุตต์</text>

  <a href="/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-17/" target="_top">
    <text x="660" y="142" class="head">ขันธวารวรรค</text>
  </a>
  <text x="558" y="182" class="detail">&#8226; ขันธสังยุตต์</text>
  <text x="558" y="222" class="detail">&#8226; ราธสังยุตต์</text>
  <text x="558" y="262" class="detail">&#8226; ทิฏฐิสังยุตต์</text>
  <text x="558" y="302" class="detail">&#8226; โอกกันตสังยุตต์</text>
  <text x="558" y="342" class="detail">&#8226; อุปปาทสังยุตต์</text>
  <text x="558" y="382" class="detail">&#8226; กิเลสสังยุตต์</text>
  <text x="558" y="422" class="detail">&#8226; สาริปุตตสังยุตต์</text>
  <text x="558" y="462" class="detail">&#8226; นาคสังยุตต์</text>
  <text x="558" y="502" class="detail">&#8226; สุปัณณสังยุตต์</text>
  <text x="558" y="542" class="detail">&#8226; คันธัพพกายสังยุตต์</text>
  <text x="558" y="582" class="detail">&#8226; วลาหกสังยุตต์</text>
  <text x="558" y="622" class="detail">&#8226; วัจฉโคตตสังยุตต์</text>
  <text x="558" y="662" class="detail">&#8226; สมาธิสังยุตต์</text>

  <a href="/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-18/" target="_top">
    <text x="880" y="142" class="head">สฬายตนวรรค</text>
  </a>
  <text x="778" y="182" class="detail">&#8226; สฬายตนสังยุตต์</text>
  <text x="778" y="222" class="detail">&#8226; เวทนาสังยุตต์</text>
  <text x="778" y="262" class="detail">&#8226; มาตุคามสังยุตต์</text>
  <text x="778" y="302" class="detail">&#8226; ชัมพุขาทกสังยุตต์</text>
  <text x="778" y="342" class="detail">&#8226; สามัณฑกสังยุตต์</text>
  <text x="778" y="382" class="detail">&#8226; โมคคัลลานสังยุตต์</text>
  <text x="778" y="422" class="detail">&#8226; จิตตคหปติปุจฌาสังยุตต์</text>
  <text x="778" y="462" class="detail">&#8226; คามณิสังยุตต์</text>
  <text x="778" y="502" class="detail">&#8226; อสังขตสังยุตต์</text>
  <text x="778" y="542" class="detail">&#8226; อัพยากตสังยุตต์</text>

  <a href="/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/vol-19/" target="_top">
    <text x="1100" y="142" class="head">มหาวารวรรค</text>
  </a>
  <text x="998" y="182" class="detail">&#8226; มัคคสังยุตต์</text>
  <text x="998" y="222" class="detail">&#8226; โพชฌงคสังยุตต์</text>
  <text x="998" y="262" class="detail">&#8226; สติปัฏฐานสังยุตต์</text>
  <text x="998" y="302" class="detail">&#8226; อินทรียสังยุตต์</text>
  <text x="998" y="342" class="detail">&#8226; สัมมัปปธานสังยุตต์</text>
  <text x="998" y="382" class="detail">&#8226; พลสังยุตต์</text>
  <text x="998" y="422" class="detail">&#8226; อิทธิปาทสังยุตต์</text>
  <text x="998" y="462" class="detail">&#8226; อนุรุทธสังยุตต์</text>
  <text x="998" y="502" class="detail">&#8226; ฌานสังยุตต์</text>
  <text x="998" y="542" class="detail">&#8226; อานาปานสังยุตต์</text>
  <text x="998" y="582" class="detail">&#8226; โสตาปัตติสังยุตต์</text>
  <text x="998" y="622" class="detail">&#8226; สัจจสังยุตต์</text>
</svg>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(SVG, encoding="utf-8", newline="\n")
    print("Wrote", OUT)
