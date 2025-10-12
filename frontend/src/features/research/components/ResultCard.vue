<template>
  <div class="result-card" @click="handleClick">
    <h3>{{ result.title }}</h3>
    <p>{{ result.year }} · {{ result.type }} · {{ result.degree }}</p>
    <p>{{ result.category }} · {{ result.advisor }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  result: Object
})

const handleClick = () => {
  // เวลา click จะไปโชว์รายละเอียด หรือ emit event ออกไป
  console.log("Clicked:", props.result.title)
}
</script>