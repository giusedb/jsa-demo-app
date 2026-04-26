<script lang="ts">
import {defineComponent} from 'vue'
import { RecordSet } from 'jsalchemy';
import { getCurrentInstance } from 'vue';

export default defineComponent({
  name: "InvoiceList",
  inject: ['orm'],
  components: { RecordSet },
  data() {
    this.orm.getModel('Invoice').then(model => this.Invoice = model);
    return {
      Invoice: null,
      rpp: 10,
      page: 1,
    }
  },
  methods: {
    newInvoice() {
      navigateTo('/invoices/newInvoice')
    }
  },
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <div class="flex row justify-between">
        <h2>List of invoices</h2>
        <div>
          <u-button size="lg" label="Reset" @click="Invoice.fixture()" color="error" variant="subtle" class="me-3"/>
          <u-button size="lg" label="new" @click="newInvoice"/>
        </div>
      </div>
    </template>
    <p>The following is a full list of invoices, click any of them to see the details</p>
    <record-set resource="Invoice" v-model:page="page" :records-per-page="rpp">
      <template #default="{ records, total }">
        <div class="flex justify-between">
          <h3>There are {{ total }} invoices.</h3>
          <div>
              <u-pagination v-if="total > rpp" :total="total"
                            v-model:page="page" :sibling-count="1"
                            :items-per-page="rpp"/>
          </div>
        </div>
        <u-card v-for="invoice in records" >
          <template #header>
            <div class="flex flex-row justify-between" @click="invoice.open = !invoice.open" >
              <h3 v-if="invoice.provider">{{ invoice.provider.name }}</h3>
              <h6>
                {{ invoice.number }} -
                <number :num="invoice.total_amount" /> &euro;
                <u-icon :name="invoice.open ? 'material-symbols-folder-open' : 'material-symbols-folder'"/>
                <u-icon name="ic-round-arrow-forward" @click="navigateTo('/invoices/providers/' + invoice.provider_id)"/>
              </h6>
            </div>
          </template>
          <template #default v-if="invoice.open">
            <div  class="w-full">
              <div v-if="invoice.lines.items" v-for="line in invoice.lines.items" :key="line.id"
                   class="grid grid-cols-8">
                <div class="col-span-1 ">({{ line.id }})</div>
                <div class="col-span-4">{{ line.product }}</div>
                <div class="col-span-1 text-end">{{ line.quantity }}</div>
                <div class="col-span-1 text-end">{{ line.price }} &euro;</div>
                <div class="col-span-1 text-end">
                  <number :num="line.price * line.quantity"/> &euro;
                </div>
              </div>
            </div>
          </template>
        </u-card>
      </template>
    </record-set>
  </u-card>
</template>

<style scoped>

</style>