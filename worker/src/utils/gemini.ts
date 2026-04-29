import { GEMINI_BASE, GEMINI_TIMEOUT_MS } from '../constants'

export function geminiHeaders(apiKey: string): Record<string, string> {
  return {
    'Content-Type': 'application/json',
    'x-goog-api-key': apiKey,
  }
}

export function geminiUrl(model: string, action: string): string {
  return `${GEMINI_BASE}/models/${model}:${action}`
}

export function geminiTimeout(): AbortSignal {
  return AbortSignal.timeout(GEMINI_TIMEOUT_MS)
}

/** Retry เมื่อ Gemini คืน 429 / RESOURCE_EXHAUSTED (ช่วยกรณีชั่วคราว) */
export async function fetchWith429Retries(
  fetchFn: () => Promise<globalThis.Response>,
  maxAttempts = 3,
): Promise<{ ok: true; res: globalThis.Response } | { ok: false; status: number; text: string }> {
  let lastStatus = 0
  let lastText = ''
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const res = await fetchFn()
    if (res.ok) return { ok: true, res }
    lastText = await res.text()
    lastStatus = res.status
    const retry429 = lastStatus === 429 || lastText.includes('RESOURCE_EXHAUSTED')
    if (retry429 && attempt < maxAttempts - 1) {
      await new Promise((r) => setTimeout(r, 1200 * (attempt + 1)))
      continue
    }
    return { ok: false, status: lastStatus, text: lastText }
  }
  return { ok: false, status: lastStatus, text: lastText }
}

export function geminiErrorPayload(status: number, errText: string): { status: number; error: string } {
  if (status === 429 || errText.includes('RESOURCE_EXHAUSTED')) {
    return {
      status: 429,
      error: 'ขณะนี้โควต้า AI เต็มหรือถูกจำกัดชั่วคราว กรุณาลองใหม่ภายหลัง',
    }
  }

  return {
    status: 502,
    error: 'ไม่สามารถเชื่อมต่อบริการ AI ได้ในขณะนี้ กรุณาลองใหม่ภายหลัง',
  }
}
