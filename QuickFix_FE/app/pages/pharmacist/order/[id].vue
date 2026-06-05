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
const pid = route.params.id
const item_list = ref([])

const fetchItemList = async () => {
  let error = false
  try {
    isloading.value = true
    item_list.value = await api(`orderitem/manage/${route.params.id}`, {
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
const handlePrepReady = async (stat) => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`order/prepready/${route.params.id}`, {
      method: 'PUT', query: {
        stat :stat
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
    if(stat == 'READY'){
      navigateTo('/pharmacist/order')
    }
  }
}
const handleorderbatch = async (id, batch_id) => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`orderitem/setbatch`, {
      method: 'PUT', query: {
        id: id,
        batch: batch_id
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

const selectedTotal = computed(() => {
  let sum = 0
  return item_list.value.reduce((sum, item) => {
      const price = item.price_at_purchase || 0
      const qty = item.quantity || 0
      return sum + (price * qty)
    }, 0)
  })


onMounted(async () => {
  await Promise.all([
    fetchItemList(),
    handlePrepReady('PREPARING')
  ])
})
</script>

<template>
  <div class="h-full w-full flex flex-col bg-c-neutral p-10 gap-8 mt-14">
    <div>
      <h1 class="text-3xl font-semibold">Manage Order</h1>
      <p>Order ID: {{ pid.toUpperCase() }}</p>
    </div>
    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-8">
        <div class="w-full bg-c-tertiary rounded-lg border shadow-sm overflow-hidden">
          <div class="flex flex-col w-full divide-y">
            <div v-for="(item, index) in item_list" :key="item.id" class="w-full">

              <v-expansion-panels variant="accordion" flat>
                <v-expansion-panel class="bg-transparent">

                  <template v-slot:title>
                    <Orderitem :item="item" />
                  </template>

                  <template v-slot:text>
                    <div class="bg-c-neutral rounded-lg p-4 border border-slate-200 my-2 ml-4 mr-8">
                      <div class="flex justify-between items-center mb-2">
                        <h3 class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Available Stock
                          Batches</h3>
                      </div>

                      <div
                        class="grid grid-cols-12 gap-4 items-center w-full py-2 font-semibold text-sm text-c-primary border-b">
                        <div class="col-span-2">
                          <p>Batch Number</p>
                        </div>
                        <div class="col-span-2">
                          <p>Supplier</p>
                        </div>
                        <div class="col-span-2">
                          <p>Expiry Date</p>
                        </div>
                        <div class="col-span-2">
                          <p>Stock</p>
                        </div>
                        <div class="col-span-2">
                          <p>Stock Status</p>
                        </div>
                        <div class="col-span-2 text-right">
                          <p>Batch Select</p>
                        </div>
                      </div>

                      <div v-if="item?.product?.batches.length" v-for="(batch, idx) in item?.product?.batches"
                        :key="idx"
                        class="grid grid-cols-12 gap-4 items-center w-full py-3 text-sm text-slate-600 border-b last:border-0 hover:bg-slate-100/50 px-1 transition-colors">
                        <div class="col-span-2 font-mono text-slate-700">
                          <p>{{ batch?.batch_number }}</p>
                        </div>
                        <div class="col-span-2">
                          <p>{{ batch?.supplier_name }}</p>
                        </div>
                        
                        <div class="col-span-2">
                          <p :class="new Date(batch?.expiry_date) < new Date() ? 'text-rose-500 font-semibold' : ''">
                            {{ new Date(batch?.expiry_date).toLocaleDateString('en-GB') }}
                          </p>
                        </div>
                        <div class="col-span-2">
                          <p>{{ batch?.stock_qty}}</p>
                        </div>
                        <div class="col-span-2">
                          <Batchstatuschip :current="batch.stock_qty" :minimum="item.minimum_stock" />
                        </div>
                        <div class="col-span-2 text-right flex justify-center">
                          <v-checkbox v-model="item.batch" :value="batch.id"
                          density="compact" hide-details @update:model-value="handleorderbatch(item.id, batch.id)" ></v-checkbox>
                        </div>
                      </div>

                      <div v-else class="text-center py-4 text-sm text-slate-400 italic">
                        No active stock batches found for this medical item profile.
                      </div>
                    </div>
                  </template>

                </v-expansion-panel>
              </v-expansion-panels>

            </div>
          </div>

        </div>
      </div>
      <div class="max-w-4xl mx-auto w-full flex flex-col gap-8 items-start col-span-4">
        <div class="bg-c-tertiary border w-full p-4 rounded-lg flex flex-col gap-3">
          <p class=" text-lg font-semibold">Order Summary</p>
          <v-divider></v-divider>
          <div class="text-lg flex justify-between">
            <p>Total</p>
            <p>{{ Number(selectedTotal)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</p>
          </div>
          <v-btn color="primary" size="large" @click.prevent="handlePrepReady('READY')">Ready Order</v-btn>
        </div>
      </div>
    </div>
  </div>

</template>