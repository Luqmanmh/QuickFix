<script setup>
const api = useApi()
const isloading = ref(true)
const cat = ref()
const selected = ref({
  categories:[]
})
const emit = defineEmits(['filter'])

const fetchCategory = async () => {
  let error = false
  try {
    isloading.value = true
    cat.value = await api('category/list', {
      method: 'GET'
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

const defFilter = () => {
  emit('filter', {
    category_list: selected.value.categories,
    // dosage: selected.value.dosage,
    price_low: selected.value.price_low,
    price_high: selected.value.price_high,
    presc: selected.value.presc,
  })
}

onMounted(async () => {
  await Promise.all([
    fetchCategory(),
  ])
})
</script>

<template>
  <div class="bg-white rounded-lg p-4 flex flex-col border-c-tertiary border gap-4">
    <div class="flex gap-2">
      <v-icon color="primary">mdi mdi-filter</v-icon>
      <p class=" text-lg font-semibold text-c-primary">Filters</p>
    </div>
    <div>
      <p>Categories</p>
      <div class="checkbox-group">
        <v-checkbox v-for="c in cat" :key="c.id" v-model="selected.categories" :value="c.id" :label="c.name"
          density="compact" hide-details @update:model-value="defFilter"></v-checkbox>
        <v-checkbox v-model="selected.presc" label="Need Prescription" :value="true" density="compact" hide-details
        @update:model-value="defFilter">
        </v-checkbox>
      </div>
    </div>
    <!-- <div>
      <p>Dosage Type</p>
      <v-text-field variant="outlined" density="compact" hide-details placeholder="pills, tablets, syrup"
      v-model="selected.dosage">
      </v-text-field>
    </div> -->
    <div class="w-full">
      <p>Price Range</p>
      <div class="flex flex-col justify-center w-full">
        <v-text-field variant="outlined" density="compact" hide-details placeholder="price low"
          v-model="selected.price_low" @update:model-value="defFilter">
        </v-text-field>
        <v-icon color="primary" class="mx-auto">mdi mdi-minus</v-icon>
        <v-text-field variant="outlined" density="compact" hide-details placeholder="price high"
          v-model="selected.price_high" @update:model-value="defFilter">
        </v-text-field>
      </div>
    </div>
  </div>
</template>