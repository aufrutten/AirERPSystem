<script setup lang="ts">
import { useRouter } from "vue-router";
import type { AxiosError, AxiosResponse } from "axios";


const google_oauth_callback = useRouter().resolve({ name: 'google-oauth2-callback' }).href;
const google_redirect_uri = `https://${window.location.host}${google_oauth_callback}`
const google_auth_uri = "https://accounts.google.com/o/oauth2/auth"

const getTheme = () => {
  const theme = localStorage.getItem('theme')
  if (theme == null){
    localStorage.setItem('theme', 'auto')
  }
  if (theme === 'auto'){
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  return theme
}
const isDark: boolean = getTheme() === 'dark'

function signInWithGoogle() {
  // Redirect the user to the Google OAuth2 authorization URL
  window.api.get("/accounts/auth/google-oauth2")
      .then((response: AxiosResponse) => {
        const client_id = response.data['client_id']
        window.location.href = `${google_auth_uri}?client_id=${client_id}&access_type=online&redirect_uri=${google_redirect_uri}&response_type=token&scope=openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read`;
      })
      .catch((error: AxiosError) => {
        console.error(error)
      })
}
</script>

<template>
  <router-link class="w-100 btn btn-lg btn-outline-secondary" :to="{name: 'register'}">Sign up</router-link>

  <small class="text-muted">By clicking Sign in, you agree to the terms of use.</small>
  <hr class="my-4">
  <h2 class="fs-5 fw-bold mb-3">Or use a third-party</h2>

  <button @click="signInWithGoogle" class="w-100 py-2 mb-2 btn rounded-3" :class="{'btn-outline-dark': !isDark, 'btn-outline-light': isDark}" type="button" style="font-weight: bold">
    <i class="bi bi-google" style="font-size: 20px"></i> Sign up with Google
  </button>
  <button class="w-100 py-2 mb-2 btn btn-outline-primary rounded-3" type="button" style="font-weight: bold">
    <i class="bi bi-facebook" style="font-size: 20px"></i> Sign up with Facebook
  </button>
  <button class="w-100 py-2 mb-2 btn btn-dark rounded-3" type="button" href="#" style="font-weight: bold">
    <i class="bi bi-apple" style="font-size: 20px"></i> Sign up with AppleID
  </button>
</template>

<style>
</style>
