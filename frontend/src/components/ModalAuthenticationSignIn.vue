<template>
  <base-modal class="sign-in-modal">
    <template #modal-header>
      <h2>
        Welcome Back!
      </h2>
      <h5>
        Sign in to access your personalized content and connect with others.
      </h5>
    </template>

    <base-form
      action="/auth-token"
      method="POST"
      :form-data="credentials"
      #default="{ errors }"
    >
      <fieldset name="credentials">
        <base-input
          class="credentials"
          label="email address"
          type="email"
          v-model="credentials.emailAddress"
          :error="errors.emailAddress"
          required
        />
        <base-input
          class="credentials"
          label="password"
          type="password"
          v-model="credentials.password"
          :error="errors.password"
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
      <p>
        <small>
          <a href="/">Forgot password?</a>
        </small>
      </p>

      <p>
        <small>
          Don't have an account?
          <router-link to="/">Register</router-link>
        </small>
      </p>
    </template>
  </base-modal>
</template>

<script>
import BaseModal from "@/components/BaseModal"
import BaseForm from "@/components/BaseForm"
import BaseInput from "@/components/BaseInput"
import BaseButton from "@/components/BaseButton"

export default {
  name: "ModalAuthenticationSignIn",

  components: {
    BaseButton,
    BaseInput,
    BaseForm,
    BaseModal
  },

  data () {
    return {
      credentials: {
        emailAddress: "",
        password: ""
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.sign-in-modal /deep/ .container {
  text-align: center;

  @include media-query(tablet-small) {
    width: 650px;
    height: 450px;
  }
}

.credentials {
  display: block;
  margin: {
    left: auto;
    right: auto;
  }
}
</style>
