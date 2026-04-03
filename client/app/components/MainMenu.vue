<script setup lang="ts">
import { inject } from 'vue';

const orm: Orm = inject('orm');
const isLoggedIn = ref(false);

const componentsMenu = [
  { label: 'Tests', href: '/tests', icon: 'i-icon-park-outline-experiment'},
  { label: 'Todos', children: [
    { label: 'Basic', href: '/todoBasic', icon: 'i-mdi-format-list-checks'},
    { label: 'Sorted', href: '/todoSorted', icon: 'tdesign-order-descending'},
    { label: 'Paginated', href: '/todoPaginated', icon: 'lineicons:pagination'},
    { label: 'Multi fields', href: '/todoForm', icon: 'material-symbols-format-align-center-rounded'},
    { label: 'Filtered', href: '/todoFiltered', icon: 'material-symbols-filter-alt-sharp'},
  ]}
  // {label: 'Invoices', icon: 'i-mdi-apple', children: [
  //     { label: 'Providers', description: 'Manage the providers for this demo',
  //       icon: 'i-ion-business-sharp', href: '/invoices/providers'},
  //     { label: 'Invoices', description: 'Manage all invoices regardless of the providers',
  //      icon: 'i-ion-invoice-arrow-left', href: '/invoices/invoices'}
  //   ]},
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
