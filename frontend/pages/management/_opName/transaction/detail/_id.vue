<template>
  <div>
    <v-container fluid>
      <nuxt-link :to="`/management/${$route.params.opName}/transaction/`">
        戻る
      </nuxt-link>
      <p class="text-h4">
        トランザクション詳細
      </p>
      <v-container>
        <v-card>
          <v-simple-table class="mb-10" style="white-space:nowrap;">
            <template>
              <tbody>
                <tr>
                  <td>トランザクションID</td>
                  <td>{{ transaction_data.id }}</td>
                </tr>
                <tr>
                  <td>用途</td>
                  <td v-if="transaction_data.usage === 2">
                    <v-chip color="green" dark label small>
                      付与
                    </v-chip>
                  </td>
                  <td v-if="transaction_data.usage === 1">
                    <v-chip color="#FF7474" dark label small>
                      支払い
                    </v-chip>
                  </td>
                </tr>
                <tr>
                  <td>発行日時</td>
                  <td>{{ $moment(transaction_data.time).format('YYYY/MM/DD HH:mm') }}</td>
                </tr>
                <tr v-if="transaction_data.status === 1">
                  <td>利用日時</td>
                  <td>{{ $moment(transaction_data.trading_time).format('YYYY/MM/DD HH:mm') }}</td>
                </tr>
                <tr>
                  <td>利用期限</td>
                  <td>{{ $moment(transaction_data.time).add(30, 'm').format('YYYY/MM/DD HH:mm') }}</td>
                </tr>
                <tr v-if="transaction_data.status === 1">
                  <td>ステータス</td>
                  <td v-if="transaction_data.status ===1" style="color: rgba(74,197,35,0.7); font-size: 13px">
                    ・完了
                  </td>
                  <td v-if="transaction_data.status ===2" style="color: rgba(63,63,63,0.72); font-size: 13px">
                    ・未支払い
                  </td>
                  <td v-if="transaction_data.status ===3" style="color: rgba(63,63,63,0.72); font-size: 13px">
                    ・発行済み
                  </td>
                </tr>
                <tr v-if="transaction_data.status === 1">
                  <td>ウォレットID</td>
                  <td>{{ transaction_data.wallet }}</td>
                </tr>
                <tr>
                  <td>ポイント</td>
                  <td>{{ transaction_data.point }} P</td>
                </tr>
                <tr>
                  <td>トランザクションURL</td>
                  <td>{{ transaction_url }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
        <v-row class="justify-end mr-1">
          <v-btn class="mr-2" @click="setData()">
            更新
          </v-btn>
          <v-btn class="mr-2" @click="qrModal = true">
            QR表示
          </v-btn>
          <v-btn class="mr-2">
            SNS
          </v-btn>
        </v-row>
        <v-dialog
          v-if="qrModal"
          v-model="qrModal"
          width="500"
        >
          <v-card>
            <v-layout justify-center>
              <qrcode :value="transaction_url" :options="{ width: 250 }" class="grey lighten-2" />
            </v-layout>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="primary"
                text
                @click="qrModal = false"
              >
                閉じる
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </v-container>
  </div>
</template>
<script>
export default {
  layout: 'management/Main',
  async asyncData ({ app, params, error }) {
    const opDataRes = await app.$axios.$get(`api/management/op-detail/?op_name=${params.opName}`)
      .catch(function (e) {
        if (e.response && e.response.status === 400) {
          return error({})
        }
      }
      )
    return {
      op_data: opDataRes
    }
  },
  data () {
    return {
      transaction_data: [],
      qrModal: false,
      transaction_url: ''
    }
  },
  head () {
    return {
      title: `${this.$route.params.opName}-トランザクション-詳細`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  created () {
    this.setData()
  },
  methods: {
    async setData () {
      const params = this.$route.params
      await this.$axios.$get(`api/management/management-transaction-detail/?op_name=${params.opName}&t_id=${params.id}`).then(function (res) {
        this.transaction_url = `http://127.0.0.1:3000/transaction/${params.id}`
        return this.transaction_data = res.detail
      }.bind(this)).catch(function () {
        return this.$nuxt.error({})
      }.bind(this))
    }
  }

}
</script>
<style scoped>

</style>
