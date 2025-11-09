// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,

  css: ['assets/main.css'],
  modules: [
    '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui'
  ],
  nitro: {
    routeRules: {
      '/jsalchemy/**': {
        proxy: 'http://localhost:4000/jsalchemy/**',
        ssr: false,
      },
      '/auth/**': {
        proxy: 'http://localhost:4000/auth/**',
        ssr: false,
      }
    }
  },

})