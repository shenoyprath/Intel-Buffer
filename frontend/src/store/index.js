import Vue from "vue"
import Vuex from "vuex"

import responsiveDesign from "@/store/modules/responsive-design"
import user from "@/store/modules/user"

Vue.use(Vuex)

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",

  modules: {
    responsiveDesign,
    user
  }
})
