/** SITE_ORIGIN ใน wrangler ใส่ได้หลายค่าคั่นด้วยลูกน้ำ เช่น https://ptb.tptk.org,https://www.ptb.tptk.org */
function parseAllowedOrigins(config: string): string[] {
  return config
    .split(',')
    .map((s) => s.trim().replace(/\/$/, ''))
    .filter(Boolean)
}

/** อนุญาต Vite / dev server บนเครื่อง (รวม 127.0.0.1) */
function isLocalDevOrigin(origin: string): boolean {
  try {
    const u = new URL(origin)
    if (u.protocol !== 'http:' && u.protocol !== 'https:') return false
    return u.hostname === 'localhost' || u.hostname === '127.0.0.1'
  } catch {
    return false
  }
}

export function corsHeaders(origin: string, siteOriginConfig: string): Record<string, string> {
  const normalizedOrigin = origin.replace(/\/$/, '')
  const allowedList = parseAllowedOrigins(siteOriginConfig)
  const isAllowed =
    allowedList.includes('*') ||
    (normalizedOrigin !== '' && allowedList.includes(normalizedOrigin)) ||
    isLocalDevOrigin(normalizedOrigin)

  const fallback = allowedList[0] ?? 'https://ptb.tptk.org'
  const allowOrigin = isAllowed && normalizedOrigin !== '' ? normalizedOrigin : fallback
  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    Vary: 'Origin',
  }
}
