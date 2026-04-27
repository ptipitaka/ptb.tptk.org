import type { DefaultTheme } from 'vitepress'

const WI = '10-part-5-word-index'
const WI_URL = 'word-index'

/** หน้าย่อยภายใต้ภาค ๕ สารบัญค้นคำ — ชื่อบุคคล */
const wordIndexPersonsSubpages = [
  'buddha',
  'bhikkhu',
  'bhikkhuni',
  'rulers',
  'maha-amatya',
  'gahapati',
  'upasaka',
  'upasika',
  'devas',
  'other-sects',
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

/** rewrites: บันทึกทางวิชาการ — โฟลเดอร์ 11-on-academic-notes */
export function onAcademicNotesRewrites(): Record<string, string> {
  return {
    '11-on-academic-notes/index.md': 'on-academic-notes/index.md',
  }
}

/** rewrites: ภาค ๕ สารบัญค้นคำ — โฟลเดอร์ 10-part-5-word-index */
export function wordIndexRewrites(): Record<string, string> {
  const rewrites: Record<string, string> = {
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

export function onAcademicNotesSidebar(): DefaultTheme.SidebarItem {
  return {
    text: 'ว่าด้วยบันทึกทางวิชาการ',
    link: '/on-academic-notes/',
  }
}

export function wordIndexSidebar(): DefaultTheme.SidebarItem {
  return {
    text: 'ภาค ๕ สารบัญค้นคำ',
    collapsed: true,
    items: [
      { text: 'เกริ่นนำ', link: `/${WI_URL}/` },
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
            text: 'พระภิกษุ',
            link: `/${WI_URL}/persons/bhikkhu/`,
          },
          {
            text: 'พระภิกษุณี',
            link: `/${WI_URL}/persons/bhikkhuni/`,
          },
          {
            text: 'พระราชา',
            link: `/${WI_URL}/persons/rulers/`,
          },
          {
            text: 'มหาอำมาตย์',
            link: `/${WI_URL}/persons/maha-amatya/`,
          },
          {
            text: 'เศรษฐี คฤหบดี',
            link: `/${WI_URL}/persons/gahapati/`,
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
            text: 'บุคคลในลัทธิอื่น',
            link: `/${WI_URL}/persons/other-sects/`,
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
  }
}
