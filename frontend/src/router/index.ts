
import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/account/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/account/login/google-callback',
      name: 'google-oauth2-callback',
      component: () => import('@/views/GoogleLoginView.vue')
    },
    {
      path: '/account/confirm',
      name: 'account-confirm',
      component: () => import('@/views/EmailConfirmView.vue')
    },
    {
      path: '/account/logout',
      name: 'logout',
      component: () => import('@/views/LogoutView.vue')
    },
    {
      path: '/account/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue')
    },
    {
      path: '/account/reset-password',
      name: 'forgot-password',
      component: () => import('@/views/ForgotPasswordView.vue')
    },
    {
      path: '/account/me',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue')
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: () => import('../views/404.vue')
    },
  ]
})

export default router