<script>
import WidgetBase from "@/jsalchemy-forms/fields/WidgetBase.vue";

export default {
  extends: WidgetBase
}
</script>

<template>
<!--  <div>form.val: {{ form.val[field.name]}}</div>-->
<!--  <div>val: {{ val }}</div>-->
<!--  <div>modelValue: {{ modelValue }}</div>-->

  <input v-if="editable"
         v-model="val"
         type="text"
         class="form-control"
         maxlength="1"
         :class="field.name in form.errors ? 'field-error' : ''">
  <div v-else class="text-secondary">{{ val }} </div>
</template>

<style scoped>

</style>
