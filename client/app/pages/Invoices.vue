<script lang="ts">
import {defineComponent} from "vue";
import {RecordSet} from "../../../libs/jsa-client";

export default defineComponent({
  name: "Providers",
  components: {RecordSet},
  inject: { orm },
  data() {
    return {
      selectedProvider: null,
    }
  },
  computed: {
  },
  methods: {
  }
})

</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h3>Invoice list</h3>
      <p>
        You already defined some provider, select the provider you what to see all invoices
      </p>
    </template>
    <record-set resource="Provider" >
      <template #default="{ records }">
        <ul>
          <li v-for="provider in records">
            {{ provider.name }}
          </li>
        </ul>
      </template>
    </record-set>
  </u-card>
</template>

<style scoped>

</style>