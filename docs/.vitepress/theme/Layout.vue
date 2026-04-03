<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import ChatWidget from './components/ChatWidget.vue'

const Layout = DefaultTheme.Layout
</script>

<template>
  <Layout>
    <template #layout-bottom>
      <ChatWidget />
    </template>
  </Layout>
</template>
