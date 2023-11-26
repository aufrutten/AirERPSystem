
<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from "@/components/header/Header.vue";
import ThemeButton from "@/components/ThemeButton.vue";
</script>

<template>
  <ThemeButton />
  <Header />
  <RouterView />
</template>
