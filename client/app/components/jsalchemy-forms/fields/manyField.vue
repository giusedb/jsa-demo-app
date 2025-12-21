<script lang="ts">
import {defineComponent} from 'vue'
import WidgetBase from "../fields/WidgetBase.vue";
import _ from "lodash";
import JsonTable from "~/components/JsonTable.vue";

export default defineComponent({
  name: "MultiReferenceField",
  components: {JsonTable},
  emits: ['update:modelValue'],
  extends: WidgetBase,
  inject: ['modelForm'],
  data() {
    return {
      refs: null,
      calledRefs: false,
      focusItem: null,
      selected: [],
      initialSelection: [],
    }
  },
  computed: {
    orm() {
      if (!this.modelForm) { return undefined}
      return this.modelForm.orm;
    },
    obj () {
      return this.form.val
    },
    val() {
      return this.obj[this.field.attribute];
    },
    allItems() {
      if (!this.refs) {
        this.loadReference();
        return [];
      }
      return this.refs;
    },
    items() {
      return this.selected.map(x => this.idxRef[x]);
    },
    idxRef() {
      if (!this.allItems.length) return {};
      return this.pkIndex.idx;
    },
    pkIndex() {
      return this.orm.resources.collections[this.field.resource].pkIndex
    },
    nonSelectedItems() {
      return this.allItems.filter(x =>
        !this.selected.includes(this.pkIndex.getKey(x)))
    },
    formStatus() {
      return this.form.status;
    }
  },
  methods: {
    async loadReference() {
      if (!this.orm) { return [] }
      this.refs = await this.orm.query(this.field.resource, {});
      this.calledRefs = true;
      const linked = await this.form.val[_.camelCase('get ' + this.field.attribute)]()
      this.selected.push(...linked.map(x => this.pkIndex.getKey(x)));
      this.initialSelection.push(...this.selected);
    },
    addSelection() {
      if (this.selected === null) { return }
      const key = this.pkIndex.getKey(this.focusItem);
      if (!this.selected.includes(key)) {
        this.selected.push(key)
      }
      this.$emit('update:modelValue', this.selected);
    },
    removeSelection(ref) {
      const key = this.pkIndex.getKey(ref);
      const i = this.selected.indexOf(key);
      if (i !== -1) {
        this.selected.splice(i, 1);
      }
      this.$emit('update:modelValue', this.selected);
    },
    afterSubmit() {
      alert(JSON.stringify(this.selected));
    }
  },
});
</script>

<template>
  <div class="form-control">
    <span v-if="items && items.length"
          v-for="item in items" :key="item.id"
          class="btn btn-sm btn-secondary" >
      <span>{{ item }}</span>
      <button class="badge rounded-pill bg-danger"
              @click="removeSelection(item)">X</button>
    </span>
    <span v-else>
      empty
    </span>
  </div>
  <div class="row">
    <div class="col-12">
      <select v-model="focusItem" class="form-control col-8" @change="addSelection">
        <option :value="null">No value</option>
        <option v-for="item in nonSelectedItems" :key="item.id"
                :value="item">{{ item }}</option>
      </select>
    </div>
  </div>
</template>

<style scoped>

</style>
