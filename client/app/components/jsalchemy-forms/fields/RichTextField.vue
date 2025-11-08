<script>
import WidgetBase from "@/jsalchemy-forms/fields/WidgetBase.vue";

export default {
  extends: WidgetBase,
  props: {
    modelValue: { type: String, default: ''},
  }
}
</script>

<template>
  <textarea v-if="editable"
            v-model="val"
            :placeholder="field.label || field.name"
            class="form-control"
            :class="field.name in form.errors ? 'field-error' : ''" />
  <div v-else class="text-secondary">{{ val }} </div>
</template>

<style scoped>

</style>
