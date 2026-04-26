<script lang="ts">
import {defineComponent} from 'vue'
import { Orm } from "jsalchemy";
import {parseInt} from "lodash";

export default defineComponent({
  name: "invoiceDetail",
  inject: {
    orm: { type: Orm },
  },
  data() {
    return {
      invoiceId: null,
      invoice: null,
      edit: false,
    }
  },
  mounted() {
    const route = useRoute()
    this.invoiceId = parseInt(route.params.id);
    console.log('Orm', this.orm);
    (async () => {
      this.invoice = await this.orm.get('Invoice', this.invoiceId);
    })();
  }
})
</script>

<template>
  <u-card class="w-full" v-if="invoice">
    <template #header>
      <h3 class="flex justify-between">
        <span>
          {{ invoice.number }}
          from {{ invoice.provider?.name }}
          <span class="text-end">
            {{ invoice.total_amount }}
          </span>
        </span>
        <u-button icon="material-symbols-edit" label="edit" variant="outline" color="info"/>
      </h3>
    </template>
    <div class="flext columns-8" v-for="line in invoice.lines.items">
        <div class="col-span-1 ">({{ line.id }})</div>
        <div class="col-span-4">{{ line.product }}</div>
        <div class="col-span-1 text-end">{{ line.quantity }}</div>
        <div class="col-span-1 text-end">
          <number :num="line.price" force-decimals/> &euro;
        </div>
        <div class="col-span-1 text-end">
          <number :num="line.price * line.quantity" force-decimals/> &euro;
        </div>
    </div>
  </u-card>
  <div v-else>
    ... loading ...
  </div>
</template>

<style scoped>

</style>