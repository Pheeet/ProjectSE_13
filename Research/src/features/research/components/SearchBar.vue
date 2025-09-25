<template>
<div class="card research-wrap">
<div class="search-row">
<input
class="input"
type="search"
:value="modelValue.query"
placeholder="ค้นหาคำสำคัญ เช่น AI, NLP, Computer Vision"
@input="$emit('update:modelValue', { ...modelValue, query: $event.target.value })"
/>
<button class="btn" @click="$emit('search')">ค้นหา</button>
</div>


<div class="filters-row">
<select class="select" :value="modelValue.advisor" @change="$emit('update:modelValue', { ...modelValue, advisor: $event.target.value })">
<option value="">อาจารย์ที่ปรึกษา — ทั้งหมด</option>
<option v-for="a in advisors" :key="a" :value="a">{{ a }}</option>
</select>


<select class="select" :value="modelValue.category" @change="$emit('update:modelValue', { ...modelValue, category: $event.target.value })">
<option value="">หมวดหมู่ — ทั้งหมด</option>
<option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
</select>


<select class="select" :value="modelValue.year" @change="$emit('update:modelValue', { ...modelValue, year: $event.target.value })">
<option value="">ปีการศึกษา — ทั้งหมด</option>
<option v-for="y in years" :key="y" :value="y">{{ y }}</option>
</select>


<select class="select" :value="modelValue.type" @change="$emit('update:modelValue', { ...modelValue, type: $event.target.value })">
<option value="">ชนิดผลงาน — ทั้งหมด</option>
<option value="research">วิจัย</option>
<option value="student">ผลงานนักศึกษา</option>
</select>
</div>


<div class="toolbar">
<button class="btn" @click="$emit('reset')">ล้างตัวกรอง</button>
<span class="muted">ผลลัพธ์: {{ countLabel }}</span>
</div>
</div>
</template>


<script setup>
const props = defineProps({
modelValue: { type: Object, required: true },
advisors: { type: Array, default: () => [] },
categories: { type: Array, default: () => [] },
years: { type: Array, default: () => [] },
resultCount: { type: Number, default: 0 }
})


const emit = defineEmits(['update:modelValue', 'search', 'reset'])


const countLabel = computed(() =>
props.resultCount ? `${props.resultCount} รายการ` : '—'
)
</script>