<script>
import JsonTable from "../../JsonTable.vue";
import WidgetBase from "./WidgetBase.vue";

export default {
  components: {JsonTable},
  extends: WidgetBase,
  props: {
    modelValue: {type: String, default: ''},
  }
}
</script>

<template>
  <u-input v-if="editable"
           v-model="val"
           class="w-full"
           :placeholder="field.label || field.name"/>
  <div v-else class="text-secondary">{{ val }} </div>
</template>

<style scoped>

</style>
