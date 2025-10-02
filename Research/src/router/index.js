import { createRouter, createWebHistory } from 'vue-router'
import ResearchHorizontal from '@/features/research/pages/ResearchHorizontal.vue'
import ResearchVertical from '@/features/research/pages/ResearchVertical.vue'

const routes = [
    { path: '/', redirect: '/research/horizontal' },
    { path: '/research/horizontal', component: ResearchHorizontal },
    { path: '/research/vertical', component: ResearchVertical },
]

export default createRouter({
    history: createWebHistory(),
    routes,
})