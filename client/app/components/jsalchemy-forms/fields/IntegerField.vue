<script>
import WidgetBase from "./WidgetBase.vue";

export default {
  extends: WidgetBase,
  props: {
    modelValue: {type: [Number, null], default: null},
  },
  methods: {
    checkKey(evt) {
      if (['KeyE', 'Period'].includes(evt.code)) {
        evt.preventDefault();
      }
    },
  }
}
</script>

<template>
  <UInputNumber v-if="editable"
                v-model="form.val[field.name]"
                @keydown="checkKey"/>
  <div v-else class="text-secondary">
    {{ val }}
  </div>
</template>

<style scoped>

</style>
