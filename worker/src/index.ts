import type { Env } from './types'
import { corsHeaders } from './utils/cors'
import { jsonResponse } from './utils/response'
import { handleExpand } from './handlers/expand'
import { handleEmbed } from './handlers/embed'
import { handleChat } from './handlers/chat'

export type { Env }

const routes: Record<string, (req: Request, env: Env, cors: Record<string, string>) => Promise<Response>> = {
  '/api/expand': handleExpand,
  '/api/embed': handleEmbed,
  '/api/chat': handleChat,
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

    const handler = routes[url.pathname]
    if (!handler) {
      return jsonResponse({ error: 'Not found' }, 404, cors)
    }

    return handler(request, env, cors)
  },
}
