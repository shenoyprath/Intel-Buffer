<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  computed: {
    isTouchDevice () {
      const vendorPrefixes = " -webkit- -moz- -o- -ms- ".split(" ")
      // noinspection JSUnresolvedVariable
      if (("ontouchstart" in window) ||
        // eslint-disable-next-line no-undef
        (window.DocumentTouch && document instanceof DocumentTouch)) {
        return true
      }

      const query = ["(", vendorPrefixes.join("touch-enabled),("), "heartz", ")"].join("")
      const mq = query => window.matchMedia(query).matches
      return mq(query)
    }
  }
}
</script>

<style lang="scss">
@import url("https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css");
@import url("https://fonts.googleapis.com/css?family=Eczar:600|Work+Sans:400,700");
@import url("https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.7.0/animate.min.css");

*,
*::before,
*::after {
  box-sizing: border-box;
}

a {
  color: $theme-blue;
  text-decoration: none;

  @include if-hover-enabled {
    &:hover, &:focus {
      border-bottom: 1px solid $theme-blue;
    }
  }
}

b {
  font-weight: 700;
}

h1, h2, h3, h4, h5, h6 {
  font: {
    family: "Eczar", serif;
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
    family: "Work Sans", sans-serif;
    weight: 400;
  }
}
</style>
