<template>
  <div class="verification-container">
    <h2>Email Verification</h2>
    <p v-if="loading">Validating your link, please wait...</p>
    <div v-else-if="error" class="error-box">
      {{ error }}
    </div>
    <div v-else class="success-box">
      <p>Account verified successfully! Redirecting you to your dashboard...</p>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth';
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const api = useApi();

const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  const uid = route.query.uid;
  const token = route.query.token;

  if (!uid || !token) {
    error.value = "Invalid or incomplete verification link.";
    loading.value = false;
    return;
  }

  try {
    // Send payload to Django
    const data = await api('usermng/verify-email/', {
      method: 'POST',
      body: { uid, token }
    });

    console.log(data)

    // Send user into dashboard after 3 seconds
    setTimeout(() => {
      router.push("/shop?message='your account is active please login'");
    }, 3000);

  } catch (err) {
    console.log("Full Django Error Payload:", err.response?._data);
    error.value = err.response?._data?.err || "Verification failed. The link may have expired.";
  } finally {
    loading.value = false;
  }
});
</script>