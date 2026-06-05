<script setup>
import { triggerSnackbar } from '#imports'

const props = defineProps({
  form: {
    type: Object,
    required: true
  },
  isEditing: {
    type: Boolean,
    default: false
  },
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['done'])
const isloading = ref(false)
const api = useApi()

const selectedFile = ref(null)

const handleFileChange = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    selectedFile.value = file
  }
}

const previewUrl = computed(() => {
  if (!selectedFile.value) return null

  if (process.client) {
    return window.URL.createObjectURL(selectedFile.value)
  }

  return null
})

const handleSaveProduct = async () => {
  try {
    isloading.value = true
    const formData = new FormData()
    formData.append('id', props.form.id || '')
    formData.append('sku', props.form.sku || '')
    formData.append('name', props.form.name || '')
    formData.append('generic_name', props.form.generic_name || '')
    formData.append('category', props.form.category || '')
    formData.append('dosage_form', props.form.dosage_form || '')
    formData.append('strength', props.form.strength || '')
    formData.append('price', props.form.price || 0)
    formData.append('minimum_stock', props.form.minimum_stock || 0)
    formData.append('description', props.form.description || '')
    formData.append('requires_prescription', props.form.requires_prescription ? 'true' : 'false') 

    if (selectedFile.value) {
      formData.append('image', selectedFile.value)
    }

    if (props.isEditing) {
      await api(`product/action`, {
        method: 'PUT',
        body: formData
      })
    } else {
      await api(`product/action`, {
        method: 'POST',
        body: formData
      })
    }
    
    triggerSnackbar(props.isEditing ? 'Product Profile Updated' : 'Product Profile Created', 'primary')
    emit('done')
  } catch (err) {
    console.error('Error executing product save:', err)
  } finally {
    isloading.value = false
  }
}
</script>

<template>
  <v-card class="p-4 rounded-lg shadow-md" color="neutral">
    <v-card-title class="text-xl font-bold text-slate-800 border-b pa-4">
      {{ props.isEditing ? 'Edit Product Profile' : 'Add New Product Profile' }}
    </v-card-title>

    <v-card-text class="pt-4 px-8 flex flex-col gap-4">
      <div class="grid grid-cols-2 gap-4">
        <v-text-field
          v-model="props.form.sku"
          label="SKU / Barcode ID"
          variant="outlined"
          density="comfortable"
          class="bg-white"
          hide-details
        ></v-text-field>
        <v-text-field
          v-model="props.form.name"
          label="Chamical Item Name"
          variant="outlined"
          density="comfortable"
          class="bg-white"
          hide-details
        ></v-text-field>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <v-text-field
          v-model="props.form.generic_name"
          label="Generic / Commercial Name"
          variant="outlined"
          density="comfortable"
          class="bg-white"
          hide-details
        ></v-text-field>
        <v-text-field
          v-model="props.form.strength"
          label="Strength (e.g., 500mg, 10ml)"
          variant="outlined"
          density="comfortable"
          class="bg-white"
          hide-details
        ></v-text-field>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <v-autocomplete
          v-model="props.form.category"
          :items="props.categories"
          item-title="name"
          item-value="id"
          label="Select Category"
          variant="outlined"
          density="comfortable"
          class="bg-white"
          hide-details
        ></v-autocomplete>
        <v-text-field
          v-model="props.form.dosage_form"
          label="Dosage Form (e.g., Capsule, Syrup)"
          variant="outlined"
          density="comfortable"
          class="bg-white"
          hide-details
        ></v-text-field>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-xs font-bold text-slate-500 mb-1 uppercase">Unit Base Price (IDR)</p>
          <v-number-input
            controlVariant="split"
            v-model="props.form.price"
            variant="outlined"
            density="comfortable"
            class="bg-white"
            :min="0"
            hide-details
          ></v-number-input>
        </div>
        <div>
          <p class="text-xs font-bold text-slate-500 mb-1 uppercase">Minimum Stock Threshold</p>
          <v-number-input
            controlVariant="split"
            v-model="props.form.minimum_stock"
            variant="outlined"
            density="comfortable"
            class="bg-white"
            :min="0"
            hide-details
          ></v-number-input>
        </div>
      </div>

      <v-textarea
        v-model="props.form.description"
        label="Product Indications & Description"
        variant="outlined"
        density="comfortable"
        class="bg-white"
        rows="8"
        hide-details
      ></v-textarea>

      <div class="border border-dashed border-slate-300 bg-white p-4 rounded-lg flex flex-col gap-2">
        <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Product Cover Image</p>
        
        <div class="flex items-center gap-4">
          <div class="w-16 h-16 rounded border bg-slate-50 flex items-center justify-center overflow-hidden shrink-0">
            <img 
              v-if="selectedFile" 
              :src="previewUrl" 
              class="w-full h-full object-cover" 
            />
            <img 
              v-else-if="props.form.image_url" 
              :src="props.form.image_url" 
              class="w-full h-full object-cover" 
            />
            <v-icon v-else color="grey-lighten-1" size="large">mdi-image-outline</v-icon>
          </div>

          <div class="flex-1">
            <input 
              type="file" 
              accept="image/*" 
              id="product-image-file-input" 
              class="hidden" 
              @change="handleFileChange" 
            />
            <label 
              for="product-image-file-input" 
              class="v-btn v-btn--density-comfortable v-btn--size-default v-theme--light v-btn--variant-tonal text-primary font-bold cursor-pointer inline-flex items-center px-4 rounded"
            >
              <v-icon class="mr-2">mdi-upload</v-icon>
              {{ props.form.image_url || selectedFile ? 'Change Image' : 'Choose Image File' }}
            </label>
            <p v-if="selectedFile" class="text-xs text-emerald-600 font-medium mt-1">Staged: {{ selectedFile.name }}</p>
          </div>
        </div>
      </div>

      <v-checkbox
        v-model="props.form.requires_prescription"
        label="This item requires a doctor prescription to buy"
        color="primary"
        hide-details
      ></v-checkbox>
    </v-card-text>
    
    <v-card-actions class="justify-end gap-2 pt-4 border-t px-8">
      <v-btn variant="text" color="slate-500" @click="emit('done')">Cancel</v-btn>
      <v-btn 
        color="primary" 
        variant="flat" 
        class="px-6"
        :disabled="!props.form.name || !props.form.sku || !props.form.category || !props.form.price"
        @click="handleSaveProduct"
      >
        {{ props.isEditing ? 'Save Product Details' : 'Register Product' }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>