<!--eslint-disable-->
<template>
  <v-toolbar
    flat
    color="#7886FF">
    <v-toolbar-title class="align-self-center">
      <span class="white--text">
        DEJIPO
      </span>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items
      v-if="auth.loggedIn">
      <v-menu
        transition="slide-y-transition"
        bottom
        offset-y
        z-index="99999">
        <template v-slot:activator="{ on, attrs }">
          <v-avatar
            v-bind="attrs"
            v-on="on"
            color="primary"
            size="40"
            class="align-self-center">
            <img
              src="https://cdn.pixabay.com/photo/2018/05/26/18/06/dog-3431913_960_720.jpg"
              alt="user-icon">
          </v-avatar>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-avatar>
              <img alt="user-icon"
                   src="https://cdn.pixabay.com/photo/2018/05/26/18/06/dog-3431913_960_720.jpg">
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="font-weight-bold">{{ user.name }}</v-list-item-title>
              <v-list-item-subtitle class="font-weight-light">{{ user.email }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-list>
          <v-list-item-group>
            <nuxt-link to="/management">
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-dev-to</v-icon>
                </v-list-item-icon>
                <v-list-item-title class="font-weight-bold">マネジメント
                </v-list-item-title>
              </v-list-item>
            </nuxt-link>
            <v-divider></v-divider>
            <v-list-item @click="logout">
              <v-list-item-icon>
                <v-icon>mdi-logout</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="font-weight-bold">ログアウト</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>
    </v-toolbar-items>
  </v-toolbar>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>
export default {
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

<style scoped>
a {
  text-decoration: none;
}
</style>
