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
   * ระดับความเกี่ยวข้องกับรายการบุคคล (ดู `.cursor/rules/ptb-word-index.mdc`)
   * — primary: เรื่องราวของผู้นั้นโดยตรง
   * — secondary: ผู้นั้นมีบทบาทสำคัญในเรื่อง (รวมผู้ถามที่นำไปสู่เหตุการณ์หรือผลสำคัญ เช่น บัญญัติสิกขาบท)
   */
  tier?: 'primary' | 'secondary'
}>()

const defaultLabel = 'เปิดความย่อในพระไตรปิฎกฉบับสำหรับประชาชน'

const linkTitle = computed(() => {
  const base = props.label ?? defaultLabel
  if (props.tier === 'primary') {
    return `${base} — อ้างอิงระดับ ๑: เนื้อหาเกี่ยวกับผู้นี้โดยตรง`
  }
  if (props.tier === 'secondary') {
    return `${base} — อ้างอิงระดับ ๒: บทบาทสำคัญในเรื่อง`
  }
  return base
})

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
