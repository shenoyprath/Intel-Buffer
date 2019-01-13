<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
// noinspection JSUnusedGlobalSymbols
export default {}
</script>

<style lang="scss">
@import url('https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css');
@import url('https://fonts.googleapis.com/css?family=Work+Sans:400,700|Source+Code+Pro:400,700');

// theme colors
$theme-blue: #1e90ff;
$theme-silver: #808080;

*,
*::before,
*::after {
  box-sizing: border-box;
}

@mixin vendor-prefixed($prop, $val) {
  @each $vendor in ('-webkit-', '-moz-', '-ms-', '-o-', '') {
    #{$vendor}#{$prop}: #{$val};
  }
}

#app {
  font: {
    family: 'Work Sans', sans-serif;
    weight: 400;
  }
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  margin: 0;
  background-color: #000;
  color: #fff;

  width: 100vw;
  height: 100vh;

  a {
    color: $theme-blue;
    text-decoration: none;
  }

  &.no-touch a:hover,
  a:focus {
    border: {
      bottom: {
        width: 1px;
        style: solid;
        color: $theme-blue;
      }
    }
  }

  b {
    font-weight: 700;
  }

  button {
    display: inline-block;
    overflow: visible;

    font: {
      family: inherit;
      size: 1rem;
      weight: 400;
    }

    text: {
      transform: none;
      align: center;
    }

    vertical-align: middle;
    line-height: 1.5;
    white-space: nowrap;

    padding: 0.375rem 0.75rem;
    outline: none;
    margin: 0;

    @include vendor-prefixed(user-select, none);

    border: {
      width: 1px;
      style: solid;
      color: transparent;
      radius: 0.25em;
    }

    cursor: pointer;
    @include vendor-prefixed(transition, all .2s ease-in-out)
  }
}
</style>
