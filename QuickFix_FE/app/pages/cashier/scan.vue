<script setup>
import { ref, watch } from 'vue'
import { triggerSnackbar } from '#imports'
import debounce from 'lodash.debounce'
import { isActionItem } from 'vuetify/lib/labs/VCommandPalette/types.mjs'

useHead({
  title: 'Scan Orders'
})
definePageMeta({
  middleware: 'authmid',
  role: ['cashier', 'admin'],
  layout: 'back'
})

const api = useApi()
const isloading = ref(false)
const orderSearchQuery = ref('')
const cam = ref(true)
const item = ref(null)

const headerItem = [
  { title: "Product", key: "product.name", align: "center" },
  { title: "Dosage Type", key: "product.dosage_form", align: "center" },
  { title: "Dosage", key: "product.strength", align: "center" },
  { title: "Quantity", key: "quantity", align: "center" },
  { title: "Price", key: "price_at_purchase", align: "center" },
]

const orderData = ref({
  id: 'QF-2024-8839-PX',
  customer: { name: 'Alexander Murphy', dob: '12/05/1982', age: 41 },
  items: [
    { name: 'Amoxicillin 500mg', details: 'Capsule • Take 3x daily', qty: 30, price: 14.50 },
    { name: 'Lisinopril 10mg', details: 'Tablet • Once daily morning', qty: 90, price: 22.00 }
  ],
  totalAmount: 46.49
})

function onDetect(detectedCodes) {
  if (detectedCodes && detectedCodes.length > 0) {

    orderSearchQuery.value = detectedCodes[0].rawValue
  }
}

function onError(err) {
  triggerSnackbar(`Failed to scan qr code: ${err?.message}`, 'danger')
}

const handleFindOrder = async () => {
  if (!orderSearchQuery.value || orderSearchQuery.value.trim() === '') {
    item.value = null
    return
  }

  let error = false
  try {
    isloading.value = true
    const res = await api(`order/scan`, {
      method: 'GET',
      query: {
        id: orderSearchQuery.value.trim()
      }
    })

    // Save response payload
    item.value = res || res
    console.log(item.value)
  } catch (err) {
    console.log('error getting items', err)
    triggerSnackbar('Failed to load matching order profile records', 'danger')
    item.value = null
    error = true
  } finally {
    isloading.value = false
  }
}

const selectedTotal = computed(() => {
  let sum = 0
  return item?.value.data?.items.reduce((sum, item) => {
      const price = item.price_at_purchase || 0
      const qty = item.quantity || 0
      return sum + (price * qty)
    }, 0)
  })

const debouncedFetch = debounce(() => {
  handleFindOrder()
}, 500)

watch(orderSearchQuery, (newValue) => {
  if (newValue === null || newValue.trim() === '') {
    item.value = null          
    orderSearchQuery.value = '' 
    return                    
  }
  debouncedFetch()
})

const handleProcessPickup = () => {
  const userConfirmed = window.confirm("Confirm verification metrics and finalize package handoff distribution?")
  if (userConfirmed) {
    window.alert("Transaction finalized successfully!")
  }
}
</script>

