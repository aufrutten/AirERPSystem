<script setup lang="ts">
import Links from "@/components/header/Links.vue";
import AccountDropMenu from "@/components/header/AccountDropMenu.vue";
import {onMounted} from "vue";

onMounted(()=>{
  let title_header = document.getElementById("title-header")
  if (title_header){
    title_header.innerHTML = import.meta.env.VITE_PROJECT_NAME
  }
})
</script>

<template>
  <header data-bs-theme="dark">
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <div class="container-fluid">
        <router-link id="title-header" class="navbar-brand" :to="{name: 'home'}"></router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"  data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <Links/>
          <AccountDropMenu/>
        </div>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.navbar-brand{
  font-weight: bold;
}
</style>
