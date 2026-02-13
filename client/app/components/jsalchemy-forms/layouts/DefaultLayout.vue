<script>

import JsonTable from "~/components/JsonTable.vue";

export default {
  name: "DefaultLayout",
  inject: ['form'],
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
  },
  emits: ['update']
}
</script>

<template>
  <UCard>
    <template #header>
      <h3>{{ form.title }}</h3>
    </template>
    <template #default>
      <UAlert v-if="form.firstSubmit && form.topError" color="danger" :description="form.topError" />
      <UForm>
        <UFormField v-for="field in form.fields" :key="field.name" :label="field.label || field.name">
          <component :is="form.widgets[field.name]"
                     v-model="form.val[field.name]"
                     :field="field"
                     @update="onUpdate"
                     @mounted="form.onWidgetMounted(field.name)"
                     :is-edit="form.editableFields.has(field.name)" />
        </UFormField>
      </UForm>
    </template>
    <template #footer>
      <div class="flex justify-between">
        <UButton v-if="showCancel" label="cancel"
                 color="secondary" icon="i-lucide-x"
                 variant="subtle"
                 @click.prevent="form.cancel" />

        <UButton v-if="showEdit" label="edit"color="primary"
                 variant="subtle"
                 @click="form.edit" />

        <UButton v-if="showSave" label="save" type="submit"
                 color="primary" icon="i-lucide-check"
                 variant="subtle"
                 @click="form.submit" />
      </div>
    </template>
  </UCard>
  <div class="card" v-if="false">
    <div class="card-header d-flex justify-content-between">
      <h3>
        <span>{{ form.title }}</span>
      </h3>
    </div>
    <div class="card-body">
      <div class="border-1 border-primary">
        <div v-if="form.serverWaiting" class="progress-container">
          <div class="progress-bar">
            <div class="progress-bar-value"></div>
          </div>
        </div>


        <div v-for="field in form.fields" :key="field.name" class="row">
          <div class="col-5 h5 pb-4">
            <label :for="field.name">
              {{ field.label || field.name }}
            </label>
          </div>
          <div class="col-7">
            <component :is="form.widgets[field.name]"
                       v-model="form.val[field.name]"
                       :field="field"
                       @update="onUpdate"
                       @mounted="form.onWidgetMounted(field.name)"
                       :is-edit="form.editableFields.has(field.name)" />
            <div v-if="form.firstSubmit && field.name in form.errors"
                 class="alert alert-danger p-0 ps-3">
              <div v-for="error in form.errors[field.name]" :key="error">
                {{ error }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer d-flex justify-content-between">
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
    <div>
      form.val
      <json-table v-model="form.val" />
    </div>
  </div>
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
