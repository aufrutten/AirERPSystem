import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from "vue-router";
import type { AxiosResponse } from "axios";


export const accountData = defineStore('account', () => {
  const router = useRouter()

  const IsAuthenticated = ref(!!localStorage.getItem('access_token'))
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const photo_profile = ref( localStorage.getItem('photo_profile') || '')

  function connect_account(email: string, access_token: string, refresh_token: string){
    window.api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    window.api.get("/accounts/me").then((response: AxiosResponse) => {
      IsAuthenticated.value = true
      localStorage.clear()
      localStorage.setItem('email', email);
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      if (response.data['photo'] !== null){
        photo_profile.value = response.data['photo']
        localStorage.setItem('photo_profile', response.data['photo'])
      }
    })
  }

  function disconnect_account(){
    localStorage.clear()
    accessToken.value = ''
    photo_profile.value = ''
    IsAuthenticated.value = false

    const logout = () => {
      window.api.defaults.headers.common['Authorization'] = ''
    }

    window.api.delete("/accounts/auth")
      .then(() => {logout()})
      .catch(() => {logout()})
      .finally(() => {
        logout()
        router.push({name: 'home'}).then(()=>{})}
      )
  }

  return { accessToken, IsAuthenticated, photo_profile, router, connect_account, disconnect_account}
})
