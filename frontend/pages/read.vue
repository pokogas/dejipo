<template>
  <div class="fullscreen">
    <qrcode-stream :camera="camera" @decode="onDecode" @init="onInit">
      <div id="loading" v-if="loading">
        <v-progress-circular indeterminate/>
      </div>
    </qrcode-stream>
  </div>
</template>

<script>
export default {
  layout: 'Main',
  head() {
    return {
      title: '読み取り'
    }
  },
  data() {
    return {
      camera: 'auto',
      result: null,
      showScanConfirmation: false,
      loading: false,
      destroyed: false,
    }
  },
  methods: {
    errorModal(error_mes) {
      this.$swal.fire({
        icon: 'error',
        position: 'top-end',
        toast: true,
        showConfirmButton: false,
        timer: 2500,
        title: `${error_mes}`,
      })
    },
    receive(op_name, usage, point, t_id) {
      this.$axios.$post(`api/transaction/?id=${t_id}`).then(function (res) {
        if (res.result === "OK") {
          this.$swal.fire({
            icon: 'success',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail.op_name} ${res.detail.point}ポイント受け取りました。`,
          })
          return this.unpause()
        } else if (res.result === "NO") {
          this.errorModal(res.detail)
          return this.unpause()
        }
      }.bind(this))
    },
    payment(op_name, usage, point, t_id) {
      this.$axios.$post(`api/transaction/?id=${t_id}`).then(function (res) {
        if (res.result === "OK") {
          this.$swal.fire({
            icon: 'success',
            position: 'top-end',
            toast: true,
            showConfirmButton: false,
            timer: 2500,
            title: `${res.detail.op_name} ${res.detail.point}ポイントを支払いました。`,
          })
          return this.unpause()
        } else if (res.result === "NO") {
          this.errorModal(res.detail)
          return this.unpause()
        }
      }.bind(this));
    },
    transactionModal(op_name, usage, point, t_id) {
      let str_usage = "";
      if (usage === 1) {
        str_usage = "支払い"
      } else if (usage === 2) {
        str_usage = "受け取る"
      }
      this.$swal.fire({
        title: `${str_usage}`,
        html: "<div class=\"grey--text text--darken-2 text-center\">" + `<p>${op_name}</p><br><p>${point}P</p>` + "</div>",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: `${str_usage}`,
        cancelButtonText: "キャンセル"
      }).then((result) => {
        if (result.isConfirmed) {
          if (usage === 1) {
            this.payment(op_name, usage, point, t_id)
          } else if (usage === 2) {
            this.receive(op_name, usage, point, t_id)
          }
        }
        this.unpause()
      })
    },
    async getTransaction(url) {
      let transaction_id = url.split("/")[4]
      if (url.split("/")[3] !== "transaction") {
        this.errorModal("無効なQRコードです")
        return this.unpause()
      }
      let transactionData = null
      await this.$axios.get(`api/transaction/?id=${transaction_id}`).then(function (res) {
        transactionData = res
      }.bind(this))
      if (transactionData.data.result === "NO") {
        this.errorModal(transactionData.data.detail)
        return this.unpause()
      }
      const t = transactionData.data.detail
      this.transactionModal(t.op_name, t.usage, t.point, t.id)

    },
    async onInit (promise) {
      this.loading = true
      try {
        await promise
      } catch (e) {
        // eslint-disable-next-line no-undef
        if (e.name === 'NotAllowedError') {
          this.errorModal('この機能を使用するためにはカメラの許可が必要です。')
        }
      } finally {
        this.showScanConfirmation = this.camera === "off"
        this.loading = false
      }
    },
    async onDecode(content) {
      this.result = content
      this.pause()
      await this.getTransaction(content)
    },

    unpause() {
      this.camera = 'auto'
    },

    pause() {
      this.camera = 'off'
    },
    async reload() {
      this.destroyed = true

      await this.$nextTick()

      this.destroyed = false
    },

    timeout(ms) {
      return new Promise(resolve => {
        window.setTimeout(resolve, ms)
      })
    }
  }
}
</script>
<style>
.fullscreen {
  position: fixed;
  z-index: 1;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
}

#loading {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  z-index: 9999;
  position: fixed;
  background-color: rgba(26, 42, 51, 0.72);
}

.page-enter-active, .page-leave-active {
  transition: opacity 0.1s
}

.page-enter, .page-leave-active {
  opacity: 0
}
</style>
