import type { Env, ChatRequest, GeminiGenerateResponse } from '../types'
import { SYSTEM_PROMPT } from '../prompts'
import { CHAT_TEMPERATURE, CHAT_MAX_TOKENS } from '../constants'
import { geminiHeaders, geminiUrl, geminiTimeout } from '../utils/gemini'
import { jsonResponse } from '../utils/response'

export async function handleChat(
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

  let geminiRes: globalThis.Response
  try {
    geminiRes = await fetch(
      geminiUrl(env.GEMINI_MODEL, 'streamGenerateContent') + '?alt=sse',
      {
        method: 'POST',
        headers: geminiHeaders(env.GEMINI_API_KEY),
        body: JSON.stringify({
          contents: [{ role: 'user', parts: [{ text: prompt }] }],
          generationConfig: { temperature: CHAT_TEMPERATURE, maxOutputTokens: CHAT_MAX_TOKENS },
        }),
        signal: geminiTimeout(),
      },
    )
  } catch (err) {
    console.error('Chat: Gemini fetch failed', err)
    return jsonResponse({ error: 'Gemini timeout or network error' }, 502, cors)
  }

  if (!geminiRes.ok || !geminiRes.body) {
    const errText = await geminiRes.text()
    console.error('Chat: Gemini error', geminiRes.status, errText)
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

  const sseWrite = (payload: unknown) =>
    writer.write(encoder.encode(`data: ${JSON.stringify(payload)}\n\n`))

  await sseWrite({ type: 'sources', sources })

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
            const parsed: GeminiGenerateResponse = JSON.parse(jsonStr)
            const text = parsed?.candidates?.[0]?.content?.parts?.[0]?.text
            if (text) {
              await sseWrite({ type: 'text', text })
            }
          } catch {
            // skip malformed SSE chunk
          }
        }
      }
      await writer.write(encoder.encode('data: [DONE]\n\n'))
    } catch (err) {
      console.error('Chat: SSE stream error', err)
      try {
        await sseWrite({ type: 'error', error: 'Stream interrupted' })
      } catch {
        // writer already closed
      }
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
