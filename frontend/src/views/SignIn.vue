<template>
  <div class="sign-in animated fadeIn slow">
    <div class="sign-in-modal animated slideInUp">
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
.sign-in {
  @include full-size;
  @include center;

  z-index: get-z-index(modal, main);
  @if ($background-color == #000) {
    background: rgba(0, 0, 0, 0.4);
  } @else if ($background-color == #fff) {
    background: rgba(255, 255, 255, 0.4);
  }
}

.sign-in-modal {
  @include center;

  height: 100%;
  min-height: 575px;
  min-width: 100%;

  color: $foreground-color;
  border-radius: 10px;
  border: none;

  padding: {
    top: 10px;
    bottom: 10px;
  }

  @include media-query(tablet-small) {
    min-width: 0;
    max-width: 850px;

    @if ($background-color == #000) {
      border: 1px solid #6e6e6e;
    } @else if ($background-color == #fff) {
      border: 1px solid #d5d5dc;
    }
  }

  * {
    margin: {
      top: 10px;
      bottom: 10px;
    }
  }

  input {
    width: 75%;
    max-width: 350px;
    height: 50px;
    padding: 10px 2px;

    border: none;
    border-radius: 0;
    border-bottom: 2px solid $foreground-color;
    transition: border-bottom .3s ease-in-out;

    color: $foreground-color;
    background-color: $background-color;
    box-shadow: none;
    outline: none;
    appearance: none;

    font-size: 20px;
    margin: {
      left: 10px;
      right: 10px;
    }

    &::placeholder {
      color: $foreground-color;
      opacity: .4;
    }

    &:focus {
      border-bottom: 4px solid $theme-blue;
    }
  }

  button {
    @include grow-on-hover;

    color: $background-color;
    background-color: $foreground-color;
  }
}
</style>
