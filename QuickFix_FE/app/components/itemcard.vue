<script setup>

const props = defineProps({
  obj: {
    type: Object
  },
  cart: {
    type: Boolean
  }
})

</script>

<template>
  <nuxt-link :to="`shop/item/${props.obj?.id}`">
    <div class="bg-white rounded-lg h-fit flex-1 min-w-60 max-w-full sm:max-w-[calc(50%-12px)] md:max-w-[calc(33.33%-16px)] lg:max-w-[calc(25%-18px)] border-c-tertiary border">
      <div class=" relative">
        <v-chip v-if="props.obj.requires_prescription" class="position-absolute top-0 left-0 m-2 z-10 text-white"
          color="primary" variant="elevated" density="compact">Require Prescription</v-chip>
        <v-img :src="props.obj?.image_url ?? '/drugsingle.png'" class="rounded-lg"></v-img>
      </div>
      <div class="p-4">
        <p class=" text-lg font-semibold">{{ props.obj?.generic_name }}</p>
        <p class=" text-sm font-light">{{ props.obj?.category_name }}</p>
        <div class="flex justify-between mt-3 items-center">
          <p class=" text-c-primary">{{ Number(props.obj.price)?.toLocaleString('id-ID', {
            style: 'currency', currency: 'IDR',
            trailingZeroDisplay: 'stripIfInteger'
          }) }}</p>
        </div>
      </div>
    </div>
  </nuxt-link>
</template>