<script setup lang="ts">
import { ref } from 'vue'
import ObjectTypeSelector from './components/ObjectTypeSelector.vue'
import CandidateList from './components/CandidateList.vue'
import MatchReview from './components/MatchReview.vue'

const selectedType = ref<string | null>(null)
const selectedQid = ref<string | null>(null)

function onTypeSelected(type: string) {
  selectedType.value = type
  selectedQid.value = null
}

function onCandidateSelected(qid: string) {
  selectedQid.value = qid
}
</script>

<template>
  <div class="app">
    <header>
      <h1>Wikidata-OSM Matcher</h1>
    </header>
    <main>
      <ObjectTypeSelector v-if="!selectedType" @select="onTypeSelected" />
      <template v-else>
        <button @click="selectedType = null; selectedQid = null" class="back-btn">
          ← Byt objekttyp
        </button>
        <MatchReview
          v-if="selectedQid"
          :type="selectedType"
          :qid="selectedQid"
          @back="selectedQid = null"
        />
        <CandidateList
          v-else
          :type="selectedType"
          @select="onCandidateSelected"
        />
      </template>
    </main>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
  color: #333;
}

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  margin-bottom: 20px;
}

h1 {
  font-size: 1.5rem;
  color: #1a1a1a;
}

.back-btn {
  background: none;
  border: none;
  color: #0066cc;
  cursor: pointer;
  margin-bottom: 16px;
  font-size: 0.9rem;
}

.back-btn:hover {
  text-decoration: underline;
}
</style>
