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
  background-color: $background-color;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;

  height: 100vh;
  width: 100vw;
  z-index: get-z-index(main);

  padding: {
    left: 10px;
    right: 10px;
  }
}
</style>
