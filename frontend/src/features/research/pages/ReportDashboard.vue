<template>
  <section class="container">
    <div class="wrap">
      <!-- FILTER BAR -->
      <div class="panel filters">
        <input
          v-model="state.query"
          placeholder="ค้นหา (title/keywords)"
          style="min-width: 240px"
        />

        <span class="small">ปีตั้งแต่:</span>
        <input
          v-model.number="state.yearStart"
          type="number"
          style="width: 110px"
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
          style="width: 110px"
          :min="MIN_YEAR"
          :max="MAX_YEAR"
          step="1"
          @keypress="blockMinus"
          @input="clampEnd"
          @blur="clampEnd"
        />

        <select v-model="state.category">
          <option value="">ทุก Category</option>
          <option v-for="c in facets.categories" :key="c" :value="c">
            {{ c }}
          </option>
        </select>

        <select v-model="state.type">
          <option value="">ทุก Type</option>
          <option v-for="t in facets.types" :key="t" :value="t">{{ t }}</option>
        </select>

        <select v-model="state.degree">
          <option value="">ทุก Degree</option>
          <option v-for="d in facets.degrees" :key="d" :value="d">
            {{ d }}
          </option>
        </select>

        <select v-model="state.advisor" style="min-width: 280px">
          <option value="">ทุกอาจารย์</option>
          <option v-for="a in facets.advisors" :key="a" :value="a">
            {{ a }}
          </option>
        </select>

        <div class="filters-actions">
          <button class="ghost btn" @click="reset">ล้างตัวกรอง</button>
          <button class="primary btn export" @click="exportCSV">Export CSV</button>
          <button class="primary btn print" @click="printDashboard">Print</button>
        </div>
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
            <div class="n">{{ latestYear || "—" }}</div>
          </div>
          <div class="kpi">
            <div class="l">Most Active Degree</div>
            <div class="n">{{ categoryInsights.topDegree || "—" }}</div>
          </div>
          <div class="kpi">
            <div class="l">Most Popular Category</div>
            <div class="n">
              <template v-if="categoryInsights.topCategory">
                {{ categoryInsights.topCategory }}
              </template>
              <template v-else>—</template>
            </div>
          </div>
        </div>

        <div class="panel" style="margin-top: 14px">
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
                <td colspan="6" class="small" style="color: #8b9099">—</td>
              </tr>
              <tr v-for="r in results" :key="r.id">
                <td>{{ r.title }}</td>
                <td>{{ r.year }}</td>
                <td>
                  <span class="badge">{{ r.type }}</span>
                </td>
                <td>{{ r.degree || "—" }}</td>
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
        <div class="panel chart wide" style="grid-column: 1 / 3">
          <div class="small">แนวโน้มผลงานรายปี</div>
          <Line :data="chartYearData" :options="lineBarOptions" />
        </div>

        <!-- 2) สัดส่วนประเภทผลงาน (ย่อวงกลมเล็กลง + legend ขวา) -->
        <div class="panel chart" style="margin-top: 14px; height: 320px">
          <div class="small">สัดส่วนประเภทผลงาน</div>
          <Pie :data="chartTypeData" :options="pieOptions" />
        </div>

        <!-- 3) Top Research Groups -->
        <div
          class="panel chart wide"
          style="grid-column: 1 / 3; margin-top: 14px"
        >
          <div class="small">อาจารย์ที่ปรึกษายอดนิยม</div>
          <Bar :data="chartGroupsData" :options="lineBarOptions" />
        </div>
      </div>

      <div class="footer" style="grid-column: 1/3">Dashboard</div>
    </div>
  </section>
</template>

<script setup>
/* Vue */
import { reactive, computed, onMounted, watch, ref } from "vue";

/* Chart.js + vue-chartjs (+ datalabels) */
import { Line, Pie, Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  ChartDataLabels
);

/* Data service */
import { getFacets, searchPublications } from "@/services/search.service.js";

