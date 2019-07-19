import { mapActions, mapGetters, mapMutations } from "vuex"

export default {
  computed: {
    ...mapGetters("authenticationProcess", [
      "authCoaxing"
    ])
  },

  methods: {
    ...mapMutations("authenticationProcess", [
      "obviateAuth",
      "makeAccountExistent",
      "makeAccountNonexistent"
    ]),

    ...mapActions("authenticationProcess", [
      "authenticateUser"
    ])
  }
}
