// Composable for theme management
export const useTheme = () => {
  const colorMode = useColorMode()

  const isDark = computed(() => colorMode.value === 'dark')
  const isLight = computed(() => colorMode.value === 'light')

  const toggleTheme = () => {
    colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
  }

  const setTheme = (theme: 'light' | 'dark' | 'system') => {
    colorMode.preference = theme
  }

  return {
    colorMode,
    isDark,
    isLight,
    toggleTheme,
    setTheme
  }
}