/* ====== CONFIGURATIONS ====== */
const TOP_N_ADVISORS = 4; 
const CSV_EXPORT_COLUMNS = [
  "title",
  "year",
  "type",
  "degree",
  "category",
  "advisor",
];

/* ====== YEAR LIMITS ====== */
const facets = getFacets();
const MIN_YEAR = computed(() => facets.minYear);
const MAX_YEAR = computed(() => facets.maxYear);
/* ---- state ---- */
let state = reactive({
  query: "",
  advisor: "",
  category: "",
  type: "",
  degree: "",
  yearStart: facets.minYear,
  yearEnd: facets.maxYear,
});

// 1. เฝ้าดูค่า minYear จาก service
watch(
  () => facets.minYear,
  (newMinYear) => {
    state.yearStart = newMinYear;
  }
);

// 2. เฝ้าดูค่า maxYear จาก service
watch(
  () => facets.maxYear,
  (newMaxYear) => {
    state.yearEnd = newMaxYear;
  }
);

let results = reactive([]);

/* ====== THEME-AWARE COLORS (อ่านจาก CSS variables) ====== */
const TEXT = ref("#e8eaed");
const GRID = ref("rgba(255,255,255,0.08)");
const cssVar = (name, fallback) =>
  getComputedStyle(document.documentElement).getPropertyValue(name)?.trim() ||
  fallback;

function updateColors() {
  // ถ้า theme เปลี่ยนจะอัปเดตอัตโนมัติ
  TEXT.value = cssVar("--text", TEXT.value);
  // เดา grid จากธีมคร่าว ๆ
  const isLight =
    document.documentElement.getAttribute("data-theme") === "light";
  GRID.value = isLight ? "rgba(0,0,0,0.06)" : "rgba(255,255,255,0.08)";
}
onMounted(() => {
  updateColors();
  new MutationObserver(updateColors).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
});

/* ====== YEAR GUARDS ====== */
const blockMinus = (e) => {
  if (e.key === "-") e.preventDefault();
};
const clampStart = () => {
  if (state.yearStart == null || isNaN(state.yearStart))
    state.yearStart = MIN_YEAR.value;
  state.yearStart = Math.max(
    MIN_YEAR.value,
    Math.min(MAX_YEAR.value, state.yearStart)
  );
  if (state.yearEnd != null && state.yearStart > state.yearEnd)
    state.yearEnd = state.yearStart;
};
const clampEnd = () => {
  if (state.yearEnd == null || isNaN(state.yearEnd))
    state.yearEnd = MAX_YEAR.value;
  state.yearEnd = Math.max(
    MIN_YEAR.value,
    Math.min(MAX_YEAR.value, state.yearEnd)
  );
  if (state.yearStart != null && state.yearEnd < state.yearStart)
    state.yearStart = state.yearEnd;
};

/* ---- helpers ---- */
function applyFilters(rows) {
  const q = state.query.trim().toLowerCase();
  const y1 = Number(state.yearStart) || MIN_YEAR.value;
  const y2 = Number(state.yearEnd) || MAX_YEAR.value;
  return rows.filter((r) => {
    if (
      q &&
      !(
        r.title.toLowerCase().includes(q) ||
        (r.abstract || "").toLowerCase().includes(q)
      )
    )
      return false;
    if (Number(r.year) < y1 || Number(r.year) > y2) return false;
    if (state.category && r.category !== state.category) return false;
    if (state.type && r.type !== state.type) return false;
    if (state.degree && r.degree !== state.degree) return false;
    if (state.advisor && r.advisor !== state.advisor) return false;
    return true;
  });
}

async function load() {
  const { items } = await searchPublications({});
  results.splice(0, results.length, ...applyFilters(items));
}
watch(
  state,
  () => {
    load();
  },
  { deep: true }
);

function reset() {
  Object.assign(state, {
    query: "",
    advisor: "",
    category: "",
    type: "",
    degree: "",
    yearStart: MIN_YEAR.value,
    yearEnd: MAX_YEAR.value,
  });
  load();
}

