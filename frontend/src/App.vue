<template>
  <div id="app">
    <splash-screen v-if="isSplashVisible" class="animated fadeOut slower delay-2s"></splash-screen>
    <router-view v-else class="animated fadeIn delay-1s"/>
  </div>
</template>

<script>
import SplashScreen from '@/components/SplashScreen'

export default {
  data () {
    return {
      isSplashVisible: true
    }
  },
  computed: {
    isTouchDevice () {
      const vendorPrefixes = ' -webkit- -moz- -o- -ms- '.split(' ')
      // noinspection JSUnresolvedVariable
      if (('ontouchstart' in window) ||
        // eslint-disable-next-line no-undef
        (window.DocumentTouch && document instanceof DocumentTouch)) {
        return true
      }

      const query = ['(', vendorPrefixes.join('touch-enabled),('), 'heartz', ')'].join('')
      const mq = query => window.matchMedia(query).matches
      return mq(query)
    }
  },
  components: {
    'splash-screen': SplashScreen
  },
  mounted () {
    setTimeout(() => {
      this.isSplashVisible = false
    }, 4000)
  }
}
</script>

<style lang="scss">
@import url('https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css');
@import url('https://fonts.googleapis.com/css?family=Eczar:600|Work+Sans:400,700');
@import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.7.0/animate.min.css');
@import url('https://use.fontawesome.com/releases/v5.6.3/css/all.css');

*,
*::before,
*::after {
  box-sizing: border-box;
}

a {
  color: $theme-blue;
  text-decoration: none;

  @include if-hover-enabled {
    &:hover,
    &:focus {
      border: {
        bottom: {
          width: 1px;
          style: solid;
          color: $theme-blue;
        }
      }
    }
  }
}

b {
  font-weight: 700;
}

button {
  display: inline-block;
  overflow: visible;

  vertical-align: middle;
  line-height: 1.5;
  white-space: nowrap;

  padding: 0.375rem 0.75rem;
  outline: none;
  margin: 0;
  user-select: none;

  cursor: pointer;
  transition: all .2s ease-in-out;

  font: {
    family: inherit;
    size: 1rem;
    weight: 400;
  }

  text: {
    transform: none;
    align: center;
  }

  border: {
    width: 1px;
    style: solid;
    color: transparent;
    radius: 0.25em;
  }
}

h1, h2, h3, h4, h5, h6 {
  font: {
    family: 'Eczar', serif;
    weight: 600;
  }
}

#{$app} {
  background-color: $background-color;
  color: $foreground-color;

  min-width: 100%;
  min-height: 100%;

  top: 0;
  left: 0;
  position: absolute;
  z-index: get-z-index(main);
  margin: 0;

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  font: {
    family: 'Work Sans', sans-serif;
    weight: 400;
  }
}
</style>
