<script setup lang="ts">
import { computed, provide, ref } from 'vue'

export type PtbListContext = {
  auto: boolean
  markerWidth: string
  indentLevel: number
  /** รายการแยกวงเล็บ — ลูกใช้ display:contents เพื่อเข้ากริดเดียวกับพ่อ */
  splitGloss: boolean
  /** columns > 1 — เยื้องที่ .ptb-list แทน padding ต่อรายการ (ให้คอลัมน์สมดุล) */
  multiColumn: boolean
  /** ค่าเริ่ม wrap-hanging ให้ทุก PtbListItem — รายการรายการใส่ wrapHanging เองจะทับ */
  wrapHanging: string
  next: (itemId: number) => number
}

const props = withDefaults(defineProps<{
  auto?: boolean
  /** Markdown ส่งมาเป็น string (เช่น start="5") — coerce ด้านล่าง */
  start?: number | string
  markerWidth?: string
  /** Markdown ส่งมาเป็น string — coerce ก่อน provide ให้ลูก */
  indentLevel?: number | string
  /** ลิงก์ fragment เช่น `#AbCdEfGhIj` — แบบเดียวกับ id บนหัวข้อ `.ptb-h-block` */
  id?: string
  topGap?: string
  bottomGap?: string
  /**
   * จัดบล็อกรายการให้กึ่งกลางในแนวนอน (ภายในคอลัมน์เนื้อหา): ความกว้างตามเนื้อหา + margin ซ้าย/ขวา auto
   * หรือใช้ class `ptb-list--center` แทนได้
   */
  centered?: boolean
  /**
   * จำนวนคอลัมน์ของรายการ (เช่น 2) — ลำดับเลขใน DOM ยังเป็น ๑ ๒ ๓ … ตามลำดับการอ่านที่กำหนดด้วย columnOrder
   */
  columns?: number | string
  /**
   * เมื่อ columns > 1: `row` = เติมแถวละซ้าย→ขวาแล้วลงแถว (๑|๒ / ๓|๔)
   * `column` = เติมคอลัมน์ซ้ายบน→ล่างแล้วไปคอลัมน์ขวา (๑–๕ คอลัมน์ซ้าย ๖–๑๐ คอลัมน์ขวา)
   */
  columnOrder?: 'row' | 'column'
  /**
   * กำหนดคอลัมน์เมื่อ columns > 1:
   * - ค่าเดียว (ไม่มี comma): ความกว้างขั้นต่ำต่อแทร็ก เช่น `18rem` `min(24ch,100%)` → minmax(ค่า, 1fr) ทุกคอลัมน์
   * - หลายค่าคั่นด้วย comma เป็นตัวเลขเท่านั้น: สัดส่วน fr ต่อคอลัมน์ (เหมือนตัวคูณระดับ indent) เช่น `0.5,1` → minmax(0,0.5fr) minmax(0,1fr)
   */
  columnMinWidth?: string
  /**
   * แยกคำอธิบายในวงเล็บไปคอลัมน์ขวา: ใช้ `marker="…"` เป็นข้อความหลัก + slot เป็นวงเล็บ — คอลัมน์ขวากว้างคงที่ (`glossColumnWidth`) ให้จุดเริ่ม `(` ตรงแนวกัน
   */
  splitGloss?: boolean
  /** ความกว้างคอลัมน์วงเล็บ (CSS) เมื่อ splitGloss — เช่น `15ch` `min(16ch, 40%)` */
  glossColumnWidth?: string
  /**
   * ความกว้างสูงสุดข้อความใน marker (CSS) เมื่อ splitGloss — ใช้เป็น max-width ให้ข้อความยาวขึ้นบรรทัดใหม่
   * (คอลัมน์ซ้ายกว้างตามข้อความที่ยาวที่สุดในรายการโดยอัตโนมัติ ไม่เติมช่องว่างถึงค่านี้ทุกแถว)
   */
  glossLeftMax?: string
  /**
   * บรรทัดต่อเยื้องเทียบบรรทัดแรก (เช่น 15ch) — เหมือนใส่ wrapHanging นี้ในทุก PtbListItem ภายใน
   */
  wrapHanging?: string
}>(), {
  auto: false,
  start: 1,
  markerWidth: '4ch',
  indentLevel: 1,
  topGap: '0.5em',
  bottomGap: '0.2em',
  centered: false,
  columns: 1,
  columnOrder: 'row',
  columnMinWidth: '',
  splitGloss: false,
  glossColumnWidth: '15ch',
  glossLeftMax: '32ch',
  wrapHanging: '',
})

