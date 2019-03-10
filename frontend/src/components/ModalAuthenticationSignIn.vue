<template>
  <div class="authentication-modal-container animated fadeIn slow">
    <button class="close">&#x2715;</button>

    <div class="authentication-modal animated slideInUp">
      <base-logo height="25pt"/>
      <h2>Sign in to Continue</h2>
      <p class="description">
        Access your personalized content and interact with others
      </p>

      <form
        id="sign-in-form"
        class="animated zoomIn delay-1s"
      >
        <input
          id="email-address"
          type="email"
          placeholder="Email Address"
          autofocus
        />
        <input
          id="password"
          type="password"
          placeholder="Password"
        />
      </form>

      <router-link to="/">Forgot Password?</router-link>
      <button
        type="submit"
        form="sign-in-form"
      >
        Sign In
      </button>

      <p>
        Don't have an account?
        <router-link to="/">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import BaseLogo from "@/components/BaseLogo"

export default {
  name: "ModalAuthenticationSignIn",

  components: {
    "base-logo": BaseLogo
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/mixins/authentication_modal";

@include authentication-modal;
</style>
