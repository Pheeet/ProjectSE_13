import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@/styles/research.css'

/* ===== THEME BOOTSTRAP ===== */
const THEME_KEY = 'csrs-theme'
const prefersLight =
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: light)').matches

const initial = localStorage.getItem(THEME_KEY) || (prefersLight ? 'light' : 'dark')
document.documentElement.setAttribute('data-theme', initial)

window.__toggleTheme = () => {
    const cur = document.documentElement.getAttribute('data-theme') || 'dark'
    const next = cur === 'light' ? 'dark' : 'light'
    document.documentElement.setAttribute('data-theme', next)
    localStorage.setItem(THEME_KEY, next)
}

/* ===== MOUNT ===== */
createApp(App).use(router).mount('#app')