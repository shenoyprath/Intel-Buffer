import rwdBreakpointWidths from "@/utils/rwd-breakpoint-widths"

export default {
  namespaced: true,

  state: {
    windowWidth: null
  },

  getters: {
    mqMinWidth (state) {
      return (breakpoint) => {
        return state.windowWidth >= rwdBreakpointWidths[breakpoint]
      }
    },

    mqMaxWidth (state) {
      return (breakpoint) => {
        return state.windowWidth <= rwdBreakpointWidths[breakpoint]
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
