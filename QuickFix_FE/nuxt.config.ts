// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ["~/assets/css/main.css"],
  modules: [
    "vuetify-nuxt-module",
    "@pinia/nuxt",
    "pinia-plugin-persistedstate/nuxt",
    "nuxt-qrcode",
  ],
  runtimeConfig: {
    public: {
      apiBaseUrl: "",
      actUrl: "",
    },
  },
  vuetify: {
    moduleOptions: {
      styles: true,
    },
    vuetifyOptions: "vuetify.config.ts",
  },
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: {
      include: [
        "@vue/devtools-core",
        "@vue/devtools-kit",
        "lodash.debounce", // CJS
        "vue-qrcode-reader",
      ],
    },
  },
});
