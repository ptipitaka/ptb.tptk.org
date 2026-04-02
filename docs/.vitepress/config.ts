import { defineConfig } from 'vitepress'
import { pagefindPlugin } from 'vitepress-plugin-pagefind'
import attrs from 'markdown-it-attrs'
import { part4DigestRewrites, part4DigestSidebar } from './part4-digest'
import { part5DigestRewrites, part5DigestSidebar } from './part5-digest'

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
  // ให้ URL ไม่มี prefix 00- แต่โฟลเดอร์ยังใช้ 00- สำหรับเรียงลำดับ
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
    ...part5DigestRewrites(),
    '11-biography-sujib-punyanubhab/index.md': 'biography-sujib-punyanubhab/index.md',
    '12-working-committee/index.md': 'working-committee/index.md',
    '13-peoples-tipitaka-foundation/index.md': 'peoples-tipitaka-foundation/index.md',
  },
  vite: {
    publicDir: 'public',
    plugins: [
      pagefindPlugin({
        forceLanguage: 'th',
        btnPlaceholder: 'ค้นหา',
        placeholder: 'ค้นหาในหนังสือ',
        emptyText: 'ไม่พบผลลัพธ์',
        heading: 'พบ {{searchResult}} รายการ',
      }),
    ],
  },
  themeConfig: {
    // ค่าเริ่มต้น = h2–h6; ถ้า frontmatter ใส่ outline: [2, 3] จะถูกจำกัดเฉพาะช่วงนั้น (ทับค่านี้)
    outline: 'deep',
    outlineTitle: 'ในหน้านี้',
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
      part5DigestSidebar(),
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
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { href: 'https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap', rel: 'stylesheet' }],
  ],
})
