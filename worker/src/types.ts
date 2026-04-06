export interface Env {
  GEMINI_API_KEY: string
  GEMINI_MODEL: string
  EMBEDDING_MODEL: string
  EMBEDDING_DIMENSIONS: string
  SITE_ORIGIN: string
}

export interface ExpandRequest {
  text: string
}

export interface EmbedRequest {
  text?: string
  texts?: string[]
}

export interface ChatRequest {
  question: string
  context: ChatContext[]
}

export interface ChatContext {
  title: string
  url: string
  breadcrumb: string
  text: string
}

export interface GeminiGenerateResponse {
  candidates?: {
    content?: {
      parts?: { text?: string }[]
    }
  }[]
}

export interface GeminiEmbedResponse {
  embedding: { values: number[] }
}

export interface GeminiBatchEmbedResponse {
  embeddings: { values: number[] }[]
}
