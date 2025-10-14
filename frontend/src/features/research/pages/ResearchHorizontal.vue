<template>
  <section class="container">
    <div class="wrap">
      <!-- FILTER BAR -->
      <div class="panel filters">
        <input v-model="state.query" placeholder="ค้นหา (title/keywords)" style="min-width:240px" />
        <span class="small">ปีตั้งแต่:</span>
        <input v-model.number="state.yearStart" type="number" style="width:110px" />
        <span class="small">ถึง:</span>
        <input v-model.number="state.yearEnd" type="number" style="width:110px" />

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
        <div class="panel chart">
          <div class="small">แนวโน้มผลงานรายปี</div>
          <Line :data="chartYearData" :options="lineBarOptions" />
        </div>

        <!-- 2) สัดส่วนประเภทผลงาน (ขยายสูง + datalabels + legend ล่าง) -->
        <div class="panel chart" style="margin-top:14px; height: 260px;">
          <div class="small">สัดส่วนประเภทผลงาน</div>
          <Pie :data="chartTypeData" :options="pieOptions" />
        </div>

        <!-- 3) Top Research Groups -->
        <div class="panel chart" style="margin-top:14px">
          <div class="small">Top Research Groups</div>
          <Bar :data="chartGroupsData" :options="lineBarOptions" />
        </div>
      </div>

      <div class="footer" style="grid-column:1/3">Dashboard</div> <!-- 3) Top Research Groups -->
    </div>
  </section>
</template>

<script setup>
/* Vue */
import { reactive, computed, onMounted, watch } from 'vue'

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

/* ---- state ---- */
let state = reactive({
  query: '',
  advisor: '',
  category: '',
  type: '',
  degree: '',
  yearStart: '',
  yearEnd: ''
})

let results = reactive([])
const facets = getFacets()

/* ---- helpers ---- */
function applyFilters(rows) {
  const q = state.query.trim().toLowerCase()
  const y1 = Number(state.yearStart) || 0
  const y2 = Number(state.yearEnd) || 9999
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

watch(state, (newVal, oldVal) => {
  // หากมีการเปลี่ยนแปลงใน state ให้เรียก load() ใหม่
  // อาจจะมีการ Debounce เพื่อป้องกันการยิง API ถี่เกินไป
  load()
}, { deep: true }) // ต้องใช้ deep: true เพราะ state เป็น reactive object

function reset() {
  Object.assign(state, { query:'', advisor:'', category:'', type:'', degree:'', yearStart:'', yearEnd:'' })
  load()
}

/* ---- KPIs ---- */
const latestYear = computed(() =>
  results.reduce((m, r) => Math.max(m, Number(r.year) || 0), 0)
)

/* ---- Charts ---- */
const typeColors = ['#42A5F5','#66BB6A','#FFA726','#AB47BC','#EC407A','#26C6DA']

const lineBarOptions = {
  responsive: true,
  plugins: { legend: { labels: { color: '#e8eaed' } }, datalabels: { display: false } },
  scales: {
    x: { ticks: { color: '#e8eaed' }, grid: { color: 'rgba(255,255,255,0.08)' } },
    y: { ticks: { color: '#e8eaed' }, grid: { color: 'rgba(255,255,255,0.08)' } }
  }
}

const pieOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom', labels: { color: '#e8eaed' } },
    datalabels: {
      color: '#fff',
      font: { weight: 'bold' },
      formatter: (value, ctx) => {
        const ds = ctx.chart.data.datasets[0]
        const total = ds.data.reduce((a,b)=>a+b, 0) || 1
        const pct = (value / total) * 100
        return pct >= 3 ? `${pct.toFixed(0)}%` : ''   
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
  }
}

/* 1) แนวโน้มรายปี: คำนวณจาก results */
const chartYearData = computed(() => {
  const countByYear = {}
  results.forEach(r => {
    const y = String(r.year)
    countByYear[y] = (countByYear[y] || 0) + 1
  })
  const labels = Object.keys(countByYear).sort()
  const data = labels.map(l => countByYear[l])

  // fallback เผื่อยังไม่มีข้อมูล
  const finalLabels = labels.length ? labels : ['2021','2022','2023','2024','2025']
  const finalData = labels.length ? data : [0,0,0,0,0]

  return {
    labels: finalLabels,
    datasets: [{
      label: 'จำนวนผลงาน',
      data: finalData,
      borderColor: '#8ab4f8',
      backgroundColor: '#8ab4f880',
      fill: true,
      tension: 0.25
    }]
  }
})

/* 2) สัดส่วนประเภทผลงาน: คำนวณจาก results (fallback เป็น mock) */
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

onMounted(load)
</script>
