<script setup lang="ts">
import { ref } from "vue";
import { accountData } from "@/stores/account";
import type { AxiosResponse, AxiosError } from "axios";


const account = accountData()
const errors: any = ref({})

function submit() {
  const form = document.getElementById('loginForm')
  const payHoly = new FormData(form)
  window.api.post('accounts/auth', payHoly)
      .then((response: AxiosResponse) => response.data)
      .then(data => {
        account.connect_account(data['email'], data['access_token'], data['refresh_token'])
        account.router.replace({name: 'home'})
      })
      .catch((error: AxiosError) => {
        console.log(error.response)
        errors.value = error?.response?.data
      })
}
</script>

<template>
  <form @submit.prevent="submit" class="needs-validation" novalidate autocomplete="on" id="loginForm">
    <div class="form-floating mb-3">
      <input name="email" :class="{'is-invalid': errors?.email, 'is-valid': !errors?.email}" class="form-control" placeholder="email" id="email" type="email">
      <label for="email">Email address</label>
      <span v-if="errors?.email" class="invalid-feedback">
        <strong>{{errors?.email[0]}}</strong>
      </span>
    </div>

    <div class="form-floating mb-3">
      <input name= "password" :class="{'is-invalid': errors?.password, 'is-valid': !errors?.password}" type="password" class="form-control" placeholder="password" id="password">
      <label for="password">Password</label>
      <span v-if="errors?.password" class="invalid-feedback">
        <strong>{{errors?.password[0]}}</strong>
      </span>
    </div>

    <div class="checkbox mb-3 form-check">
      <input name="remember_me" type="checkbox" class="form-check-input" id="remember_me">
      <label for="remember_me" class="form-check-label">Remember me</label>
      <router-link class="icon-link icon-link-hover float-end" :to="{name: 'forgot-password'}">Forgot password</router-link>
    </div>

    <input type="submit" value="Sign in" class="btn btn-primary w-100 mb-2 btn btn-lg rounded-3 btn-primary">
  </form>
</template>

<style scoped>
</style>