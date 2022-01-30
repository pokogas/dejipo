<!--eslint-disable-->
<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <v-container>
      <div style="max-width:500px" class="mx-auto">
        <p class="font-weight-bold" style="font-size: 60px ; color: #7886FF">404ページ</p>
      </div>
      <v-card max-width="500px" class="mx-auto">
        <v-card-title>
          お探しのページは見つかりませんでした。
        </v-card-title>
        <v-card-subtitle>
          <nuxt-link to="/home">ホームに戻る</nuxt-link>
        </v-card-subtitle>
      </v-card>
    </v-container>
  </v-app>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>
export default {}
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
<!--eslint-disable-->
