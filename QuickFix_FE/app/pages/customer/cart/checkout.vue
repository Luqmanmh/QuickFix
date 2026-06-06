<script setup>
useHead({
  title: 'Order Checkout'
})
definePageMeta({
  middleware: 'authmid',
  role: ['customer']
})
import { useCheckoutStore } from "~/stores/checkout";
const checkoutStore = useCheckoutStore()
const payment = ref(true)
const api = useApi()
const isloading = ref(false)
const paymentMethod = ref('ON_SITE')
const showPaymentModal = ref(false)

const createOrder = async () => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`order/create`, {
      method: 'POST', 
      body: {
        cart_items : checkoutStore.checkoutItemids,
        payment_method: paymentMethod.value
      }
    })
    console.log(response)
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      isloading.value = false
      const showPaymentModal = ref(false)
      triggerSnackbar('Order Created Successfully', 'primary')
      navigateTo('/customer/order')
    }
  }
}

const vanum = computed(() => {
  return '8834002612365' + (checkoutStore.checkoutItemids[0]*7).toString()
})

const copyText = async(text) => {
  await navigator.clipboard.writeText(text);
}

const handleCreateOrder = async () => {
  if (paymentMethod.value === 'ON_SITE') {
    await createOrder()
  } else {
    showPaymentModal.value = true
  }
}

onMounted(() => {
  if (checkoutStore.totalItemsCount === 0) {
    navigateTo('/customer/cart')
  }
})

</script>

<template>
  <main class="h-full w-full flex flex-col bg-c-neutral p-10 gap-8 mt-14">
    <div class="text-start max-w-384 md:min-w-7xl mx-auto">
      <h1 class="text-3xl font-semibold text-start">Checkout</h1>
    </div>
    <div class="max-w-384 md:min-w-7xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
      <div class="max-w-8xl mx-auto w-full flex flex-col gap-8 items-start col-span-8">
        <div class="bg-c-tertiary p-2 w-full rounded-lg flex flex-col items-center gap-3 border-gray-400 border!">
          <div v-for="(item, index) in checkoutStore.checkoutItems" class="w-full">
            <Orderitem :item="item"/>
          </div>
        </div>
      </div>
      <div class="max-w-4xl mx-auto w-full flex flex-col gap-8 items-start col-span-4">
        <div class="bg-c-tertiary w-full p-4 rounded-lg flex flex-col gap-3 border-gray-400 border!">
          <p class=" text-lg font-semibold">Order Summary</p>
          <v-divider></v-divider>
          <div>
            <p class="">Payment Options</p>
            <v-radio-group v-model="paymentMethod" hide-details mandatory>
              <span class="text-slate-500 mt-2">On-Site:</span>
              <v-radio label="Pay At Pharmacy Counter " value="ON_SITE" color="primary"></v-radio>
              <v-divider></v-divider>
              <span class="text-slate-500 mt-2">Online:</span>
              <v-radio label="QRIS" value="QRIS" color="primary"></v-radio>
              <v-radio label="BNI Virtual Acount" value="BNI" color="primary"></v-radio>
              <v-radio label="BCA Virtual Acount" value="BCA" color="primary"></v-radio>
            </v-radio-group>
          </div>
          <div class="text-lg flex justify-between">
            <p>Total</p>
            <p>{{ Number(checkoutStore.itemsSubtotal)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</p>
          </div>
          <v-btn color="primary" size="large" @click.prevent="handleCreateOrder">{{ paymentMethod === 'ONLINE' ? 'Pay Now & Checkout' : 'Place Order' }}</v-btn>
        </div>
      </div>
    </div>

    <v-dialog v-model="showPaymentModal" max-width="500" persistent>
      <v-card class="rounded-xl pa-4">
        <v-card-title class="text-xl font-bold d-flex items-center ga-2 border-b pb-3">
          <v-icon color="primary">
            {{ paymentMethod === 'QRIS' ? 'mdi-qrcode' : 'mdi-bank-transfer' }}
          </v-icon>
          <span>Online Payment Gateway</span>
        </v-card-title>

        <v-card-text class="py-6 flex flex-col items-center text-center gap-4">
          <p class="text-sm text-slate-500">
            You are processing an online transaction via <strong class="text-slate-800">{{ paymentMethod }}</strong> for a total invoice value of:
          </p>z
          
          <span class="text-3xl font-black text-cyan-900 bg-slate-50 px-6 py-2 rounded-xl border border-dashed">
            {{ Number(checkoutStore.itemsSubtotal)?.toLocaleString('id-ID', { style: 'currency', currency: 'IDR', trailingZeroDisplay: 'stripIfInteger' }) }}
          </span>

          <div v-if="paymentMethod === 'QRIS'" class="p-4 bg-white border border-slate-200 rounded-2xl shadow-inner mt-2">
            <v-icon size="180" color="grey-darken-3">mdi-qrcode-scan</v-icon>
            <p class="text-[10px] uppercase font-bold text-slate-400 mt-2 tracking-wider">Simulated QRIS</p>
          </div>

          <div v-else class="w-full bg-slate-50 border p-4 rounded-xl text-left font-mono mt-2 text-sm flex flex-col gap-1.5">
            <div class="flex justify-between">
              <span class="text-slate-400">Bank:</span>
              <span class="font-bold text-slate-700">{{ paymentMethod }} Transfer</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-slate-400">VA Number:</span>
              <div>
                <span class="font-bold text-cyan-800 tracking-wider">{{vanum}}</span>
                <v-btn icon="mdi mdi-content-copy" size="x-small" variant="text" @click.prevent="copyText(vanum)"></v-btn>
              </div>
            </div>
            <p class="text-[10px] text-center text-slate-400 font-sans mt-2 italic">
              Instructions: Transfer the exact amount above to complete checkout verification.
            </p>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pt-3 flex gap-2">
          <v-btn variant="outlined" color="grey" class="flex-1 font-bold" rounded="lg" :disabled="isloading" @click="showPaymentModal = false">
            Cancel
          </v-btn>
          <v-btn color="primary" variant="flat" class="flex-1 font-bold" rounded="lg" :loading="isloading" @click="createOrder">
            Simulate Success
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </main>
</template>