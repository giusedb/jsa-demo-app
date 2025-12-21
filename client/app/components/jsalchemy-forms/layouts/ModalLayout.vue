<script>

import JsonTable from "~/components/JsonTable.vue";

export default {
  name: "DefaultLayout",
  inject: ['form', 'modal'],
  components: {JsonTable},
  computed: {
    val() {
      return this.form.val;
    },
    showEdit() {
      return this.form.editSwitch && !this.form.isEdit;
    },
    showSave() {
      return this.form.isEdit;
    },
    showCancel() {
      return this.form.isEdit;
    },
  },
  methods: {
    onUpdate(name, value) {
      this.$emit('update', name, value);
    },
    submit(evt) {
      this.form.submit(evt);
      this.modal.close();
    },
    cancel(evt) {
      console.log('layout.cancel');
      this.modal.close();
    }
  },
  emits: ['update', 'close'],
}
</script>

<template>
  <UAlert v-if="form.firstSubmit && form.topError" color="danger"
          :description="form.topError" />
  <UForm @submit.prevent="submit">
    <UFormField v-for="field in form.fields" :key="field.name"
                :label="field.label || field.name">
      <component :is="form.widgets[field.name]"
                 v-model="form.val[field.name]"
                 :field="field"
                 @update="onUpdate"
                 @mounted="form.onWidgetMounted(field.name)"
                 :is-edit="form.editableFields.has(field.name)" />
    </UFormField>
  </UForm>
  <teleport to="#modal-buttons">
    <div class="flex justify-between">
      <UButton v-if="showCancel" label="cancel"
               color="secondary" icon="i-line-md-close"
               variant="subtle"
               @click.prevent="cancel" />

      <UButton v-if="showEdit" label="edit" color="primary"
               variant="subtle"
               @click="form.edit" />

      <UButton v-if="showSave" label="save" type="submit"
               color="primary" icon="i-line-md-confirm"
               variant="subtle"
               @click="submit" />
    </div>
  </teleport>
</template>

<style scoped>
  .progress-container {
    width: 97%;
    margin: auto;
  }

  .progress-bar {
    height: 2px;
    background-color: rgba(5, 114, 206, 0.2);
    width: 100%;
    overflow: hidden;
  }

  .progress-bar-value {
    width: 100%;
    height: 100%;
    background-color: rgb(123, 83, 236);
    animation: indeterminateAnimation 1s infinite linear;
    transform-origin: 0% 50%;
  }

  @keyframes indeterminateAnimation {
    0% {
      transform:  translateX(0) scaleX(0);
    }
    40% {
      transform:  translateX(0) scaleX(0.4);
    }
    100% {
      transform:  translateX(100%) scaleX(0.5);
    }
  }

</style>
