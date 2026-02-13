<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Providers",
  inject: { orm },
  data() {
    return {
      providers: orm
    }
  }
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h3>Provider list</h3>
      <p>
        Under the invoices menu, the demo showcases a One to Many relation among two
        DB entities and shows to interact with data without any definition of endpoint
        interaction.
      </p>
    </template>
    <ul>
      <li v-for="a of items">{{ a }}</li>
    </ul>
  </u-card>
</template>

<style scoped>

</style>