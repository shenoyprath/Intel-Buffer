export default {
  namespaced: true,

  state: {
    windowWidth: null,

    /*
     * Frozen to tell Vuex that the object is non-reactive.
     */
    breakpointWidths: Object.freeze({
      phoneSmall: 320,
      phone: 400,
      phoneWide: 480,
      phoneTablet: 560,

      tabletSmall: 640,
      tablet: 768,
      tabletWide: 1024,

      desktop: 1248,
      desktopWide: 1440
    })
  },

  getters: {
    /**
     * Returns an object detailing whether `@media (min-width: <breakpoint width>)`
     * is active for each breakpoint width. `mqMaxWidth` not provided to enforce
     * mobile-first design. If absolutely necessary, just use negation.
     * See issue #18 for more details on implementation.
     */
    mqMinWidth (state) {
      const query = {}
      for (const [breakpoint, width] of Object.entries(state.breakpointWidths)) {
        query[breakpoint] = (state.windowWidth >= width)
      }
      return query
    }
  },

  mutations: {
    updateWindowWidth (state) {
      state.windowWidth = window.innerWidth
    }
  },

  actions: {
    initResponsiveDesign ({ commit }) {
      commit("updateWindowWidth")
      window.addEventListener(
        "resize",
        commit.bind(null, "updateWindowWidth")
      )
    }
  }
}
