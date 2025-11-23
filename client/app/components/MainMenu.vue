<script setup lang="ts">
import { inject } from 'vue';

const orm = inject('orm');

const componentsMenu = [
  {label: 'Todos', href: '/todos', icon: 'i-mdi-format-list-checks'},
  {label: 'Playground', href: '/test', icon: 'i-material-symbols-playground-2-outline-rounded'}
]

const identifiedMenu = [
  {label: 'Profile', href: '/profile', icon: 'i-mdi-account'},
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
  const requireLogin = componentsMenu.map(x => x.href)
  if (!orm.user && requireLogin.includes(window.location.pathname)) {
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
