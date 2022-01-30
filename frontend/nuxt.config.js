export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,
  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    proxy: true,
  },
  proxy: {
    '/api': 'http://127.0.0.1:8000'
  },
  server: {
    port: 3000,
    host: '0.0.0.0'
  },
  router: {
    middleware: ['auth']
  },
  auth: {
    redirect: {
      login: '/login',
      logout: '/login',
      home: '/home'
    },
    localStorage: false,
    strategies: {
      local: {
        tokenType: 'JWT',
        token: {
          type: 'JWT',
          property: 'access',
        },
        user: { //追加
          property: false
        },
        endpoints: {
          login: {
            url: '/api/auth/jwt/create/',
            method: 'post',
            propertyName: 'access'
          },
          logout: {
            url: false,
          },
          user: {
            url: '/api/auth/users/me/',
            method: 'get',
            propertyName: 'access'
          }
        }
      },
    },
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - DEJIPO',
    htmlAttrs: {
      lang: 'ja'
    },
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1'},
      {hid: 'description', name: 'description', content: ''},
      {name: 'format-detection', content: 'telephone=no'}
    ],
    link: [
      {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'}
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ['~/plugins/qrReader', '~/plugins/qrCode', '@/plugins/axios', {
    src: '~/plugins/infiniteloading',
    ssr: false
  }],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
    '@nuxtjs/moment'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    'vue-sweetalert2/nuxt'
  ],


  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      themes: {
        light: {
          background: "#efefef"
        }
      }
    }
  },
  moment: {
    // ここにオプションが記述できる
    locales: ['ja']
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {}
}
