<script setup>
import { snackbarStore } from '~/stores/useSnack.js';
const route = useRoute()
const alert = ref(false)

onMounted(() => {
  if (route.query.message) {
    alert.value = true
  }
})
</script>

<template>
  <div class="h-screen flex flex-col ">
    <v-snackbar v-model="snackbarStore.show" location="top " timeout="5000" :color="snackbarStore.color">
      {{ snackbarStore.message }}
      <template v-slot:actions>
        <v-btn color="pink" variant="text" @click="snackbarStore.show = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <navbar />
    <div class="flex overflow-hidden">
      <sidenav/>
      <main class="flex-1 bg-c-neutral! overflow-y-auto">
        <slot />
      </main>
    </div>
  </div>
</template>
