import { mapGetters } from "vuex"

/**
 * Utility mixin to make it easier to use media queries in components.
 */
export default {
  computed: {
    ...mapGetters("responsiveDesign", [
      "mqMinWidth"
    ])
  }
}
