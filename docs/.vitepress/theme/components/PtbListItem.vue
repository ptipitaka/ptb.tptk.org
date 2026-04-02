<script setup lang="ts">
import { computed, getCurrentInstance, inject } from 'vue'
import type { PtbListContext } from './PtbList.vue'
import PtbMarkdownInline from './PtbMarkdownInline.vue'

const THAI_DIGITS = ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙']

const toThaiNumber = (value: number) => String(value).replace(/\d/g, (digit) => THAI_DIGITS[Number(digit)] ?? digit)

const props = withDefaults(defineProps<{
  marker?: string
  markerWidth?: string
  auto?: boolean
  /** Markdown ส่งมาเป็น string (เช่น "1.5" "2") — coerce ด้านล่าง */
  indentLevel?: number | string
  indent?: string
  /**
   * จองคอลัมน์ marker ให้กว้างเท่าเลขนำ (ใช้ร่วมกับ markerWidth บน PtbList) โดยไม่แสดงข้อความใน marker
   * — ให้เนื้อหาเริ่มที่คอลัมน์ขวาเดียวกับแถวที่มี marker="๑." ฯลฯ (เช่น บรรทัด «ตอบ» ให้ตรงแนวกับ «ถาม»)
   */
  markerSpacer?: boolean
  /**
   * ความเยื้องของบรรทัดต่อ (หลังตัดบรรทัด) เทียบบรรทัดแรก — ค่า CSS เช่น 15ch
   * (padding-left + text-indent บรรทัดแรกติดลบ ตาม custom.css .ptb-list-item__wrap-hanging)
   */
  wrapHanging?: string
}>(), {
  marker: '',
  markerWidth: '',
  auto: false,
  indentLevel: 0,
  indent: '',
  markerSpacer: false,
  wrapHanging: '',
})

/** แอตทริบิวต์ใน .md เป็น string — แปลงเป็นตัวเลขก่อนคำนวณ indent */
const indentLevelNum = computed(() => {
  const n = Number(props.indentLevel)
  return Number.isFinite(n) ? n : 0
})

const listContext = inject<PtbListContext | null>('ptb-list-context', null)
const isSplitGlossRow = computed(() => Boolean(listContext?.splitGloss))
const shouldUseAuto = computed(() => props.auto || Boolean(listContext?.auto))
const instanceId = getCurrentInstance()?.uid ?? 0

const computedMarker = computed(() => {
  if (props.marker) return props.marker
  if (!shouldUseAuto.value || !listContext) return ''
  return `${toThaiNumber(listContext.next(instanceId))}.`
})

/** ไม่มี marker จริง (รายการไม่มีเลข): อย่าสงวนความกว้าง 4ch — ไม่เช่นนั้น width: fit-content + กึ่งกลางจะดูเยื้อง */
const computedMarkerWidth = computed(() => {
  if (props.markerWidth) return props.markerWidth
  if (props.markerSpacer) return listContext?.markerWidth || '4ch'
  if (!computedMarker.value.length) return '0ch'
  return listContext?.markerWidth || '4ch'
})
const computedIndentLevel = computed(() => {
  if (indentLevelNum.value > 0) return indentLevelNum.value
  return listContext?.indentLevel ?? 1
})
const computedIndent = computed(() => {
  /* หลายคอลัมน์: PtbList ห่อใส่ padding-left แล้ว — รายการลูกอย่าเยื้องซ้ำ (คอลัมน์จะสมดุล) */
  if (listContext?.multiColumn) return '0'
  return props.indent || `calc(${computedIndentLevel.value} * var(--ptb-list-item-indent-per-level))`
})

const hasMarker = computed(() => computedMarker.value.length > 0)
const useMarkerSpacer = computed(() => props.markerSpacer)

/** รายการรายการระบุ wrapHanging เองจะทับค่าจาก PtbList */
const effectiveWrapHanging = computed(() => {
  const fromItem = (props.wrapHanging || '').trim()
  if (fromItem.length) return fromItem
  return (listContext?.wrapHanging || '').trim()
})

const wrapHangingVars = computed(() => {
  const v = effectiveWrapHanging.value
  if (!v.length) return undefined
  return { '--ptb-wrap-hanging': v } as Record<string, string>
})
const useWrapHanging = computed(() => Boolean(wrapHangingVars.value))

/** โหมด hanging (ไม่มี marker): รวม --ptb-wrap-hanging ที่ <p> — อย่าใช้ span ภายในเพราะทำให้ text-indent / ::first-line ของ p ไม่ครอบข้อความ */
const hangingBlockStyle = computed(() => ({
  '--ptb-marker-width': computedMarkerWidth.value,
  '--ptb-item-indent': computedIndent.value,
  ...(wrapHangingVars.value || {}),
}))
</script>

<template>
  <p
    v-if="useMarkerSpacer"
    class="ptb-list-item ptb-list-item--grid ptb-list-item--marker-spacer"
    :class="{ 'ptb-list-item--split-gloss-row': isSplitGlossRow }"
    :style="{ '--ptb-marker-width': computedMarkerWidth, '--ptb-item-indent': computedIndent }"
  >
    <span class="ptb-list-item__marker ptb-list-item__marker--spacer" aria-hidden="true" />
    <span
      class="ptb-list-item__content"
      :class="useWrapHanging ? 'ptb-list-item__wrap-hanging' : undefined"
      :style="wrapHangingVars"
    >
      <PtbMarkdownInline>
        <slot />
      </PtbMarkdownInline>
    </span>
  </p>

  <p
    v-else-if="!hasMarker"
    class="ptb-list-item ptb-list-item--hanging"
    :class="{ 'ptb-list-item--has-text-wrap-hanging': useWrapHanging }"
    :style="hangingBlockStyle"
  >
    <PtbMarkdownInline>
      <slot />
    </PtbMarkdownInline>
  </p>

  <p
    v-else
    class="ptb-list-item ptb-list-item--grid"
    :class="{ 'ptb-list-item--split-gloss-row': isSplitGlossRow }"
    :style="{ '--ptb-marker-width': computedMarkerWidth, '--ptb-item-indent': computedIndent }"
  >
    <span class="ptb-list-item__marker">{{ computedMarker }}</span>
    <span
      class="ptb-list-item__content"
      :class="useWrapHanging ? 'ptb-list-item__wrap-hanging' : undefined"
      :style="wrapHangingVars"
    >
      <PtbMarkdownInline>
        <slot />
      </PtbMarkdownInline>
    </span>
  </p>
</template>
