<!--eslint-disable-->
<template>
  <div style="margin-bottom: 100px">
    <v-container>
      <div v-if="wallet">
        <v-card elevation="0" class="rounded-lg mb-2">
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="font-weight-bold grey--text text--darken-2">
                合計所持ポイント
              </v-list-item-title>
              <div class="text-right">
              <span class="font-weight-bold indigo--text text--lighten-2 pr-1"
                    style="font-size: 26px">{{ walletDetailData.point }}</span><span>P</span>
                <p class="pt-1" style="font-size: 14px; color: #676767">円換算
                  ¥{{ walletDetailData.point * walletDetailData.op.cost }}</p>
              </div>
              <v-list-item-title class="font-weight-bold grey--text text--darken-2">
                累計獲得ポイント
              </v-list-item-title>
              <div class="text-right"><span
                class="font-weight-bold indigo--text text--lighten-2 pr-1"
                style="font-size: 26px">{{ walletDetailData.total_get_point }}</span><span>P</span>
                <p class="pt-1" style="font-size: 14px; color: #676767">円換算
                  ¥{{ walletDetailData.total_get_point * walletDetailData.op.cost }}</p>
              </div>
            </v-list-item-content>
          </v-list-item>
        </v-card>
        <v-card class="rounded-lg toc-view mb-2" id="gallery">
          <v-tabs
            fixed-tabs
            v-model="tab">
            <v-tab href="#top">トップ</v-tab>
            <v-tab href="#trading_history">取引履歴</v-tab>
          </v-tabs>
        </v-card>
        <div>
          <v-tabs-items v-model="tab" class="transparent-body">
            <v-tab-item value="top">
              <div style="margin-bottom: 1000px">
                <p class="text-center">トップ</p>
                <p></p>
              </div>
            </v-tab-item>
            <v-tab-item value="trading_history">
              <div class="infinite-scroll">
                <v-card elevation="0" class="rounded-lg py-4 overflow-auto" height="500">
                  <p class="text-center orange--text" v-if="transaction">まだ取引がありません。</p>
                  <v-list two-line>
                    <div v-for="value in transactionList" v-bind:key="value.id">
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title v-if="value.use_usage === 2">付与</v-list-item-title>
                          <v-list-item-title v-if="value.use_usage === 1">使用</v-list-item-title>
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
                  <infinite-loading
                    ref="infiniteLoading"
                    spinner="spiral"
                    @infinite="infiniteHandler">
                    <div slot="no-more">以上</div>
                    <div slot="no-results"/>
                  </infinite-loading>
                </v-card>
              </div>
            </v-tab-item>
          </v-tabs-items>
        </div>
      </div>
      <div v-else>
        ウォレットを所持していません
      </div>
    </v-container>
  </div>
</template>
<!--eslint-disable-->
<script>


export default {
  layout: "Main",
  head() {
    return {
      title: this.$route.params.opName,
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
  data() {
    return {
      tab: 'tab',
      transaction: false,
      transactionData: null,
      next: null,
      transactionList: [],
    }
  },
  methods: {
    logout() {
      this.$auth.logout()
    },
    infiniteHandler() {
      if (this.next === null || this.next === undefined) {
        return this.$refs.infiniteLoading.stateChanger.complete()
      } else {
        setTimeout(() => {
          this.$axios.$get(this.next).then(function (res) {
            this.transactionData = res
            this.next = this.next = this.urlConversion(res.next)
            for (let i in res.results)
              this.transactionList.push(res.results[i])
          }.bind(this));
          this.$refs.infiniteLoading.stateChanger.loaded()
        }, 800)
      }
    },
    async setData() {
      let params = this.$route.params.opName
      await this.$axios.$get(`api/transaction/transaction-each-wallet-list/?op_name=${params}`).then(function (res) {
        this.transactionData = res
        this.next = this.urlConversion(res.next)
      }.bind(this));
      if (this.transactionData.results.length < 1) {
        this.transaction = true
      }
      for (let i in this.transactionData.results)
        this.transactionList.push(this.transactionData.results[i])
    },
    urlConversion(url) {
      if (url === null || url === undefined) {
        return null
      }
      let param = url.split("/")[6]
      return `api/transaction/transaction-each-wallet-list/${param}`
    },
  },
  created() {
    this.setData()
  },
  async asyncData({app, params}) {
    const walletDetailRes = await app.$axios.$get(`api/dejipo/user-wallet-detail/?op_name=${params.opName}`);
    if (walletDetailRes.length === 0) {
      return {
        wallet: false
      }
    }
    return {
      wallet: true,
      walletDetailData: walletDetailRes[0],
    }
  },
}

</script>
<style scoped>
.toc-view {
  position: sticky;
  top: 1rem;
  z-index: 999;
}

.transparent-body {
  background: transparent
}
</style>
