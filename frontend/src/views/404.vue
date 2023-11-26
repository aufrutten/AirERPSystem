<template>
  <div>
    <h1>404 - Page Not Found</h1>
    <p>The requested page could not be found.</p>
    <router-link :to="{name: 'home'}" class="btn btn-outline-secondary" aria-current="page">Back to home</router-link>
  </div>
</template>

<style scoped>
  div {
    margin-top: 19%;
    margin-left: 40%;
    margin-right: 40%;
  }
</style>
<script setup lang="ts">
</script>