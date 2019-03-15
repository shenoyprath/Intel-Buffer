<template>
  <nav class="navbar">
    <div class="nav-header">
      <router-link to="/">
        <base-logo/>
      </router-link>

      <button
        :class="['hamburger', menuOpenClass]"
        @click="isMenuOpen = !isMenuOpen"
      >
        <span></span>
      </button>
    </div>

    <transition
      enter-active-class="animated bounceInRight"
      leave-active-class="animated bounceOutRight"
    >
      <div
        :class="['nav-menu', menuOpenClass]"
        v-show="isMenuOpen"
      >
          <section
            :key="navSection.name"
            v-for="navSection in navSections"
          >
            <h1>{{ navSection.name }}</h1>

            <ul>
              <li
                class="nav-link"
                v-for="navLink in navSection.links"
                :key="navLink">
                <router-link to="#">{{ navLink }}</router-link>
              </li>
            </ul>
          </section>
      </div>
    </transition>
  </nav>
</template>

<script>
import BaseLogo from '@/components/BaseLogo'

export default {
  name: 'navbar',

  components: {
    'base-logo': BaseLogo
  },

  data () {
    return {
      isMenuOpen: false,

      navSections: {
        personalize: {
          name: 'personalize',
          links: [
            'register',
            'sign in'
          ]
        },

        chronicles: {
          name: 'chronicles',
          links: [
            'most read',
            'latest',
            'featured',
            'heaps',
            'eye appealers',
            'for you',
            'write'
          ]
        },

        news: {
          name: 'news',
          links: [
            'top stories',
            'breaking',
            'opinion'
          ]
        },

        topics: {
          name: 'topics',
          links: [
            'arts',
            'computing',
            'engineering',
            'entertainment',
            'gaming',
            'history',
            'medicine',
            'science',
            'sports',
            'more...'
          ]
        }
      }
    }
  },

  computed: {
    menuOpenClass () {
      return this.isMenuOpen ? 'open' : ''
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  a {
    border: none;
    color: inherit;
  }
}

.nav-header {
  display: flex;
  justify-content: space-between;

  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
  z-index: get-z-index(priority);

  padding: 10px;
  background-color: $background-color;

  * {
    display: inline;
    vertical-align: middle;
  }
}

$menu-open-class: open;

.hamburger {
  background-color: transparent;
  padding: 10px;

  // span is the middle line in the hamburger, ::before is the upper line, ::after is the lower line

  &.#{$menu-open-class} {
    span::before {
      bottom: 0;
    }

    span::after {
      top: 0;
    }
  }

  span {
    position: relative;
    background-color: $foreground-color;

    $gap-to-middle: 8px;
    &::before {
      background-color: $theme-silver;
      bottom: $gap-to-middle;
      transition: bottom .2s ease-out,
      transform .2s ease-out;
    }

    &::after {
      background-color: $theme-blue;
      top: $gap-to-middle;
      transition: top .2s ease-out,
      transform .2s ease-out;
    }

    &::before, &::after {
      content: "";
      position: absolute;
    }

    &, &::before, &::after {
      display: block;

      height: 4px;
      width: 2em;

      border-radius: 10px;
    }
  }

  @include if-hover-enabled {
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

    &.#{$menu-open-class}:hover {
      transform: rotateZ(-45deg);
    }
  }
}

.nav-menu {
  $below-nav-header: 50px; // margin needed to place object directly below the nav-header

  overflow-y: scroll;
  z-index: get-z-index(modal, main);

  margin: {
    top: $below-nav-header;
    bottom: 15px;
  }

  padding: {
    left: 15px;
    right: 15px;
  }

  @include media-query(phone-tablet) {
    max-width: 200px;
    position: absolute;
    right: 0;
    max-height: calc(100vh - #{$below-nav-header});
  }

  h1 {
    margin: {
      top: 30px;
      bottom: 10px;
    }
    text-transform: capitalize;
  }

  ul {
    margin: 0;
    padding: 0;
    list-style: none;
    font-size: 0;
  }
}

.nav-link {
  margin: 15px;
  display: table; // block element without taking 100% of parent width
  font-size: 20px;
  text-transform: capitalize;
  transition: color .2s ease-in-out;

  @include if-hover-enabled {
    &:hover {
      color: $theme-blue;
    }
  }
}
</style>
