<template>
  <section class="container">
    <div class="wrap">
      <!-- FILTER BAR -->
      <div class="panel filters">
        <input v-model="state.query" placeholder="ค้นหา (title/keywords)" style="min-width:240px" />

        <span class="small">ปีตั้งแต่:</span>
        <input
          v-model.number="state.yearStart"
          type="number"
          style="width:110px"
          :min="MIN_YEAR"
          :max="MAX_YEAR"
          step="1"
          @keypress="blockMinus"
          @input="clampStart"
          @blur="clampStart"
        />

        <span class="small">ถึง:</span>
        <input
          v-model.number="state.yearEnd"
          type="number"
          style="width:110px"
          :min="MIN_YEAR"
          :max="MAX_YEAR"
          step="1"
          @keypress="blockMinus"
          @input="clampEnd"
          @blur="clampEnd"
        />

        <select v-model="state.category">
          <option value="">ทุก Category</option>
          <option v-for="c in facets.categories" :key="c" :value="c">{{ c }}</option>
        </select>

        <select v-model="state.type">
          <option value="">ทุก Type</option>
          <option v-for="t in facets.types" :key="t" :value="t">{{ t }}</option>
        </select>

        <select v-model="state.degree">
          <option value="">ทุก Degree</option>
          <option v-for="d in facets.degrees" :key="d" :value="d">{{ d }}</option>
        </select>

        <select v-model="state.advisor" style="min-width:280px">
          <option value="">ทุกอาจารย์</option>
          <option v-for="a in facets.advisors" :key="a" :value="a">{{ a }}</option>
        </select>

        <button class="ghost btn" @click="reset">ล้างตัวกรอง</button>
        <button class="primary btn" @click="exportCSV">Export CSV</button>
      </div>

      <!-- LEFT COLUMN -->
      <div>
        <div class="grid-kpi">
          <div class="kpi">
            <div class="l">ผลงานทั้งหมด</div>
            <div class="n">{{ results.length }}</div>
          </div>
          <div class="kpi">
            <div class="l">ปีล่าสุด</div>
            <div class="n">{{ latestYear || '—' }}</div>
          </div>
          <div class="kpi">
            <div class="l">204499</div>
            <div class="n">{{ results.filter(r=>r.type==='204499').length }}</div>
          </div>
          <div class="kpi">
            <div class="l">Co-operative</div>
            <div class="n">{{ results.filter(r=>r.type==='Co-operative').length }}</div>
          </div>
        </div>

        <div class="panel" style="margin-top:14px">
          <div class="small">ตารางผลงานล่าสุด</div>
          <table class="table">
            <thead>
              <tr>
                <th>ชื่อเรื่อง</th>
                <th>ปี</th>
                <th>Type</th>
                <th>Degree</th>
                <th>Category</th>
                <th>Advisor</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!results.length">
                <td colspan="6" class="small" style="color:#8b9099">—</td>
              </tr>
              <tr v-for="r in results" :key="r.id">
                <td>{{ r.title }}</td>
                <td>{{ r.year }}</td>
                <td><span class="badge">{{ r.type }}</span></td>
                <td>{{ r.degree || '—' }}</td>
                <td>{{ r.category }}</td>
                <td>{{ r.advisor }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- RIGHT COLUMN (3 แผนภูมิ) -->
      <div>
        <!-- 1) แนวโน้มรายปี -->
        <div class="panel chart wide" style="grid-column: 1 / 3;">
          <div class="small">แนวโน้มผลงานรายปี</div>
          <Line :data="chartYearData" :options="lineBarOptions" />
        </div>

        <!-- 2) สัดส่วนประเภทผลงาน (ย่อวงกลมเล็กลง + legend ขวา) -->
        <div class="panel chart" style="margin-top:14px; height: 320px;">
          <div class="small">สัดส่วนประเภทผลงาน</div>
          <Pie :data="chartTypeData" :options="pieOptions" />
        </div>

        <!-- 3) Top Research Groups -->
        <div class="panel chart wide" style="grid-column: 1 / 3; margin-top:14px;">
          <div class="small">Top Research Groups</div>
          <Bar :data="chartGroupsData" :options="lineBarOptions" />
        </div>
      </div>

      <div class="footer" style="grid-column:1/3">Dashboard</div>
    </div>
  </section>
