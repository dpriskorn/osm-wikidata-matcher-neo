<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { getCandidates, type CandidateInfo } from '../api'

const props = defineProps<{
  type: string
}>()

const emit = defineEmits<{
  select: [qid: string]
}>()

const candidates = ref<CandidateInfo[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

async function load() {
  loading.value = true
  error.value = null
  try {
    candidates.value = await getCandidates(props.type)
  } catch (e) {
    error.value = 'Kunde inte ladda kandidater'
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.type, load)
</script>

<template>
  <div class="candidate-list">
    <h2>Objekt som behöver matchas</h2>
    <p v-if="loading">Laddar...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <ul v-else-if="candidates.length" class="list">
      <li
        v-for="c in candidates"
        :key="c.qid"
        @click="emit('select', c.qid)"
        class="item"
      >
        <span class="qid">{{ c.qid }}</span>
        <span class="label">{{ c.label }}</span>
        <span v-if="c.country_label" class="country">{{ c.country_label }}</span>
      </li>
    </ul>
    <p v-else>Inga objekt hittades.</p>
  </div>
</template>

<style scoped>
.candidate-list {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

h2 {
  margin-bottom: 16px;
  font-size: 1.1rem;
}

.list {
  list-style: none;
}

.item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s;
}

.item:hover {
  background: #f5f5f5;
}

.qid {
  font-family: monospace;
  font-size: 0.85rem;
  color: #666;
  min-width: 80px;
}

.label {
  flex: 1;
  font-weight: 500;
}

.country {
  font-size: 0.85rem;
  color: #888;
}

.error {
  color: #cc0000;
}
</style>
