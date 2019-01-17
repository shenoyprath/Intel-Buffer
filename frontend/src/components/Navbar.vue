<template>
  <nav class="navbar">
    <router-link to="/"><logo></logo></router-link>
    <button class="hamburger">
      <span></span>
    </button>
  </nav>
</template>

<script>
import Logo from '@/components/Logo'

export default {
  name: 'navbar',
  components: {
    'logo': Logo
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 10px;

  overflow: hidden;
  display: flex;
  justify-content: space-between;
  align-items: center;

  * {
    position: relative;
    display: inline;
    vertical-align: middle;

    color: $foreground-color;
  }

  a {
    border: none; // override global a element's bottom border
  }
}

.navbar-btn {
  @include grow-on-hover();
}

.logo {
  height: 40px;
}

.hamburger {
  background-color: transparent;
  padding: 10px;

  // span is the middle line in the hamburger, ::before is the upper line, ::after is the lower line.
  span {
    position: relative;
    background-color: $foreground-color;

    &, &::before, &::after {
      display: block;

      height: 4px;
      width: 2em;

      border-radius: 10px;
    }

    &::before, &::after {
      content: "";
      position: absolute;
    }

    $gap-to-middle: 8px;
    &::before {
      background-color: $theme-silver;
      bottom: $gap-to-middle;
      transition: bottom .2s ease-out,
      transform .2s ease-out .2s;
    }

    &::after {
      background-color: $theme-blue;
      top: $gap-to-middle;
      transition: top .2s ease-out,
      transform .2s ease-out .2s;
    }
  }

  @include if-hover-supported {
    &:hover {
      span::before {
        bottom: 0;
      }
      span::after {
        top: 0;
      }
      span::before, span::after {
        transform: rotateZ(-90deg);
      }
    }
  }
}
</style>
