import rwdBreakpointWidths from "@/utils/rwd-breakpoint-widths"

export default {
  namespaced: true,

  state: {
    windowWidth: null
  },

  getters: {
    /*
     * `mqMaxWidth` not provided to enforce mobile-first design.
     * If absolutely necessary, return value can obviously be negated.
     */
    mqMinWidth (state) {
      return (breakpoint) => {
        return state.windowWidth >= rwdBreakpointWidths[breakpoint]
      }
    }
  },

  mutations: {
    updateWindowWidth (state) {
      state.windowWidth = window.innerWidth
    }
  },

  actions: {
    initMediaQuery ({ commit }) {
      commit("updateWindowWidth")
      window.addEventListener(
        "resize",
        commit.bind(null, "updateWindowWidth")
      )
    }
  }
}
