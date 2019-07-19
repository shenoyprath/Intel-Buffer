<template>
  <base-modal
    class="registration-modal"
    width="650px"
    height="480px"
    :floating="mqMinWidth.tabletSmall"
    @close="obviateAuth"
  >
    <template #modal-header>
      <modal-authentication-headnote
        title="Join IntelBuffer."
        :subtitle="
          authCoaxing ||
          'Tailor your experience, interact with your favorite authors, and share your knowledge.'
        "
      />
    </template>

    <base-form
      action="/user"
      method="POST"
      :form-data="newUser"
      @valid="authenticateUser"
      #default="{ errors }"
    >
      <fieldset name="identity">
        <base-input
          label="first name"
          type="text"
          :error="errors.firstName"
          v-model="newUser.firstName"
          required
        />
        <base-input
          label="last name"
          type="text"
          :error="errors.lastName"
          v-model="newUser.lastName"
          required
        />
      </fieldset>

      <fieldset name="credentials">
        <base-input
          label="email address"
          type="email"
          :error="errors.emailAddress"
          v-model="newUser.emailAddress"
          required
        />
        <base-input
          label="password"
          type="password"
          :error="errors.password"
          v-model="newUser.password"
          required
        />
      </fieldset>

      <base-button
        type="submit"
        grow-on-hover
      >
        Register
      </base-button>
    </base-form>

    <template #modal-footer>
      <modal-authentication-footnote>
        By registering, you agree to our
        <router-link to="#">
          Terms
        </router-link> and
        <router-link to="#">
          Privacy Policy
        </router-link>
      </modal-authentication-footnote>

      <modal-authentication-footnote>
        Already have an account?
        <a @click.prevent="makeAccountExistent">
          Sign in
        </a>
      </modal-authentication-footnote>
    </template>
  </base-modal>
</template>

<script>
import BaseForm from "@/components/BaseForm"
import BaseInput from "@/components/BaseInput"
import BaseModal from "@/components/BaseModal"
import BaseButton from "@/components/BaseButton"
import ModalAuthenticationHeadnote from "@/components/ModalAuthenticationHeadnote"
import ModalAuthenticationFootnote from "@/components/ModalAuthenticationFootnote"

import authentication from "@/mixins/authentication"
import mediaQuery from "@/mixins/media-query"

export default {
  name: "TheModalAuthenticationRegister",

  components: {
    BaseForm,
    BaseInput,
    BaseModal,
    BaseButton,
    ModalAuthenticationHeadnote,
    ModalAuthenticationFootnote
  },

  mixins: [
    authentication,
    mediaQuery
  ],

  data () {
    return {
      newUser: {
        firstName: "",
        lastName: "",

        emailAddress: "",
        password: ""
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.registration-modal {
  text-align: center;
}
</style>
