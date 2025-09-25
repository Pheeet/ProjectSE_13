<template>
  <div class="panel chart">
    <div class="small">แนวโน้มผลงานรายปี (mock)</div>
    <LineChart :chart-data="data" :chart-options="options" />
  </div>
</template>

<script setup>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const data = {
  labels: ['2021','2022','2023','2024','2025'],
  datasets: [
    {
      label: 'จำนวนผลงาน',
      data: [12, 18, 15, 22, 27], // mock data
      borderColor: '#8ab4f8',
      backgroundColor: '#8ab4f880',
      fill: true
    }
  ]
}
const options = { responsive: true, plugins: { legend: { labels:{ color:'#e8eaed'} } }, scales:{ x:{ticks:{color:'#e8eaed'}}, y:{ticks:{color:'#e8eaed'}} } }

const LineChart = Line
</script>
