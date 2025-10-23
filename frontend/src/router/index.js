import { createRouter, createWebHistory } from 'vue-router'
import ReportDashboard from '@/features/research/pages/ReportDashboard.vue'
import ReportSearch from '@/features/research/pages/ReportSearch.vue'

const routes = [
    { path: '/', redirect: '/research/dashboard' },
    { path: '/research/dashboard', component: ReportDashboard },
    { path: '/research/search', component: ReportSearch },
]




export default createRouter({
    history: createWebHistory(),
    routes,
})