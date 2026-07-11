<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getWikidataLabel } from './api'
import HealthBanner from './components/HealthBanner.vue'

const route = useRoute()
const typeLabel = ref<string | null>(null)

async function fetchTypeLabel() {
  if (route.params.typeQid) {
    try {
      typeLabel.value = await getWikidataLabel(route.params.typeQid as string)
    } catch {
      typeLabel.value = null
    }
  } else {
    typeLabel.value = null
  }
}

watch(() => route.params.typeQid, fetchTypeLabel, { immediate: true })

const pageTitle = computed(() => {
  if (route.path === '/') return 'Wikidata-OSM Matcher'
  if (route.params.typeQid) {
    const qid = route.params.typeQid
    if (typeLabel.value) return `Typ: ${typeLabel.value} (${qid})`
    return `Typ: ${qid}`
  }
  return 'Wikidata-OSM Matcher'
})
</script>

<template>
  <div class="app">
    <HealthBanner />
    <div class="container py-3">
      <header class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h4 mb-0">{{ pageTitle }}</h1>
        <nav v-if="route.path !== '/'">
          <router-link to="/" class="btn btn-outline-primary btn-sm">← Byt objekttyp</router-link>
        </nav>
      </header>
      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<style>
body {
  background-color: #f5f5f5;
}
</style>