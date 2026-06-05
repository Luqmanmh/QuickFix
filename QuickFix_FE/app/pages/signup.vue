<script setup>
useHead({
  title: 'Signup to QuickFIx'
})
import { useAuthStore } from '@/stores/auth';
const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const email = ref('')
const pass = ref('')
const repass = ref('')
const isLoading = ref(false)
const eye = ref(1)
const tab = ref('one')
const details = ref({})

const genderSel = [
  { val: "M", label: "Male" },
  { val: "F", label: "Female" }
]

const handleSignup = async () => {
  remError()
  isLoading.value = true
  const log = await authStore.signup(username.value, email.value, pass.value, repass.value, details.value)
  isLoading.value = false
  if (log == "success") {
    await navigateTo({
      path: '/login',
      query: {
        message: 'Please activate your account from the email sent to you'
      }
    })
  }
}

const remError = () => {
  authStore.error = null
}
</script>

<template>
  <div class="h-full w-full flex flex-col justify-center bg-c-neutral">
    <div class="mx-auto w-1/3 border! border-black justify-center bg-white rounded-lg p-3">
      <div class="flex items-center gap-2 text-foreground-light w-full justify-center px-6 py-2">
        <div class="text-center">
          <p class=" text-2xl font-bold text-c-primary">Create Account</p>
        </div>
      </div>
      <v-tabs v-model="tab" color="primary" density="compact" grow disabled>
        <v-tab value="one"></v-tab>
        <v-tab value="two"></v-tab>
      </v-tabs>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="one">
          <div class="flex flex-col px-8 py-8">
            <v-form class="ga-8 d-flex flex-col">
              <v-text-field v-model="username" variant="outlined" class="bg-neutral" density="comfortable"
                label="Username" hide-details type="username"></v-text-field>
              <v-text-field v-model="email" variant="outlined" class="bg-neutral" density="comfortable" label="Email"
                hide-details type="email"></v-text-field>
              <div class="flex items-center">
                <v-text-field v-model="pass" variant="outlined" class="bg-neutral" density="comfortable"
                  label="Password" hide-details :type="eye ? 'password' : 'text'"></v-text-field>
                <v-btn variant="text" color="primary" :icon="eye ? 'mdi mdi-eye-outline' : 'mdi mdi-eye-off-outline'"
                  @click="eye = !eye"></v-btn>
              </div>
              <div class="">
                <div class="flex items-center">
                  <v-text-field v-model="repass" variant="outlined" class="bg-neutral" density="comfortable"
                    label="Re-enter Password" hide-details :type="eye ? 'password' : 'text'"></v-text-field>
                  <v-btn variant="text" color="primary" :icon="eye ? 'mdi mdi-eye-outline' : 'mdi mdi-eye-off-outline'"
                    @click="eye = !eye"></v-btn>
                </div>
                <p v-if="pass != repass" class="text-red text-sm">passwords don't match</p>
              </div>
              <p v-if="authStore.error" class="text-red text-sm -my-2">*{{ authStore.error }}</p>
              <div class="w-full flex flex-col">
                <v-btn color="primary" class="text-white" @click="tab = 'two'">Next <v-icon>mdi
                    mdi-arrow-right</v-icon></v-btn>
              </div>
            </v-form>

          </div>
        </v-tabs-window-item>
        <v-tabs-window-item value='two'>
          <div class="flex flex-col px-8 py-8">
            <v-form class="ga-8 d-flex flex-col">
              <v-text-field v-model="details.fullname" variant="outlined" class="bg-neutral" density="comfortable"
                label="Fullname" hide-details type="username"></v-text-field>
              <v-text-field variant="outlined" v-model="details.dob" class="bg-neutral" density="comfortable"
                placeholder="dd/mm/yyyy" label="Date of Birth" hide-details type="date" />
              <v-select v-model="details.gender" variant="outlined" class="bg-neutral" density="comfortable"
                label="Gender" hide-details :items="genderSel" item-value="val" item-title="label"></v-select>
              <v-text-field v-model="details.number" variant="outlined" class="bg-neutral" density="comfortable"
                label="Phone Number" hide-details type="text"></v-text-field>
              <div class="w-full flex flex-col">
                <v-btn color="primary" class="text-white" type="submit" @click.prevent="handleSignup()">Register</v-btn>
              </div>
            </v-form>
            <v-btn class="text-black mt-3" variant="outlined" @click="tab = 'one'"><v-icon>mdi
                mdi-arrow-left</v-icon> Back</v-btn>
          </div>
        </v-tabs-window-item>
      </v-tabs-window>
      <div class="flex justify-center gap-1">
        <p class=" font-light">Already have an account?</p>
        <nuxt-link class="text-c-primary hover:text-black cursor-pointer">Log in</nuxt-link>
        <p class=" font-light">here</p>
      </div>
    </div>
  </div>
</template>