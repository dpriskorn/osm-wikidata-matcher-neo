import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { router } from './router'
import { i18n } from './i18n'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { Tooltip } from 'bootstrap'
import 'leaflet/dist/leaflet.css'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)
app.mount('#app')

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
tooltipTriggerList.forEach(el => new Tooltip(el))
