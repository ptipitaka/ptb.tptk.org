<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  PART3_PITAKA_PASSAGES,
  type Part3PitakaKey,
  type Part3PassageEntry,
} from '../part3PitakaPassages'

const props = defineProps<{
  /** ชื่อโฟลเดอร์ภายใต้ part-3-tipitaka-selected-passages/ — ลิงก์สุ่มเฉพาะในข้อของคัมภีร์นี้ */
  pitaka: Part3PitakaKey
}>()

const entries = PART3_PITAKA_PASSAGES[props.pitaka]
const fallback = entries[0] as Part3PassageEntry | undefined

/** หลัง mount สุ่ม; ก่อน hydrate ใช้รายการแรก (เรียงตาม id) ให้ตรง SSR */
const selected = ref<Part3PassageEntry | null>(null)

function pickRandom(): void {
  if (entries.length === 0) return
  const i = Math.floor(Math.random() * entries.length)
  selected.value = entries[i]!
}

const entry = computed(() => selected.value ?? fallback!)

const href = computed(() => {
  const e = entry.value
  if (!e) return '#'
  const frag = e.anchor || `p3-${e.id}`
  return `/part-3-tipitaka-selected-passages/${props.pitaka}/#${frag}`
})

onMounted(() => {
  pickRandom()
})
</script>

<template>
  <a :href="href">{{ entry.title }}</a>
</template>
