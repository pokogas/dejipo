<!--eslint-disable-->
<template>
  <v-bottom-navigation
    v-model="value"
    dark
    grow
    shift
    fixed
    v-if="auth.loggedIn">
    <v-btn to="/home">
      <span>ホーム</span>
      <v-icon>mdi-home</v-icon>
    </v-btn>
    <v-btn to="/wallet">
      <span>ウォレット</span>
      <v-icon>mdi-wallet</v-icon>
    </v-btn>
    <v-btn to="/read">
      <span>読み取り</span>
      <v-icon>mdi-qrcode-scan</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>
export default {
  data: () => ({value: 0}),
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
<style scoped>
a {
  text-decoration: none;
}

.v-bottom-navigation--fixed {
  position: fixed !important;
}

.v-item-group.v-bottom-navigation .v-btn {
  height: inherit !important;
  background-color: #2e2e2e;
}
</style>
