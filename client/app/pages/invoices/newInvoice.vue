<script lang="ts">
import {defineComponent} from 'vue'
const lineFields = ['product', 'quantity', 'price'];

export default defineComponent({
  name: "newInvoice",
  inject: ['orm'],
  data() {
    return {
      ready: false,
      invoice: null,
      providers: null,
      lines: [],
      Line: null,
      touch: 0,
    }
  },
  computed: {
    providerItems() {
      const x = this.touch;
      return this.providers.map(p => { return {value: p.id, label: p.name }});
    }
  },
  methods: {
    newLine() {
      this.lines.push(new this.Line({}));
    },
    tryAdd() {
      if (this.lines.every(x => lineFields.every(f => x[f]))) {
        this.newLine();
      }
    },
    async completeInvoice() {
      await this.invoice.$save();
      this.lines.forEach(line => line.invoice_id = this.invoice.id);
      if (await this.orm.saveBulk(this.lines.filter(x => lineFields.every(f => x[f])))) {
        navigateTo('/invoices/invoices')
      }
    }
  },
  async mounted() {
    const Invoice = await orm.getModel('Invoice');
    this.invoice = new Invoice({});
    const providers = await this.orm.query('Provider', {});
    this.providers = await providers.fetch()
    this.Line = await this.orm.getModel('Line');
    this.newLine();
    this.ready = true;
    this.orm.on('got-data', () => {
      this.touch ++;
      this.$forceUpdate();
      console.log('Got data and refresh UI')
    })
  }
})
</script>

<template>
  <u-page-card class="w-full">
    <template #header>
      <h3>New invoice</h3>
    </template>
    <template v-if="ready">
      <u-form-field label="Provider">
        <u-select v-model="invoice.provider_id" :items="providerItems" class="w-full"/>
      </u-form-field>
      <u-form-field label="Number">
        <u-input v-model="invoice.number" class="w-full" />
      </u-form-field>
      <u-card class="w-full">
        <template #header>
          <h3>Lines</h3>
        </template>
        <u-form v-for="line in lines" class="grid grid-cols-8 ">
          <u-form-field label="Product" class="col-span-6 me-2">
            <u-input v-model="line.product" class="w-full" placeholder="Pizza for breakfast" />
          </u-form-field>
          <u-form-field label="Quantity" class="col me-2">
            <u-input v-model="line.quantity" placeholder="1" type="number"/>
          </u-form-field>
          <u-form-field label="Euros" class="col">
            <u-input v-model="line.price" placeholder="3" type="number"
                     @keydown.tab="tryAdd" />
          </u-form-field>
        </u-form>
        <div class="flex flex-row justify-end mt-2">
          <u-button variant="subtle" label="Complete the invoice"
                    icon="lets-icons-done-fill"
                    @click="completeInvoice" />
        </div>
      </u-card>
    </template>
  </u-page-card>
</template>

<style scoped>

</style>