// stores/auth.js
import { defineStore } from "pinia";
export const useAuthStore = defineStore("auth", {
  state: () => ({
    role: null,
    username: null,
    userid: null,
    error: ref(null),
    isLoggedIn: false
  }),
  // persist: true,
  persist: {
    storage: piniaPluginPersistedstate.cookies(),
  },
  actions: {
    async login(username, password) {
      const config = useRuntimeConfig();
      try {
        const response = await $fetch(
          `${config.public.apiBaseUrl}usermng/login`,
          {
            method: "POST",
            body: { username, password },
            credentials: 'include',
          },
        );
        this.role = response.role;
        this.userid = response.userid;
        this.username = response.username;
        this.isLoggedIn = true;
        this.error = null;
        return true;
      } catch (error) {
        this.error = error.data.detail;
        return false;
      }
    },
    async signup(username, email, password, repassword, details) {
      const config = useRuntimeConfig();
      try {
        console.log(details)
        const payload = {
          username: username,
          email: email,
          password: password,
          repassword: repassword,

          fullname: details.fullname,
          dob: details.dob,
          gender: details.gender, 
          number: details.number,
        };
        const response = await $fetch(
          `${config.public.apiBaseUrl}usermng/signup`,
          { method: "POST", body: payload, credentials: 'include' },
        );
        return "success";
      } catch (error) {
        this.error = error;
        console.log(this.error);
        return this.error;
      }
    },

    logout() {
      this.role = null;
      this.userid = null;
      this.username = null;
      this.isLoggedIn = false

      const authCookie = useCookie("auth");
      authCookie.value = null;
    },
  },
});
