
import '@/assets/main.css'
import '@/assets/main'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'

import axios from "axios";
import type { AxiosInstance } from "axios";
import $ from "jquery";

const app = createApp(App)

const API_HOST: string = import.meta.env.VITE_BACKEND_HOST || 'api.aufrutten.com'
const API_DEBUG_HOST: string = import.meta.env.VITE_DEBUG_BACKEND_HOST || 'api.aufrutten.local'

const apiConfig: {} = {
  'withCredentials': true,
  'baseURL': import.meta.env.PROD  ? `https://${API_HOST}` : `https://${API_DEBUG_HOST}`,
}

declare global {
  interface Window {
    api: AxiosInstance,
    $: any,
  }
}
window.$ = $

window.api = axios.create(apiConfig)
window.api.defaults.headers['Accept'] = 'application/json'
window.api.defaults.headers['Content-Type'] = 'application/json'

const accessToken: string|null = localStorage.getItem('access_token')
if (accessToken !== null){ window.api.defaults.headers['Authorization'] = `Bearer ${accessToken}` }

const title = document.querySelector('title');
if (title){title.innerHTML = import.meta.env.VITE_PROJECT_NAME}

app.use(createPinia())
app.use(router)

app.mount('#app')
