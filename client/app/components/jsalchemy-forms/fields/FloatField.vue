<script>
import WidgetBase from "@/jsalchemy-forms/fields/WidgetBase.vue";

export default {
  extends: WidgetBase,
}
</script>

<template>
  <input v-if="editable" v-model="form.val[field.name]"
         @keydown="checkKey"
         type="number" :name="field.name"
         class="form-control"
         :class="form.firstSubmit && field.name in form.errors ? 'field-error' : ''">
  <div v-else class="text-secondary">
    {{ val }}
  </div>
</template>

<style scoped>

</style>
