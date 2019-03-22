<template>
  <transition
    enter-active-class="animated zoomIn faster"
    leave-active-class="animated zoomOut faster"
  >
    <div
      class="modal"
      v-if="isVisible"
    >
      <button
        class="close"
        @click="hide"
      >
      </button>

      <section class="content">
        <slot name="header"/>

        <slot name="body"/>

        <slot name="footer"/>
      </section>
    </div>
  </transition>
</template>

<script>
export default {
  name: "BaseModal",

  data: () => ({
    isVisible: false
  }),

  methods: {
    show () {
      this.isVisible = true
    },

    hide () {
      this.isVisible = false
    }
  }
}
</script>

<style lang="scss" scoped>
.modal {
  @include center;
  @include full-size;

  position: fixed;
  top: 0;
  left: 0;
  z-index: get-z-index(modal, main);

  // If opacity is defined separately, it carries over to child elements.
  @if ($background-color == #000) {
    background-color: rgba(0, 0, 0, 0.97);
  } @else if ($background-color == #fff) {
    background: rgba(255, 255, 255, 0.97);
  }
}

.close {
  @include grow-on-hover;

  display: inline-block;
  position: absolute;
  top: 0;
  left: 0;

  width: 40px;
  height: 40px;
  overflow: hidden;

  background-color: transparent;
  padding: 0;

  &::before, &::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 0;

    height: 1px;
    width: 100%;
    margin-top: -1px;

    background-color: $foreground-color;
  }

  &::before {
    transform: rotate(45deg);
  }

  &::after {
    transform: rotate(-45deg);
  }
}

.content {
  background-color: $background-color;
  text-align: left;
  max: {
    width: 100vw;
    height: 90vh;
  }
  overflow: {
    x: hidden;
    y: scroll;
  }
  padding: 10px;

  @include media-query(phone-tablet) {
    max-width: 90vw;
  }
}
</style>
