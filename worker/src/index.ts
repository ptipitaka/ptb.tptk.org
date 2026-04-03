export interface Env {
  GEMINI_API_KEY: string
  GEMINI_MODEL: string
  EMBEDDING_MODEL: string
  EMBEDDING_DIMENSIONS: string
  SITE_ORIGIN: string
}

const GEMINI_BASE = 'https://generativelanguage.googleapis.com/v1beta'

function corsHeaders(origin: string, allowed: string): Record<string, string> {
  const isAllowed =
    origin === allowed ||
    allowed === '*' ||
    origin.startsWith('http://localhost:')
  return {
    'Access-Control-Allow-Origin': isAllowed ? origin : allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  }
}

function jsonResponse(data: unknown, status: number, cors: Record<string, string>) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...cors, 'Content-Type': 'application/json' },
  })
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url)
    const origin = request.headers.get('Origin') ?? ''
    const cors = corsHeaders(origin, env.SITE_ORIGIN)

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors })
    }

    if (request.method !== 'POST') {
      return jsonResponse({ error: 'Method not allowed' }, 405, cors)
    }

    if (url.pathname === '/api/expand') {
      return handleExpand(request, env, cors)
    }

    if (url.pathname === '/api/embed') {
      return handleEmbed(request, env, cors)
    }

    if (url.pathname === '/api/chat') {
      return handleChat(request, env, cors)
    }

    return jsonResponse({ error: 'Not found' }, 404, cors)
  },
}

const EXPAND_PROMPT = `คุณคือผู้ช่วยขยายคำค้นหาเกี่ยวกับหนังสือ "พระไตรปิฎกฉบับสำหรับประชาชน"
หนังสือเล่มนี้เขียนในสมัยที่ประเทศไทยยังเรียกว่า "สยาม" ดังนั้นคำศัพท์จะเป็นแบบโบราณ เช่น "แผ่นดินสยาม" แทน "ประเทศไทย", "พม่า" แทน "เมียนมาร์"

เมื่อได้รับคำถาม ให้สร้างคำค้นหา 3 รูปแบบที่แตกต่างกัน ครอบคลุมทั้ง:
- คำศัพท์สมัยใหม่และโบราณ
- คำพ้องความหมาย
- ศัพท์บาลี/สันสกฤตที่เกี่ยวข้อง (ถ้ามี)

ตอบเป็น JSON array ของ strings เท่านั้น ไม่ต้องอธิบาย ตัวอย่าง:
คำถาม: "การสังคายนาในเมืองไทย"
["การสังคายนาในเมืองไทย", "การสังคายนาในแผ่นดินสยาม", "สังคายนาพระไตรปิฎกในสยามประเทศ"]`

