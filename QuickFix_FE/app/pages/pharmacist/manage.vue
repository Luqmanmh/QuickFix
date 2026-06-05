<script setup>
useHead({
  title: 'Manage Items'
})
definePageMeta({
  middleware: 'authmid',
  role: ['pharmacist', 'admin'],
  layout: 'back'
})
import debounce from 'lodash.debounce';
const route = useRoute()
const api = useApi()
const isloading = ref(true)
const item_list = ref()
const supplier_list = ref()
const category_list = ref()

// Fixed from previous object structural mapping update
const query = ref({
  quest: '',
  category_list: [],
})
const page_len = ref(5)
const page = ref(1)

// batch edit stuff
const isBatchModalOpen = ref(false)
const isBatchEditing = ref(false)
const defaultBatchForm = {
  id: null,
  product_id: null,
  batch_number: '',
  supplier: null, 
  expiry_date: '',
  stock_qty: 1
}
const batchForm = ref({ ...defaultBatchForm })
const openBatchAddModal = (productId) => {
  isBatchEditing.value = false
  batchForm.value = { ...defaultBatchForm, product_id: productId }
  isBatchModalOpen.value = true
}
const openBatchEditModal = (productId, batchObj) => {
  isBatchEditing.value = true
  batchForm.value = {
    id: batchObj.id,
    product_id: productId,
    batch_number: batchObj.batch_number,
    supplier: batchObj.supplier_id,
    expiry_date: batchObj.expiry_date,
    stock_qty: batchObj.stock_qty
  }
  isBatchModalOpen.value = true
}

// product edit stuff 
const isProductModalOpen = ref(false)
const isProductEditing = ref(false)
const defaultProductForm = {
  id: null,
  sku: '',
  name: '',
  generic_name: '',
  category: null,
  dosage_form: '',
  strength: '',
  price: 0,
  minimum_stock: 5,
  description: '',
  requires_prescription: false,
  image_url: null
}
const productForm = ref({ ...defaultProductForm })
const openProductAddModal = () => {
  isProductEditing.value = false
  productForm.value = { ...defaultProductForm }
  isProductModalOpen.value = true
}
const openProductEditModal = (itemObj) => {
  isProductEditing.value = true
  productForm.value = {
    id: itemObj.id,
    sku: itemObj.sku,
    name: itemObj.name,
    generic_name: itemObj.generic_name,
    category:  itemObj.category,
    dosage_form: itemObj.dosage_form,
    strength: itemObj.strength,
    price: itemObj.price,
    minimum_stock: itemObj.minimum_stock,
    description: itemObj.description,
    requires_prescription: itemObj.requires_prescription,
    image_url: itemObj.image_url
  }
  isProductModalOpen.value = true
}

const handleDone = async() =>{
  isBatchModalOpen.value = false
  isProductModalOpen.value = false
  await fetchItem()
}

