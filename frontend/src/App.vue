<template>
  <div>
    <!-- Header -->
    <header class="app-header">
      <div class="app-brand">
        <strong>CS Research Search</strong>
        <span class="app-nav">
          <router-link to="/research/dashboard">Dashboard</router-link>
          <router-link to="/research/search">Research</router-link>
        </span>
      </div>

      <!-- ปุ่มสลับธีม (มุมขวาบน) -->
      <button class="theme-toggle" @click="toggleTheme" aria-label="Toggle theme">
        <span class="only-dark">Light</span>
        <span class="only-light">Dark</span>
      </button>
    </header>

    <!-- Page content -->
    <router-view />
  </div>
</template>

<script setup>
const toggleTheme = () => window.__toggleTheme && window.__toggleTheme()
</script>
