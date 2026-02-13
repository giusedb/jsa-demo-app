<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "InvoiceList"
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h2>List of invoices</h2>
    </template>
    <p>The following is a full list of invoices, click any of them to see the details</p>
  </u-card>
</template>

<style scoped>

</style>