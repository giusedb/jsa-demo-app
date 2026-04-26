<script lang="ts">
import {defineComponent} from 'vue'
import {RSet} from 'jsalchemy'

export default defineComponent({
  name: "TreeNodeTreeNode",
  props: {
    nodes: { type: [Array, RSet], required: true },
    childrenAttribute: { type: String, default: 'children' },
    childrenFunc: { type: Function, default: null },
    icons: { type: Object, default: () => ({
      open: 'vaadin-folder-open',
      closed: 'vaadin-folder'
    }) },
  },
  emits: ['select'],
  data() {
    return {
      opened: new Set(),
    }
  },
  methods: {
    toggle(node) {
      if (this.opened.has(node.$pk))
        this.opened.delete(node.$pk);
      else
        this.opened.add(node.$pk);
    },
    children(node) {
      if (this.childrenFunc) {
        return this.childrenFunc(node)
      }
      return node[this.childrenAttribute]
    }
  },
  computed: {
    openIcon() {
      return this.icons?.open || 'vaadin-folder-open';
    },
    closeIcon() {
      return this.icons?.closed || 'vaadin-folder';
    },
    items() {
      if (this.nodes instanceof RSet) {
        return this.nodes.items;
      }
      return this.nodes
    }
  },
})
</script>

<template>
  <ul v-if="items">
    <li v-for="node in items" :key="node.$pk" class="ps-2">
      <icon :name="opened.has(node.$pk) ? openIcon : closeIcon"
            @click="toggle(node)"/>
      <span @click="$emit('select', node)">
        <slot name="default" :node="node">{{ node }}</slot>
      </span>
      <tree-node v-if="opened.has(node.$pk)"
                 :nodes="children(node)"
                 @select="$emit('select', $event)">
        <template #default="{node}">
          <slot name="default" :node="node">{{ node }}</slot>
        </template>
      </tree-node>
    </li>
  </ul>
</template>

<style scoped>

</style>