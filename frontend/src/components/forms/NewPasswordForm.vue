<script setup lang="ts">
import {ref} from "vue";
import {accountData} from "@/stores/account";
import type {AxiosError} from "axios";


const props = defineProps({
  uid: String,
  token: String
})

const payload = ref({
  uid: props.uid,
  token: props.token,
  password: '',
})

const account = accountData()
const errors: any = ref({})
const confirm_password = ref('')

function submit() {
  console.log(payload.value)
  if (confirm_password.value === payload.value.password && payload.value.password !== '') {
    window.api.put(`/accounts/reset-password`, payload.value)
        .then(() => {
          account.router.replace({name: 'home'})
        })
        .catch((error: AxiosError) => {
          console.log(error)
          errors.value = error.response?.data
        })
  }
}
</script>

<template>
  <form @submit.prevent="submit" class="row g-3 mt-3 needs-validation" autocomplete="on" novalidate>
    <div class="col-md-6">
      <label for="inputPassword" class="form-label">New password</label>
      <input autocomplete="new-password" name="password" id="inputPassword" type="password" class="form-control"
             :class="{'is-invalid': errors?.password, 'is-valid': !errors?.password && payload.password}"
             v-model="payload.password">
      <div v-if="errors?.password" class="invalid-feedback">
        <strong>{{ errors?.password[0] }}</strong>
      </div>
    </div>

    <div class="col-md-6">
      <label for="inputPassword" class="form-label">Confirm password</label>
      <input autocomplete="confirm-password" name="password" id="inputPassword" type="password" class="form-control"
             :class="{'is-invalid': payload.password !== confirm_password, 'is-valid': payload.password === confirm_password && payload.password !== ''}"
             v-model="confirm_password">
      <div class="invalid-feedback">
        <strong>Password mismatch</strong>
      </div>
      <div class="valid-feedback">
        <strong>Correct, the passwords are the same</strong>
      </div>

    </div>

    <input type="submit" value="Change password" class="btn btn-primary w-100 mb-2 btn btn-lg rounded-3 btn-primary">
  </form>
</template>

<style scoped>
</style>