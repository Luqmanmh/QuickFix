<script setup>
useHead({
  title: 'Order'
})
definePageMeta({
  middleware: 'authmid',
  role: ['customer']
})
const api = useApi()
const isloading = ref(true)
const orders = ref()

const fetchOrders = async () => {
  let error = false
  try {
    isloading.value = true
    orders.value = await api(`order/list`, {
      method: 'GET'
    })
    // console.log(orders.value)
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

const downloadQR = (id) => {
  const svg = document.querySelector(`#qr-${id} svg`)
  console.log(svg)
  if (!svg) return

  const svgData = new XMLSerializer().serializeToString(svg)

  const blob = new Blob([svgData], {
    type: 'image/svg+xml;charset=utf-8'
  })

  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = url
  link.download = `qr-${id}.svg`
  link.click()

  URL.revokeObjectURL(url)
}

onMounted(async () => {
  await Promise.all([
    fetchOrders(),
  ])
})

</script>

<template>
  <main class="flex-1 w-full bg-c-neutral p-6 md:p-12 overflow-y-auto mt-14">
    <div class="max-w-384 md:min-w-7xl mx-auto flex flex-col gap-8 items-start">
      <div class="text-start max-w-384 md:min-w-7xl mx-auto">
        <h1 class="text-3xl font-semibold text-start">Your Orders</h1>
      </div>
      <div class="text-start max-w-384 md:min-w-7xl mx-auto">
        <div v-for="(order, index) in orders" class="w-full p-1 rounded-lg flex items-center gap-3">
          <v-expansion-panels class="border! rounded-lg border-black my-0" color="white">
            <v-expansion-panel>
              <template v-slot:title>
                <div class="grid grid-cols-6 gap-4 justify-between w-full mx-3 p-4">
                  <div>
                    <p class="text-xs font-bold text-gray-500">ORDER ID</p>
                    <p class="text-c-primary font-bold text-lg">{{ order.id }}</p>
                  </div>
                  <div class="text-center" @click.stop>
                    <p class="text-xs font-bold text-gray-500">QR CODE</p>
                    <v-dialog max-width="500">
                      <template v-slot:activator="{ props: activatorProps }">
                        <v-btn v-bind="activatorProps" variant="outlined" icon="mdi mdi-qrcode" rounded="15"
                          color="primary"></v-btn>
                      </template>
                      <template v-slot:default="{ isActive }">
                        <v-card title="Order QR">
                          <v-card-text>
                            <div :id="`qr-${order.id}`">
                              <Qrcode :value="order.id" variant="pixelated" />
                            </div>
                            <v-btn @click="downloadQR(order.id)" class="w-100" color="primary">
                              Download
                            </v-btn>
                          </v-card-text>
                        </v-card>
                      </template>
                    </v-dialog>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-gray-500">PRESCRIPTION</p>
                    <p class="text-c-primary font-bold text-lg">{{ order.prescription ?? 'No' }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-gray-500">CHANNEL</p>
                    <p class="text-c-primary font-bold text-lg">{{ order.channel }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-gray-500">STATUS</p>
                    <p class="text-c-primary font-bold text-lg">{{ order.status }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-gray-500">Total Price</p>
                    <p class="text-c-primary font-bold text-lg">{{ Number(order.total_amount)?.toLocaleString('id-ID', {
                      style: 'currency', currency: 'IDR',
                      trailingZeroDisplay: 'stripIfInteger'
                    }) }}</p>
                  </div>
                </div>
              </template>
              <template v-slot:text>
                <div class="flex flex-col gap-4">
                  <div v-for="(item, idx) in order.items" class="flex flex-col gap-4">
                    <Orderitemcard :item="item" />
                  </div>
                </div>
              </template>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </div>
    </div>
  </main>
</template>