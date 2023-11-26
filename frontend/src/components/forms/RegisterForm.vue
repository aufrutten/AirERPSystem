<script setup lang="ts">
import { ref } from "vue";
import { accountData } from "@/stores/account";
import type { AxiosError } from "axios";

const account = accountData()
const errors: any = ref({})
const payload = ref({
  photo: null,
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  birthday: null,
  sex: ''
})

function submit() {
  window.api.post('/accounts/register', payload.value)
      .then(() => {
        account.router.replace({name: 'login'})
      })
      .catch((error: AxiosError) => {
        errors.value = error.response?.data
      });
}
</script>

<template>

<form @submit.prevent="submit" class="row g-2 needs-validation" autocomplete="on" novalidate>
  <div class="col-md-6">
    <label for="inputEmail" class="form-label">Email</label>
    <input autocomplete="email" id="inputEmail" type="email" class="form-control" :class="{'is-invalid': errors?.email, 'is-valid': !errors?.email && payload.email}" v-model="payload.email">
    <div v-if="errors?.email" class="invalid-feedback">
      <strong>{{ errors?.email[0] }}</strong>
    </div>
  </div>

  <div class="col-md-6">
    <label for="inputPassword" class="form-label">Password</label>
    <input autocomplete="new-password" name="password" id="inputPassword" type="password" class="form-control" :class="{'is-invalid': errors?.password, 'is-valid': !errors?.password && payload.password}" v-model="payload.password">
    <div v-if="errors?.password" class="invalid-feedback">
      <strong>{{ errors?.password[0] }}</strong>
    </div>
  </div>

  <div class="col-12">
    <label for="inputName" class="form-label">Name</label>
    <input autocomplete="given-name" id="inputName" placeholder="John" type="text" class="form-control" :class="{'is-invalid': errors.first_name, 'is-valid': !errors.first_name && payload.first_name}" v-model="payload.first_name">
    <div v-if="errors?.first_name" class="invalid-feedback">
      <strong>{{ errors?.first_name[0] }}</strong>
    </div>
  </div>
  <div class="col-12">
    <label for="inputSurname" class="form-label">Surname</label>
    <input autocomplete="family-name" id="inputSurname" placeholder="Smith" type="text" class="form-control" :class="{'is-invalid': errors?.last_name, 'is-valid': !errors?.last_name && payload.last_name}" v-model="payload.last_name">
    <div v-if="errors?.last_name" class="invalid-feedback">
      <strong>{{ errors?.last_name[0] }}</strong>
    </div>
  </div>

  <div class="col-md-6">
    <label for="inputBirthday" class="form-label">Birthday</label>
    <input id="inputBirthday" type="date" class="form-control" :class="{'is-invalid': errors?.birthday, 'is-valid': !errors?.birthday && payload.birthday}" v-model="payload.birthday">
    <div v-if="errors?.birthday" class="invalid-feedback">
      <strong>{{ errors?.birthday[0] }}</strong>
    </div>
  </div>

  <div class="col-md-6">
    <label for="inputSex" class="form-label">Sex</label>
    <select autocomplete="sex" id="inputSex" class="form-select" :class="{'is-invalid': errors?.sex, 'is-valid': !errors?.sex && payload.sex}" v-model="payload.sex">
      <option>Male</option>
      <option>Female</option>
    </select>
    <div v-if="errors?.sex" class="invalid-feedback">
      <strong>{{ errors?.sex[0] }}</strong>
    </div>
  </div>

  <input type="submit" value="Sing up" class="btn btn-primary w-100 mt-4 btn btn-lg rounded-3 btn-primary">
  <router-link :to="{name: 'forgot-password'}" class="btn btn-outline-secondary w-100 btn btn-lg rounded-3">Forgot password</router-link>
  <small class="text-muted">By clicking Sign up, you agree to the terms of use.</small>
</form>
</template>

<style scoped>
</style>