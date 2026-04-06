<script setup lang="ts">
import { computed, ref, useId, useSlots } from 'vue'
import PtbMarkdownInline from './PtbMarkdownInline.vue'

const props = defineProps<{
  term: string
  desc: string
}>()

const slots = useSlots()
const open = ref(false)
const detailsId = useId()

const hasDetails = computed(() => {
  const fn = slots.default
  if (!fn) return false
  const children = fn()
  return Array.isArray(children) && children.length > 0
})

function toggle() {
  if (!hasDetails.value) return
  open.value = !open.value
}
</script>

<template>
  <div
    class="wi-entry"
    :class="{ 'wi-entry--expanded': hasDetails && open }"
  >
    <div v-if="hasDetails" class="wi-entry__meta">
      <button
        type="button"
        class="wi-entry__head"
        :aria-expanded="open"
        :aria-controls="detailsId"
        @click="toggle"
      >
        <span class="wi-entry__term">
          <PtbMarkdownInline>{{ props.term }}</PtbMarkdownInline>
        </span>
        <span class="wi-entry__toggle" aria-hidden="true">{{ open ? '−' : '+' }}</span>
      </button>
      <p class="wi-entry__desc">
        <PtbMarkdownInline>{{ props.desc }}</PtbMarkdownInline>
      </p>
    </div>

    <template v-else>
      <p class="wi-entry__term">
        <PtbMarkdownInline>{{ props.term }}</PtbMarkdownInline>
      </p>
      <p class="wi-entry__desc">
        <PtbMarkdownInline>{{ props.desc }}</PtbMarkdownInline>
      </p>
    </template>

    <div
      v-if="hasDetails"
      :id="detailsId"
      class="wi-entry__details"
      role="region"
      :class="{ 'wi-entry__details--open': open }"
      :aria-hidden="!open"
      :aria-label="`รายละเอียด — ${props.term}`"
    >
      <div class="wi-entry__details-inner">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.wi-entry {
  margin-block: 20px;
  border-radius: 0.625rem;
  border: 1px solid transparent;
  box-sizing: border-box;
  transition:
    background 0.38s cubic-bezier(0.2, 0.85, 0.2, 1),
    border-color 0.38s cubic-bezier(0.2, 0.85, 0.2, 1),
    box-shadow 0.38s cubic-bezier(0.2, 0.85, 0.2, 1),
    transform 0.38s cubic-bezier(0.2, 0.85, 0.2, 1);
}

.wi-entry--expanded {
  position: relative;
  z-index: 1;
  /* ลบ padding-top ของ .wi-entry (custom.css) — มิฉะนั้นแถบ wi-entry__meta จะไม่ชิดขอบบนกล่อง เกิดช่องว่างสีขาวเหนือหัวข้อ */
  padding-top: 0;
  background: var(--vp-c-bg-soft);
  border-color: color-mix(in srgb, var(--vp-c-divider) 70%, transparent);
  box-shadow:
    0 1px 2px rgb(0 0 0 / 0.04),
    0 10px 28px rgb(0 0 0 / 0.07),
    0 0 0 1px rgb(0 0 0 / 0.02);
  transform: translateY(-2px);
}

/* กล่องเดียวสำหรับ term+desc — ขอบซ้ายขวาตรงกัน (ไม่ใช้ negative margin แยกที่ button กับ p) */
.wi-entry__meta {
  display: flex;
  flex-direction: column;
}

.wi-entry--expanded .wi-entry__meta {
  margin-left: -1rem;
  margin-right: -1rem;
  width: calc(100% + 2rem);
  box-sizing: border-box;
  background: color-mix(in srgb, var(--vp-c-bg-soft) 90%, black);
  /* ชิดมุมบนกับกล่องภายนอก (wi-entry ใช้ border-radius 0.625rem) */
  border-radius: 0.625rem 0.625rem 0.5rem 0.5rem;
  overflow: hidden;
  transition: background 0.38s cubic-bezier(0.2, 0.85, 0.2, 1);
}

.wi-entry--expanded .wi-entry__head {
  margin: 0;
  width: 100%;
  max-width: none;
  padding: 0.55rem 1rem 0.5rem;
  border-radius: 0;
  background: transparent;
  border-bottom: 1px solid color-mix(in srgb, var(--vp-c-divider) 55%, transparent);
}

.wi-entry--expanded .wi-entry__meta .wi-entry__desc {
  margin: 0;
  width: 100%;
  max-width: none;
  padding: 0.45rem 1rem 0.65rem;
  border-radius: 0;
  background: transparent;
  line-height: 1.65;
}

.wi-entry__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  width: 100%;
  margin: 0;
  padding: 0;
  text-align: start;
  font: inherit;
  color: inherit;
  background: transparent;
  border: none;
  cursor: pointer;
}

.wi-entry__head .wi-entry__term {
  flex: 1;
  min-width: 0;
  text-align: start;
}

.wi-entry__head:hover .wi-entry__term {
  color: var(--vp-c-brand-1);
}

.wi-entry__head:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
  border-radius: 0.375rem;
}

.wi-entry__toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  align-self: flex-start;
  width: 1.5rem;
  min-height: 1.5rem;
  margin-top: 0.08em;
  border-radius: 0.25rem;
  font-family: ui-monospace, 'Cascadia Code', 'Segoe UI', sans-serif;
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1;
  color: var(--vp-c-text-2);
  transition:
    color 0.18s ease,
    background 0.18s ease;
}

.wi-entry__head:hover .wi-entry__toggle {
  color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 10%, transparent);
}

.wi-entry__details {
  display: grid;
  grid-template-rows: 0fr;
  overflow: hidden;
  transition: grid-template-rows 0.42s cubic-bezier(0.2, 0.88, 0.2, 1);
}

.wi-entry__details--open {
  grid-template-rows: 1fr;
}

.wi-entry__details-inner {
  min-height: 0;
  overflow: hidden;
  padding-top: 0;
  transform-origin: top center;
  transform: scaleY(0.97);
  opacity: 0.88;
  transition:
    padding-top 0.38s cubic-bezier(0.2, 0.88, 0.2, 1),
    transform 0.42s cubic-bezier(0.2, 0.88, 0.2, 1),
    opacity 0.35s ease;
}

.wi-entry__details--open .wi-entry__details-inner {
  padding-top: 0.75rem;
  padding-bottom: 0.125rem;
  border-top: 1px solid color-mix(in srgb, var(--vp-c-divider) 40%, transparent);
  transform: scaleY(1);
  opacity: 1;
}

.wi-entry__details-inner :deep(p:first-child) {
  margin-top: 0;
}

.wi-entry__details-inner :deep(p:last-child) {
  margin-bottom: 0;
}

.wi-entry__details-inner :deep(ul),
.wi-entry__details-inner :deep(ol) {
  margin-top: 0.5rem;
  margin-bottom: 0.75rem;
}

.wi-entry__details-inner :deep(h2),
.wi-entry__details-inner :deep(h3) {
  color: var(--vp-c-text-1);
}
</style>
