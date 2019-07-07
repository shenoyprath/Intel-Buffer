import Vue from "vue"
import Vuex from "vuex"

import createPersistedState from "vuex-persistedstate"

import authenticationProcess from "@/store/modules/authentication-process"
import responsiveDesign from "@/store/modules/responsive-design"
import user from "@/store/modules/user"

Vue.use(Vuex)

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",

  modules: {
    authenticationProcess,
    responsiveDesign,
    user
  },

  plugins: [
    createPersistedState({
      paths: [
        "user"
      ]
    })
  ]
})
