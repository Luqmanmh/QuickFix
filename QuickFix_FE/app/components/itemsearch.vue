<script setup>
import debounce from 'lodash.debounce';
const api = useApi()
const isloading = ref(true)
const props = defineProps({
  category_list:{
    type:Object
  }
})


const query = ref('')
const category_picks = ref([])
const emit = defineEmits(['querys'])

const handleBounce = debounce(() => {
  defQuerys()
}, 500)

const defQuerys = () => {
  emit('querys', {
    query:query.value,
    category_picks:category_picks.value
  })
}

</script>

<template>
  <v-row class="">
    <v-col cols="6">
      <div>
        <v-text-field label="Search Name or Generic Name" type="text" autocomplete="false" v-model="query" variant="outlined"
          density="comfortable" hide-details clearable @update:model-value="handleBounce"/>
      </div>
    </v-col>
    <v-col cols="4">
      <div>
        <v-autocomplete clearable chips label="Category" :items="props.category_list" multiple v-model="category_picks"
           item-title="name" item-value="id" density="comfortable" hide-details autocomplete="false"
           @update:model-value="handleBounce"
          variant="outlined"></v-autocomplete>
      </div>
    </v-col>
    <v-col cols="2" class="align-content-center">
      <div class=" w-full mx-auto flex justify-end">
        <v-btn
        color="primary"
        size="large"
        class="px-6 mx-auto"
        @click="defQuerys()"
        >
        <v-icon>mdi mdi-magnify</v-icon>
        Search</v-btn>
      </div>
    </v-col>
  </v-row>
</template>