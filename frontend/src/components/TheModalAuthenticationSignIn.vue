<template>
  <base-modal
    class="sign-in-modal"
    width="500px"
    height="500px"
    :floating="mediaMinWidth.phoneTablet"
    @close="obviateAuth"
  >
    <template #modal-header>
      <modal-authentication-headnote
        title="Welcome Back!"
        :subtitle="
          authCoaxing ||
          'Access your personalized content and connect with your audience.'
        "
      />
    </template>

    <base-form
      action="/auth-token"
      method="POST"
      :form-data="credentials"
      @valid="setUser"
      #default="{ errors }"
    >
      <fieldset name="credentials">
        <base-input
          label="email address"
          type="email"
          :error="errors.emailAddress"
          v-model="credentials.emailAddress"
          required
        />
        <base-input
          label="password"
          type="password"
          :error="errors.password"
          v-model="credentials.password"
          required
        />
      </fieldset>

      <base-button
        type="submit"
        grow-on-hover
      >
        Sign in
      </base-button>
    </base-form>

    <template #modal-footer>
      <modal-authentication-footnote>
        <router-link to="#">
          Forgot password?
        </router-link>
      </modal-authentication-footnote>

      <modal-authentication-footnote>
        Don't have an account?
        <a @click.prevent="requireRegistration">
          Create one
        </a>
      </modal-authentication-footnote>
    </template>
  </base-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

import BaseForm from "@/components/BaseForm"
import BaseInput from "@/components/BaseInput"
import BaseModal from "@/components/BaseModal"
import BaseButton from "@/components/BaseButton"
import ModalAuthenticationHeadnote from "@/components/ModalAuthenticationHeadnote"
import ModalAuthenticationFootnote from "@/components/ModalAuthenticationFootnote"

import mediaQuery from "@/mixins/media-query"

export default {
  name: "TheModalAuthenticationSignIn",

  components: {
    BaseForm,
    BaseInput,
    BaseModal,
    BaseButton,
    ModalAuthenticationHeadnote,
    ModalAuthenticationFootnote
  },

  mixins: [
    mediaQuery
  ],

  data () {
    return {
      credentials: {
        emailAddress: "",
        password: ""
      }
    }
  },

  computed: {
    ...mapGetters("authenticationModal", [
      "authCoaxing"
    ])
  },

  methods: {
    ...mapActions("authenticationModal", [
      "requireRegistration",
      "obviateAuth"
    ]),

    ...mapActions("currentUser", [
      "setUser"
    ])
  }
}
</script>

<style lang="scss" scoped>
.sign-in-modal {
  text-align: center;
}
</style>
