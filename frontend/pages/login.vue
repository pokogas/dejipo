<template>
  <div>
    <v-container>
      <div style="max-width:500px" class="mx-auto">
        <div>
          <p style="color: #7886FF; font-size: 28px" class="text-center font-weight-bold ma-10 pt-10">DEJIPO</p>
        </div>
        <div>
          <p class="text-center font-weight-bold ma-2 mb-5" style="font-size: 16px; color: #606060;">メールアドレスでログイン</p>
          <v-form ref="form">
            <v-text-field
              v-model="form.email"
              type="email"
              :rules="emailRules"
              label="メールアドレス"
              outlined
              color="#7886FF"
              elevation="0"
              class="rounded-lg">
            </v-text-field>
            <v-text-field
              v-model="form.password"
              type="password"
              :rules="passwordRules"
              label="パスワード"
              outlined
              color="#7886FF"
              class="rounded-lg">
            </v-text-field>
          </v-form>
          <v-btn @click="login" :disabled.sync="this.usableBtn !== true" :loading="this.usableBtn !== true" block
                 x-large color="#7886FF">
            <span class="white--text font-weight-bold">ログイン</span>
          </v-btn>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: 'ログイン',
    }
  },
  middleware({store, redirect}) {
    if (store.$auth.loggedIn) {
      redirect("/home")
    }
  },
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      usableBtn: true,
      emailRules: [
        v => !!v || '入力してください。',
        v => /.+@.+\..+/.test(v) || '正しいメールアドレスを入力してください。'
      ],
      passwordRules: [
        v => !!v || '入力してください。',
      ]
    }
  },
  methods: {
    async login() {
      if (this.$refs.form.validate()) {
        this.usableBtn = false
        try {
          await this.$auth.loginWith('local', {data: this.form});
          return this.$router.replace({path: '/home'});
        } catch (error) {
          this.$swal(
            'エラー',
            'パスワードまたはメールアドレスが間違っています',
            'error'
          )
          return this.usableBtn = true
        }
      }
    }
  }
}
</script>
