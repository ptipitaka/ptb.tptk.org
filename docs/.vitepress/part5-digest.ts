import type { DefaultTheme } from 'vitepress'

/** rewrites: โฟลเดอร์ docs ใช้ prefix 10- เรียงหลังภาค ๔ — URL ไม่มีเลขนำ */
export function part5DigestRewrites(): Record<string, string> {
  return {
    '10-part-5-academic-notes-and-index/index.md':
      'part-5-academic-notes-and-index/index.md',
    '10-part-5-academic-notes-and-index/on-academic-notes/index.md':
      'part-5-academic-notes-and-index/on-academic-notes/index.md',
    '10-part-5-academic-notes-and-index/word-index/index.md':
      'part-5-academic-notes-and-index/word-index/index.md',
  }
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
        link: '/part-5-academic-notes-and-index/word-index/',
      },
    ],
  }
}
