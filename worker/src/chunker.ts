export interface Chunk {
  id: string
  filePath: string
  url: string
  anchor: string
  title: string
  breadcrumb: string[]
  text: string
}

const VUE_COMPONENT_RE =
  /<\/?(?:PtbParagraph|PtbList|PtbListItem|PtbFootnote|PtbSubtitle|PtbTipitakaRef|ImageLightbox)[^>]*>/g
const HTML_TAG_RE = /<\/?[a-z][^>]*>/gi
const ATTRS_RE = /\{[^}]*\}/g
const FRONTMATTER_RE = /^---\n[\s\S]*?\n---\n?/
const HEADING_RE = /^(#{1,6})\s+(.+)$/

function stripVueAndHtml(text: string): string {
  return text
    .replace(VUE_COMPONENT_RE, '')
    .replace(HTML_TAG_RE, '')
    .replace(ATTRS_RE, '')
    .replace(/\*\*/g, '')
    .replace(/__/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function extractHeadingText(raw: string): string {
  return raw
    .replace(/<PtbFootnote>[\s\S]*?<\/PtbFootnote>/g, '')
    .replace(ATTRS_RE, '')
    .replace(/\*\*/g, '')
    .trim()
}

function buildUrl(filePath: string, rewrites: Record<string, string>): string {
  let rel = filePath.replace(/\\/g, '/')
  if (rel.startsWith('docs/')) rel = rel.slice(5)
  const rewritten = rewrites[rel] ?? rel
  return '/' + rewritten.replace(/\/index\.md$/, '/').replace(/\.md$/, '')
}

/**
 * Split a markdown file into chunks by heading boundaries.
 * Each chunk captures text under a heading (or the page intro before the first heading).
 */
export function chunkMarkdown(
  filePath: string,
  content: string,
  rewrites: Record<string, string>,
): Chunk[] {
  const withoutFm = content.replace(FRONTMATTER_RE, '')
  const lines = withoutFm.split('\n')
  const baseUrl = buildUrl(filePath, rewrites)

  const chunks: Chunk[] = []
  let currentLevel = 0
  let currentHeading = ''
  let currentAnchor = ''
  const breadcrumb: string[] = []
  let buffer: string[] = []

  function flush() {
    const text = stripVueAndHtml(buffer.join('\n'))
    if (text.length < 20) {
      buffer = []
      return
    }
    const url = currentAnchor ? `${baseUrl}#${currentAnchor}` : baseUrl
    const id = `${filePath}:${currentAnchor || '_intro'}`
    chunks.push({
      id,
      filePath,
      url,
      anchor: currentAnchor,
      title: currentHeading || filePath,
      breadcrumb: [...breadcrumb],
      text: text.slice(0, 2000),
    })
    buffer = []
  }

  for (const line of lines) {
    const m = line.match(HEADING_RE)
    if (m) {
      flush()
      const level = m[1].length
      const rawHeading = m[2]
      currentLevel = level
      currentHeading = extractHeadingText(rawHeading)

      const anchorMatch = rawHeading.match(/\{#([^\s}]+)/)
      currentAnchor = anchorMatch ? anchorMatch[1] : ''

      while (breadcrumb.length >= level) breadcrumb.pop()
      breadcrumb.push(currentHeading)
    } else {
      buffer.push(line)
    }
  }
  flush()

  return chunks
}
