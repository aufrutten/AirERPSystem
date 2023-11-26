<script setup lang="ts">
import ThirtySignIn from "@/components/ThirtySignIn.vue";
import LoginForm from "@/components/forms/LoginForm.vue";
</script>

<template>
  <div class="col-md-10 mx-auto col-lg-5">
    <div class="modal-content rounded-4 shadow mt-lg-5">
      <div class="modal-header p-5 pb-4 border-bottom-0">
        <h1 class="fw-bold mb-0 fs-2">Sign in</h1>
        <router-link :to="{name: 'home'}" class="btn-close"></router-link>
      </div>

      <div class="modal-body p-5 pt-0">
        <LoginForm/>
        <ThirtySignIn/>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>

