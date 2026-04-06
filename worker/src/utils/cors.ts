export function corsHeaders(origin: string, allowed: string): Record<string, string> {
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
