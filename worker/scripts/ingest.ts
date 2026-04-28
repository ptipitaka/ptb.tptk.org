/**
 * Ingest script — reads all docs/*.md files, chunks them,
 * generates embeddings via Gemini, and outputs a static JSON
 * file at docs/public/chat-index.json for client-side search.
 *
 * Usage:
 *   GEMINI_API_KEY=... npx tsx scripts/ingest.ts
 */

import { readFileSync, readdirSync, statSync, writeFileSync, mkdirSync } from 'fs'
import { join, relative } from 'path'
import { chunkMarkdown, type Chunk } from '../src/chunker'

const GEMINI_API_KEY = env('GEMINI_API_KEY')
const EMBEDDING_MODEL = 'gemini-embedding-001'
const EMBEDDING_DIMS = 768
const BATCH_SIZE = 20
const DOCS_DIR = join(__dirname, '..', '..', 'docs')
const OUTPUT_DIR = join(DOCS_DIR, 'public')
const OUTPUT_FILE = join(OUTPUT_DIR, 'chat-index.json')

function env(name: string): string {
  const v = process.env[name]
  if (!v) throw new Error(`Missing env: ${name}`)
  return v
}

function collectMdFiles(dir: string): string[] {
  const results: string[] = []
  for (const entry of readdirSync(dir)) {
    if (entry === '.vitepress' || entry === 'node_modules' || entry === 'public') continue
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) {
      results.push(...collectMdFiles(full))
    } else if (entry.endsWith('.md')) {
      results.push(full)
    }
  }
  return results
}

function buildRewrites(): Record<string, string> {
  const map: Record<string, string> = {
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
    '12-biography-sujib-punyanubhab/index.md': 'biography-sujib-punyanubhab/index.md',
    '13-working-committee/index.md': 'working-committee/index.md',
    '14-peoples-tipitaka-foundation/index.md': 'peoples-tipitaka-foundation/index.md',
  }

  const part6WordIndex = '10-part-5-word-index'
  const part6WordIndexUrl = 'word-index'
  const part6WordIndexCategories = [
    'key-doctrines',
    'doctrinal-terms',
    'persons',
    'scriptures',
    'vinaya-terms',
    'places',
  ] as const
  const part6WordIndexPersons = [
    'buddha',
    'bhikkhu',
    'bhikkhuni',
    'rulers',
    'gahapati',
    'upasaka',
    'upasika',
    'devas',
    'other-sects',
  ] as const

  map['11-on-academic-notes/index.md'] = 'on-academic-notes/index.md'
  map[`${part6WordIndex}/index.md`] = `${part6WordIndexUrl}/index.md`
  for (const cat of part6WordIndexCategories) {
    map[`${part6WordIndex}/${cat}/index.md`] = `${part6WordIndexUrl}/${cat}/index.md`
  }
  for (const slug of part6WordIndexPersons) {
    map[`${part6WordIndex}/persons/${slug}/index.md`] =
      `${part6WordIndexUrl}/persons/${slug}/index.md`
  }

  const suttaNikayaMap: Record<string, [number, number]> = {
    'digha-nikaya': [9, 11],
    'majjhima-nikaya': [12, 14],
    'samyutta-nikaya': [15, 19],
    'anguttara-nikaya': [20, 24],
    'khuddaka-nikaya': [25, 33],
  }

  for (const pitaka of ['vinaya-pitaka', 'sutta-pitaka', 'abhidhamma-pitaka']) {
    const base = `09-part-4-tipitaka-digest/${pitaka}`
    const target = `part-4-tipitaka-digest/${pitaka}`
    map[`${base}/${pitaka.replace('-pitaka', '')}-structure.md`] =
      `${target}/${pitaka.replace('-pitaka', '')}-structure.md`
  }

  for (const nikaya of Object.keys(suttaNikayaMap)) {
    const base = `09-part-4-tipitaka-digest/sutta-pitaka/${nikaya}`
    const target = `part-4-tipitaka-digest/sutta-pitaka/${nikaya}`
    map[`${base}/${nikaya.replace('-nikaya', '')}-structure.md`] =
      `${target}/${nikaya.replace('-nikaya', '')}-structure.md`
  }

  function volPitaka(v: number) {
    if (v <= 8) return 'vinaya-pitaka'
    if (v <= 33) return 'sutta-pitaka'
    return 'abhidhamma-pitaka'
  }

  function volNikaya(v: number) {
    if (v <= 11) return 'digha-nikaya'
    if (v <= 14) return 'majjhima-nikaya'
    if (v <= 19) return 'samyutta-nikaya'
    if (v <= 24) return 'anguttara-nikaya'
    return 'khuddaka-nikaya'
  }

  const pad = (v: number) => String(v).padStart(2, '0')
  for (let v = 1; v <= 45; v++) {
    const pitaka = volPitaka(v)
    if (v >= 9 && v <= 33) {
      const nikaya = volNikaya(v)
      map[`09-part-4-tipitaka-digest/sutta-pitaka/${nikaya}/vol-${pad(v)}.md`] =
        `part-4-tipitaka-digest/sutta-pitaka/${nikaya}/vol-${pad(v)}.md`
    } else {
      map[`09-part-4-tipitaka-digest/${pitaka}/vol-${pad(v)}.md`] =
        `part-4-tipitaka-digest/${pitaka}/vol-${pad(v)}.md`
    }
  }

  return map
}

