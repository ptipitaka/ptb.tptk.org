import type { Env, EmbedRequest, GeminiEmbedResponse, GeminiBatchEmbedResponse } from '../types'
import { DEFAULT_EMBEDDING_DIMS } from '../constants'
import {
  fetchWith429Retries,
  geminiErrorPayload,
  geminiHeaders,
  geminiTimeout,
  geminiUrl,
} from '../utils/gemini'
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
  const body = JSON.stringify({
    model: `models/${model}`,
    content: { parts: [{ text }] },
    outputDimensionality: dims,
  })
  const url = geminiUrl(model, 'embedContent')

  let outcome: Awaited<ReturnType<typeof fetchWith429Retries>>
  try {
    outcome = await fetchWith429Retries(() =>
      fetch(url, {
        method: 'POST',
        headers: geminiHeaders(apiKey),
        body,
        signal: geminiTimeout(),
      }),
    )
  } catch (err) {
    console.error('Embed: Gemini fetch failed', err)
    return jsonResponse({ error: 'Gemini embed timeout or network error' }, 502, cors)
  }

  if (!outcome.ok) {
    console.error('Embed: Gemini error', outcome.status, outcome.text)
    const payload = geminiErrorPayload(outcome.status, outcome.text)
    return jsonResponse({ error: payload.error }, payload.status, cors)
  }

  const data: GeminiEmbedResponse = await outcome.res.json()
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

  const batchBody = JSON.stringify({ requests })
  const batchUrl = geminiUrl(model, 'batchEmbedContents')

  let outcome: Awaited<ReturnType<typeof fetchWith429Retries>>
  try {
    outcome = await fetchWith429Retries(() =>
      fetch(batchUrl, {
        method: 'POST',
        headers: geminiHeaders(apiKey),
        body: batchBody,
        signal: geminiTimeout(),
      }),
    )
  } catch (err) {
    console.error('Embed batch: Gemini fetch failed', err)
    return jsonResponse({ error: 'Gemini embed timeout or network error' }, 502, cors)
  }

  if (!outcome.ok) {
    console.error('Embed batch: Gemini error', outcome.status, outcome.text)
    const payload = geminiErrorPayload(outcome.status, outcome.text)
    return jsonResponse({ error: payload.error }, payload.status, cors)
  }

  const data: GeminiBatchEmbedResponse = await outcome.res.json()
  const embeddings = data.embeddings.map((e) => e.values)

  const avgLen = embeddings[0].length
  const avg = new Array<number>(avgLen).fill(0)
  for (const emb of embeddings) {
    for (let i = 0; i < avgLen; i++) avg[i] += emb[i]
  }
  for (let i = 0; i < avgLen; i++) avg[i] /= embeddings.length

  return jsonResponse({ embedding: avg }, 200, cors)
}
