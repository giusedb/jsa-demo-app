<script lang="ts">
import {defineComponent} from 'vue'
import VueForm from "./VueForm.vue";
import _ from 'lodash';

const referenceTypes = {
  one: 'Reference',
  m2m: 'MultiReference',
}


export default defineComponent({
  name: "ModelForm",
  components: {VueForm},
  inject: {orm: {default: null, type: "Orm"}},
  props: {
    model: {type: String },
    modelValue: { type: [Object, null], default: null},
    columns: { type: Array, default: () => null },
    defaultValue: {type: Object, default: () => { return {}}},
    readOnly: { type: Array, default: []},
    localOrm: {type: "Orm", default: null},
  },
  data() {
    return {
      cls: null,
      val: null,
      serverWaiting: false,
      validationErrors: {},
      copy: null,
    }
  },
  computed: {
    PKs() {
      return new Set(this.cls.$pk);
    },
    fields() {
      if (!this.cls) { return [] }
      let allColumns = this.columns;
      if (!allColumns) {
        allColumns = Object.keys(this.cls.fields);
        allColumns.push(...Object.keys(this.cls.references));
      }
      const ret = _(allColumns)
        .map(x => this.cls.fields[x] || this.cls.references[x])
        .filter(Boolean)
        .filter(f => !f.hidden)
        .map(field => {
          if (field.name)
            return {
              name: field.name,
              label: field.label || field.name || field.attribute,
              icon: field.icon,
              widget: field.widget || (field.type in referenceTypes ? referenceTypes[field.type] : field.type),
              readOnly: field.readonly || this.PKs.has(field.name) || this.readOnly.includes(field.name),
            }
          const fld = Object.assign({}, field);
          fld.label = field.label || field.attribute;
          fld.name = '$' + field.attribute;
          fld.readOnly = field.readOnly  || this.readOnly.includes(field.attribute);
          fld.widget = field.widget || field.type in referenceTypes ? referenceTypes[field.type] : field.type
          return fld;
        })
      return ret.value();
    },
    $orm() {
      return this.localOrm || this.orm;
    },
  },
  methods: {
    async save(obj) {
      Object.assign(this.val, obj);
      this.serverWaiting = true;
      this.validationErrors = {};
      try {
        const res = await this.val.$save();
        if (res.$validation) {
          this.validationErrors = res.$validation.errors;
          this.$emit('validation', res.$validation);
        } else {
          this.val = res;
          _(this.fields)
            .filter(x => x.type === 'm2m')
            .forEach(field =>
              this.val[_.camelCase('set ' + field.attribute)](...this.val['$' + field.attribute]));
          this.$emit('saved', this.val);
        }
      } finally {
        this.serverWaiting = false;
      }
    }
  },
  watch: {
    val(value) {
      this.copy = value;
    },
  },
  async mounted() {
    if (this.modelValue) {
      this.val = this.modelValue;
      this.cls = this.modelValue.constructor;
    } else {
      this.cls = await this.$orm.getModel(this.model);
      this.val = new this.cls(this.defaultValue || {});
    }
    this.copy = this.val;
  },
  provide() {
    return {
      modelForm: this,
    }
  },
  emits: ['saved', 'edit', 'after:leave', 'close'],
})
</script>

<template>
  <vue-form :fields="fields" v-bind="$attrs"
            v-model="copy"
            :parent-errors="validationErrors"
            :wait-for-parent="serverWaiting"
            :title="model"
            @before-submit="save"/>
</template>

<style scoped>

</style>
