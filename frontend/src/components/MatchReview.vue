<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMatches, confirmMatch, rejectMatch, type MatchResponse } from '../api'

const props = defineProps<{
  type: string
  qid: string
}>()

const emit = defineEmits<{
  back: []
}>()

const loading = ref(true)
const error = ref<string | null>(null)
const data = ref<MatchResponse | null>(null)
const confirming = ref(false)
const rejecting = ref(false)
const statusMsg = ref<string | null>(null)

onMounted(async () => {
  await load()
})

async function load() {
  loading.value = true
  error.value = null
  statusMsg.value = null
  try {
    data.value = await getMatches(props.type, props.qid)
  } catch (e) {
    error.value = 'Kunde inte ladda matcher'
  } finally {
    loading.value = false
  }
}

async function handleConfirm(osmId: string, osmType: string, osmName: string) {
  confirming.value = true
  statusMsg.value = null
  try {
    await confirmMatch(props.type, props.qid, osmId, osmType, osmName)
    statusMsg.value = 'Matchning sparad!'
    setTimeout(() => emit('back'), 1500)
  } catch (e) {
    error.value = 'Kunde inte spara matchning'
  } finally {
    confirming.value = false
  }
}

async function handleReject() {
  rejecting.value = true
  statusMsg.value = null
  try {
    await rejectMatch(props.type, props.qid)
    statusMsg.value = 'Markerad som "ingen match"'
    setTimeout(() => emit('back'), 1500)
  } catch (e) {
    error.value = 'Kunde inte spara'
  } finally {
    rejecting.value = false
  }
}

function openWikidata() {
  window.open(`https://www.wikidata.org/wiki/${props.qid}`, '_blank')
}
</script>

<template>
  <div class="match-review">
    <button @click="emit('back')" class="back-btn">← Tillbaka</button>

    <div class="header">
      <h2>{{ data?.label || qid }}</h2>
      <button @click="openWikidata" class="link-btn">Öppna i Wikidata ↗</button>
    </div>

    <p v-if="loading">Laddar...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="statusMsg" class="status">{{ statusMsg }}</p>

    <div v-if="data && data.matches.length === 0" class="no-matches">
      <p>Inga OSM-kandidater hittades.</p>
      <button
        @click="handleReject"
        :disabled="rejecting"
        class="reject-btn"
      >
        {{ rejecting ? 'Sparar...' : 'Markera som "ingen match"' }}
      </button>
    </div>

    <ul v-if="data && data.matches.length" class="matches">
      <li v-for="m in data.matches" :key="m.osm_id" class="match">
        <div class="match-header">
          <a :href="m.osm_url" target="_blank" class="osm-link">
            {{ m.osm_type.toUpperCase() }}/{{ m.osm_id }}
          </a>
          <span class="similarity" :class="m.similarity >= 0.7 ? 'high' : m.similarity >= 0.5 ? 'medium' : 'low'">
            {{ Math.round(m.similarity * 100) }}% match
          </span>
        </div>
        <p class="osm-name">{{ m.osm_name }}</p>
        <button
          @click="handleConfirm(m.osm_id, m.osm_type, m.osm_name)"
          :disabled="confirming"
          class="confirm-btn"
        >
          {{ confirming ? 'Sparar...' : 'Bekräfta' }}
        </button>
      </li>
    </ul>

    <div v-if="data && data.matches.length > 1" class="reject-section">
      <button
        @click="handleReject"
        :disabled="rejecting"
        class="reject-btn secondary"
      >
        {{ rejecting ? 'Sparar...' : 'Ingen av dessa matchar' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.match-review {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.back-btn {
  background: none;
  border: none;
  color: #0066cc;
  cursor: pointer;
  margin-bottom: 16px;
  font-size: 0.9rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  font-size: 1.2rem;
}

.link-btn {
  background: none;
  border: none;
  color: #0066cc;
  cursor: pointer;
  font-size: 0.9rem;
}

.matches {
  list-style: none;
}

.match {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 12px;
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.osm-link {
  font-family: monospace;
  color: #0066cc;
  text-decoration: none;
}

.osm-link:hover {
  text-decoration: underline;
}

.similarity {
  font-size: 0.85rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
}

.similarity.high {
  background: #d4edda;
  color: #155724;
}

.similarity.medium {
  background: #fff3cd;
  color: #856404;
}

.similarity.low {
  background: #f8d7da;
  color: #721c24;
}

.osm-name {
  margin-bottom: 12px;
  color: #666;
}

.confirm-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.confirm-btn:hover {
  background: #218838;
}

.confirm-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.reject-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.reject-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.reject-btn:hover {
  background: #c82333;
}

.reject-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.reject-btn.secondary {
  background: #6c757d;
}

.reject-btn.secondary:hover {
  background: #5a6268;
}

.no-matches {
  text-align: center;
  padding: 40px;
}

.error {
  color: #cc0000;
  margin-bottom: 12px;
}

.status {
  color: #28a745;
  margin-bottom: 12px;
}
</style>
