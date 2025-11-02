<script setup>

const toast = useToast();
orm.on('error-json', (data, status, url, payload, request) => {
  toast.add({
    title: `${data.message} connecting to "${url}"`,
    color: 'error',
    description: `AJAX error ${status} with payload ${JSON.stringify(payload)}`,
    icon: 'i-line-md-alert'})
});
global.orm = orm;
</script>

<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtLayout>
      <NuxtPage ref="page"/>
    </NuxtLayout>
  </div>
</template>
