<script setup>
useHead({
  title: 'Log In to QuickFIx'
})
import { useAuthStore } from '@/stores/auth';
const router = useRouter()
const authStore = useAuthStore()
const unamemail = ref('')
const pass = ref('')
const isLoading = ref(false)
const eye = ref(1)

const handleLogin = async () => {
  remError()
  isLoading.value = true
  const log = await authStore.login(unamemail.value, pass.value)
  isLoading.value = false
  if (log) {
    switch (authStore.role?.toLowerCase()) {
      case 'admin':
        return router.push('/admin')
      case 'cashier':
        return navigateTo(`/cashier/scan`);
      case 'pharmacist':
        return navigateTo(`/pharmacist/manage`);
      default:
        return navigateTo(`/shop`);
    }
  }
}

const remError = () => {
  authStore.error = null
}
</script>

<template>
  <div class="h-full w-full flex flex-col justify-center bg-c-neutral">
    <div class="mx-auto w-1/3 border! border-black justify-center bg-white rounded-lg">
      <div class="flex items-center gap-2 text-foreground-light w-full justify-center p-6">
        <div class="text-center">
          <p class=" text-2xl font-bold text-c-primary">Welcome Back</p>
          <p class=" text-xs">Log in to access your medical dashboard securely.</p>
        </div>
      </div>
      <div class="flex flex-col px-8 py-8">
        <v-form class="ga-8 d-flex flex-col">
          <v-text-field v-model="unamemail" variant="outlined" class="bg-neutral" density="comfortable"
            label="Username or Email" hide-details type="username"></v-text-field>
          <div>
            <div class="flex items-center">
              <v-text-field v-model="pass" variant="outlined" class="bg-neutral" density="comfortable" label="Password"
                hide-details :type="eye ? 'password' : 'text'"></v-text-field>
              <v-btn variant="text" color="primary" :icon="eye ? 'mdi mdi-eye-outline' : 'mdi mdi-eye-off-outline'"
                @click="eye = !eye"></v-btn>
              </div>
              <p v-if="authStore.error" class="text-red">{{ authStore.error }}</p>
          </div>
          <div class="w-full flex flex-col">
            <v-btn color="primary" class="text-white" @click.prevent="handleLogin()" @keydown.enter="handleLogin()"
              type="submit">Login</v-btn>
          </div>
          <div class="flex justify-center gap-1">
            <p class=" font-light">dont have an account?</p>
            <nuxt-link class="text-c-primary hover:text-black cursor-pointer">Sign up</nuxt-link>
            <p class=" font-light">here</p>
          </div>

        </v-form>
        <div>

        </div>
      </div>


    </div>
  </div>
</template>