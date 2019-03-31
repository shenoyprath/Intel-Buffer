<template>
  <div
    class="input-root animated"
    :class="{
      shake: error
    }"
    :style="{
      width: `${size}em`
    }"
  >
    <transition
      enter-active-class="animated fadeInUp faster"
      leave-active-class="animated fadeOutDown faster"
    >
      <label
        class="floating-label"
        :class="{
          focus: isFocus,
          error: error
        }"
        :for="id"
        v-show="isFocus || currentValue"
      >
        {{ label }}
      </label>
    </transition>

    <!-- Fading is not required for the character count. Sliding is good enough. -->
    <transition
      enter-active-class="animated slideInUp faster"
      leave-active-class="animated slideOutDown faster"
    >
      <span
        class="maxlength"
        v-if="isFocus && Number.isFinite(maxlength)"
      >
        {{ currentLength }}/{{ maxlength }}
      </span>
    </transition>

    <div class="fix-to-bottom">
      <!--suppress HtmlFormInputWithoutLabel -->
      <input
        class="enhanced-input"

        :class="{
          focus: isFocus,
          error: error
        }"
        :id="id"
        :placeholder="isFocus ? '' : placeholder"
        :maxlength="maxlength"

        @focus="isFocus = true"
        @blur="isFocus = false"

        v-bind="$attrs"
        v-on="listeners"
        v-model="currentValue"
      />

      <transition
        enter-active-class="animated fadeInDown faster"
        leave-active-class="animated fadeOutUp faster"
      >
        <span
          class="error"
          v-if="error"
        >
          {{ error }}
        </span>
        <span
          class="helper"
          v-else-if="isFocus && helper"
        >
          {{ helper }}
        </span>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: "BaseInput",

  inheritAttrs: false,

  props: {
    /*
     * By default, will generate unique id for each instance of the component using `this._uid`.
     */
    id: {
      type: String,
      default () {
        // noinspection JSUnresolvedVariable
        return this._uid.toString()
      },
      validator: (id) => !!id
    },

    /*
     * Used to identify an input in a form.
     * Official name used by the API for this field in the schema.
     */
    fieldName: {
      type: String,
      validator: (fieldName) => !!fieldName
    },

    /*
     * Must be extremely brief and specific.
     */
    label: {
      type: String,
      required: true,
      validator: (label) => !!label
    },

    placeholder: {
      type: String,
      default () {
        return this.label
      }
    },

    value: {
      type: String,
      default: ""
    },

    /*
     * Should only take up a single line.
     */
    helper: {
      type: String,
      default: ""
    },

    /*
     * Keep it short and preferably a single line in length.
     * Should never take up more than two lines.
     * If error is two lines long, adjust the height of the root accordingly.
     */
    error: {
      type: String,
      default: ""
    },

    maxlength: {
      type: Number,
      default: Number.POSITIVE_INFINITY,
      validator (num) {
        return num === Number.POSITIVE_INFINITY || (Number.isInteger(num) && num >= 0)
      }
    },

    size: {
      type: Number,
      default: 15,
      validator: (num) => Number.isFinite(num) && num >= 0
    }
  },

  data () {
    return {
      currentValue: this.value,
      isFocus: false
    }
  },

  computed: {
    currentLength () {
      return this.currentValue.length
    },

    /**
     * Used to attach all event listeners to the `<input/>` instead of the root node.
     * The `input` listener ensures that the parent component can still use `v-model`.
     */
    listeners () {
      return {
        ...this.$listeners,
        input: () => {
          this.$emit("input", this.currentValue)
        }
      }
    }
  },

  watch: {
    value (newValue) {
      this.currentValue = newValue
    }
  }
}
</script>

<style lang="scss" scoped>
/*
 * v-show & v-if don't preserve space when they hide elements which makes content jump.
 * To prevent this, a minimum height is added and everything below the label is fixed to the bottom of the root.
 * `visibility: hidden` would be a better way to go, but that wouldn't allow for transition animations.
 * https://github.com/vuejs/vue/issues/2382
 */
.input-root {
  display: inline-block;
  min-height: 5.2em;
  min-width: 15em;
  margin: 5px;
  position: relative;

  .fix-to-bottom {
    position: absolute;
    top: 1em; // accounts for the height of the label.
    width: 100%;
  }
}

%input-assistance {
  display: block;
  font-size: 14px;
  color: $theme-silver;

  &.error {
    color: $theme-red;
  }
}

%capitalize {
  text-transform: capitalize;
}

.floating-label {
  @extend %input-assistance;
  @extend %capitalize;

  float: left;
  padding: {
    left: 2px;
    right: 2px;
  }
  transition: color .3s ease-in-out;

  &.focus:not(.error) {
    color: $theme-blue;
  }
}

.maxlength {
  @extend %input-assistance;

  float: right;
}

.enhanced-input {
  box-shadow: none;
  appearance: none;
  outline: none;

  border-radius: 0;
  border: none;
  border-bottom: 2px solid $foreground-color;
  transition: border-bottom-color .3s ease-in-out;

  width: 100%;
  padding: 10px 2px;
  background-color: $background-color;
  color: $foreground-color;

  &:disabled {
    border-bottom-style: dotted;
  }

  &::placeholder {
    @extend %capitalize;
  }

  &.focus {
    border-bottom-color: $theme-blue;
  }

  &.error {
    border-bottom-color: $theme-red;
  }
}

.fix-to-bottom span {
  @extend %input-assistance;

  &.error, &.helper {
    margin: 5px 0;
  }

  &.error:before {
    content: "\26A0\fe0e"; // ⚠️
    color: $theme-red;
  }
}
</style>
