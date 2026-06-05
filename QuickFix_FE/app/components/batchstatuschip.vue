<script setup>
const props = defineProps({
  current: {
    type: Number,
  },
  minimum: {
    type: Number,
    default:0
  }
})

</script>

<template>
  <v-chip v-if="props.current === 0" color="red-darken-4" text-color="white" size="small" variant="outlined"
    class="font-weight-bold text-uppercase">
    OUT OF STOCK
  </v-chip>

  <v-chip v-else-if="props.current <= props.minimum" color="red-accent-2" text-color="white"
    size="small" variant="outlined" class="font-weight-bold text-uppercase">
    LOW STOCK
  </v-chip>

  <v-chip v-else color="primary" class="font-weight-bold text-uppercase" size="small"
    variant="outlined">
    IN STOCK
  </v-chip>
</template>