/* ---- KPIs ---- */
const latestYear = computed(() =>
  results.reduce((m, r) => Math.max(m, Number(r.year) || 0), 0)
);

const categoryInsights = computed(() => {
  const categoryCounts = {};
  const degreeCounts = {};

  results.forEach((r) => {
    const categoryKey = (r.category && r.category.trim()) || "Uncategorized";
    categoryCounts[categoryKey] = (categoryCounts[categoryKey] || 0) + 1;

    const degreeKey = (r.degree && r.degree.trim()) || "Unspecified";
    degreeCounts[degreeKey] = (degreeCounts[degreeKey] || 0) + 1;
  });

  const sortEntries = (entries) =>
    entries.sort((a, b) => {
      if (b[1] === a[1]) return a[0].localeCompare(b[0]);
      return b[1] - a[1];
    });

  const categoryEntries = sortEntries(Object.entries(categoryCounts));
  const degreeEntries = sortEntries(Object.entries(degreeCounts));
  const topDegreeName = degreeEntries[0]?.[0];

  return {
    totalCategories: categoryEntries.length,
    topCategory: categoryEntries[0]?.[0] || "",
    topCategoryCount: categoryEntries[0]?.[1] || 0,
    topDegree:
      topDegreeName && topDegreeName !== "Unspecified" ? topDegreeName : "",
    topDegreeCount: degreeEntries[0]?.[1] || 0,
  };
});

/* ---- Charts ---- */
const typeColors = [
  "#42A5F5",
  "#66BB6A",
  "#FFA726",
  "#AB47BC",
  "#EC407A",
  "#26C6DA",
];

const lineBarOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: TEXT.value } },
    datalabels: { display: false },
  },
  scales: {
    x: { ticks: { color: TEXT.value }, grid: { color: GRID.value } },
    y: { ticks: { color: TEXT.value }, grid: { color: GRID.value } },
  },
}));

/* ✅ ย่อ “วงกลม” เล็กลง และทำสี legend ให้คอนทราสต์ตามธีม */
const pieOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { top: 8, right: 8, bottom: 8, left: 8 } },
  plugins: {
    legend: {
      position: "right",
      labels: { boxWidth: 14, boxHeight: 14, padding: 10, color: TEXT.value },
    },
    datalabels: {
      clamp: true,
      clip: false,
      color: "#fff",
      font: { weight: "bold", size: 11 },
      formatter: (value, ctx) => {
        const ds = ctx.chart.data.datasets[0];
        const total = ds.data.reduce((a, b) => a + b, 0) || 1;
        const pct = (value / total) * 100;
        return pct >= 5 ? `${pct.toFixed(0)}%` : "";
      },
    },
    tooltip: {
      callbacks: {
        label: (c) => {
          const v = c.parsed;
          const ds = c.chart.data.datasets[0];
          const total = ds.data.reduce((a, b) => a + b, 0) || 1;
          const pct = ((v / total) * 100).toFixed(1);
          return ` ${c.label}: ${v} (${pct}%)`;
        },
      },
    },
  },
  elements: { arc: { borderWidth: 1 } },
}));

/* 1) แนวโน้มรายปี: ตรึงแกน 2021–2025 */
const chartYearData = computed(() => {
  const baseline = [];
  if (MIN_YEAR.value && MAX_YEAR.value) {
    for (let y = MIN_YEAR.value; y <= MAX_YEAR.value; y++) {
      baseline.push(String(y));
    }
  }

  const countByYear = Object.fromEntries(baseline.map((y) => [y, 0]));
  results.forEach((r) => {
    const y = String(r.year);
    if (countByYear[y] != null) countByYear[y]++;
  });
  return {
    labels: baseline,
    datasets: [
      {
        label: "จำนวนผลงาน",
        data: baseline.map((y) => countByYear[y]),
        borderColor: "#8ab4f8",
        backgroundColor: "#8ab4f880",
        fill: true,
        tension: 0.25,
      },
    ],
  };
});

