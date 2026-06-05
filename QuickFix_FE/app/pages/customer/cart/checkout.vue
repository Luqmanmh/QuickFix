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

const createOrder = async () => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`order/create`, {
      method: 'POST', 
      body: {
        cart_items : checkoutStore.checkoutItemids,
      }
    })
    console.log(response)
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      triggerSnackbar('Order Created Successfully', 'primary')
      isloading.value = false
    }
  }
}

const handleCreateOrder = async () => {
  await createOrder()
  navigateTo('/customer/order')
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
            <v-checkbox
            label="On SIte"
            v-model="payment"
            :value="true" 
            density="comfortable" 
            hide-details
            ></v-checkbox>

          </div>
          <div class="text-lg flex justify-between">
            <p>Total</p>
            <p>{{ Number(checkoutStore.itemsSubtotal)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</p>
          </div>
          <v-btn color="primary" size="large" @click.prevent="handleCreateOrder">Checkout</v-btn>
        </div>
      </div>
    </div>
  </main>
</template>