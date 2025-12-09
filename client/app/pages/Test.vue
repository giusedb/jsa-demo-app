<script lang="ts">
import {defineComponent} from 'vue'

let recSet = null;

async function cippa() {
  const titles = ['Bravo', 'Foxthrot', 'Alfa', 'Romeo', 'Mike', 'Charlie', 'Stan', 'Vodka', 'Rhum', 'Hotel'];
  const descriptions = ['D2', 'D5', 'D9', 'D4', 'D3', 'D6', 'D1', 'D8', 'D9', 'DA'];

  const Model = await orm.getModel('Todo');

  _(titles).zip(descriptions).forEach(async ([title, description]) => {
    const item = new Model({ title, description});
    console.log(await item.$save());
  });
}
global.cippa = cippa;

global.destroy = async () => {
  const recSet = new RecordSet(orm.resources, 'Todo', {}, { rpp: 200 });
  recSet.on('records', (recs, total) => {
    orm.delete(...recs);
  });
}

export default defineComponent({
  name: "Test",
  inject: { orm },
  data() {
    return {
      records: [],
      filter: {
        title: '',
      },
      sort: 'title',
      page: 1,
      touch: 0,
      recSet: null,
    }
  },
  computed: {
    pendings () {
      const cippa = this.touch;
      if (recSet)
        return recSet.sortedPks['|title'].idPages
      return {}
    },
    collected() {
      const x = this.touch;
      if (!recSet) {
        return {}
      }
      const pkIndex = this.orm.resources.collections.Todo.pkIndex.idx;
      return Object.fromEntries(Object.entries(recSet.sortedPks['|title'].idPages)
          .map(([p, ids]) =>
              [p, ids.map(id => id in pkIndex ? 'X' : '-')]));
    },
    pages() {
      return _.range(1, 20)
    }
  },
  watch: {
    sort(val) {
      recSet.sort = [val];
    },
    page(val) {
      recSet.page = val;
    }
  },
  mounted() {
    recSet = new RecordSet(this.orm.resources, 'Todo', {}, { rpp: 3, sort: ['title']});
    this.recSet = recSet;
    recSet.on('records', (recs, total) => {
      this.records.length = 0;
      this.records.push(...recs);
      this.totalCount = total;
      this.touch++;
    });
    global.rs = recSet;
  }
})
</script>

<template>
  <div class="w-full">
    <h2>Test playground</h2>
    <p>
      Use this page for testing components and features you need to make before making them in
      an effective component.
    </p>
    <u-card class="border border-gray-700">
      <div class="grid grid-cols-2">
        <div class="">
          <table>
            <tbody>
            <tr>
              <td>TotalCount</td>
              <td class="text-teal-600">{{ totalCount }}</td>
            </tr>
            <tr>
              <td>records</td>
              <td>{{ records.length }}</td>
            </tr>
            <tr>
              <td>Sort by</td>
              <td class="w-fit">
                <u-select v-model="sort" :items="['id', 'title', 'description', 'completed', '~id', '~title']"
                          class="w-full"/>
              </td>
            </tr>
            <tr>
              <td>Page</td>
              <td class="w-fit">
                <u-badge v-for="p in pages" :key="p"
                         :variant="p % 3 === 1 ? 'outline' : 'solid'"
                         :label="p" :color="p === page ? 'primary' : 'secondary'"
                         @click="page = p"/>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
        <div class="col-span-1">
          <sorted v-if="recSet" :record-set="recSet" init-sorted="|title"/>
        </div>
      </div>
    </u-card>
    <u-card >
      <template #header>
        <h3>Records</h3>
      </template>
      <u-page-list ref="list" v-if="records.length">
        <u-card v-for="record in records" :key="record?.id">
          <div class="flex justify-between">
            <div>
              {{ record?.title }} ({{ record?.id }})
            </div>
            <u-button @click="record.$delete()"
                      variant="subtle"
                      icon="i-mdi-delete"
                      color="error">Delete</u-button>
          </div>

        </u-card>
      </u-page-list>
    </u-card>
  </div>
</template>

<style scoped>

</style>