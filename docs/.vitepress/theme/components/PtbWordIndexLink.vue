<script setup lang="ts">
/**
 * ลิงก์ไปความย่อในพระไตรปิฎกฉบับสำหรับประชาชน — แสดงเป็นข้อความ ใช้คู่กับ PtbWordIndexRefs (คลาส wi-entry__refs)
 */
defineProps<{
  href: string
  /** ข้อความบนลิงก์ + tooltip */
  label?: string
}>()

const defaultLabel = 'เปิดความย่อในพระไตรปิฎกฉบับสำหรับประชาชน'
</script>

<template>
  <a
    class="ptb-wi-link-text"
    :href="href"
    :title="label ?? defaultLabel"
  >
    {{ label ?? defaultLabel }}
  </a>
</template>

<style scoped>
.ptb-wi-link-text:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
  border-radius: 0.375rem;
}
</style>
