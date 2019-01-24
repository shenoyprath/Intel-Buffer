<template>
  <div class="splash-screen">
    <logo></logo>
    <h2>A buffer to store your knowledge while it gets downloaded by others</h2>
  </div>
</template>

<script>
import Logo from '@/components/Logo'

export default {
  name: 'SplashScreen',
  components: {
    'logo': Logo
  }
}
</script>

<style lang="scss" scoped>
.splash-screen {
  @include full-size;
  @include center;

  background-color: $background-color;
  z-index: get-z-index(main);

  padding: {
    left: 10px;
    right: 10px;
  }
}
</style>
