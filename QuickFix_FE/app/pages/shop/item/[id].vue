<script setup>
useHead({
  title: 'Medicine Detail'
})
import { triggerSnackbar } from '#imports'
const route = useRoute()
const api = useApi()
const isloading = ref(true)
const detail = ref()
const amount = ref(1)

const fetchItemDetail = async () => {
  let error = false
  try {
    isloading.value = true
    detail.value = await api(`shop/details/${route.params.id}`, {
      method: 'GET'
    })
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      isloading.value = false
    }
  }
}

const addToCart = async () => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`cartitem/action`, {
      method: 'POST', 
      body: {
        item_id : route.params.id,
        quant : amount.value
      }
    })

    console.log(response)
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      isloading.value = false
      triggerSnackbar('Item successfully added to cart!', 'primary')
    }
  }
}

const subtotal = computed(()=>{
  const price = detail.value?.price || 0;
  const qty = amount.value || 1;
  return price * qty;
})

onMounted(async () => {
  await Promise.all([
    fetchItemDetail(),
  ])
})
</script>

<template>
  <main class="flex-1 w-full bg-c-neutral p-6 md:p-12 overflow-y-auto mt-14">
    <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
      <div class="md:col-span-5 flex justify-center">
        <div class="rounded-lg p-4 bg-white h-120 w-120 border-c-tertiary border flex items-center justify-center shadow-sm">
          <v-img :src="detail?.image_link ?? '/drugsingle.png'" class="rounded-lg w-full h-full" cover></v-img>
        </div>
      </div>
      
      <div class="md:col-span-7 flex flex-col gap-6 w-full">
        <div>
          <p class="text-sm text-gray-500 uppercase tracking-wide">{{ detail?.category_name }}</p>
          <h1 class="text-4xl font-semibold text-c-primary mt-1 mb-2">
            {{ `${detail?.generic_name} (${detail?.name})` }}
          </h1>
          <v-chip v-if="detail?.requires_prescription" class="text-white" color="primary" variant="elevated" density="compact">
            Require Prescription
          </v-chip>
        </div>

        <div class="bg-tertiary border p-5 rounded-lg flex flex-col gap-4 shadow-sm bg-white">
          <div>
            <h2 class="text-c-primary font-semibold text-3xl">
              {{ Number(detail?.price)?.toLocaleString('id-ID', {
                style: 'currency', currency: 'IDR',
                trailingZeroDisplay: 'stripIfInteger'
              }) }}
            </h2>
          </div>
          <v-divider></v-divider>
          
          <div class="flex gap-8">
            <div>
              <p class="text-xs font-bold text-gray-500">DOSAGE TYPE</p>
              <p class="text-c-primary font-bold">{{ detail?.dosage_form }}</p>
            </div>
            <div>
              <p class="text-xs font-bold text-gray-500">DOSAGE</p>
              <p class="text-c-primary font-bold">{{ detail?.strength }}</p>
            </div>
          </div>
          <v-divider></v-divider>

          <div class="flex flex-wrap items-end justify-between gap-4 mt-2">
            <div class="flex flex-col gap-1 min-w-40">
              <p class="text-xs font-bold text-gray-500">QUANTITY</p>
              <v-number-input :reverse="false" controlVariant="split" :hideInput="false" v-model="amount"
                inset variant="outlined" density="compact" :min="1" :max="detail?.stock?.stock_qty__sum"
                hide-details class="w-40"></v-number-input>
              <p class="text-sm font-semibold mt-2 text-gray-600">
                Subtotal: <span class="text-c-primary font-bold">{{ Number(subtotal)?.toLocaleString('id-ID', {
                  style: 'currency', currency: 'IDR',
                  trailingZeroDisplay: 'stripIfInteger'
                }) }}</span>
              </p>
            </div>
            <v-btn class="py-2 px-6" size="large" color="primary" @click.prevent="addToCart()"
            :disabled="detail?.requires_prescription">
              <v-icon class="mr-2">mdi-cart-arrow-down</v-icon> Add to Cart
            </v-btn>
          </div>
        </div>

        <div class="bg-tertiary border p-5 rounded-lg flex flex-col gap-3 shadow-sm bg-white">
          <h3 class="text-xl text-c-primary font-semibold">Description</h3>
          <v-divider></v-divider>
          <p class="whitespace-pre-line wrap-break-word text-justify text-gray-700 leading-relaxed">{{ detail?.description }}</p>
        </div>
      </div>

    </div>
  </main>
</template>