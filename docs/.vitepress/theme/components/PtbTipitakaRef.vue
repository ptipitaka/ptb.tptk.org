<script setup lang="ts">
import { computed } from 'vue'
import PtbMarkdownInline from './PtbMarkdownInline.vue'

const props = withDefaults(
  defineProps<{
    /** ตำแหน่งข้อความอ้างอิงใต้คำพูด — ค่าเริ่มต้นตรงกับแบบเดิม (ชิดขวา) */
    align?: 'left' | 'center' | 'right'
  }>(),
  { align: 'right' },
)

const alignClass = computed(() => {
  const map = {
    left: 'ptb-quote-citation--left',
    center: 'ptb-quote-citation--center',
    right: 'ptb-quote-citation--right',
  }
  return map[props.align]
})
</script>

<template>
  <p
    class="ptb-tipitaka-ref ptb-quote-citation ptb-text-xs ptb-paragraph-no-indent"
    :class="alignClass"
  >
    <PtbMarkdownInline>
      <slot />
    </PtbMarkdownInline>
  </p>
</template>
