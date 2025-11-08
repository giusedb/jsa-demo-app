<script>
import WidgetBase from "@/jsalchemy-forms/fields/WidgetBase.vue";

export default {
  extends: WidgetBase,
  computed: {
    items() {
      return _(this.field.choices)
        .map(c => {
          if (typeof c === 'string') {
            return {text: c, value: c}
          } else if (typeof c === 'number') {
            return {text: "" + c, value: c};
          } else if (typeof c === 'object') {
            if (['text', 'value'].every(x => x in c)) {
              return c;
            } else {
              return {value: c, text: c.toString()};
            }
          }
          return c;
        })
        .value()
    },
  }
}
</script>

<template>
<!--  <div>form.val: {{ form.val[field.name]}}</div>-->
<!--  <div>val: {{ val }}</div>-->
<!--  <div>modelValue: {{ modelValue }}</div>-->
<!--  <div>Items: {{ items }}</div>-->

  <select v-if="editable"
          v-model="val"
          class="form-control" >
    <option v-for="item in items" :key="item.text"
      :value="item.value">
      {{ item.text }}
    </option>
  </select>
  <div v-else class="text-secondary">{{ val }} </div>

</template>

<style scoped>

</style>
