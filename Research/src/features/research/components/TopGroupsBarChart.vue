<template>
  <div class="panel chart">
    <div class="small">Top Research Groups (mock)</div>
    <BarChart :chart-data="data" :chart-options="options" />
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const data = {
  labels: ['NLP Lab','Vision Lab','IoT Lab','Security Lab'],
  datasets: [
    {
      label: 'จำนวนผลงาน',
      data: [14, 10, 7, 5],
      backgroundColor: '#8ab4f8'
    }
  ]
}
const options = { responsive: true, plugins: { legend: { labels:{ color:'#e8eaed'} } }, scales:{ x:{ticks:{color:'#e8eaed'}}, y:{ticks:{color:'#e8eaed'}} } }

const BarChart = Bar
</script>