const fetchItem = async () => {
  let error = false
  try {
    isloading.value = true
    item_list.value = await api(`manage/list`, {
      method: 'GET', query: {
        query: query.value?.quest, // Fixed matching key mapping name typo 'quedt'
        category: query.value?.category_list,
        page_len: page_len.value,
        page: page.value
      }
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
const handleAmount = debounce(async (id, amt) => {
  let error = false
  try {
    isloading.value = true
    let response = await api(`batch/action`, {
        method: 'PUT',
        query:{
          id: id,
          stock_qty:amt,
          type: "ADJUSTMENT"
        }
      })
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      isloading.value = false
    }
  }
}, 800)
const handleProdDelete = async (id, number) => {
  let error = false
  const confirm = window.confirm(
    `are you sure to delete Product ${number}`
  )
  if (!confirm){
    return
  }
  try {
    isloading.value = true
    let response = await api(`product/action`, {
        method: 'DELETE',
        query:{
          id: id,
        }
      })
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      isloading.value = false
      fetchItem()
    }
  }
}
const handleProdactivate = async (id, value) => {
  let error = false
  
  try {
    isloading.value = true
    let response = await api(`product/activate`, {
        method: 'PUT',
        query:{
          id: id,
          is_active:value
        }
      })
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      isloading.value = false
      fetchItem()
    }
  }
}
const handleBatchDelete = async (id, number) => {
  let error = false
  const confirm = window.confirm(
    `are you sure to delete batch ${number}`
  )
  if (!confirm){
    return
  }
  try {
    isloading.value = true
    let response = await api(`batch/action`, {
        method: 'DELETE',
        query:{
          id: id,
        }
      })
  } catch (err) {
    console.log('error getting items', err)
    error = true
  } finally {
    if (!error) {
      isloading.value = false
      fetchItem()
    }
  }
}
const fetchSupplier = async () => {
  let error = false
  try {
    isloading.value = true
    supplier_list.value = await api(`supplier/list`, {
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
const fetchCategories = async () => {
  let error = false
  try {
    isloading.value = true
    category_list.value = await api(`category/list`, {
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

const handleQuerying = async (data) => {
  query.value.quest = data.query
  query.value.category_list = data.category_picks
  await fetchItem()
}


onMounted(async () => {
  await Promise.all([
    fetchItem(),
    fetchSupplier(),
    fetchCategories(),
  ])
})
</script>

<template>
  <main class="w-full flex flex-col p-6 md:p-10 gap-6 mt-14">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-semibold text-slate-800">Pharmacy Inventory</h1>
      <v-btn color="primary" prepend-icon="mdi mdi-file-pdf-box" variant="outlined" disabled> Download Report</v-btn>
    </div>
    <div>
      <Itemsearch :category_list="category_list" @querys="handleQuerying" class="bg-c-tertiary p-2 rounded-lg border"/>
    </div>
    <div class="w-full flex justify-between">
      <div>
        <v-btn color="primary" prepend-icon="mdi mdi-upload" class="me-5" disabled> Upload Bulk</v-btn>
      </div>
      <div class="flex w-1/3 justify-end gap-4">
        <v-btn color="primary" prepend-icon="mdi mdi-plus" disabled> Add Category</v-btn>
        <v-btn color="primary" prepend-icon="mdi mdi-plus" @click="openProductAddModal()"> Add Product</v-btn>
      </div>
    </div>
    
    <div class="w-full bg-white rounded-lg border shadow-sm overflow-hidden">
      <div class="grid grid-cols-12 gap-4 items-center w-full px-6 py-3 bg-c-tertiary border-b font-semibold text-sm text-c-primary">
        <div class="col-span-2"><p>SKU ID</p></div>
        <div class="col-span-2"><p>Item Name</p></div>
        <div class="col-span-2"><p>Generic Name</p></div>
        <div class="col-span-2"><p>Category</p></div>
        <div class="col-span-1"><p>Price</p></div>
        <div class="col-span-1"><p>Strength</p></div>
        <div class="col-span-1"><p>Active Status</p></div>
        <div class="col-span-1 text-right"><p class="pr-6">Actions</p></div>
      </div>

      <div class="flex flex-col w-full divide-y">
        <div v-for="(item, index) in item_list?.data" :key="item.id" class="w-full">
          
          <v-expansion-panels variant="accordion" flat>
            <v-expansion-panel class="bg-transparent">
              
              <template v-slot:title>
                <div class="grid grid-cols-12 gap-4 items-center w-full text text-slate-700 py-1">
                  <div class="col-span-2 font-mono text-slate-500"><p>{{ item?.sku }}</p></div>
                  <div class="col-span-2 font-medium"><p>{{ item?.name }}</p></div>
                  <div class="col-span-2 text-slate-500"><p>{{ item?.generic_name }}</p></div>
                  <div class="col-span-2">
                    <v-chip size="small" variant="tonal" color="primary">{{ item?.category_name }}</v-chip>
                  </div>
                  <div class="col-span-1 font-semibold">
                    <p>{{ Number(item?.price)?.toLocaleString('id-ID', { style: 'currency', currency: 'IDR', trailingZeroDisplay: 'stripIfInteger' }) }}</p>
                  </div>
                  <div class="col-span-1 text-center"><p>{{ item?.strength || '-' }}</p></div>
                  <div class="col-span-1 text-center flex items-center justify-center" @click.stop>
                    <v-switch
                      v-model="item.is_active"
                      hide-details
                      inset="material"
                      size="small"
                      color="primary"
                      true-icon ="mdi mdi-check"
                      false-icon ="mdi mdi-close"
                      @update:model-value="handleProdactivate(item.id, item.is_active)"
                    ></v-switch>
                  </div>
                  <div class="col-span-1 text-right flex items-center justify-end" @click.stop>
                    <v-btn size="small" variant="text" color="primary" icon="mdi-pencil" @click="openProductEditModal(item)"></v-btn>
                    <v-btn size="small" variant="text" color="error" icon="mdi-delete" @click="handleProdDelete(item?.id, item?.sku)"></v-btn>
                  </div>
                </div>
              </template>

              <template v-slot:text>
                <div class="bg-c-neutral rounded-lg p-4 border border-slate-200 my-2 ml-4 mr-8">
                  <div class="flex justify-between items-center mb-2">
                    <h3 class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Available Stock Batches</h3>
                    <v-btn size="x-small" color="primary" prepend-icon="mdi-plus" class="font-bold" @click="openBatchAddModal(item.id)">
                        Add New Batch
                    </v-btn>
                  </div>
                  
                  <div class="grid grid-cols-12 gap-4 items-center w-full py-2 font-semibold text-sm text-c-primary border-b">
                    <div class="col-span-2"><p>Batch Number</p></div>
                    <div class="col-span-2"><p>Supplier</p></div>
                    <div class="col-span-1"><p>Expiry Date</p></div>
                    <div class="col-span-3"><p>Quantity Stock</p></div>
                    <div class="col-span-1"><p>Stock Status</p></div>
                    <div class="col-span-3 text-right"><p>Batch Actions</p></div>
                  </div>

                  <div v-if="item?.batches?.length" v-for="(batch, idx) in item?.batches" :key="idx" 
                       class="grid grid-cols-12 gap-4 items-center w-full py-3 text-sm text-slate-600 border-b last:border-0 hover:bg-slate-100/50 px-1 transition-colors">
                    <div class="col-span-2 font-mono text-slate-700"><p>{{ batch?.batch_number }}</p></div>
                    <div class="col-span-2"><p>{{ batch?.supplier_name }}</p></div>
                    <div class="col-span-1">
                      <p :class="new Date(batch?.expiry_date) < new Date() ? 'text-rose-500 font-semibold' : ''">
                        {{ new Date(batch?.expiry_date).toLocaleDateString('en-GB') }}
                      </p>
                    </div>
                    <div class="col-span-3">
                      <v-number-input 
                        controlVariant="stacked" 
                        v-model="batch.stock_qty"
                        @update:model-value="handleAmount(batch.id, batch.stock_qty)"
                        variant="outlined" 
                        density="compact" 
                        :min="0" 
                        hide-details 
                        class="w-32 bg-white"
                      ></v-number-input>
                    </div>
                    <div class="col-span-1 text-right">
                      <Batchstatuschip :current="batch.stock_qty" :minimum="item.minimum_stock"/>
                    </div>
                    <div class="col-span-3 text-right">
                      <v-btn size="x-small" color="primary" variant="tonal" class="font-bold mr-2" @click="openBatchEditModal(item.id, batch)">
                        Edit
                      </v-btn>
                      <v-btn size="x-small" color="red" variant="tonal" class="font-bold mr-2" @click="handleBatchDelete(batch.id, batch.batch_number)">
                        delete
                      </v-btn>
                    </div>
                  </div>
                  
                  <div v-else class="text-center py-4 text-sm text-slate-400 italic">
                    No active stock batches found for this medical item profile.
                  </div>
                </div>
              </template>

            </v-expansion-panel>
          </v-expansion-panels>

        </div>
        <v-pagination :length="item_list?.pagin?.total_page" active-color="primary" v-model="page"
              :total-visible="5" @update:model-value="fetchItem()">
        </v-pagination>
      </div>

    </div>

    <v-dialog v-model="isBatchModalOpen" max-width="500px" persistent>
      <Batchedit :form="batchForm" :is-editing="isBatchEditing" :supplier="supplier_list" @done="handleDone()"/>
    </v-dialog>

    <v-dialog v-model="isProductModalOpen" max-width="650px" persistent>
      <Productedit 
        :form="productForm" 
        :is-editing="isProductEditing" 
        :categories="category_list" 
        @done="handleDone()"
      />
    </v-dialog>
  </main>
</template>

<style scoped>
/* twins */
:deep(.v-expansion-panel-title) {
  padding-left: 1.5rem !important;
  padding-right: 1.5rem !important;
  min-height: 52px !important;
}
:deep(.v-expansion-panel-text__wrapper) {
  padding: 0 !important;
}
</style>