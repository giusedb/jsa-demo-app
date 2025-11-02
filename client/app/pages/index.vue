<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "index.vue",
})
</script>

<template >
  <u-page-hero title="JSAlchemy"
               orientation="horizontal"
               :links="[{label: 'Get Started', href: '/', icon: 'i-mdi-arrow-right'}]"
               headline="Demo app"
               description="SQLAlchemy and JavaScript run together" >
    <p>API-less connection to the server that effortlessly connects
    your fron-end to the backend</p>
  </u-page-hero>
</template>

<style scoped>

</style>