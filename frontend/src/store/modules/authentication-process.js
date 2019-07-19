export default {
  namespaced: true,

  state: {
    isAuthRequired: false,
    accountExists: false,
    authBenefits: null
  },

  getters: {
    canStartAuthProcess (state, getters, rootState, rootGetters) {
      return state.isAuthRequired && rootGetters["user/isUserAnonymous"]
    },

    authCoaxing (state) {
      if (!state.authBenefits) {
        return ""
      }

      if (state.accountExists) {
        return `Sign in to ${state.authBenefits}.`
      }
      return `Create an account to ${state.authBenefits}.`
    }
  },

  mutations: {
    requireAuth (state) {
      state.isAuthRequired = true
    },

    obviateAuth (state) {
      state.isAuthRequired = false
      state.accountExists = false
      state.authBenefits = null
    },

    makeAccountExistent (state) {
      state.accountExists = true
    },

    makeAccountNonexistent (state) {
      state.accountExists = false
    },

    setAuthBenefits (state, authBenefits) {
      state.authBenefits = authBenefits
    }
  },

  actions: {
    authenticateUser ({ commit }, { id, firstName, lastName }) {
      commit(
        "user/setCurrentUser",
        { id, firstName, lastName },
        { root: true }
      )
      commit("obviateAuth")
    }
  }
}
