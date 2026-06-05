import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCheckoutStore = defineStore('checkout', () => {
  const checkoutItems = ref({})
  const checkoutItemids = ref([])

  const totalItemsCount = computed(() => checkoutItems.value.length)
  
  const itemsSubtotal = computed(() => {
    return checkoutItems.value.reduce((sum, item) => {
      const price = item.product?.price || 0
      const qty = item.quantity || 0
      return sum + (price * qty)
    }, 0)
  })

  function setCheckoutItems(items) {
    checkoutItems.value = items
  }
  function setCheckoutItemids(items) {
    checkoutItemids.value = items
  }

  function clearStore() {
    checkoutItems.value = []
  }

  return {
    checkoutItems,
    checkoutItemids,
    totalItemsCount,
    itemsSubtotal,
    setCheckoutItems,
    setCheckoutItemids,
    clearStore
  }
})