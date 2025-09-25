<template>
  <section class="container">
    <div class="layout">
      <!-- SIDEBAR FILTERS -->
      <aside class="panel sidebar">
        <div class="small">ค้นหา</div>
        <input v-model="state.query" placeholder="ค้นหาคำหลัก (ไทย/อังกฤษ)" />
        <div class="small">ปี</div>
        <div class="toolbar">
          <input v-model.number="state.yearStart" type="number" placeholder="ตั้งแต่"/>
          <input v-model.number="state.yearEnd" type="number" placeholder="ถึง"/>
        </div>
        <div class="small">Category</div>
        <select v-model="state.category">
          <option value="">ทุก Category</option>
          <option v-for="c in facets.categories" :key="c" :value="c">{{ c }}</option>
        </select>
        <div class="small">Type</div>
        <select v-model="state.type">
          <option value="">ทุก Type</option>
          <option v-for="t in facets.types" :key="t" :value="t">{{ t }}</option>
        </select>
        <div class="small">Degree</div>
        <select v-model="state.degree">
          <option value="">ทุก Degree</option>
          <option v-for="d in facets.degrees" :key="d" :value="d">{{ d }}</option>
        </select>
        <div class="small">Advisor</div>
        <select v-model="state.advisor">
          <option value="">ทุกอาจารย์</option>
          <option v-for="a in facets.advisors" :key="a" :value="a">{{ a }}</option>
        </select>
        <div class="toolbar" style="margin-top:6px">
          <button class="ghost btn" @click="reset">ล้างตัวกรอง</button>
          <button class="primary btn" :disabled="loading" @click="runSearch">{{ loading? 'กำลังค้นหา…' : 'ค้นหา' }}</button>
        </div>
      </aside>

      <!-- RESULTS + PREVIEW -->
      <section>
        <div class="results">
          <div class="card">
            <div class="small">ผลการค้นหา</div>
            <div class="result-list">
              <div v-if="!results.length" class="result-item small">— ไม่พบผลลัพธ์ตามตัวกรอง</div>
              <div v-for="r in results" :key="r.id" class="result-item" :class="{active: selected && selected.id===r.id}" @click="selected=r">
                <div><strong>{{ r.title }}</strong></div>
                <div class="small">{{ r.year }} • {{ r.type }} • {{ r.degree }} • {{ r.category }} • {{ r.advisor }}</div>
              </div>
            </div>
          </div>
          <div class="card preview">
            <div class="small">ตัวอย่าง/รายละเอียด</div>
            <div v-if="!selected" class="skeleton" style="height:480px;margin-top:8px"></div>
            <div v-else style="margin-top:8px">
              <div><strong>{{ selected.title }}</strong></div>
              <div class="small">{{ selected.category }} • {{ selected.type }} • {{ selected.degree }} • {{ selected.year }}</div>
              <div style="margin-top:8px">ที่ปรึกษา: {{ selected.advisor }}</div>
              <p style="margin-top:8px">{{ selected.abstract }}</p>
              <div class="chips" style="margin-top:8px">
                <span class="badge">{{ selected.category }}</span>
                <span class="badge">{{ selected.type }}</span>
                <span class="badge">{{ selected.degree }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="panel" style="margin-top:14px">
          <div class="small">ผลลัพธ์แบบตาราง</div>
          <table class="table">
            <thead><tr>
              <th style="width:34%">ชื่อเรื่อง</th><th>ปี</th><th>Category</th><th>Type</th><th>Degree</th><th>Advisor</th>
            </tr></thead>
            <tbody>
              <tr v-if="!results.length"><td colspan="6" class="small" style="color:#8b9099">— ไม่มีข้อมูล</td></tr>
              <tr v-for="r in results" :key="'t-'+r.id">
                <td>{{ r.title }}</td>
                <td>{{ r.year }}</td>
                <td>{{ r.category }}</td>
                <td><span class="badge">{{ r.type }}</span></td>
                <td>{{ r.degree }}</td>
                <td>{{ r.advisor }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="footer">Vertical ALT</div>
      </section>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { getFacets, searchPublications } from '@/services/search.service' 

const facets = getFacets()
let state = reactive({ query:'', advisor:'', category:'', type:'', degree:'', yearStart:'', yearEnd:'' })
let results = ref([])
let loading = ref(false)
let selected = ref(null)

function applyFilters(rows){
  const q = state.query.trim().toLowerCase()
  const y1 = Number(state.yearStart)||0
  const y2 = Number(state.yearEnd)||9999
  return rows.filter(r=>{
    if(q && !(r.title.toLowerCase().includes(q) || (r.abstract||'').toLowerCase().includes(q))) return false
    if(Number(r.year) < y1 || Number(r.year) > y2) return false
    if(state.category && r.category !== state.category) return false
    if(state.type && r.type !== state.type) return false
    if(state.degree && r.degree !== state.degree) return false
    if(state.advisor && r.advisor !== state.advisor) return false
    return true
  })
}

async function runSearch(){
  loading.value = true
  try{
    const { items } = await searchPublications(state)
    results.value = applyFilters(items)
    selected.value = results.value[0] || null
  } finally { loading.value = false }
}

function reset(){
  Object.assign(state,{ query:'', advisor:'', category:'', type:'', degree:'', yearStart:'', yearEnd:'' })
  results.value=[]; selected.value=null
}

onMounted(runSearch)
</script>