interface BatchEmbedResponse {
  embeddings: { values: number[] }[]
}

async function batchEmbed(texts: string[]): Promise<number[][]> {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${EMBEDDING_MODEL}:batchEmbedContents?key=${GEMINI_API_KEY}`
  const requests = texts.map((text) => ({
    model: `models/${EMBEDDING_MODEL}`,
    content: { parts: [{ text }] },
    outputDimensionality: EMBEDDING_DIMS,
  }))

  const MAX_RETRIES = 5
  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ requests }),
    })

    if (res.status === 429) {
      const wait = Math.pow(2, attempt + 1) * 1000
      console.log(`  Rate limited (429), retrying in ${wait / 1000}s...`)
      await new Promise((r) => setTimeout(r, wait))
      continue
    }

    if (!res.ok) {
      const body = await res.text()
      throw new Error(`Gemini batchEmbedContents ${res.status}: ${body}`)
    }

    const data = (await res.json()) as BatchEmbedResponse
    return data.embeddings.map((e) => e.values)
  }

  throw new Error('Gemini batchEmbedContents: max retries exceeded (429)')
}

interface IndexEntry {
  id: string
  url: string
  title: string
  breadcrumb: string
  text: string
  embedding: number[]
}

async function main() {
  console.log('Collecting markdown files...')
  const files = collectMdFiles(DOCS_DIR)
  console.log(`Found ${files.length} .md files`)

  const rewrites = buildRewrites()

  console.log('Chunking...')
  const allChunks: Chunk[] = []
  for (const file of files) {
    const content = readFileSync(file, 'utf-8')
    const relPath = relative(join(DOCS_DIR, '..'), file).replace(/\\/g, '/')
    const chunks = chunkMarkdown(relPath, content, rewrites)
    allChunks.push(...chunks)
  }
  console.log(`Total chunks: ${allChunks.length}`)

  console.log('Generating embeddings...')
  const entries: IndexEntry[] = []

  for (let i = 0; i < allChunks.length; i += BATCH_SIZE) {
    const batch = allChunks.slice(i, i + BATCH_SIZE)
    const texts = batch.map((c) => {
      const ctx = c.breadcrumb.join(' > ')
      return ctx ? `${ctx}\n\n${c.text}` : c.text
    })

    const embeddings = await batchEmbed(texts)

    for (let j = 0; j < batch.length; j++) {
      const chunk = batch[j]
      entries.push({
        id: chunk.id,
        url: chunk.url,
        title: chunk.title,
        breadcrumb: chunk.breadcrumb.join(' > '),
        text: chunk.text,
        embedding: embeddings[j],
      })
    }

    console.log(`  ${Math.min(i + BATCH_SIZE, allChunks.length)}/${allChunks.length}`)

    if (i + BATCH_SIZE < allChunks.length) {
      await new Promise((r) => setTimeout(r, 1000))
    }
  }

  mkdirSync(OUTPUT_DIR, { recursive: true })
  writeFileSync(OUTPUT_FILE, JSON.stringify(entries))

  const sizeMB = (Buffer.byteLength(JSON.stringify(entries)) / (1024 * 1024)).toFixed(2)
  console.log(`Done! Wrote ${entries.length} entries to chat-index.json (${sizeMB} MB)`)
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
