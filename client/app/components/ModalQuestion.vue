<script setup lang="ts">
const props = defineProps<{
  title: string,
  message: string,
  buttons?: Array<{label: string, result?: string, icon?: string}>,
  result: Function,
}>()

const emit = defineEmits<{ close: [boolean] }>()
const close = () => {
  props.result()
  emit('close', false)
}
</script>

<template>
  <UModal :close="{ onClick: close }"
          :title="title" >
    <template #footer>
      <div class="flex justify-between">
        <u-button v-for="button in buttons" :key="button.label"
                 :icon="button.icon" class="me-4"
                 :label="button.label" @click="result(button.result)" />
      </div>
    </template>
    <template #body>
      {{ message }}
    </template>
  </UModal>
</template>
