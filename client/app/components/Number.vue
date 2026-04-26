<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Number",
  props: {
    num: { type: Number, mandatory: true },
    decimals: { type: Number, default: 2},
    forceDecimals: {type: Boolean, default: false},
  },
  computed: {
    number() {
      const c = (10 ** this.decimals)
      const num = Math.round((this.num || 0) * c) / c;
      let x: string, y: string;
      let out = this.num?.toString();
      if (out.includes('.')) {
        [x, y] = out.split('.');
      } else {
        [x, y] = [out, ''];
      }
      if (this.forceDecimals && (y.length < this.decimals))
        y += Array.from({length: this.decimals - y.length}, () => '0').join('');
      if (y.length > this.decimals)
        y = y.substring(0, this.decimals);
      return `${x}${y.length? '.' : ''}${y}`
    }
  }
})
</script>

<template>
  <span>
    {{ number }}
  </span>
</template>

<style scoped>

</style>