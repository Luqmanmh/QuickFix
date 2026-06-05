<script setup>
const props = defineProps({
  form :{
    type: Object
  },
  isEditing:{
    type: Boolean
  },
  supplier:{
    type : Object
  }
})
import { triggerSnackbar } from '#imports'
const emit = defineEmits(['done'])
const isloading = ref(true)
const api = useApi()


const handleSaveBatch = async () => {
  try {
    isloading.value = true
    
    if (props.isEditing) {
      await api(`batch/action`, {
        method: 'PUT',
        query:{
          ...props.form,
          type: "ADJUSTMENT"
        }
      })
    } else {

      await api(`batch/action`, {
        method: 'POST',
        body: props.form
      })
    }
    
    emit('done')
  } catch (err) {
    console.error('Error saving batch transaction:', err)
  } finally {
    isloading.value = false
    triggerSnackbar('Batch Edited', 'primary')
  }
}
</script>

<template>
  <v-card class="p-4 rounded-lg" color="neutral">
    <v-card-title class="text-xl font-bold text-slate-800 border-b pa-4">
      {{ isEditing ? 'Edit Stock Batch' : 'Add New Stock Batch' }}
    </v-card-title>

    <v-card-text class="pt-4 px-8 flex flex-col gap-4">
      <v-text-field
        v-model="props.form.batch_number"
        color="white"
        class="bg-white"
        label="Batch Number / Code"
        variant="outlined"
        density="comfortable"
        placeholder="e.g., BCH-2026-001"
        hide-details
      ></v-text-field>

      <v-autocomplete
        v-model="props.form.supplier"
        color="white"
        class="bg-white"
        :items="supplier"
        item-title="name"
        item-value="id"
        label="Select Supplier Warehouse"
        variant="outlined"
        density="comfortable"
        hide-details
      ></v-autocomplete>

      <v-text-field
        v-model="props.form.expiry_date"
        class="bg-white"
        type="date"
        label="Expiration Date"
        variant="outlined"
        density="comfortable"
        hide-details
        persistent-placeholder
      ></v-text-field>

      <div>
        <p class="text-xs font-bold text-slate-500 mb-1 uppercase tracking-wide">Initial Inventory Stock Qty</p>
        <v-number-input
          controlVariant="split"
          v-model="props.form.stock_qty"
          variant="outlined"
          density="comfortable"
          :min="0"
          hide-details
          class="w-full bg-white"
        ></v-number-input>
      </div>
    </v-card-text>

    <v-card-actions class="justify-end gap-2 pt-4 border-t">
      <v-btn variant="text" color="slate-500" @click="emit('done')">Cancel</v-btn>
      <v-btn 
        color="primary" 
        variant="flat" 
        class="px-4"
        :disabled="!props.form.batch_number || !props.form.supplier || !props.form.expiry_date"
        @click="handleSaveBatch"
      >
        {{ isEditing ? 'Save Changes' : 'Register Batch' }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>