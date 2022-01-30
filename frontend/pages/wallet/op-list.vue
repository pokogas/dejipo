<template>
  <div>
    <Header/>
    <v-container>
      <nuxt-link to="/wallet">
        <v-list-item-subtitle>
          ウォレット一覧に戻る
        </v-list-item-subtitle>
      </nuxt-link>
      <v-app-bar-title>
        OPを検索
      </v-app-bar-title>
      <v-form ref="form">
        <v-text-field
          label="ID"
          v-model="keyword"
          :rules="[rules.required]"
        ></v-text-field>
      </v-form>
      <v-row class="justify-end mr-1" @click="">
        <v-btn class="" color="#7886FF" @click="searchBtn">
          <v-icon color="white" class="pr-1" dense>mdi-magnify</v-icon>
          <span class="white--text">検索</span></v-btn>
      </v-row>
      <div class="pt-7">
        <v-list>
          <div>
            <v-card elevation="0" class="rounded-lg overflow-auto" height="500">
              <v-list two-line>
                <div v-for="op in listOriginalPoint" :key="op.id">
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>{{ op.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ op.detailed_name }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-btn icon color="green" @click="openDetailModal(op)">
                        <v-icon>mdi-plus</v-icon>
                      </v-btn>
                    </v-list-item-action>
                  </v-list-item>
                  <v-divider></v-divider>
                </div>
                <p v-if="listOriginalPoint.length === 0" class="text-center">OPが見つかりませんでした。</p>
              </v-list>
            </v-card>
          </div>
        </v-list>
      </div>
      <v-dialog
        v-if="detailModal"
        v-model="detailModal"
        persistent
        max-width="290">
        <v-card>
          <v-card-title>
            {{ detailModalItem.name }}
          </v-card-title>
          <v-card-subtitle>
            {{ detailModalItem.detailed_name }}
          </v-card-subtitle>
          <v-card-text>
            {{ detailModalItem.introduction }}
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="gray darken-1"
              text
              @click="closeDetailModal()">
              キャンセル
            </v-btn>
            <v-btn
              color="green darken-1"
              text
              @click="addWallet(detailModalItem.id,detailModalItem.name)">
              追加
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
    <Footer/>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title:  "ウォレット追加",
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
  data() {
    return {
      keyword: '',
      listOriginalPoint: [],
      detailModal: false,
      detailModalItem: null,
      userWalletList: null,
      rules: {
        required: value => !!value || '入力してください',
      },
    }
  },
  created() {
    this.$axios.$get('api/dejipo/user-wallet-list/').then(function (res) {
      this.userWalletList = res
    }.bind(this))
  },
  methods: {
    logout() {
      this.$auth.logout()
    },
    async searchBtn() {
      if (this.$refs.form.validate()) {
        this.listOriginalPoint = []
        await this.$axios.$get(`api/dejipo/original-point-list/?name=${this.keyword}`).then(function (res) {
          this.listOriginalPoint = res
        }.bind(this))
      }
    },
    openDetailModal(item) {
      this.detailModalItem = null
      this.detailModalItem = item
      this.detailModal = true
    },
    closeDetailModal() {
      this.detailModalItem = null
      this.detailModal = false
    },
    addWallet(op_id, op_name) {
      for (let i in this.userWalletList) {
        if (this.userWalletList[i].op.id === op_id) {
          this.$swal.fire({
            icon: 'warning',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: '所持済み',
          })
          return this.detailModal = false
        }
      }
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
    },
  },
  async asyncData({app}) {
    let originalPointListRes = await app.$axios.$get('api/dejipo/original-point-list/');
    return {
      users: originalPointListRes
    }
  },

}
</script>
