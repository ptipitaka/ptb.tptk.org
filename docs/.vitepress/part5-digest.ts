import type { DefaultTheme } from 'vitepress'

const WI = '10-part-5-academic-notes-and-index/word-index'
const WI_URL = 'part-5-academic-notes-and-index/word-index'

/** หน้าย่อยภายใต้สารบัญค้นคำ — ชื่อบุคคล */
const wordIndexPersonsSubpages = [
  'buddha',
  'thera',
  'theri',
  'rulers',
  'upasaka',
  'upasika',
  'devas',
  'sect-leaders',
] as const

const wordIndexCategories = [
  'key-doctrines',
  'doctrinal-terms',
  'persons',
  'events',
  'scriptures',
  'vinaya-terms',
  'places',
  'cosmology',
  'jataka-and-perfections',
  'tipitaka-history',
] as const

/** rewrites: โฟลเดอร์ docs ใช้ prefix 10- เรียงหลังภาค ๔ — URL ไม่มีเลขนำ */
export function part5DigestRewrites(): Record<string, string> {
  const rewrites: Record<string, string> = {
    '10-part-5-academic-notes-and-index/index.md':
      'part-5-academic-notes-and-index/index.md',
    '10-part-5-academic-notes-and-index/on-academic-notes/index.md':
      'part-5-academic-notes-and-index/on-academic-notes/index.md',
    [`${WI}/index.md`]: `${WI_URL}/index.md`,
  }
  for (const cat of wordIndexCategories) {
    rewrites[`${WI}/${cat}/index.md`] = `${WI_URL}/${cat}/index.md`
  }
  for (const slug of wordIndexPersonsSubpages) {
    rewrites[`${WI}/persons/${slug}/index.md`] =
      `${WI_URL}/persons/${slug}/index.md`
  }
  return rewrites
}

export function part5DigestSidebar(): DefaultTheme.SidebarItem {
  return {
    text: 'ภาค ๕ บันทึกทางวิชาการและสารบัญค้นคำ',
    collapsed: true,
    items: [
      { text: 'เกริ่นนำ', link: '/part-5-academic-notes-and-index/' },
      {
        text: 'ว่าด้วยบันทึกทางวิชาการ',
        link: '/part-5-academic-notes-and-index/on-academic-notes/',
      },
      {
        text: 'สารบัญค้นคำ',
        link: `/${WI_URL}/`,
        collapsed: true,
        items: [
          {
            text: '๑. หลักธรรมสำคัญ',
            link: `/${WI_URL}/key-doctrines/`,
          },
          {
            text: '๒. ศัพท์ธรรมะ',
            link: `/${WI_URL}/doctrinal-terms/`,
          },
          {
            text: '๓. ชื่อบุคคล',
            link: `/${WI_URL}/persons/`,
            collapsed: true,
            items: [
              {
                text: 'พระพุทธเจ้า',
                link: `/${WI_URL}/persons/buddha/`,
              },
              {
                text: 'พระเถระ',
                link: `/${WI_URL}/persons/thera/`,
              },
              {
                text: 'พระเถรี',
                link: `/${WI_URL}/persons/theri/`,
              },
              {
                text: 'ผู้ครองนคร',
                link: `/${WI_URL}/persons/rulers/`,
              },
              {
                text: 'อุบาสก',
                link: `/${WI_URL}/persons/upasaka/`,
              },
              {
                text: 'อุบาสิกา',
                link: `/${WI_URL}/persons/upasika/`,
              },
              {
                text: 'เทวดา',
                link: `/${WI_URL}/persons/devas/`,
              },
              {
                text: 'เจ้าลัทธิ',
                link: `/${WI_URL}/persons/sect-leaders/`,
              },
            ],
          },
          {
            text: '๔. ชื่อสถานที่',
            link: `/${WI_URL}/places/`,
          },
          {
            text: '๕. เหตุการณ์สำคัญ',
            link: `/${WI_URL}/events/`,
          },
          {
            text: '๖. ชื่อคัมภีร์',
            link: `/${WI_URL}/scriptures/`,
          },
          {
            text: '๗. ศัพท์เกี่ยวกับพระวินัย',
            link: `/${WI_URL}/vinaya-terms/`,
          },
          {
            text: '๘. จักรวาลวิทยาและสังสารวัฏ',
            link: `/${WI_URL}/cosmology/`,
          },
          {
            text: '๙. ชาดก อดีตชาติ และบารมี',
            link: `/${WI_URL}/jataka-and-perfections/`,
          },
          {
            text: '๑๐. บุคคลในประวัติศาสตร์',
            link: `/${WI_URL}/tipitaka-history/`,
          },
        ],
      },
    ],
  }
}
