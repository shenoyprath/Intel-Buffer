<template>
  <div class="authentication-modal-container animated fadeIn slow">
    <div class="authentication-modal animated slideInUp">
      <base-logo height="25pt"/>
      <h2>Sign in to Continue</h2>

      <form class="animated zoomIn delay-1s">
        <input
          id="email"
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
      <button>Sign In</button>
      <p>
        Don't have an account?
        <router-link to="/">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import BaseLogo from '@/components/BaseLogo'

export default {
  name: 'SignIn',
  components: {
    'base-logo': BaseLogo
  }
}
</script>

<style lang="scss" scoped>
@import '../styles/mixins/authentication_modal.scss';

@include authentication-modal;
</style>