const normalizedStart = Number(props.start)
const counter = ref(Number.isFinite(normalizedStart) ? normalizedStart : 1)
const assignedNumbers = new Map<number, number>()

const columnsNum = computed(() => {
  const n = Number(props.columns)
  return Number.isFinite(n) && n > 1 ? Math.floor(n) : 1
})

/** ค่าเช่น `0.5,1` → สัดส่วน fr ต่อคอลัมน์ (ต้องเป็นตัวเลขทุกชิ้น) */
function parseColumnFrWeights(str: string): number[] | null {
  if (!str.includes(',')) return null
  const parts = str.split(',').map((s) => s.trim()).filter(Boolean)
  if (parts.length < 2) return null
  const nums = parts.map((p) => Number(p))
  if (!nums.every((n) => Number.isFinite(n) && n > 0)) return null
  return nums
}

const columnFrWeights = computed(() => {
  const raw = props.columnMinWidth?.trim()
  if (!raw) return null
  return parseColumnFrWeights(raw)
})

const columnFrTemplate = computed(() => {
  const weights = columnFrWeights.value
  if (!weights?.length || columnsNum.value <= 1) return ''
  const n = columnsNum.value
  const w = [...weights.slice(0, n)]
  while (w.length < n) w.push(1)
  return w.map((x) => `minmax(0, ${x}fr)`).join(' ')
})

const resolvedIndentLevel = computed(() => {
  const n = Number(props.indentLevel)
  return Number.isFinite(n) ? n : 1
})

const listWrapStyle = computed(() => {
  const style: Record<string, string> = {
    '--ptb-list-top-gap': props.topGap,
    '--ptb-list-bottom-gap': props.bottomGap,
  }
  if (props.splitGloss) {
    style['--ptb-list-right-col'] = props.glossColumnWidth
    style['--ptb-list-left-col'] = props.glossLeftMax
    style['--ptb-list-body-indent'] = `calc(${resolvedIndentLevel.value} * var(--ptb-list-item-indent-per-level))`
  }
  if (columnsNum.value > 1) {
    style['--ptb-list-cols'] = String(columnsNum.value)
    /* เยื้องทั้งบล็อกครั้งเดียว — รายการลูกไม่ใส่ padding-left ซ้ำ (ดูคอลัมน์เท่ากัน) */
    style['paddingLeft'] = `calc(${resolvedIndentLevel.value} * var(--ptb-list-item-indent-per-level))`
  }
  const raw = props.columnMinWidth?.trim()
  if (columnsNum.value <= 1 || !raw) return style

  if (columnFrWeights.value) {
    const t = columnFrTemplate.value
    if (t) style['--ptb-list-cols-template'] = t
  } else if (!raw.includes(',')) {
    /* ค่าเดียวเช่น 18rem — ถ้ามี comma แต่ parse fr ไม่ผ่าน อย่าใส่ "1,1,1" ลง --ptb-list-col-min (ไม่ใช่ความยาว CSS เดี่ยว) */
    style['--ptb-list-col-min'] = raw
  }
  return style
})

const listLayoutClass = computed(() => {
  const n = columnsNum.value
  return {
    'ptb-list--multi-col': n > 1,
    'ptb-list--order-row': n > 1 && props.columnOrder === 'row',
    'ptb-list--order-column': n > 1 && props.columnOrder === 'column',
    'ptb-list--col-min':
      n > 1 &&
      Boolean(props.columnMinWidth?.trim()) &&
      !columnFrWeights.value,
    'ptb-list--col-fr': n > 1 && Boolean(columnFrTemplate.value),
    [`ptb-list--cols-${n}`]: n > 1,
  }
})

provide<PtbListContext>('ptb-list-context', {
  auto: props.auto,
  markerWidth: props.markerWidth,
  get splitGloss() {
    return props.splitGloss
  },
  get indentLevel() {
    return resolvedIndentLevel.value
  },
  get multiColumn() {
    return columnsNum.value > 1
  },
  get wrapHanging() {
    return (props.wrapHanging || '').trim()
  },
  next: (itemId: number) => {
    const existing = assignedNumbers.get(itemId)
    if (existing != null) return existing
    const value = counter.value
    assignedNumbers.set(itemId, value)
    counter.value += 1
    return value
  },
})
</script>

<template>
  <div
    :id="props.id"
    class="ptb-list"
    :class="[
      { 'ptb-list--center': props.centered, 'ptb-list--split-gloss': props.splitGloss },
      listLayoutClass,
    ]"
    :style="listWrapStyle"
    :tabindex="props.id ? -1 : undefined"
  >
    <slot />
  </div>
</template>
