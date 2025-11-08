<script>

import WidgetBase from "./WidgetBase.vue";
import JsonTable from "~/components/JsonTable.vue";

export default {
  components: {JsonTable},
  extends: WidgetBase,
  inject: ['orm'],
  data() {
    return {
      refs: null,
      calledRefs: false,
    }
  },
  computed: {
    items() {
      if (!this.refs) {
        this.loadReference();
        if (this.calledRefs) { return [] }
      }
      return this.refs.map(x => ({
        label: x.name,
        value: x.$pk
      }));
    },
    model() {
      return this.form.$parent.cls;
    }
  },
  methods: {
    loadReference() {
      if (!this.orm) { return [] }
      this.orm.query(this.field.resource, {}).then(res => {
        this.calledRefs = true;
        this.refs = res;
      });
    }
  }
}
</script>

<template>
  <u-select v-if="editable" v-model="form.val[field.local_attribute]"
            :name="field.local_attribute"
            :items="items"
            :placeholder="field.label || field.name"
            class="w-full" />
  <template v-else>
    {{ form.val[field.attribute] }}
  </template>
</template>

<style scoped>

</style>
