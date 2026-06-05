<script setup>
useHead({
  title: 'Manage Orders'
})
definePageMeta({
  middleware: 'authmid',
  role: ['pharmacist', 'admin'],
  layout: 'back'
})
import debounce from 'lodash.debounce';
const route = useRoute()
const api = useApi()
const isloading = ref(true)
const item_list = ref([])
const tab = ref('one')

const headerItem = [
  { title: "ID", key: "id", align: "start", headerProps: { class: 'bg-c-tertiary text-c-primary font-bold' } },
  { title: "Customer Username", key: "user.username", align: "center", headerProps: { class: 'bg-c-tertiary text-c-primary font-bold' } },
  { title: "Status", key: "status", align: "center", headerProps: { class: 'bg-c-tertiary text-c-primary font-bold' } },
  { title: "Total Amount", key: "total_amount", align: "center", headerProps: { class: 'bg-c-tertiary text-c-primary font-bold' } },
  { title: "Actions", key: "actions", align: "end", sortable: false, headerProps: { class: 'bg-c-tertiary text-c-primary font-bold' } },
]

const fetchItemList = async () => {
  let error = false
  try {
    isloading.value = true
    item_list.value = await api('order/manage/list', {
      method: 'GET', query: {
      }
    })
  } catch (err) {
    console.log('error getting items', err)
    error = true
    // reloadNuxtApp()
  } finally {
    if (!error) {
      isloading.value = false
    }
  }
}



onMounted(async () => {
  await Promise.all([
    fetchItemList(),
  ])
})

</script>

<template>
  <main class="h-full w-full flex flex-col bg-c-neutral p-10 gap-8 mt-14">
    <div>
      <div class=" lg:w-1/2">
        <h1 class="text-3xl font-semibold">Manage Orders</h1>
        <p class=" text-gray-600">Manage all ongoing orders waiting to be prepared. Click on action button to start preparing</p>
      </div>
      <v-tabs v-model="tab">
        <v-tab value="one">Incoming Orders</v-tab>
        <v-tab value="two">Preparing Orders</v-tab>
      </v-tabs>

      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="one" class="d-flex flex-column ga-2">
          <v-data-table :headers="headerItem" :items="item_list.created" class="shadow-lg border rounded mt-3" hide-default-footer>
            <template #item.total_amount="{item}">
              <p>{{ Number(item.total_amount)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</p>
            </template>
            <template #item.actions="{item}">
              <nuxt-link :to="`order/${item.id}`" class="w-full h-full"><v-icon>mdi mdi-chevron-right</v-icon></nuxt-link>
            </template>
          </v-data-table>
        </v-tabs-window-item>
        <v-tabs-window-item value="two" class="d-flex flex-column ga-2">
          <v-data-table :headers="headerItem" :items="item_list.prepare" class="shadow-lg border rounded mt-3" hide-default-footer>
            <template #item.total_amount="{item}">
              <p>{{ Number(item.total_amount)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</p>
            </template>
            <template #item.actions="{item}">
              <nuxt-link :to="`order/${item.id}`" class="w-full h-full"><v-icon>mdi mdi-chevron-right</v-icon></nuxt-link>
            </template>
          </v-data-table>
        </v-tabs-window-item>
      </v-tabs-window>
    </div>
  </main>
</template>