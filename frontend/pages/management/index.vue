<template>
  <v-main>
    <v-container>
      <v-card elevation="0">
        <v-toolbar elevation="0">
          <v-toolbar-title>Original Point</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-list-item-action>
            <v-btn
              color="indigo lighten-2"
              elevation="0"
              class="font-weight-bold white--text"
              to="/management/create">
              作成
            </v-btn>
          </v-list-item-action>
        </v-toolbar>
        <v-data-table height="500px" hide-default-footer
                      :headers="headers"
                      :items="mgOpList">
          <template v-slot:item.permission_level="{ item }">
            <v-chip
              :color="getPermissionColor(item.permission_level)"
              dark
            >
              <span v-if="item.permission_level ===1">Admin</span>
              <span v-if="item.permission_level ===2">Staff</span>
            </v-chip>
          </template>
          <template v-slot:item.action="{item}">
            <v-btn icon :to="`/management/${item.op.name}`">
              <v-icon>
                mdi-open-in-new
              </v-icon>
            </v-btn>
          </template>
          <template v-slot:no-data>管理しているOriginalPointがありません。
          </template>
        </v-data-table>
      </v-card>
    </v-container>
  </v-main>
</template>
<script>
export default {
  layout: "management/Top",
  head() {
    return {
      title: `ホーム`,
      titleTemplate: 'DEJIPO-Management'
    }
  },
  computed: {
    auth() {
      return this.$auth
    },
    user() {
      return this.$auth.user;
    }
  },
  data() {
    return {
      mgOpList: [],
      headers: [
        {text: 'OP名', value: 'op.name', align: 'start',},
        {text: '利用者数', value: 'op.user_count'},
        {text: '累計発行数', value: 'op.total_issuing_number'},
        {text: '権限レベル', value: 'permission_level'},
        {text: '', value: 'action', sortable: false},
      ],
    }
  },
  methods: {
    logout() {
      return this.$auth.logout()
    },
    async setData() {
      await this.$axios.$get(`api/management/user-management-op-list/`).then(function (res) {
        this.mgOpList = res
      }.bind(this))
    },
    getPermissionColor(permission_level){
      if (permission_level === 1) return 'green'
      if (permission_level === 2) return 'orange'
    }
  },
  created() {
    this.setData()
  }
}
</script>
