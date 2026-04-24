import { defineConfig } from 'vitepress'
import attrs from 'markdown-it-attrs'
import { part4DigestRewrites, part4DigestSidebar } from './part4-digest'
import {
  onAcademicNotesRewrites,
  onAcademicNotesSidebar,
  wordIndexRewrites,
  wordIndexSidebar,
} from './part5-digest'

/**
 * Thai + Pali tokenizer — INDEX side (lightweight, no n-grams).
 *
 * Uses Intl.Segmenter('th') for Thai word boundaries.
 * For Pali compounds (detected by tiny fragments ≤ 2 codepoints),
 * emits the full compound + suffix compounds at segment boundaries
 * to allow prefix matching without bloating the index with n-grams.
 *
 * VitePress serialises this function via toString() + eval in a Web Worker,
 * so everything must be inlined — no outer-scope references.
 */
function thaiIndexTokenize(text: string): string[] {
  const c = thaiIndexTokenize as any
  if (!c._w) c._w = new Intl.Segmenter('th', { granularity: 'word' })
  const wseg: Intl.Segmenter = c._w
  const THAI_RE = /[\u0E00-\u0E7F]/
  const tokens: string[] = []

  function flushGroup(group: string[]) {
    if (group.length === 0) return
    if (group.length === 1) {
      tokens.push(group[0])
      return
    }
    const compound = group.join('')
    const hasTinyFragment = group.some(p => [...p].length <= 2)
    if (hasTinyFragment) {
      tokens.push(compound)
      for (let start = 1; start < group.length; start++) {
        const suffix = group.slice(start).join('')
        if ([...suffix].length >= 4) tokens.push(suffix)
      }
    } else {
      for (const p of group) tokens.push(p)
      tokens.push(compound)
    }
  }

  let thaiGroup: string[] = []
  for (const s of wseg.segment(text)) {
    if (s.isWordLike) {
      const word = s.segment.toLowerCase()
      if (THAI_RE.test(word)) {
        thaiGroup.push(word)
        continue
      }
      flushGroup(thaiGroup)
      thaiGroup = []
      tokens.push(word)
    } else {
      flushGroup(thaiGroup)
      thaiGroup = []
    }
  }
  flushGroup(thaiGroup)
  return tokens
}

/**
 * Thai + Pali tokenizer — SEARCH (query) side.
 *
 * Splits on whitespace/punctuation only — keeps typed queries like
 * "โสณกุฏิกัณณะ" as a single token for prefix matching.
 * Includes \p{M} (combining marks) so Thai vowels/tones stay attached.
 */
function thaiSearchTokenize(text: string): string[] {
  const SPLIT = /[^\p{L}\p{N}\p{M}]+/u
  const tokens: string[] = []
  for (const word of text.split(SPLIT)) {
    if (word) tokens.push(word.toLowerCase())
  }
  return tokens
}

