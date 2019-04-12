<template>
  <div class="authentication-modal-container animated fadeIn slow">
    <button class="close">&#x2715;</button>

    <div class="authentication-modal animated slideInUp">
      <base-logo height="25pt"/>
      <h2>Register to Personalize IntelBuffer</h2>
      <p class="description">
        Become a member to personalize your content, follow your favorite authors, and share your knowledge
      </p>

      <form class="animated zoomIn delay-1s">
        <input
          id="first-name"
          type="text"
          placeholder="First Name"
          autofocus
        />
        <input
          id="last-name"
          type="text"
          placeholder="Last Name"
        />

        <input
          id="email"
          type="email"
          placeholder="Email Address"
        />
        <input
          id="password"
          type="password"
          placeholder="Password"
        />
      </form>

      <p>
        By clicking register, you agree to our
        <router-link to="/">Terms</router-link>
      </p>
      <button>Register</button>
      <p>
        Already registered?
        <router-link to="/">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import BaseLogo from "@/components/BaseLogo"

export default {
  name: "ModalAuthenticationRegister",

  components: {
    BaseLogo
  }
}
</script>

<style lang="scss" scoped>

</style>
