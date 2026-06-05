<script setup>
import { useAuthStore } from '~/stores/auth';
const useAuth = useAuthStore()
const route = useRoute()

</script>
<template>
  <aside class=" min-w-48 bg-c-tertiary border! border-r-neutral-500 h-screen pt-14"">
    <div class=" p-4 flex flex-col gap-4">
    <div class="w-fit mx-auto text-center">
      <p class="text-3xl text-c-primary">Staff Panel</p>
      <p class="-mt-1 text-sm">Klinik Makmur Jaya</p>
    </div>
    <v-divider :thickness="2"></v-divider>
    <div v-if="useAuth.role?.toLowerCase() === 'pharmacist' || useAuth.role?.toLowerCase() === 'admin'" class="flex gap-2 flex-col">
      <nuxt-link :to="`/pharmacist/manage`" class="p-2 w-full rounded-lg items-center flex gap-3"
        :class="route.path.includes('manage') ? 'bg-c-secondary' : ' hover:border hover:border-b-c-primary'"><v-icon>mdi mdi-package</v-icon>Inventory</nuxt-link>
      <nuxt-link :to="`/pharmacist/order`" class="p-2 w-full rounded-lg items-center flex gap-3"
        :class="route.path.includes('order') ? 'bg-c-secondary' : 'hover:bg-c-secondary'"><v-icon>mdi mdi-receipt-text</v-icon>Order</nuxt-link>
    </div>
    <div v-if="useAuth.role?.toLowerCase() === 'cashier' || useAuth.role?.toLowerCase() === 'admin'" class="flex gap-2 flex-col">
      <nuxt-link :to="`/cashier/scan`" class="p-2 w-full rounded-lg items-center flex gap-3"
        :class="route.path.includes('scan') ? 'bg-c-secondary' : ' hover:border hover:border-b-c-primary'"><v-icon>mdi mdi-qrcode-scan</v-icon>Scan Order</nuxt-link>
    </div>
    </div>
  </aside>
</template>