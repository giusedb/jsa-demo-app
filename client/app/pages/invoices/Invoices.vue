<script lang="ts">
import {defineComponent} from 'vue'
import { RecordSet } from 'jsalchemy';
import newInvoice from "~/pages/invoices/newInvoice.vue";

export default defineComponent({
  name: "InvoiceList",
  components: { RecordSet },
  methods: {
    newInvoice() {
      navigateTo('/invoices/newInvoice')
    }
  }
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <div class="flex row justify-between">
        <h2>List of invoices</h2>
        <u-button size="lg" label="new" @click="newInvoice"/>
      </div>
    </template>
    <p>The following is a full list of invoices, click any of them to see the details</p>
    <record-set resource="Invoice" >
      <template #default="{ records, total }">
        <ul>
          <li v-for="invoice in records">
            {{ invoice.id }}
          </li>
        </ul>
      </template>
    </record-set>
  </u-card>
</template>

<style scoped>

</style>