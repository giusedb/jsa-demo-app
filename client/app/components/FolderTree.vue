<script lang="ts">
import {defineComponent} from 'vue'
import TreeNode from './FileSystem/TreeNode.vue'

export default defineComponent({
  name: "FolderTree",
  inject: ['orm'],
  components: {
    TreeNode
  },
  props: {
    folder: {type: Object, required: true},
  },
  data() {
    const fileColumns = [
      {
        accessorKey: 'name',
        header: 'Name',
      }
    ]
    return {
      sFolder: this.folder,
      fileColumns,
      newFolderName: '',
      newFileName: '',
    }
  },
  methods: {
    children(node) {
      if (node.mounts_id) {
        return node.mounts?.root?.children
      }
      return node.children?.items
    },
    async addFolder() {
      const Folder = await this.orm.getModel('Folder');
      const folder = new Folder({name: this.newFolderName, parent_id: this.sFolder.id});
      await folder.$save();
      this.newFolderName = '';
    },
    async addFile() {
      const File = await this.orm.getModel('File');
      const file = new File({name: this.newFileName, folder_id: this.sFolder.id});
      await file.$save();
      this.newFileName = '';
    },
    async rename(item) {
      item.name = this.newFileName;
      await item.$save();
    }
  }
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <div class="w-full flex justify-between">
        <h3>Folder: {{ folder }}</h3>
        <div>
          <u-popover v-if="sFolder" model-value
                     trigger="click">
            <u-button label="New folder" icon="vaadin-folder" variant="subtle" color="secondary"/>
            <template #content>
              <u-page-card>
                <template #title>
                  <h3>Folder</h3>
                  <u-input v-model="newFolderName" placeholder="Folder name" @keyup.enter="addFolder"/>
                </template>
              </u-page-card>
            </template>
          </u-popover>
          <u-popover v-if="sFolder" model-value ref="filePopover"
                     trigger="click">
            <u-button label="New File" icon="vaadin-file-movie" variant="subtle" color="secondary"/>
            <template #content>
              <u-page-card>
                <template #title>
                  <h3>File</h3>
                  <u-input v-model="newFileName" placeholder="Create a file by name"
                           @keyup.enter="addFile"/>
                </template>
              </u-page-card>
            </template>
          </u-popover>
        </div>
      </div>
    </template>
    <div class="grid grid-cols-6 overflow-y-scroll">
      <div class="col-span-1">
        <h4>Tree</h4>
        <tree-node :nodes="folder?.children?.items"
                   :children-func="children"
                   @select="sFolder = $event">
          <template #default="{node}">
            <span :class="{'font-bold': sFolder.$pk === node.$pk}"
                  class="ps-2 cursor-pointer">
              <u-chip v-if="node.mounts_id" :label="node.mounts_id" color="error">
                {{ node }}
              </u-chip>
              <template v-else>
                {{ node }}
              </template>
            </span>
          </template>
        </tree-node>
      </div>
      <div class="col-span-5">
        <h3>Folder: {{ sFolder }}</h3>
        <div class="grid grid-cols-3">
          <div v-for="file in sFolder?.files?.items"
               class="flexjustify-between border-1 col-span-1 m-2 p-2 border-gray-300" style="border-radius: 8px;">
            <div>
              <h5><u-icon name="vaadin-file-o"/>{{ file.name}}</h5>
            </div>
            <div class="flex justify-end">
              <u-popover trigger="click">
                <u-button icon="vaadin-edit" variant="subtle" color="secondary" class="me-1" @click="newFileName = file.name"/>
                <template #content>
                  <u-page-card>
                    <template #header>
                      <h3>rename file {{ file }}</h3>
                    </template>
                    <u-input v-model="newFileName" @keyup.enter="rename(file)" />
                  </u-page-card>
                </template>
              </u-popover>
              <u-button icon="vaadin-trash" variant="subtle" color="error" @click="file.$delete()"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </u-card>
</template>

<style scoped>

</style>