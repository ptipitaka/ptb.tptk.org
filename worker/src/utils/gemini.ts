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
