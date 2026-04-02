<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import PtbMarkdownInline from './PtbMarkdownInline.vue'

const props = defineProps<{
  label?: string
}>()

const markerLabel = computed(() => props.label ?? '(*)')
/** ค่า CSS สำหรับ `content:` ของปุ่ม — ใช้ JSON.stringify เพื่อใส่เครื่องหมายคำพูดให้ถูกต้อง */
const triggerMarkerCss = computed(() =>
  props.label ? JSON.stringify(props.label) : undefined,
)
const isOpen = ref(false)
const id = `ptb-footnote-${Math.random().toString(36).slice(2, 10)}`

const close = () => {
  if (!isOpen.value) return
  isOpen.value = false
}

const open = () => {
  window.dispatchEvent(new CustomEvent('ptb-footnote-open', { detail: { id } }))
  isOpen.value = true
}

const toggle = () => {
  if (isOpen.value) {
    close()
    return
  }
  open()
}

const onFootnoteOpen = (event: Event) => {
  const customEvent = event as CustomEvent<{ id?: string }>
  if (customEvent.detail?.id !== id) {
    close()
  }
}

const onEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape') close()
}

onMounted(() => {
  window.addEventListener('ptb-footnote-open', onFootnoteOpen as EventListener)
  window.addEventListener('keydown', onEscape)
})

onBeforeUnmount(() => {
  window.removeEventListener('ptb-footnote-open', onFootnoteOpen as EventListener)
  window.removeEventListener('keydown', onEscape)
})
</script>

<template>
  <span class="ptb-inline-footnote">
    <button
      type="button"
      class="ptb-inline-footnote__trigger"
      :style="triggerMarkerCss ? { '--ptb-fn-marker': triggerMarkerCss } : undefined"
      :aria-expanded="isOpen ? 'true' : 'false'"
      :aria-label="`เปิดเชิงอรรถ ${markerLabel}`"
      @click="toggle"
    />

    <Teleport to="body">
      <div v-if="isOpen" class="ptb-inline-footnote__sheet-layer" role="dialog" aria-modal="true">
        <div class="ptb-inline-footnote__overlay" @click="close" />
        <section class="ptb-inline-footnote__sheet">
          <button
            type="button"
            class="ptb-inline-footnote__close"
            aria-label="ปิดเชิงอรรถ"
            @click="close"
          >
            X
          </button>
          <div class="ptb-inline-footnote__content">
            <PtbMarkdownInline>
              <slot />
            </PtbMarkdownInline>
          </div>
        </section>
      </div>
    </Teleport>

  </span>
</template>
