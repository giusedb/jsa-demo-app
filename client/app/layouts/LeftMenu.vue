<script setup lang="ts">
</script>

<template>
  <div>
    <u-header title="JSAlchemy">
      <template #left>
        <main-menu />
      </template>
      <template #right>
        <theme-toggle />
        <profile-menu />
      </template>
    </u-header>
    <div class="grid grid-cols-12 border-r-1 border-gray-200">
      <div class="col-span-3">
        <ul class="list">
          <li><a href="/">Home</a></li>
          <li><a href="/todos">Todos</a></li>
        </ul>
      </div>
      <dev class="col-span-9">
        <slot/>
      </dev>
    </div>
  </div>
</template>

<style scoped></style>
