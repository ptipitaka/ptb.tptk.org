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
