<script setup lang="ts">
import {onMounted, ref } from "vue";

import ForgotPasswordForm from "@/components/forms/ForgotPasswordForm.vue";
import NewPasswordForm from "@/components/forms/NewPasswordForm.vue";

const uid = ref('')
const token = ref('')

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  uid.value = urlParams.get('uid') || '';
  token.value = urlParams.get('token') || '';
})

</script>

<template>
  <div class="col-md-10 mx-auto col-lg-5">
    <div class="modal-content rounded-4 shadow mt-lg-5">
      <div class="modal-header p-5 pb-4 border-bottom-0">
        <h1 class="fw-bold mb-0 fs-2">Forgot password</h1>
        <router-link :to="{name: 'login'}" class="btn-close"></router-link>
      </div>
      <div class="modal-body p-5 pt-0">
        <ForgotPasswordForm v-if="!token" />
        <NewPasswordForm v-else :uid="uid" :token="token"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>