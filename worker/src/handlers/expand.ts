import type { Env, ExpandRequest, GeminiGenerateResponse } from '../types'
import { EXPAND_PROMPT } from '../prompts'
import { EXPAND_TEMPERATURE, EXPAND_MAX_TOKENS, MAX_EXPAND_QUERIES } from '../constants'
import { geminiHeaders, geminiUrl, geminiTimeout } from '../utils/gemini'
import { jsonResponse } from '../utils/response'

export async function handleExpand(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  let body: ExpandRequest
  try {
    body = await request.json()
  } catch {
    return jsonResponse({ error: 'Invalid JSON' }, 400, cors)
  }

  const text = body.text?.trim()
  if (!text) {
    return jsonResponse({ error: 'Missing text' }, 400, cors)
  }

  let res: globalThis.Response
  try {
    res = await fetch(geminiUrl(env.GEMINI_MODEL, 'generateContent'), {
      method: 'POST',
      headers: geminiHeaders(env.GEMINI_API_KEY),
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: `${EXPAND_PROMPT}\n\nคำถาม: "${text}"` }] }],
        generationConfig: { temperature: EXPAND_TEMPERATURE, maxOutputTokens: EXPAND_MAX_TOKENS },
      }),
      signal: geminiTimeout(),
    })
  } catch (err) {
    console.error('Expand: Gemini fetch failed', err)
    return jsonResponse({ queries: [text] }, 200, cors)
  }

  if (!res.ok) {
    console.error('Expand: Gemini returned', res.status)
    return jsonResponse({ queries: [text] }, 200, cors)
  }

  const data: GeminiGenerateResponse = await res.json()
  const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text ?? ''

  try {
    const match = raw.match(/\[[\s\S]*\]/)
    const queries: string[] = match ? JSON.parse(match[0]) : [text]
    return jsonResponse({ queries: queries.slice(0, MAX_EXPAND_QUERIES) }, 200, cors)
  } catch (err) {
    console.error('Expand: failed to parse response', err, raw)
    return jsonResponse({ queries: [text] }, 200, cors)
  }
}
