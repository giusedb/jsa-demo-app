<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "JsonTable",
  props: {
    modelValue: {type: Object},
  },
  data() {
    return {
      colors: {
        String: 'black',
        Number: 'red',
        Boolean: 'green',
        Date: 'blue'
      }
    }
  }
})
</script>

<template>
  <table class="table table-responsive table-bordered">
    <tr v-for="(value, key) in modelValue" :key="key">
      <th>
        {{ key }}
      </th>
      <td :style="{ color: colors[value?.constructor.name] }">
        <template v-if="typeof value === 'object'">
          <JsonTable :modelValue="value"/>
        </template>
        <template v-else>
          {{ value }}
        </template>
      </td>
    </tr>
  </table>
</template>

<style scoped>

</style>
