<template>
  <div>
    <v-container fluid>
      <p class="text-h4">トランザクション</p>
      <div>
        <v-row>
          <v-col cols="12" lg="4" md="4">
            <v-card elevation="1" height="300px">
              <v-card-title>
                <div style="font-size: 15px" class="font-weight-bold">情報</div>
              </v-card-title>
              <v-simple-table>
                <template>
                  <tbody>
                  <tr>
                    <td>累計発行ポイント</td>
                    <td>{{ op_data[0].total_issuing_number }}P</td>
                  </tr>
                  <tr>
                    <td>作成トランザクション</td>
                    <td>0個</td>
                  </tr>
                  <tr>
                    <td>完了済みトランザクション</td>
                    <td>0</td>
                  </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card>
          </v-col>
          <v-col cols="12" lg="4" md="4">
            <v-card elevation="1" height="300px">
              <v-card-title>
                <div style="font-size: 15px" class="font-weight-bold">未定</div>
              </v-card-title>
              <div class="pl-7 pb-5">
                <span class="font-weight-light" style="font-size: 26px"></span>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" lg="4" md="4">
            <v-card elevation="1" class="pb-2" height="300px">
              <v-card-title>
                <div style="font-size: 15px" class="font-weight-bold">操作</div>
              </v-card-title>
              <div class="ma-2">
                <v-btn block class="mb-3" color="#7886FF" elevation="0" :to="`/management/${$route.params.opName}/transaction/create`">
                  <v-icon class="white--text" dense>mdi-plus</v-icon>
                  <span class="font-weight-bold white--text">トランザクションの作成</span>
                </v-btn>
                <v-btn block class="mb-3" color="#EEEEEE" elevation="0" :to="`/management/${$route.params.opName}/transaction/search`">
                  <v-icon color="#7886FF" dense>mdi-text-box-search-outline</v-icon>
                  <span class="font-weight-bold" style="color: #7886FF">トランザクションの照会</span>
                </v-btn>
              </div>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" lg="12" md="12">
            <v-card elevation="1">
              <v-card-title>
                <div style="font-size: 15px" class="font-weight-bold">トランザクション履歴</div>
                <v-btn icon @click="readDataFromAPI()"><v-icon>mdi-update</v-icon></v-btn>
              </v-card-title>
              <v-data-table
                :page="page"
                :pageCount="numberOfPages"
                :headers="headers"
                :items="results"
                :options.sync="options"
                :server-items-length="totalItems"
                :loading="loading"
                class="elevation-1"
                style="white-space: nowrap">
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
                  <span style="color: rgba(63,63,63,0.72)" v-else-if="item.status === 2 &&  $moment().diff(item.use_time, `seconds`) <= 1800">・未支払い</span>
                  <span style="color: rgba(63,63,63,0.72)" v-else-if="item.status === 3 &&  $moment().diff(item.use_time, `seconds`) <= 1800">・発行済み</span>
                  <span style="color: rgba(183,87,87,0.72)" v-else-if="item.status === 2 || item.status === 3 &&  $moment().diff(item.use_time, `seconds`) >= 1800">・期限切れ</span>
                </template>
                <template v-slot:item.action="{item}">
                <v-btn icon :to="`/management/${$route.params.opName}/transaction/detail/${item.id}`">
                  <v-icon>
                    mdi-open-in-new
                  </v-icon>
                </v-btn>
              </template>
              <template v-slot:no-data>トランザクションがありません。
              </template>
              </v-data-table>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </v-container>
  </div>
</template>
<script>
export default {
  layout: "management/Main",
  head() {
    return {
      title: `${this.$route.params.opName}-トランザクション`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  data() {
    return {
      page: 1,
      totalItems: 0,
      numberOfPages: 0,
      results: [],
      loading: true,
      options: {},
      headers: [
        {text: "トランザクションID", value: "id", sortable: false, align: 'start',},
        {text: "発行日時", value: "use_time"},
        {text: "用途", value: "use_usage"},
        {text: "ステータス", value: "status"},
        {text: "ポイント", value: "point"},
        {text: '', value: 'action', sortable: false},
      ],
    }
  },
  watch: {
    options: {
      handler() {
        this.readDataFromAPI();
      },
    },
    deep: true,
  },
  mounted() {
  },
  created() {
  },
  methods: {
    readDataFromAPI() {
      this.loading = true;
      let params = this.$route.params.opName
      const {page, sortBy, sortDesc} = this.options;
      let sortData = ""
      if (sortDesc[0]) {
        sortData = `-${sortBy}`
      } else {
        sortData = `${sortBy}`
      }
      let pageNumber = page;
      this.$axios.$get(`api/management/management-transaction-list/?op_name=${params}&page=${pageNumber}&ordering=${sortData}`)
        .then((response) => {
          this.loading = false;
          this.totalItems = response.count;
          this.totalPassengers = response.totalPassengers;
          this.numberOfPages = response.totalPages;
          this.results = response.results
        });
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
  }
  ,
}
</script>
<style scoped>

</style>
