<script lang="ts">
import { RecordSet } from 'jsalchemy'
export default defineComponent({
  components: { RecordSet },
  inject: ['orm'],
  data() {
    const availableSort = [
          { label: 'Title', sort: ['title'] },
          { label: 'Id', sort: ['id'] },
          { label: 'Id Desc', sort: ['~id'] },];
    return {
      todo: {
        title: '',
        description: '',
      },
      selectedSort: availableSort[0],
      availableSort,
      rpp: 5,
      page: 1,
      touch: 0,
    }
  },
  computed: {
    pgItems(): [string, number][] {
      const x = this.touch;
      try {
        return [...orm.resources.collections.Todo.pagers.get('').pagers.entries()
            .map(([k, x]) => [k, x.pages.get(1).length])]
      } catch (e) {
        return []
      }
    },
    pgUnplaced(): [string, number][] {
      const x = this.touch;
      try {
        return [...orm.resources.collections.Todo.pagers.get('').pagers.entries()
            .map(([k, x]) => [k, x.unplacedItems.length])]
      } catch (e) {
        return [];
      }
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
  mounted(): any {
    this.orm.on('updated-Todo', () => this.touch++);
    this.orm.on('deleted-Todo', () => this.touch++);
    this.orm.on('new-Todo', () => this.touch++);
  }
})
</script>

<template>
  <u-card class="w-full">
    <div class="flex">
      <table class="flex-col me-2">
        <tr v-for="[k, v] in pgItems" @click="touch++">
          <td>{{ k }}</td>
          <td>{{ v }}</td>
        </tr>
      </table>
      <table class="flex-col">
        <tr v-for="[k, v] in pgUnplaced" @click="touch++">
          <td>{{ k }}</td>
          <td>{{ v }}</td>
        </tr>
      </table>
    </div>
    <template #header>
      <h2>Basic Todo App</h2>
    </template>
    <div class="w-full flex justify-between p-1">
      <div class="w-full me-3">
        <label for="name"><h6>todo:</h6></label>
        <u-input v-model="todo.title" class="mx-2 w-full" @keydown.enter="add"/>
      </div>
      <u-button label="submit" icon="i-mdi-plane" variant="subtle"
                @click="add"/>
      <div class="w-50">
        <u-select v-model="rpp" :items="[5, 10, 15, 20]" variant="subtle" />
      </div>
    </div>
    <record-set resource="Todo" :sort="selectedSort.sort" :records-per-page="rpp" :page="page">
      <template #default="{records, total }">
        <u-card class="p-2">
          <template #header>
            <div class="flex w-full justify-between">
              <h5>Items: {{ total }}</h5>
              <u-pagination v-if="total > rpp" :total="total"
                            v-model:page="page" :sibling-count="2" :items-per-page="rpp"/>
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