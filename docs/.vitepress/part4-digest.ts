import type { DefaultTheme } from 'vitepress'
import volumeTitles from './part4-volume-titles.json'

export const part4VolumeTitles: readonly string[] = volumeTitles

export type Part4PitakaSlug = 'vinaya-pitaka' | 'sutta-pitaka' | 'abhidhamma-pitaka'

/** นิกายย่อยของสุตตันตปิฎก (เล่ม ๙–๓๓) — โฟลเดอร์ตาม slug เดียวกับภาค ๓ */
export type Part4SuttaNikayaSlug =
  | 'digha-nikaya'
  | 'majjhima-nikaya'
  | 'samyutta-nikaya'
  | 'anguttara-nikaya'
  | 'khuddaka-nikaya'

/** เล่ม ๑–๘ วินัย, ๙–๓๓ สุตตันตะ, ๓๔–๔๕ อภิธัมมะ */
export function part4PitakaForVolume(volumeOneBased: number): Part4PitakaSlug {
  if (volumeOneBased >= 1 && volumeOneBased <= 8) return 'vinaya-pitaka'
  if (volumeOneBased >= 9 && volumeOneBased <= 33) return 'sutta-pitaka'
  if (volumeOneBased >= 34 && volumeOneBased <= 45) return 'abhidhamma-pitaka'
  throw new Error(`part4: volume out of range 1–45 (${volumeOneBased})`)
}

/** เล่ม ๙–๑๑ ทีฆ, ๑๒–๑๔ มัชฌิม, ๑๕–๑๙ สังยุตตะ, ๒๐–๒๔ อังคุตตระ, ๒๕–๓๓ ขุททกะ */
export function part4SuttaNikayaForVolume(volumeOneBased: number): Part4SuttaNikayaSlug {
  if (volumeOneBased >= 9 && volumeOneBased <= 11) return 'digha-nikaya'
  if (volumeOneBased >= 12 && volumeOneBased <= 14) return 'majjhima-nikaya'
  if (volumeOneBased >= 15 && volumeOneBased <= 19) return 'samyutta-nikaya'
  if (volumeOneBased >= 20 && volumeOneBased <= 24) return 'anguttara-nikaya'
  if (volumeOneBased >= 25 && volumeOneBased <= 33) return 'khuddaka-nikaya'
  throw new Error(`part4: not a sutta volume (${volumeOneBased})`)
}

function volumeItems(fromVol: number, toVol: number): DefaultTheme.SidebarItem[] {
  const items: DefaultTheme.SidebarItem[] = []
  for (let v = fromVol; v <= toVol; v++) {
    items.push({ text: part4VolumeTitles[v - 1], link: volLink(v) })
  }
  return items
}

export function part4DigestRewrites(): Record<string, string> {
  const out: Record<string, string> = {
    '09-part-4-tipitaka-digest/index.md': 'part-4-tipitaka-digest/index.md',
    '09-part-4-tipitaka-digest/vinaya-pitaka/vinaya-structure.md':
      'part-4-tipitaka-digest/vinaya-pitaka/vinaya-structure.md',
    '09-part-4-tipitaka-digest/sutta-pitaka/suttanta-structure.md':
      'part-4-tipitaka-digest/sutta-pitaka/suttanta-structure.md',
    '09-part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/digha-structure.md':
      'part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/digha-structure.md',
    '09-part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/majjhima-structure.md':
      'part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/majjhima-structure.md',
    '09-part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/samyutta-structure.md':
      'part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/samyutta-structure.md',
    '09-part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/anguttara-structure.md':
      'part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/anguttara-structure.md',
    '09-part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/khuddaka-structure.md':
      'part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/khuddaka-structure.md',
    '09-part-4-tipitaka-digest/abhidhamma-pitaka/abhidhamma-structure.md':
      'part-4-tipitaka-digest/abhidhamma-pitaka/abhidhamma-structure.md',
    '09-part-4-tipitaka-digest/abhidhamma-pitaka/abhidhamma-explanation.md':
      'part-4-tipitaka-digest/abhidhamma-pitaka/abhidhamma-explanation.md',
    '09-part-4-tipitaka-digest/abhidhamma-pitaka/7-books-of-abhidhamma.md':
      'part-4-tipitaka-digest/abhidhamma-pitaka/7-books-of-abhidhamma.md',
  }
  for (let v = 1; v <= 45; v++) {
    const pitaka = part4PitakaForVolume(v)
    const num = String(v).padStart(2, '0')
    if (pitaka === 'sutta-pitaka') {
      const nikaya = part4SuttaNikayaForVolume(v)
      const rel = `part-4-tipitaka-digest/sutta-pitaka/${nikaya}/vol-${num}.md`
      out[`09-part-4-tipitaka-digest/sutta-pitaka/${nikaya}/vol-${num}.md`] = rel
    } else {
      const rel = `part-4-tipitaka-digest/${pitaka}/vol-${num}.md`
      out[`09-part-4-tipitaka-digest/${pitaka}/vol-${num}.md`] = rel
    }
  }
  return out
}

