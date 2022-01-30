<!--eslint-disable-->
<template>
  <v-container fluid>
    <p class="text-h4">ユーザー管理</p>
    <v-btn @click="inviteUrlClickBtn()">招待URL</v-btn>
    <v-card class="pr-4 pl-4 mt-4 mb-4 overflow-x-auto">
      <v-chip-group
        v-model="selection" active-class="deep-purple accent-2 white--text"
        mandatory>
        <v-chip @click="chipClick(`registration_user`)">登録済み</v-chip>
        <v-chip @click="chipClick(`wallet_registration_user`)">ウォレット登録済み</v-chip>
        <v-chip @click="chipClick(`inviting_application_list`)">招待申請</v-chip>
      </v-chip-group>
    </v-card>
    <div>
      <v-row justify="start">
        <v-col
          v-for="value in userList" v-bind:key="value.id"
          lg="auto"
          md="auto"
          cols="12">
          <v-list>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>{{ value.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ value.email }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon color="green" v-show="selection === 2" @click="inviteAction(`approval`, value.id)">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
                <v-btn icon color="red" v-show="selection === 2" @click="inviteAction(`rejection`, value.id)">
                  <v-icon>mdi-minus</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
      <infinite-loading
        ref="infiniteLoading"
        spinner="spiral"
        @infinite="infiniteHandler">
        <div slot="no-more">
          <v-banner></v-banner>
        </div>
        <div slot="no-results"/>
      </infinite-loading>
    </div>
    <div>
      <v-row justify="center">
        <v-dialog
          v-model="inviteUrl.dialog"
          v-show="inviteUrl.dialog"
          persistent
          max-width="600px">
          <v-card>
            <v-card-title>
              <span class="text-h6">招待URL</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <div v-if="inviteUrl.option_data !== null">
                  <v-row>
                    <v-col
                      cols="12">
                      <v-text-field
                        :value="inviteUrl.url"
                        label="Solo"
                        solo
                        readonly
                        messages="招待URL"
                        append-icon='mdi-clipboard-multiple-outline'
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <div>
                    <p>利用期限 <span
                      v-if="inviteUrl.option_data.time_limit === 0">無期限</span><span
                      v-else>{{
                        this.$moment(inviteUrl.option_data.use_time).add(inviteUrl.option_data.time_limit, 's').format('YYYY/MM/DD HH:mm')
                      }}</span></p>
                    <p>カウンター :{{ inviteUrl.option_data.using_count }} <span
                      v-if="inviteUrl.option_data.use_limit_count === 0">上限なし</span><span
                      v-else>(上限{{ inviteUrl.option_data.use_limit_count }}回)</span></p>
                  </div>
                </div>
                <div v-else>
                  <p class="text-center red--text">URLを発行してください。</p>
                </div>
                <div>
                  <v-expansion-panels accordion>
                    <v-expansion-panel>
                      <v-expansion-panel-header>オプション</v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div class="ma-1">
                          <span>利用期限</span>
                          <div class="overflow-x-auto">
                            <v-chip-group
                              active-class="deep-purple accent-2 white--text"
                              mandatory
                              v-model="inviteUrl.options.use_time_limit_num">
                              <v-chip
                                v-for="time in inviteUrl.options.use_time_limits"
                                :key="time.sec"
                                :value="time.sec">{{ time.title }}
                              </v-chip>
                            </v-chip-group>
                          </div>
                          <span>利用上限</span>
                          <div class="">
                            <v-switch
                              flat
                              v-model="inviteUrl.use_max">
                              label=""
                            </v-switch>
                            <v-slider
                              :disabled="inviteUrl.use_max === false"
                              thumb-label="always"
                              step="100"
                              ticks="always"
                              v-model="inviteUrl.options.use_max_num"
                              max="1000"
                              min="0"></v-slider>
                            <span v-if="inviteUrl.use_max">上限あり</span>
                            <span v-else>上限無し</span>
                          </div>
                        </div>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </div>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="black darken-1"
                text
                @click="inviteUrl.dialog = false">
                閉じる
              </v-btn>
              <v-btn
                color="green lighten-1"
                elevation="0"
                @click="inviteUrlIssueBtn()"
                v-if="inviteUrl.option_data !== null">
                <span class="white--text">再発行</span>
              </v-btn>
              <v-btn
                color="green lighten-1"
                elevation="0"
                @click="inviteUrlIssueBtn()"
                v-else-if="inviteUrl.option_data === null">
                <span class="white--text">発行</span>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </div>
  </v-container>
</template>
<!--eslint-disable-->
<script>


export default {
  layout: "management/Main",
  head() {
    return {
      title: `${this.$route.params.opName}-ユーザー管理`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
  data() {
    return {
      selection: 0,
      userList: [],
      userData: null,
      next: null,
      inviteUrl: {
        dialog: false,
        use_max: false,
        option_data: null,
        url: "",
        options: {
          use_time_limit_num: 0,
          use_max_num: 0,
          use_time_limits: [
            {"title": "無制限", "sec": 0},
            {"title": "30分", "sec": 1800},
            {"title": "1時間", "sec": 3600},
            {"title": "6時間", "sec": 21600},
            {"title": "12時間", "sec": 43200},
            {"title": "1日", "sec": 86400},
          ],
        },
      }
    }
  },
  methods: {
    // 招待URL関連start
    inviteUrlConvertingSetData(data) {
      this.inviteUrl.option_data = data
      this.inviteUrl.options.use_max_num = data.use_limit_count
      this.inviteUrl.options.use_time_limit_num = data.time_limit
      this.inviteUrl.url = `http://127.0.0.1:3000/invite/op/${data.id}`
      this.inviteUrl.use_max = data.use_limit_count !== 0;
    },
    inviteUrlGetData() {
      let params = this.$route.params
      this.$axios.$get(`api/management/management-op-invite-option-setting/?op_name=${params.opName}`).then((res) => {
        if (res.detail === "招待URLを作成してください") {
          this.option_data = null
          return
        }
        this.inviteUrlConvertingSetData(res.detail)
      });
    },
    inviteUrlPostData() {
      let data = {
        "time_limit": this.inviteUrl.options.use_time_limit_num,
        "use_limit_count": this.inviteUrl.options.use_max_num
      };
      let params = this.$route.params
      this.$axios.$post(`api/management/management-op-invite-option-setting/?op_name=${params.opName}`, data)
        .then((res) => {
          this.$swal.fire({
            icon: 'success',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `URLを発行しました。`,
          })
          return this.inviteUrlConvertingSetData(res.detail)
        })
    },
    inviteUrlClickBtn() {
      this.inviteUrlGetData()
      this.inviteUrl.dialog = true
    },
    inviteUrlIssueBtn() {
      this.inviteUrlPostData()
    },
    // 招待URL関連end

    chipClick(option) {
      this.userList = [];
      this.userData = null;
      this.next = "";
      this.setData(option)
      return this.$refs.infiniteLoading.stateChanger.reset()
    },
    async inviteAction(action, id) {
      let params = this.$route.params
      await this.$axios.$post(`api/management/management-op-invite-action/?op_name=${params.opName}&action=${action}&user_id=${id}`).then((res) => {
        this.userData = res
        this.next = this.urlConversion(res.next)
        this.$swal.fire({
          icon: 'success',
          position: 'top-end',
          toast: true,
          showConfirmButton: false,
          timer: 2500,
          title: `${res.detail}`,
        })
      });
      this.userList = [];
      this.userData = null;
      this.next = null;
      return await this.setData(`inviting_application_list`)
    },
    infiniteHandler() {
      if (this.next === null || this.next === undefined) {
        return this.$refs.infiniteLoading.stateChanger.complete()
      } else {
        setTimeout(() => {
          this.$axios.$get(this.next).then(function (res) {
            this.userData = res
            this.next = this.next = this.urlConversion(res.next)
            for (let i in res.results)
              this.userList.push(res.results[i])
          }.bind(this));
          this.$refs.infiniteLoading.stateChanger.loaded()
        }, 800)
      }
    },
    async setData(option) {
      let params = this.$route.params
      await this.$axios.$get(`api/management/management-op-user-list/?op_name=${params.opName}&option=${option}`).then((res) => {
        this.userData = res
        this.next = this.urlConversion(res.next)
      });
      if (this.userData.results.length < 1) {
        this.transaction = true
      }
      for (let i in this.userData.results)
        this.userList.push(this.userData.results[i])
    },
    urlConversion(url) {
      if (url === null || url === undefined) {
        return null
      }
      let param = url.split("/")[6]
      return `api/management/management-op-user-list/${param}`
    },
  },
  created() {
    this.setData("registration_user")
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