</template>

<script setup>
/* Vue */
import { reactive, computed, onMounted, watch, ref } from 'vue'

/* Chart.js + vue-chartjs (+ datalabels) */
import { Line, Pie, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  LineElement, BarElement, ArcElement,
  CategoryScale, LinearScale, PointElement
} from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

ChartJS.register(
  Title, Tooltip, Legend,
  LineElement, BarElement, ArcElement,
  CategoryScale, LinearScale, PointElement,
  ChartDataLabels
)

/* Data service */
import { getFacets, searchPublications } from '@/services/search.service.js'

/* ====== YEAR LIMITS ====== */
const MIN_YEAR = 2021
const MAX_YEAR = 2025

/* ---- state ---- */
let state = reactive({
  query: '',
  advisor: '',
  category: '',
  type: '',
  degree: '',
  yearStart: MIN_YEAR,
  yearEnd: MAX_YEAR
})

let results = reactive([])
const facets = getFacets()

/* ====== THEME-AWARE COLORS (อ่านจาก CSS variables) ====== */
const TEXT = ref('#e8eaed')
const GRID = ref('rgba(255,255,255,0.08)')
const cssVar = (name, fallback) =>
  getComputedStyle(document.documentElement).getPropertyValue(name)?.trim() || fallback

function updateColors() {
  // ถ้า theme เปลี่ยนจะอัปเดตอัตโนมัติ
  TEXT.value = cssVar('--text', TEXT.value)
  // เดา grid จากธีมคร่าว ๆ
  const isLight = document.documentElement.getAttribute('data-theme') === 'light'
  GRID.value = isLight ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.08)'
}
onMounted(() => {
  updateColors()
  new MutationObserver(updateColors).observe(document.documentElement, {
    attributes: true, attributeFilter: ['data-theme']
  })
})

/* ====== YEAR GUARDS ====== */
const blockMinus = (e) => { if (e.key === '-') e.preventDefault() }
const clampStart = () => {
  if (state.yearStart == null || isNaN(state.yearStart)) state.yearStart = MIN_YEAR
  state.yearStart = Math.max(MIN_YEAR, Math.min(MAX_YEAR, state.yearStart))
  if (state.yearEnd != null && state.yearStart > state.yearEnd) state.yearEnd = state.yearStart
}
const clampEnd = () => {
  if (state.yearEnd == null || isNaN(state.yearEnd)) state.yearEnd = MAX_YEAR
  state.yearEnd = Math.max(MIN_YEAR, Math.min(MAX_YEAR, state.yearEnd))
  if (state.yearStart != null && state.yearEnd < state.yearStart) state.yearStart = state.yearEnd
}

/* ---- helpers ---- */
function applyFilters(rows) {
  const q = state.query.trim().toLowerCase()
  const y1 = Number(state.yearStart) || MIN_YEAR
  const y2 = Number(state.yearEnd) || MAX_YEAR
  return rows.filter(r => {
    if (q && !(r.title.toLowerCase().includes(q) || (r.abstract || '').toLowerCase().includes(q))) return false
    if (Number(r.year) < y1 || Number(r.year) > y2) return false
    if (state.category && r.category !== state.category) return false
    if (state.type && r.type !== state.type) return false
    if (state.degree && r.degree !== state.degree) return false
    if (state.advisor && r.advisor !== state.advisor) return false
    return true
  })
}

async function load() {
  const { items } = await searchPublications({})
  results.splice(0, results.length, ...applyFilters(items))
}
watch(state, () => { load() }, { deep: true })

function reset() {
  Object.assign(state, {
    query: '',
    advisor: '',
    category: '',
    type: '',
    degree: '',
    yearStart: MIN_YEAR,
    yearEnd: MAX_YEAR
  })
  load()
}

/* ---- KPIs ---- */
const latestYear = computed(() =>
  results.reduce((m, r) => Math.max(m, Number(r.year) || 0), 0)
)

