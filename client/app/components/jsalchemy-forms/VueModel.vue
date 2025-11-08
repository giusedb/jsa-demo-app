<script>
import { _ } from 'lodash'

import StringField from "@/jsalchemy-forms/fields/StringField.vue";
import {defineAsyncComponent} from "vue";
import JsonTable from "~/components/JsonTable.vue";

export default {
  components: {JsonTable},
  props: {
    modelValue: { type: Object },
    model: { type: String, mandatory: true },
    new: { type: Boolean, default: false },
    layout: { type: String, default: 'Default' },
    readOnly: { type: Boolean, default: false },
    editSwitch: { type: Boolean, default: false },
    fields: { "type": Array, "default": [] },
    title: {type: [String, null], default: null },
    actionUrl: { type: [String, null], default: null },
    waitForParent: { type: Boolean, default: false },
    parentErrors: { type: Object, default: () => {return {}}},
  },
  data() {
    return {
      cls: null,
      val: null,
      toggleEdit: false,
      touchError: 0,
      firstSubmit: false,
      status: 'loading',
      mountedWidgets: new Set(),
    };
  },
  computed: {
    isEdit() {
      if (this.readOnly) {
        return false;
      }
      if (this.editSwitch) {
        return this.toggleEdit;
      }
      return true;
    },
    widgets() {
      const resolveComponentType = (field) => {
        if (field.widget) {
          try {
            return defineAsyncComponent(() => import(`./fields/${field.widget}Field.vue`), {pippo: 10})
          } catch (err) {
            return StringField
          }
        }
      }
      return Object.fromEntries(_(this.fields)
        .map(field => [field.name, resolveComponentType(field)]));
    },
    readOnlyFields() {
      return new Set(_(this.fields)
        .filter(field => field.readOnly)
        .map('name'));
    },
    editableFields() {
      if (!this.isEdit) {
        return new Set();
      }
      return new Set(_(this.fields)
        .map('name')
        .filter(name => !this.readOnlyFields.has(name)))
    },
    validators() {
      if (this.fields && this.fields.length) {
        const ret = _(this.fields)
            .filter('validate')
            .map(x => [x.name, Array.isArray(x.validate) ? x.validate : [x.validate]])
          .value();
        return ret;
      }
      return {};
    },
    errors() {
      const x = this.touchError;
      if (!this.val) { return {}}
      const localErrors = Object.fromEntries(_(this.validators)
        .map(([name, validators]) => [name,
          validators.map(validate => {
            try {
              return validate(this.val[name], this.val);
            } catch (error) {
              console.warn('Validator ', validate, 'failed due to', error);
            }
          })
            .filter(Boolean)])
        .filter(x => x[1].length)
      );
      _(this.parentErrors).entries().forEach(([name, errors]) => {
        if (!(name in localErrors)) {
          localErrors[name] = [];
        }
        if (typeof errors === 'array') {
          localErrors[name].push(...errors);
        } else {
          localErrors[name].push(errors);
        }
      });
      return localErrors
    },
    topError() {
      if (Object.keys(this.errors).length) {
        return 'There is a basic validation error see the details below';
      }
      return null
    },
    serverWaiting() {
      return this.status == 'sending' || this.waitForParent;
    },
    layoutComponent() {
      return defineAsyncComponent(() => import(`./layouts/${this.layout}Layout.vue`));
    }
  },
  methods: {
    async submit(evt) {
      evt.preventDefault();
      this.firstSubmit = true;
      this.status = 'submitting';
      this.$emit('beforeSubmit', this.val);
      let res = null;
      if (this.actionUrl) {
        console.warn(`TODO POST: ${JSON.stringify(this.val)}`);
      }
      this.status = 'submitted'
      if (res) {
        this.$emit('afterSubmit', res);
        this.init();
      } else {
        this.$emit('validation', res);
      }
      if (!this.topError) {
        this.init();
        this.toggleEdit = false;
        this.status = 'show'
      }
    },
    edit() {
      this.toggleEdit = true;
      this.status = 'edit';
      this.$emit('edit');
    },
    cancel(silent) {
      this.init();
      this.toggleEdit = false;
      this.status = 'show'
      this.$emit('cancel');
    },
    updateValue(fieldName, value) {
      this.val[fieldName] = value;
      setTimeout(() => {this.touchError ++;});
    },
    loadLayout() {
      return defineAsyncComponent(() => import(`./layouts/${this.layout}Layout.vue`));
    },
    onWidgetMounted(name) {
      this.mountedWidgets.add(name);
      if (this.mountedWidgets.size === this.fields.length) {
        // TODO improvve the focus with the widgets
        const widget = this.widgets[this.fields[0].name];
        setTimeout(() => {
          this.$el.parentElement.querySelector('input,textarea,select').focus();
        },100);
        this.$emit('mounted');
      }
    },
    init() {
      if (this.new || !this.modelValue) {
        this.val = Object.fromEntries(_(this.fields).map('name').map(x => [x, null]));
      } else if (this.modelValue) {
        this.val = Object.assign({}, this.modelValue);
      }
    },
  },
  mounted() {
    this.init();
    this.status = 'show';
  },
  watch: {
    modelValue(val) {
      this.val = val;
    },
    val(newVal) {
      this.$emit('update:modelValue', this.val);
    }
  },
  provide() {
    return {
      form: this,
    }
  },
  emits: ['beforeSubmit', 'afterSubmit', 'validation', 'edit', 'cancel', 'update:modelValue', 'mounted'],
}
</script>

<template>
  <div v-if="serverWaiting" class="progress-container">
    <div class="progress-bar">
      <div class="progress-bar-value"></div>
    </div>
  </div>
  <component :is="layoutComponent"/>
</template>

<style scoped>
  .shadow {
    box-shadow: 0px 4px 15px #00000050;
    border-radius: 15px;
  }
</style>