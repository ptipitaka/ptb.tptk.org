import type { Env, EmbedRequest, GeminiEmbedResponse, GeminiBatchEmbedResponse } from '../types'
import { DEFAULT_EMBEDDING_DIMS } from '../constants'
import { geminiHeaders, geminiUrl, geminiTimeout } from '../utils/gemini'
import { jsonResponse } from '../utils/response'

export async function handleEmbed(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  let body: EmbedRequest
  try {
    body = await request.json()
  } catch {
    return jsonResponse({ error: 'Invalid JSON' }, 400, cors)
  }

  const dims = parseInt(env.EMBEDDING_DIMENSIONS, 10) || DEFAULT_EMBEDDING_DIMS
  const model = env.EMBEDDING_MODEL

  const texts: string[] = body.texts
    ? body.texts.map((t) => t.trim()).filter(Boolean)
    : body.text?.trim()
      ? [body.text.trim()]
      : []

  if (texts.length === 0) {
    return jsonResponse({ error: 'Missing text or texts' }, 400, cors)
  }

  if (texts.length === 1) {
    return embedSingle(texts[0], model, dims, env.GEMINI_API_KEY, cors)
  }

  return embedBatch(texts, model, dims, env.GEMINI_API_KEY, cors)
}

async function embedSingle(
  text: string,
  model: string,
  dims: number,
  apiKey: string,
  cors: Record<string, string>,
): Promise<Response> {
  let res: globalThis.Response
  try {
    res = await fetch(geminiUrl(model, 'embedContent'), {
      method: 'POST',
      headers: geminiHeaders(apiKey),
      body: JSON.stringify({
        model: `models/${model}`,
        content: { parts: [{ text }] },
        outputDimensionality: dims,
      }),
      signal: geminiTimeout(),
    })
  } catch (err) {
    console.error('Embed: Gemini fetch failed', err)
    return jsonResponse({ error: 'Gemini embed timeout or network error' }, 502, cors)
  }

  if (!res.ok) {
    const errText = await res.text()
    console.error('Embed: Gemini error', res.status, errText)
    return jsonResponse({ error: `Gemini embed error: ${errText}` }, 502, cors)
  }

  const data: GeminiEmbedResponse = await res.json()
  return jsonResponse({ embedding: data.embedding.values }, 200, cors)
}

async function embedBatch(
  texts: string[],
  model: string,
  dims: number,
  apiKey: string,
  cors: Record<string, string>,
): Promise<Response> {
  const requests = texts.map((text) => ({
    model: `models/${model}`,
    content: { parts: [{ text }] },
    outputDimensionality: dims,
  }))

  let res: globalThis.Response
  try {
    res = await fetch(geminiUrl(model, 'batchEmbedContents'), {
      method: 'POST',
      headers: geminiHeaders(apiKey),
      body: JSON.stringify({ requests }),
      signal: geminiTimeout(),
    })
  } catch (err) {
    console.error('Embed batch: Gemini fetch failed', err)
    return jsonResponse({ error: 'Gemini embed timeout or network error' }, 502, cors)
  }

  if (!res.ok) {
    const errText = await res.text()
    console.error('Embed batch: Gemini error', res.status, errText)
    return jsonResponse({ error: `Gemini embed error: ${errText}` }, 502, cors)
  }

  const data: GeminiBatchEmbedResponse = await res.json()
  const embeddings = data.embeddings.map((e) => e.values)

  const avgLen = embeddings[0].length
  const avg = new Array<number>(avgLen).fill(0)
  for (const emb of embeddings) {
    for (let i = 0; i < avgLen; i++) avg[i] += emb[i]
  }
  for (let i = 0; i < avgLen; i++) avg[i] /= embeddings.length

  return jsonResponse({ embedding: avg }, 200, cors)
}
