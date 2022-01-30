<!--eslint-disable-->
<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <div>
      <Nuxt/>

    </div>
  </v-app>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>
export default {
  computed: {
    auth() {
      return this.$auth
    },
    user() {
      return this.$auth.user;
    },
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
