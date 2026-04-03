<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'

const CHAT_API = import.meta.env.VITE_CHAT_API_URL ?? 'https://ptb-chat.polished-frost-545c.workers.dev'
const INDEX_URL = import.meta.env.BASE_URL + 'chat-index.json'
const TOP_K = 8

interface IndexEntry {
  id: string
  url: string
  title: string
  breadcrumb: string
  text: string
  embedding: number[]
}

interface HistoryItem {
  role: 'user' | 'assistant'
  text: string
  sources?: { title: string; url: string; breadcrumb?: string }[]
}

let indexData: IndexEntry[] | null = null
let indexLoading: Promise<void> | null = null

function loadIndex(): Promise<void> {
  if (indexData) return Promise.resolve()
  if (indexLoading) return indexLoading
  indexLoading = fetch(INDEX_URL)
    .then((res) => {
      if (!res.ok) throw new Error(`Index load failed: ${res.status}`)
      return res.json()
    })
    .then((data: IndexEntry[]) => {
      indexData = data
    })
  return indexLoading
}

function dotProduct(a: number[], b: number[]): number {
  let sum = 0
  for (let i = 0; i < a.length; i++) sum += a[i] * b[i]
  return sum
}

function magnitude(v: number[]): number {
  let sum = 0
  for (let i = 0; i < v.length; i++) sum += v[i] * v[i]
  return Math.sqrt(sum)
}

function cosineSimilarity(a: number[], b: number[]): number {
  const magA = magnitude(a)
  const magB = magnitude(b)
  if (magA === 0 || magB === 0) return 0
  return dotProduct(a, b) / (magA * magB)
}

function searchIndex(queryEmbedding: number[], topK: number): IndexEntry[] {
  if (!indexData) return []
  const scored = indexData.map((entry) => ({
    entry,
    score: cosineSimilarity(queryEmbedding, entry.embedding),
  }))
  scored.sort((a, b) => b.score - a.score)
  return scored.slice(0, topK).map((s) => s.entry)
}

async function expandQuery(text: string): Promise<string[]> {
  try {
    const res = await fetch(`${CHAT_API}/api/expand`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    if (!res.ok) return [text]
    const data = await res.json()
    return data.queries?.length ? data.queries : [text]
  } catch {
    return [text]
  }
}

async function getEmbedding(text: string): Promise<number[]> {
  const queries = await expandQuery(text)

  const res = await fetch(`${CHAT_API}/api/embed`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(queries.length > 1 ? { texts: queries } : { text: queries[0] }),
  })
  if (!res.ok) throw new Error(`Embed API error: ${res.status}`)
  const data = await res.json()
  return data.embedding
}

const isOpen = ref(false)
const question = ref('')
const isLoading = ref(false)
const answer = ref('')
const sources = ref<{ title: string; url: string; breadcrumb?: string }[]>([])
const messagesEl = ref<HTMLElement | null>(null)
const inputEl = ref<HTMLInputElement | null>(null)
const history = ref<HistoryItem[]>([])
const indexReady = ref(false)
const indexError = ref('')

function toggle() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    nextTick(() => inputEl.value?.focus())
    if (!indexData && !indexLoading) {
      loadIndex()
        .then(() => { indexReady.value = true })
        .catch((e) => { indexError.value = e.message })
    }
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight
    }
  })
}

