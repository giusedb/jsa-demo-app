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
      todo: {
        title: '',
        description: '',
        completed: false
      }
    }
  },
  methods: {
    async addTodo() {
      const Todo = await this.orm.getModel('Todo')
      const todo = new Todo(Object.assign({}, this.todo));
      await todo.$save();
    },
    edit(todo) {
      this.todo = todo;
    }
  }
})
</script>

<template>
  <record-set resource="Todo" :filter="{}">
    <template #default="{ records }">
      <u-card class="w-full">
        <template #header>
          <h2>Todos</h2>
        </template>
        <div class="grid grid-cols-2">
          <u-form class="col-span-1">
            <div class="grid grid-cols-2">
              <u-input v-model="todo.title" label="Title" icon="i-mdi-format-title"
                       class="col-span-2" placeholder="Title"/>
              <u-input v-model="todo.description" label="Description" icon="i-mdi-format-text"
                       class="col-span-2" placeholder="Description"/>
    <!--          <u-checkbox v-model="todo.completed" label="Completed" />-->
            </div>
            <u-button variant="subtle" icon="i-mdi-plus" @click="addTodo">Add Todo</u-button>
          </u-form>
          <u-page-list title="Todos" class="col-span-1">
            <u-page-card v-for="todo in records"
                         :title="todo.title"
                         :description="todo.description"
                         icon="todo.completed ? 'i-line-md-square-to-confirm-square-transition' : 'i-line-md-square'" >
              <template #footer>
                <div class="flex justify-between">
                  <div>
                  </div>
                  <div>
                    <u-button variant="subtle" icon="i-mdi-delete" @click="todo.$delete()"></u-button>
                    <u-button variant="subtle" icon="i-mdi-pencil" @click="edit(todo)"></u-button>
                  </div>
                </div>
              </template>
            </u-page-card>
          </u-page-list>
        </div>
      </u-card>
    </template>
  </record-set>
</template>

<style scoped></style>
