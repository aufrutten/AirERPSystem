<template>
  <ul class="navbar-nav me-auto mb-2 mb-md-0">
    <li class="nav-item">
      <router-link :to="{name: 'home'}" class="nav-link active" aria-current="page">Home</router-link>
    </li>
    <li class="nav-item">
      <router-link to="#" class="nav-link">Search</router-link>
    </li>
    <li class="nav-item">
      <router-link to="#" class="nav-link disabled" aria-disabled="true">Hotel</router-link>
    </li>
  </ul>
</template>