<script setup>

const props = defineProps({
  item: {
    type: Object
  }
})

</script>

<template>
  <div class="w-full! bg-c-tertiary p-4 rounded-lg border-c-neutral">
    <div class="w-full! flex justify-between">
      <div class="flex gap-4">
        <div>
          <v-img :src="item.product?.image_url ?? '/drugsingle.png'" class="rounded-lg" width="73"></v-img>
        </div>
        <p class="text-xl whitespace-pre-line wrap-break-word text-justify leading-relaxed">{{
          `${item.product?.generic_name} (${item.product?.name})` }}</p>
      </div>
      <div>
        <p class=" font-light mb-1 text-end">{{item.quantity}} x {{ Number(item.product?.price)?.toLocaleString('id-ID', {
          style: 'currency', currency: 'IDR',
          trailingZeroDisplay: 'stripIfInteger'
        }) }}</p>
      </div>
    </div>
  </div>
</template>