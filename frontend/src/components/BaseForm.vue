<template>
  <form
    v-bind="$attrs"
    v-on="$listeners"
    @submit.prevent="submitForm"
  >
    <transition
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
    >
      <p
        class="schema-error"
        v-show="errors._schema"
      >
        {{ errors._schema }}
      </p>
    </transition>
    <slot :errors="errors"/>
  </form>
</template>

<script>
import api from "@/rest-api/api"

export default {
  name: "BaseForm",

  inheritAttrs: false,

  props: {
    action: {
      type: String,
      required: true,
      validator: (action) => action.startsWith("/")
    },

    method: {
      type: String,
      required: true,
      validator (method) {
        return [
          "DELETE",
          "GET",
          "PATCH",
          "POST",
          "PUT"
        ].includes(method.toUpperCase())
      }
    },

    formData: {
      type: Object
    }
  },

  data () {
    return {
      errors: {
        _schema: ""
      }
    }
  },

  methods: {
    async submitForm () {
      this.errors = {}
      try {
        const response = await api({
          url: this.action,
          method: this.method,
          data: this.formData
        })
        this.$emit("valid", response.data)
      } catch (e) {
        // to preserve real estate, only 1st error of each field must be shown.
        for (const [fieldName, errors] of Object.entries(e.response.data.errors)) {
          this.$set(this.errors, fieldName, errors[0])
        }
        this.$emit("invalid") // parent should access errors only in slot.
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.schema-error {
  display: block;
  padding: 10px;

  color: #ff0000;
  border: {
    color: #ff0000;
    radius: 5px;
    style: solid;
    width: 1px;
  }
  text-align: center;
  font-size: 13px;
}

fieldset {
  border: none;
  margin: 0;
  padding: 0;
}
</style>
