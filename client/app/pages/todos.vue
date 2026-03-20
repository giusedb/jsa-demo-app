<script lang="ts">
import {defineComponent} from 'vue'
import { RecordSet } from 'jsalchemy'

export default defineComponent({
  name: "Todos",
  inject: { orm },
  components: {
    RecordSet
  },
  data() {
    return {
      defaultTodo: {
        title: '',
        description: '',
        completed: false,
      },
      todo: {},
      recordPerPage: 5,
      page: 1,
      recSet: null,
    }
  },
  methods: {
    async addTodo() {
      const Todo = await this.orm.getModel('Todo')
      const todo = new Todo(Object.assign({}, this.todo));
      await todo.$save();
      Object.assign(this.todo, this.defaultTodo);
      this.$refs.title.inputRef.focus();
    },
    async updateTodo() {
      await this.todo.$save();
      this.todo = Object.assign({}, this.defaultTodo);
      this.$refs.title.inputRef.focus();
    },
    edit(todo) {
      this.todo = todo.$clone();
    },
    toggleCompletion(todo) {
      todo.completed = !todo.completed;
      todo.$save();
    },
  },
  mounted(): any {
    this.todo = Object.assign({}, this.defaultTodo);
  }
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h2>Just a simple todo app</h2>
      <p>
        The purpose of this demo is to show the basic usage of JSAlchemy for simple CRUD operation
        across a simple table with no direct or indirect dependencies.
      </p>
      <p>
        Therefore there is no <i>popup</i> or any <i>modal alert</i> or any other UI element
        that is not part of the default <i>u-button</i> or <i>u-input</i> or <i>u-textarea</i>
      </p>
    </template>
    <div class="grid grid-cols-2">
      <u-form class="border-e border-e-gray-700 me-3 pe-2 col-span-1">
          <u-form-field label="Title">
            <u-input v-model="todo.title" icon="i-mdi-format-title" ref="title"
                     class="w-full" placeholder="Todo's title"/>
          </u-form-field>
          <u-form-field label="Description">
            <u-textarea v-model="todo.description" class="w-full"
                        icon="i-mdi-format-text" placeholder="Desccribe your todo here"/>
          </u-form-field>
          <u-form-field label="Completion">
            <div class="flex justify-between">
              <u-checkbox v-model="todo.completed" :label="todo.completed ? 'Completed' : 'Not completed'"/>
              <u-button v-if="todo.constructor === Object"
                        variant="subtle" icon="i-mdi-plus" label="Add Todo"
                        @click="addTodo" />
              <u-button v-else color="secondary"
                        variant="subtle" icon="i-mdi-pencil" :label="`Update ${todo.title}`"
                        @click="updateTodo" />

            </div>
          </u-form-field>
      </u-form>
      <u-page-list title="Todos" class="col-span-1">
        <record-set ref="recordSet" resource="Todo" :filter="{}" :page="page"
                    name="primary-todos"  :records-per-page="recordPerPage" :sort="['title']"
                    @recordSet="recSet = $event">
          <template #default="{ records, total, loading }">
            <u-pagination v-if="total > recordPerPage" :total="total"
                          v-model:page="page" :sibling-count="7" :items-per-page="recordPerPage"/>
            <div class="flex flex-row content-between">
              <u-form-field class="w-full">
                Records per page: <u-select v-model="recordPerPage" :items="[5, 10, 20]"/>
              </u-form-field>
            </div>
            <ul>
              <li v-for="todo in records" :key="todo.id"
                  class="flex flex-row justify-between">
                <div>{{ todo.title }}</div>
                <div>
                  <u-button icon="i-mdi-trash" variant="subtle"
                            @click="todo.$delete()"/>
                </div>
              </li>
            </ul>
          </template>
        </record-set>
      </u-page-list>
    </div>
  </u-card>
</template>

<style scoped></style>
