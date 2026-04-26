<script setup lang="ts">
import { inject } from 'vue';

const orm: Orm = inject('orm');
const isLoggedIn = ref(false);

const componentsMenu = [
  { label: 'Tests', href: '/tests', icon: 'i-icon-park-outline-experiment'},
  { label: 'Todos', children: [
    { label: 'Basic', href: '/todoBasic', icon: 'i-mdi-format-list-checks',
      description: 'Basic Todo screen'},
    { label: 'Sorted', href: '/todoSorted', icon: 'tdesign-order-descending',
      description: 'Sortable todo screen'},
    { label: 'Paginated', href: '/todoPaginated', icon: 'lineicons:pagination',
      description: 'Paginated todo screen with 10 items per page'},
    { label: 'Multi fields', href: '/todoForm', icon: 'material-symbols-format-align-center-rounded',
      description: 'Todo screen with multiple fields'},
    { label: 'Filtered', href: '/todoFiltered', icon: 'material-symbols-filter-alt-sharp',
      description: 'Fully functional Todo screen with filters sorting, pagination etc...'},
    { label: 'DoubleSided', href: '/todoDoubleSided', icon: 'material-symbols-filter-alt-sharp',
      description: 'Page split for 2 states of Todos'},
  ]},
  {label: 'Invoices', icon: 'i-mdi-apple', children: [
      { label: 'Providers', description: 'Manage the providers for this demo',
        icon: 'i-ion-business-sharp', href: '/invoices/providers'},
      { label: 'Invoices', description: 'Manage all invoices regardless of the providers',
       icon: 'i-ion-invoice-arrow-left', href: '/invoices/invoices'}
    ]},
  { label: 'File Systen emulation', icon: 'vaadin-harddrive',
    description: 'Fyle system emulation',
    children: [
      { label: 'Mount points', icon: 'vaadin-harddrive', href: '/file-system/mountpoints',
        description: 'list all mount points available'}
    ]}
  // {label: 'Playground', href: '/test', icon: 'i-material-symbols-playground-2-outline-rounded'},
]

const identifiedMenu = [
  {label: 'Profile', action: () => orm.logout() , icon: 'i-mdi-account'},
  {label: 'Logout', icon: 'i-mdi-logout', onClick: () => orm.logout()},
]

const anonymousMenu = [
  {label: 'Login', href: '/login', icon: 'i-mdi-login'},
  {label: 'Register', href: '/register', icon: 'i-mdi-account-plus'}
]

const userMenu = computed(() => {
  if (orm.user) {
    return identifiedMenu
  } else {
    return anonymousMenu
  }
});

const mainMenu = computed(() => {
  const menu = [{label: 'Home', href: '/', icon: 'i-mdi-home'}];
  if (orm.user) {
    menu.push(...componentsMenu);
  }
  return menu;
});

onMounted(() => {
  const loginRequired = [];
  for (const item of componentsMenu) {
    if (item.children) {
      for (const child of item.children) {
        loginRequired.push(child.href);
      }
    }
    loginRequired.push(item.href)
  }
  const requireLogin = loginRequired.includes(window.location.pathname);
  if (!orm.user && requireLogin) {
    navigateTo('/login');
  }
})

</script>

<template>
    <u-header title="JSAlchemy">
      <template #left>
        <u-navigation-menu :items="mainMenu"/>
      </template>
      <template #right>
        <theme-toggle />
        <u-navigation-menu :items="userMenu" />
      </template>
    </u-header>
</template>

<style scoped></style>
