<script lang="ts">
import {defineComponent} from 'vue'
import { Orm } from "jsalchemy";
import {parseInt} from "lodash";

export default defineComponent({
  name: "Provider.vue",
  inject: {
    orm: { type: Orm },
  },
  data() {
    return {
      providerId: null,
      provider: null,
    }
  },
  methods: {
    openAll() {
      this.provider.invoices.items.forEach(i => i.open = true);
    }
  },
  mounted() {
    const route = useRoute()
    this.providerId = parseInt(route.params.id);
    console.log('Orm', this.orm);
    (async () => {
      this.provider = await this.orm.get('Provider', this.providerId);
    })();
  }
})
</script>

<template>
  <u-card class="w-full" v-if="provider">
    <template #header>
      <div class="flex justify-between">
        <div>
          <h3>
            {{ provider.name }}
          </h3>
          <h6>
            {{ provider.address }}
          </h6>
        </div>
        <u-button icon="material-symbols-folder-open" label="Open all" @click="openAll"/>
      </div>
    </template>
    <h4>Invoices</h4>
    <u-card v-for="invoice in provider.invoices.items">
      <template #header>
        <h5 class="w-full flex justify-between"
            @click.prevent="invoice.open = !invoice.open">
          <div>{{ invoice.number }}</div>
          <div>
            <number :num="invoice.total_amount" force-decimals/> &euro;
            <u-icon :name="invoice.open ? 'material-symbols-folder-open' : 'material-symbols-folder'" class="ms-3"/>
            <u-button icon="material-symbols-edit"
                      color="info"
                      variant="outline"
                      class="ms-3"
                      @click.prevent="navigateTo('/invoices/' + invoice.id)"/>
          </div>
        </h5>
      </template>
      <template #default v-if="invoice.open">
        <div  class="w-full">
          <div v-if="invoice.lines.items" v-for="line in invoice.lines.items" :key="line.id"
               class="grid grid-cols-8">
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
        </div>
      </template>
    </u-card>
  </u-card>
  <div v-else>
    ... loading ...
  </div>
</template>

<style scoped>

</style>