<template>
  <div class="home">
    <navbar></navbar>
  </div>
</template>

<script>
import Navbar from '../components/Navbar'

export default {
  name: 'home',
  components: {
    'navbar': Navbar
  }
}
</script>
