import Vue from "vue"
import Vuex from "vuex"

import createPersistedState from "vuex-persistedstate"

import authenticationModal from "@/store/modules/authentication-modal"
import currentUser from "@/store/modules/current-user"
import responsiveDesign from "@/store/modules/responsive-design"

Vue.use(Vuex)

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",

  modules: {
    authenticationModal,
    currentUser,
    responsiveDesign
  },

  plugins: [
    createPersistedState({
      paths: [
        "currentUser"
      ]
    })
  ]
})