async function handleExpand(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  let body: { text: string }
  try {
    body = await request.json()
  } catch {
    return jsonResponse({ error: 'Invalid JSON' }, 400, cors)
  }

  const text = body.text?.trim()
  if (!text) {
    return jsonResponse({ error: 'Missing text' }, 400, cors)
  }

  const res = await fetch(
    `${GEMINI_BASE}/models/${env.GEMINI_MODEL}:generateContent?key=${env.GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: `${EXPAND_PROMPT}\n\nคำถาม: "${text}"` }] }],
        generationConfig: { temperature: 0.4, maxOutputTokens: 256 },
      }),
    },
  )

  if (!res.ok) {
    return jsonResponse({ queries: [text] }, 200, cors)
  }

  const data: any = await res.json()
  const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text ?? ''

  try {
    const match = raw.match(/\[[\s\S]*\]/)
    const queries: string[] = match ? JSON.parse(match[0]) : [text]
    return jsonResponse({ queries: queries.slice(0, 4) }, 200, cors)
  } catch {
    return jsonResponse({ queries: [text] }, 200, cors)
  }
}

async function handleEmbed(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  let body: { text?: string; texts?: string[] }
  try {
    body = await request.json()
  } catch {
    return jsonResponse({ error: 'Invalid JSON' }, 400, cors)
  }

  const dims = parseInt(env.EMBEDDING_DIMENSIONS, 10) || 768
  const model = env.EMBEDDING_MODEL

  const texts: string[] = body.texts
    ? body.texts.map((t) => t.trim()).filter(Boolean)
    : body.text?.trim() ? [body.text.trim()] : []

  if (texts.length === 0) {
    return jsonResponse({ error: 'Missing text or texts' }, 400, cors)
  }

  if (texts.length === 1) {
    const res = await fetch(
      `${GEMINI_BASE}/models/${model}:embedContent?key=${env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: `models/${model}`,
          content: { parts: [{ text: texts[0] }] },
          outputDimensionality: dims,
        }),
      },
    )

    if (!res.ok) {
      const errText = await res.text()
      return jsonResponse({ error: `Gemini embed error: ${errText}` }, 502, cors)
    }

    const data: any = await res.json()
    return jsonResponse({ embedding: data.embedding.values }, 200, cors)
  }

  const requests = texts.map((text) => ({
    model: `models/${model}`,
    content: { parts: [{ text }] },
    outputDimensionality: dims,
  }))

  const res = await fetch(
    `${GEMINI_BASE}/models/${model}:batchEmbedContents?key=${env.GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ requests }),
    },
  )

  if (!res.ok) {
    const errText = await res.text()
    return jsonResponse({ error: `Gemini embed error: ${errText}` }, 502, cors)
  }

  const data: any = await res.json()
  const embeddings: number[][] = data.embeddings.map((e: any) => e.values)

  const avgLen = embeddings[0].length
  const avg = new Array(avgLen).fill(0)
  for (const emb of embeddings) {
    for (let i = 0; i < avgLen; i++) avg[i] += emb[i]
  }
  for (let i = 0; i < avgLen; i++) avg[i] /= embeddings.length

  return jsonResponse({ embedding: avg }, 200, cors)
}

interface ChatRequest {
  question: string
  context: { title: string; url: string; breadcrumb: string; text: string }[]
}

const SYSTEM_PROMPT = `คุณคือผู้ช่วยตอบคำถามเกี่ยวกับ "พระไตรปิฎกฉบับสำหรับประชาชน" โดย อาจารย์สุชีพ ปุญญานุภาพ
ตอบเป็นภาษาไทยเท่านั้น ใช้ข้อมูลจากเนื้อหาที่ให้ (context) เท่านั้น หากไม่มีข้อมูลเพียงพอให้ตอบว่าไม่พบข้อมูลในหนังสือ
อ้างอิงแหล่งที่มาเป็นลิงก์ในรูปแบบ Markdown [ชื่อหัวข้อ](url) ท้ายคำตอบ
ตอบกระชับ ชัดเจน ไม่เกิน 500 คำ`

async function handleChat(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  let body: ChatRequest
  try {
    body = await request.json()
  } catch {
    return jsonResponse({ error: 'Invalid JSON' }, 400, cors)
  }

  const question = body.question?.trim()
  if (!question) {
    return jsonResponse({ error: 'Missing question' }, 400, cors)
  }

  const chunks = body.context ?? []
  if (chunks.length === 0) {
    return jsonResponse({ error: 'Missing context' }, 400, cors)
  }

  const contextParts = chunks.map((c, i) => {
    const path = c.breadcrumb || c.title
    return `[${i + 1}] ${path}\nURL: ${c.url}\n${c.text}`
  })

  const prompt = `${SYSTEM_PROMPT}

--- เนื้อหาอ้างอิง ---
${contextParts.join('\n\n')}
--- จบเนื้อหาอ้างอิง ---

คำถาม: ${question}`

  const geminiRes = await fetch(
    `${GEMINI_BASE}/models/${env.GEMINI_MODEL}:streamGenerateContent?key=${env.GEMINI_API_KEY}&alt=sse`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: prompt }] }],
        generationConfig: { temperature: 0.3, maxOutputTokens: 2048 },
      }),
    },
  )

  if (!geminiRes.ok || !geminiRes.body) {
    const errText = await geminiRes.text()
    return jsonResponse({ error: `Gemini error: ${errText}` }, 502, cors)
  }

  const sources = chunks.map((c) => ({
    title: c.title,
    url: c.url,
    breadcrumb: c.breadcrumb,
  }))
  const { readable, writable } = new TransformStream()
  const writer = writable.getWriter()
  const encoder = new TextEncoder()

  writer.write(encoder.encode(`data: ${JSON.stringify({ type: 'sources', sources })}\n\n`))

  const reader = geminiRes.body.getReader()
  const decoder = new TextDecoder()

  ;(async () => {
    let buffer = ''
    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const jsonStr = line.slice(6).trim()
          if (!jsonStr || jsonStr === '[DONE]') continue
          try {
            const parsed = JSON.parse(jsonStr)
            const text = parsed?.candidates?.[0]?.content?.parts?.[0]?.text
            if (text) {
              await writer.write(
                encoder.encode(`data: ${JSON.stringify({ type: 'text', text })}\n\n`),
              )
            }
          } catch {
            // skip malformed SSE
          }
        }
      }
      await writer.write(encoder.encode('data: [DONE]\n\n'))
    } finally {
      await writer.close()
    }
  })()

  return new Response(readable, {
    headers: {
      ...cors,
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  })
}