export default defineConfig({
  markdown: {
    config(md) {
      md.use(attrs)
    },
  },
  title: 'พระไตรปิฎกฉบับสำหรับประชาชน',
  description: 'พระไตรปิฎกฉบับสำหรับประชาชน (PTF 4th Edition) — เว็บหนังสือ',
  lang: 'th',
  base: '/',
  srcDir: '.',
  vite: {
    resolve: {
      // Avoid Windows realpath drive-letter case mismatch during VitePress page import resolution.
      preserveSymlinks: true,
    },
  },
  rewrites: {
    '00-speech-of-appreciation/index.md': 'speech-of-appreciation/index.md',
    '01-preface/index.md': 'preface/index.md',
    '02-introduction/index.md': 'introduction/index.md',
    '03-buddhist-council-illustration/index.md': 'buddhist-council-illustration/index.md',
    '04-tipitaka-structure/index.md': 'tipitaka-structure/index.md',
    '05-abbreviations/index.md': 'abbreviations/index.md',
    '06-part-1-knowledge-of-the-tipitaka/what-is-the-tipitaka/index.md':
      'part-1-knowledge-of-the-tipitaka/what-is-the-tipitaka/index.md',
    '06-part-1-knowledge-of-the-tipitaka/buddhist-councils/index.md':
      'part-1-knowledge-of-the-tipitaka/buddhist-councils/index.md',
    '06-part-1-knowledge-of-the-tipitaka/structure-of-each-pitaka/index.md':
      'part-1-knowledge-of-the-tipitaka/structure-of-each-pitaka/index.md',
    '07-part-2-historical-documents/index.md': 'part-2-historical-documents/index.md',
    '07-part-2-historical-documents/section-1/index.md':
      'part-2-historical-documents/section-1/index.md',
    '07-part-2-historical-documents/section-2/index.md':
      'part-2-historical-documents/section-2/index.md',
    '07-part-2-historical-documents/section-3/index.md':
      'part-2-historical-documents/section-3/index.md',
    '08-part-3-tipitaka-selected-passages/index.md': 'part-3-tipitaka-selected-passages/index.md',
    '08-part-3-tipitaka-selected-passages/vinaya-pitaka/index.md':
      'part-3-tipitaka-selected-passages/vinaya-pitaka/index.md',
    '08-part-3-tipitaka-selected-passages/digha-nikaya/index.md':
      'part-3-tipitaka-selected-passages/digha-nikaya/index.md',
    '08-part-3-tipitaka-selected-passages/majjhima-nikaya/index.md':
      'part-3-tipitaka-selected-passages/majjhima-nikaya/index.md',
    '08-part-3-tipitaka-selected-passages/samyutta-nikaya/index.md':
      'part-3-tipitaka-selected-passages/samyutta-nikaya/index.md',
    '08-part-3-tipitaka-selected-passages/anguttara-nikaya/index.md':
      'part-3-tipitaka-selected-passages/anguttara-nikaya/index.md',
    '08-part-3-tipitaka-selected-passages/khuddaka-nikaya/index.md':
      'part-3-tipitaka-selected-passages/khuddaka-nikaya/index.md',
    '08-part-3-tipitaka-selected-passages/abhidhamma-pitaka/index.md':
      'part-3-tipitaka-selected-passages/abhidhamma-pitaka/index.md',
    ...part4DigestRewrites(),
    ...onAcademicNotesRewrites(),
    ...wordIndexRewrites(),
    '12-biography-sujib-punyanubhab/index.md': 'biography-sujib-punyanubhab/index.md',
    '13-working-committee/index.md': 'working-committee/index.md',
    '14-peoples-tipitaka-foundation/index.md': 'peoples-tipitaka-foundation/index.md',
  },
  themeConfig: {
    outline: 'deep',
    outlineTitle: 'ในหน้านี้',
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: 'ค้นหา', buttonAriaLabel: 'ค้นหา' },
          modal: {
            displayDetails: 'แสดงรายละเอียด',
            resetButtonTitle: 'ล้างการค้นหา',
            backButtonTitle: 'ปิดการค้นหา',
            noResultsText: 'ไม่พบผลลัพธ์สำหรับ',
            footer: {
              selectText: 'เลือก',
              navigateText: 'นำทาง',
              closeText: 'ปิด',
            },
          },
        },
        miniSearch: {
          options: {
            tokenize: thaiIndexTokenize,
          },
          searchOptions: {
            fuzzy: false,
            prefix: true,
            combineWith: 'AND',
            boost: { title: 10, titles: 8, text: 1 },
            tokenize: thaiSearchTokenize,
          },
        },
      },
    },
    sidebar: [
      { text: 'หน้าหลัก', link: '/' },
      { text: 'พระคติธรรม', link: '/speech-of-appreciation/' },
      { text: 'คำปรารภ', link: '/preface/' },
      { text: 'คำนำ', link: '/introduction/' },
      { text: 'ภาพการสังคายนา', link: '/buddhist-council-illustration/' },
      { text: 'แผนภูมิพระไตรปิฎก', link: '/tipitaka-structure/' },
      { text: 'อักษรย่อชื่อคัมภีร์', link: '/abbreviations/' },
      {
        text: 'ภาค ๑ ความรู้เรื่องพระไตรปิฎก',
        collapsed: true,
        items: [
          {
            text: 'พระไตรปิฎกคืออะไร',
            link: '/part-1-knowledge-of-the-tipitaka/what-is-the-tipitaka/',
          },
          {
            text: 'การสังคายนา',
            link: '/part-1-knowledge-of-the-tipitaka/buddhist-councils/',
          },
          {
            text: 'การจัดหมวดหมู่ของแต่ละปิฎก',
            link: '/part-1-knowledge-of-the-tipitaka/structure-of-each-pitaka/',
          },
        ],
      },
      {
        text: 'ภาค ๒ ว่าด้วยเอกสารทางประวัติศาสตร์',
        collapsed: true,
        items: [
          { text: 'เกริ่นนำ', link: '/part-2-historical-documents/' },
          {
            text: 'ส่วนที่ ๑ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๑',
            link: '/part-2-historical-documents/section-1/',
          },
          {
            text: 'ส่วนที่ ๒ เอกสารที่เกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๕',
            link: '/part-2-historical-documents/section-2/',
          },
          {
            text: 'ส่วนที่ ๓ เอกสารเกี่ยวกับพระไตรปิฎก ในรัชกาลที่ ๗',
            link: '/part-2-historical-documents/section-3/',
          },
        ],
      },
      {
        text: 'ภาค ๓ ข้อความน่ารู้จากพระไตรปิฎก',
        collapsed: true,
        items: [
          { text: 'เกริ่นนำ', link: '/part-3-tipitaka-selected-passages/' },
          {
            text: 'วินัยปิฎก (วิ.)',
            link: '/part-3-tipitaka-selected-passages/vinaya-pitaka/',
          },
          {
            text: 'ทีฆนิกาย (ที.)',
            link: '/part-3-tipitaka-selected-passages/digha-nikaya/',
          },
          {
            text: 'มัชฌิมนิกาย (ม.)',
            link: '/part-3-tipitaka-selected-passages/majjhima-nikaya/',
          },
          {
            text: 'สังยุตตนิกาย (สํ.)',
            link: '/part-3-tipitaka-selected-passages/samyutta-nikaya/',
          },
          {
            text: 'อังคุตตรนิกาย (องฺ.)',
            link: '/part-3-tipitaka-selected-passages/anguttara-nikaya/',
          },
          {
            text: 'ขุททกนิกาย (ขุ.)',
            link: '/part-3-tipitaka-selected-passages/khuddaka-nikaya/',
          },
          {
            text: 'อภิธรรมปิฎก (อภิ.)',
            link: '/part-3-tipitaka-selected-passages/abhidhamma-pitaka/',
          },
        ],
      },
      part4DigestSidebar(),
      wordIndexSidebar(),
      onAcademicNotesSidebar(),
      {
        text: 'ประวัติสังเขป อาจารย์สุชีพ',
        link: '/biography-sujib-punyanubhab/',
      },
      {
        text: 'คณะทำงาน',
        link: '/working-committee/',
      },
      {
        text: 'มูลนิธิพระไตรปิฎกเพื่อประชาชน',
        link: '/peoples-tipitaka-foundation/',
      },
    ],
  },
  head: [
    ['link', { rel: 'icon', type: 'image/png', href: '/favicon.png', sizes: '32x32' }],
    ['link', { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { href: 'https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap', rel: 'stylesheet' }],
  ],
})
