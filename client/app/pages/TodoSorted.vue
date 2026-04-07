<script lang="ts">
import { RecordSet } from 'jsalchemy'
export default defineComponent({
  components: { RecordSet },
  inject: ['orm'],
  data() {
    const availableSort = [
          { label: 'Title', sort: ['title'] },
          { label: 'Title Desc', sort: ['~title'] },
          { label: 'Id', sort: ['id'] },
          { label: 'Id Desc', sort: ['~id'] },];
    return {
      todo: {
        title: '',
        description: '',
      },
      selectedSort: availableSort[0],
      availableSort,
      rpp: 20,
      touch: 0,
    }
  },
  methods: {
    async add() {
      const Todo = await this.orm.getModel('Todo');
      const todo = new Todo(this.todo);
      todo.$save();
      this.todo.title = '';
    }
  },
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h2>Todo list with sorting</h2>
      <p>
        In addition to the previous example this adds the ability to sort the list of todos by title or id, either
        ascending and discending
      </p>
    </template>
    <div class="w-full flex justify-between p-1">
      <label for="name"><h6>Todo:</h6></label>
      <div class="w-full me-3">
        <u-input v-model="todo.title" class="mx-2 w-full" @keydown.enter="add"/>
      </div>
      <u-button label="Add a Todo" icon="i-mdi-paper-plane" variant="outline" color="secondary"
                @click="add"/>
    </div>
    <record-set resource="Todo" :sort="selectedSort.sort">
      <template #default="{records, total }">
        <u-card class="p-2">
          <template #header>
            <div class="flex w-full justify-between">
              <h5>Items: {{ total }}</h5>
              <UFieldGroup class="cursor-pointer">
                <u-badge v-for="sort in availableSort"
                         :variant="selectedSort === sort ? 'solid' : 'subtle'"
                         @click="selectedSort = sort">
                  {{ sort.label }}
                </u-badge>
              </UFieldGroup>
            </div>
          </template>
          <ul>
            <li v-for="todo in records" :key="todo.id"
                class="w-full flex justify-between">
              <div>{{ todo.title }}</div>
              <u-button label="delete" color="error"
                        icon="i-mdi-delete" variant="subtle"
                        @click="todo.$delete()"/>
            </li>
          </ul>
        </u-card>
      </template>
    </record-set>
  </u-card>
</template>

<style scoped>

</style>