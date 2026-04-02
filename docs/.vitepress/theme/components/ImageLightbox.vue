<script setup lang="ts">
import { ref, watch } from 'vue'

defineProps<{
  src: string
  alt?: string
}>()

const open = ref(false)
const overlayEl = ref<HTMLElement | null>(null)

function close() {
  open.value = false
  document.body.style.overflow = ''
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') close()
}

watch(open, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
    setTimeout(() => overlayEl.value?.focus(), 50)
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<template>
  <div class="image-lightbox-wrapper">
    <button
      type="button"
      class="lightbox-trigger"
      aria-label="ขยายภาพ"
      @click="open = true"
    >
      <img :src="src" :alt="alt ?? ''" class="lightbox-thumb" loading="lazy" />
    </button>

    <Teleport to="body">
      <Transition name="lightbox">
        <div
          v-show="open"
          class="lightbox-overlay"
          role="dialog"
          aria-modal="true"
          :aria-label="alt ?? 'ภาพขยาย'"
          tabindex="-1"
          ref="overlayEl"
          @click.self="close"
          @keydown="onKeydown"
        >
          <button
            type="button"
            class="lightbox-close"
            aria-label="ปิด"
            @click="close"
          >
            ×
          </button>
          <img
            :src="src"
            :alt="alt ?? ''"
            class="lightbox-full"
            @click.stop
          />
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.image-lightbox-wrapper {
  text-align: center;
  margin: 1rem 0;
}

.lightbox-trigger {
  display: inline-block;
  cursor: pointer;
  border: none;
  padding: 0;
  background: none;
  border-radius: 8px;
  overflow: hidden;
  max-width: 100%;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}

.lightbox-trigger:hover,
.lightbox-trigger:focus-visible {
  transform: translateY(-3px);
  box-shadow: 0 10px 22px rgba(0, 0, 0, 0.2), 0 2px 6px rgba(0, 0, 0, 0.12);
}

.lightbox-trigger:active {
  transform: translateY(-1px);
}

.lightbox-trigger:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 3px;
}

.lightbox-thumb {
  max-width: 100%;
  height: auto;
  vertical-align: middle;
  display: block;
  transition: filter 0.18s ease;
}

.lightbox-trigger:hover .lightbox-thumb,
.lightbox-trigger:focus-visible .lightbox-thumb {
  filter: brightness(1.03);
}

@media (prefers-reduced-motion: reduce) {
  .lightbox-trigger,
  .lightbox-thumb {
    transition: none;
  }
}

.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  cursor: zoom-out;
}

.lightbox-overlay:focus {
  outline: none;
}

.lightbox-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 2.5rem;
  height: 2.5rem;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.lightbox-close:hover {
  background: rgba(255, 255, 255, 0.25);
}

.lightbox-full {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  cursor: default;
}

.lightbox-enter-active,
.lightbox-leave-active {
  transition: opacity 0.2s ease;
}

.lightbox-enter-from,
.lightbox-leave-to {
  opacity: 0;
}
</style>
