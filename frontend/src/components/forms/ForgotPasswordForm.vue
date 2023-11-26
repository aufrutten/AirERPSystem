<script setup lang="ts">
import { ref } from "vue";
import { accountData } from "@/stores/account";
import type { AxiosError } from "axios";

const account = accountData()
const errors: any = ref({})
const payload = ref({
  email: ''
})

function submit() {
  console.log(payload.value)
  if (payload.value.email !== ''){
    window.api.post(`/accounts/reset-password`, payload.value)
        .then(() => {
          account.router.replace({name: 'home'})
        })
        .catch((error: AxiosError) => {
          console.log(error)
          errors.value = error.response?.data
        });
  }
}
</script>

<template>
<form @submit.prevent="submit" class="row g-3 mt-3 needs-validation" autocomplete="on" novalidate>
  <div class="input-group mb-3 md">
    <input type="text" class="form-control" :class="{'is-invalid': errors?.email, 'is-valid': !errors?.email && payload.email}" v-model="payload.email" placeholder="Recipient email address" aria-label="Recipient email address" aria-describedby="button-addon2">
    <button class="btn btn-primary" type="submit" id="button-addon2">Forgot password</button>
    <div v-if="errors?.email" class="invalid-feedback">
      <strong>{{ errors?.email[0] }}</strong>
    </div>
  </div>
</form>
</template>

<style scoped>
</style>