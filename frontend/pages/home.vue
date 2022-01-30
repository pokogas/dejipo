<!--eslint-disable-->
<template>
  <div>
    <v-container>
      <v-card elevation="0" class="rounded-lg mb-2">
        <v-list-item three-line>
          <v-list-item-content>
            <v-list-item-title class="mb-1 font-weight-bold grey--text text--darken-2 pt-2">
              合計所持ポイント
            </v-list-item-title>
            <div class="text-right"><span
              class="font-weight-bold indigo--text text--lighten-2 pr-1"
              style="font-size: 26px">{{ totalPoint }}</span><span>P</span>
              <p class="pt-1" style="font-size: 14px; color: #676767">円換算 ¥{{ yenConversion }}</p>
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-card>
      <v-app-bar-title class="mb-1 font-weight-bold grey--text text--darken-2 pt-2" style="font-size: 16px">
        タイムライン
      </v-app-bar-title>
      <v-card elevation="0" class="rounded-lg py-4 overflow-auto" height="500">
        <v-container>
          <p v-if="timeLineData.length === 0" class="text-center orange--text">まだ取引がありません。</p>
          <v-list two-line>
            <div v-for="value in timeLineData" v-bind:key="value.id">
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>{{ value.op.name }}</v-list-item-title>
                  <v-list-item-subtitle>{{ $moment(value.trading_time).format('YYYY/MM/DD HH:mm') }}
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action v-if="value.use_usage === 2" class="green--text">+{{ value.point }} P
                </v-list-item-action>
                <v-list-item-action v-if="value.use_usage === 1" class="red--text">-{{ value.point }} P
                </v-list-item-action>
              </v-list-item>
              <v-divider></v-divider>
            </div>
          </v-list>
        </v-container>
      </v-card>
    </v-container>
  </div>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>
export default {
  head() {
    return {
      title: 'ホーム',
    }
  },
  data() {
    return {
      totalPoint: 0
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
  methods: {
    logout() {
      this.$auth.logout()
    },
  },
  created() {
  },
  layout: "Main",
  async asyncData({app}) {
    const walletListRes = await app.$axios.$get('api/dejipo/user-wallet-list/');
    let point = 0;
    let yenConversion = 0;
    for (const i in walletListRes) {
      point += walletListRes[i].point
    }
    for (const i in walletListRes) {
      yenConversion += walletListRes[i].point * walletListRes[i].op.cost
    }

    const transactionRes = await app.$axios.$get('api/transaction/user-transaction-list/');

    return {
      totalPoint: point,
      timeLineData: transactionRes.results,
      yenConversion: yenConversion
    }
  },
}
</script>
<!--eslint-disable-->
