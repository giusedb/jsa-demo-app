<script lang="ts">
import { RecordSet } from 'jsalchemy'
export default defineComponent({
  components: { RecordSet },
  inject: ['orm'],
  data() {
    return {
      todo: {
        title: '',
        description: '',
      },
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
      <h2>Basic Todo App</h2>
      <p>
        This is a very simple todo app. It's only porpuse is to showcase the simplicity of managing a list in JSAlchemy
        together with a minimal interaction such as create and delete Todos
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
    <record-set resource="Todo">
      <template #default="{records, total }">
        <u-card class="p-2">
          <template #header>
            <div class="flex w-full justify-between">
              <h5>Items: {{ total }}</h5>
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