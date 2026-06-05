import { reactive } from 'vue'

export const snackbarStore = reactive({
  show: false,
  message: '',
  color: 'success' // success, error, secondary, etc.
})

export function triggerSnackbar(message, color = 'success') {
  snackbarStore.message = message
  snackbarStore.color = color
  snackbarStore.show = true
}