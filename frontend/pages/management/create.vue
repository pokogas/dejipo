<template>
  <v-main>
    <div>
      <v-container>
        <p class="text-h4">OPを作成</p>
        <v-card class="pa-6 mx-auto" max-width="1200px">
          <v-form ref="form">
            <v-row>
              <v-col cols="4">
                <v-subheader>OP名</v-subheader>
              </v-col>
              <v-col cols="8">
                <v-text-field
                  outlined
                  :rules="[rules.op_name.only_alphabetical,rules.op_name.max_counter,rules.op_name.min_counter, rules.required,rules.no_space,rules.op_name.existing]"
                  v-model="create_data.op_name"
                  :value="create_data.op_name"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-subheader>OP詳細名</v-subheader>
              </v-col>
              <v-col cols="8">
                <v-text-field
                  outlined
                  :rules="[rules.detailed_name.counter, rules.required,rules.no_space]"
                  v-model="create_data.detailed_name"
                  :value="create_data.detailed_name"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-subheader>OP紹介文</v-subheader>
              </v-col>
              <v-col cols="8">
                <v-textarea
                  outlined
                  :rules="[rules.introduction.counter, rules.required,rules.no_space]"
                  v-model="create_data.introduction"
                  :value="create_data.introduction"
                ></v-textarea>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-subheader>1P当たりの価値</v-subheader>
              </v-col>
              <v-col cols="8">
                <v-text-field
                  outlined
                  :rules="[rules.cost.min, rules.cost.max, rules.no_space]"
                  v-model="create_data.cost"
                  :value="create_data.cost"
                  prefix="¥"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
          <v-row>
            <v-col cols="4">
              <v-subheader>OP公開</v-subheader>
            </v-col>
            <v-col cols="8">
              <v-switch
                v-model="create_data.publishing"
                inset
              ></v-switch>
              <span v-if="create_data.publishing">公開</span>
              <span v-else>非公開</span>
            </v-col>
          </v-row>
          <div class="mt-10 mb-4">
            <v-row class="justify-end mr-1" transition="slide-y-reverse-transition">
              <v-fab-transition>
                <v-btn class="mr-2" color="#7886FF" @click="confirmBtn()"><span
                  class="white--text">作成</span></v-btn>
              </v-fab-transition>
            </v-row>
          </div>
        </v-card>

        <v-dialog
          v-if="confirmDialog===true"
          v-model="confirmDialog"
          persistent
          max-width="800">
          <v-card>
            <v-card-title>最終確認</v-card-title>
            <v-card-subtitle>以下の内容でOPを作成しますか？</v-card-subtitle>
            <v-simple-table class="mb-10" style="white-space:nowrap;">
              <template>
                <tbody>
                <tr>
                  <td>OP名</td>
                  <td>{{ create_data.op_name }}</td>
                </tr>
                <tr>
                  <td>OP詳細名</td>
                  <td>{{ create_data.detailed_name }}</td>
                </tr>
                <tr>
                  <td>1P当たりの価値</td>
                  <td>¥ {{ create_data.cost }}</td>
                </tr>
                <tr>
                  <td>OP公開</td>
                  <td>
                    <span v-if="create_data.publishing">公開</span>
                    <span v-else>非公開</span>
                  </td>
                </tr>
                </tbody>
              </template>
            </v-simple-table>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="red darken-3"
                text
                @click="confirmDialog = false">
                キャンセル
              </v-btn>
              <v-btn
                color="green darken-1"
                text
                @click="create()">
                確定
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

      </v-container>
    </div>
  </v-main>
</template>
<script>
export default {
  layout: "management/Top",
  head() {
    return {
      title: `OP作成`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  data() {
    return {
      confirmDialog: false,
      rules: {
        op_name: {
          max_counter: value => value.length <= 10 || '10字以下で入力して下さい。',
          min_counter: value => value.length >= 3 || '3文字以下で入力して下さい。',
          only_alphabetical: value => /^[a-zA-Z]*$/.test(value) || 'アルファベット大文字小文字のみ使用可能',
          existing: value => (value && this.op_name_exist !== true) || "このOPネームは使用できません。",
        },
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
      create_data: {
        op_name: "",
        detailed_name: "",
        introduction: "",
        cost: 0,
        publishing: false
      },
      op_name_exist: false
    }
  },
  methods: {
    async confirmBtn() {
      this.op_name_exist = false
      if (this.$refs.form.validate()) {
        await this.$axios.$get(`api/management/management-op-create/?c_op_name=${this.create_data.op_name}`)
          .then((res) => {
            if (res.detail === "利用不可") {
              this.op_name_exist = true
            }
          })
      }
      if (this.$refs.form.validate()) {
        return this.confirmDialog = true
      }
    },
    create() {
      if (this.$refs.form.validate()) {
        let data = {
          "op_name": this.create_data.op_name,
          "detailed_name": this.create_data.detailed_name,
          "introduction": this.create_data.introduction,
          "cost": this.create_data.cost,
          "publishing": this.create_data.publishing
        }
        this.$axios.$post(`api/management/management-op-create/`, data)
          .then((res) => {
            this.$swal.fire({
              icon: 'success',
              position: 'top-end',
              toast: true,
              showConfirmButton: false,
              timer: 2500,
              title: `OPを作成しました`,
            })
            return this.$router.replace({path: `/management/${res.detail.op_name}`});
          })
          .catch(function (e) {
            if (e.response && e.response.status === 405) {
              console.log("error")
            }
          })
      }
    },
    querySelections(v) {
      this.op_name.loading = true
      console.log(v)
      this.op_name.loading = false
    },
  },
  watch: {
    search(val) {
      val && val !== this.select && this.querySelections(val)
    },
  },
  created() {
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
}
</script>
<style scoped>

</style>
