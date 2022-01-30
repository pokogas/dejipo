<!--eslint-disable-->
<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <div>
      <v-navigation-drawer
        v-model="drawer"
        app>
        <v-container>
          <nuxt-link to="/management">
            <span>TOPへ戻る</span>
          </nuxt-link>
        </v-container>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>
              <strong style="font-size: 18px">{{ this.$route.params.opName }}</strong>
              <v-list-item-subtitle class="ml-2">管理ページ</v-list-item-subtitle>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list
          nav
          dense>
          <v-list nav dense>
            <v-list-item-group
              color="#7886FF"
              v-for="nav_list in nav_lists"
              :key="nav_list.name">
              <v-list-item :to="nav_list.link" exact>
                <v-list-item-icon>
                  <v-icon>{{ nav_list.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title class="font-weight-bold">{{ nav_list.name }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-list>
      </v-navigation-drawer>
      <v-app-bar app elevation="0" color="#7886FF">
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        <v-toolbar-title class="align-self-center">
          <nuxt-link to="/management" class="white--text">
            DEJIPO <span style="font-size: 16px">Management</span>
          </nuxt-link>
        </v-toolbar-title>
      </v-app-bar>
      <v-main>
        <Nuxt/>
      </v-main>
    </div>
  </v-app>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>
export default {
  data() {
    return {
      drawer: null,
      nav_lists: [
        {
          name: "ホーム",
          icon: "mdi-home",
          link: `/management/${this.$route.params.opName}`,
        },
        {
          name: "トランザクション",
          icon: "mdi-circle-multiple",
          link: `/management/${this.$route.params.opName}/transaction`,
        },
        {
          name: "ユーザー管理",
          icon: "mdi-account",
          link: `/management/${this.$route.params.opName}/user`,
        },
        {
          name: "設定",
          icon: "mdi-cog-outline",
          link: `/management/${this.$route.params.opName}/setting`,
        },
      ],
    }
  }
}
</script>
<!--eslint-disable-->
<style scoped>

</style>
