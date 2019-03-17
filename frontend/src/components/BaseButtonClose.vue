<template>
  <button class="close"></button>
</template>

<script>
export default {
  name: "BaseButtonClose"
}
</script>

<style lang="scss" scoped>
.close {
  @include grow-on-hover;

  position: relative;
  display: inline-block;

  width: 50px;
  height: 50px;
  overflow: hidden;

  background-color: transparent;

  &::before, &::after {
    content: '';
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
</style>
