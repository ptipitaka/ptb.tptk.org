<script setup lang="ts">
import MarkdownIt from 'markdown-it'
import { nextTick, onMounted, onUpdated, ref } from 'vue'

const root = ref<HTMLElement | null>(null)

const inlineMarkdown = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: false,
})

const shouldParse = (text: string) => /[*_`[\]]/.test(text)

const parseInlineMarkdown = () => {
  const el = root.value
  if (!el) return

  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT)
  const textNodes: Text[] = []
  let current = walker.nextNode()
  while (current) {
    textNodes.push(current as Text)
    current = walker.nextNode()
  }

  for (const textNode of textNodes) {
    const raw = textNode.nodeValue ?? ''
    if (!raw.trim() || !shouldParse(raw)) continue

    const html = inlineMarkdown.renderInline(raw)
    if (!html || html === raw) continue

    const holder = document.createElement('span')
    holder.innerHTML = html

    const fragment = document.createDocumentFragment()
    while (holder.firstChild) {
      fragment.appendChild(holder.firstChild)
    }
    textNode.parentNode?.replaceChild(fragment, textNode)
  }
}

const scheduleParse = () => {
  void nextTick(parseInlineMarkdown)
}

onMounted(scheduleParse)
onUpdated(scheduleParse)
</script>

<template>
  <span ref="root">
    <slot />
  </span>
</template>
