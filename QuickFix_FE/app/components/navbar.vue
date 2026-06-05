<script setup>
import { useAuthStore } from '~/stores/auth';
const useAuth = useAuthStore()
const route = useRoute()

const handleLogout = async () => {
  useAuth.logout()
  await navigateTo('/login', { replace: true })
}
const dashboardRoute = computed(() => {
  switch (useAuth.role?.toLowerCase()) {
    case 'admin':
      return '/admin'
    case 'cashier':
      return '/cashier/scan'
    case 'pharmacist':
      return '/pharmacist/manage'
    default:
      return '/shop'
  }
})
</script>

<template>
<header>
    <nav
      class="fixed top-0 left-0 right-0 w-full z-50 flex items-center justify-between px-6 py-2 border! border-b-neutral-500 bg-c-tertiary! text-primary">
      <div class="flex align-middle items-center gap-20">
        <div>
          <nuxt-link :to="dashboardRoute" class="flex items-center gap-2 text-foreground-light no-underline bg-c-primary p-1 rounded">
            <v-img src="/logo.png" alt="SmartStock Pro" width="133px" />
          </nuxt-link>
        </div>
        <div class="flex items-center gap-5">
          <nuxt-link v-if="useAuth.role?.toLowerCase() === 'customer' || !useAuth.role" :to="`/shop`" class="p-1"
            :class="route.path.includes('shop') ? ' text-c-primary border-b border-b-c-primary! font-bold!' : ' hover:border-b hover:border-b-c-primary'">Shop</nuxt-link>
          
          <div v-if="useAuth.role?.toLowerCase() === 'customer'" class="flex gap-2">
            <nuxt-link :to="`/customer/order`" class="p-1"
              :class="route.path.includes('order') ? ' text-c-primary border-b border-b-c-primary! font-bold!' : ' hover:border-b hover:border-b-c-primary'">Order</nuxt-link>
          </div>
        </div>
      </div>

      <div v-if="!useAuth.role" class="flex gap-3">
        <nuxt-link to="/login" class="no-underline font-medium hover:text-slate-700 text-c-primary">Login</nuxt-link>
        <nuxt-link to="/signup" class="no-underline font-medium hover:text-slate-700 text-c-primary">Signup</nuxt-link>
      </div>

      <div v-if="useAuth.role" class="flex items-center gap-1">
        <nuxt-link to="/customer/cart" class="mr-10"><v-icon>mdi mdi-cart-outline</v-icon></nuxt-link>
        <div class="flex items-center gap-1 text-lg my-auto font-medium text-slate-700">
          <p class="mb-0 mr-1">{{ useAuth.username }}</p>
          <v-icon color="primary">mdi-account-circle</v-icon>
        </div>

        <v-tooltip text="Logout" location="bottom">
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" variant="text" icon="mdi-logout" color="primary" density="comfortable"
              @click.prevent="handleLogout()" />
          </template>
        </v-tooltip>
      </div>
    </nav>
  </header>
</template>