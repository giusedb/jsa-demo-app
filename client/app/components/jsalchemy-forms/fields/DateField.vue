<script>
import WidgetBase from "@/jsalchemy-forms/fields/WidgetBase.vue";

export default {
  extends: WidgetBase,
  methods: {
    parseInput(value) {
      if (value)
        return JSON.stringify(value).substring(1, 11);
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
           type="date"
           class="form-control"
           :class="field.name in form.errors ? 'field-error' : ''">
  <div v-else class="text-secondary">{{ val }} </div>
</template>

<style scoped>

</style>
