<template>
  <button
    v-bind="$attrs"
    v-on="$listeners"
    :class="{
      'grow-on-hover': growOnHover
    }"
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

.grow-on-hover {
  @include grow-on-hover;
}
</style>
