<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useBackendHealth } from '../composables/useBackendHealth'

const { isBackendDown, startPolling, stopPolling } = useBackendHealth()

onMounted(startPolling)
onUnmounted(stopPolling)
</script>

<template>
  <div v-if="isBackendDown" class="alert alert-danger m-0 rounded-0 text-center" role="alert">
    Backend är nere – kan inte ansluta till API
  </div>
</template>
