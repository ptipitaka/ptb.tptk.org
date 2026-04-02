<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useRoute, useData } from 'vitepress'
import { computed } from 'vue'

const Layout = DefaultTheme.Layout
const route = useRoute()
const { frontmatter } = useData()

const searchKeywordsText = computed(() => {
  const kw = frontmatter.value.searchKeywords
  if (!kw) return ''
  return Array.isArray(kw) ? kw.join(', ') : String(kw)
})

const searchContentText = computed(() => {
  return frontmatter.value.searchContent || ''
})

const hasSearchData = computed(() => {
  return !!(searchKeywordsText.value || searchContentText.value)
})
</script>

<template>
  <Layout>
    <template #doc-before>
      <div
        v-if="hasSearchData"
        class="vp-search-hidden"
        data-pagefind-body
        aria-hidden="true"
      >
        <!-- searchContent: เนื้อหาเต็ม (transcript) — Pagefind ใช้สร้าง excerpt ที่มีบริบท -->
        <p v-if="searchContentText">{{ searchContentText }}</p>
        <!-- searchKeywords: คำค้นเสริม — ช่วยให้ match ชื่อเฉพาะที่อาจไม่อยู่ในเนื้อหาหลัก -->
        <span v-if="searchKeywordsText" data-pagefind-meta="keywords">{{ searchKeywordsText }}</span>
      </div>
    </template>
  </Layout>
</template>

<style scoped>
.vp-search-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
