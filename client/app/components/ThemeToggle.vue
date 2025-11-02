<script setup lang="ts">
const colorMode = useColorMode()

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
}
const icon = computed(() => {
  if (colorMode.value === 'dark')
    return 'i-mdi-white-balance-sunny'
  return 'i-mdi-weather-night'
})
</script>

<template>
  <u-button
    variant="link"
    :icon="icon"
    class="theme-toggle"
    :title="colorMode.value === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
    @click="toggleTheme">
  </u-button>
</template>