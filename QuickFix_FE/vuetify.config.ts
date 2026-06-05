import { defineVuetifyConfiguration } from 'vuetify-nuxt-module/custom-configuration'

export default defineVuetifyConfiguration({
  icons: {
    defaultSet: 'mdi',
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#007979',
          secondary: '#98eff1',
          tertiary : '#fdf1e7',
          neutral: '#FFF0E4'
        }
      }
    }
  }
})