/* 2) สัดส่วนประเภทผลงาน (radius 82% เพื่อย่อวงกลม) */
const chartTypeData = computed(() => {
  const colorMap = new Map();
  let hueCounter = 15; // ค่าสีเริ่มต้น (Hue) สำหรับการสร้างสีใหม่

  (facets.types || []).forEach((type, index) => {
    if (index < typeColors.length) {
      // ใช้ 6 สีหลักจนกว่าจะหมด
      colorMap.set(type, typeColors[index]);
    } else {
      // ถ้าสีหลักหมด ให้สร้างสี HSL ใหม่
      // ใช้ S=80%, L=65% (สด, สว่าง)
      const newColor = `hsl(${hueCounter}, 80%, 65%)`;
      colorMap.set(type, newColor);

      // หมุน Hue ไป 41 องศา (เป็น prime-like number)
      // เพื่อให้สีที่ได้รอบต่อไปไม่ใกล้กับสีเดิม
      hueCounter = (hueCounter + 41) % 360;
    }
  });

  // 2. นับเฉพาะที่กรองแล้ว
  const counts = {};
  results.forEach((r) => {
    const type = r.type || "Unknown"; // จัดการกับ type ที่ไม่มีชื่อ
    counts[type] = (counts[type] || 0) + 1;
  });

  const labels = [];
  const data = [];
  const backgroundColors = [];

  for (const [label, count] of Object.entries(counts)) {
    if (count > 0) {
      // เอาเฉพาะที่มีข้อมูล
      labels.push(label);
      data.push(count);

      //ดึงสีที่ถูกต้องจาก "แผนที่สี"
      let color = colorMap.get(label);
      if (!color) {
        color = `hsl(${hueCounter}, 70%, 55%)`;
        hueCounter = (hueCounter + 41) % 360;
        colorMap.set(label, color);
      }
      backgroundColors.push(color);
    }
  }

  return {
    labels,
    datasets: [
      {
        data,
        radius: "82%",
        backgroundColor: backgroundColors,
      },
    ],
  };
});

/* 3) อาจารย์ที่ปรึกษายอดนิยม */
const chartGroupsData = computed(() => {

  // นับจำนวนผลงานของอาจารย์แต่ละคนจาก 'results'
  const counts = {};
  results.forEach(r => {
    const advisor = r.advisor || 'Unknown'; 
    counts[advisor] = (counts[advisor] || 0) + 1;
  });

  // 2. แปลงเป็น Array, เรียงลำดับ, และเอา Top 4
  const sortedAdvisors = Object.entries(counts)
    .sort((a, b) => b[1] - a[1]) // เรียงจากมากไปน้อย
    .slice(0, TOP_N_ADVISORS);

  // เตรียมข้อมูลให้ Chart.js
  const labels = sortedAdvisors.map(entry => entry[0]); 
  const data = sortedAdvisors.map(entry => entry[1]);  

  return {
    labels: labels,
    datasets: [{
      label: 'จำนวนผลงาน',
      data: data,
      backgroundColor: '#8ab4f8'
    }]
  }
});

/* ---- export ---- */
function exportCSV() {
  if (!results.length) return;
  const cols = CSV_EXPORT_COLUMNS;
  const head = cols.join(",");
  const esc = (s) => String(s ?? "").replace(/"/g, '""');
  const lines = results
    .map((r) => cols.map((c) => `"${esc(r[c])}"`).join(","))
    .join("\n");
  const csv = head + "\n" + lines;
  const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "dashboard-alt.csv";
  a.click();
  URL.revokeObjectURL(a.href);
}

function printDashboard() {
  window.print();
}

/* เริ่มต้นด้วยการ clamp และโหลดข้อมูล */
clampStart();
clampEnd();
onMounted(load);
</script>
