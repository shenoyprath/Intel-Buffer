<template>
  <div class="the-splash-screen">
    <base-logo/>
    <h2>A buffer to store your knowledge while it gets downloaded by others</h2>
  </div>
</template>

<script>
import BaseLogo from '@/components/BaseLogo'

export default {
  name: 'TheSplashScreen',

  components: {
    'base-logo': BaseLogo
  }
}
</script>

<style lang="scss" scoped>
.the-splash-screen {
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
