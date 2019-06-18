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
    }
  },

  mutations: {
    setCurrentUser (state, { id, firstName, lastName }) {
      state.id = id
      state.firstName = firstName
      state.lastName = lastName
    }
  },

  actions: {}
}
