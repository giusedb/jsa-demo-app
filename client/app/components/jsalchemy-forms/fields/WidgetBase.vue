<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  inject: ['form'],
  props: {
    modelValue: { type: [Number, String, Object, null], mandatory: true },
    field: { type: Object, mandatory: true },
    isEdit: { type: Boolean, mandatory: true},
    onInput(value) {
      this.$emit('input', this.field.name, value);
    },
  },
  data() {
    return {
      val: null,
    }
  },
  computed: {
    editable() {
      return this.form && this.form.val && this.isEdit
    },
  },
  methods: {
    parseInput(value) {
      return value;
    },
    parseOutput(value) {
      return value;
    }
  },
  watch: {
    modelValue(newVal) {
      newVal = this.parseInput(newVal);
      // if (newVal !== this.val)
        this.val = newVal;
    },
    val(newVal) {
      newVal = this.parseOutput(newVal)
      // if (newVal !== this.val)
        this.form.updateValue(this.field.name, newVal);
    },
  },
  mounted() {
    this.val = this.parseInput(this.modelValue);
    this.$emit('mounted', this.field.name);
  },
  emits: ['update', 'mounted'],
});
</script>

<template>
  <h4>Please extend this widget</h4>
</template>

<style scoped>

</style>
