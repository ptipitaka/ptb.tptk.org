import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const root = path.join(__dirname, '..')
const src = path.join(root, 'part1-4-https-urls.txt')
const out = path.join(root, 'part1-4-page-urls.txt')

const text = fs.readFileSync(src, 'utf8')
const set = new Set()
for (const line of text.split(/\r?\n/)) {
  const t = line.trim()
  if (!t.startsWith('https://')) continue
  set.add(t.split('#')[0])
}
const all = [...set]

function partOf(url) {
  if (url.includes('/part-1-')) return 1
  if (url.includes('/part-2-')) return 2
  if (url.includes('/part-3-')) return 3
  if (url.includes('/part-4-')) return 4
  return 0
}

const byPart = { 1: [], 2: [], 3: [], 4: [] }
for (const u of all) {
  const p = partOf(u)
  if (p) byPart[p].push(u)
}
for (const p of [1, 2, 3, 4]) {
  byPart[p].sort((a, b) => a.localeCompare(b, 'en'))
}

const date = new Date().toISOString().slice(0, 10)
const lines = [
  '# พระไตรปิฎกฉบับสำหรับประชาชน — URL ทุกหน้า (ระดับ page) ภาค ๑–๔',
  '# ฐาน: https://ptb.tptk.org',
  '# ไม่รวม anchor (#...); รวมจาก part1-4-https-urls.txt',
  `# สร้างเมื่อ: ${date}`,
  `# รวม ${all.length} หน้า`,
  '',
  `## ภาค ๑ ความรู้เรื่องพระไตรปิฎก (${byPart[1].length} หน้า)`,
  ...byPart[1],
  '',
  `## ภาค ๒ ว่าด้วยเอกสารทางประวัติศาสตร์ (${byPart[2].length} หน้า)`,
  ...byPart[2],
  '',
  `## ภาค ๓ ข้อความน่ารู้จากพระไตรปิฎก (${byPart[3].length} หน้า)`,
  ...byPart[3],
  '',
  `## ภาค ๔ บทคัดย่อพระไตรปิฎก ๔๕ เล่ม (${byPart[4].length} หน้า)`,
  ...byPart[4],
  '',
]

fs.writeFileSync(out, lines.join('\n'), 'utf8')
console.log('Wrote', out)
console.log('total', all.length, 'by part:', [1, 2, 3, 4].map((p) => byPart[p].length))
