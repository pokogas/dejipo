<template>
  <div>
    <v-container fluid>
      <p class="text-h4">設定</p>
      <v-container>
        <v-card class="pa-4 mb-8">
          <p>基本設定</p>
          <v-form ref="basic_form">
            <v-row>
              <v-col cols="4">
                <v-subheader>OP詳細名</v-subheader>
              </v-col>
              <v-col cols="8">
                <v-text-field
                  solo
                  :value="saving_data.basic.detailed_name"
                  :rules="[rules.required, rules.detailed_name.counter,rules.no_space]"
                  v-model="saving_data.basic.detailed_name"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-subheader>OP紹介文</v-subheader>
              </v-col>
              <v-col cols="8">
                <v-textarea
                  solo
                  :value="saving_data.basic.introduction"
                  :rules="[rules.required, rules.introduction.counter,rules.no_space]"
                  v-model="saving_data.basic.introduction"
                ></v-textarea>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-subheader>1P当たりの価値</v-subheader>
              </v-col>
              <v-col cols="8">
                <v-text-field
                  solo
                  prefix="¥"
                  :value="saving_data.basic.cost"
                  :rules="[rules.cost.min, rules.cost.max, rules.no_space]"
                  v-model="saving_data.basic.cost"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card>
        <v-card class="pa-4 mb-6">
          <p>プライバシー設定</p>
          <v-row>
            <v-col cols="4">
              <v-subheader>OP公開</v-subheader>
            </v-col>
            <v-col cols="8">
              <v-switch
                v-model="saving_data.privacy.publishing"
                inset
              ></v-switch>
              <span v-if="saving_data.privacy.publishing">公開</span>
              <span v-else>非公開</span>
            </v-col>
          </v-row>
        </v-card>
        <div class="mb-3">
          <v-row class="justify-end mr-1" transition="slide-y-reverse-transition">
            <v-fab-transition>
              <v-btn v-show="!saveBtn" class="mr-2" color="#7886FF" @click="dataSave()"><span
                class="white--text">保存</span></v-btn>
            </v-fab-transition>
          </v-row>
        </div>
      </v-container>
    </v-container>
  </div>
</template>
<script>
export default {
  layout: "management/Main",
  head() {
    return {
      title: `${this.$route.params.opName}-設定`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  data() {
    return {
      saving_data: {
        basic: {
          cost: 0,
          detailed_name: "",
          introduction: "",
        },
        privacy: {
          publishing: false
        },
      },
      check_data: {
        basic: {
          cost: 0,
          detailed_name: "",
          introduction: "",
        },
        privacy: {
          publishing: false
        },
      },
      saveBtn: true,
      rules: {
        detailed_name: {
          counter: value => value.length <= 49 || '49字以下で入力して下さい。',
        },
        introduction: {
          counter: value => value.length <= 799 || '799字以下で入力して下さい。',
        },
        cost: {
          max: value => value <= 99999999 || '99999999以下で入力して下さい。',
          min: value => value > -1 || '0以上で入力して下さい。',
        },
        required: value => !!value || '入力してください',
        no_space: value => /.*\S+.*/.test(value) || '空白のみは使用できません。'
      },
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
  created() {
    this.dataSet()
  },
  methods: {
    dataSave() {
      if (this.$refs.basic_form.validate()) {
        if (!this.saveBtn) {
          let params = this.$route.params.opName
          let data = {
            "detailed_name": this.saving_data.basic.detailed_name,
            "introduction": this.saving_data.basic.introduction,
            "cost": this.saving_data.basic.cost,
            "publishing": this.saving_data.privacy.publishing
          }
          this.$axios.$post(`api/management/management-op-setting/?op_name=${params}`, data)
            .then(() => {
              this.saveBtn = true
              this.$swal.fire({
                icon: 'success',
                position: 'top-end',
                toast: true,
                showConfirmButton: false,
                timer: 2500,
                title: `設定完了しました。`,
              })
              return this.dataSet()
            })
        }
      }
    },
    dataSet() {
      let params = this.$route.params.opName
      this.$axios.$get(`api/management/management-op-setting/?op_name=${params}`)
        .then((res) => {
          this.saving_data.basic.cost = res.cost
          this.saving_data.basic.detailed_name = res.detailed_name
          this.saving_data.basic.introduction = res.introduction
          this.saving_data.privacy.publishing = res.publishing
          this.check_data.basic.cost = res.cost
          this.check_data.basic.detailed_name = res.detailed_name
          this.check_data.basic.introduction = res.introduction
          this.check_data.privacy.publishing = res.publishing
        })
    },
  },
  watch: {
    saving_data: {
      handler: function (newVal) {
        this.saveBtn = JSON.stringify(newVal) === JSON.stringify(this.check_data)
      },
      deep: true,
      immediate: false
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
