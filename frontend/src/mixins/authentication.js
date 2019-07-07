import { mapGetters, mapMutations } from "vuex"

export default {
  computed: {
    ...mapGetters("authenticationProcess", [
      "authCoaxing"
    ])
  },

  methods: {
    ...mapMutations("authenticationProcess", [
      "obviateAuth",
      "toggleAccountExistence"
    ]),

    ...mapMutations("user", [
      "setCurrentUser"
    ]),

    authenticateUser (user) {
      this.setCurrentUser(user)
      this.obviateAuth()
    }
  }
}
