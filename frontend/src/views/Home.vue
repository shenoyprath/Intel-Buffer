<template>
  <div class="home">
    <the-splash-screen
      class="animated fadeOut slow delay-2s"
      v-if="isSplashVisible"
    />

    <div
      class="animated fadeIn"
      v-else
    >
      <navbar/>
    </div>
  </div>
</template>

<script>
import TheSplashScreen from "@/components/TheSplashScreen"
import Navbar from "../components/Navbar"

export default {
  name: "home",

  components: {
    "the-splash-screen": TheSplashScreen,
    "navbar": Navbar
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
