<template>
  <base-modal class="registration-modal">
    <template #modal-header>
      <h2>
        Join IntelBuffer.
      </h2>
      <h5>
        {{ registrationBenefits }}
      </h5>
    </template>

    <base-form
      action="/user"
      method="POST"
      :form-data="newUser"
      #default="{ errors }"
    >
      <fieldset name="name">
        <base-input
          label="first name"
          type="text"
          v-model="newUser.firstName"
          :error="errors.firstName"
        />
        <base-input
          label="last name"
          type="text"
          v-model="newUser.lastName"
          :error="errors.lastName"
        />
      </fieldset>

      <fieldset name="credentials">
        <base-input
          label="email address"
          type="email"
          v-model="newUser.emailAddress"
          :error="errors.emailAddress"
          required
        />
        <base-input
          label="password"
          type="password"
          v-model="newUser.password"
          :error="errors.password"
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
      <p>
        <small>
          Already have an account? <a href="/">Sign in</a>
        </small>
      </p>

      <p>
        <small>
          By registering, you agree to our
          <router-link to="/">Terms</router-link> and
          <router-link to="/">Privacy Policy</router-link>
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
  name: "ModalAuthenticationRegister",

  components: {
    BaseButton,
    BaseInput,
    BaseForm,
    BaseModal
  },

  props: {
    registrationBenefits: {
      type: String,
      default: (
        "Tailor your experience, " +
        "follow your favorite authors, " +
        "and share your knowledge."
      )
    }
  },

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
.registration-modal /deep/ .container {
  text-align: center;

  @include media-query(tablet-small) {
    width: 650px;
    height: 460px;
  }
}
</style>
