<script setup lang="ts">
import PtbMarkdownInline from './PtbMarkdownInline.vue'

/** ลิงก์ fragment เช่น `#AbCdEfGhIj` — ใช้รหัสถาวรแบบเดียวกับ `{#… .ptb-h-block}` บนหัวข้อ */
defineProps<{
  id?: string
}>()
</script>

<template>
  <p
    class="ptb-paragraph"
    :id="id"
    :tabindex="id ? -1 : undefined"
  >
    <PtbMarkdownInline>
      <slot />
    </PtbMarkdownInline>
  </p>
</template>
