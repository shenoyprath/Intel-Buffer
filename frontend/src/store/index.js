import Vue from "vue"
import Vuex from "vuex"

import mediaQuery from "@/store/modules/media-query"
import user from "@/store/modules/user"

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    mediaQuery,
    user
  }
})
