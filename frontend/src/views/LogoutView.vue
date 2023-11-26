<script setup lang="ts">
import {accountData} from "@/stores/account";
const account = accountData()
account.disconnect_account()
</script>

<template>
 <h1 class="align-middle d-flex justify-content-center">Logout</h1>
</template>

<style scoped>
h1 {
  margin-top: 20%;
}
</style>
