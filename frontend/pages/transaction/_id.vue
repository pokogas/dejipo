<template>
  <div>
    <v-container>
      <div v-if="transaction" class="text-center">
        <p>{{ transaction_data.data.detail.op_name }}</p>
        <p class="font-weight-bold green--text text--lighten-2" style="font-size: 30px"
           v-if="transaction_data.data.detail.usage === 2">
          {{ transaction_data.data.detail.point }}<span
          style="font-size: 20px" class="grey--text text--darken-2">P</span></p>
        <p class="font-weight-bold red--text text--lighten-2" style="font-size: 30px"
           v-if="transaction_data.data.detail.usage === 1">
          {{ transaction_data.data.detail.point }}<span
          style="font-size: 20px" class="grey--text text--darken-2">P</span></p>
        <div class="grey--text text--darken-2">
          <span v-if="transaction_data.data.detail.usage === 2">受け取り期限</span>
          <span v-if="transaction_data.data.detail.usage === 1">支払い期限</span><br>
          <span>{{ this.$moment(transaction_data.data.detail.time).add(30, 'm').format('YYYY/MM/DD a HH:mm') }}</span>
        </div>
        <div v-if="auth.loggedIn">
          <div v-if="wallet_data.data.length === 0">
            <v-btn
              elevation="2"
              large
              outlined
              class="mt-2"
              @click="addWallet(transaction_data.data.detail.op_id)">ウォレットを追加
            </v-btn>
          </div>
          <div v-else>
            <v-btn
              v-if="transaction_data.data.detail.usage === 2"
              elevation="2"
              large
              outlined
              class="mt-2"
              @click="receive()">受け取る
            </v-btn>
            <v-btn
              v-if="transaction_data.data.detail.usage === 1"
              elevation="2"
              large
              outlined
              class="mt-2"
              @click="payment()">支払い
            </v-btn>
          </div>
          <p class="font-weight-bold text-left mt-4" style="margin:0;">{{ transaction_data.data.detail.op_name }}
            ウォレット</p>
          <div v-if="wallet_data.data.length === 0" class="pt-5">
            ウォレットを所持していません
          </div>
          <v-card class="mt-5" outlined v-else>
            <div>
              <v-list-item three-line>
                <v-list-item-content>
                  <v-list-item-title class="font-weight-bold grey--text text--darken-2 text-left">
                    所持ポイント
                  </v-list-item-title>
                  <div class="text-right"><span
                    class="font-weight-bold indigo--text text--lighten-2 pr-1"
                    style="font-size: 26px">{{ wallet_data.data[0].point }}</span><span>P</span>
                  </div>
                </v-list-item-content>
              </v-list-item>
            </div>
          </v-card>
        </div>
        <div v-else>
          <v-btn
            elevation="2"
            large
            outlined
            class="mt-2"
            to="/login">ログイン
          </v-btn>
          <p class="mt-4 red--text">受け取りにはログインが必要です。</p>
        </div>
      </div>
      <div v-else class="text-center subtitle-1">
        {{ error_text }}
      </div>
    </v-container>
  </div>
</template>
<script>

export default {
  layout: "OnlyHeader",
  auth: false,
  head() {
    return {
      title: `${this.transaction_data.data.detail.op_name}トランザクション`,
    }
  },
  computed: {
    auth() {
      return this.$auth
    },

  },
  data() {
    return {
      transaction: false,
      transaction_data: null,
      wallet_data: null,
      error_text: "",
    }
  },
  created() {
  },
  mounted() {
    this.dataSet()
  },
  methods: {
    async dataSet() {
      let params = this.$route.params.id
      await this.$axios.get(`api/transaction/?id=${params}`).then(function (res) {
        this.transaction_data = res
      }.bind(this))
      if (this.transaction_data.data.result === "NO") {
        this.transaction = false
        this.error_text = this.transaction_data.data.detail
        return
      }
      if (this.$auth.loggedIn) {
        await this.$axios.get(`api/dejipo/user-wallet-detail/?op_name=${this.transaction_data.data.detail.op_name}`).then(function (res) {
          this.wallet_data = res
        }.bind(this))
      }
      this.transaction = true
    },
    addWallet(op_id) {
      this.$axios.$post(`api/op/wallet-create/?op_id=${op_id}`);
      this.$axios.$get('api/dejipo/user-wallet-list/').then(function (res) {
        this.userWalletList = res
      }.bind(this))
      this.detailModal = false
      this.$swal.fire({
        icon: 'success',
        position: 'top-end',
        toast: true,
        showConfirmButton: false,
        timer: 2500,
        title: 'ウォレットを作成しました',
      })
      this.dataSet()
    },
    receive() {
      let params = this.$route.params.id
      this.$axios.$post(`api/transaction/?id=${params}`).then(function (res) {
        if (res.result === "OK") {
          this.$swal.fire({
            icon: 'success',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail.op_name} ${res.detail.point}ポイント受け取りました。`,
          })
          this.$router.replace({path: '/home'});
        } else if (res.result === "NO") {
          this.$swal.fire({
            icon: 'error',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail}`,
          })
          this.$router.replace({path: '/home'});
        }
      }.bind(this))
    },
    payment() {
      let params = this.$route.params.id
      this.$axios.$post(`api/transaction/?id=${params}`).then(function (res) {
        if (res.result === "OK") {
          this.$swal.fire({
            icon: 'success',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail.op_name} ${res.detail.point}ポイントを支払いました。`,
          })
          this.$router.replace({path: '/home'});
        } else if (res.result === "NO") {
          this.$swal.fire({
            icon: 'error',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail}`,
          })
        }
      }.bind(this));
    }
  },
}
</script>
