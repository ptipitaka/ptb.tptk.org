import DefaultTheme from 'vitepress/theme'
import './custom.css'
import '../../05-abbreviations/custom.css'
import Layout from './Layout.vue'
import ImageLightbox from './components/ImageLightbox.vue'
import PtbFootnote from './components/PtbFootnote.vue'
import PtbParagraph from './components/PtbParagraph.vue'
import PtbSubtitle from './components/PtbSubtitle.vue'
import PtbTipitakaRef from './components/PtbTipitakaRef.vue'
import PtbList from './components/PtbList.vue'
import PtbListItem from './components/PtbListItem.vue'
import PtbRandomPitakaLink from './components/PtbRandomPitakaLink.vue'
import PtbWordIndexEntry from './components/PtbWordIndexEntry.vue'
import PtbWordIndexLink from './components/PtbWordIndexLink.vue'
import PtbWordIndexRefs from './components/PtbWordIndexRefs.vue'

/** โหลด custom.css ของแต่ละหน้า (โหลดหลัง central จึง override ได้) — เพิ่ม entry เมื่อมี custom.css ในโฟลเดอร์นั้น */
const PAGE_CUSTOM_CSS: Record<string, () => Promise<unknown>> = {
  '': () => import('../../index/custom.css'),
  'tipitaka-structure': () => import('../../04-tipitaka-structure/custom.css'),
  'abbreviations': () => import('../../05-abbreviations/custom.css'),
  '05-abbreviations': () => import('../../05-abbreviations/custom.css'),
}

/** โหลด CSS เฉพาะ path ย่อย (เพิ่ม entry เมื่อมี custom.css ในโฟลเดอร์ย่อย) */
const PAGE_CUSTOM_CSS_BY_PATH_PREFIX: [string, () => Promise<unknown>][] = [
  [
    '/word-index',
    () =>
      import(
        '../../10-part-5-word-index/custom.css'
      ),
  ],
  [
    '/part-2-historical-documents/section-3',
    () => import('../../07-part-2-historical-documents/section-3/custom.css'),
  ],
  [
    '/part-4-tipitaka-digest/vinaya-pitaka',
    () => import('../../09-part-4-tipitaka-digest/vinaya-pitaka/custom.css'),
  ],
  [
    '/part-4-tipitaka-digest/sutta-pitaka',
    () => import('../../09-part-4-tipitaka-digest/sutta-pitaka/custom.css'),
  ],
  [
    '/part-4-tipitaka-digest/abhidhamma-pitaka',
    () => import('../../09-part-4-tipitaka-digest/abhidhamma-pitaka/custom.css'),
  ],
]

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app, router }) {
    app.component('ImageLightbox', ImageLightbox)
    app.component('PtbFootnote', PtbFootnote)
    app.component('PtbParagraph', PtbParagraph)
    app.component('PtbSubtitle', PtbSubtitle)
    app.component('PtbTipitakaRef', PtbTipitakaRef)
    app.component('PtbList', PtbList)
    app.component('PtbListItem', PtbListItem)
    app.component('PtbRandomPitakaLink', PtbRandomPitakaLink)
    app.component('PtbWordIndexEntry', PtbWordIndexEntry)
    app.component('PtbWordIndexLink', PtbWordIndexLink)
    app.component('PtbWordIndexRefs', PtbWordIndexRefs)

    /** VitePress router ใช้ `route` ไม่มี `currentRoute` — ต้องอ่าน path จากนั้นหรือจาก href หลังนำทาง */
    const loadPageCss = (href?: string) => {
      const pathname = href
        ? new URL(href, 'http://a.com').pathname
        : (router.route?.path ?? '')
      const normalized =
        pathname.replace(/\/$/, '') || '/'
      const segment = pathname.replace(/^\/|\/$/g, '').split('/')[0] || ''
      const loader = PAGE_CUSTOM_CSS[segment]
      if (loader) void loader()
      for (const [prefix, subLoader] of PAGE_CUSTOM_CSS_BY_PATH_PREFIX) {
        if (
          normalized === prefix ||
          normalized.startsWith(`${prefix}/`)
        ) {
          void subLoader()
        }
      }
    }
    loadPageCss()
    router.onAfterRouteChanged = loadPageCss
  },
}
