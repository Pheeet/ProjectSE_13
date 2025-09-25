<template>
<article class="card">
<header style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
<h3 style="margin:0; font-size:16px;">{{ item.title }}</h3>
<span class="badge">{{ item.year }}</span>
</header>
<p class="muted" style="margin:6px 0 10px;">{{ item.authors.join(', ') }}</p>
<p style="margin:0 0 8px;">{{ item.abstract }}</p>
<footer class="toolbar">
<span class="badge">{{ item.category }}</span>
<span class="badge">{{ item.type === 'research' ? 'วิจัย' : 'ผลงานนักศึกษา' }}</span>
</footer>
</article>
</template>


<script setup>
const props = defineProps({ item: { type: Object, required: true } })
</script>