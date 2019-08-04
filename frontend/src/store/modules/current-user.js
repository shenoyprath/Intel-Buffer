export default {
  namespaced: true,

  state: {
    id: null,

    firstName: null,
    lastName: null
  },

  getters: {
    isUserAnonymous (state) {
      return state.id == null
    },

    getUser (state) {
      return {
        id: state.id,

        firstName: state.firstName,
        lastName: state.lastName
      }
    }
  },

  mutations: {
    setId (state, { id }) {
      state.id = id
    },

    setFirstName (state, { firstName }) {
      state.firstName = firstName
    },

    setLastName (state, { lastName }) {
      state.lastName = lastName
    }
  },

  actions: {
    setUser ({ commit, dispatch }, { id, firstName, lastName }) {
      commit({
        type: "setId",
        id: id
      })
      commit({
        type: "setFirstName",
        firstName: firstName
      })
      commit({
        type: "setLastName",
        lastName: lastName
      })

      dispatch({
        type: "authenticationModal/obviateAuth"
      }, {
        root: true
      })
    },

    unsetUser ({ commit }) {
      commit({
        type: "setId",
        id: null
      })
      commit({
        type: "setFirstName",
        firstName: null
      })
      commit({
        type: "setLastName",
        lastName: null
      })
    },

    unsetExpiredUser ({ dispatch }) {
      dispatch("unsetUser")
      dispatch({
        type: "authenticationModal/requireSignIn",
        authBenefits: "renew your session and regain access to your account"
      }, {
        root: true
      })
    }
  }
}
