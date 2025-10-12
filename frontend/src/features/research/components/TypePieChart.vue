<template>
  <div class="panel chart">
    <div class="small">สัดส่วนประเภทผลงาน (mock)</div>
    <PieChart :chart-data="data" :chart-options="options" />
  </div>
</template>

<script setup>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const data = {
  labels: ['204499','Co-operative','Other Type'],
  datasets: [
    {
      data: [12, 5, 8], // mock data
      backgroundColor: ['#8ab4f8','#b388ff','#f28b82']
    }
  ]
}
const options = { responsive: true, plugins: { legend: { labels:{ color:'#e8eaed'} } } }

const PieChart = Pie
</script>
