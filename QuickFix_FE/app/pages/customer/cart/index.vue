<script setup>
useHead({
  title: 'Cart'
})
definePageMeta({
  middleware: 'authmid',
  role: ['customer']
})
import { triggerSnackbar } from '#imports'
import debounce from 'lodash.debounce';
import { useCheckoutStore } from "~/stores/checkout";
const checkoutStore = useCheckoutStore()
const route = useRoute()
const api = useApi()
const isloading = ref(true)
const page = ref(1)
const cart_item = ref()
const selected = ref([])

const fetchCart = async () => {
  let error = false
  try {
    isloading.value = true
    cart_item.value = await api(`cartitem/action`, {
      method: 'GET',
      query: {
        page: page.value
      }
    })
  } catch (err) {
    console.log('error getting items', err)
    triggerSnackbar('Failed to load items', 'danger')
    error = true
  } finally {
    if (!error) {
      isloading.value = false
    }
  }
}

const editAmount = async (id, quant) => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`cartitem/action`, {
      method: 'PUT',
      query: {
        item_id:id,
        quant:quant
      }
    })
  } catch (err) {
    console.log('error getting items', err)
    triggerSnackbar('Failed to load items', 'danger')
    error = true
  } finally {
    if (!error) {
      isloading.value = false
    }
  }
}

const deleteItem = async (id,) => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`cartitem/action`, {
      method: 'DELETE',
      query: {
        item_id:id,
      }
    })
  } catch (err) {
    console.log('error getting items', err)
    triggerSnackbar('Failed to load items', 'danger')
    error = true
  } finally {
    if (!error) {
      isloading.value = false
      fetchCart()
    }
  }
}

const proceedToCheckout = () => {
  const chosenItems = cart_item.value.data.filter(item => selected.value.includes(item.id))
  
  checkoutStore.setCheckoutItems(chosenItems)
  checkoutStore.setCheckoutItemids(selected.value)
  
  navigateTo('/customer/cart/checkout')
}

const handleBounce = debounce((id, quant) => {
  editAmount(id, quant)
}, 800)

const selectedTotal = computed(() => {
  if (!cart_item.value?.data) return 0
  
  return cart_item.value.data.reduce((sum, item) => {
    if (selected.value.includes(item.id)) {
      const price = item.product?.price || 0
      const qty = item.quantity || 0
      return sum + (price * qty)
    }
    return sum
  }, 0)
})

const isAllSelected = computed({
  get() {
    if (!cart_item.value?.data?.length) return false
    return selected.value.length === cart_item.value.data.length
  },
  set(value) {
    if (value) {
      selected.value = cart_item.value.data.map(item => item.id)
    } else {
      selected.value = []
    }
  }
})

onMounted(async () => {
  await Promise.all([
    fetchCart(),
  ])
})

</script>

<template>
  <main class="h-full w-full flex flex-col bg-c-neutral p-10 gap-8 mt-14">
    <!-- {{ cart_item }} -->
    <div class="text-start max-w-384 md:min-w-7xl mx-auto">
      <h1 class="text-3xl font-semibold text-start">Your Cart</h1>
    </div>
    <div class="max-w-384 md:min-w-7xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
      <div class="max-w-8xl mx-auto w-full flex flex-col gap-8 items-start col-span-8">
        <div class="bg-white border! w-full py-1 px-4 rounded-lg flex items-center gap-3 -mb-3">
          <v-checkbox 
            v-model="isAllSelected" 
            label="Select All Items" 
            hide-details
            color="primary"
            class="v-checkbox-select-all"
          ></v-checkbox>
        </div>
        <div class="flex flex-col w-full gap-1">
          <div v-for="(item, index) in cart_item?.data" class="bg-white border! w-full p-4 rounded-lg flex items-center gap-3">
            <v-checkbox v-model="selected" hide-details color="primary" :value="item.id">
            </v-checkbox>
            <div class="w-full! flex justify-between">
              <div class="flex gap-4">
                <div>
                  <v-img :src="item.product?.image_url ?? '/drugsingle.png'" class="rounded-lg" width="73"></v-img>
                </div>
                <p class="text-xl whitespace-pre-line wrap-break-word text-justify leading-relaxed">{{
                  `${item.product?.generic_name} (${item.product?.name})` }}</p>
              </div>
              <div>
                <p class=" font-light mb-1 text-end">{{ Number(item.product?.price)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</p>
                <div class="flex gap-3">
                  <v-btn variant="plain" color="red" @click.prevent="deleteItem(item.id)"><v-icon size="x-large">mdi mdi-delete</v-icon></v-btn>
                  <v-number-input :reverse="false" controlVariant="split" :hideInput="false" v-model="item.quantity"
                    inset variant="outlined" density="compact" :min="1" :max="item?.product?.stock?.stock_qty__sum"
                    hide-details class="w-40" @update:model-value="handleBounce(item.id, item.quantity)"></v-number-input>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="max-w-4xl mx-auto w-full flex flex-col gap-8 items-start col-span-4">
        <div class="bg-c-tertiary border! w-full p-4 rounded-lg flex flex-col gap-3">
          <p class=" text-lg font-semibold">Order Summary</p>
          <v-divider></v-divider>
          <div class="text-lg flex justify-between">
            <p>Selected Total</p>
            <p>{{ Number(selectedTotal)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</p>
          </div>
          <v-btn color="primary" size="large" @click="proceedToCheckout">Proceed to Checkout</v-btn>
        </div>
      </div>
    </div>
  </main>
</template>