<template>


  <main class="w-full min-h-screen bg-c-neutral p-6 md:p-10 flex flex-col gap-6 mt-14 text-slate-800">
    <div class="grid grid-cols-12 gap-6 w-full">

      <v-card class="col-span-12 md:col-span-8 pa-6 rounded-xl border border-slate-200" elevation="0" color="white">
        <h2 class="text-xl font-bold text-c-primary mb-1">Order Identification</h2>
        <p class="text-sm text-slate-500 mb-6">Enter the 12-digit Order ID to retrieve Order details.</p>

        <div class="flex flex-col sm:flex-row gap-3 items-center w-full">
          <v-text-field v-model="orderSearchQuery" prepend-inner-icon="mdi-pound" variant="outlined"
            density="comfortable" hide-details clearable class="w-full bg-white text-lg font-mono" color="cyan-800"
            :loading="isloading" placeholder="e.g., QF-2024-8839-PX"></v-text-field>

          <v-btn color="#1b5a5a" class="text-white px-6 font-bold h-12 w-full sm:w-auto" flat prepend-icon="mdi-magnify"
            size="large" @click="handleFindOrder">
            Find Order
          </v-btn>
        </div>
      </v-card>

      <v-card
        class="col-span-12 md:col-span-4 pa-6 rounded-xl flex flex-col items-center justify-center text-center border border-neutral-800"
        elevation="0">
        <div class="w-full">
          <QrcodeStream @error="onError" @detect="onDetect" class="w-60! mx-auto p-4 bg-c-primary rounded-2xl mb-2" />
        </div>
        <div>
          <p class="font-semibold">Scan QR Code</p>
          <p class="font-thin text-xs w-2/3 mx-auto mt-2">Place the customer's mobile receipt in front of the scanner
          </p>
        </div>
      </v-card>
    </div>

    <div v-if="item">
      <div class="grid grid-cols-12 gap-6 w-full">
        <v-card class="col-span-12 md:col-span-4 pa-6 rounded-xl border border-slate-200 flex flex-col justify-between"
          elevation="0" color="white">
          <div>
            <div class="flex items-start gap-4 mb-6">
              <div class="flex flex-col">
                <h3 class="text-xl font-bold text-slate-800 leading-tight">{{ item?.user?.first_name || 'Customer' }}
                </h3>
                <p class="text-xs text-slate-500 mt-0.5">Username: {{ item?.user?.username }}
                </p>
              </div>
            </div>
          </div>

          <div class=" mt-2 flex justify-between items-center text-xs">
            <span class="text-slate-400 uppercase font-bold tracking-wider">Date of Birth</span>
            <div class="flex items-center gap-1 text-emerald-600 font-bold">
              <p class="text-slate-500 mt-0.5">{{ new Date(item?.profile?.date_of_birth).toLocaleDateString('en-GB') }}
              </p>
            </div>
          </div>
          <div class="mt-2 flex justify-between items-center text-xs">
            <span class="text-slate-400 uppercase font-bold tracking-wider">Gender</span>
            <div class="flex items-center gap-1 text-emerald-600 font-bold">
              <p class="text-slate-500 mt-0.5">{{ item?.profile?.gender == 'M' ? 'Male' : 'Female' }}</p>
            </div>
          </div>
          <div class="mt-2 flex justify-between items-center text-xs">
            <span class="text-slate-400 uppercase font-bold tracking-wider">Phone Number</span>
            <div class="flex items-center gap-1 text-emerald-600 font-bold">
              <p class="text-slate-500 mt-0.5">{{ item?.profile?.phone_number }}</p>
            </div>
          </div>
          <div class="mt-2 flex justify-between items-center text-xs">
            <span class="text-slate-400 uppercase font-bold tracking-wider">Allergies</span>
            <div class="flex items-center gap-1 text-emerald-600 font-bold">
              <p class="text-slate-500 mt-0.5">{{ item?.profile?.allergies ?? '-' }}</p>
            </div>
          </div>
          <div class="mt-2 flex justify-between items-center text-xs">
            <span class="text-slate-400 uppercase font-bold tracking-wider">Chronic Condition</span>
            <div class="flex items-center gap-1 text-emerald-600 font-bold">
              <p class="text-slate-500 mt-0.5">{{ item?.profile?.chronic_conditions ?? '-' }}</p>
            </div>
          </div>

        </v-card>

        <v-card class="col-span-12 md:col-span-8 rounded-xl border border-slate-200 overflow-hidden flex flex-col"
          elevation="0" color="white">
          <div
            class="bg-c-tertiary px-6 py-3 border-b flex justify-between items-center text-xs font-bold uppercase tracking-wider text-c-primary">
            <span>Order Items ({{ item?.data?.items.length }})</span>
          </div>

          <v-data-table :headers="headerItem" :items="item?.data?.items" class="shadow-sm border rounded mt-3"
            hide-default-footer>

            <template #item.product.name="{ item }">
              <span class="font-bold text-slate-800">{{ item.product?.name }}</span>
            </template>

            <template #item.product.dosage_form="{ item }">
              <span>{{ item.product?.dosage_form }}</span>
            </template>

            <template #item.product.strength="{ item }">
              <v-chip size="x-small" variant="tonal" color="primary">
                {{ item.product?.strength }}
              </v-chip>
            </template>

            <template #item.price_at_purchase="{ item }">
              <span class="font-mono font-bold text-slate-700">
                {{ Number(item.price_at_purchase)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}
              </span>
            </template>
          </v-data-table>
        </v-card>

      </div>
      <v-card
        class="w-full pa-6 rounded-xl border! border-c-tertiary bg-white grid grid-cols-12 gap-6 items-center mt-3"
        elevation="0">

        <div class="col-span-12 sm:col-span-4 flex flex-col pb-4 sm:pb-0">
          <span class="text-xs uppercase font-bold text-slate-400 tracking-wider">Total Amount Due</span>
          <span class="text-4xl font-black text-cyan-900 mt-1">
            {{ Number(selectedTotal)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}
          </span>
        </div>

        <div class="col-span-12 sm:col-span-5 text-right">
          <v-btn width="100%" height="3rem" rounded="12" color="primary" @click="handleProcessPickup">
            <span class="text-lg">Complete Pickup</span>
          </v-btn>
        </div>

      </v-card>
    </div>
    <div v-else class="text-center py-12 text-sm text-slate-400 italic">
      <v-icon size="large" class="mb-2 block mx-auto">mdi-qrcode-scan</v-icon>
      <p>Scan code or submit an Order ID string parameter above to review full details.</p>
    </div>
  </main>
</template>