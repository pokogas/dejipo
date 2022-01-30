<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12" lg="6" md="6">
          <v-card elevation="1">
            <v-card-title>
              <div style="font-size: 15px" class="font-weight-bold">累計発行ポイント</div>
            </v-card-title>
            <div class="pl-7 pb-5">
              <span class="font-weight-light" style="font-size: 26px">{{ op_data[0].total_issuing_number }}</span>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" lg="6" md="6">
          <v-card elevation="1">
            <v-card-title>
              <div style="font-size: 15px" class="font-weight-bold">合計利用者数</div>
            </v-card-title>
            <div class="pl-7 pb-5">
              <span class="font-weight-light" style="font-size: 26px">{{ op_data[0].user_count }}</span>
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" lg="6" md="6">
          <v-card elevation="1">
            <v-card-title>
              <div style="font-size: 15px" class="font-weight-bold">最近のトランザクション</div>
            </v-card-title>
            <v-data-table height="450px" hide-default-footer
                          :headers="headers"
                          :items="mgTransactionList"
                          style="white-space: nowrap">
              <template v-slot:item.id="{ item }">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                      x-small
                      >
                      IDを確認
                    </v-btn>
                  </template>
                  <span>{{ item.id }}</span>
                </v-tooltip>
              </template>
              <template v-slot:item.use_time="{ item }">
                <span>{{ $moment(item.use_time).format('YYYY/MM/DD HH:mm') }}</span>
              </template>
              <template v-slot:item.use_usage="{ item }">
                <v-chip
                  :color="getTransactionUseColor(item.use_usage)"
                  dark label small>
                  <span v-if="item.use_usage ===1">支払い</span>
                  <span v-if="item.use_usage ===2">付与</span>
                </v-chip>
              </template>
              <template v-slot:item.status="{ item }">
                  <span style="color: rgba(74,197,35,0.7)" v-if="item.status ===1">・完了</span>
                  <span style="color: rgba(63,63,63,0.72)" v-else-if="item.status === 2 &&  $moment().diff(item.use_time, `seconds`) < 1800">・未支払い</span>
                  <span style="color: rgba(63,63,63,0.72)" v-else-if="item.status === 3 &&  $moment().diff(item.use_time, `seconds`) < 1800">・発行済み</span>
                  <span style="color: rgba(183,87,87,0.72)" v-else-if="item.status === 2 || item.status === 3 &&  $moment().diff(item.use_time, `seconds`) > 1800">・期限切れ</span>
              </template>
              <template v-slot:item.action="{item}">
                <v-btn icon :to="`/management/${$route.params.opName}/transaction/detail/${item.id}`">
                  <v-icon>
                    mdi-open-in-new
                  </v-icon>
                </v-btn>
              </template>
              <template v-slot:no-data>最近のトランザクションがありません。</template>
            </v-data-table>
          </v-card>
        </v-col>
        <v-col cols="12" lg="6" md="6">
          <v-card elevation="1">
            <v-card-title>
              <div style="font-size: 15px" class="font-weight-bold">イベント</div>
            </v-card-title>
            <div class="pl-7 pb-5">
              <span class="font-weight-light" style="font-size: 18px">この機能は現在使用できません。</span>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
export default {
  layout: "management/Main",
  head() {
    return {
      title: `${this.$route.params.opName}-HOME`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  data() {
    return {
      headers: [
        {text: 'トランザクションID', value: 'id', sortable: false, align: 'start',},
        {text: '発行日時', value: 'use_time'},
        {text: '用途', value: 'use_usage'},
        {text: 'ポイント', value: 'point'},
        {text: 'ステータス', value: 'status'},
        {text: '', value: 'action', sortable: false},
      ],
      mgTransactionList: []
    }
  },
  mounted() {
  },
  created() {
    this.setData()
  },
  methods: {
    async setData() {
      let params = this.$route.params.opName
      await this.$axios.$get(`api/management/management-transaction-list/?op_name=${params}`).then(function (res) {
        this.mgTransactionList = res.results.slice(0, 8);
      }.bind(this))
        .catch(function (e) {
            if (e.response && e.response.status === 400) {
              return this.error({});
            }
          }
        )
    },
    getTransactionUseColor(use_usage) {
      if (use_usage === 1) return '#FF7474'
      if (use_usage === 2) return 'green'
    }
  },
  async asyncData({app, params, error}) {
    let opDataRes = await app.$axios.$get(`api/management/op-detail/?op_name=${params.opName}`)
      .catch(function (e) {
          if (e.response && e.response.status === 400) {
            return error({});
          }
        }
      )
    return {
      op_data: opDataRes,
    }
  },
}
</script>
<style scoped>

</style>
