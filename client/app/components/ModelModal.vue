<script lang="ts">
import ModelForm from "~/components/jsalchemy-forms/ModelForm.vue";

export default defineComponent({
  components: {ModelForm},
  data() {
    return {
      closeFunc: null,
    }
  },
  methods: {
    close() {
      this.$attrs.modal.close();
    },
  },
  provide() {
    return {
      modal: this,
    }
  },
});
</script>

<template>
  <UModal :dismissible="true" ref="uModal"
          :close="{ onClick: close }">
    <template #header>
      {{ $attrs.title || $attrs.model }}
    </template>
    <template #body>
      <model-form layout="Modal" v-bind="$attrs"/>
    </template>
    <template #footer="{ close }" @mounted="setClose(close)">
      <div id="modal-buttons">
        <slot name="buttons"></slot>
      </div>
    </template>
  </UModal>
</template>

<style scoped></style>
