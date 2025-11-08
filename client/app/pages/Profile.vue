<script lang="ts">
import { ContentRenderer} from "#components";

export default defineComponent({
  name: "Profile",
  components: { ContentRenderer },
})
</script>

<template>
  <u-container>
    <u-card title="Profile" icon="i-mdi-account">
      <template #header>
        <h3>{{ orm.user.first_name }} {{ orm.user.last_name }}&apos;s profile</h3>
      </template>
      <u-avatar text="SA" :size="'2xl'"/>
      <div class="grid grid-cols-4">
        <div class="p-2 col-span-1"><i>First Name</i></div>
        <div class="p-2 col-span-3"><b>{{ orm.user.first_name }}</b></div>
        <div class="p-2 col-span-1"><i>Last Name</i></div>
        <div class="p-2 col-span-3"><b>{{ orm.user.last_name }}</b></div>
        <div class="p-2 col-span-1"><i>Email</i></div>
        <div class="p-2 col-span-3"><b>{{ orm.user.email }}</b></div>
      </div>
      <hr  class="border-2 border-gray-700">
    </u-card>
  </u-container>
</template>

<style scoped></style>
