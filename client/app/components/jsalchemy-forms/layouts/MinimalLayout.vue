<script lang="ts">
import {defineComponent} from 'vue'
import DefaultLayout from "@/jsalchemy-forms/layouts/DefaultLayout.vue";

export default defineComponent({
  name: "MinimalLayout",
  extends: DefaultLayout,
})
</script>

<template>
  <div v-if="form.serverWaiting" class="progress-container">
    <div class="progress-bar">
      <div class="progress-bar-value"></div>
    </div>
  </div>
  <div v-if="form.firstSubmit && form.topError"
       class="alert alert-danger">
    {{ form.topError }}
  </div>
  <template v-for="field in form.fields" :key="field.name">
    <div class="row">
      <strong class="col-12">
        {{ field.label || field.name }}
      </strong>
    </div>
    <component :is="form.widgets[field.name]"
               v-model="form.val[field.name]"
               :field="field"
               @update="onUpdate"
               :is-edit="form.editableFields.has(field.name)" />
    <div v-if="form.firstSubmit && field.name in form.errors"
         class="alert alert-danger p-0 ps-3">
      <div v-for="error in form.errors[field.name]" :key="error">
        {{ error }}
      </div>
    </div>
  </template>
  <div class="d-flex justify-content-between">
    <div>
      <button v-if="showCancel" class="btn btn-outline-secondary" @click="form.cancel">
        cancel
      </button>
    </div>
    <button v-if="showEdit" class="btn btn-secondary" @click="form.edit">
      Edit
    </button>
    <button v-if="showSave" type="submit" class="btn btn-primary" @click="form.submit">
      Save
    </button>
  </div>
</template>

<style scoped>

</style>
