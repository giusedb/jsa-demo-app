<script lang="ts">
import { RecordSet } from 'jsalchemy'
export default defineComponent({
  components: { RecordSet },
  inject: ['orm'],
  data() {
    const availableSort = [
          { label: 'Title', sort: ['title'] },
          { label: 'Title Desc', sort: ['~title'] },
          { label: 'Description', sort: ['description'] },
          { label: 'Decription Desc', sort: ['~description'] },
          { label: 'Id', sort: ['id'] },
          { label: 'Id Desc', sort: ['~id'] },];
    return {
      todo: {
        title: '',
        description: '',
      },
      rpp: 50,
      page: 1,
      selectedSort: {
        incompleted: availableSort[0],
        completed: availableSort[0],
      },
      availableSort,
      touch: 0,
      availableRpp: [5, 10, 20, 30, 40, 50],
    }
  },
  methods: {
    async add() {
      const Todo = await this.orm.getModel('Todo');
      const todo = new Todo(this.todo);
      await todo.$save();
      this.todo.title = '';
      this.todo.description = '';
      await this.$refs.title.focus();
    },
    toggle(todo) {
      todo.completed = !todo.completed;
      todo.$save();
    }
  },
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h2>Double-sided Todo list</h2>
      <p>
        In this screen items are in the column based on their completion
      </p>
    </template>
    <div class="flex w-full justify-between p-1">
    </div>
    <div class="w-full flex justify-between p-1">
      <label for="name"><h6>Title</h6></label>
      <div class="w-full me-3">
        <u-input v-model="todo.title" class="mx-2 w-full" @keydown.enter="add" ref="title"/>
      </div>
    </div>
    <div class="w-full flex justify-between p-1">
      <label for="name"><h6>Description</h6></label>
      <div class="w-full me-3">
        <u-input v-model="todo.description" class="mx-2 w-full" @keydown.enter="add"/>
      </div>
      <u-button label="Add a Todo" icon="i-mdi-paper-plane" variant="outline" color="secondary"
                @click="add"/>
      <u-select v-model="rpp" :items="availableRpp" class="mx-2" />
    </div>
    <div class="flex justify-between">
      <record-set resource="Todo"
                  :sort="selectedSort.incompleted.sort"
                  :records-per-page="rpp"
                  v-model:page="page"
                  :filter="{ completed: false}">
        <template #default="{records, total, loading }">
          <u-card class="p-2">
            <template #header>
              <div class="flex w-full justify-between">
                <h5>Items: {{ total }}</h5>
                <UFieldGroup class="cursor-pointer">
                  <u-badge v-for="sort in availableSort"
                           :variant="selectedSort.incompleted === sort ? 'solid' : 'subtle'"
                           @click="selectedSort.incompleted = sort">
                    {{ sort.label }}
                  </u-badge>
                </UFieldGroup>
              </div>
            </template>
            <ul>
              <li v-for="todo in records" :key="todo.id"
                  class="w-full flex justify-between">
                <div class="flex w-full justify-between pe-3">
                  <div>{{ todo.title }}</div>
                  <div class="ro">
                    <span class="text-secondary text-sm me-3">{{ todo.description }}</span>
                    <u-icon :name="todo.completed ? 'nrk-media-completed' : 'carbon-incomplete'"
                            @click="toggle(todo)"/>
                  </div>
                </div>
                <u-button label="delete" color="error"
                          icon="i-mdi-delete" variant="subtle"
                          @click="todo.$delete()"/>
              </li>
            </ul>
          </u-card>
        </template>
      </record-set>
      <record-set resource="Todo"
                  :sort="selectedSort.completed.sort"
                  :records-per-page="rpp"
                  v-model:page="page"
                  :filter="{ completed: true}">
        <template #default="{records, total, loading }">
          <u-card class="p-2">
            <template #header>
              <div class="flex w-full justify-between">
                <h5>Items: {{ total }}</h5>
                <UFieldGroup class="cursor-pointer">
                  <u-badge v-for="sort in availableSort"
                           :variant="selectedSort.completed === sort ? 'solid' : 'subtle'"
                           @click="selectedSort.completed = sort">
                    {{ sort.label }}
                  </u-badge>
                </UFieldGroup>
              </div>
            </template>
            <ul>
              <li v-for="todo in records" :key="todo.id"
                  class="w-full flex justify-between">
                <div class="flex w-full justify-between pe-3">
                  <div>{{ todo.title }}</div>
                  <div class="ro">
                    <span class="text-secondary text-sm me-3">{{ todo.description }}</span>
                    <u-icon :name="todo.completed ? 'nrk-media-completed' : 'carbon-incomplete'"
                            @click="toggle(todo)"/>
                  </div>
                </div>
                <u-button label="delete" color="error"
                          icon="i-mdi-delete" variant="subtle"
                          @click="todo.$delete()"/>
              </li>
            </ul>
          </u-card>
        </template>
      </record-set>
    </div>
  </u-card>
</template>

<style scoped>

</style>