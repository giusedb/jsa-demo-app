<script lang="ts">
import { RecordSet } from 'jsalchemy'
import {parseInt} from "lodash";

const route = useRoute();

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
    const availableFilters = [
      { label: 'All', filter: {}, unique: 'all'},
      { label: 'Not Completed', filter: { completed: false }, unique: 'incomplete' },
      { label: 'Completed', filter: { completed: true }, unique: 'completed' },
    ];
    return {
      todo: {
        title: '',
        description: '',
      },
      rpp: 10,
      page: 1,
      selectedSort: availableSort[0],
      availableSort,
      touch: 0,
      availableRpp: [5, 10, 20, 30, 40, 50],
      filters: availableFilters,
      filter: availableFilters[0],
      loading: true,
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
    },
    applyFilter(filter) {
      navigateTo('/todoFiltered/' + filter.unique);
      this.filter = filter;
    }
  },
  mounted() {
    const initialFilter  = route.params.initialFilter;
    const idx = this.filters.map(x => x.unique).indexOf(initialFilter);
    if (idx >= 0) {
      this.filter = this.filters[idx]
    }
    this.loading = false;
  },
})
</script>

<template>
  <u-card class="w-full" v-if="!loading">
    <template #header>
      <h2>Filtered Todo list</h2>
      <p>
        Now that you can create, delete all your todo, and also play with the completion, I think it would be nice to
        see that you can also filtere the records you see on your screen
      </p>
    </template>
    <div class="flex w-full justify-between p-1">
      <h6>Filter by completions</h6>
      <div class="w-1/2 me-3">
        <UFieldGroup class="cursor-pointer">
          <u-badge v-for="option in filters" :key="option.label"
                   :variant="filter.label === option.label ? 'solid' : 'subtle'"
                   @click="applyFilter(option)">
            {{ option.label}}
          </u-badge>
        </UFieldGroup>
      </div>
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
    <record-set resource="Todo" :sort="selectedSort.sort" :records-per-page="rpp" v-model:page="page" :filter="filter.filter">
      <template #default="{records, total, loading }">
        <u-card class="p-2">
          <template #header>
            <div class="flex w-full justify-between">
              <h5>Items: {{ total }}</h5>
              <u-pagination v-if="total > rpp" :total="total"
                            v-model:page="page" :sibling-count="2"
                            :items-per-page="rpp"/>
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
  </u-card>
</template>

<style scoped>

</style>