<script setup lang="ts">
import RegisterForm from "@/components/forms/RegisterForm.vue";
</script>

<template>
  <div class="col-md-10 mx-auto col-lg-5">
    <div class="modal-content rounded-4 shadow mt-lg-5">
      <div class="modal-header p-5 pb-4 border-bottom-0">
        <h1 class="fw-bold mb-0 fs-2">Sign up</h1>
        <router-link :to="{name: 'login'}"><button type="reset" class="btn-close"></button></router-link>
      </div>

      <div class="modal-body p-5 pt-0">
        <RegisterForm/>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>

