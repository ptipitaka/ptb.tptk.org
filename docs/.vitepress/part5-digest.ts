import type { DefaultTheme } from 'vitepress'

const WI = '10-part-5-academic-notes-and-index/word-index'
const WI_URL = 'part-5-academic-notes-and-index/word-index'

const wordIndexCategories = [
  'key-doctrines',
  'doctrinal-terms',
  'persons',
  'events',
  'scriptures',
  'vinaya-terms',
  'places',
  'cosmology',
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
            text: '๒. คำศัพท์เกี่ยวกับหลักธรรม',
            link: `/${WI_URL}/doctrinal-terms/`,
          },
          {
            text: '๓. ชื่อบุคคล',
            link: `/${WI_URL}/persons/`,
          },
          {
            text: '๔. เหตุการณ์สำคัญ',
            link: `/${WI_URL}/events/`,
          },
          {
            text: '๕. ชื่อคัมภีร์และชื่อเรื่อง',
            link: `/${WI_URL}/scriptures/`,
          },
          {
            text: '๖. ศัพท์เกี่ยวกับพระวินัย',
            link: `/${WI_URL}/vinaya-terms/`,
          },
          {
            text: '๗. ชื่อสถานที่',
            link: `/${WI_URL}/places/`,
          },
          {
            text: '๘. จักรวาลวิทยาและสังสารวัฏ',
            link: `/${WI_URL}/cosmology/`,
          },
        ],
      },
    ],
  }
}
