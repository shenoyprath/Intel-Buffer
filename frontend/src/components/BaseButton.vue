<template>
  <button
    :class="{
      'grow-on-hover': growOnHover
    }"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <slot/>
  </button>
</template>

<script>
export default {
  name: "BaseButton",

  inheritAttrs: false,

  props: {
    growOnHover: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss" scoped>
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

  background-color: $foreground-color;
  color: $background-color;

  font: {
    family: inherit;
    size: 0.9rem;
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

  &:disabled {
    opacity: 0.65;
    cursor: default;
  }
}

.grow-on-hover {
  @include grow-on-hover;
}
</style>
