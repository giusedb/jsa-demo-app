<script setup lang="ts">
</script>

<template>
  <div class="h-full">
    <MainMenu />
    <div class="w-full max-w-(--ui-container) mx-auto px-4 sm:px-6 lg:px-8
                flex items-center justify-between">
        <slot/>
    </div>
    <Footer class="absolute w-full bottom-0"/>
  </div>
</template>

<style scoped></style>