function volLink(volumeOneBased: number): string {
  const pitaka = part4PitakaForVolume(volumeOneBased)
  const num = String(volumeOneBased).padStart(2, '0')
  if (pitaka === 'sutta-pitaka') {
    const nikaya = part4SuttaNikayaForVolume(volumeOneBased)
    return `/part-4-tipitaka-digest/sutta-pitaka/${nikaya}/vol-${num}`
  }
  return `/part-4-tipitaka-digest/${pitaka}/vol-${num}`
}

const SUTTA_NIKAYA_SIDEBAR: { text: string; from: number; to: number }[] = [
  { text: 'ทีฆนิกาย', from: 9, to: 11 },
  { text: 'มัชฌิมนิกาย', from: 12, to: 14 },
  { text: 'สังยุตตนิกาย', from: 15, to: 19 },
  { text: 'อังคุตตรนิกาย', from: 20, to: 24 },
  { text: 'ขุททกนิกาย', from: 25, to: 33 },
]

export function part4DigestSidebar(): DefaultTheme.SidebarItem {
  const vinayaItems: DefaultTheme.SidebarItem[] = [
    {
      text: 'แผนภูมิวินัยปิฎก',
      link: '/part-4-tipitaka-digest/vinaya-pitaka/vinaya-structure',
    },
    ...volumeItems(1, 8),
  ]
  const suttaItems: DefaultTheme.SidebarItem[] = [
    {
      text: 'แผนภูมิสุตตันตปิฎก',
      link: '/part-4-tipitaka-digest/sutta-pitaka/suttanta-structure',
    },
    ...SUTTA_NIKAYA_SIDEBAR.map(({ text, from, to }) => {
      const vols = volumeItems(from, to)
      if (from === 9 && to === 11) {
        return {
          text,
          collapsed: true,
          items: [
            {
              text: 'แผนภูมิทีฆนิกาย',
              link: '/part-4-tipitaka-digest/sutta-pitaka/digha-nikaya/digha-structure',
            },
            ...vols,
          ],
        }
      }
      if (from === 12 && to === 14) {
        return {
          text,
          collapsed: true,
          items: [
            {
              text: 'แผนภูมิมัชฌิมนิกาย',
              link: '/part-4-tipitaka-digest/sutta-pitaka/majjhima-nikaya/majjhima-structure',
            },
            ...vols,
          ],
        }
      }
      if (from === 15 && to === 19) {
        return {
          text,
          collapsed: true,
          items: [
            {
              text: 'แผนภูมิสังยุตตนิกาย',
              link: '/part-4-tipitaka-digest/sutta-pitaka/samyutta-nikaya/samyutta-structure',
            },
            ...vols,
          ],
        }
      }
      if (from === 20 && to === 24) {
        return {
          text,
          collapsed: true,
          items: [
            {
              text: 'แผนภูมิอังคุตตรนิกาย',
              link: '/part-4-tipitaka-digest/sutta-pitaka/anguttara-nikaya/anguttara-structure',
            },
            ...vols,
          ],
        }
      }
      if (from === 25 && to === 33) {
        return {
          text,
          collapsed: true,
          items: [
            {
              text: 'แผนภูมิขุททกนิกาย',
              link: '/part-4-tipitaka-digest/sutta-pitaka/khuddaka-nikaya/khuddaka-structure',
            },
            ...vols,
          ],
        }
      }
      return { text, collapsed: true, items: vols }
    }),
  ]
  const abhidhammaItems: DefaultTheme.SidebarItem[] = [
    {
      text: 'แผนภูมิอภิธัมมปิฎก',
      link: '/part-4-tipitaka-digest/abhidhamma-pitaka/abhidhamma-structure',
    },
    {
      text: 'คำอธิบายอภิธรรมปิฎก',
      link: '/part-4-tipitaka-digest/abhidhamma-pitaka/abhidhamma-explanation',
    },
    {
      text: 'อภิธรรม ๗ คัมภีร์',
      link: '/part-4-tipitaka-digest/abhidhamma-pitaka/7-books-of-abhidhamma',
    },
    ...volumeItems(34, 45),
  ]
  return {
    text: 'ภาค ๔ ความย่อแห่งพระไตรปิฎก',
    collapsed: true,
    items: [
      { text: 'เกริ่นนำ', link: '/part-4-tipitaka-digest/' },
      {
        text: 'วินัยปิฎก',
        collapsed: true,
        items: vinayaItems,
      },
      {
        text: 'สุตตันตปิฎก',
        collapsed: true,
        items: suttaItems,
      },
      {
        text: 'อภิธัมมปิฎก',
        collapsed: true,
        items: abhidhammaItems,
      },
    ],
  }
}
