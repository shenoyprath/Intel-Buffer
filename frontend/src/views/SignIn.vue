<template>
  <div class="sign-in animated fadeIn slow">
    <div class="sign-in-modal animated slideInUp">
      <logo height="25pt"></logo>
      <h2>Sign in to Continue</h2>

      <form>
        <input id="email" class="animated zoomIn delay-1s" type="email" placeholder="Email Address" autofocus>
        <input id="password" class="animated zoomIn delay-1s" type="password" placeholder="Password">
      </form>

      <router-link to="/">Forgot Password?</router-link>
      <button>Sign In</button>
      <p>Don't have an account? <router-link to="/">Register</router-link></p>
    </div>
  </div>
</template>

<script>
import Logo from '@/components/Logo'
export default {
  name: 'SignIn',
  components: {
    'logo': Logo
  }
}
</script>

<style lang="scss" scoped>

</style>