async function send() {
  const q = question.value.trim()
  if (!q || isLoading.value) return

  history.value.push({ role: 'user', text: q })
  question.value = ''
  isLoading.value = true
  answer.value = ''
  sources.value = []
  scrollToBottom()

  try {
    await loadIndex()
    indexReady.value = true

    const queryVec = await getEmbedding(q)

    const results = searchIndex(queryVec, TOP_K)
    if (results.length === 0) {
      const msg = 'ไม่พบข้อมูลที่เกี่ยวข้องในหนังสือ'
      answer.value = msg
      history.value.push({ role: 'assistant', text: msg })
      return
    }

    const context = results.map((r) => ({
      title: r.title,
      url: r.url,
      breadcrumb: r.breadcrumb,
      text: r.text,
    }))

    const res = await fetch(`${CHAT_API}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, context }),
    })

    if (!res.ok || !res.body) {
      throw new Error(`HTTP ${res.status}`)
    }

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let fullText = ''
    let parsedSources: { title: string; url: string }[] = []

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() ?? ''

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue
        const data = line.slice(6).trim()
        if (!data || data === '[DONE]') continue
        try {
          const parsed = JSON.parse(data)
          if (parsed.type === 'sources') {
            parsedSources = parsed.sources ?? []
            sources.value = parsedSources
          } else if (parsed.type === 'text') {
            fullText += parsed.text
            answer.value = fullText
            scrollToBottom()
          }
        } catch { /* skip */ }
      }
    }

    history.value.push({
      role: 'assistant',
      text: fullText || 'ไม่สามารถสร้างคำตอบได้',
      sources: parsedSources,
    })
  } catch (err: any) {
    const errMsg = `เกิดข้อผิดพลาด: ${err.message ?? 'ไม่ทราบสาเหตุ'}`
    answer.value = errMsg
    history.value.push({ role: 'assistant', text: errMsg })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

function closeOnEscape(e: KeyboardEvent) {
  if (e.key === 'Escape' && isOpen.value) {
    isOpen.value = false
  }
}

function looksLikePathTitle(title: string): boolean {
  const t = title.trim()
  if (!t) return true
  return (
    t.startsWith('docs/') ||
    t.includes('/index.md') ||
    t.endsWith('.md') ||
    t.includes(':_intro')
  )
}

function fallbackTitleFromUrl(rawUrl: string): string {
  const path = rawUrl.split('#')[0].split('?')[0]
  const parts = path.split('/').filter(Boolean)
  if (parts.length === 0) return 'หน้าหลัก'

  const aliases: Record<string, string> = {
    'speech-of-appreciation': 'พระคติธรรม',
    preface: 'คำปรารภ',
    introduction: 'คำนำ',
    'buddhist-council-illustration': 'ภาพการสังคายนา',
    'tipitaka-structure': 'แผนภูมิพระไตรปิฎก',
    abbreviations: 'อักษรย่อชื่อคัมภีร์',
    'part-3-tipitaka-selected-passages': 'ภาค ๓ ข้อความน่ารู้จากพระไตรปิฎก',
    'vinaya-pitaka': 'วินัยปิฎก (วิ.)',
    'digha-nikaya': 'ทีฆนิกาย (ที.)',
    'majjhima-nikaya': 'มัชฌิมนิกาย (ม.)',
    'samyutta-nikaya': 'สังยุตตนิกาย (สํ.)',
    'anguttara-nikaya': 'อังคุตตรนิกาย (องฺ.)',
    'khuddaka-nikaya': 'ขุททกนิกาย (ขุ.)',
    'abhidhamma-pitaka': 'อภิธรรมปิฎก (อภิ.)',
  }

  const last = parts[parts.length - 1]
  const prev = parts.length > 1 ? parts[parts.length - 2] : ''
  if (aliases[last]) return aliases[last]
  if (aliases[prev]) return aliases[prev]

  const selected = last === 'index' ? prev : last
  if (!selected) return 'แหล่งอ้างอิง'

  return decodeURIComponent(selected)
    .replace(/\.md$/i, '')
    .replace(/[-_]/g, ' ')
    .trim()
}

function sourceLabel(src: { title: string; url: string; breadcrumb?: string }): string {
  const title = (src.title ?? '').trim()
  if (title && !looksLikePathTitle(title)) return title
  const breadcrumb = (src.breadcrumb ?? '').trim()
  if (breadcrumb) return breadcrumb
  return fallbackTitleFromUrl(src.url)
}

onMounted(() => document.addEventListener('keydown', closeOnEscape))
onUnmounted(() => document.removeEventListener('keydown', closeOnEscape))
</script>

<template>
  <Teleport to="body">
    <button
      class="ptb-chat-fab"
      :class="{ 'ptb-chat-fab--open': isOpen }"
      :aria-label="isOpen ? 'ปิดแชท' : 'ถามเกี่ยวกับพระไตรปิฎก'"
      @click="toggle"
    >
      <svg v-if="!isOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>

    <Transition name="ptb-chat-slide">
      <div v-if="isOpen" class="ptb-chat-panel">
        <div class="ptb-chat-header">
          <strong>ถาม-ตอบ พระไตรปิฎก</strong>
          <button class="ptb-chat-close" aria-label="ปิด" @click="isOpen = false">&times;</button>
        </div>

        <div ref="messagesEl" class="ptb-chat-messages">
          <div v-if="indexError" class="ptb-chat-empty ptb-chat-error">
            <p>ไม่สามารถโหลดข้อมูลค้นหาได้: {{ indexError }}</p>
          </div>
          <div v-else-if="history.length === 0" class="ptb-chat-empty">
            <p>สวัสดีครับ สามารถถามคำถามเกี่ยวกับเนื้อหาในหนังสือ "พระไตรปิฎกฉบับสำหรับประชาชน" ได้เลยครับ</p>
          </div>
          <template v-for="(msg, i) in history" :key="i">
            <div :class="['ptb-chat-msg', `ptb-chat-msg--${msg.role}`]">
              <div class="ptb-chat-msg__text" v-html="renderMarkdown(msg.text)" />
              <div v-if="msg.sources?.length" class="ptb-chat-msg__sources">
                <span>แหล่งอ้างอิง:</span>
                <a
                  v-for="(src, j) in msg.sources"
                  :key="j"
                  :href="src.url"
                  class="ptb-chat-source-link"
                  @click="isOpen = false"
                >{{ sourceLabel(src) }}</a>
              </div>
            </div>
          </template>

          <div v-if="isLoading && answer" class="ptb-chat-msg ptb-chat-msg--assistant">
            <div class="ptb-chat-msg__text" v-html="renderMarkdown(answer)" />
          </div>
          <div v-if="isLoading && !answer" class="ptb-chat-msg ptb-chat-msg--assistant ptb-chat-msg--loading">
            <span class="ptb-chat-dots"><span /><span /><span /></span>
          </div>
        </div>

        <div class="ptb-chat-input-area">
          <input
            ref="inputEl"
            v-model="question"
            class="ptb-chat-input"
            type="text"
            placeholder="พิมพ์คำถาม..."
            :disabled="isLoading"
            @keydown="handleKeydown"
          />
          <button
            class="ptb-chat-send"
            :disabled="isLoading || !question.trim()"
            @click="send"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script lang="ts">
function renderMarkdown(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="ptb-chat-link">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
}
</script>

<style scoped>
.ptb-chat-fab {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 1100;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: var(--vp-c-brand-1, #3451b2);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
  transition: transform 0.2s, background 0.2s;
}

.ptb-chat-fab:hover {
  transform: scale(1.08);
  background: var(--vp-c-brand-2, #2c3e8f);
}

.ptb-chat-fab--open {
  background: var(--vp-c-text-2, #666);
}

.ptb-chat-panel {
  position: fixed;
  bottom: 5.5rem;
  right: 1.5rem;
  z-index: 1100;
  width: 400px;
  max-width: calc(100vw - 2rem);
  height: 520px;
  max-height: calc(100vh - 8rem);
  background: var(--vp-c-bg, #fff);
  border: 1px solid var(--vp-c-divider, #e2e8f0);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.15);
}

.ptb-chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  border-bottom: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft, #f6f6f7);
}

.ptb-chat-header strong {
  font-size: 0.95rem;
}

.ptb-chat-close {
  appearance: none;
  border: none;
  background: none;
  font-size: 1.4rem;
  cursor: pointer;
  color: var(--vp-c-text-2);
  padding: 0 0.25rem;
  line-height: 1;
}

.ptb-chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.ptb-chat-empty {
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
  text-align: center;
  padding: 2rem 0.5rem;
  line-height: 1.6;
}

.ptb-chat-error {
  color: var(--vp-c-danger-1, #e53e3e);
}

.ptb-chat-msg {
  max-width: 88%;
  padding: 0.6rem 0.85rem;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.6;
  word-break: break-word;
}

.ptb-chat-msg--user {
  align-self: flex-end;
  background: var(--vp-c-brand-1, #3451b2);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.ptb-chat-msg--assistant {
  align-self: flex-start;
  background: var(--vp-c-bg-soft, #f6f6f7);
  color: var(--vp-c-text-1);
  border-bottom-left-radius: 4px;
}

.ptb-chat-msg__text :deep(a) {
  color: var(--vp-c-brand-1);
  text-decoration: underline;
}

.ptb-chat-msg--user .ptb-chat-msg__text :deep(a) {
  color: #dbeafe;
}

.ptb-chat-msg__sources {
  margin-top: 0.5rem;
  padding-top: 0.4rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.8rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: baseline;
}

.ptb-chat-msg__sources span {
  color: var(--vp-c-text-2);
  font-weight: 500;
}

.ptb-chat-source-link {
  color: var(--vp-c-brand-1);
  text-decoration: none;
  font-size: 0.78rem;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  background: var(--vp-c-bg, #fff);
  border: 1px solid var(--vp-c-divider);
  white-space: nowrap;
}

.ptb-chat-source-link:hover {
  background: var(--vp-c-brand-soft, #eef2ff);
}

.ptb-chat-msg--loading {
  padding: 0.8rem 1rem;
}

.ptb-chat-dots {
  display: inline-flex;
  gap: 4px;
}

.ptb-chat-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--vp-c-text-3, #999);
  animation: ptbDotPulse 1.2s infinite ease-in-out;
}

.ptb-chat-dots span:nth-child(2) { animation-delay: 0.2s; }
.ptb-chat-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes ptbDotPulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1); }
}

.ptb-chat-input-area {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg, #fff);
}

.ptb-chat-input {
  flex: 1;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  font-size: 0.9rem;
  font-family: inherit;
  background: var(--vp-c-bg, #fff);
  color: var(--vp-c-text-1);
  outline: none;
  transition: border-color 0.2s;
}

.ptb-chat-input:focus {
  border-color: var(--vp-c-brand-1);
}

.ptb-chat-input::placeholder {
  color: var(--vp-c-text-3);
}

.ptb-chat-send {
  appearance: none;
  border: none;
  background: var(--vp-c-brand-1, #3451b2);
  color: #fff;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.2s;
}

.ptb-chat-send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.ptb-chat-send:not(:disabled):hover {
  background: var(--vp-c-brand-2, #2c3e8f);
}

.ptb-chat-slide-enter-active,
.ptb-chat-slide-leave-active {
  transition: opacity 0.25s, transform 0.25s;
}

.ptb-chat-slide-enter-from,
.ptb-chat-slide-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.96);
}

@media (max-width: 480px) {
  .ptb-chat-panel {
    right: 0;
    bottom: 0;
    width: 100vw;
    max-width: 100vw;
    height: 100dvh;
    max-height: 100dvh;
    border-radius: 0;
  }

  .ptb-chat-fab {
    bottom: 1rem;
    right: 1rem;
    width: 48px;
    height: 48px;
  }

  .ptb-chat-fab--open {
    z-index: 1200;
  }

  .ptb-chat-close {
    font-size: 1.6rem;
    padding: 0.2rem 0.5rem;
  }
}
</style>
