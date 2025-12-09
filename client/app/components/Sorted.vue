<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Sorted",
  inject: {orm},
  props: {
    recordSet: { type: Object, required: true },
    initSorted: { type: String, default: null },
  },
  data() {
    return {
      sorted: null,
      records: [],
      touch: 0,
    }
  },
  computed: {
    sorteds() {
      const x = this.touch;
      return Object.keys(this.recordSet.sortedPks);
    },
    pages() {
      const x = this.touch;
      if (!this.recordSet.resource) { return [] }
      if (!(this.sorted in this.recordSet.sortedPks))
        return [];
      const pages = this.recordSet.sortedPks[this.sorted].idPages;
      const incomplete = this.recordSet.sortedPks[this.sorted].incompletePages;
      const pkIndex = this.recordSet.resMan.collections[this.recordSet.resource.name].pkIndex.idx;
      return Object.entries(pages).map(([p, ids]) => {
        return {
          page: parseInt(p),
          incomplete: incomplete.has(parseInt(p)),
          records: ids.map(x => {
            return {
              pk: x,
              collected: x in pkIndex,
            }
          })
        }
      });
    },
    pendings() {
      const x = this.touch;
      if (!(this.sorted in this.recordSet.sortedPks))
        return [];
      const items = this.recordSet.sortedPks[this.sorted].pendings;
      const keys = Object.keys(items).sort((a, b) => {
        return items[a].minPage - items[b].minPage;
      });
      return keys.map(key => {
        return {
          pk: key,
          min: `[${items[key].minPage}, ${items[key].min}]`,
          max: `[${items[key].maxPage}, ${items[key].max}]`,
        }
      });
    }
  },
  mounted() {
    this.recordSet.on('records', (recs, total) => {
      this.records = recs;
      console.log(recs);
      this.touch ++;
    });
    this.recordSet.on('refresh', () => {
      this.touch ++;
    });
    if (this.initSorted) {
      this.sorted = this.initSorted;
    }
  }
})
</script>

<template>
  <template v-if="recordSet">
    <div class="flex justify-between w-full">
      <u-form-field label="Select the sorting model to moitor">
        <u-badge v-for="s in sorteds" :key="s"
                 :label="s" :color="s === sorted ? 'primary' : 'secondary'"
                  @click="sorted = s"/>
      </u-form-field>
      <div>{{ sorted }}</div>
    </div>
    <div class="flex justify-between">
    <div>
      <h4>Items</h4>
      <table class="pages">
        <tbody>
          <tr v-for="page in pages">
            <th class="w-10">
              <strong :class="page.incomplete ? 'bg-error-300' : ''">{{ page.page }} </strong>
            </th>
            <td v-for="rec in page.records" class="id-cell" :class="rec.collected ? 'bg-success-700' : 'bg-error-700'">
              {{ rec.pk }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div>
      <h5>Pending items</h5>
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>min</th>
            <th>max</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in pendings">
            <th>{{ p.pk }}</th>
            <td>{{ p.min }}</td>
            <td>{{ p.max}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </template>
</template>

<style scoped>
.id-cell {
  width: 20px;
  font-size: small;
  border-radius: 5px;
  border: 1px solid #c0c0c050;
}
</style>