<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getObjectTypes, type ObjectTypeInfo } from '../api'

const emit = defineEmits<{
  select: [type: string]
}>()

const types = ref<ObjectTypeInfo[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    types.value = await getObjectTypes()
  } catch (e) {
    error.value = 'Kunde inte ladda objekttyper'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="selector">
    <h2>Välj objekttyp</h2>
    <p v-if="loading">Laddar...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <div v-else class="type-grid">
      <button
        v-for="t in types"
        :key="t.object_type"
        @click="emit('select', t.object_type)"
        class="type-btn"
      >
        {{ t.label }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.selector {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

h2 {
  margin-bottom: 16px;
  font-size: 1.1rem;
}

.type-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.type-btn {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #fafafa;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.type-btn:hover {
  background: #0066cc;
  color: white;
  border-color: #0066cc;
}

.error {
  color: #cc0000;
}
</style>
