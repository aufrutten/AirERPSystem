
<script setup lang="ts">
import { accountData } from "@/stores/account";
const account = accountData()
</script>

<template>
  <div class="dropdown" v-if="account.IsAuthenticated">
    <a href="#" class="d-block link-body-emphasis text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
      <img v-if="account.photo_profile" :src="account.photo_profile" alt="mdo" width="32" height="32" class="rounded-circle">
      <i v-else class="bi bi-person-circle" style="font-size: 28px"></i>
    </a>
    <ul class="dropdown-menu text-small dropdown-menu-md-end">
      <router-link to="#" class="dropdown-item">My Bookings</router-link>
      <router-link :to="{name: 'profile'}" class="dropdown-item">Profile</router-link>
      <li><hr class="dropdown-divider"></li>
      <router-link :to="{name: 'logout'}" class="dropdown-item">Sign out</router-link>
    </ul>
  </div>

  <div v-else>
    <router-link :to="{name: 'login'}" class="btn btn-outline-success">Sign In</router-link>
  </div>
</template>
