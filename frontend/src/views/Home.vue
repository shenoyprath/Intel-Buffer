<template>
  <div class="home">
    <splash-screen class="animated fadeOut slow delay-2s" v-if="isSplashVisible"></splash-screen>

    <div class="animated fadeIn" v-else>
      <navbar></navbar>
    </div>
  </div>
</template>

<script>
import SplashScreen from '@/components/SplashScreen'
import Navbar from '../components/Navbar'

export default {
  name: 'home',
  components: {
    'splash-screen': SplashScreen,
    'navbar': Navbar
  },
  data () {
    return {
      isSplashVisible: true
    }
  },
  mounted () {
    setTimeout(() => {
      this.isSplashVisible = false
    }, 4000)
  }
}
</script>
