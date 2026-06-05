<script setup>
useHead({
  title: 'Shop'
})
import debounce from 'lodash.debounce';
import { useAuthStore } from '~/stores/auth';
const useAuth = useAuthStore()
const route = useRoute()
const api = useApi()
const isloading = ref(true)
const item_list = ref([])
const item_auto = ref([])
const query = ref({})
const quest = ref()
const page_len = ref(30)
const page = ref(1)

const handleBounce = debounce(() => {
  fetchAutocomplete()
}, 500)


const fetchItemList = async () => {
  let error = false
  try {
    isloading.value = true
    item_list.value = await api('shop/itemlist', {
      method: 'GET', query: {
        query: quest.value,
        category: query.value?.category_list,
        dosage: query.value?.dosage,
        price_low: query.value?.price_low,
        price_high: query.value?.price_high,
        presc: query.value?.presc,
        page_len: page_len.value,
        page: page.value
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

const fetchAutocomplete = async () => {
  let error = false
  try {
    isloading.value = true
    item_auto.value = await api('shop/autocomplete', {
      method: 'GET', query: {
        query: quest.value,
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

const handleFilter = async (data) => {
  query.value = data
  await fetchItemList()
}

onMounted(async () => {
  await Promise.all([
    fetchItemList(),
  ])
})
</script>

<template>
  <main class="h-full w-full flex flex-col bg-c-neutral p-10 gap-8 mt-14">
    <div class="">
      <h1 class="text-3xl font-semibold">Pharmacy Catalog</h1>
      <p class=" text-gray-600">Browse our certified range of medications and wellness products.<br> High-standard
        pharmaceutical care at your fingertips.</p>
    </div>
    <v-row>
      <v-col cols="2">
        <Shopfilter @filter="handleFilter"/>
      </v-col>
      <v-col cols="10">
        <div class="flex gap-8">
          <v-autocomplete type="text" variant="outlined" label="Search Item" autocomplete="false"
            v-model="quest" density="comfortable" hide-details clearable class="bg-white" 
            @update:search="handleBounce()" @update:model-value="fetchItemList()" :items="item_auto" item-value="name" append-icon="" 
            :item-title="item => item ? `${item.name} (${item.generic_name}) ` : ''" placeholder="Search medicine"
            no-auto-scroll></v-autocomplete>
          <!-- <v-btn color="primary" prepend-icon="mdi mdi-magnify" @click.prevent="fetchItemList()" density="">Search</v-btn> -->
        </div>
        <div class="mt-10 grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-8">
          <div v-for="(item, idx) in item_list.data">
            <Itemcard :obj="item"/>
          </div>
        </div>
        <div>
          <v-pagination :length="item_list.pagin?.total_page" active-color="primary" v-model="page"
              :total-visible="5" @update:model-value="fetchItemList()">
            </v-pagination>
        </div>
      </v-col>
    </v-row>
  </main>
</template>