/* ---- Charts ---- */
const typeColors = ['#42A5F5','#66BB6A','#FFA726','#AB47BC','#EC407A','#26C6DA']

const lineBarOptions = computed(() => ({
  responsive: true,
  plugins: { legend: { labels: { color: TEXT.value } }, datalabels: { display: false } },
  scales: {
    x: { ticks: { color: TEXT.value }, grid: { color: GRID.value } },
    y: { ticks: { color: TEXT.value }, grid: { color: GRID.value } }
  }
}))

/* ✅ ย่อ “วงกลม” เล็กลง และทำสี legend ให้คอนทราสต์ตามธีม */
const pieOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { top: 8, right: 8, bottom: 8, left: 8 } },
  plugins: {
    legend: {
      position: 'right',
      labels: { boxWidth: 14, boxHeight: 14, padding: 10, color: TEXT.value }
    },
    datalabels: {
      clamp: true, clip: false,
      color: '#fff',
      font: { weight: 'bold', size: 11 },
      formatter: (value, ctx) => {
        const ds = ctx.chart.data.datasets[0]
        const total = ds.data.reduce((a,b)=>a+b, 0) || 1
        const pct = (value / total) * 100
        return pct >= 5 ? `${pct.toFixed(0)}%` : ''
      }
    },
    tooltip: {
      callbacks: {
        label: (c) => {
          const v = c.parsed
          const ds = c.chart.data.datasets[0]
          const total = ds.data.reduce((a,b)=>a+b, 0) || 1
          const pct = ((v/total)*100).toFixed(1)
          return ` ${c.label}: ${v} (${pct}%)`
        }
      }
    }
  },
  elements: { arc: { borderWidth: 1 } }
}))

/* 1) แนวโน้มรายปี: ตรึงแกน 2021–2025 */
const chartYearData = computed(() => {
  const baseline = ['2021','2022','2023','2024','2025']
  const countByYear = Object.fromEntries(baseline.map(y => [y, 0]))
  results.forEach(r => { const y = String(r.year); if (countByYear[y] != null) countByYear[y]++ })
  return {
    labels: baseline,
    datasets: [{
      label: 'จำนวนผลงาน',
      data: baseline.map(y => countByYear[y]),
      borderColor: '#8ab4f8',
      backgroundColor: '#8ab4f880',
      fill: true,
      tension: 0.25
    }]
  }
})

/* 2) สัดส่วนประเภทผลงาน (radius 82% เพื่อย่อวงกลม) */
const chartTypeData = computed(() => {
  const labels = (facets.types && facets.types.length)
    ? facets.types
    : ['204499','Co-operative','Other Type']
  const counts = {}
  results.forEach(r => { counts[r.type] = (counts[r.type] || 0) + 1 })
  const data = labels.map((t, i) => counts[t] ?? ([12,5,8][i] ?? 0))
  return {
    labels,
    datasets: [{
      data,
      radius: '82%', // 👈 ย่อวงกลมลงเล็กน้อย
      backgroundColor: labels.map((_,i)=> typeColors[i % typeColors.length])
    }]
  }
})

/* 3) Top Research Groups: mock */
const chartGroupsData = {
  labels: ['NLP Lab','Vision Lab','IoT Lab','Security Lab'],
  datasets: [{
    label: 'จำนวนผลงาน',
    data: [14, 10, 7, 5],
    backgroundColor: '#8ab4f8'
  }]
}

/* ---- export ---- */
function exportCSV() {
  if (!results.length) return
  const cols = ['title','year','type','degree','category','advisor']
  const head = cols.join(',')
  const esc = s => String(s ?? '').replace(/"/g, '""')
  const lines = results.map(r => cols.map(c => `"${esc(r[c])}"`).join(',')).join('\n')
  const csv = head + '\n' + lines
  const blob = new Blob([csv], { type: 'text/csv' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'dashboard-alt.csv'
  a.click()
  URL.revokeObjectURL(a.href)
}

/* เริ่มต้นด้วยการ clamp และโหลดข้อมูล */
clampStart()
clampEnd()
onMounted(load)
</script>
