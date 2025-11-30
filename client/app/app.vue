<script setup>
import { orm } from '~/composables/JSAlchemy';
provide('orm', orm);

const toast = useToast();
orm.on('error-json', (data, status, url, payload, request) => {
  toast.add({
    title: `${data.message} connecting to "${url}"`,
    color: 'error',
    description: `AJAX error ${status} with payload ${JSON.stringify(payload)}`,
    icon: 'i-line-md-alert'})
});
orm.on('error', (message) => {
  console.error(message);
  toast.add({
    title: "Error occurred",
    color: 'error',
    description: `details: ${message}`,
    icon: 'i-line-md-alert'});
});
global.orm = orm;
global.toast = toast;

</script>

<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtLayout>
      <NuxtPage ref="page"/>
      <UToaster />
    </NuxtLayout>
  </div>
</template>
