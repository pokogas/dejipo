<template>
  <div>
    <v-container fluid>
      <nuxt-link :to="`/management/${$route.params.opName}/transaction/`">
        戻る
      </nuxt-link>
      <p class="text-h4">
        トランザクション作成
      </p>
      <v-container>
        <v-card class="pa-5 mx-auto" max-width="600px">
          <div class="mb-3">
            <span>用途</span>
            <v-chip-group
              v-model="selection"
              active-class="deep-purple accent-4 white--text"
              column
              mandatory
            >
              <v-chip>支払い</v-chip>
              <v-chip>付与</v-chip>
            </v-chip-group>
          </div>
          <div class="mb-3">
            <span>ポイント数</span>
            <v-row>
              <v-col cols="6">
                <v-form ref="form">
                  <v-text-field
                    v-model="point"
                    label="0"
                    solo
                    :rules="[rules.required, rules.counter, rules.max, rules.min, rules.isInt]"
                    type="number"
                    @input="checkInput()"
                  />
                </v-form>
              </v-col>
            </v-row>
          </div>
          <div class="mb-3">
            <v-row class="justify-end mr-1">
              <v-btn class="mr-2" color="#7886FF" @click="confirmBtn()">
                <span class="white--text">作成</span>
              </v-btn>
            </v-row>
          </div>
        </v-card>
        <v-dialog
          v-if="confirmDialog===true"
          v-model="confirmDialog"
          persistent
          max-width="290"
        >
          <v-card>
            <v-simple-table class="mb-10" style="white-space:nowrap;">
              <template>
                <tbody>
                  <tr>
                    <td>用途</td>
                    <td v-if="selection === 1">
                      <v-chip color="green" dark label small>
                        付与
                      </v-chip>
                    </td>
                    <td v-if="selection === 0">
                      <v-chip color="#FF7474" dark label small>
                        支払い
                      </v-chip>
                    </td>
                  </tr>
                  <tr>
                    <td>ポイント</td>
                    <td>{{ point }} P</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="red darken-3"
                text
                @click="confirmDialog = false"
              >
                キャンセル
              </v-btn>
              <v-btn
                color="green darken-1"
                text
                @click="completeBtn()"
              >
                確定
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
      point: 0,
      selection: 0,
      confirmDialog: false,
      rules: {
        required: value => !!value || '入力してください',
        counter: value => value.length <= 8 || '8桁以下で入力して下さい。',
        max: value => value <= 99999999 || '99999999以下で入力して下さい。',
        min: value => value > 0 || '1以上で入力して下さい。',
        isInt: value => Number.isInteger(Number(value)) || '小数点は使用できません'
      }
    }
  },
  head () {
    return {
      title: `${this.$route.params.opName}-トランザクション-作成`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  computed: {
    auth () {
      return this.$auth
    }
  },
  created () {
  },
  methods: {
    checkInput () {
      this.point = this.point.replace(/^0+/, '')
    },
    confirmBtn () {
      if (this.$refs.form.validate()) {
        this.point = this.point.replace(/^0+/, '')
        this.confirmDialog = true
      }
    },
    completeBtn () {
      console.log(`${this.point} ${this.selection}`)
      return this.complete()
    },
    complete () {
      const params = this.$route.params.opName
      this.$axios.$post(`api/management/management-transaction-create/?op_name=${params}&use_usage=${this.selection}&point=${this.point}`).then(function (res) {
        const t_id = res.detail.t_id
        this.confirmDialog = false
        this.$swal.fire({
          icon: 'success',
          position: 'top-end',
          toast: true,
          showConfirmButton: false,
          timer: 2500,
          title: 'トランザクションを作成しました'
        })
        return this.$router.replace({ path: `/management/${this.$route.params.opName}/transaction/detail/${t_id}` })
      }.bind(this))
    }
  }
}
</script>
<style scoped>

</style>
