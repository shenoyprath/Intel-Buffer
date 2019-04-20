<template>
  <transition
    enter-active-class="animated pulse faster"
    leave-active-class="animated fadeOut faster"
  >
    <div
      class="overlay"
      @click.self="$emit('implicit-close')"
      v-if="isVisible"
    >
      <div
        class="modal"
        v-bind="$attrs"
        v-on="$listeners"
      >
        <base-button
          class="close"
          grow-on-hover
          @click="$emit('explicit-close')"
        />
        <section class="content">
          <header>
            <slot name="modal-header"/>
          </header>

          <slot/>

          <footer>
            <slot name="modal-footer"/>
          </footer>
        </section>
      </div>
    </div>
  </transition>
</template>

<script>
import BaseButton from "@/components/BaseButton"

export default {
  name: "BaseModal",

  components: {
    BaseButton
  },

  inheritAttrs: false,

  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss" scoped>
.overlay {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;

  @if ($background-color == #000) {
    background-color: rgba(0, 0, 0, 0.95);
  } @else if ($background-color == #fff) {
    background-color: rgba(255, 255, 255, 0.95);
  }
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: 100%;
  max-width: 100%;

  height: 100%;
  max-height: 100%;

  z-index: get-z-index(modal, main);
  background-color: $background-color;

  @include media-query(tablet-small) {
    width: 600px;
    height: 400px;

    @if ($background-color == #000) {
      border: 1px solid #6e6e6e;
      box-shadow: 0 4px 8px 0 rgba(255, 255, 255, 0.2),
                  0 6px 20px 0 rgba(255, 255, 255, 0.19);
    } @else if ($background-color == #fff) {
      border: 1px solid #d5d5dc;
      box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2),
                  0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }
    border-radius: 3px;
  }
}

.close {
  display: inline-block;
  position: absolute;
  top: 0;
  right: 0;
  z-index: get-z-index(modal, main);

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
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);

  width: 100%;
  max-width: 100%;
  height: auto;
  max-height: 100%;

  padding: {
    top: 20px;
    bottom: 20px;
    left: 50px;
    right: 50px;
  }
  overflow: auto;

  @include media-query(tablet-small) {
    top: 0;
    transform: none;
    height: 100%;
  }
}
</style>
