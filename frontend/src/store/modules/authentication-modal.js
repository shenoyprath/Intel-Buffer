export default {
  namespaced: true,

  state: {
    isVisibilityDesired: false,
    componentType: null, // either `register` or `sign-in`.
    authBenefits: null // see `authCoaxing` getter for more context.
  },

  getters: {
    isAuthModalVisible (state, getters, rootState, rootGetters) {
      return state.isVisibilityDesired && rootGetters["currentUser/isUserAnonymous"]
    },

    authModalComponent (state) {
      if (state.componentType) {
        return `the-modal-authentication-${state.componentType}`
      }
      return ""
    },

    authCoaxing (state) {
      if (state.authBenefits) {
        if (state.componentType === "register") {
          return `Create an account to ${state.authBenefits}.`
        } else if (state.componentType === "sign-in") {
          return `Sign in to ${state.authBenefits}.`
        }
      }
      return ""
    }
  },

  mutations: {
    show (state) {
      state.isVisibilityDesired = true
    },

    hide (state) {
      state.isVisibilityDesired = false
    },

    setComponentType (state, { componentType }) {
      state.componentType = componentType
    },

    setAuthBenefits (state, { authBenefits }) {
      state.authBenefits = authBenefits
    }
  },

  actions: {
    _showComponentWithBenefits ({ commit, rootGetters }, { componentType, authBenefits }) {
      if (rootGetters["currentUser/isUserAnonymous"]) {
        commit("show")
        commit({
          type: "setComponentType",
          componentType: componentType
        })
        commit({
          type: "setAuthBenefits",
          authBenefits: authBenefits
        })
      }
    },

    requireRegistration ({ dispatch, state }, { authBenefits = null }) {
      dispatch({
        type: "_showComponentWithBenefits",
        componentType: "register",
        authBenefits: authBenefits
      })
    },

    requireSignIn ({ dispatch }, { authBenefits = null }) {
      dispatch({
        type: "_showComponentWithBenefits",
        componentType: "sign-in",
        authBenefits: authBenefits
      })
    },

    obviateAuth ({ commit }) {
      commit("hide")
      commit({
        type: "setComponentType",
        componentType: null
      })
      commit({
        type: "setAuthBenefits",
        authBenefits: null
      })
    }
  }
}
