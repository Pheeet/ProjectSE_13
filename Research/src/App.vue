<template>
<div class="app-shell">
<header class="app-header">
<h1>CS Research Search</h1>
<nav>
<RouterLink to="/research/horizontal">Horizontal</RouterLink>
<span> · </span>
<RouterLink to="/research/vertical">Vertical</RouterLink>
</nav>
</header>


<main class="app-main">
<RouterView />
</main>
</div>
</template>


<script setup>
// no-op
</script>


<style>
.app-shell { min-height: 100vh; display: flex; flex-direction: column; }
.app-header { padding: 12px 16px; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; gap: 12px; }
.app-header h1 { font-size: 16px; margin: 0; }
.app-header nav a { text-decoration: none; }
.app-main { padding: 16px; width: 100%; max-width: 1100px; margin: 0 auto; }
</style>