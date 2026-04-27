<script setup lang="ts">
import { computed } from 'vue'

/**
 * ลิงก์ไปความย่อในพระไตรปิฎกฉบับสำหรับประชาชน — แสดงเป็นข้อความ ใช้คู่กับ PtbWordIndexRefs (คลาส wi-entry__refs)
 */
const props = defineProps<{
  href: string
  /** ข้อความบนลิงก์ + tooltip */
  label?: string
  /**
   * ระดับอ้างอิง (สี/น้ำหนักลิงก์) ตาม `.cursor/rules/ptb-word-index.mdc`
   * ไม่ใส่ในพร็อพ `title` — tooltip แสดงเท่าที่ `label` เท่านั้น
   */
  tier?: 'primary' | 'secondary'
}>()

const defaultLabel = 'เปิดความย่อในพระไตรปิฎกฉบับสำหรับประชาชน'

/** Tooltip: ตรงกับ breadcrumb ใน label เท่านั้น (ไม่ต่อท้ายข้อความอ้างอิงระดับ) */
const linkTitle = computed(() => props.label ?? defaultLabel)

const linkClass = computed(() => {
  return [
    'ptb-wi-link-text',
    props.tier === 'primary' && 'ptb-wi-link-text--primary',
    props.tier === 'secondary' && 'ptb-wi-link-text--secondary',
  ].filter(Boolean)
})
</script>

<template>
  <a
    :class="linkClass"
    :href="href"
    :title="linkTitle"
  >
    {{ label ?? defaultLabel }}
  </a>
</template>

<style scoped>
.ptb-wi-link-text--primary {
  color: var(--vp-c-brand-1);
  font-weight: 600;
}

.ptb-wi-link-text--secondary {
  color: var(--vp-c-text-2);
  font-weight: 500;
  border-bottom: 1px dotted var(--vp-c-divider);
}

.ptb-wi-link-text:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
  border-radius: 0.375rem;
}
</style>
