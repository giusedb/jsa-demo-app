<script>
import WidgetBase from "./WidgetBase.vue";

export default {
  extends: WidgetBase,
  methods: {
    parseInput(value) {
      if (value)
        return JSON.stringify(new Date(value.getTime() - value.getTimezoneOffset() * 60000)).substring(1,17);
      return null;
    },
    parseOutput(value) {
      if (value) {
        return new Date(value)
      }
      return null;
    }
  }
}
</script>

<template>
<!--  <div>form.val: {{ form.val[field.name]}}</div>-->
<!--  <div>val: {{ val }}</div>-->
<!--  <div>modelValue: {{ modelValue }}</div>-->

  <input v-if="editable"
           v-model="val"
           type="datetime-local"
           class="form-control"
           :class="field.name in form.errors ? 'field-error' : ''">
  <div v-else class="text-secondary">{{ modelValue }} </div>
</template>

<style scoped>

</style>
