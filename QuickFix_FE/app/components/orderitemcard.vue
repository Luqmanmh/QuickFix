<script setup>
const props = defineProps({
  item: {
    type: Object
  }
})

</script>

<template>
  <div>
    <v-expansion-panels class="border! rounded-lg border-black">
      <v-expansion-panel>
        <template v-slot:title>
          <Orderitem :item="item" />
        </template>
        <template v-slot:text>
          <div class="flex gap-4 justify-between w-full mx-3 p-2">
            <div class="text-sm">
              <p class="text-xs font-bold text-gray-500">BATCH NUMBER</p>
              <p class="text-c-primary font-bold text-lg">{{ item.batch.batch_number }}</p>
            </div>
            <div class="text-sm">
              <p class="text-xs font-bold text-gray-500">EXPIRY DATE</p>
              <p class="text-c-primary font-bold text-lg">{{ new Date(item.batch.expiry_date).toLocaleDateString('en-GB') }}</p>
            </div>
            <div class="text-sm">
              <p class="text-xs font-bold text-gray-500">SUPPLIER</p>
              <p class="text-c-primary font-bold text-lg">{{ item.batch.supplier_name }}</p>
            </div>
          </div>
        </template>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>