<template>
  <div>
    <v-container>
      <v-btn to="wallet/op-list">
        ウォレットを追加
      </v-btn>
      <v-app-bar-title class="mb-1 font-weight-bold grey--text text--darken-2 pt-2" style="font-size: 16px">
        ウォレット
      </v-app-bar-title>
      <p class="text-center" v-if="walletJsonData.length === 0">ウォレットを所持していません</p>
      <v-card elevation="0" class="rounded-lg mb-2" v-for="value in walletJsonData" v-bind:key="value.id">
        <nuxt-link :to="`/wallet/${value.op.name}/`" class="btn btn-sm btn-success">
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="mb-1 font-weight-bold grey--text text--darken-2 pt-2 mb-6">
                {{ value.op.name }}
              </v-list-item-title>
              <div class="text-right"><span
                class="font-weight-bold indigo--text text--lighten-2 pr-1"
                style="font-size: 26px">{{ value.point }}</span><span>P</span>
              </div>
            </v-list-item-content>
          </v-list-item>
        </nuxt-link>
      </v-card>
    </v-container>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: 'ウォレット',
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
  layout:"Main",
  methods: {
    logout() {
      this.$auth.logout()
    },
  },
  async asyncData({app}) {
    const res = await app.$axios.$get('api/dejipo/user-wallet-list/');
    return {
      walletJsonData: res
    }
  },

}
</script>
<style>

</style>
