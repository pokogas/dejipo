<template>
  <v-container fluid>
    <nuxt-link :to="`/management/${$route.params.opName}/transaction/`">戻る</nuxt-link>
    <p class="text-h4">トランザクション照会</p>
    <v-container>
      <v-card class="pa-5 mx-auto mb-5" max-width="1000px">検索フォーム
        <v-text-field
          label="トランザクションID"
          required
          v-model="formData.id"
        ></v-text-field>
        <div class="mb-3">
          <v-row class="justify-end mr-1" @click="readDataFromAPI()">
            <v-btn class="" color="#7886FF">
              <v-icon color="white" class="pr-1" dense>mdi-magnify</v-icon>
              <span class="white--text">検索</span></v-btn>
          </v-row>
        </div>
      </v-card>
      <v-card class="pa-5 mx-auto" max-width="1000px">
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
              :color="getTransactionUseColor(item.use_usage)" dark label small>
              <span v-if="item.use_usage ===1">支払い</span>
              <span v-if="item.use_usage ===2">付与</span>
            </v-chip>
          </template>
          <template v-slot:item.status="{ item }">
            <span style="color: rgba(74,197,35,0.7)" v-if="item.status ===1">・完了</span>
            <span style="color: rgba(63,63,63,0.72)"
                  v-else-if="item.status === 2 &&  $moment().diff(item.use_time, `seconds`) <= 1800">・未支払い</span>
            <span style="color: rgba(63,63,63,0.72)"
                  v-else-if="item.status === 3 &&  $moment().diff(item.use_time, `seconds`) <= 1800">・発行済み</span>
            <span style="color: rgba(183,87,87,0.72)"
                  v-else-if="item.status === 2 || item.status === 3 &&  $moment().diff(item.use_time, `seconds`) >= 1800">・期限切れ</span>
          </template>
          <template v-slot:item.action="{item}">
            <v-btn icon :to="`/management/${$route.params.opName}/transaction/detail/${item.id}`">
              <v-icon>
                mdi-open-in-new
              </v-icon>
            </v-btn>
          </template>
          <template v-slot:no-data>トランザクションが見つかりませんでした。
          </template>
        </v-data-table>
      </v-card>
    </v-container>
  </v-container>
</template>
<script>
export default {
  layout: "management/Main",
  head() {
    return {
      title: `${this.$route.params.opName}-トランザクション-検索`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  data() {
    return {
      formData: {
        id: ""
      },
      page: 1,
      totalItems: 0,
      numberOfPages: 0,
      results: [],
      loading: true,
      options: {},
      headers: [
        {text: "トランザクションID", value: "id", sortable: false, align: 'start',},
        {text: "発行日時", value: "use_time", sortable: false},
        {text: "用途", value: "use_usage", sortable: false},
        {text: "ステータス", value: "status", sortable: false},
        {text: "ポイント", value: "point", sortable: false},
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
      const {page} = this.options;
      let pageNumber = 1;
      this.$axios.$get(`api/management/management-transaction-search/?op_name=${params}&id=${this.formData.id}&page=${pageNumber}`)
        .then((response) => {
          this.loading = false;
          this.totalItems = response.count;
          this.totalPassengers = response.totalPassengers;
          this.numberOfPages = response.totalPages;
          this.results = response.results
        })
        .catch((response) => {
          this.loading = false;
          this.results = []
        })
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
