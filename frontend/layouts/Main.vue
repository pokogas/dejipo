<!--eslint-disable-->
<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <div>
      <Header/>
      <Nuxt/>
      <Footer/>
    </div>
  </v-app>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>
export default {
  name:"Main",
  data: () => ({value: 3}),
  computed: {
    auth() {
      return this.$auth
    },
    user() {
      return this.$auth.user;
    }
  },
  methods: {
    logout() {
      return this.$auth.logout()
    },
  }
}

</script>
<!--eslint-disable-->
<style>
a {
  text-decoration: none;
}
</style>
