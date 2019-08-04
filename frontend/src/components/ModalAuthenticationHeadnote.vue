<template>
  <div>
    <h2>
      {{ title }}
    </h2>

    <h5>
      {{ subtitle }}
    </h5>
  </div>
</template>

<script>
export default {
  name: "ModalAuthenticationHeadnote",

  props: {
    title: {
      type: String,
      required: true,
      validator: (title) => title
    },

    subtitle: {
      type: String,
      required: true,
      validator: (subtitle) => subtitle
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
