/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
        '144': '36rem',
      },
      screens: {
        'xs': '475px',
      },
    },
  },
  plugins: [
    // Custom component plugin for form widgets
    function({ addComponents, theme }) {
      addComponents({
        // Layout components
        '.layout-container': {
          '@apply min-h-screen bg-gray-50 dark:bg-gray-900': {},
        },
        '.layout-sidebar': {
          '@apply w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700': {},
        },
        '.layout-main': {
          '@apply flex-1 flex flex-col': {},
        },

        // Card components
        '.card': {
          '@apply bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6': {},
        },
        '.card-header': {
          '@apply border-b border-gray-200 dark:border-gray-700 pb-4 mb-4': {},
        },
        '.card-body': {
          '@apply flex-1': {},
        },
        '.card-footer': {
          '@apply border-t border-gray-200 dark:border-gray-700 pt-4 mt-4': {},
        },

        // Badge components
        '.badge': {
          '@apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium': {},
        },
        '.badge-primary': {
          '@apply bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200': {},
        },
        '.badge-success': {
          '@apply bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': {},
        },
        '.badge-warning': {
          '@apply bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200': {},
        },
        '.badge-danger': {
          '@apply bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200': {},
        },

        // Modal components
        '.modal-overlay': {
          '@apply fixed inset-0 bg-black bg-opacity-50 z-40': {},
        },
        '.modal-container': {
          '@apply fixed inset-0 z-50 flex items-center justify-center p-4': {},
        },
        '.modal-content': {
          '@apply bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto': {},
        },
        '.modal-header': {
          '@apply border-b border-gray-200 dark:border-gray-700 p-6': {},
        },
        '.modal-body': {
          '@apply p-6': {},
        },
        '.modal-footer': {
          '@apply border-t border-gray-200 dark:border-gray-700 p-6 flex justify-end space-x-3': {},
        },

        // Form components - Full viewport size
        '.form-container': {
          '@apply w-full h-full min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900': {},
        },
        '.form-card': {
          '@apply w-full max-w-2xl bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8': {},
        },
        '.form-group': {
          '@apply mb-6': {},
        },
        '.form-label': {
          '@apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2': {},
        },

        // Form widgets - Full width within form
        '.form-input': {
          '@apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white': {},
        },
        '.form-textarea': {
          '@apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white min-h-[120px]': {},
        },
        '.form-select': {
          '@apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white': {},
        },
        '.form-checkbox': {
          '@apply h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded': {},
        },
        '.form-radio': {
          '@apply h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600': {},
        },

        // Button components
        '.btn': {
          '@apply inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed': {},
        },
        '.btn-primary': {
          '@apply bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500': {},
        },
        '.btn-secondary': {
          '@apply bg-gray-600 hover:bg-gray-700 text-white focus:ring-gray-500': {},
        },
        '.btn-outline': {
          '@apply border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700': {},
        },
      })
    },
  ],
}