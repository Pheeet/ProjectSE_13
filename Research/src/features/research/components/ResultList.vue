<template>
<section class="result-list">
<ResultCard v-for="r in results" :key="r.id" :item="r" />
<p v-if="!results.length" class="muted">ไม่พบผลลัพธ์</p>
</section>
</template>


<script setup>
import ResultCard from './ResultCard.vue'
const props = defineProps({ results: { type: Array, default: () => [] } })
</script>