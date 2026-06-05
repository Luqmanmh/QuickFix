import { useAuthStore } from '~/stores/auth';

export const useApi = () => {
  const authStore = useAuthStore();
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBaseUrl;

  const api = $fetch.create({
    baseURL,
    credentials: 'include', 
    mode:'cors',

    onRequest({ request, options }) {},

    async onResponseError({ request, response, options }) {
      
      if (response.status === 401) {      
        try {
          await $fetch(`${baseURL}usermng/refresh`, {
            method: 'POST',
            credentials: 'include',
          });
          return api(request, options);

        } catch (e) {
          console.error("Failed to refresh token:", e); 
          // authStore.logout(); 
          return Promise.reject(e);
        }
      }
    }
  });

  return api;
};