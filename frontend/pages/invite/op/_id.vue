<!--eslint-disable-->
<template>
  <div>
    <v-container>
      <div style="max-width:500px" class="mx-auto">
        <div v-if="invite" class="text-center">
          <p style="font-size: 26px" class="font-weight-bold">{{ invite_data.data.detail.op_name }}</p>
          <div>
            上記のOPから参加の招待が届いています。
          </div>
          <div class="mt-10">
            <div v-if="auth.loggedIn">
              <v-btn
                elevation="2"
                block
                large
                color="#7886FF"
                class="mt-2" @click="application()"><span style="font-size: 17px" class="white--text font-weight-bold">参加申請</span>
              </v-btn>
            </div>
            <div v-else>
              <v-btn
                elevation="2"
                outlined
                class="mt-2"
                block
                color="red"
                large
                to="/login">
                ログイン
              </v-btn>
              <p class="mt-4 red--text">招待申請をするにはログインが必要です。</p>
            </div>
          </div>
        </div>
        <div v-else class="text-center subtitle-1">
          {{ error_text }}
        </div>
      </div>
    </v-container>
  </div>
</template>
<!--eslint-disable-->
<!--eslint-disable-->
<script>

export default {
  layout: "OnlyHeader",
  auth: false,
  head() {
    return {
      title: `招待`,
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
  },
  data() {
    return {
      invite: false,
      invite_data: null,
      error_text: "",
    }
  },
  created() {
  },
  mounted() {
    this.dataSet()
  },
  methods: {
    async dataSet() {
      let params = this.$route.params.id
      await this.$axios.get(`api/management/management-op-invite/?invite_id=${params}`).then(function (res) {
        console.log(res)
        this.invite_data = res
      }.bind(this))
      if (this.invite_data.data.result === "NO") {
        this.invite = false
        this.error_text = this.invite_data.data.detail
        return
      }
      return this.invite = true
    },
    application() {
      let params = this.$route.params.id
      this.$axios.$post(`api/management/management-op-invite/?invite_id=${params}`).then(function (res) {
        if (res.result === "OK") {
          this.$swal.fire({
            icon: 'success',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail}`,
          })
          this.$router.replace({path: '/home'});
        } else if (res.result === "NO") {
          this.$swal.fire({
            icon: 'error',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail}`,
          })
          this.$router.replace({path: '/home'});
        }
      }.bind(this))
    },
  },
}
</script>
<!--eslint-disable-->
